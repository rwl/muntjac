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
from com.vaadin.data.util.IndexedContainer import (IndexedContainer,)
from com.vaadin.data.Property import (Property, ValueChangeListener,)
from com.vaadin.ui.AbstractField import (AbstractField,)
from com.vaadin.data.Item import (Item,)
from com.vaadin.terminal.gwt.client.ui.dd.VerticalDropLocation import (VerticalDropLocation,)
from com.vaadin.event.dd.acceptcriteria.ContainsDataFlavor import (ContainsDataFlavor,)
from com.vaadin.terminal.Resource import (Resource,)
from com.vaadin.terminal.KeyMapper import (KeyMapper,)
from com.vaadin.event.dd.acceptcriteria.ClientSideCriterion import (ClientSideCriterion,)
from com.vaadin.event.dd.acceptcriteria.TargetDetailIs import (TargetDetailIs,)
from com.vaadin.data.Container import (Container, ItemSetChangeEvent, ItemSetChangeListener, ItemSetChangeNotifier, PropertySetChangeEvent, PropertySetChangeListener, PropertySetChangeNotifier, Viewer,)
from com.vaadin.event.dd.TargetDetailsImpl import (TargetDetailsImpl,)
# from java.io.Serializable import (Serializable,)
# from java.util.Collection import (Collection,)
# from java.util.Collections import (Collections,)
# from java.util.HashMap import (HashMap,)
# from java.util.HashSet import (HashSet,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedHashSet import (LinkedHashSet,)
# from java.util.LinkedList import (LinkedList,)
# from java.util.Map import (Map,)
# from java.util.Set import (Set,)


