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

from muntjac.ui.abstract_field import AbstractField
from muntjac.terminal.resource import IResource
from muntjac.terminal.key_mapper import KeyMapper

from muntjac.data import property as prop
from muntjac.data import container
from muntjac.data import item

from muntjac.data.util.indexed_container import IndexedContainer

from muntjac.event.dd.acceptcriteria.target_detail_is import TargetDetailIs
from muntjac.event.dd.target_details_impl import TargetDetailsImpl

from muntjac.event.dd.acceptcriteria.contains_data_flavor import \
    ContainsDataFlavor

from muntjac.event.dd.acceptcriteria.client_side_criterion import \
    ClientSideCriterion

from muntjac.terminal.gwt.client.ui.dd.vertical_drop_location import \
    VerticalDropLocation


class AbstractSelect(AbstractField, container.IContainer, container.IViewer,
            container.IPropertySetChangeListener,
            container.IPropertySetChangeNotifier,
            container.IItemSetChangeNotifier,
            container.IItemSetChangeListener):
    """A class representing a selection of items the user has selected
    in a UI. The set of choices is presented as a set of L{IItem}s in a
    L{IContainer}.

    A C{Select} component may be in single- or multiselect mode. Multiselect
    mode means that more than one item can be selected simultaneously.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    #: IItem caption mode: IItem's ID's C{String} representation
    #  is used as caption.
    ITEM_CAPTION_MODE_ID = 0

    #: IItem caption mode: IItem's C{String} representation is
    #  used as caption.
    ITEM_CAPTION_MODE_ITEM = 1

    #: IItem caption mode: Index of the item is used as caption. The index
    #  mode can only be used with the containers implementing the
    #  L{muntjac.data.container.IIndexed} interface.
    ITEM_CAPTION_MODE_INDEX = 2

    #: IItem caption mode: If an IItem has a caption it's used, if not,
    #  IItem's ID's string representation is used as caption.
    #  B{This is the default}.
    ITEM_CAPTION_MODE_EXPLICIT_DEFAULTS_ID = 3

    #: IItem caption mode: Captions must be explicitly specified.
    ITEM_CAPTION_MODE_EXPLICIT = 4

    #: IItem caption mode: Only icons are shown, captions are hidden.
    ITEM_CAPTION_MODE_ICON_ONLY = 5

    #: IItem caption mode: IItem captions are read from property specified
    #  with C{setItemCaptionPropertyId}.
    ITEM_CAPTION_MODE_PROPERTY = 6


    def __init__(self, *args):
        """Creates an empty Select with caption, that is connected to a
        data-source or is filled from a collection of option values.

        @param args: tuple of the form
            - ()
            - (caption)
              1. the caption of the component.
            - (caption, dataSource)
              1. the caption of the component.
              2. the IContainer datasource to be selected from by
                 this select.
            - (caption, options)
              1. the caption of the component.
              2. the Collection containing the options.
        """
        #: Is the select in multiselect mode?
        self._multiSelect = False

        #: Select options.
        self.items = None

        #: Is the user allowed to add new options?
        self._allowNewOptions = None

        #: Keymapper used to map key values.
        self.itemIdMapper = KeyMapper()

        #: IItem icons.
        self._itemIcons = dict()

        #: IItem captions.
        self._itemCaptions = dict()

        #: IItem caption mode.
        self._itemCaptionMode = self.ITEM_CAPTION_MODE_EXPLICIT_DEFAULTS_ID

        #: IItem caption source property id.
        self._itemCaptionPropertyId = None

        #: IItem icon source property id.
        self._itemIconPropertyId = None

        #: List of property set change event listeners.
        self._propertySetEventListeners = set()

        #: List of item set change event listeners.
        self._itemSetEventListeners = set()

        self._propertySetEventCallbacks = dict()

        self._itemSetEventCallbacks = dict()

        #: IItem id that represents null selection of this select.
        #
        #  Data interface does not support nulls as item ids. Selecting the
        #  item identified by this id is the same as selecting no items at
        #  all. This setting only affects the single select mode.
        self._nullSelectionItemId = None

        # Null (empty) selection is enabled by default
        self._nullSelectionAllowed = True

        self._newItemHandler = None

        #: Caption (IItem / IProperty) change listeners
        self._captionChangeListener = None

        super(AbstractSelect, self).__init__()

        nargs = len(args)
        if nargs == 0:
            self.setContainerDataSource(IndexedContainer())
        elif nargs == 1:
            caption, = args
            self.setContainerDataSource(IndexedContainer())
            self.setCaption(caption)
        elif nargs == 2:
            if isinstance(args[1], list):
                caption, options = args
                # Create the options container and add given options to it
                c = IndexedContainer()
                if options is not None:
                    for o in options:
                        c.addItem(o)

                self.setCaption(caption)
                self.setContainerDataSource(c)
            else:
                caption, dataSource = args
                self.setCaption(caption)
                self.setContainerDataSource(dataSource)
        else:
            raise ValueError, 'too many arguments'


    def paintContent(self, target):
        """Paints the content of this component.

        @param target:
                   the Paint Event.
        @raise PaintException:
                    if the paint operation failed.
        """
        # Paints field properties
        super(AbstractSelect, self).paintContent(target)

        # Paints select attributes
        if self.isMultiSelect():
            target.addAttribute('selectmode', 'multi')

        if self.isNewItemsAllowed():
            target.addAttribute('allownewitem', True)

        if self.isNullSelectionAllowed():
            target.addAttribute('nullselect', True)
            if self.getNullSelectionItemId() is not None:
                target.addAttribute('nullselectitem', True)

        # Constructs selected keys array
        if self.isMultiSelect():
            selectedKeys = [None] * len(self.getValue())
        elif (self.getValue() is None
                and self.getNullSelectionItemId() is None):
            selectedKeys = [None] * 0
        else:
            selectedKeys = [None] * 1

        # first remove all previous item/property listeners
        self.getCaptionChangeListener().clear()
        # Paints the options and create array of selected id keys

        target.startTag('options')
        keyIndex = 0
        # Support for external null selection item id
        ids = self.getItemIds()
        if (self.isNullSelectionAllowed()
                and (self.getNullSelectionItemId() is not None)
                and (self.getNullSelectionItemId() not in ids)):
            idd = self.getNullSelectionItemId()
            # Paints option
            target.startTag('so')
            self.paintItem(target, idd)
            if self.isSelected(idd):
                selectedKeys[keyIndex] = self.itemIdMapper.key(idd)
                keyIndex += 1  # post increment
            target.endTag('so')

        i = self.getItemIds()
        # Paints the available selection options from data source
        for idd in i:
            if (not self.isNullSelectionAllowed()
                    and (idd is not None)
                    and (idd == self.getNullSelectionItemId())):
                # Remove item if it's the null selection item but null
                # selection is not allowed
                continue

            key = self.itemIdMapper.key(idd)
            # add listener for each item, to cause repaint
            # if an item changes
            self.getCaptionChangeListener().addNotifierForItem(idd)
            target.startTag('so')
            self.paintItem(target, idd)
            if self.isSelected(idd) and (keyIndex < len(selectedKeys)):
                selectedKeys[keyIndex] = key
                keyIndex += 1  # post increment
            target.endTag('so')
        target.endTag('options')

        # Paint variables
        target.addVariable(self, 'selected', selectedKeys)
        if self.isNewItemsAllowed():
            target.addVariable(self, 'newitem', '')


    def paintItem(self, target, itemId):
        key = self.itemIdMapper.key(itemId)
        caption = self.getItemCaption(itemId)
        icon = self.getItemIcon(itemId)
        if icon is not None:
            target.addAttribute('icon', icon)

        target.addAttribute('caption', caption)
        if (itemId is not None) and (itemId == self.getNullSelectionItemId()):
            target.addAttribute('nullselection', True)

        target.addAttribute('key', key)
        if self.isSelected(itemId):
            target.addAttribute('selected', True)


    def changeVariables(self, source, variables):
        """Invoked when the value of a variable has changed.

        @see: L{AbstractComponent.changeVariables}
        """
        super(AbstractSelect, self).changeVariables(source, variables)

        # New option entered (and it is allowed)
        if self.isNewItemsAllowed():
            newitem = variables.get('newitem')
            if (newitem is not None) and (len(newitem) > 0):
                self.getNewItemHandler().addNewItem(newitem)

        # Selection change
        if 'selected' in variables:
            ka = variables.get('selected')

            # Multiselect mode
            if self.isMultiSelect():

                # TODO Optimize by adding repaintNotNeeded when applicable

                # Converts the key-array to id-set
                s = list()
                for i in range( len(ka) ):
                    idd = self.itemIdMapper.get(ka[i])
                    if (not self.isNullSelectionAllowed()
                            and (idd is None
                            or idd == self.getNullSelectionItemId())):
                        # skip empty selection if nullselection
                        # is not allowed
                        self.requestRepaint()
                    elif (idd is not None) and self.containsId(idd):
                        s.append(idd)

                if not self.isNullSelectionAllowed() and (len(s) < 1):
                    # empty selection not allowed, keep old value
                    self.requestRepaint()
                    return

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
                if (not self.isNullSelectionAllowed()
                        and (len(ka) == 0 or ka[0] is None
                        or ka[0] == self.getNullSelectionItemId())):
                    self.requestRepaint()
                    return

                if len(ka) == 0:
                    # Allows deselection only if the deselected item
                    # is visible
                    current = self.getValue()
                    visible = self.getVisibleItemIds()
                    if visible is not None and current in visible:
                        self.setValue(None, True)
                else:
                    idd = self.itemIdMapper.get(ka[0])
                    if not self.isNullSelectionAllowed() and (idd is None):
                        self.requestRepaint()
                    elif (idd is not None
                            and idd == self.getNullSelectionItemId()):
                        self.setValue(None, True)
                    else:
                        self.setValue(idd, True)


    def setNewItemHandler(self, newItemHandler):
        """Setter for new item handler that is called when user adds
        new item in newItemAllowed mode.
        """
        self._newItemHandler = newItemHandler


    def getNewItemHandler(self):
        """Getter for new item handler.

        @return: newItemHandler
        """
        if self._newItemHandler is None:
            self._newItemHandler = DefaultNewItemHandler()
        return self._newItemHandler


    def getVisibleItemIds(self):
        """Gets the visible item ids. In Select, this returns list of all
        item ids, but can be overriden in subclasses if they paint only
        part of the items to the terminal or null if no items is visible.
        """
        if self.isVisible():
            return self.getItemIds()
        return None


    def getType(self, propertyId=None):
        """Returns the type of the property. C{getValue} and
        C{setValue} methods must be compatible with this type:
        one can safely cast C{getValue} to given type and pass
        any variable assignable to this type as a parameter to
        C{setValue}.

        @param propertyId:
                   the Id identifying the property.
        @return: the Type of the property.
        @see: L{IContainer.getType}
        """
        if propertyId is None:
            if self.isMultiSelect():
                return set
            else:
                return object
        else:
            return self.items.getType(propertyId)


    def getValue(self):
        """Gets the selected item id or in multiselect mode a set of
        selected ids.

        @see: L{AbstractField.getValue}
        """
        retValue = super(AbstractSelect, self).getValue()

        if self.isMultiSelect():

            # If the return value is not a set
            if retValue is None:
                return set()

            if isinstance(retValue, set):
                return retValue

            elif isinstance(retValue, list):
                return set(retValue)

            else:
                s = set()
                if self.items.containsId(retValue):
                    s.add(retValue)
                return s
        else:
            return retValue


    def setValue(self, newValue, repaintIsNotNeeded=None):
        """Sets the visible value of the property.

        The value of the select is the selected item id. If the select
        is in multiselect-mode, the value is a set of selected item keys.
        In multiselect mode all collections of id:s can be assigned.

        @param newValue:
                   the New selected item or collection of selected items.
        @param repaintIsNotNeeded:
                   True if caller is sure that repaint is not needed.
        @see: L{AbstractField.setValue}
        """
        if repaintIsNotNeeded is None:
            if newValue == self.getNullSelectionItemId():
                newValue = None
            self.setValue(newValue, False)
        else:
            if self.isMultiSelect():

                if newValue is None:
                    super(AbstractSelect, self).setValue(set(),
                            repaintIsNotNeeded)
                elif hasattr(newValue, '__iter__'):
                    super(AbstractSelect, self).setValue(set(newValue),
                            repaintIsNotNeeded)

            elif (newValue is None) or (self.items.containsId(newValue)):
                super(AbstractSelect, self).setValue(newValue,
                        repaintIsNotNeeded)

    # IContainer methods

    def getItem(self, itemId):
        """Gets the item from the container with given id. If the container
        does not contain the requested item, null is returned.

        @param itemId:
                   the item id.
        @return: the item from the container.
        """
        return self.items.getItem(itemId)


    def getItemIds(self):
        """Gets the item Id collection from the container.

        @return: the Collection of item ids.
        """
        return self.items.getItemIds()


    def getContainerPropertyIds(self):
        """Gets the property Id collection from the container.

        @return: the Collection of property ids.
        """
        return self.items.getContainerPropertyIds()


    # Gets the number of items in the container.
    #
    # @return: the Number of items in the container.
    # @see: L{IContainer.size}
    def size(self):
        return len(self.items)


    def __len__(self):
        return self.size()


    def containsId(self, itemId):
        """Tests, if the collection contains an item with given id.

        @param itemId:
                   the Id the of item to be tested.
        """
        if itemId is not None:
            return self.items.containsId(itemId)
        else:
            return False


    def getContainerProperty(self, itemId, propertyId):
        """Gets the IProperty identified by the given itemId and propertyId
        from the IContainer

        @see: L{IContainer.getContainerProperty}
        """
        return self.items.getContainerProperty(itemId, propertyId)


    def addContainerProperty(self, propertyId, typ, defaultValue):
        """Adds the new property to all items. Adds a property with given
        id, type and default value to all items in the container.

        This functionality is optional. If the function is unsupported,
        it always returns false.

        @return: True if the operation succeeded.
        @see: L{IContainer.addContainerProperty}
        """
        retval = self.items.addContainerProperty(propertyId, typ,
                defaultValue)

        if (retval and (not isinstance(self.items,
                container.IPropertySetChangeNotifier))):
            self.firePropertySetChange()

        return retval


    def removeAllItems(self):
        """Removes all items from the container.

        This functionality is optional. If the function is unsupported,
        it always returns false.

        @return: True if the operation succeeded.
        @see: L{IContainer.removeAllItems}
        """
        retval = self.items.removeAllItems()
        self.itemIdMapper.removeAll()

        if retval:
            self.setValue(None)
            if not isinstance(self.items, container.IItemSetChangeNotifier):
                self.fireItemSetChange()

        return retval


    def addItem(self, itemId=None):
        """Create a new item into container. The created new item is returned
        and ready for setting property values. if the creation fails, null
        is returned. In case the container already contains the item, null
        is returned.

        This functionality is optional. If the function is unsupported, it
        always returns null.

        @param itemId:
                   the Identification of the item to be created.
        @return: the Created item with the given id, or null in case of
                failure.
        @see: L{IContainer.addItem}
        """
        if itemId is None:
            retval = self.items.addItem()
            if (retval is not None) and (not isinstance(self.items,
                    container.IItemSetChangeNotifier)):
                self.fireItemSetChange()
            return retval
        else:
            retval = self.items.addItem(itemId)
            if (retval is not None) and (not isinstance(self.items,
                    container.IItemSetChangeNotifier)):
                self.fireItemSetChange()
            return retval


    def removeItem(self, itemId):
        self.unselect(itemId)
        retval = self.items.removeItem(itemId)
        self.itemIdMapper.remove(itemId)
        if retval and (not isinstance(self.items,
                    container.IItemSetChangeNotifier)):
            self.fireItemSetChange()
        return retval


    def removeContainerProperty(self, propertyId):
        """Removes the property from all items. Removes a property with
        given id from all the items in the container.

        This functionality is optional. If the function is unsupported,
        it always returns false.

        @return: True if the operation succeeded.
        @see: L{IContainer.removeContainerProperty}
        """
        retval = self.items.removeContainerProperty(propertyId)
        if retval and (not isinstance(self.items,
                container.IPropertySetChangeNotifier)):
            self.firePropertySetChange()
        return retval


    def setContainerDataSource(self, newDataSource):
        """Sets the IContainer that serves as the data source of the viewer.

        As a side-effect the fields value (selection) is set to null due
        old selection not necessary exists in new IContainer.

        @see: L{muntjac.data.container.IViewer.setContainerDataSource}

        @param newDataSource:
                   the new data source.
        """
        if newDataSource is None:
            newDataSource = IndexedContainer()

        self.getCaptionChangeListener().clear()

        if self.items != newDataSource:

            # Removes listeners from the old datasource
            if self.items is not None:
                if isinstance(self.items,
                        container.IItemSetChangeNotifier):
                    self.items.removeListener(self,
                            container.IItemSetChangeListener)

                if isinstance(self.items,
                        container.IPropertySetChangeNotifier):
                    self.items.removeListener(self,
                            container.IPropertySetChangeListener)

            # Assigns new data source
            self.items = newDataSource

            # Clears itemIdMapper also
            self.itemIdMapper.removeAll()

            # Adds listeners
            if self.items is not None:
                if isinstance(self.items,
                        container.IItemSetChangeNotifier):
                    self.items.addListener(self,
                            container.IItemSetChangeListener)
                if isinstance(self.items,
                        container.IPropertySetChangeNotifier):
                    self.items.addListener(self,
                            container.IPropertySetChangeListener)

            # We expect changing the data source should also clean value.
            # See #810, #4607, #5281
            self.setValue(None)

            self.requestRepaint()


    def getContainerDataSource(self):
        """Gets the viewing data-source container.

        @see: L{muntjac.data.container.IViewer.getContainerDataSource}
        """
        return self.items

    # Select attributes

    def isMultiSelect(self):
        """Is the select in multiselect mode? In multiselect mode

        @return: the Value of property multiSelect.
        """
        return self._multiSelect


    def setMultiSelect(self, multiSelect):
        """Sets the multiselect mode. Setting multiselect mode false may
        loose selection information: if selected items set contains one
        or more selected items, only one of the selected items is kept as
        selected.

        @param multiSelect:
                   the New value of property multiSelect.
        """
        if multiSelect and (self.getNullSelectionItemId() is not None):
            raise ValueError, ('Multiselect and NullSelectionItemId can '
                    'not be set at the same time.')

        if multiSelect != self._multiSelect:

            # Selection before mode change
            oldValue = self.getValue()

            self._multiSelect = multiSelect

            # Convert the value type
            if multiSelect:
                s = set()
                if oldValue is not None:
                    s.add(oldValue)

                self.setValue(s)
            else:
                s = oldValue
                if (s is None) or (len(s) == 0):
                    self.setValue(None)
                else:
                    # Set the single select to contain only the first
                    # selected value in the multiselect
                    self.setValue(s[0])  # FIXME: check iterator

            self.requestRepaint()


    def isNewItemsAllowed(self):
        """Does the select allow adding new options by the user. If true,
        the new options can be added to the IContainer. The text entered by
        the user is used as id. Note that data-source must allow adding new
        items.

        @return: True if additions are allowed.
        """
        return self._allowNewOptions


    def setNewItemsAllowed(self, allowNewOptions):
        """Enables or disables possibility to add new options by the user.

        @param allowNewOptions:
                   the New value of property allowNewOptions.
        """
        # Only handle change requests
        if self._allowNewOptions != allowNewOptions:

            self._allowNewOptions = allowNewOptions

            self.requestRepaint()


    def setItemCaption(self, itemId, caption):
        """Override the caption of an item. Setting caption explicitly
        overrides id, item and index captions.

        @param itemId:
                   the id of the item to be re-captioned.
        @param caption:
                   the New caption.
        """
        if itemId is not None:
            self._itemCaptions[itemId] = caption
            self.requestRepaint()


    def getItemCaption(self, itemId):
        """Gets the caption of an item. The caption is generated as specified
        by the item caption mode. See C{setItemCaptionMode()} for
        more details.

        @param itemId:
                   the id of the item to be queried.
        @return: the caption for specified item.
        """
        # Null items can not be found
        if itemId is None:
            return None

        caption = None

        test = self.getItemCaptionMode()
        if test == self.ITEM_CAPTION_MODE_ID:
            caption = str(itemId)

        elif test == self.ITEM_CAPTION_MODE_INDEX:
            if isinstance(self.items, container.IIndexed):
                caption = str(self.items.indexOfId(itemId))
            else:
                caption = 'ERROR: IContainer is not indexed'

        elif test == self.ITEM_CAPTION_MODE_ITEM:
            i = self.getItem(itemId)
            if i is not None:
                caption = str(i)

        elif test == self.ITEM_CAPTION_MODE_EXPLICIT:
            caption = self._itemCaptions.get(itemId)

        elif test == self.ITEM_CAPTION_MODE_EXPLICIT_DEFAULTS_ID:
            caption = self._itemCaptions.get(itemId)
            if caption is None:
                caption = str(itemId)

        elif test == self.ITEM_CAPTION_MODE_PROPERTY:
            p = self.getContainerProperty(itemId,
                    self.getItemCaptionPropertyId())
            if p is not None:
                caption = str(p)

        # All items must have some captions
        return caption if caption is not None else ''


    def setItemIcon(self, itemId, icon):
        """Sets the icon for an item.

        @param itemId:
                   the id of the item to be assigned an icon.
        @param icon:
                   the icon to use or null.
        """
        if itemId is not None:
            if icon is None:
                if itemId in self._itemIcons:
                    del self._itemIcons[itemId]
            else:
                self._itemIcons[itemId] = icon
            self.requestRepaint()


    def getItemIcon(self, itemId):
        """Gets the item icon.

        @param itemId:
                   the id of the item to be assigned an icon.
        @return: the icon for the item or null, if not specified.
        """
        explicit = self._itemIcons.get(itemId)
        if explicit is not None:
            return explicit

        if self.getItemIconPropertyId() is None:
            return None

        ip = self.getContainerProperty(itemId, self.getItemIconPropertyId())
        if ip is None:
            return None

        icon = ip.getValue()
        if isinstance(icon, IResource):
            return icon

        return None


    def setItemCaptionMode(self, mode):
        """Sets the item caption mode.

        The mode can be one of the following ones:

          - C{ITEM_CAPTION_MODE_EXPLICIT_DEFAULTS_ID} : Items
            Id-objects C{toString} is used as item caption. If caption
            is explicitly specified, it overrides the id-caption.
          - C{ITEM_CAPTION_MODE_ID} : Items Id-objects
            C{toString} is used as item caption.
          - C{ITEM_CAPTION_MODE_ITEM} : IItem-objects
            C{toString} is used as item caption.
          - C{ITEM_CAPTION_MODE_INDEX} : The index of the item is
            used as item caption. The index mode can only be used with the
            containers implementing C{IContainer.IIndexed} interface.
          - C{ITEM_CAPTION_MODE_EXPLICIT} : The item captions must
            be explicitly specified.
          - C{ITEM_CAPTION_MODE_PROPERTY} : The item captions are
            read from property, that must be specified with
            C{setItemCaptionPropertyId}.

        The C{ITEM_CAPTION_MODE_EXPLICIT_DEFAULTS_ID} is the default
        mode.

        @param mode:
                   the One of the modes listed above.
        """
        if ((self.ITEM_CAPTION_MODE_ID <= mode)
                and (mode <= self.ITEM_CAPTION_MODE_PROPERTY)):
            self._itemCaptionMode = mode
            self.requestRepaint()


    def getItemCaptionMode(self):
        """Gets the item caption mode.

        The mode can be one of the following ones:

          - C{ITEM_CAPTION_MODE_EXPLICIT_DEFAULTS_ID} : Items
            Id-objects C{toString} is used as item caption. If caption
            is explicitly specified, it overrides the id-caption.
          - C{ITEM_CAPTION_MODE_ID} : Items Id-objects
            C{toString} is used as item caption.
          - C{ITEM_CAPTION_MODE_ITEM} : IItem-objects
            C{toString} is used as item caption.
          - C{ITEM_CAPTION_MODE_INDEX} : The index of the item is
            used as item caption. The index mode can only be used with the
            containers implementing C{IContainer.IIndexed} interface.
          - C{ITEM_CAPTION_MODE_EXPLICIT} : The item captions must
            be explicitly specified.
          - C{ITEM_CAPTION_MODE_PROPERTY} : The item captions are
            read from property, that must be specified with
            C{setItemCaptionPropertyId}.

        The C{ITEM_CAPTION_MODE_EXPLICIT_DEFAULTS_ID} is the default
        mode.

        @return: the One of the modes listed above.
        """
        return self._itemCaptionMode


    def setItemCaptionPropertyId(self, propertyId):
        """Sets the item caption property.

        Setting the id to a existing property implicitly sets the item caption
        mode to C{ITEM_CAPTION_MODE_PROPERTY}. If the object is in
        C{ITEM_CAPTION_MODE_PROPERTY} mode, setting caption property
        id null resets the item caption mode to
        C{ITEM_CAPTION_EXPLICIT_DEFAULTS_ID}.

        Setting the property id to null disables this feature. The id is null
        by default.

        @param propertyId:
                   the id of the property.
        """
        if propertyId is not None:
            self._itemCaptionPropertyId = propertyId
            self.setItemCaptionMode(self.ITEM_CAPTION_MODE_PROPERTY)
            self.requestRepaint()
        else:
            self._itemCaptionPropertyId = None
            if self.getItemCaptionMode() == self.ITEM_CAPTION_MODE_PROPERTY:
                self.setItemCaptionMode(
                        self.ITEM_CAPTION_MODE_EXPLICIT_DEFAULTS_ID)
            self.requestRepaint()


    def getItemCaptionPropertyId(self):
        """Gets the item caption property.

        @return: the Id of the property used as item caption source.
        """
        return self._itemCaptionPropertyId


    def setItemIconPropertyId(self, propertyId):
        """Sets the item icon property.

        If the property id is set to a valid value, each item is given an
        icon got from the given property of the items. The type of the
        property must be assignable to IResource.

        Note: The icons set with C{setItemIcon} function override
        the icons from the property.

        Setting the property id to null disables this feature. The id is
        null by default.

        @param propertyId:
                   the id of the property that specifies icons for items
                   or null
        @raise ValueError:
                    If the propertyId is not in the container or is not of
                    a valid type
        """
        if propertyId is None:
            self._itemIconPropertyId = None

        elif propertyId not in self.getContainerPropertyIds():
            raise ValueError, 'IProperty id not found in the container'

        elif issubclass(self.getType(propertyId), IResource):
            self._itemIconPropertyId = propertyId
        else:
            raise ValueError, 'IProperty type must be assignable to IResource'

        self.requestRepaint()


    def getItemIconPropertyId(self):
        """Gets the item icon property.

        If the property id is set to a valid value, each item is given an
        icon got from the given property of the items. The type of the
        property must be assignable to Icon.

        Note: The icons set with C{setItemIcon} function override
        the icons from the property.

        Setting the property id to null disables this feature. The id is null
        by default.

        @return: the Id of the property containing the item icons.
        """
        return self._itemIconPropertyId


    def isSelected(self, itemId):
        """Tests if an item is selected.

        In single select mode testing selection status of the item identified
        by L{getNullSelectionItemId} returns true if the value of the
        property is null.

        @param itemId:
                   the Id the of the item to be tested.
        @see: L{getNullSelectionItemId}
        @see: L{setNullSelectionItemId}
        """
        if itemId is None:
            return False

        if self.isMultiSelect():
            return itemId in self.getValue()
        else:
            value = self.getValue()
            if value is None:
                return itemId == self.getNullSelectionItemId()
            else:
                return itemId == value


    def select(self, itemId):
        """Selects an item.

        In single select mode selecting item identified by
        L{getNullSelectionItemId} sets the value of the property
        to null.

        @param itemId:
                   the identifier of IItem to be selected.
        @see: L{getNullSelectionItemId}
        @see: L{setNullSelectionItemId}
        """
        if not self.isMultiSelect():
            self.setValue(itemId)
        elif (not self.isSelected(itemId) and (itemId is not None)
                and self.items.containsId(itemId)):
            s = set(self.getValue())
            s.add(itemId)
            self.setValue(s)


    def unselect(self, itemId):
        """Unselects an item.

        @param itemId:
                   the identifier of the IItem to be unselected.
        @see: L{getNullSelectionItemId}
        @see: L{setNullSelectionItemId}
        """
        if self.isSelected(itemId):
            if self.isMultiSelect():
                s = set(self.getValue())
                s.remove(itemId)
                self.setValue(s)
            else:
                self.setValue(None)


    def containerPropertySetChange(self, event):
        """Notifies this listener that the Containers contents has changed.

        @see: L{IPropertySetChangeListener.containerPropertySetChange}
        """
        self.firePropertySetChange()


    def addListener(self, listener, iface=None):
        """Adds a new IProperty or IItem set change listener for this
        IContainer.

        @see: L{IPropertySetChangeNotifier.addListener}
        @see: L{IItemSetChangeNotifier.addListener}
        """
        if (isinstance(listener, container.IItemSetChangeListener) and
                (iface is None or
                        issubclass(iface, container.IItemSetChangeListener))):

            self._itemSetEventListeners.add(listener)

        if (isinstance(listener, container.IPropertySetChangeListener) and
                (iface is None or
                    issubclass(iface, container.IPropertySetChangeListener))):

            self._propertySetEventListeners.add(listener)

        super(AbstractSelect, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if eventType == container.IItemSetChangeEvent:

            self._itemSetEventCallbacks[callback] = args

        elif eventType == container.IPropertySetChangeEvent:

            self._propertySetEventCallbacks[callback] = args

        else:
            super(AbstractSelect, self).addCallback(callback, eventType, *args)


    def removeListener(self, listener, iface=None):
        """Removes a previously registered IProperty and IItemset change
        listener.

        @see: L{IPropertySetChangeNotifier.removeListener}
        @see: L{IItemSetChangeNotifier.removeListener}
        """
        if (isinstance(listener, container.IItemSetChangeListener) and
                (iface is None or iface == container.IItemSetChangeListener)):
            if listener in self._itemSetEventListeners:
                self._itemSetEventListeners.remove(listener)

        if (isinstance(listener, container.IPropertySetChangeListener) and
                (iface is None or
                        iface == container.IPropertySetChangeListener)):
            if listener in self._propertySetEventListeners:
                self._propertySetEventListeners.remove(listener)

        super(AbstractSelect, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, container.IItemSetChangeEvent):
            if callback in self._itemSetEventCallbacks:
                del self._itemSetEventCallbacks[callback]

        elif eventType == container.IPropertySetChangeEvent:
            if callback in self._propertySetEventCallbacks:
                del self._propertySetEventCallbacks[callback]

        else:
            super(AbstractSelect, self).removeCallback(callback, eventType)


    def getListeners(self, eventType):
        if issubclass(eventType, container.IItemSetChangeEvent):
            return set(self._itemSetEventListeners)

        elif issubclass(eventType, container.IPropertySetChangeEvent):
            return set(self._propertySetEventListeners)

        return super(AbstractSelect, self).getListeners(eventType)


    def containerItemSetChange(self, event):
        """Lets the listener know a Containers IItem set has changed.

        @see: L{IItemSetChangeListener.containerItemSetChange}
        """
        # Clears the item id mapping table
        self.itemIdMapper.removeAll()

        # Notify all listeners
        self.fireItemSetChange()


    def firePropertySetChange(self):
        """Fires the property set change event."""
        event = IPropertySetChangeEvent(self)

        for l in self._propertySetEventListeners:
            l.containerPropertySetChange(event)

        for callback, args in self._propertySetEventCallbacks.iteritems():
            callback(event, *args)

        self.requestRepaint()


    def fireItemSetChange(self):
        """Fires the item set change event."""
        event = IItemSetChangeEvent(self)

        for l in self._itemSetEventListeners:
            l.containerItemSetChange(event)

        for callback, args in self._itemSetEventCallbacks.iteritems():
            callback(event, *args)

        self.requestRepaint()


    def isEmpty(self):
        """For multi-selectable fields, also an empty collection of values
        is considered to be an empty field.

        @see: L{AbstractField.isEmpty}.
        """
        if not self._multiSelect:
            return super(AbstractSelect, self).isEmpty()
        else:
            value = self.getValue()
            return (super(AbstractSelect, self).isEmpty()
                    or (isinstance(value, list) and len(value) == 0))


    def setNullSelectionAllowed(self, nullSelectionAllowed):
        """Allow or disallow empty selection by the user. If the select is
        in single-select mode, you can make an item represent the empty
        selection by calling C{setNullSelectionItemId()}. This
        way you can for instance set an icon and caption for the null
        selection item.

        @param nullSelectionAllowed:
                   whether or not to allow empty selection
        @see: L{setNullSelectionItemId}
        @see: L{isNullSelectionAllowed}
        """
        if nullSelectionAllowed != self._nullSelectionAllowed:
            self._nullSelectionAllowed = nullSelectionAllowed
            self.requestRepaint()


    def isNullSelectionAllowed(self):
        """Checks if null empty selection is allowed by the user.

        @return: whether or not empty selection is allowed
        @see: L{setNullSelectionAllowed}
        """
        return self._nullSelectionAllowed


    def getNullSelectionItemId(self):
        """Returns the item id that represents null value of this select in
        single select mode.

        Data interface does not support nulls as item ids. Selecting the item
        identified by this id is the same as selecting no items at all. This
        setting only affects the single select mode.

        @return: the Object Null value item id.
        @see: L{setNullSelectionItemId}
        @see: L{isSelected}
        @see: L{select}
        """
        return self._nullSelectionItemId


    def setNullSelectionItemId(self, nullSelectionItemId):
        """Sets the item id that represents null value of this select.

        Data interface does not support nulls as item ids. Selecting the
        item identified by this id is the same as selecting no items at all.
        This setting only affects the single select mode.

        @param nullSelectionItemId:
                   the nullSelectionItemId to set.
        @see: L{getNullSelectionItemId}
        @see: L{isSelected}
        @see: L{select}
        """
        if (nullSelectionItemId is not None) and self.isMultiSelect():
            raise ValueError, ('Multiselect and NullSelectionItemId can '
                    'not be set at the same time.')

        self._nullSelectionItemId = nullSelectionItemId


    def attach(self):
        """Notifies the component that it is connected to an application.

        @see: L{AbstractField.attach}
        """
        super(AbstractSelect, self).attach()


    def detach(self):
        """Detaches the component from application.

        @see: L{AbstractComponent.detach}
        """
        self.getCaptionChangeListener().clear()
        super(AbstractSelect, self).detach()


    def getCaptionChangeListener(self):
        if self._captionChangeListener is None:
            self._captionChangeListener = CaptionChangeListener(self)
        return self._captionChangeListener


class IFiltering(object):
    """Interface for option filtering, used to filter options based on
    user entered value. The value is matched to the item caption.
    C{FILTERINGMODE_OFF} (0) turns the filtering off.
    C{FILTERINGMODE_STARTSWITH} (1) matches from the start of
    the caption. C{FILTERINGMODE_CONTAINS} (1) matches anywhere
    in the caption.
    """

    FILTERINGMODE_OFF = 0

    FILTERINGMODE_STARTSWITH = 1

    FILTERINGMODE_CONTAINS = 2

    def setFilteringMode(self, filteringMode):
        """Sets the option filtering mode.

        @param filteringMode:
                   the filtering mode to use
        """
        raise NotImplementedError


    def getFilteringMode(self):
        """Gets the current filtering mode.

        @return: the filtering mode in use
        """
        raise NotImplementedError


class MultiSelectMode(object):
    """Multi select modes that controls how multi select behaves."""

    #: The default behavior of the multi select mode
    DEFAULT = 'DEFAULT'

    #: The previous more simple behavior of the multselect
    SIMPLE = 'SIMPLE'

    _values = [DEFAULT, SIMPLE]

    @classmethod
    def values(cls):
        return cls._values[:]

    @classmethod
    def ordinal(cls, val):
        return cls._values.index(val)


class INewItemHandler(object):

    def addNewItem(self, newItemCaption):
        raise NotImplementedError


class DefaultNewItemHandler(INewItemHandler):
    """This is a default class that handles adding new items that are typed
    by user to selects container.

    By extending this class one may implement some logic on new item
    addition like database inserts.
    """

    def addNewItem(self, newItemCaption):
        # Checks for readonly
        if self.isReadOnly():
            raise prop.ReadOnlyException()

        # Adds new option
        if self.addItem(newItemCaption) is not None:

            # Sets the caption property, if used
            if self.getItemCaptionPropertyId() is not None:
                try:
                    prop = self.getContainerProperty(newItemCaption,
                            self.getItemCaptionPropertyId())
                    prop.setValue(newItemCaption)
                except prop.ConversionException:
                    # The conversion exception is safely ignored, the
                    # caption is just missing
                    pass

            if self.isMultiSelect():
                values = set(self.getValue())
                values.add(newItemCaption)
                self.setValue(values)
            else:
                self.setValue(newItemCaption)


class IItemSetChangeEvent(container.IItemSetChangeEvent):
    """Implementation of item set change event."""

    def __init__(self, container):
        self._container = container


    def getContainer(self):
        """Gets the IProperty where the event occurred.

        @see: L{muntjac.data.container.IItemSetChangeEvent.getContainer}
        """
        return self._container


class IPropertySetChangeEvent(container.IPropertySetChangeEvent):
    """Implementation of property set change event."""

    def __init__(self, container):
        self._container = container


    def getContainer(self):
        """Retrieves the IContainer whose contents have been modified.

        @see: L{muntjac.data.container.IPropertySetChangeEvent.getContainer}
        """
        return self._container


class AbstractSelectTargetDetails(TargetDetailsImpl):
    """TargetDetails implementation for subclasses of L{AbstractSelect}
    that implement L{DropTarget}.
    """

    def __init__(self, rawVariables, select):
        """Constructor that automatically converts itemIdOver key to
        corresponding item Id
        """
        super(AbstractSelectTargetDetails, self).__init__(rawVariables, select)

        # The item id over which the drag event happened.
        self.idOver = None

        # eagar fetch itemid, mapper may be emptied
        keyover = self.getData('itemIdOver')
        if keyover is not None:
            self.idOver = select.itemIdMapper.get(keyover)


    def getItemIdOver(self):
        """If the drag operation is currently over an L{IItem}, this
        method returns the identifier of that L{IItem}.
        """
        return self.idOver


    def getDropLocation(self):
        """Returns a detailed vertical location where the drop happened on
        IItem.
        """
        detail = self.getData('detail')
        if detail is None:
            return None
        return VerticalDropLocation.valueOf(detail)


class CaptionChangeListener(item.IPropertySetChangeListener,
            prop.IValueChangeListener):
    """This is a listener helper for IItem and IProperty changes that should
    cause a repaint. It should be attached to all items that are displayed,
    and the default implementation does this in paintContent(). Especially
    "lazyloading" components should take care to add and remove listeners as
    appropriate. Call addNotifierForItem() for each painted item (and
    remember to clear).

    NOTE: singleton, use getCaptionChangeListener().
    """

    def __init__(self, select):
        self._select = select

        # TODO clean this up - type is either item.IPropertySetChangeNotifier
        # or property.IValueChangeNotifier
        self._captionChangeNotifiers = set()


    def addNotifierForItem(self, itemId):
        test = self._select.getItemCaptionMode()
        if test == self._select.ITEM_CAPTION_MODE_ITEM:
            i = self._select.getItem(itemId)
            if i is None:
                return

            if isinstance(i, item.IPropertySetChangeNotifier):
                i.addListener(self._select.getCaptionChangeListener(),
                        item.IPropertySetChangeListener)
                self._captionChangeNotifiers.add(i)

            pids = i.getItemPropertyIds()
            if pids is not None:
                for pid in pids:
                    p = i.getItemProperty(pid)
                    if (p is not None
                            and isinstance(p, prop.IValueChangeNotifier)):
                        p.addListener(self._select.getCaptionChangeListener(),
                                prop.IValueChangeListener)
                        self._captionChangeNotifiers.add(p)

        elif test == self._select.ITEM_CAPTION_MODE_PROPERTY:
            p = self._select.getContainerProperty(itemId,
                    self._select.getItemCaptionPropertyId())
            if p is not None and isinstance(p, prop.IValueChangeNotifier):
                p.addListener(self._select.getCaptionChangeListener(),
                        prop.IValueChangeListener)
                self._captionChangeNotifiers.add(p)


    def clear(self):
        for notifier in self._captionChangeNotifiers:
            if isinstance(notifier, item.IPropertySetChangeNotifier):
                notifier.removeListener(self._select.getCaptionChangeListener(),
                        item.IPropertySetChangeListener)
            else:
                notifier.removeListener(self._select.getCaptionChangeListener(),
                        prop.IValueChangeListener)
        self._captionChangeNotifiers.clear()


    def valueChange(self, event):
        self._select.requestRepaint()


    def itemPropertySetChange(self, event):
        self._select.requestRepaint()


class AbstractItemSetCriterion(ClientSideCriterion):
    """Abstract helper class to implement item id based criterion.

    Note, inner class used not to open itemIdMapper for public access.
    """

    def __init__(self, select, *itemId):
        if (self.itemIds is None) or (select is None):
            raise ValueError, 'Accepted item identifiers must be accepted.'
        self.itemIds = set(itemId)
        self.select = select


    def paintContent(self, target):
        super(AbstractItemSetCriterion, self).paintContent(target)
        keys = [None] * len(self.itemIds)

        for i, itemId in enumerate(self.itemIds):
            key = self.select.itemIdMapper.key(itemId)
            keys[i] = key

        target.addAttribute('keys', keys)
        target.addAttribute('s', self.select)


class TargetItemIs(AbstractItemSetCriterion):
    """Criterion which accepts a drop only if the drop target is (one of)
    the given IItem identifier(s). Criterion can be used only on a drop
    targets that extends AbstractSelect like L{Table} and L{Tree}.
    The target and identifiers of valid Items are given in constructor.
    """

    def __init__(self, select, *itemId):
        """@param select:
                   the select implementation that is used as a drop target
        @param itemId:
                   the identifier(s) that are valid drop locations
        """
        super(TargetItemIs, self).__init__(select, itemId)


    def accept(self, dragEvent):
        dropTargetData = dragEvent.getTargetDetails()
        if dropTargetData.getTarget() != self.select:
            return False
        return dropTargetData.getItemIdOver() in self.itemIds


class AcceptItem(AbstractItemSetCriterion):
    """This criterion accepts a only a L{Transferable} that contains
    given IItem (practically its identifier) from a specific AbstractSelect.
    """

    def __init__(self, select, *itemId):
        """@param select:
                   the select from which the item id's are checked
        @param itemId:
                   the item identifier(s) of the select that are accepted
        """
        super(AcceptItem, self).__init__(select, itemId)


    def accept(self, dragEvent):
        transferable = dragEvent.getTransferable()

        if transferable.getSourceComponent() != self.select:
            return False

        return transferable.getItemId() in self.itemIds

    # A simple accept criterion which ensures that L{Transferable}
    # contains an L{IItem} (or actually its identifier). In other words
    # the criterion check that drag is coming from a L{IContainer} like
    # L{Tree} or L{Table}.
    ALL = ContainsDataFlavor('itemId')


class VerticalLocationIs(TargetDetailIs):
    """An accept criterion to accept drops only on a specific vertical
    location of an item.

    This accept criterion is currently usable in Tree and Table
    implementations.
    """

    TOP = None
    BOTTOM = None
    MIDDLE = None

    def __init__(self, l):
        super(VerticalLocationIs, self).__init__('detail', l)

VerticalLocationIs.TOP    = VerticalLocationIs(VerticalDropLocation.TOP)
VerticalLocationIs.BOTTOM = VerticalLocationIs(VerticalDropLocation.BOTTOM)
VerticalLocationIs.MIDDLE = VerticalLocationIs(VerticalDropLocation.MIDDLE)


class ItemDescriptionGenerator(object):
    """Implement this interface and pass it to Tree.setItemDescriptionGenerator
    or Table.setItemDescriptionGenerator to generate mouse over descriptions
    ("tooltips") for the rows and cells in Table or for the items in Tree.
    """

    def generateDescription(self, source, itemId, propertyId):
        """Called by Table when a cell (and row) is painted or a item is
        painted in Tree

        @param source:
                     The source of the generator, the Tree or Table the
                     generator is attached to
        @param itemId:
                     The itemId of the painted cell
        @param propertyId:
                     The propertyId of the cell, null when getting row
                     description
        @return: The description or "tooltip" of the item.
        """
        raise NotImplementedError
