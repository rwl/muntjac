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

from muntjac.data.item import \
    IItem, IPropertySetChangeEvent, IPropertySetChangeNotifier, \
    IPropertySetChangeListener

from muntjac.util import EventObject


class PropertysetItem(IItem, IPropertySetChangeNotifier):  # Cloneable
    """Class for handling a set of identified Properties. The elements
    contained in a C{MapItem} can be referenced using locally unique
    identifiers. The class supports listeners who are interested in changes
    to the Property set managed by the class.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self):
        # Mapping from property id to property.
        self._map = dict()

        # List of all property ids to maintain the order.
        self._list = list()

        # List of property set modification listeners.
        self._propertySetChangeListeners = list()

        self._propertySetChangeCallbacks = dict()


    def getItemProperty(self, idd):
        """Gets the Property corresponding to the given Property ID stored in
        the Item. If the Item does not contain the Property, C{None} is
        returned.

        @param idd: the identifier of the Property to get.
        @return: the Property with the given ID or C{None}
        """
        return self._map.get(idd)


    def getItemPropertyIds(self):
        """Gets the collection of IDs of all Properties stored in the Item.

        @return: collection containing IDs of the Properties
                 stored the Item
        """
        return list(self._list)


    def removeItemProperty(self, idd):
        """Removes the Property identified by ID from the Item. This
        functionality is optional. If the method is not implemented, the
        method always returns C{False}.

        @param idd: the ID of the Property to be removed.
        @return: C{True} if the operation succeeded C{False} if not
        """
        # Cant remove missing properties
        if idd not in self._map:
            return False

        del self._map[idd]

        self._list.remove(idd)

        # Send change events
        self.fireItemPropertySetChange()

        return True


    def addItemProperty(self, idd, prop):
        """Tries to add a new Property into the Item.

        @param id:
                   the ID of the new Property.
        @param prop:
                   the Property to be added and associated with the id.
        @return: C{True} if the operation succeeded, C{False} if not
        """
        # Null ids are not accepted
        if idd is None:
            raise ValueError, 'Item property id can not be null'

        # Cant add a property twice
        if idd in self._map:
            return False

        # Put the property to map
        self._map[idd] = prop
        self._list.append(idd)

        # Send event
        self.fireItemPropertySetChange()

        return True


    def __str__(self):
        """Gets the string representation of the contents of the Item.
        The format of the string is a space separated catenation of the
        string representations of the Properties contained by the Item.

        @return: String representation of the Item contents
        """
        retValue = ''
        for i, propertyId in enumerate(self.getItemPropertyIds()):
            retValue += str( self.getItemProperty(propertyId) )
            if i < len(self.getItemPropertyIds()) - 1:
                retValue += ' '
        return retValue


    def addListener(self, listener, iface=None):
        """Registers a new property set change listener for this Item.

        @param listener: the new Listener to be registered.
        """
        if (isinstance(listener, IPropertySetChangeListener) and
            (iface is None or
                issubclass(iface, IPropertySetChangeListener))):
            self._propertySetChangeListeners.append(listener)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, IPropertySetChangeEvent):
            self._propertySetChangeCallbacks[callback] = args
        else:
            super(PropertysetItem, self).addCallback(callback,
                    eventType, *args)


    def removeListener(self, listener, iface=None):
        """Removes a previously registered property set change listener.

        @param listener: the Listener to be removed.
        """
        if (isinstance(listener, IPropertySetChangeListener) and
            (iface is None or
                issubclass(iface, IPropertySetChangeListener))):
            if listener in self._propertySetChangeListeners:
                self._propertySetChangeListeners.remove(listener)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, IPropertySetChangeEvent):
            if callback in self._propertySetChangeCallbacks:
                del self._propertySetChangeCallbacks[callback]
        else:
            super(PropertysetItem, self).removeCallback(callback, eventType)


    def fireItemPropertySetChange(self):
        """Sends a Property set change event to all interested listeners."""
        event = PropertySetChangeEvent(self)
        for listener in self._propertySetChangeListeners:
            listener.itemPropertySetChange(event)

        for callback, args in self._propertySetChangeCallbacks.iteritems():
            callback(event, *args)


    def getListeners(self, eventType):
        if issubclass(eventType, IPropertySetChangeEvent):
            return list(self._propertySetChangeListeners)
        return list()


    def getCallbacks(self, eventType):
        if issubclass(eventType, IPropertySetChangeEvent):
            return dict(self._propertySetChangeCallbacks)
        return dict()


    def clone(self):
        """Creates and returns a copy of this object.

        The method C{clone} performs a shallow copy of the C{PropertysetItem}.

        Note: All arrays are considered to implement the interface Cloneable.
        Otherwise, this method creates a new instance of the class of this
        object and initializes all its fields with exactly the contents of the
        corresponding fields of this object, as if by assignment, the contents
        of the fields are not themselves cloned. Thus, this method performs a
        "shallow copy" of this object, not a "deep copy" operation.

        @raise CloneNotSupportedException:
                    if the object's class does not support the Cloneable
                    interface.
        """
        npsi = PropertysetItem()
        npsi.list = list(self._list) if self._list is not None else None
        npsi.propertySetChangeListeners = list(self._propertySetChangeListeners)
        npsi.map = self._map.copy()
        return npsi


    def __eq__(self, obj):
        if (obj is None) or (not isinstance(obj, PropertysetItem)):
            return False

        other = obj
        if other._list != self._list:
            if other._list is None:
                return False
            if not (other._list == self._list):
                return False

        if other._map != self._map:
            if other._map is None:
                return False
            if other._map != self._map:
                return False

        if other._propertySetChangeListeners != self._propertySetChangeListeners:
            thisEmpty = ((self._propertySetChangeListeners is None)
                    or len(self._propertySetChangeListeners) == 0)

            otherEmpty = ((other.propertySetChangeListeners is None)
                    or len(other.propertySetChangeListeners) == 0)

            if thisEmpty and otherEmpty:
                return True

            if otherEmpty:
                return False

            if (other.propertySetChangeListeners !=
                    self._propertySetChangeListeners):
                return False

        return True


    def __hash__(self):
        return (((0 if self._list is None else hash(self._list))
                ^ (0 if self._map is None else hash(self._map)))
                ^ (0 if (self._propertySetChangeListeners is None)
                        or (len(self._propertySetChangeListeners) == 0)
                        else hash(self._propertySetChangeListeners)))


class PropertySetChangeEvent(EventObject, IItem, IPropertySetChangeEvent):
    """An C{event} object specifying an Item whose Property set has
    changed.

    @author: Vaadin Ltd.
    @version: 1.1.0
    """

    def __init__(self, source):
        super(PropertySetChangeEvent, self).__init__(source)


    def getItem(self):
        """Gets the Item whose Property set has changed.

        @return: source object of the event as an C{Item}
        """
        return self.getSource()
