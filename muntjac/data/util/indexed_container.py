# Copyright (C) 2010 IT Mill Ltd.
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

from muntjac.data import property as prop

from muntjac.data.item import IItem

from muntjac.data.util.abstract_in_memory_container import \
    AbstractInMemoryContainer

from muntjac.data.util.filter.simple_string_filter import \
    SimpleStringFilter

from muntjac.data.util.filter.unsupported_filter_exception import \
    UnsupportedFilterException

from muntjac.data.util.abstract_container import BaseItemSetChangeEvent,\
    AbstractContainer

from muntjac.data import container
from muntjac.util import EventObject
from muntjac.util import fullname

# item type is really IndexedContainerItem, but using IItem
# not to show it in public API
class IndexedContainer(AbstractInMemoryContainer,
            container.IPropertySetChangeNotifier,
            prop.IValueChangeNotifier, container.ISortable,
            container.IFilterable, container.ISimpleFilterable):
    """An implementation of the <code>{@link IContainer.Indexed}</code> interface
    with all important features.

    Features:
    <ul>
    <li> {@link IContainer.Indexed}
    <li> {@link IContainer.Ordered}
    <li> {@link IContainer.ISortable}
    <li> {@link IContainer.IFilterable}
    <li> {@link Cloneable} (deprecated, might be removed in the future)
    <li>Sends all needed events on content changes.
    </ul>

    @see com.vaadin.data.IContainer

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, itemIds=None):

        # Internal structure
        # Linked list of ordered IProperty IDs.
        self._propertyIds = list()

        # IProperty ID to type mapping.
        self._types = dict()

        # Hash of Items, where each IItem is implemented as a mapping from
        # IProperty ID to IProperty value.
        self._items = dict()

        # Set of properties that are read-only.
        self._readOnlyProperties = set()

        # List of all IProperty value change event listeners listening all
        # the properties.
        self._propertyValueChangeListeners = None

        # Data structure containing all listeners interested in changes to single
        # Properties. The data structure is a hashtable mapping IProperty IDs to a
        # hashtable that maps IItem IDs to a linked list of listeners listening
        # IProperty identified by given IProperty ID and IItem ID.
        self._singlePropertyValueChangeListeners = None

        self._defaultPropertyValues = None

        self._nextGeneratedItemId = 1

        super(IndexedContainer, self).__init__()

        if itemIds is not None:
            for itemId in itemIds:
                self.internalAddItemAtEnd(itemId,
                        IndexedContainerItem(itemId, self), False)

            self.filterAll()

    # IContainer methods

    def getUnfilteredItem(self, itemId):
        if itemId is not None and itemId in self._items:
            return IndexedContainerItem(itemId, self)

        return None


    def getContainerPropertyIds(self):
        return list(self._propertyIds)


    def getType(self, propertyId):
        """Gets the type of a IProperty stored in the list.

        @param id
                   the ID of the IProperty.
        @return Type of the requested IProperty
        """
        return self._types.get(propertyId)


    def getContainerProperty(self, itemId, propertyId):
        if not self.containsId(itemId):
            return None

        return IndexedContainerProperty(itemId, propertyId, self)


    def addContainerProperty(self, propertyId, typ, defaultValue):
        # Fails, if nulls are given
        if propertyId is None or typ is None:
            return False

        # Fails if the IProperty is already present
        if propertyId in self._propertyIds:
            return False

        # Adds the IProperty to IProperty list and types
        self._propertyIds.append(propertyId)
        self._types[propertyId] = typ

        # If default value is given, set it
        if defaultValue is not None:
            # for existing rows
            for item in self.getAllItemIds():
                prop = self.getItem(item).getItemProperty(propertyId)
                prop.setValue(defaultValue)

            # store for next rows
            if self._defaultPropertyValues is None:
                self._defaultPropertyValues = dict()

            self._defaultPropertyValues[propertyId] = defaultValue

        # Sends a change event
        self.fireContainerPropertySetChange()

        return True


    def removeAllItems(self):
        origSize = len(self)

        self.internalRemoveAllItems()

        self._items.clear()

        # fire event only if the visible view changed, regardless of whether
        # filtered out items were removed or not
        if origSize != 0:
            # Sends a change event
            self.fireItemSetChange()

        return True


    def addItem(self, itemId=None):
        if itemId is None:
            idd = self.generateId()
            # Adds the IItem into container
            self.addItem(idd)
            return idd
        else:
            item = self.internalAddItemAtEnd(itemId,
                    IndexedContainerItem(itemId, self), False)
            if not self.isFiltered():
                # always the last item
                self.fireItemAdded(self.size() - 1, itemId, item)
            elif self.passesFilters(itemId) and not self.containsId(itemId):
                self.getFilteredItemIds().append(itemId)
                # always the last item
                self.fireItemAdded(self.size() - 1, itemId, item)

            return item


    def addDefaultValues(self, t):
        """Helper method to add default values for items if available

        @param t: data table of added item
        """
        if self._defaultPropertyValues is not None:
            for key in self._defaultPropertyValues.keys():
                t[key] = self._defaultPropertyValues.get(key)


    def removeItem(self, itemId):
        if itemId is None or itemId not in self._items:
            return False
        else:
            del self._items[itemId]

        origSize = self.size()
        position = self.indexOfId(itemId)
        if self.internalRemoveItem(itemId):
            # fire event only if the visible view changed, regardless of
            # whether filtered out items were removed or not
            if self.size() != origSize:
                self.fireItemRemoved(position, itemId)

            return True
        else:
            return False


    def removeContainerProperty(self, propertyId):

        # Fails if the IProperty is not present
        if propertyId not in self._propertyIds:
            return False

        # Removes the IProperty to IProperty list and types
        self._propertyIds.remove(propertyId)
        if propertyId in self._types:
            del self._types[propertyId]
        if self._defaultPropertyValues is not None:
            if propertyId in self._defaultPropertyValues:
                del self._defaultPropertyValues[propertyId]

        # If remove the IProperty from all Items
        for item in self.getAllItemIds():
            self._items.get(item).remove(propertyId)

        # Sends a change event
        self.fireContainerPropertySetChange()

        return True


    def addItemAfter(self, previousItemId, newItemId=None):
        if newItemId is None:
            idd = self.generateId()
            if self.addItemAfter(previousItemId, idd) is not None:
                return idd
            else:
                return None
        else:

            return self.internalAddItemAfter(previousItemId, newItemId,
                    IndexedContainerItem(newItemId, self), True)


    def addItemAt(self, index, newItemId=None):
        if newItemId is None:
            idd = self.generateId()
            # Adds the IItem into container
            self.addItemAt(index, idd)
            return idd
        else:
            return self.internalAddItemAt(index, newItemId,
                    IndexedContainerItem(newItemId, self), True)


    def generateId(self):
        """Generates an unique identifier for use as an item id. Guarantees
        that the generated id is not currently used as an id.

        @return
        """
        while True:  # FIXME: do statement
            idd = int(self._nextGeneratedItemId)
            self._nextGeneratedItemId += 1
            if idd not in self._items:
                break
        return idd


    def registerNewItem(self, index, newItemId, item):
        t = dict()
        self._items[newItemId] = t
        self.addDefaultValues(t)


    def addListener(self, listener, iface):
        if iface == container.IPropertySetChangeListener:
            super(IndexedContainer, self).addListener(listener, iface)
        elif iface == prop.IValueChangeListener:
            if self._propertyValueChangeListeners is None:
                self._propertyValueChangeListeners = list()

            self._propertyValueChangeListeners.append(listener)
        else:
            super(IndexedContainer, self).addListener(listener, iface)


    def addPropertySetChangeListener(self, listener):
        self.addListener(listener, container.IPropertySetChangeListener)


    def addValueChangeListener(self, listener):
        self.addListener(listener, prop.IValueChangeListener)


    def removeListener(self, listener, iface):
        if iface == container.IPropertySetChangeListener:
            super(IndexedContainer, self).removeListener(listener, iface)
        elif iface == prop.IValueChangeListener:
            if self._propertyValueChangeListeners is not None:
                self._propertyValueChangeListeners.remove(listener)
        else:
            super(IndexedContainer, self).removeListener(listener, iface)


    def removePropertySetChangeListener(self, listener):
        self.removeListener(listener, container.IPropertySetChangeListener)


    def removeValueChangeListener(self, listener):
        self.removeListener(listener, prop.IValueChangeListener)


    def firePropertyValueChange(self, source):
        """Sends a IProperty value change event to all interested listeners.

        @param source
                   the IndexedContainerProperty object.
        """
        # Sends event to listeners listening all value changes
        if self._propertyValueChangeListeners is not None:
            l = list(self._propertyValueChangeListeners)
            event = PropertyValueChangeEvent(source)
            for listener in l:
                listener.valueChange(event)

        # Sends event to single property value change listeners
        if self._singlePropertyValueChangeListeners is not None:

            propertySetToListenerListMap = \
                self._singlePropertyValueChangeListeners.get(source.propertyId)

            if propertySetToListenerListMap is not None:
                listenerList = propertySetToListenerListMap.get(source.itemId)
                if listenerList is not None:
                    event = PropertyValueChangeEvent(source)
                    listeners = list(listenerList)
                    for l in listeners:
                        l.valueChange(event)


    def getListeners(self, eventType):
        if issubclass(eventType, prop.ValueChangeEvent):
            if self._propertyValueChangeListeners is None:
                return list()
            else:
                return list(self._propertyValueChangeListeners)
        return super(IndexedContainer, self).getListeners(eventType)


    def fireItemAdded(self, position, itemId, item):
        if position >= 0:
            AbstractContainer.fireItemSetChange(self,
                    ItemSetChangeEvent(self, position))


    def fireItemSetChange(self):
        AbstractContainer.fireItemSetChange(self, ItemSetChangeEvent(self, -1))


    def addSinglePropertyChangeListener(self, propertyId, itemId, listener):
        """Adds new single IProperty change listener.

        @param propertyId
                   the ID of the IProperty to add.
        @param itemId
                   the ID of the IItem .
        @param listener
                   the listener to be added.
        """
        if listener is not None:
            if self._singlePropertyValueChangeListeners is None:
                self._singlePropertyValueChangeListeners = dict()

            propertySetToListenerListMap = \
                    self._singlePropertyValueChangeListeners.get(propertyId)

            if propertySetToListenerListMap is None:
                propertySetToListenerListMap = dict()
                self._singlePropertyValueChangeListeners[propertyId] = \
                        propertySetToListenerListMap

            listenerList = propertySetToListenerListMap.get(itemId)

            if listenerList is None:
                listenerList = list()
                propertySetToListenerListMap[itemId] = listenerList

            listenerList.append(listener)


    def removeSinglePropertyChangeListener(self, propertyId, itemId, listener):
        """Removes a previously registered single IProperty change listener.

        @param propertyId
                   the ID of the IProperty to remove.
        @param itemId
                   the ID of the IItem.
        @param listener
                   the listener to be removed.
        """
        if (listener is not None
                and self._singlePropertyValueChangeListeners is not None):

            propertySetToListenerListMap = \
                    self._singlePropertyValueChangeListeners.get(propertyId)

            if propertySetToListenerListMap is not None:
                listenerList = propertySetToListenerListMap.get(itemId)

                if listenerList is not None:
                    listenerList.remove(listener)
                    if len(listenerList) == 0:
                        if itemId in propertySetToListenerListMap:
                            del propertySetToListenerListMap[itemId]

                if len(propertySetToListenerListMap) == 0:
                    if propertyId in self._singlePropertyValueChangeListeners:
                        del self._singlePropertyValueChangeListeners[propertyId]

            if len(self._singlePropertyValueChangeListeners) == 0:
                self._singlePropertyValueChangeListeners = None


    def sort(self, propertyId, ascending):
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
        if self.getAllItemIds() is not None:
            nc.setAllItemIds(self.getAllItemIds().clone())  # FIXME: clone
        else:
            nc.setAllItemIds(None)

        if self.getItemSetChangeListeners() is not None:
            nc.setItemSetChangeListeners(list(self.getItemSetChangeListeners()))
        else:
            nc.setItemSetChangeListeners(None)

        if self._propertyIds is not None:
            nc._propertyIds = self._propertyIds.clone()
        else:
            nc._propertyIds = None

        if self.getPropertySetChangeListeners() is not None:
            nc.setPropertySetChangeListeners(
                    list(self.getPropertySetChangeListeners()))
        else:
            nc.setPropertySetChangeListeners(None)

        if self._propertyValueChangeListeners is not None:
            nc.propertyValueChangeListeners = self._propertyValueChangeListeners.clone()
        else:
            nc.propertyValueChangeListeners = None

        if self._readOnlyProperties is not None:
            nc.readOnlyProperties = self._readOnlyProperties.clone()
        else:
            nc.readOnlyProperties = None

        if self._singlePropertyValueChangeListeners is not None:
            nc.singlePropertyValueChangeListeners = self._singlePropertyValueChangeListeners.clone()
        else:
            nc.singlePropertyValueChangeListeners = None

        if self._types is not None:
            nc.types = self._types.clone()
        else:
            nc.types = None

        nc.setFilters(self.getFilters().clone())

        if self.getFilteredItemIds() is None:
            nc.setFilteredItemIds(None)
        else:
            nc.setFilteredItemIds( self.getFilteredItemIds().clone() )

        # Clone property-values
        if self._items is None:
            nc.items = None
        else:
            nc.items = dict()
            for idd in self._items.keys():
                it = self._items.get(idd)
                nc.items[id] = it.clone()
        return nc


    def addContainerFilter(self, *args):
        nargs = len(args)
        if nargs == 1:
            fltr, = args
            self.addFilter(fltr)
        elif nargs == 4:
            propertyId, filterString, ignoreCase, onlyMatchPrefix = args
            # the filter instance created here is always valid for
            # in-memory containers
            try:
                self.addFilter(SimpleStringFilter(propertyId, filterString,
                        ignoreCase, onlyMatchPrefix))
            except UnsupportedFilterException:
                pass
        else:
            raise ValueError, 'invalid number of elements'


    def removeAllContainerFilters(self):
        self.removeAllFilters()


    def removeContainerFilters(self, propertyId):
        self.removeFilters(propertyId)


    def removeContainerFilter(self, fltr):
        self.removeFilter(fltr)


class IndexedContainerItem(IItem):

    def __init__(self, itemId, container):  # FIXME: inner class
        """Constructs a new ListItem instance and connects it to a host
        container.

        @param itemId: the IItem ID of the new IItem.
        """
        if itemId is None:
            raise ValueError

        # IItem ID in the host container for this IItem.
        self._itemId = itemId

        self._container = container


    def getItemProperty(self, idd):
        return IndexedContainerProperty(self._itemId, idd, self._container)


    def getItemPropertyIds(self):
        return list(self._container._propertyIds)


    def __str__(self):
        """Gets the <code>String</code> representation of the contents of the
        IItem. The format of the string is a space separated catenation of the
        <code>String</code> representations of the Properties contained by
        the IItem.

        @return <code>String</code> representation of the IItem contents
        """
        retValue = ''

        for i, propertyId in enumerate(self._container._propertyIds):
            retValue += str(self.getItemProperty(propertyId))
            if i < len(self._container._propertyIds) - 1:
                retValue += ' '

        return retValue


    def __hash__(self):
        """Calculates a integer hash-code for the IItem that's unique inside the
        list. Two Items inside the same list have always different
        hash-codes, though Items in different lists may have identical
        hash-codes.

        @return A locally unique hash-code as integer
        """
        return hash(self._itemId)


    def __eq__(self, obj):
        """Tests if the given object is the same as the this object. Two Items
        got from a list container with the same ID are equal.

        @param obj
                   an object to compare with this object
        @return <code>true</code> if the given object is the same as this
                object, <code>false</code> if not
        """
        if obj is None or obj.__class__ != IndexedContainerItem:
            return False

        li = obj

        return self.getHost() == li.getHost() and self._itemId == li.itemId


    def getHost(self):
        return self._container


    def addItemProperty(self, idd, prop):
        """IndexedContainerItem does not support adding new properties. Add
        properties at container level. See
        {@link IndexedContainer#addContainerProperty(Object, Class, Object)}

        @see com.vaadin.data.IItem#addProperty(Object, IProperty)
        """
        raise NotImplementedError, ('Indexed container item '
                + 'does not support adding new properties')


    def removeItemProperty(self, idd):
        """Indexed container does not support removing properties. Remove
        properties at container level. See
        {@link IndexedContainer#removeContainerProperty(Object)}

        @see com.vaadin.data.IItem#removeProperty(Object)
        """
        raise NotImplementedError, \
                'Indexed container item does not support property removal'


class IndexedContainerProperty(prop.IProperty, prop.IValueChangeNotifier):
    """A class implementing the {@link IProperty} interface to be contained in
    the {@link IndexedContainerItem} contained in the
    {@link IndexedContainer}.

    @author IT Mill Ltd.
    @author Richard Lincoln

    @version @VERSION@
    @since 3.0
    """

    def __init__(self, itemId, propertyId, container):  # FIXME: inner class
        """Constructs a new {@link IndexedContainerProperty} object.

        @param itemId
                   the ID of the IItem to connect the new IProperty to.
        @param propertyId
                   the IProperty ID of the new IProperty.
        @param host
                   the list that contains the IItem to contain the new
                   IProperty.
        """
        if (itemId is None) or (propertyId is None):
            # Null ids are not accepted
            raise ValueError, 'IContainer item or property ids can not be null'

        # ID of the IItem, where this property resides.
        self._propertyId = propertyId

        # Id of the IProperty.
        self._itemId = itemId

        self._container = container


    def getType(self):
        return self._container._types.get(self._propertyId)


    def getValue(self):
        return self._container._items.get(self._itemId).get(self._propertyId)


    def isReadOnly(self):
        return self in self._container._readOnlyProperties


    def setReadOnly(self, newStatus):
        if newStatus:
            self._container._readOnlyProperties.add(self)
        else:
            self._container._readOnlyProperties.remove(self)


    def setValue(self, newValue):
        # Gets the IProperty set
        propertySet = self._container._items.get(self._itemId)

        # Support null values on all types
        if newValue is None:
            propertySet.remove(self._propertyId)
        elif issubclass(newValue.__class__, self.getType()):
            propertySet[self._propertyId] = newValue
        else:
            try:
                # Gets the string constructor
                #constr = self.getType().getConstructor([str])
                constr = self.getType().__init__  # FIXME: getConstructor
                # Creates new object from the string
                propertySet[self._propertyId] = constr(*[str(newValue)])
            except Exception:
                raise prop.ConversionException, ('Conversion for value \''
                        + newValue + '\' of class ' + fullname(newValue)
                        + ' to ' + self.getType().__name__ + ' failed')

        # update the container filtering if this property is being filtered
        if self._container.isPropertyFiltered(self._propertyId):
            self.filterAll()

        self._container.firePropertyValueChange(self)


    def __str__(self):
        """Returns the value of the IProperty in human readable textual format.
        The return value should be assignable to the <code>setValue</code>
        method if the IProperty is not in read-only mode.

        @return <code>String</code> representation of the value stored in the
                IProperty
        """
        value = self.getValue()

        if value is None:
            return None

        return str(value)


    def __hash__(self):
        """Calculates a integer hash-code for the IProperty that's unique inside
        the IItem containing the IProperty. Two different Properties inside the
        same IItem contained in the same list always have different
        hash-codes, though Properties in different Items may have identical
        hash-codes.

        @return A locally unique hash-code as integer
        """
        return hash(self._itemId) ^ hash(self._propertyId)


    def __eq__(self, obj):
        """Tests if the given object is the same as the this object. Two
        Properties got from an IItem with the same ID are equal.

        @param obj
                   an object to compare with this object
        @return <code>true</code> if the given object is the same as this
                object, <code>false</code> if not
        """
        if obj is None or obj.__class__ != IndexedContainerProperty:
            return False

        lp = obj

        return (lp.getHost() == self.getHost()
                and lp._propertyId == self._propertyId
                and lp._itemId == self._itemId)


    def addListener(self, listener, iface):
        if iface == prop.IValueChangeListener:
            self._container.addSinglePropertyChangeListener(self._propertyId,
                    self._itemId, listener)
        else:
            super(IndexedContainerProperty, self).addListener(listener, iface)


    def addValueChangeListener(self, listener):
        self.addListener(listener, prop.IValueChangeListener)


    def removeListener(self, listener, iface):
        if iface == prop.IValueChangeListener:
            self._container.removeSinglePropertyChangeListener(self._propertyId,
                    self._itemId, listener)
        else:
            super(IndexedContainerProperty, self).addListener(listener, iface)


    def removeValueChangeListener(self, listener):
        self.removeListener(listener, prop.IValueChangeListener)


    def getHost(self):
        return self._container


class ItemSetChangeEvent(BaseItemSetChangeEvent):
    """An <code>event</code> object specifying the list whose IItem set has
    changed.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, source, addedItemIndex):
        super(ItemSetChangeEvent, self).__init__(source)
        self._addedItemIndex = addedItemIndex


    def getAddedItemIndex(self):
        """Iff one item is added, gives its index.

        @return -1 if either multiple items are changed or some other change
                than add is done.
        """
        return self._addedItemIndex


class PropertyValueChangeEvent(EventObject, prop.ValueChangeEvent):
    """An <code>event</code> object specifying the IProperty in a list whose
    value has changed.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, source):
        super(PropertyValueChangeEvent, self).__init__(source)


    def getProperty(self):
        return self.getSource()
