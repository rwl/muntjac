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

from com.vaadin.data.Item import (Item, PropertySetChangeEvent, PropertySetChangeNotifier,)


class PropertysetItem(Item, Item, PropertySetChangeNotifier, Cloneable):
    """Class for handling a set of identified Properties. The elements contained in
    a </code>MapItem</code> can be referenced using locally unique identifiers.
    The class supports listeners who are interested in changes to the Property
    set managed by the class.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # Private representation of the item
    # Mapping from property id to property.
    _map = dict()
    # List of all property ids to maintain the order.
    _list = LinkedList()
    # List of property set modification listeners.
    _propertySetChangeListeners = None
    # Item methods

    def getItemProperty(self, id):
        """Gets the Property corresponding to the given Property ID stored in the
        Item. If the Item does not contain the Property, <code>null</code> is
        returned.

        @param id
                   the identifier of the Property to get.
        @return the Property with the given ID or <code>null</code>
        """
        return self._map[id]

    def getItemPropertyIds(self):
        """Gets the collection of IDs of all Properties stored in the Item.

        @return unmodifiable collection containing IDs of the Properties stored
                the Item
        """
        # Item.Managed methods
        return Collections.unmodifiableCollection(self._list)

    def removeItemProperty(self, id):
        """Removes the Property identified by ID from the Item. This functionality
        is optional. If the method is not implemented, the method always returns
        <code>false</code>.

        @param id
                   the ID of the Property to be removed.
        @return <code>true</code> if the operation succeeded <code>false</code>
                if not
        """
        # Cant remove missing properties
        if self._map.remove(id) is None:
            return False
        self._list.remove(id)
        # Send change events
        self.fireItemPropertySetChange()
        return True

    def addItemProperty(self, id, property):
        """Tries to add a new Property into the Item.

        @param id
                   the ID of the new Property.
        @param property
                   the Property to be added and associated with the id.
        @return <code>true</code> if the operation succeeded, <code>false</code>
                if not
        """
        # Null ids are not accepted
        if id is None:
            raise self.NullPointerException('Item property id can not be null')
        # Cant add a property twice
        if id in self._map:
            return False
        # Put the property to map
        self._map.put(id, property)
        self._list.add(id)
        # Send event
        self.fireItemPropertySetChange()
        return True

    def toString(self):
        """Gets the <code>String</code> representation of the contents of the Item.
        The format of the string is a space separated catenation of the
        <code>String</code> representations of the Properties contained by the
        Item.

        @return <code>String</code> representation of the Item contents
        """
        # Notifiers
        retValue = ''
        _0 = True
        i = self.getItemPropertyIds()
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

    class PropertySetChangeEvent(EventObject, Item, PropertySetChangeEvent):
        """An <code>event</code> object specifying an Item whose Property set has
        changed.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """

        def __init__(self, source):
            super(PropertySetChangeEvent, self)(source)

        def getItem(self):
            """Gets the Item whose Property set has changed.

            @return source object of the event as an <code>Item</code>
            """
            return self.getSource()

    def addListener(self, listener):
        """Registers a new property set change listener for this Item.

        @param listener
                   the new Listener to be registered.
        """
        if self._propertySetChangeListeners is None:
            self._propertySetChangeListeners = LinkedList()
        self._propertySetChangeListeners.add(listener)

    def removeListener(self, listener):
        """Removes a previously registered property set change listener.

        @param listener
                   the Listener to be removed.
        """
        if self._propertySetChangeListeners is not None:
            self._propertySetChangeListeners.remove(listener)

    def fireItemPropertySetChange(self):
        """Sends a Property set change event to all interested listeners."""
        if self._propertySetChangeListeners is not None:
            l = list(self._propertySetChangeListeners)
            event = PropertysetItem.PropertySetChangeEvent(self)
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(l)):
                    break
                l[i].itemPropertySetChange(event)

    def getListeners(self, eventType):
        if Item.PropertySetChangeEvent.isAssignableFrom(eventType):
            if self._propertySetChangeListeners is None:
                return Collections.EMPTY_LIST
            else:
                return Collections.unmodifiableCollection(self._propertySetChangeListeners)
        return Collections.EMPTY_LIST

    def clone(self):
        """Creates and returns a copy of this object.
        <p>
        The method <code>clone</code> performs a shallow copy of the
        <code>PropertysetItem</code>.
        </p>
        <p>
        Note : All arrays are considered to implement the interface Cloneable.
        Otherwise, this method creates a new instance of the class of this object
        and initializes all its fields with exactly the contents of the
        corresponding fields of this object, as if by assignment, the contents of
        the fields are not themselves cloned. Thus, this method performs a
        "shallow copy" of this object, not a "deep copy" operation.
        </p>

        @throws CloneNotSupportedException
                    if the object's class does not support the Cloneable
                    interface.

        @see java.lang.Object#clone()
        """
        # (non-Javadoc)
        # 
        # @see java.lang.Object#equals(java.lang.Object)

        npsi = PropertysetItem()
        npsi.list = self._list.clone() if self._list is not None else None
        npsi.propertySetChangeListeners = self._propertySetChangeListeners.clone() if self._propertySetChangeListeners is not None else None
        npsi.map = self._map.clone()
        return npsi

    def equals(self, obj):
        # (non-Javadoc)
        # 
        # @see java.lang.Object#hashCode()

        if (obj is None) or (not isinstance(obj, PropertysetItem)):
            return False
        other = obj
        if other.list != self._list:
            if other.list is None:
                return False
            if not (other.list == self._list):
                return False
        if other.map != self._map:
            if other.map is None:
                return False
            if not (other.map == self._map):
                return False
        if other.propertySetChangeListeners != self._propertySetChangeListeners:
            thisEmpty = (self._propertySetChangeListeners is None) or self._propertySetChangeListeners.isEmpty()
            otherEmpty = (other.propertySetChangeListeners is None) or other.propertySetChangeListeners.isEmpty()
            if thisEmpty and otherEmpty:
                return True
            if otherEmpty:
                return False
            if not (other.propertySetChangeListeners == self._propertySetChangeListeners):
                return False
        return True

    def hashCode(self):
        return ((0 if self._list is None else self._list.hashCode()) ^ (0 if self._map is None else self._map.hashCode())) ^ (0 if (self._propertySetChangeListeners is None) or self._propertySetChangeListeners.isEmpty() else self._propertySetChangeListeners.hashCode())
