# Copyright (C) 2011 Vaadin Ltd
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __pyjamas__ import (ARGERROR, POSTINC,)
from com.vaadin.event.FieldEvents import (BlurEvent, BlurListener, BlurNotifier, FieldEvents, FocusEvent, FocusListener, FocusNotifier,)
from com.vaadin.ui.AbstractSelect import (AbstractSelect,)
from com.vaadin.data.util.filter.SimpleStringFilter import (SimpleStringFilter,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Collection import (Collection,)
# from java.util.HashSet import (HashSet,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedList import (LinkedList,)
# from java.util.List import (List,)
# from java.util.Map import (Map,)
# from java.util.Set import (Set,)


class Select(AbstractSelect, AbstractSelect, Filtering, FieldEvents, BlurNotifier, FieldEvents, FocusNotifier):
    """<p>
    A class representing a selection of items the user has selected in a UI. The
    set of choices is presented as a set of {@link com.vaadin.data.Item}s in a
    {@link com.vaadin.data.Container}.
    </p>

    <p>
    A <code>Select</code> component may be in single- or multiselect mode.
    Multiselect mode means that more than one item can be selected
    simultaneously.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # Holds value of property pageLength. 0 disables paging.
    pageLength = 10
    _columns = 0
    # Current page when the user is 'paging' trough options
    _currentPage = -1
    _filteringMode = FILTERINGMODE_STARTSWITH
    _filterstring = None
    _prevfilterstring = None
    # Number of options that pass the filter, excluding the null item if any.
    _filteredSize = None
    # Cache of filtered options, used only by the in-memory filtering system.
    _filteredOptions = None
    # Flag to indicate that request repaint is called by filter request only
    _optionRequest = None
    # True if the container is being filtered temporarily and item set change
    # notifications should be suppressed.

    _filteringContainer = None
    # Flag to indicate whether to scroll the selected item visible (select the
    # page on which it is) when opening the popup or not. Only applies to
    # single select mode.
    # 
    # This requires finding the index of the item, which can be expensive in
    # many large lazy loading containers.

    _scrollToSelectedItem = True
    # Constructors
    # Component methods

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            super(Select, self)()
        elif _1 == 1:
            caption, = _0
            super(Select, self)(caption)
        elif _1 == 2:
            if isinstance(_0[1], Collection):
                caption, options = _0
                super(Select, self)(caption, options)
            else:
                caption, dataSource = _0
                super(Select, self)(caption, dataSource)
        else:
            raise ARGERROR(0, 2)

    def paintContent(self, target):
        """Paints the content of this component.

        @param target
                   the Paint Event.
        @throws PaintException
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
        else:
            selectedKeys = [None] * (0 if self.getValue() is None and self.getNullSelectionItemId() is None else 1)
        target.addAttribute('pagelength', self.pageLength)
        target.addAttribute('filteringmode', self.getFilteringMode())
        # Paints the options and create array of selected id keys
        keyIndex = 0
        target.startTag('options')
        if self._currentPage < 0:
            self._optionRequest = False
            self._currentPage = 0
            self._filterstring = ''
        nullFilteredOut = self._filterstring is not None and not ('' == self._filterstring) and self._filteringMode != self.FILTERINGMODE_OFF
        # null option is needed and not filtered out, even if not on current
        # page
        nullOptionVisible = needNullSelectOption and not nullFilteredOut
        # first try if using container filters is possible
        options = self.getOptionsWithFilter(nullOptionVisible)
        if None is options:
            # not able to use container filters, perform explicit in-memory
            # filtering
            options = self.getFilteredOptions()
            self._filteredSize = len(options)
            options = self.sanitetizeList(options, nullOptionVisible)
        paintNullSelection = needNullSelectOption and self._currentPage == 0 and not nullFilteredOut
        if paintNullSelection:
            target.startTag('so')
            target.addAttribute('caption', '')
            target.addAttribute('key', '')
            target.endTag('so')
        i = options
        # Paints the available selection options from data source
        while i.hasNext():
            id = i.next()
            if (
                not self.isNullSelectionAllowed() and id is not None and id == self.getNullSelectionItemId() and not self.isSelected(id)
            ):
                continue
            # Gets the option attribute values
            key = self.itemIdMapper.key(id)
            caption = self.getItemCaption(id)
            icon = self.getItemIcon(id)
            self.getCaptionChangeListener().addNotifierForItem(id)
            # Paints the option
            target.startTag('so')
            if icon is not None:
                target.addAttribute('icon', icon)
            target.addAttribute('caption', caption)
            if id is not None and id == self.getNullSelectionItemId():
                target.addAttribute('nullselection', True)
            target.addAttribute('key', key)
            if self.isSelected(id) and keyIndex < len(selectedKeys):
                target.addAttribute('selected', True)
                selectedKeys[POSTINC(globals(), locals(), 'keyIndex')] = key
            target.endTag('so')
        target.endTag('options')
        target.addAttribute('totalitems', len(self) + (1 if needNullSelectOption else 0))
        if (self._filteredSize > 0) or nullOptionVisible:
            target.addAttribute('totalMatches', self._filteredSize + (1 if nullOptionVisible else 0))
        # Paint variables
        target.addVariable(self, 'selected', selectedKeys)
        if self.isNewItemsAllowed():
            target.addVariable(self, 'newitem', '')
        target.addVariable(self, 'filter', self._filterstring)
        target.addVariable(self, 'page', self._currentPage)
        self._currentPage = -1
        # current page is always set by client
        self._optionRequest = True
        # Hide the error indicator if needed
        if (
            self.isRequired() and self.isEmpty() and self.getComponentError() is None and self.getErrorMessage() is not None
        ):
            target.addAttribute('hideErrors', True)

    def getOptionsWithFilter(self, needNullSelectOption):
        """Returns the filtered options for the current page using a container
        filter.

        As a size effect, {@link #filteredSize} is set to the total number of
        items passing the filter.

        The current container must be {@link Filterable} and {@link Indexed}, and
        the filtering mode must be suitable for container filtering (tested with
        {@link #canUseContainerFilter()}).

        Use {@link #getFilteredOptions()} and
        {@link #sanitetizeList(List, boolean)} if this is not the case.

        @param needNullSelectOption
        @return filtered list of options (may be empty) or null if cannot use
                container filters
        """
        container = self.getContainerDataSource()
        if self.pageLength == 0:
            # no paging: return all items
            self._filteredSize = len(container)
            return list(container.getItemIds())
        if (
            ((not isinstance(container, Filterable)) or (not isinstance(container, Indexed))) or (self.getItemCaptionMode() != self.ITEM_CAPTION_MODE_PROPERTY)
        ):
            return None
        filterable = container
        filter = self.buildFilter(self._filterstring, self._filteringMode)
        # adding and removing filters leads to extraneous item set
        # change events from the underlying container, but the ComboBox does
        # not process or propagate them based on the flag filteringContainer
        if filter is not None:
            self._filteringContainer = True
            filterable.addContainerFilter(filter)
        indexed = container
        indexToEnsureInView = -1
        # if not an option request (item list when user changes page), go
        # to page with the selected item after filtering if accepted by
        # filter
        selection = self.getValue()
        if (
            self.isScrollToSelectedItem() and not self._optionRequest and not self.isMultiSelect() and selection is not None
        ):
            # ensure proper page
            indexToEnsureInView = indexed.indexOfId(selection)
        self._filteredSize = len(container)
        self._currentPage = self.adjustCurrentPage(self._currentPage, needNullSelectOption, indexToEnsureInView, self._filteredSize)
        first = self.getFirstItemIndexOnCurrentPage(needNullSelectOption, self._filteredSize)
        last = self.getLastItemIndexOnCurrentPage(needNullSelectOption, self._filteredSize, first)
        options = list()
        _0 = True
        i = first
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i <= last and i < self._filteredSize):
                break
            options.add(indexed.getIdByIndex(i))
        # to the outside, filtering should not be visible
        if filter is not None:
            filterable.removeContainerFilter(filter)
            self._filteringContainer = False
        return options

    def buildFilter(self, filterString, filteringMode):
        """Constructs a filter instance to use when using a Filterable container in
        the <code>ITEM_CAPTION_MODE_PROPERTY</code> mode.

        Note that the client side implementation expects the filter string to
        apply to the item caption string it sees, so changing the behavior of
        this method can cause problems.

        @param filterString
        @param filteringMode
        @return
        """
        filter = None
        if None is not filterString and not ('' == filterString):
            _0 = filteringMode
            _1 = False
            while True:
                if _0 == self.FILTERINGMODE_OFF:
                    _1 = True
                    break
                if (_1 is True) or (_0 == self.FILTERINGMODE_STARTSWITH):
                    _1 = True
                    filter = SimpleStringFilter(self.getItemCaptionPropertyId(), filterString, True, True)
                    break
                if (_1 is True) or (_0 == self.FILTERINGMODE_CONTAINS):
                    _1 = True
                    filter = SimpleStringFilter(self.getItemCaptionPropertyId(), filterString, True, False)
                    break
                break
        return filter

    def containerItemSetChange(self, event):
        if not self._filteringContainer:
            super(Select, self).containerItemSetChange(event)

    def sanitetizeList(self, options, needNullSelectOption):
        """Makes correct sublist of given list of options.

        If paint is not an option request (affected by page or filter change),
        page will be the one where possible selection exists.

        Detects proper first and last item in list to return right page of
        options. Also, if the current page is beyond the end of the list, it will
        be adjusted.

        @param options
        @param needNullSelectOption
                   flag to indicate if nullselect option needs to be taken into
                   consideration
        """
        if self.pageLength != 0 and len(options) > self.pageLength:
            indexToEnsureInView = -1
            # if not an option request (item list when user changes page), go
            # to page with the selected item after filtering if accepted by
            # filter
            selection = self.getValue()
            if (
                self.isScrollToSelectedItem() and not self._optionRequest and not self.isMultiSelect() and selection is not None
            ):
                # ensure proper page
                indexToEnsureInView = options.index(selection)
            size = len(options)
            self._currentPage = self.adjustCurrentPage(self._currentPage, needNullSelectOption, indexToEnsureInView, size)
            first = self.getFirstItemIndexOnCurrentPage(needNullSelectOption, size)
            last = self.getLastItemIndexOnCurrentPage(needNullSelectOption, size, first)
            return options.subList(first, last + 1)
        else:
            return options

    def getFirstItemIndexOnCurrentPage(self, needNullSelectOption, size):
        """Returns the index of the first item on the current page. The index is to
        the underlying (possibly filtered) contents. The null item, if any, does
        not have an index but takes up a slot on the first page.

        @param needNullSelectOption
                   true if a null option should be shown before any other options
                   (takes up the first slot on the first page, not counted in
                   index)
        @param size
                   number of items after filtering (not including the null item,
                   if any)
        @return first item to show on the UI (index to the filtered list of
                options, not taking the null item into consideration if any)
        """
        # Not all options are visible, find out which ones are on the
        # current "page".
        first = self._currentPage * self.pageLength
        if needNullSelectOption and self._currentPage > 0:
            first -= 1
        return first

    def getLastItemIndexOnCurrentPage(self, needNullSelectOption, size, first):
        """Returns the index of the last item on the current page. The index is to
        the underlying (possibly filtered) contents. If needNullSelectOption is
        true, the null item takes up the first slot on the first page,
        effectively reducing the first page size by one.

        @param needNullSelectOption
                   true if a null option should be shown before any other options
                   (takes up the first slot on the first page, not counted in
                   index)
        @param size
                   number of items after filtering (not including the null item,
                   if any)
        @param first
                   index in the filtered view of the first item of the page
        @return index in the filtered view of the last item on the page
        """
        # page length usable for non-null items
        effectivePageLength = self.pageLength - (1 if needNullSelectOption and self._currentPage == 0 else 0)
        return self.Math.min(size - 1, (first + effectivePageLength) - 1)

    def adjustCurrentPage(self, page, needNullSelectOption, indexToEnsureInView, size):
        """Adjusts the index of the current page if necessary: make sure the current
        page is not after the end of the contents, and optionally go to the page
        containg a specific item. There are no side effects but the adjusted page
        index is returned.

        @param page
                   page number to use as the starting point
        @param needNullSelectOption
                   true if a null option should be shown before any other options
                   (takes up the first slot on the first page, not counted in
                   index)
        @param indexToEnsureInView
                   index of an item that should be included on the page (in the
                   data set, not counting the null item if any), -1 for none
        @param size
                   number of items after filtering (not including the null item,
                   if any)
        """
        if indexToEnsureInView != -1:
            newPage = (indexToEnsureInView + (1 if needNullSelectOption else 0)) / self.pageLength
            page = newPage
        # adjust the current page if beyond the end of the list
        if page * self.pageLength > size:
            page = (size + (1 if needNullSelectOption else 0)) / self.pageLength
        return page

    def getFilteredOptions(self):
        """Filters the options in memory and returns the full filtered list.

        This can be less efficient than using container filters, so use
        {@link #getOptionsWithFilter(boolean)} if possible (filterable container
        and suitable item caption mode etc.).

        @return
        """
        if (
            ((None is self._filterstring) or ('' == self._filterstring)) or (self.FILTERINGMODE_OFF == self._filteringMode)
        ):
            self._prevfilterstring = None
            self._filteredOptions = LinkedList(self.getItemIds())
            return self._filteredOptions
        if self._filterstring == self._prevfilterstring:
            return self._filteredOptions
        if (
            self._prevfilterstring is not None and self._filterstring.startswith(self._prevfilterstring)
        ):
            items = self._filteredOptions
        else:
            items = self.getItemIds()
        self._prevfilterstring = self._filterstring
        self._filteredOptions = LinkedList()
        _0 = True
        it = items
        while True:
            if _0 is True:
                _0 = False
            if not it.hasNext():
                break
            itemId = it.next()
            caption = self.getItemCaption(itemId)
            if (caption is None) or (caption == ''):
                continue
            else:
                caption = caption.toLowerCase()
            _1 = self._filteringMode
            _2 = False
            while True:
                if _1 == self.FILTERINGMODE_CONTAINS:
                    _2 = True
                    if caption.find(self._filterstring) > -1:
                        self._filteredOptions.add(itemId)
                    break
                if (_2 is True) or (_1 == self.FILTERINGMODE_STARTSWITH):
                    _2 = True
                if True:
                    _2 = True
                    if caption.startswith(self._filterstring):
                        self._filteredOptions.add(itemId)
                    break
                break
        return self._filteredOptions

    def changeVariables(self, source, variables):
        """Invoked when the value of a variable has changed.

        @see com.vaadin.ui.AbstractComponent#changeVariables(java.lang.Object,
             java.util.Map)
        """
        # Not calling super.changeVariables due the history of select
        # component hierarchy
        # Selection change
        if 'selected' in variables:
            ka = variables['selected']
            if self.isMultiSelect():
                # Multiselect mode
                # TODO Optimize by adding repaintNotNeeded whan applicaple
                # Converts the key-array to id-set
                s = LinkedList()
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(ka)):
                        break
                    id = self.itemIdMapper.get(ka[i])
                    if id is not None and self.containsId(id):
                        s.add(id)
                # Limits the deselection to the set of visible items
                # (non-visible items can not be deselected)
                visible = self.getVisibleItemIds()
                if visible is not None:
                    newsel = self.getValue()
                    if newsel is None:
                        newsel = set()
                    else:
                        newsel = set(newsel)
                    newsel.removeAll(visible)
                    newsel.addAll(s)
                    self.setValue(newsel, True)
            elif len(ka) == 0:
                # Allows deselection only if the deselected item is visible
                current = self.getValue()
                visible = self.getVisibleItemIds()
                if visible is not None and visible.contains(current):
                    self.setValue(None, True)
            else:
                id = self.itemIdMapper.get(ka[0])
                if id is not None and id == self.getNullSelectionItemId():
                    self.setValue(None, True)
                else:
                    self.setValue(id, True)
            # Single select mode
        if newFilter = variables['filter'] is not None:
            # this is a filter request
            self._currentPage = variables['page'].intValue()
            self._filterstring = newFilter
            if self._filterstring is not None:
                self._filterstring = self._filterstring.toLowerCase()
            self.optionRepaint()
        elif self.isNewItemsAllowed():
            # New option entered (and it is allowed)
            newitem = variables['newitem']
            if newitem is not None and len(newitem) > 0:
                self.getNewItemHandler().addNewItem(newitem)
                # rebuild list
                self._filterstring = None
                self._prevfilterstring = None
        if FocusEvent.EVENT_ID in variables:
            self.fireEvent(FocusEvent(self))
        if BlurEvent.EVENT_ID in variables:
            self.fireEvent(BlurEvent(self))

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
        """Note, one should use more generic setWidth(String) method instead of
        this. This now days actually converts columns to width with em css unit.

        Sets the number of columns in the editor. If the number of columns is set
        0, the actual number of displayed columns is determined implicitly by the
        adapter.

        @deprecated

        @param columns
                   the number of columns to set.
        """
        if columns < 0:
            columns = 0
        if self._columns != columns:
            self._columns = columns
            self.setWidth(columns, Select.UNITS_EM)
            self.requestRepaint()

    def getColumns(self):
        """@deprecated see setter function
        @return
        """
        return self._columns

    def addListener(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], BlurListener):
                listener, = _0
                self.addListener(BlurEvent.EVENT_ID, BlurEvent, listener, BlurListener.blurMethod)
            else:
                listener, = _0
                self.addListener(FocusEvent.EVENT_ID, FocusEvent, listener, FocusListener.focusMethod)
        else:
            raise ARGERROR(1, 1)

    def removeListener(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], BlurListener):
                listener, = _0
                self.removeListener(BlurEvent.EVENT_ID, BlurEvent, listener)
            else:
                listener, = _0
                self.removeListener(FocusEvent.EVENT_ID, FocusEvent, listener)
        else:
            raise ARGERROR(1, 1)

    def setMultiSelect(self, multiSelect):
        """@deprecated use {@link ListSelect}, {@link OptionGroup} or
                    {@link TwinColSelect} instead
        @see com.vaadin.ui.AbstractSelect#setMultiSelect(boolean)
        """
        super(Select, self).setMultiSelect(multiSelect)

    def isMultiSelect(self):
        """@deprecated use {@link ListSelect}, {@link OptionGroup} or
                    {@link TwinColSelect} instead

        @see com.vaadin.ui.AbstractSelect#isMultiSelect()
        """
        return super(Select, self).isMultiSelect()

    def setScrollToSelectedItem(self, scrollToSelectedItem):
        """Sets whether to scroll the selected item visible (directly open the page
        on which it is) when opening the combo box popup or not. Only applies to
        single select mode.

        This requires finding the index of the item, which can be expensive in
        many large lazy loading containers.

        @param scrollToSelectedItem
                   true to find the page with the selected item when opening the
                   selection popup
        """
        self._scrollToSelectedItem = scrollToSelectedItem

    def isScrollToSelectedItem(self):
        """Returns true if the select should find the page with the selected item
        when opening the popup (single select combo box only).

        @see #setScrollToSelectedItem(boolean)

        @return true if the page with the selected item will be shown when
                opening the popup
        """
        return self._scrollToSelectedItem