class AbstractSelect(AbstractField, Container, Container, Viewer, Container, PropertySetChangeListener, Container, PropertySetChangeNotifier, Container, ItemSetChangeNotifier, Container, ItemSetChangeListener):
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
    @since 5.0
    """
    # Item caption mode: Item's ID's <code>String</code> representation is used
    # as caption.

    ITEM_CAPTION_MODE_ID = 0
    # Item caption mode: Item's <code>String</code> representation is used as
    # caption.

    ITEM_CAPTION_MODE_ITEM = 1
    # Item caption mode: Index of the item is used as caption. The index mode
    # can only be used with the containers implementing the
    # {@link com.vaadin.data.Container.Indexed} interface.

    ITEM_CAPTION_MODE_INDEX = 2
    # Item caption mode: If an Item has a caption it's used, if not, Item's
    # ID's <code>String</code> representation is used as caption. <b>This is
    # the default</b>.

    ITEM_CAPTION_MODE_EXPLICIT_DEFAULTS_ID = 3
    # Item caption mode: Captions must be explicitly specified.
    ITEM_CAPTION_MODE_EXPLICIT = 4
    # Item caption mode: Only icons are shown, captions are hidden.
    ITEM_CAPTION_MODE_ICON_ONLY = 5
    # Item caption mode: Item captions are read from property specified with
    # <code>setItemCaptionPropertyId</code>.

    ITEM_CAPTION_MODE_PROPERTY = 6

    class Filtering(Serializable):
        """Interface for option filtering, used to filter options based on user
        entered value. The value is matched to the item caption.
        <code>FILTERINGMODE_OFF</code> (0) turns the filtering off.
        <code>FILTERINGMODE_STARTSWITH</code> (1) matches from the start of the
        caption. <code>FILTERINGMODE_CONTAINS</code> (1) matches anywhere in the
        caption.
        """
        FILTERINGMODE_OFF = 0
        FILTERINGMODE_STARTSWITH = 1
        FILTERINGMODE_CONTAINS = 2

        def setFilteringMode(self, filteringMode):
            """Sets the option filtering mode.

            @param filteringMode
                       the filtering mode to use
            """
            pass

        def getFilteringMode(self):
            """Gets the current filtering mode.

            @return the filtering mode in use
            """
            pass

    class MultiSelectMode(object):
        """Multi select modes that controls how multi select behaves."""
        # The default behavior of the multi select mode
        # The previous more simple behavior of the multselect
        # Is the select in multiselect mode?
        DEFAULT = 'DEFAULT'
        SIMPLE = 'SIMPLE'
        _values = [DEFAULT, SIMPLE]

        @classmethod
        def values(cls):
            return cls._enum_values[:]

    _multiSelect = False
    # Select options.
    items = None
    # Is the user allowed to add new options?
    _allowNewOptions = None
    # Keymapper used to map key values.
    itemIdMapper = KeyMapper()
    # Item icons.
    _itemIcons = dict()
    # Item captions.
    _itemCaptions = dict()
    # Item caption mode.
    _itemCaptionMode = ITEM_CAPTION_MODE_EXPLICIT_DEFAULTS_ID
    # Item caption source property id.
    _itemCaptionPropertyId = None
    # Item icon source property id.
    _itemIconPropertyId = None
    # List of property set change event listeners.
    _propertySetEventListeners = None
    # List of item set change event listeners.
    _itemSetEventListeners = None
    # Item id that represents null selection of this select.
    # 
    # <p>
    # Data interface does not support nulls as item ids. Selecting the item
    # identified by this id is the same as selecting no items at all. This
    # setting only affects the single select mode.
    # </p>

    _nullSelectionItemId = None
    # Null (empty) selection is enabled by default
    _nullSelectionAllowed = True
    _newItemHandler = None
    # Caption (Item / Property) change listeners
    _captionChangeListener = None
    # Constructors

    def __init__(self, *args):
        """Creates an empty Select. The caption is not used.
        ---
        Creates an empty Select with caption.
        ---
        Creates a new select that is connected to a data-source.

        @param caption
                   the Caption of the component.
        @param dataSource
                   the Container datasource to be selected from by this select.
        ---
        Creates a new select that is filled from a collection of option values.

        @param caption
                   the Caption of this field.
        @param options
                   the Collection containing the options.
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.setContainerDataSource(IndexedContainer())
        elif _1 == 1:
            caption, = _0
            self.setContainerDataSource(IndexedContainer())
            self.setCaption(caption)
        elif _1 == 2:
            if isinstance(_0[1], Collection):
                caption, options = _0
                c = IndexedContainer()
                if options is not None:
                    _0 = True
                    i = options
                    while True:
                        if _0 is True:
                            _0 = False
                        if not i.hasNext():
                            break
                        c.addItem(i.next())
                self.setCaption(caption)
                self.setContainerDataSource(c)
            else:
                caption, dataSource = _0
                self.setCaption(caption)
                self.setContainerDataSource(dataSource)
        else:
            raise ARGERROR(0, 2)

    # Creates the options container and add given options to it
    # Component methods

    def paintContent(self, target):
        """Paints the content of this component.

        @param target
                   the Paint Event.
        @throws PaintException
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
        else:
            selectedKeys = [None] * (0 if self.getValue() is None and self.getNullSelectionItemId() is None else 1)
        # ==
        # first remove all previous item/property listeners
        self.getCaptionChangeListener().clear()
        # Paints the options and create array of selected id keys
        target.startTag('options')
        keyIndex = 0
        # Support for external null selection item id
        ids = self.getItemIds()
        if (
            self.isNullSelectionAllowed() and self.getNullSelectionItemId() is not None and not ids.contains(self.getNullSelectionItemId())
        ):
            id = self.getNullSelectionItemId()
            # Paints option
            target.startTag('so')
            self.paintItem(target, id)
            if self.isSelected(id):
                selectedKeys[POSTINC(globals(), locals(), 'keyIndex')] = self.itemIdMapper.key(id)
            target.endTag('so')
        i = self.getItemIds()
        # Paints the available selection options from data source
        while i.hasNext():
            # Gets the option attribute values
            id = i.next()
            if (
                not self.isNullSelectionAllowed() and id is not None and id == self.getNullSelectionItemId()
            ):
                # Remove item if it's the null selection item but null
                # selection is not allowed
                continue
            key = self.itemIdMapper.key(id)
            # add listener for each item, to cause repaint if an item changes
            self.getCaptionChangeListener().addNotifierForItem(id)
            target.startTag('so')
            self.paintItem(target, id)
            if self.isSelected(id) and keyIndex < len(selectedKeys):
                selectedKeys[POSTINC(globals(), locals(), 'keyIndex')] = key
            target.endTag('so')
        target.endTag('options')
        # ==
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
        if itemId is not None and itemId == self.getNullSelectionItemId():
            target.addAttribute('nullselection', True)
        target.addAttribute('key', key)
        if self.isSelected(itemId):
            target.addAttribute('selected', True)

    def changeVariables(self, source, variables):
        """Invoked when the value of a variable has changed.

        @see com.vaadin.ui.AbstractComponent#changeVariables(java.lang.Object,
             java.util.Map)
        """
        super(AbstractSelect, self).changeVariables(source, variables)
        # New option entered (and it is allowed)
        if self.isNewItemsAllowed():
            newitem = variables['newitem']
            if newitem is not None and len(newitem) > 0:
                self.getNewItemHandler().addNewItem(newitem)
        # Selection change
        if 'selected' in variables:
            ka = variables['selected']
            # Multiselect mode
            if self.isMultiSelect():
                # TODO Optimize by adding repaintNotNeeded when applicable
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
                    if (
                        not self.isNullSelectionAllowed() and (id is None) or (id == self.getNullSelectionItemId())
                    ):
                        # skip empty selection if nullselection is not allowed
                        self.requestRepaint()
                    elif id is not None and self.containsId(id):
                        s.add(id)
                if not self.isNullSelectionAllowed() and len(s) < 1:
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
                    newsel.removeAll(visible)
                    newsel.addAll(s)
                    self.setValue(newsel, True)
            else:
                # Single select mode
                if (
                    not self.isNullSelectionAllowed() and ((len(ka) == 0) or (ka[0] is None)) or (ka[0] == self.getNullSelectionItemId())
                ):
                    self.requestRepaint()
                    return
                if len(ka) == 0:
                    # Allows deselection only if the deselected item is
                    # visible
                    current = self.getValue()
                    visible = self.getVisibleItemIds()
                    if visible is not None and visible.contains(current):
                        self.setValue(None, True)
                else:
                    id = self.itemIdMapper.get(ka[0])
                    if not self.isNullSelectionAllowed() and id is None:
                        self.requestRepaint()
                    elif id is not None and id == self.getNullSelectionItemId():
                        self.setValue(None, True)
                    else:
                        self.setValue(id, True)

    def setNewItemHandler(self, newItemHandler):
        """TODO refine doc Setter for new item handler that is called when user adds
        new item in newItemAllowed mode.

        @param newItemHandler
        """
        self._newItemHandler = newItemHandler

    def getNewItemHandler(self):
        """TODO refine doc

        @return
        """
        if self._newItemHandler is None:
            self._newItemHandler = self.DefaultNewItemHandler()
        return self._newItemHandler

    class NewItemHandler(Serializable):

        def addNewItem(self, newItemCaption):
            pass

    class DefaultNewItemHandler(NewItemHandler):
        """TODO refine doc

        This is a default class that handles adding new items that are typed by
        user to selects container.

        By extending this class one may implement some logic on new item addition
        like database inserts.
        """

        def addNewItem(self, newItemCaption):
            # Checks for readonly
            if self.isReadOnly():
                raise Property.ReadOnlyException()
            # Adds new option
            if self.addItem(newItemCaption) is not None:
                # Sets the caption property, if used
                if self.getItemCaptionPropertyId() is not None:
                    # The conversion exception is safely ignored, the
                    # caption is just missing

                    try:
                        self.getContainerProperty(newItemCaption, self.getItemCaptionPropertyId()).setValue(newItemCaption)
                    except Property.ConversionException, ignored:
                        pass # astStmt: [Stmt([]), None]
                if self.isMultiSelect():
                    values = set(self.getValue())
                    values.add(newItemCaption)
                    self.setValue(values)
                else:
                    self.setValue(newItemCaption)

    def getVisibleItemIds(self):
        """Gets the visible item ids. In Select, this returns list of all item ids,
        but can be overriden in subclasses if they paint only part of the items
        to the terminal or null if no items is visible.
        """
        # Property methods
        if self.isVisible():
            return self.getItemIds()
        return None

    def getType(self, *args):
        """Returns the type of the property. <code>getValue</code> and
        <code>setValue</code> methods must be compatible with this type: one can
        safely cast <code>getValue</code> to given type and pass any variable
        assignable to this type as a parameter to <code>setValue</code>.

        @return the Type of the property.
        ---
        Gets the property type.

        @param propertyId
                   the Id identifying the property.
        @see com.vaadin.data.Container#getType(java.lang.Object)
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            if self.isMultiSelect():
                return set
            else:
                return self.Object
        elif _1 == 1:
            propertyId, = _0
            return self.items.getType(propertyId)
        else:
            raise ARGERROR(0, 1)

    def getValue(self):
        """Gets the selected item id or in multiselect mode a set of selected ids.

        @see com.vaadin.ui.AbstractField#getValue()
        """
        retValue = super(AbstractSelect, self).getValue()
        if self.isMultiSelect():
            # If the return value is not a set
            if retValue is None:
                return set()
            if isinstance(retValue, set):
                return Collections.unmodifiableSet(retValue)
            elif isinstance(retValue, Collection):
                return set(retValue)
            else:
                s = set()
                if self.items.containsId(retValue):
                    s.add(retValue)
                return s
        else:
            return retValue

    def setValue(self, *args):
        """Sets the visible value of the property.

        <p>
        The value of the select is the selected item id. If the select is in
        multiselect-mode, the value is a set of selected item keys. In
        multiselect mode all collections of id:s can be assigned.
        </p>

        @param newValue
                   the New selected item or collection of selected items.
        @see com.vaadin.ui.AbstractField#setValue(java.lang.Object)
        ---
        Sets the visible value of the property.

        <p>
        The value of the select is the selected item id. If the select is in
        multiselect-mode, the value is a set of selected item keys. In
        multiselect mode all collections of id:s can be assigned.
        </p>

        @param newValue
                   the New selected item or collection of selected items.
        @param repaintIsNotNeeded
                   True if caller is sure that repaint is not needed.
        @see com.vaadin.ui.AbstractField#setValue(java.lang.Object,
             java.lang.Boolean)
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            newValue, = _0
            if newValue == self.getNullSelectionItemId():
                newValue = None
            self.setValue(newValue, False)
        elif _1 == 2:
            newValue, repaintIsNotNeeded = _0
            if self.isMultiSelect():
                if newValue is None:
                    super(AbstractSelect, self).setValue(set(), repaintIsNotNeeded)
                elif Collection.isAssignableFrom(newValue.getClass()):
                    super(AbstractSelect, self).setValue(set(newValue), repaintIsNotNeeded)
            elif (newValue is None) or self.items.containsId(newValue):
                super(AbstractSelect, self).setValue(newValue, repaintIsNotNeeded)
        else:
            raise ARGERROR(1, 2)

    # Container methods

    def getItem(self, itemId):
        """Gets the item from the container with given id. If the container does not
        contain the requested item, null is returned.

        @param itemId
                   the item id.
        @return the item from the container.
        """
        return self.items.getItem(itemId)

    def getItemIds(self):
        """Gets the item Id collection from the container.

        @return the Collection of item ids.
        """
        return self.items.getItemIds()

    def getContainerPropertyIds(self):
        """Gets the property Id collection from the container.

        @return the Collection of property ids.
        """
        return self.items.getContainerPropertyIds()

    # Gets the number of items in the container.
    # 
    # @return the Number of items in the container.
    # 
    # @see com.vaadin.data.Container#size()

    def size(self):
        return len(self.items)

    def containsId(self, itemId):
        """Tests, if the collection contains an item with given id.

        @param itemId
                   the Id the of item to be tested.
        """
        if itemId is not None:
            return self.items.containsId(itemId)
        else:
            return False

    def getContainerProperty(self, itemId, propertyId):
        """Gets the Property identified by the given itemId and propertyId from the
        Container

        @see com.vaadin.data.Container#getContainerProperty(Object, Object)
        """
        return self.items.getContainerProperty(itemId, propertyId)

    def addContainerProperty(self, propertyId, type, defaultValue):
        """Adds the new property to all items. Adds a property with given id, type
        and default value to all items in the container.

        This functionality is optional. If the function is unsupported, it always
        returns false.

        @return True if the operation succeeded.
        @see com.vaadin.data.Container#addContainerProperty(java.lang.Object,
             java.lang.Class, java.lang.Object)
        """
        retval = self.items.addContainerProperty(propertyId, type, defaultValue)
        if retval and not isinstance(self.items, Container.PropertySetChangeNotifier):
            self.firePropertySetChange()
        return retval

    def removeAllItems(self):
        """Removes all items from the container.

        This functionality is optional. If the function is unsupported, it always
        returns false.

        @return True if the operation succeeded.
        @see com.vaadin.data.Container#removeAllItems()
        """
        retval = self.items.removeAllItems()
        self.itemIdMapper.removeAll()
        if retval:
            self.setValue(None)
            if not isinstance(self.items, Container.ItemSetChangeNotifier):
                self.fireItemSetChange()
        return retval

    def addItem(self, *args):
        """Creates a new item into container with container managed id. The id of
        the created new item is returned. The item can be fetched with getItem()
        method. if the creation fails, null is returned.

        @return the Id of the created item or null in case of failure.
        @see com.vaadin.data.Container#addItem()
        ---
        Create a new item into container. The created new item is returned and
        ready for setting property values. if the creation fails, null is
        returned. In case the container already contains the item, null is
        returned.

        This functionality is optional. If the function is unsupported, it always
        returns null.

        @param itemId
                   the Identification of the item to be created.
        @return the Created item with the given id, or null in case of failure.
        @see com.vaadin.data.Container#addItem(java.lang.Object)
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            retval = self.items.addItem()
            if (
                retval is not None and not isinstance(self.items, Container.ItemSetChangeNotifier)
            ):
                self.fireItemSetChange()
            return retval
        elif _1 == 1:
            itemId, = _0
            retval = self.items.addItem(itemId)
            if (
                retval is not None and not isinstance(self.items, Container.ItemSetChangeNotifier)
            ):
                self.fireItemSetChange()
            return retval
        else:
            raise ARGERROR(0, 1)

    # (non-Javadoc)
    # 
    # @see com.vaadin.data.Container#removeItem(java.lang.Object)

    def removeItem(self, itemId):
        self.unselect(itemId)
        retval = self.items.removeItem(itemId)
        self.itemIdMapper.remove(itemId)
        if retval and not isinstance(self.items, Container.ItemSetChangeNotifier):
            self.fireItemSetChange()
        return retval

    def removeContainerProperty(self, propertyId):
        """Removes the property from all items. Removes a property with given id
        from all the items in the container.

        This functionality is optional. If the function is unsupported, it always
        returns false.

        @return True if the operation succeeded.
        @see com.vaadin.data.Container#removeContainerProperty(java.lang.Object)
        """
        # Container.Viewer methods
        retval = self.items.removeContainerProperty(propertyId)
        if retval and not isinstance(self.items, Container.PropertySetChangeNotifier):
            self.firePropertySetChange()
        return retval

    def setContainerDataSource(self, newDataSource):
        """Sets the Container that serves as the data source of the viewer.

        As a side-effect the fields value (selection) is set to null due old
        selection not necessary exists in new Container.

        @see com.vaadin.data.Container.Viewer#setContainerDataSource(Container)

        @param newDataSource
                   the new data source.
        """
        if newDataSource is None:
            newDataSource = IndexedContainer()
        self.getCaptionChangeListener().clear()
        if self.items != newDataSource:
            # Removes listeners from the old datasource
            if self.items is not None:
                if isinstance(self.items, Container.ItemSetChangeNotifier):
                    self.items.removeListener(self)
                if isinstance(self.items, Container.PropertySetChangeNotifier):
                    self.items.removeListener(self)
            # Assigns new data source
            self.items = newDataSource
            # Clears itemIdMapper also
            self.itemIdMapper.removeAll()
            # Adds listeners
            if self.items is not None:
                if isinstance(self.items, Container.ItemSetChangeNotifier):
                    self.items.addListener(self)
                if isinstance(self.items, Container.PropertySetChangeNotifier):
                    self.items.addListener(self)
            # We expect changing the data source should also clean value. See
            # #810, #4607, #5281

            self.setValue(None)
            self.requestRepaint()

    def getContainerDataSource(self):
        """Gets the viewing data-source container.

        @see com.vaadin.data.Container.Viewer#getContainerDataSource()
        """
        # Select attributes
        return self.items

    def isMultiSelect(self):
        """Is the select in multiselect mode? In multiselect mode

        @return the Value of property multiSelect.
        """
        return self._multiSelect

    def setMultiSelect(self, multiSelect):
        """Sets the multiselect mode. Setting multiselect mode false may loose
        selection information: if selected items set contains one or more
        selected items, only one of the selected items is kept as selected.

        @param multiSelect
                   the New value of property multiSelect.
        """
        if multiSelect and self.getNullSelectionItemId() is not None:
            raise self.IllegalStateException('Multiselect and NullSelectionItemId can not be set at the same time.')
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
                if (s is None) or s.isEmpty():
                    self.setValue(None)
                else:
                    # Set the single select to contain only the first
                    # selected value in the multiselect
                    self.setValue(s.next())
            self.requestRepaint()

    def isNewItemsAllowed(self):
        """Does the select allow adding new options by the user. If true, the new
        options can be added to the Container. The text entered by the user is
        used as id. Note that data-source must allow adding new items.

        @return True if additions are allowed.
        """
        return self._allowNewOptions

    def setNewItemsAllowed(self, allowNewOptions):
        """Enables or disables possibility to add new options by the user.

        @param allowNewOptions
                   the New value of property allowNewOptions.
        """
        # Only handle change requests
        if self._allowNewOptions != allowNewOptions:
            self._allowNewOptions = allowNewOptions
            self.requestRepaint()

    def setItemCaption(self, itemId, caption):
        """Override the caption of an item. Setting caption explicitly overrides id,
        item and index captions.

        @param itemId
                   the id of the item to be recaptioned.
        @param caption
                   the New caption.
        """
        if itemId is not None:
            self._itemCaptions.put(itemId, caption)
            self.requestRepaint()

    def getItemCaption(self, itemId):
        """Gets the caption of an item. The caption is generated as specified by the
        item caption mode. See <code>setItemCaptionMode()</code> for more
        details.

        @param itemId
                   the id of the item to be queried.
        @return the caption for specified item.
        """
        # Null items can not be found
        if itemId is None:
            return None
        caption = None
        _0 = self.getItemCaptionMode()
        _1 = False
        while True:
            if _0 == self.ITEM_CAPTION_MODE_ID:
                _1 = True
                caption = str(itemId)
                break
            if (_1 is True) or (_0 == self.ITEM_CAPTION_MODE_INDEX):
                _1 = True
                if isinstance(self.items, Container.Indexed):
                    caption = String.valueOf.valueOf(self.items.indexOfId(itemId))
                else:
                    caption = 'ERROR: Container is not indexed'
                break
            if (_1 is True) or (_0 == self.ITEM_CAPTION_MODE_ITEM):
                _1 = True
                i = self.getItem(itemId)
                if i is not None:
                    caption = str(i)
                break
            if (_1 is True) or (_0 == self.ITEM_CAPTION_MODE_EXPLICIT):
                _1 = True
                caption = self._itemCaptions[itemId]
                break
            if (_1 is True) or (_0 == self.ITEM_CAPTION_MODE_EXPLICIT_DEFAULTS_ID):
                _1 = True
                caption = self._itemCaptions[itemId]
                if caption is None:
                    caption = str(itemId)
                break
            if (_1 is True) or (_0 == self.ITEM_CAPTION_MODE_PROPERTY):
                _1 = True
                p = self.getContainerProperty(itemId, self.getItemCaptionPropertyId())
                if p is not None:
                    caption = str(p)
                break
            break
        # All items must have some captions
        return caption if caption is not None else ''

    def setItemIcon(self, itemId, icon):
        """Sets the icon for an item.

        @param itemId
                   the id of the item to be assigned an icon.
        @param icon
                   the icon to use or null.
        """
        if itemId is not None:
            if icon is None:
                self._itemIcons.remove(itemId)
            else:
                self._itemIcons.put(itemId, icon)
            self.requestRepaint()

    def getItemIcon(self, itemId):
        """Gets the item icon.

        @param itemId
                   the id of the item to be assigned an icon.
        @return the icon for the item or null, if not specified.
        """
        explicit = self._itemIcons[itemId]
        if explicit is not None:
            return explicit
        if self.getItemIconPropertyId() is None:
            return None
        ip = self.getContainerProperty(itemId, self.getItemIconPropertyId())
        if ip is None:
            return None
        icon = ip.getValue()
        if isinstance(icon, Resource):
            return icon
        return None

    def setItemCaptionMode(self, mode):
        """Sets the item caption mode.

        <p>
        The mode can be one of the following ones:
        <ul>
        <li><code>ITEM_CAPTION_MODE_EXPLICIT_DEFAULTS_ID</code> : Items
        Id-objects <code>toString</code> is used as item caption. If caption is
        explicitly specified, it overrides the id-caption.
        <li><code>ITEM_CAPTION_MODE_ID</code> : Items Id-objects
        <code>toString</code> is used as item caption.</li>
        <li><code>ITEM_CAPTION_MODE_ITEM</code> : Item-objects
        <code>toString</code> is used as item caption.</li>
        <li><code>ITEM_CAPTION_MODE_INDEX</code> : The index of the item is used
        as item caption. The index mode can only be used with the containers
        implementing <code>Container.Indexed</code> interface.</li>
        <li><code>ITEM_CAPTION_MODE_EXPLICIT</code> : The item captions must be
        explicitly specified.</li>
        <li><code>ITEM_CAPTION_MODE_PROPERTY</code> : The item captions are read
        from property, that must be specified with
        <code>setItemCaptionPropertyId</code>.</li>
        </ul>
        The <code>ITEM_CAPTION_MODE_EXPLICIT_DEFAULTS_ID</code> is the default
        mode.
        </p>

        @param mode
                   the One of the modes listed above.
        """
        if (
            self.ITEM_CAPTION_MODE_ID <= mode and mode <= self.ITEM_CAPTION_MODE_PROPERTY
        ):
            self._itemCaptionMode = mode
            self.requestRepaint()

    def getItemCaptionMode(self):
        """Gets the item caption mode.

        <p>
        The mode can be one of the following ones:
        <ul>
        <li><code>ITEM_CAPTION_MODE_EXPLICIT_DEFAULTS_ID</code> : Items
        Id-objects <code>toString</code> is used as item caption. If caption is
        explicitly specified, it overrides the id-caption.
        <li><code>ITEM_CAPTION_MODE_ID</code> : Items Id-objects
        <code>toString</code> is used as item caption.</li>
        <li><code>ITEM_CAPTION_MODE_ITEM</code> : Item-objects
        <code>toString</code> is used as item caption.</li>
        <li><code>ITEM_CAPTION_MODE_INDEX</code> : The index of the item is used
        as item caption. The index mode can only be used with the containers
        implementing <code>Container.Indexed</code> interface.</li>
        <li><code>ITEM_CAPTION_MODE_EXPLICIT</code> : The item captions must be
        explicitly specified.</li>
        <li><code>ITEM_CAPTION_MODE_PROPERTY</code> : The item captions are read
        from property, that must be specified with
        <code>setItemCaptionPropertyId</code>.</li>
        </ul>
        The <code>ITEM_CAPTION_MODE_EXPLICIT_DEFAULTS_ID</code> is the default
        mode.
        </p>

        @return the One of the modes listed above.
        """
        return self._itemCaptionMode

    def setItemCaptionPropertyId(self, propertyId):
        """Sets the item caption property.

        <p>
        Setting the id to a existing property implicitly sets the item caption
        mode to <code>ITEM_CAPTION_MODE_PROPERTY</code>. If the object is in
        <code>ITEM_CAPTION_MODE_PROPERTY</code> mode, setting caption property id
        null resets the item caption mode to
        <code>ITEM_CAPTION_EXPLICIT_DEFAULTS_ID</code>.
        </p>

        <p>
        Setting the property id to null disables this feature. The id is null by
        default
        </p>
        .

        @param propertyId
                   the id of the property.
        """
        if propertyId is not None:
            self._itemCaptionPropertyId = propertyId
            self.setItemCaptionMode(self.ITEM_CAPTION_MODE_PROPERTY)
            self.requestRepaint()
        else:
            self._itemCaptionPropertyId = None
            if self.getItemCaptionMode() == self.ITEM_CAPTION_MODE_PROPERTY:
                self.setItemCaptionMode(self.ITEM_CAPTION_MODE_EXPLICIT_DEFAULTS_ID)
            self.requestRepaint()

    def getItemCaptionPropertyId(self):
        """Gets the item caption property.

        @return the Id of the property used as item caption source.
        """
        return self._itemCaptionPropertyId

    def setItemIconPropertyId(self, propertyId):
        """Sets the item icon property.

        <p>
        If the property id is set to a valid value, each item is given an icon
        got from the given property of the items. The type of the property must
        be assignable to Resource.
        </p>

        <p>
        Note : The icons set with <code>setItemIcon</code> function override the
        icons from the property.
        </p>

        <p>
        Setting the property id to null disables this feature. The id is null by
        default
        </p>
        .

        @param propertyId
                   the id of the property that specifies icons for items or null
        @throws IllegalArgumentException
                    If the propertyId is not in the container or is not of a
                    valid type
        """
        if propertyId is None:
            self._itemIconPropertyId = None
        elif not self.getContainerPropertyIds().contains(propertyId):
            raise self.IllegalArgumentException('Property id not found in the container')
        elif Resource.isAssignableFrom(self.getType(propertyId)):
            self._itemIconPropertyId = propertyId
        else:
            raise self.IllegalArgumentException('Property type must be assignable to Resource')
        self.requestRepaint()

    def getItemIconPropertyId(self):
        """Gets the item icon property.

        <p>
        If the property id is set to a valid value, each item is given an icon
        got from the given property of the items. The type of the property must
        be assignable to Icon.
        </p>

        <p>
        Note : The icons set with <code>setItemIcon</code> function override the
        icons from the property.
        </p>

        <p>
        Setting the property id to null disables this feature. The id is null by
        default
        </p>
        .

        @return the Id of the property containing the item icons.
        """
        return self._itemIconPropertyId

    def isSelected(self, itemId):
        """Tests if an item is selected.

        <p>
        In single select mode testing selection status of the item identified by
        {@link #getNullSelectionItemId()} returns true if the value of the
        property is null.
        </p>

        @param itemId
                   the Id the of the item to be tested.
        @see #getNullSelectionItemId()
        @see #setNullSelectionItemId(Object)
        """
        if itemId is None:
            return False
        if self.isMultiSelect():
            return self.getValue().contains(itemId)
        else:
            value = self.getValue()
            return itemId == self.getNullSelectionItemId() if value is None else value

    def select(self, itemId):
        """Selects an item.

        <p>
        In single select mode selecting item identified by
        {@link #getNullSelectionItemId()} sets the value of the property to null.
        </p>

        @param itemId
                   the identifier of Item to be selected.
        @see #getNullSelectionItemId()
        @see #setNullSelectionItemId(Object)
        """
        if not self.isMultiSelect():
            self.setValue(itemId)
        elif (
            not self.isSelected(itemId) and itemId is not None and self.items.containsId(itemId)
        ):
            s = set(self.getValue())
            s.add(itemId)
            self.setValue(s)

    def unselect(self, itemId):
        """Unselects an item.

        @param itemId
                   the identifier of the Item to be unselected.
        @see #getNullSelectionItemId()
        @see #setNullSelectionItemId(Object)
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

        @see com.vaadin.data.Container.PropertySetChangeListener#containerPropertySetChange(com.vaadin.data.Container.PropertySetChangeEvent)
        """
        self.firePropertySetChange()

    def addListener(self, *args):
        """Adds a new Property set change listener for this Container.

        @see com.vaadin.data.Container.PropertySetChangeNotifier#addListener(com.vaadin.data.Container.PropertySetChangeListener)
        ---
        Adds an Item set change listener for the object.

        @see com.vaadin.data.Container.ItemSetChangeNotifier#addListener(com.vaadin.data.Container.ItemSetChangeListener)
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Container.ItemSetChangeListener):
                listener, = _0
                if self._itemSetEventListeners is None:
                    self._itemSetEventListeners = LinkedHashSet()
                self._itemSetEventListeners.add(listener)
            else:
                listener, = _0
                if self._propertySetEventListeners is None:
                    self._propertySetEventListeners = LinkedHashSet()
                self._propertySetEventListeners.add(listener)
        else:
            raise ARGERROR(1, 1)

    def removeListener(self, *args):
        """Removes a previously registered Property set change listener.

        @see com.vaadin.data.Container.PropertySetChangeNotifier#removeListener(com.vaadin.data.Container.PropertySetChangeListener)
        ---
        Removes the Item set change listener from the object.

        @see com.vaadin.data.Container.ItemSetChangeNotifier#removeListener(com.vaadin.data.Container.ItemSetChangeListener)
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Container.ItemSetChangeListener):
                listener, = _0
                if self._itemSetEventListeners is not None:
                    self._itemSetEventListeners.remove(listener)
                    if self._itemSetEventListeners.isEmpty():
                        self._itemSetEventListeners = None
            else:
                listener, = _0
                if self._propertySetEventListeners is not None:
                    self._propertySetEventListeners.remove(listener)
                    if self._propertySetEventListeners.isEmpty():
                        self._propertySetEventListeners = None
        else:
            raise ARGERROR(1, 1)

    def getListeners(self, eventType):
        if Container.ItemSetChangeEvent.isAssignableFrom(eventType):
            if self._itemSetEventListeners is None:
                return Collections.EMPTY_LIST
            else:
                return Collections.unmodifiableCollection(self._itemSetEventListeners)
        elif Container.PropertySetChangeEvent.isAssignableFrom(eventType):
            if self._propertySetEventListeners is None:
                return Collections.EMPTY_LIST
            else:
                return Collections.unmodifiableCollection(self._propertySetEventListeners)
        return super(AbstractSelect, self).getListeners(eventType)

    def containerItemSetChange(self, event):
        """Lets the listener know a Containers Item set has changed.

        @see com.vaadin.data.Container.ItemSetChangeListener#containerItemSetChange(com.vaadin.data.Container.ItemSetChangeEvent)
        """
        # Clears the item id mapping table
        self.itemIdMapper.removeAll()
        # Notify all listeners
        self.fireItemSetChange()

    def firePropertySetChange(self):
        """Fires the property set change event."""
        if (
            self._propertySetEventListeners is not None and not self._propertySetEventListeners.isEmpty()
        ):
            event = PropertySetChangeEvent()
            listeners = list(self._propertySetEventListeners)
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(listeners)):
                    break
                listeners[i].containerPropertySetChange(event)
        self.requestRepaint()

    def fireItemSetChange(self):
        """Fires the item set change event."""
        if (
            self._itemSetEventListeners is not None and not self._itemSetEventListeners.isEmpty()
        ):
            event = ItemSetChangeEvent()
            listeners = list(self._itemSetEventListeners)
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(listeners)):
                    break
                listeners[i].containerItemSetChange(event)
        self.requestRepaint()

    class ItemSetChangeEvent(Serializable, Container, ItemSetChangeEvent):
        """Implementation of item set change event."""

        def getContainer(self):
            """Gets the Property where the event occurred.

            @see com.vaadin.data.Container.ItemSetChangeEvent#getContainer()
            """
            return _AbstractSelect_this

    class PropertySetChangeEvent(Container, PropertySetChangeEvent, Serializable):
        """Implementation of property set change event."""

        def getContainer(self):
            """Retrieves the Container whose contents have been modified.

            @see com.vaadin.data.Container.PropertySetChangeEvent#getContainer()
            """
            return _AbstractSelect_this

    def isEmpty(self):
        """For multi-selectable fields, also an empty collection of values is
        considered to be an empty field.

        @see AbstractField#isEmpty().
        """
        if not self._multiSelect:
            return super(AbstractSelect, self).isEmpty()
        else:
            value = self.getValue()
            return super(AbstractSelect, self).isEmpty() or (isinstance(value, Collection) and value.isEmpty())

    def setNullSelectionAllowed(self, nullSelectionAllowed):
        """Allow or disallow empty selection by the user. If the select is in
        single-select mode, you can make an item represent the empty selection by
        calling <code>setNullSelectionItemId()</code>. This way you can for
        instance set an icon and caption for the null selection item.

        @param nullSelectionAllowed
                   whether or not to allow empty selection
        @see #setNullSelectionItemId(Object)
        @see #isNullSelectionAllowed()
        """
        if nullSelectionAllowed != self._nullSelectionAllowed:
            self._nullSelectionAllowed = nullSelectionAllowed
            self.requestRepaint()

    def isNullSelectionAllowed(self):
        """Checks if null empty selection is allowed by the user.

        @return whether or not empty selection is allowed
        @see #setNullSelectionAllowed(boolean)
        """
        return self._nullSelectionAllowed

    def getNullSelectionItemId(self):
        """Returns the item id that represents null value of this select in single
        select mode.

        <p>
        Data interface does not support nulls as item ids. Selecting the item
        identified by this id is the same as selecting no items at all. This
        setting only affects the single select mode.
        </p>

        @return the Object Null value item id.
        @see #setNullSelectionItemId(Object)
        @see #isSelected(Object)
        @see #select(Object)
        """
        return self._nullSelectionItemId

    def setNullSelectionItemId(self, nullSelectionItemId):
        """Sets the item id that represents null value of this select.

        <p>
        Data interface does not support nulls as item ids. Selecting the item
        idetified by this id is the same as selecting no items at all. This
        setting only affects the single select mode.
        </p>

        @param nullSelectionItemId
                   the nullSelectionItemId to set.
        @see #getNullSelectionItemId()
        @see #isSelected(Object)
        @see #select(Object)
        """
        if nullSelectionItemId is not None and self.isMultiSelect():
            raise self.IllegalStateException('Multiselect and NullSelectionItemId can not be set at the same time.')
        self._nullSelectionItemId = nullSelectionItemId

    def attach(self):
        """Notifies the component that it is connected to an application.

        @see com.vaadin.ui.AbstractField#attach()
        """
        super(AbstractSelect, self).attach()

    def detach(self):
        """Detaches the component from application.

        @see com.vaadin.ui.AbstractComponent#detach()
        """
        # Caption change listener
        self.getCaptionChangeListener().clear()
        super(AbstractSelect, self).detach()

    def getCaptionChangeListener(self):
        if self._captionChangeListener is None:
            self._captionChangeListener = self.CaptionChangeListener()
        return self._captionChangeListener

    class CaptionChangeListener(Item, PropertySetChangeListener, Property, ValueChangeListener):
        """This is a listener helper for Item and Property changes that should cause
        a repaint. It should be attached to all items that are displayed, and the
        default implementation does this in paintContent(). Especially
        "lazyloading" components should take care to add and remove listeners as
        appropriate. Call addNotifierForItem() for each painted item (and
        remember to clear).

        NOTE: singleton, use getCaptionChangeListener().
        """
        # TODO clean this up - type is either Item.PropertySetChangeNotifier or
        # Property.ValueChangeNotifier
        _captionChangeNotifiers = set()

        def addNotifierForItem(self, itemId):
            _0 = self.getItemCaptionMode()
            _1 = False
            while True:
                if _0 == self.ITEM_CAPTION_MODE_ITEM:
                    _1 = True
                    i = self.getItem(itemId)
                    if i is None:
                        return
                    if isinstance(i, Item.PropertySetChangeNotifier):
                        i.addListener(self.getCaptionChangeListener())
                        self._captionChangeNotifiers.add(i)
                    pids = i.getItemPropertyIds()
                    if pids is not None:
                        _2 = True
                        it = pids
                        while True:
                            if _2 is True:
                                _2 = False
                            if not it.hasNext():
                                break
                            p = i.getItemProperty(it.next())
                            if p is not None and isinstance(p, Property.ValueChangeNotifier):
                                p.addListener(self.getCaptionChangeListener())
                                self._captionChangeNotifiers.add(p)
                    break
                if (_1 is True) or (_0 == self.ITEM_CAPTION_MODE_PROPERTY):
                    _1 = True
                    p = self.getContainerProperty(itemId, self.getItemCaptionPropertyId())
                    if p is not None and isinstance(p, Property.ValueChangeNotifier):
                        p.addListener(self.getCaptionChangeListener())
                        self._captionChangeNotifiers.add(p)
                    break
                break

        def clear(self):
            _0 = True
            it = self._captionChangeNotifiers
            while True:
                if _0 is True:
                    _0 = False
                if not it.hasNext():
                    break
                notifier = it.next()
                if isinstance(notifier, Item.PropertySetChangeNotifier):
                    notifier.removeListener(self.getCaptionChangeListener())
                else:
                    notifier.removeListener(self.getCaptionChangeListener())
            self._captionChangeNotifiers.clear()

        def valueChange(self, event):
            self.requestRepaint()

        def itemPropertySetChange(self, event):
            self.requestRepaint()

    class TargetItemIs(AbstractItemSetCriterion):
        """Criterion which accepts a drop only if the drop target is (one of) the
        given Item identifier(s). Criterion can be used only on a drop targets
        that extends AbstractSelect like {@link Table} and {@link Tree}. The
        target and identifiers of valid Items are given in constructor.

        @since 6.3
        """

        def __init__(self, select, *itemId):
            """@param select
                       the select implementation that is used as a drop target
            @param itemId
                       the identifier(s) that are valid drop locations
            """
            super(TargetItemIs, self)(select, itemId)

        def accept(self, dragEvent):
            dropTargetData = dragEvent.getTargetDetails()
            if dropTargetData.getTarget() != self.select:
                return False
            return self.itemIds.contains(dropTargetData.getItemIdOver())

    class AbstractItemSetCriterion(ClientSideCriterion):
        """Abstract helper class to implement item id based criterion.

        Note, inner class used not to open itemIdMapper for public access.

        @since 6.3
        """
        itemIds = set()
        select = None

        def __init__(self, select, *itemId):
            if (self.itemIds is None) or (select is None):
                raise self.IllegalArgumentException('Accepted item identifiers must be accepted.')
            Collections.addAll(self.itemIds, itemId)
            self.select = select

        def paintContent(self, target):
            super(AbstractItemSetCriterion, self).paintContent(target)
            keys = [None] * len(self.itemIds)
            i = 0
            for itemId in self.itemIds:
                key = self.select.itemIdMapper.key(itemId)
                keys[POSTINC(globals(), locals(), 'i')] = key
            target.addAttribute('keys', keys)
            target.addAttribute('s', self.select)

    class AcceptItem(AbstractItemSetCriterion):
        """This criterion accepts a only a {@link Transferable} that contains given
        Item (practically its identifier) from a specific AbstractSelect.

        @since 6.3
        """

        def __init__(self, select, *itemId):
            """@param select
                       the select from which the item id's are checked
            @param itemId
                       the item identifier(s) of the select that are accepted
            """
            super(AcceptItem, self)(select, itemId)

        def accept(self, dragEvent):
            # A simple accept criterion which ensures that {@link Transferable}
            # contains an {@link Item} (or actually its identifier). In other words
            # the criterion check that drag is coming from a {@link Container} like
            # {@link Tree} or {@link Table}.

            transferable = dragEvent.getTransferable()
            if transferable.getSourceComponent() != self.select:
                return False
            return self.itemIds.contains(transferable.getItemId())

        ALL = ContainsDataFlavor('itemId')

    class AbstractSelectTargetDetails(TargetDetailsImpl):
        """TargetDetails implementation for subclasses of {@link AbstractSelect}
        that implement {@link DropTarget}.

        @since 6.3
        """
        # The item id over which the drag event happened.
        idOver = None

        def __init__(self, rawVariables):
            """Constructor that automatically converts itemIdOver key to
            corresponding item Id
            """
            super(AbstractSelectTargetDetails, self)(rawVariables, _AbstractSelect_this)
            # eagar fetch itemid, mapper may be emptied
            keyover = self.getData('itemIdOver')
            if keyover is not None:
                self.idOver = self.itemIdMapper.get(keyover)

        def getItemIdOver(self):
            """If the drag operation is currently over an {@link Item}, this method
            returns the identifier of that {@link Item}.
            """
            return self.idOver

        def getDropLocation(self):
            """Returns a detailed vertical location where the drop happened on Item."""
            detail = self.getData('detail')
            if detail is None:
                return None
            return VerticalDropLocation.valueOf(detail)

    class VerticalLocationIs(TargetDetailIs):
        """An accept criterion to accept drops only on a specific vertical location
        of an item.
        <p>
        This accept criterion is currently usable in Tree and Table
        implementations.
        """
        TOP = self.VerticalLocationIs(VerticalDropLocation.TOP)
        BOTTOM = self.VerticalLocationIs(VerticalDropLocation.BOTTOM)
        MIDDLE = self.VerticalLocationIs(VerticalDropLocation.MIDDLE)

        def __init__(self, l):
            super(VerticalLocationIs, self)('detail', l.name())
