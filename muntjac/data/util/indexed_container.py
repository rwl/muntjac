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

"""An implementation of the IIndexed interface with all important features."""

from muntjac.data import property as prop

from muntjac.data.item import IItem

from muntjac.data.util.abstract_in_memory_container import \
    AbstractInMemoryContainer

from muntjac.data.util.filter.simple_string_filter import \
    SimpleStringFilter

from muntjac.data.util.filter.unsupported_filter_exception import \
    UnsupportedFilterException

from muntjac.data.util.abstract_container import \
    BaseItemSetChangeEvent, AbstractContainer

from muntjac.data import container
from muntjac.util import EventObject
from muntjac.util import fullname

# item type is really IndexedContainerItem, but using IItem
# not to show it in public API
class IndexedContainer(AbstractInMemoryContainer,
            container.IPropertySetChangeNotifier,
            prop.IValueChangeNotifier, container.ISortable,
            container.IFilterable, container.ISimpleFilterable):
    """An implementation of the L{IContainer.Indexed} interface with all
    important features.

    Features:
      - L{IIndexed}
      - L{IOrdered}
      - L{ISortable}
      - L{IFilterable}
      - L{ICloneable} (deprecated, might be removed in the future)
      - Sends all needed events on content changes.

    @see: L{IContainer}
    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, itemIds=None):

        #: Linked list of ordered IProperty IDs.
        self._propertyIds = list()

        #: IProperty ID to type mapping.
        self._types = dict()

        #: Hash of Items, where each IItem is implemented as a mapping from
        #  IProperty ID to IProperty value.
        self._items = dict()

        #: Set of properties that are read-only.
        self._readOnlyProperties = set()

        #: List of all IProperty value change event listeners listening all
        #  the properties.
        self._propertyValueChangeListeners = list()

        self._propertyValueChangeCallbacks = dict()

        #: Data structure containing all listeners interested in changes to
        #  single Properties. The data structure is a hashtable mapping
        #  IProperty IDs to a hashtable that maps IItem IDs to a linked list
        #  of listeners listening IProperty identified by given IProperty ID
        #  and IItem ID.
        self._singlePropertyValueChangeListeners = dict()

        self._defaultPropertyValues = dict()

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

        @param propertyId:
                   the ID of the IProperty.
        @return: Type of the requested IProperty
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


    def addListener(self, listener, iface=None):
        if (isinstance(listener, container.IPropertySetChangeListener) and
                (iface is None or
                    issubclass(iface, container.IPropertySetChangeListener))):
            #super(IndexedContainer, self).addListener(listener, iface)
            pass

        if (isinstance(listener, prop.IValueChangeListener) and
                (iface is None or
                        issubclass(iface, prop.IValueChangeListener))):

            self._propertyValueChangeListeners.append(listener)

        super(IndexedContainer, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, container.IPropertySetChangeEvent):
            super(IndexedContainer, self).addCallback(callback,
                    eventType, *args)

        elif issubclass(eventType, prop.ValueChangeEvent):
            self._propertyValueChangeCallbacks[callback] = args

        else:
            super(IndexedContainer, self).addCallback(callback,
                    eventType, *args)


    def removeListener(self, listener, iface=None):
        if (isinstance(listener, container.IPropertySetChangeListener) and
                (iface is None or
                    issubclass(iface, container.IPropertySetChangeListener))):
            #super(IndexedContainer, self).removeListener(listener, iface)
            pass

        if (isinstance(listener, prop.IValueChangeListener) and
                (iface is None or
                        issubclass(iface, prop.IValueChangeListener))):
            if listener in self._propertyValueChangeListeners:
                self._propertyValueChangeListeners.remove(listener)

        super(IndexedContainer, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, container.IPropertySetChangeEvent):
            super(IndexedContainer, self).removecallback(callback, eventType)

        elif issubclass(eventType, prop.ValueChangeEvent):
            if callback in self._propertyValueChangeCallbacks:
                del self._propertyValueChangeCallbacks[callback]

        else:
            super(IndexedContainer, self).removeCallback(callback, eventType)


    def firePropertyValueChange(self, source):
        """Sends a IProperty value change event to all interested listeners.

        @param source:
                   the IndexedContainerProperty object.
        """
        # Sends event to listeners listening all value changes
        event = PropertyValueChangeEvent(source)
        for listener in self._propertyValueChangeListeners:
            listener.valueChange(event)

        for callback, args in self._propertyValueChangeCallbacks.iteritems():
            callback(event, *args)

        # Sends event to single property value change listeners
        propertySetToListenerListMap = \
            self._singlePropertyValueChangeListeners.get(source._propertyId)

        if propertySetToListenerListMap is not None:
            listenerList = propertySetToListenerListMap.get(source._itemId)
            if listenerList is not None:
                event = PropertyValueChangeEvent(source)
                for l in listenerList:
                    l.valueChange(event)


    def getListeners(self, eventType):
        if issubclass(eventType, prop.ValueChangeEvent):
            return list(self._propertyValueChangeListeners)

        return super(IndexedContainer, self).getListeners(eventType)


    def getCallbacks(self, eventType):
        if issubclass(eventType, prop.ValueChangeEvent):
            return dict(self._propertyValueChangeCallbacks)

        return super(IndexedContainer, self).getCallbacks(eventType)


    def fireItemAdded(self, position, itemId, item):
        if position >= 0:
            event = ItemSetChangeEvent(self, position)
            AbstractContainer.fireItemSetChange(self, event)


    def fireItemSetChange(self, event=None):
        if event is None:
            event = ItemSetChangeEvent(self, -1)
            super(IndexedContainer, self).fireItemSetChange(event)
        else:
            super(IndexedContainer, self).fireItemSetChange(event)


    def addSinglePropertyChangeListener(self, propertyId, itemId, listener):
        """Adds new single IProperty change listener.

        @param propertyId:
                   the ID of the IProperty to add.
        @param itemId:
                   the ID of the IItem .
        @param listener:
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

        @param propertyId:
                   the ID of the IProperty to remove.
        @param itemId:
                   the ID of the IItem.
        @param listener:
                   the listener to be removed.
        """
        if (listener is not None
                and self._singlePropertyValueChangeListeners is not None):

            propertySetToListenerListMap = \
                    self._singlePropertyValueChangeListeners.get(propertyId)

            if propertySetToListenerListMap is not None:
                listenerList = propertySetToListenerListMap.get(itemId)

                if listenerList is not None and listener in listenerList:
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

        @raise CloneNotSupportedException:
                    if an object cannot be cloned. .

        @deprecated: cloning support might be removed from IndexedContainer
                    in the future
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
                nc.items[idd] = it.clone()
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
        """Gets the string representation of the contents of the IItem. The
        format of the string is a space separated catenation of the string
        representations of the Properties contained by the IItem.

        @return: string representation of the IItem contents
        """
        retValue = ''

        for i, propertyId in enumerate(self._container._propertyIds):
            retValue += str(self.getItemProperty(propertyId))
            if i < len(self._container._propertyIds) - 1:
                retValue += ' '

        return retValue


    def __hash__(self):
        """Calculates a integer hash-code for the IItem that's unique inside
        the list. Two Items inside the same list have always different
        hash-codes, though Items in different lists may have identical
        hash-codes.

        @return: A locally unique hash-code as integer
        """
        return hash(self._itemId)


    def __eq__(self, obj):
        """Tests if the given object is the same as the this object. Two Items
        got from a list container with the same ID are equal.

        @param obj:
                   an object to compare with this object
        @return: C{True} if the given object is the same as this
                object, C{False} if not
        """
        if obj is None or obj.__class__ != IndexedContainerItem:
            return False

        li = obj

        return self.getHost() == li.getHost() and self._itemId == li._itemId


    def getHost(self):
        return self._container


    def addItemProperty(self, idd, prop):
        """IndexedContainerItem does not support adding new properties. Add
        properties at container level. See
        L{IndexedContainer.addContainerProperty}

        @see: L{IItem.addProperty}
        """
        raise NotImplementedError, ('Indexed container item '
                + 'does not support adding new properties')


    def removeItemProperty(self, idd):
        """Indexed container does not support removing properties. Remove
        properties at container level. See
        L{IndexedContainer.removeContainerProperty}

        @see: IItem.removeProperty
        """
        raise NotImplementedError, \
                'Indexed container item does not support property removal'


class IndexedContainerProperty(prop.IProperty, prop.IValueChangeNotifier):
    """A class implementing the L{IProperty} interface to be contained in
    the L{IndexedContainerItem} contained in the L{IndexedContainer}.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, itemId, propertyId, container):
        """Constructs a new L{IndexedContainerProperty} object.

        @param itemId:
                   the ID of the IItem to connect the new IProperty to.
        @param propertyId:
                   the IProperty ID of the new IProperty.
        @param container:
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
            if self._propertyId in propertySet:
                del propertySet[self._propertyId]
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
            self._container.filterAll()

        self._container.firePropertyValueChange(self)


    def __str__(self):
        """Returns the value of the IProperty in human readable textual format.
        The return value should be assignable to the C{setValue} method if the
        IProperty is not in read-only mode.

        @return: String representation of the value stored in the IProperty
        """
        value = self.getValue()

        if value is None:
            return ''

        return str(value)


    def __hash__(self):
        """Calculates a integer hash-code for the IProperty that's unique inside
        the IItem containing the IProperty. Two different Properties inside the
        same IItem contained in the same list always have different
        hash-codes, though Properties in different Items may have identical
        hash-codes.

        @return: A locally unique hash-code as integer
        """
        return hash(self._itemId) ^ hash(self._propertyId)


    def __eq__(self, obj):
        """Tests if the given object is the same as the this object. Two
        Properties got from an IItem with the same ID are equal.

        @param obj:
                   an object to compare with this object
        @return: C{True} if the given object is the same as this
                object, C{False} if not
        """
        if obj is None or obj.__class__ != IndexedContainerProperty:
            return False

        lp = obj

        return (lp.getHost() == self.getHost()
                and lp._propertyId == self._propertyId
                and lp._itemId == self._itemId)


    def addListener(self, listener, iface=None):
        if (isinstance(listener, prop.IValueChangeListener) and
                (iface is None or iface == prop.IValueChangeListener)):
            self._container.addSinglePropertyChangeListener(self._propertyId,
                    self._itemId, listener)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if eventType == prop.ValueChangeEvent:
            self._container.addSinglePropertyChangeListener(self._propertyId,
                    self._itemId, (callback, args))
        else:
            super(IndexedContainerProperty, self).addCallback(callback,
                    eventType, *args)


    def removeListener(self, listener, iface=None):
        if (isinstance(listener, prop.IValueChangeListener) and
                (iface is None or iface == prop.IValueChangeListener)):
            self._container.removeSinglePropertyChangeListener(self._propertyId,
                    self._itemId, listener)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if eventType == prop.ValueChangeEvent:
            self._container.removeSinglePropertyChangeListener(self._propertyId,
                    self._itemId, callback)

        else:
            super(IndexedContainer, self).removeCallback(callback, eventType)


    def getHost(self):
        return self._container


class ItemSetChangeEvent(BaseItemSetChangeEvent):
    """An C{Event} object specifying the list whose IItem set has changed.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, source, addedItemIndex):
        super(ItemSetChangeEvent, self).__init__(source)
        self._addedItemIndex = addedItemIndex


    def getAddedItemIndex(self):
        """Iff one item is added, gives its index.

        @return: -1 if either multiple items are changed or some other change
                than add is done.
        """
        return self._addedItemIndex


class PropertyValueChangeEvent(EventObject, prop.ValueChangeEvent):
    """An C{Event} object specifying the IProperty in a list whose
    value has changed.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, source):
        super(PropertyValueChangeEvent, self).__init__(source)


    def getProperty(self):
        return self.getSource()
