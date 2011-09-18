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
from com.vaadin.data.Property import (Property, ValueChangeEvent, ValueChangeNotifier,)
from com.vaadin.data.Item import (Item,)
from com.vaadin.data.util.AbstractInMemoryContainer import (AbstractInMemoryContainer,)
from com.vaadin.data.util.filter.SimpleStringFilter import (SimpleStringFilter,)
from com.vaadin.data.Container import (Container, Filterable, PropertySetChangeNotifier, SimpleFilterable, Sortable,)
# from java.io.Serializable import (Serializable,)
# from java.lang.reflect.Constructor import (Constructor,)


class IndexedContainer(AbstractInMemoryContainer, Container, PropertySetChangeNotifier, Property, ValueChangeNotifier, Container, Sortable, Cloneable, Container, Filterable, Container, SimpleFilterable):
    """An implementation of the <code>{@link Container.Indexed}</code> interface
    with all important features.</p>

    Features:
    <ul>
    <li> {@link Container.Indexed}
    <li> {@link Container.Ordered}
    <li> {@link Container.Sortable}
    <li> {@link Container.Filterable}
    <li> {@link Cloneable} (deprecated, might be removed in the future)
    <li>Sends all needed events on content changes.
    </ul>

    @see com.vaadin.data.Container

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # item type is really IndexedContainerItem, but using Item not to show it in
    # public API
    # Internal structure
    # Linked list of ordered Property IDs.
    _propertyIds = list()
    # Property ID to type mapping.
    _types = dict()
    # Hash of Items, where each Item is implemented as a mapping from Property
    # ID to Property value.

    _items = dict()
    # Set of properties that are read-only.
    _readOnlyProperties = set()
    # List of all Property value change event listeners listening all the
    # properties.

    _propertyValueChangeListeners = None
    # Data structure containing all listeners interested in changes to single
    # Properties. The data structure is a hashtable mapping Property IDs to a
    # hashtable that maps Item IDs to a linked list of listeners listening
    # Property identified by given Property ID and Item ID.

    _singlePropertyValueChangeListeners = None
    _defaultPropertyValues = None
    _nextGeneratedItemId = 1
    # Container constructors

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            super(IndexedContainer, self)()
        elif _1 == 1:
            itemIds, = _0
            self.__init__()
            if self._items is not None:
                _0 = True
                i = itemIds
                while True:
                    if _0 is True:
                        _0 = False
                    if not i.hasNext():
                        break
                    itemId = i.next()
                    self.internalAddItemAtEnd(itemId, self.IndexedContainerItem(itemId), False)
                self.filterAll()
        else:
            raise ARGERROR(0, 1)

    # Container methods

    def getUnfilteredItem(self, itemId):
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container#getContainerPropertyIds()

        if itemId is not None and itemId in self._items:
            return self.IndexedContainerItem(itemId)
        return None

    def getContainerPropertyIds(self):
        return Collections.unmodifiableCollection(self._propertyIds)

    def getType(self, propertyId):
        """Gets the type of a Property stored in the list.

        @param id
                   the ID of the Property.
        @return Type of the requested Property
        """
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container#getContainerProperty(java.lang.Object,
        # java.lang.Object)

        return self._types[propertyId]

    def getContainerProperty(self, itemId, propertyId):
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container#addContainerProperty(java.lang.Object,
        # java.lang.Class, java.lang.Object)

        if not self.containsId(itemId):
            return None
        return self.IndexedContainerProperty(itemId, propertyId)

    def addContainerProperty(self, propertyId, type, defaultValue):
        # Fails, if nulls are given
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container#removeAllItems()

        if (propertyId is None) or (type is None):
            return False
        # Fails if the Property is already present
        if self._propertyIds.contains(propertyId):
            return False
        # Adds the Property to Property list and types
        self._propertyIds.add(propertyId)
        self._types.put(propertyId, type)
        # If default value is given, set it
        if defaultValue is not None:
            # for existing rows
            _0 = True
            i = self.getAllItemIds()
            while True:
                if _0 is True:
                    _0 = False
                if not i.hasNext():
                    break
                self.getItem(i.next()).getItemProperty(propertyId).setValue(defaultValue)
            # store for next rows
            if self._defaultPropertyValues is None:
                self._defaultPropertyValues = dict()
            self._defaultPropertyValues.put(propertyId, defaultValue)
        # Sends a change event
        self.fireContainerPropertySetChange()
        return True

    def removeAllItems(self):
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container#addItem()

        origSize = len(self)
        self.internalRemoveAllItems()
        self._items.clear()
        # fire event only if the visible view changed, regardless of whether
        # filtered out items were removed or not
        if origSize != 0:
            # Sends a change event
            self.fireItemSetChange()
        return True

    def addItem(self, *args):
        # Creates a new id
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container#addItem(java.lang.Object)

        _0 = args
        _1 = len(args)
        if _1 == 0:
            id = self.generateId()
            # Adds the Item into container
            self.addItem(id)
            return id
        elif _1 == 1:
            itemId, = _0
            item = self.internalAddItemAtEnd(itemId, self.IndexedContainerItem(itemId), False)
            if not self.isFiltered():
                # always the last item
                self.fireItemAdded(len(self) - 1, itemId, item)
            elif self.passesFilters(itemId) and not self.containsId(itemId):
                self.getFilteredItemIds().add(itemId)
                # always the last item
                self.fireItemAdded(len(self) - 1, itemId, item)
            return item
        else:
            raise ARGERROR(0, 1)

    def addDefaultValues(self, t):
        """Helper method to add default values for items if available

        @param t
                   data table of added item
        """
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container#removeItem(java.lang.Object)

        if self._defaultPropertyValues is not None:
            for key in self._defaultPropertyValues.keys():
                t.put(key, self._defaultPropertyValues[key])

    def removeItem(self, itemId):
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container#removeContainerProperty(java.lang.Object )

        if (itemId is None) or (self._items.remove(itemId) is None):
            return False
        origSize = len(self)
        position = self.indexOfId(itemId)
        if self.internalRemoveItem(itemId):
            # fire event only if the visible view changed, regardless of
            # whether filtered out items were removed or not
            if len(self) != origSize:
                self.fireItemRemoved(position, itemId)
            return True
        else:
            return False

    def removeContainerProperty(self, propertyId):
        # Fails if the Property is not present
        # Container.Ordered methods
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container.Ordered#addItemAfter(java.lang.Object,
        # java.lang.Object)

        if not self._propertyIds.contains(propertyId):
            return False
        # Removes the Property to Property list and types
        self._propertyIds.remove(propertyId)
        self._types.remove(propertyId)
        if self._defaultPropertyValues is not None:
            self._defaultPropertyValues.remove(propertyId)
        # If remove the Property from all Items
        _0 = True
        i = self.getAllItemIds()
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            self._items[i.next()].remove(propertyId)
        # Sends a change event
        self.fireContainerPropertySetChange()
        return True

    def addItemAfter(self, *args):
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container.Ordered#addItemAfter(java.lang.Object)

        _0 = args
        _1 = len(args)
        if _1 == 1:
            previousItemId, = _0
            id = self.generateId()
            if self.addItemAfter(previousItemId, id) is not None:
                return id
            else:
                return None
        elif _1 == 2:
            previousItemId, newItemId = _0
            return self.internalAddItemAfter(previousItemId, newItemId, self.IndexedContainerItem(newItemId), True)
        else:
            raise ARGERROR(1, 2)

    # Creates a new id
    # (non-Javadoc)
    # 
    # @see com.vaadin.data.Container.Indexed#addItemAt(int, java.lang.Object)

    def addItemAt(self, *args):
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container.Indexed#addItemAt(int)

        _0 = args
        _1 = len(args)
        if _1 == 1:
            index, = _0
            id = self.generateId()
            # Adds the Item into container
            self.addItemAt(index, id)
            return id
        elif _1 == 2:
            index, newItemId = _0
            return self.internalAddItemAt(index, newItemId, self.IndexedContainerItem(newItemId), True)
        else:
            raise ARGERROR(1, 2)

    # Creates a new id

    def generateId(self):
        """Generates an unique identifier for use as an item id. Guarantees that the
        generated id is not currently used as an id.

        @return
        """
        while _0 or (id in self._items):
            _0 = False
            id = Integer.valueOf.valueOf(POSTINC(globals(), locals(), 'self._nextGeneratedItemId'))
        return id

    def registerNewItem(self, index, newItemId, item):
        # Event notifiers
        t = dict()
        self._items.put(newItemId, t)
        self.addDefaultValues(t)

    class ItemSetChangeEvent(BaseItemSetChangeEvent):
        """An <code>event</code> object specifying the list whose Item set has
        changed.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """
        _addedItemIndex = None

        def __init__(self, source, addedItemIndex):
            super(ItemSetChangeEvent, self)(source)
            self._addedItemIndex = addedItemIndex

        def getAddedItemIndex(self):
            """Iff one item is added, gives its index.

            @return -1 if either multiple items are changed or some other change
                    than add is done.
            """
            return self._addedItemIndex

    class PropertyValueChangeEvent(EventObject, Property, ValueChangeEvent, Serializable):
        """An <code>event</code> object specifying the Property in a list whose
        value has changed.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """

        def __init__(self, source):
            # (non-Javadoc)
            # 
            # @see com.vaadin.data.Property.ValueChangeEvent#getProperty()

            super(PropertyValueChangeEvent, self)(source)

        def getProperty(self):
            return self.getSource()

    def addListener(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Container.PropertySetChangeListener):
                listener, = _0
                super(IndexedContainer, self).addListener(listener)
            else:
                listener, = _0
                if self._propertyValueChangeListeners is None:
                    self._propertyValueChangeListeners = LinkedList()
                self._propertyValueChangeListeners.add(listener)
        else:
            raise ARGERROR(1, 1)

    def removeListener(self, *args):
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Property.ValueChangeNotifier#addListener(com.
        # vaadin.data.Property.ValueChangeListener)

        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Container.PropertySetChangeListener):
                listener, = _0
                super(IndexedContainer, self).removeListener(listener)
            else:
                listener, = _0
                if self._propertyValueChangeListeners is not None:
                    self._propertyValueChangeListeners.remove(listener)
        else:
            raise ARGERROR(1, 1)

    # (non-Javadoc)
    # 
    # @see com.vaadin.data.Property.ValueChangeNotifier#removeListener(com
    # .vaadin.data.Property.ValueChangeListener)

    def firePropertyValueChange(self, source):
        """Sends a Property value change event to all interested listeners.

        @param source
                   the IndexedContainerProperty object.
        """
        # Sends event to listeners listening all value changes
        if self._propertyValueChangeListeners is not None:
            l = list(self._propertyValueChangeListeners)
            event = IndexedContainer.PropertyValueChangeEvent(source)
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(l)):
                    break
                l[i].valueChange(event)
        # Sends event to single property value change listeners
        if self._singlePropertyValueChangeListeners is not None:
            propertySetToListenerListMap = self._singlePropertyValueChangeListeners[source.propertyId]
            if propertySetToListenerListMap is not None:
                listenerList = propertySetToListenerListMap[source.itemId]
                if listenerList is not None:
                    event = IndexedContainer.PropertyValueChangeEvent(source)
                    listeners = list(listenerList)
                    _1 = True
                    i = 0
                    while True:
                        if _1 is True:
                            _1 = False
                        else:
                            i += 1
                        if not (i < len(listeners)):
                            break
                        listeners[i].valueChange(event)

    def getListeners(self, eventType):
        if Property.ValueChangeEvent.isAssignableFrom(eventType):
            if self._propertyValueChangeListeners is None:
                return Collections.EMPTY_LIST
            else:
                return Collections.unmodifiableCollection(self._propertyValueChangeListeners)
        return super(IndexedContainer, self).getListeners(eventType)

    def fireItemAdded(self, position, itemId, item):
        if position >= 0:
            self.fireItemSetChange(IndexedContainer.ItemSetChangeEvent(self, position))

    def fireItemSetChange(self):
        self.fireItemSetChange(IndexedContainer.ItemSetChangeEvent(self, -1))

    def addSinglePropertyChangeListener(self, propertyId, itemId, listener):
        """Adds new single Property change listener.

        @param propertyId
                   the ID of the Property to add.
        @param itemId
                   the ID of the Item .
        @param listener
                   the listener to be added.
        """
        if listener is not None:
            if self._singlePropertyValueChangeListeners is None:
                self._singlePropertyValueChangeListeners = dict()
            propertySetToListenerListMap = self._singlePropertyValueChangeListeners[propertyId]
            if propertySetToListenerListMap is None:
                propertySetToListenerListMap = dict()
                self._singlePropertyValueChangeListeners.put(propertyId, propertySetToListenerListMap)
            listenerList = propertySetToListenerListMap[itemId]
            if listenerList is None:
                listenerList = LinkedList()
                propertySetToListenerListMap.put(itemId, listenerList)
            listenerList.add(listener)

    def removeSinglePropertyChangeListener(self, propertyId, itemId, listener):
        """Removes a previously registered single Property change listener.

        @param propertyId
                   the ID of the Property to remove.
        @param itemId
                   the ID of the Item.
        @param listener
                   the listener to be removed.
        """
        # Internal Item and Property implementations
        # A class implementing the com.vaadin.data.Item interface to be contained
        # in the list.
        # 
        # @author IT Mill Ltd.
        # 
        # @version @VERSION@
        # 
        # @since 3.0

        if (
            listener is not None and self._singlePropertyValueChangeListeners is not None
        ):
            propertySetToListenerListMap = self._singlePropertyValueChangeListeners[propertyId]
            if propertySetToListenerListMap is not None:
                listenerList = propertySetToListenerListMap[itemId]
                if listenerList is not None:
                    listenerList.remove(listener)
                    if listenerList.isEmpty():
                        propertySetToListenerListMap.remove(itemId)
                if propertySetToListenerListMap.isEmpty():
                    self._singlePropertyValueChangeListeners.remove(propertyId)
            if self._singlePropertyValueChangeListeners.isEmpty():
                self._singlePropertyValueChangeListeners = None

    class IndexedContainerItem(Item):
        # Item ID in the host container for this Item.
        _itemId = None

        def __init__(self, itemId):
            """Constructs a new ListItem instance and connects it to a host
            container.

            @param itemId
                       the Item ID of the new Item.
            """
            # Gets the item contents from the host
            # (non-Javadoc)
            # 
            # @see com.vaadin.data.Item#getItemProperty(java.lang.Object)

            if itemId is None:
                raise self.NullPointerException()
            self._itemId = itemId

        def getItemProperty(self, id):
            return self.IndexedContainerProperty(self._itemId, id)

        def getItemPropertyIds(self):
            return Collections.unmodifiableCollection(self.propertyIds)

        def toString(self):
            """Gets the <code>String</code> representation of the contents of the
            Item. The format of the string is a space separated catenation of the
            <code>String</code> representations of the Properties contained by
            the Item.

            @return <code>String</code> representation of the Item contents
            """
            retValue = ''
            _0 = True
            i = self.propertyIds
            while True:
                if _0 is True:
                    _0 = False
                if not i.hasNext():
                    break
                propertyId = i.next()
                retValue += str(self.getItemProperty(propertyId))
                if i.hasNext():
                    retValue += ' '
            return retValue

        def hashCode(self):
            """Calculates a integer hash-code for the Item that's unique inside the
            list. Two Items inside the same list have always different
            hash-codes, though Items in different lists may have identical
            hash-codes.

            @return A locally unique hash-code as integer
            """
            return self._itemId.hashCode()

        def equals(self, obj):
            """Tests if the given object is the same as the this object. Two Items
            got from a list container with the same ID are equal.

            @param obj
                       an object to compare with this object
            @return <code>true</code> if the given object is the same as this
                    object, <code>false</code> if not
            """
            if (obj is None) or (not (obj.getClass() == self.IndexedContainerItem)):
                return False
            li = obj
            return self.getHost() == li.getHost() and self._itemId == li.itemId

        def getHost(self):
            return _IndexedContainer_this

        def addItemProperty(self, id, property):
            """IndexedContainerItem does not support adding new properties. Add
            properties at container level. See
            {@link IndexedContainer#addContainerProperty(Object, Class, Object)}

            @see com.vaadin.data.Item#addProperty(Object, Property)
            """
            raise self.UnsupportedOperationException('Indexed container item ' + 'does not support adding new properties')

        def removeItemProperty(self, id):
            """Indexed container does not support removing properties. Remove
            properties at container level. See
            {@link IndexedContainer#removeContainerProperty(Object)}

            @see com.vaadin.data.Item#removeProperty(Object)
            """
            raise self.UnsupportedOperationException('Indexed container item does not support property removal')

    class IndexedContainerProperty(Property, Property, ValueChangeNotifier):
        """A class implementing the {@link Property} interface to be contained in
        the {@link IndexedContainerItem} contained in the
        {@link IndexedContainer}.

        @author IT Mill Ltd.

        @version
        @VERSION@
        @since 3.0
        """
        # ID of the Item, where this property resides.
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container.Sortable#sort(java.lang.Object[],
        # boolean[])

        _itemId = None
        # Id of the Property.
        _propertyId = None

        def __init__(self, itemId, propertyId):
            """Constructs a new {@link IndexedContainerProperty} object.

            @param itemId
                       the ID of the Item to connect the new Property to.
            @param propertyId
                       the Property ID of the new Property.
            @param host
                       the list that contains the Item to contain the new
                       Property.
            """
            # (non-Javadoc)
            # 
            # @see com.vaadin.data.Property#getType()

            if (itemId is None) or (propertyId is None):
                # Null ids are not accepted
                raise self.NullPointerException('Container item or property ids can not be null')
            self._propertyId = propertyId
            self._itemId = itemId

        def getType(self):
            # (non-Javadoc)
            # 
            # @see com.vaadin.data.Property#getValue()

            return self.types[self._propertyId]

        def getValue(self):
            # (non-Javadoc)
            # 
            # @see com.vaadin.data.Property#isReadOnly()

            return self.items[self._itemId].get(self._propertyId)

        def isReadOnly(self):
            # (non-Javadoc)
            # 
            # @see com.vaadin.data.Property#setReadOnly(boolean)

            return self in self.readOnlyProperties

        def setReadOnly(self, newStatus):
            # (non-Javadoc)
            # 
            # @see com.vaadin.data.Property#setValue(java.lang.Object)

            if newStatus:
                self.readOnlyProperties.add(self)
            else:
                self.readOnlyProperties.remove(self)

        def setValue(self, newValue):
            # Gets the Property set
            propertySet = self.items[self._itemId]
            # Support null values on all types
            if newValue is None:
                propertySet.remove(self._propertyId)
            elif self.getType().isAssignableFrom(newValue.getClass()):
                propertySet.put(self._propertyId, newValue)
            else:
                # Gets the string constructor
                try:
                    constr = self.getType().getConstructor([str])
                    # Creates new object from the string
                    propertySet.put(self._propertyId, constr([str(newValue)]))
                except java.lang.Exception, e:
                    raise Property.ConversionException('Conversion for value \'' + newValue + '\' of class ' + newValue.getClass().getName() + ' to ' + self.getType().getName() + ' failed', e)
            # update the container filtering if this property is being filtered
            if self.isPropertyFiltered(self._propertyId):
                self.filterAll()
            self.firePropertyValueChange(self)

        def toString(self):
            """Returns the value of the Property in human readable textual format.
            The return value should be assignable to the <code>setValue</code>
            method if the Property is not in read-only mode.

            @return <code>String</code> representation of the value stored in the
                    Property
            """
            value = self.getValue()
            if value is None:
                return None
            return str(value)

        def hashCode(self):
            """Calculates a integer hash-code for the Property that's unique inside
            the Item containing the Property. Two different Properties inside the
            same Item contained in the same list always have different
            hash-codes, though Properties in different Items may have identical
            hash-codes.

            @return A locally unique hash-code as integer
            """
            return self._itemId.hashCode() ^ self._propertyId.hashCode()

        def equals(self, obj):
            """Tests if the given object is the same as the this object. Two
            Properties got from an Item with the same ID are equal.

            @param obj
                       an object to compare with this object
            @return <code>true</code> if the given object is the same as this
                    object, <code>false</code> if not
            """
            # (non-Javadoc)
            # 
            # @see com.vaadin.data.Property.ValueChangeNotifier#addListener(
            # com.vaadin.data.Property.ValueChangeListener)

            if (obj is None) or (not (obj.getClass() == self.IndexedContainerProperty)):
                return False
            lp = obj
            return lp.getHost() == self.getHost() and lp.propertyId == self._propertyId and lp.itemId == self._itemId

        def addListener(self, listener):
            # (non-Javadoc)
            # 
            # @see com.vaadin.data.Property.ValueChangeNotifier#removeListener
            # (com.vaadin.data.Property.ValueChangeListener)

            self.addSinglePropertyChangeListener(self._propertyId, self._itemId, listener)

        def removeListener(self, listener):
            self.removeSinglePropertyChangeListener(self._propertyId, self._itemId, listener)

        def getHost(self):
            return _IndexedContainer_this

    def sort(self, propertyId, ascending):
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container.Sortable#getSortableContainerPropertyIds
        # ()

        self.sortContainer(propertyId, ascending)

    def getSortableContainerPropertyIds(self):
        return self.getSortablePropertyIds()

    def getItemSorter(self):
        return super(IndexedContainer, self).getItemSorter()

    def setItemSorter(self, itemSorter):
        super(IndexedContainer, self).setItemSorter(itemSorter)

    def clone(self):
        """Supports cloning of the IndexedContainer cleanly.

        @throws CloneNotSupportedException
                    if an object cannot be cloned. .

        @deprecated cloning support might be removed from IndexedContainer in the
                    future
        """
        # Creates the clone
        nc = IndexedContainer()
        # Clone the shallow properties
        nc.setAllItemIds(self.getAllItemIds().clone() if self.getAllItemIds() is not None else None)
        nc.setItemSetChangeListeners(LinkedList(self.getItemSetChangeListeners()) if self.getItemSetChangeListeners() is not None else None)
        nc.propertyIds = self._propertyIds.clone() if self._propertyIds is not None else None
        nc.setPropertySetChangeListeners(LinkedList(self.getPropertySetChangeListeners()) if self.getPropertySetChangeListeners() is not None else None)
        nc.propertyValueChangeListeners = self._propertyValueChangeListeners.clone() if self._propertyValueChangeListeners is not None else None
        nc.readOnlyProperties = self._readOnlyProperties.clone() if self._readOnlyProperties is not None else None
        nc.singlePropertyValueChangeListeners = self._singlePropertyValueChangeListeners.clone() if self._singlePropertyValueChangeListeners is not None else None
        nc.types = self._types.clone() if self._types is not None else None
        nc.setFilters(self.getFilters().clone())
        nc.setFilteredItemIds(None if self.getFilteredItemIds() is None else self.getFilteredItemIds().clone())
        # Clone property-values
        if self._items is None:
            nc.items = None
        else:
            nc.items = dict()
            _0 = True
            i = self._items.keys()
            while True:
                if _0 is True:
                    _0 = False
                if not i.hasNext():
                    break
                id = i.next()
                it = self._items[id]
                nc.items.put(id, it.clone())
        return nc

    def addContainerFilter(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            filter, = _0
            self.addFilter(filter)
        elif _1 == 4:
            propertyId, filterString, ignoreCase, onlyMatchPrefix = _0
            # the filter instance created here is always valid for in-memory
            # containers
            try:
                self.addFilter(SimpleStringFilter(propertyId, filterString, ignoreCase, onlyMatchPrefix))
            except UnsupportedFilterException, e:
                pass # astStmt: [Stmt([]), None]
        else:
            raise ARGERROR(1, 4)

    def removeAllContainerFilters(self):
        self.removeAllFilters()

    def removeContainerFilters(self, propertyId):
        self.removeFilters(propertyId)

    def removeContainerFilter(self, filter):
        self.removeFilter(filter)
