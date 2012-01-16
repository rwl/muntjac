# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

"""Defines a class representing a selection of items the user has selected
in a UI."""

from warnings import warn

from muntjac.event import field_events
from muntjac.data.util.filter.simple_string_filter import SimpleStringFilter
from muntjac.data.container import IContainer, IFilterable, IIndexed
from muntjac.ui import abstract_select

from muntjac.event.field_events import \
    FocusEvent, BlurEvent, IBlurListener, IFocusListener


class Select(abstract_select.AbstractSelect, abstract_select.IFiltering,
             field_events.IBlurNotifier, field_events.IFocusNotifier):
    """A class representing a selection of items the user has selected in a
    UI. The set of choices is presented as a set of L{IItem}s in a
    L{IContainer}.

    A C{Select} component may be in single- or multiselect mode.
    Multiselect mode means that more than one item can be selected
    simultaneously.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    CLIENT_WIDGET = None #ClientWidget(VFilterSelect, LoadStyle.LAZY)

    def __init__(self, *args):
        #: Holds value of property pageLength. 0 disables paging.
        self.pageLength = 10

        self._columns = 0

        #: Current page when the user is 'paging' trough options
        self._currentPage = -1

        self._filteringMode = self.FILTERINGMODE_STARTSWITH

        self._filterstring = None
        self._prevfilterstring = None

        #: Number of options that pass the filter, excluding the null
        #  item if any.
        self._filteredSize = None

        #: Cache of filtered options, used only by the in-memory
        #  filtering system.
        self._filteredOptions = None

        #: Flag to indicate that request repaint is called by filter
        #  request only
        self._optionRequest = None

        #: True if the container is being filtered temporarily and item
        #  set change notifications should be suppressed.
        self._filteringContainer = None

        #: Flag to indicate whether to scroll the selected item visible
        #  (select the page on which it is) when opening the popup or not.
        #  Only applies to single select mode.
        #
        #  This requires finding the index of the item, which can be expensive
        #  in many large lazy loading containers.
        self._scrollToSelectedItem = True

        nargs = len(args)
        if nargs == 0:
            super(Select, self).__init__()
        elif nargs == 1:
            caption, = args
            super(Select, self).__init__(caption)
        elif nargs == 2:
            if isinstance(args[1], IContainer):
                caption, dataSource = args
                super(Select, self).__init__(caption, dataSource)
            else:
                caption, options = args
                super(Select, self).__init__(caption, options)
        else:
            raise ValueError, 'too many arguments'


    def paintContent(self, target):
        """Paints the content of this component.

        @param target:
                   the Paint Event.
        @raise PaintException:
                    if the paint operation failed.
        """
        if self.isMultiSelect():
            # background compatibility hack. This object shouldn't be used for
            # multiselect lists anymore (ListSelect instead). This fallbacks to
            # a simpler paint method in super class.
            super(Select, self).paintContent(target)
            # Fix for #4553
            target.addAttribute('type', 'legacy-multi')
            return

        # clear caption change listeners
        self.getCaptionChangeListener().clear()

        # The tab ordering number
        if self.getTabIndex() != 0:
            target.addAttribute('tabindex', self.getTabIndex())

        # If the field is modified, but not committed, set modified attribute
        if self.isModified():
            target.addAttribute('modified', True)

        # Adds the required attribute
        if self.isRequired():
            target.addAttribute('required', True)

        if self.isNewItemsAllowed():
            target.addAttribute('allownewitem', True)

        needNullSelectOption = False
        if self.isNullSelectionAllowed():
            target.addAttribute('nullselect', True)
            needNullSelectOption = self.getNullSelectionItemId() is None
            if not needNullSelectOption:
                target.addAttribute('nullselectitem', True)

        # Constructs selected keys array
        if self.isMultiSelect():
            selectedKeys = [None] * len(self.getValue())
        elif self.getValue() is None and self.getNullSelectionItemId() is None:
            selectedKeys = []
        else:
            selectedKeys = [None]

        target.addAttribute('pagelength', self.pageLength)

        target.addAttribute('filteringmode', self.getFilteringMode())

        # Paints the options and create array of selected id keys
        keyIndex = 0

        target.startTag('options')

        if self._currentPage < 0:
            self._optionRequest = False
            self._currentPage = 0
            self._filterstring = ''

        nullFilteredOut = ((self._filterstring is not None)
                and (self._filterstring != '')
                and (self._filteringMode != self.FILTERINGMODE_OFF))
        # null option is needed and not filtered out, even if not on current
        # page
        nullOptionVisible = needNullSelectOption and not nullFilteredOut

        # first try if using container filters is possible
        options = self.getOptionsWithFilter(nullOptionVisible)
        if None is options:
            # not able to use container filters, perform explicit
            # in-memory filtering
            options = self.getFilteredOptions()
            self._filteredSize = len(options)
            options = self.sanitetizeList(options, nullOptionVisible)

        paintNullSelection = (needNullSelectOption and (self._currentPage == 0)
                and (not nullFilteredOut))

        if paintNullSelection:
            target.startTag('so')
            target.addAttribute('caption', '')
            target.addAttribute('key', '')
            target.endTag('so')

        i = iter(options)
        # Paints the available selection options from data source
        while True:
            try:
                idd = i.next()

                if ((not self.isNullSelectionAllowed())
                        and (idd is not None)
                        and (idd == self.getNullSelectionItemId())
                        and (not self.isSelected(idd))):
                    continue

                # Gets the option attribute values
                key = self.itemIdMapper.key(idd)
                caption = self.getItemCaption(idd)
                icon = self.getItemIcon(idd)
                self.getCaptionChangeListener().addNotifierForItem(idd)

                # Paints the option
                target.startTag('so')
                if icon is not None:
                    target.addAttribute('icon', icon)

                target.addAttribute('caption', caption)
                if (idd is not None) and idd == self.getNullSelectionItemId():
                    target.addAttribute('nullselection', True)

                target.addAttribute('key', key)
                if self.isSelected(idd) and (keyIndex < len(selectedKeys)):
                    target.addAttribute('selected', True)
                    selectedKeys[keyIndex] = key
                    keyIndex += 1

                target.endTag('so')
            except StopIteration:
                break
        target.endTag('options')

        target.addAttribute('totalitems', (len(self)
                + (1 if needNullSelectOption else 0)))

        if (self._filteredSize > 0) or nullOptionVisible:
            target.addAttribute('totalMatches', (self._filteredSize
                    + (1 if nullOptionVisible else 0)))

        # Paint variables
        target.addVariable(self, 'selected', selectedKeys)
        if self.isNewItemsAllowed():
            target.addVariable(self, 'newitem', '')

        target.addVariable(self, 'filter', self._filterstring)
        target.addVariable(self, 'page', self._currentPage)

        self._currentPage = -1  # current page is always set by client

        self._optionRequest = True

        # Hide the error indicator if needed
        if self.shouldHideErrors():
            target.addAttribute('hideErrors', True)


    def getOptionsWithFilter(self, needNullSelectOption):
        """Returns the filtered options for the current page using a container
        filter.

        As a size effect, L{filteredSize} is set to the total number of
        items passing the filter.

        The current container must be L{IFilterable} and L{IIndexed},
        and the filtering mode must be suitable for container filtering
        (tested with L{canUseContainerFilter}).

        Use L{getFilteredOptions} and L{sanitetizeList} if this is not the
        case.

        @param needNullSelectOption:
        @return: filtered list of options (may be empty) or null if cannot use
                 container filters
        """
        container = self.getContainerDataSource()

        if self.pageLength == 0:
            # no paging: return all items
            self._filteredSize = len(container)
            return list(container.getItemIds())

        if ((not isinstance(container, IFilterable))
                or (not isinstance(container, IIndexed))
                or (self.getItemCaptionMode() !=
                        self.ITEM_CAPTION_MODE_PROPERTY)):
            return None

        filterable = container

        fltr = self.buildFilter(self._filterstring, self._filteringMode)

        # adding and removing filters leads to extraneous item set
        # change events from the underlying container, but the ComboBox does
        # not process or propagate them based on the flag filteringContainer
        if fltr is not None:
            self._filteringContainer = True
            filterable.addContainerFilter(fltr)

        indexed = container

        indexToEnsureInView = -1

        # if not an option request (item list when user changes page), go
        # to page with the selected item after filtering if accepted by
        # filter
        selection = self.getValue()
        if (self.isScrollToSelectedItem() and (not self._optionRequest)
                and (not self.isMultiSelect()) and (selection is not None)):
            # ensure proper page
            indexToEnsureInView = indexed.indexOfId(selection)

        self._filteredSize = len(container)
        self._currentPage = self.adjustCurrentPage(self._currentPage,
                needNullSelectOption, indexToEnsureInView, self._filteredSize)
        first = self.getFirstItemIndexOnCurrentPage(needNullSelectOption,
                self._filteredSize)
        last = self.getLastItemIndexOnCurrentPage(needNullSelectOption,
                self._filteredSize, first)

        options = list()
        i = first
        while (i <= last) and (i < self._filteredSize):
            options.append( indexed.getIdByIndex(i) )
            i += 1

        # to the outside, filtering should not be visible
        if fltr is not None:
            filterable.removeContainerFilter(fltr)
            self._filteringContainer = False

        return options


    def buildFilter(self, filterString, filteringMode):
        """Constructs a filter instance to use when using a IFilterable
        container in the C{ITEM_CAPTION_MODE_PROPERTY} mode.

        Note that the client side implementation expects the filter string to
        apply to the item caption string it sees, so changing the behavior of
        this method can cause problems.
        """
        fltr = None
        if filterString is not None and filterString != '':
            test = filteringMode
            if test == self.FILTERINGMODE_OFF:
                pass
            elif test == self.FILTERINGMODE_STARTSWITH:
                fltr = SimpleStringFilter(self.getItemCaptionPropertyId(),
                        filterString, True, True)
            elif test == self.FILTERINGMODE_CONTAINS:
                fltr = SimpleStringFilter(self.getItemCaptionPropertyId(),
                        filterString, True, False)
        return fltr


    def containerItemSetChange(self, event):
        if not self._filteringContainer:
            super(Select, self).containerItemSetChange(event)


    def sanitetizeList(self, options, needNullSelectOption):
        """Makes correct sublist of given list of options.

        If paint is not an option request (affected by page or filter change),
        page will be the one where possible selection exists.

        Detects proper first and last item in list to return right page of
        options. Also, if the current page is beyond the end of the list, it
        will be adjusted.

        @param options:
        @param needNullSelectOption:
                   flag to indicate if nullselect option needs to be taken
                   into consideration
        """
        if (self.pageLength != 0) and (len(options) > self.pageLength):

            indexToEnsureInView = -1

            # if not an option request (item list when user changes page), go
            # to page with the selected item after filtering if accepted by
            # filter
            selection = self.getValue()
            if (self.isScrollToSelectedItem() and (not self._optionRequest)
                    and (not self.isMultiSelect())
                    and (selection is not None)):
                # ensure proper page
                try:
                    indexToEnsureInView = options.index(selection)
                except ValueError:
                    indexToEnsureInView = -1

            size = len(options)
            self._currentPage = self.adjustCurrentPage(self._currentPage,
                    needNullSelectOption, indexToEnsureInView, size)
            first = self.getFirstItemIndexOnCurrentPage(needNullSelectOption,
                    size)
            last = self.getLastItemIndexOnCurrentPage(needNullSelectOption,
                    size, first)
            return options[first:last + 1]
        else:
            return options


    def getFirstItemIndexOnCurrentPage(self, needNullSelectOption, size):
        """Returns the index of the first item on the current page. The index
        is to the underlying (possibly filtered) contents. The null item, if
        any, does not have an index but takes up a slot on the first page.

        @param needNullSelectOption:
                   true if a null option should be shown before any other
                   options (takes up the first slot on the first page, not
                   counted in index)
        @param size:
                   number of items after filtering (not including the null
                   item, if any)
        @return: first item to show on the UI (index to the filtered list of
                 options, not taking the null item into consideration if any)
        """
        # Not all options are visible, find out which ones are on the
        # current "page".
        first = self._currentPage * self.pageLength
        if needNullSelectOption and (self._currentPage > 0):
            first -= 1
        return first


    def getLastItemIndexOnCurrentPage(self, needNullSelectOption, size, first):
        """Returns the index of the last item on the current page. The index
        is to the underlying (possibly filtered) contents. If
        needNullSelectOption is true, the null item takes up the first slot
        on the first page, effectively reducing the first page size by one.

        @param needNullSelectOption:
                   true if a null option should be shown before any other
                   options (takes up the first slot on the first page, not
                   counted in index)
        @param size:
                   number of items after filtering (not including the null
                   item, if any)
        @param first:
                   index in the filtered view of the first item of the page
        @return: index in the filtered view of the last item on the page
        """
        # page length usable for non-null items
        if needNullSelectOption and (self._currentPage == 0):
            effectivePageLength = self.pageLength - 1
        else:
            effectivePageLength = self.pageLength

        return min(size - 1, (first + effectivePageLength) - 1)


    def adjustCurrentPage(self, page, needNullSelectOption,
                indexToEnsureInView, size):
        """Adjusts the index of the current page if necessary: make sure the
        current page is not after the end of the contents, and optionally go
        to the page containing a specific item. There are no side effects but
        the adjusted page index is returned.

        @param page:
                   page number to use as the starting point
        @param needNullSelectOption:
                   true if a null option should be shown before any other
                   options (takes up the first slot on the first page, not
                   counted in index)
        @param indexToEnsureInView:
                   index of an item that should be included on the page (in
                   the data set, not counting the null item if any), -1 for
                   none
        @param size:
                   number of items after filtering (not including the null
                   item, if any)
        """
        if indexToEnsureInView != -1:
            if needNullSelectOption:
                newPage = (indexToEnsureInView + 1) / self.pageLength
            else:
                newPage = indexToEnsureInView / self.pageLength

            page = newPage

        # adjust the current page if beyond the end of the list
        if (page * self.pageLength) > size:
            if needNullSelectOption:
                page = (size + 1) / self.pageLength
            else:
                page = size / self.pageLength

        return page


    def getFilteredOptions(self):
        """Filters the options in memory and returns the full filtered list.

        This can be less efficient than using container filters, so use
        L{getOptionsWithFilter} if possible (filterable container and suitable
        item caption mode etc.).
        """
        if ((self._filterstring is None) or (self._filterstring == '')
                or (self.FILTERINGMODE_OFF == self._filteringMode)):
            self._prevfilterstring = None
            self._filteredOptions = list(self.getItemIds())
            return self._filteredOptions

        if self._filterstring == self._prevfilterstring:
            return self._filteredOptions

        if ((self._prevfilterstring is not None)
                and self._filterstring.startswith(self._prevfilterstring)):
            items = self._filteredOptions
        else:
            items = self.getItemIds()
        self._prevfilterstring = self._filterstring

        self._filteredOptions = list()
        for itemId in items:
            caption = self.getItemCaption(itemId)
            if (caption is None) or (caption == ''):
                continue
            else:
                caption = caption.lower()

            test = self._filteringMode
            if test == self.FILTERINGMODE_CONTAINS:
                if caption.find(self._filterstring) > -1:
                    self._filteredOptions.append(itemId)
            elif test == self.FILTERINGMODE_STARTSWITH:
                pass
            else:
                if caption.startswith(self._filterstring):
                    self._filteredOptions.append(itemId)

        return self._filteredOptions


    def changeVariables(self, source, variables):
        """Invoked when the value of a variable has changed.

        @see: L{AbstractComponent.changeVariables}
        """
        # Not calling super.changeVariables due the history of select
        # component hierarchy

        # Selection change
        if 'selected' in variables:
            ka = variables.get('selected')

            if self.isMultiSelect():
                # Multiselect mode

                # TODO: Optimize by adding repaintNotNeeded when applicable

                # Converts the key-array to id-set
                s = list()
                for i in range(len(ka)):
                    idd = self.itemIdMapper.get(ka[i])
                    if (idd is not None) and self.containsId(idd):
                        s.append(idd)

                # Limits the deselection to the set of visible items
                # (non-visible items can not be deselected)
                visible = self.getVisibleItemIds()
                if visible is not None:
                    newsel = self.getValue()

                    if newsel is None:
                        newsel = set()
                    else:
                        newsel = set(newsel)

                    newsel = newsel.difference(visible)
                    newsel = newsel.union(s)

                    self.setValue(newsel, True)
            else:
                # Single select mode
                if len(ka) == 0:
                    # Allows deselection only if the deselected item is visible
                    current = self.getValue()
                    visible = self.getVisibleItemIds()

                    if (visible is not None) and (current in visible):
                        self.setValue(None, True)
                else:
                    idd = self.itemIdMapper.get(ka[0])

                    if ((idd is not None)
                            and (idd == self.getNullSelectionItemId())):
                        self.setValue(None, True)
                    else:
                        self.setValue(idd, True)

        newFilter = variables.get('filter')
        if newFilter is not None:
            # this is a filter request
            self._currentPage = int(variables.get('page'))
            self._filterstring = newFilter
            if self._filterstring is not None:
                self._filterstring = self._filterstring.lower()

            self.optionRepaint()
        elif self.isNewItemsAllowed():
            # New option entered (and it is allowed)
            newitem = variables.get('newitem')
            if (newitem is not None) and (len(newitem) > 0):
                self.getNewItemHandler().addNewItem(newitem)
                # rebuild list
                self._filterstring = None
                self._prevfilterstring = None

        if FocusEvent.EVENT_ID in variables:
            self.fireEvent( FocusEvent(self) )

        if BlurEvent.EVENT_ID in variables:
            self.fireEvent( BlurEvent(self) )


    def requestRepaint(self):
        super(Select, self).requestRepaint()
        self._optionRequest = False
        self._prevfilterstring = self._filterstring
        self._filterstring = None


    def optionRepaint(self):
        super(Select, self).requestRepaint()


    def setFilteringMode(self, filteringMode):
        self._filteringMode = filteringMode


    def getFilteringMode(self):
        return self._filteringMode


    def setColumns(self, columns):
        """Note, one should use more generic setWidth(String) method instead
        of this. This now days actually converts columns to width with em css
        unit.

        Sets the number of columns in the editor. If the number of columns is
        set 0, the actual number of displayed columns is determined implicitly
        by the adapter.

        @deprecated:

        @param columns:
                   the number of columns to set.
        """
        warn('deprecated', DeprecationWarning)

        if columns < 0:
            columns = 0

        if self._columns != columns:
            self._columns = columns
            self.setWidth(columns, Select.UNITS_EM)
            self.requestRepaint()


    def getColumns(self):
        """@deprecated: see setter function
        """
        warn('see setter function', DeprecationWarning)
        return self._columns


    def addListener(self, listener, iface=None):
        if (isinstance(listener, IBlurListener) and
                (iface is None or issubclass(iface, IBlurListener))):
            self.registerListener(BlurEvent.EVENT_ID,
                    BlurEvent, listener, IBlurListener.blurMethod)

        if (isinstance(listener, IFocusListener) and
                (iface is None or issubclass(iface, IFocusListener))):
            self.registerListener(FocusEvent.EVENT_ID,
                    FocusEvent, listener, IFocusListener.focusMethod)

        super(Select, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, BlurEvent):
            self.registerCallback(BlurEvent, callback,
                    BlurEvent.EVENT_ID, *args)

        elif issubclass(eventType, FocusEvent):
            self.registerCallback(FocusEvent, callback,
                    FocusEvent.EVENT_ID, *args)
        else:
            super(Select, self).addCallback(callback, eventType, *args)


    def removeListener(self, listener, iface=None):
        if (isinstance(listener, IBlurListener) and
                (iface is None or issubclass(iface, IBlurListener))):
            self.withdrawListener(BlurEvent.EVENT_ID, BlurEvent, listener)

        if (isinstance(listener, IFocusListener) and
                (iface is None or issubclass(iface, IFocusListener))):
            self.withdrawListener(FocusEvent.EVENT_ID, FocusEvent, listener)

        super(Select, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, BlurEvent):
            self.withdrawCallback(BlurEvent, callback, BlurEvent.EVENT_ID)

        elif issubclass(eventType, FocusEvent):
            self.withdrawCallback(FocusEvent, callback, FocusEvent.EVENT_ID)

        else:
            super(Select, self).removeCallback(callback, eventType)


    def setMultiSelect(self, multiSelect):
        """@deprecated: use L{ListSelect}, L{OptionGroup} or
                    L{TwinColSelect} instead
        @see: L{AbstractSelect.setMultiSelect}
        """
        super(Select, self).setMultiSelect(multiSelect)


    def isMultiSelect(self):
        """@deprecated: use L{ListSelect}, L{OptionGroup} or
                    L{TwinColSelect} instead

        @see: L{AbstractSelect.isMultiSelect}
        """
        return super(Select, self).isMultiSelect()


    def setScrollToSelectedItem(self, scrollToSelectedItem):
        """Sets whether to scroll the selected item visible (directly open
        the page on which it is) when opening the combo box popup or not.
        Only applies to single select mode.

        This requires finding the index of the item, which can be expensive
        in many large lazy loading containers.

        @param scrollToSelectedItem:
                   true to find the page with the selected item when opening
                   the selection popup
        """
        self._scrollToSelectedItem = scrollToSelectedItem


    def isScrollToSelectedItem(self):
        """Returns true if the select should find the page with the selected
        item when opening the popup (single select combo box only).

        @see: L{setScrollToSelectedItem}

        @return: true if the page with the selected item will be shown when
                 opening the popup
        """
        return self._scrollToSelectedItem
