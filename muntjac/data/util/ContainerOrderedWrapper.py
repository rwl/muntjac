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

from muntjac.data.Container import \
    Container, ItemSetChangeListener, ItemSetChangeNotifier, Ordered, \
    PropertySetChangeListener, PropertySetChangeNotifier


class ContainerOrderedWrapper(Container, Ordered, Container,
                              ItemSetChangeNotifier, Container,
                              PropertySetChangeNotifier):
    """A wrapper class for adding external ordering to containers not implementing
    the {@link com.vaadin.data.Container.Ordered} interface.

    If the wrapped container is changed directly (that is, not through the
    wrapper), and does not implement Container.ItemSetChangeNotifier and/or
    Container.PropertySetChangeNotifier the hierarchy information must be updated
    with the {@link #updateOrderWrapper()} method.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """

    def __init__(self, toBeWrapped):
        """Constructs a new ordered wrapper for an existing Container. Works even if
        the to-be-wrapped container already implements the Container.Ordered
        interface.

        @param toBeWrapped
                   the container whose contents need to be ordered.
        """
        # The wrapped container
        self._container = None

        # Ordering information, ie. the mapping from Item ID to the next item ID
        self._next = None

        # Reverse ordering information for convenience and performance reasons.
        self._prev = None

        # ID of the first Item in the container.
        self._first = None

        # ID of the last Item in the container.
        self._last = None

        # Is the wrapped container ordered by itself, ie. does it implement the
        # Container.Ordered interface by itself? If it does, this class will use
        # the methods of the underlying container directly.
        self._ordered = False

        self._container = toBeWrapped
        self._ordered = isinstance(self._container, Ordered)

        # Checks arguments
        if self._container is None:
            raise ValueError, 'Null can not be wrapped'

        # Creates initial order if needed
        self.updateOrderWrapper()


    def removeFromOrderWrapper(self, idd):
        """Removes the specified Item from the wrapper's internal hierarchy
        structure.
        <p>
        Note : The Item is not removed from the underlying Container.
        </p>

        @param id
                   the ID of the Item to be removed from the ordering.
        """
        if idd is not None:
            pid = self._prev.get(idd)
            nid = self._next.get(idd)
            if self._first == idd:
                self._first = nid
            if self._last == idd:
                self._first = pid
            if nid is not None:
                self._prev[nid] = pid
            if pid is not None:
                self._next[pid] = nid
            del self._next[idd]
            del self._prev[idd]


    def addToOrderWrapper(self, idd, previousItemId=None):
        """Registers the specified Item to the last position in the wrapper's
        internal ordering. The underlying container is not modified.

        @param id
                   the ID of the Item to be added to the ordering.
        ---
        Registers the specified Item after the specified itemId in the wrapper's
        internal ordering. The underlying container is not modified. Given item
        id must be in the container, or must be null.

        @param id
                   the ID of the Item to be added to the ordering.
        @param previousItemId
                   the Id of the previous item.
        """
        if previousItemId is None:
            # Adds the if to tail
            if self._last is not None:
                self._next[self._last] = idd
                self._prev[idd] = self._last
                self._last = idd
            else:
                self._first = self._last = idd
        else:
            if (self._last == previousItemId) or (self._last is None):
                self.addToOrderWrapper(idd)
            elif previousItemId is None:
                self._next[idd] = self._first
                self._prev[self._first] = idd
                self._first = idd
            else:
                self._prev[idd] = previousItemId
                self._next[idd] = self._next.get(previousItemId)
                self._prev[self._next.get(previousItemId)] = idd
                self._next[previousItemId] = idd


    def updateOrderWrapper(self):
        """Updates the wrapper's internal ordering information to include all Items
        in the underlying container.
        <p>
        Note : If the contents of the wrapped container change without the
        wrapper's knowledge, this method needs to be called to update the
        ordering information of the Items.
        </p>
        """
        if not self._ordered:

            ids = self._container.getItemIds()

            # Recreates ordering if some parts of it are missing
            if self._next is None \
                    or self._first is None \
                    or self._last is None \
                    or self._prev is not None:
                self._first = None
                self._last = None
                self._next = dict()
                self._prev = dict()

            # Filter out all the missing items
            l = list(self._next.keys())
            for idd in l:
                if not self._container.containsId(idd):
                    self.removeFromOrderWrapper(idd)

            # Adds missing items
            for idd in ids:
                if not (idd in self._next):
                    self.addToOrderWrapper(idd)


    def firstItemId(self):
        # Gets the first item stored in the ordered container Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.
        if self._ordered:
            return self._container.firstItemId()

        return self._first


    def isFirstId(self, itemId):
        # Tests if the given item is the first item in the container Don't add a
        # JavaDoc comment here, we use the default documentation from implemented
        # interface.
        if self._ordered:
            return self._container.isFirstId(itemId)

        return self._first is not None and self._first == itemId


    def isLastId(self, itemId):
        # Tests if the given item is the last item in the container Don't add a
        # JavaDoc comment here, we use the default documentation from implemented
        # interface.
        if self._ordered:
            return self._container.isLastId(itemId)

        return self._last is not None and self._last == itemId


    def lastItemId(self):
        # Gets the last item stored in the ordered container Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.
        if self._ordered:
            return self._container.lastItemId()

        return self._last


    def nextItemId(self, itemId):
        # Gets the item that is next from the specified item. Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.
        if self._ordered:
            return self._container.nextItemId(itemId)

        if itemId is None:
            return None

        return self._next.get(itemId)


    def prevItemId(self, itemId):
        # Gets the item that is previous from the specified item. Don't add a
        # JavaDoc comment here, we use the default documentation from implemented
        # interface.
        if self._ordered:
            return self._container.prevItemId(itemId)

        if itemId is None:
            return None

        return self._prev.get(itemId)


    def addContainerProperty(self, propertyId, typ, defaultValue):
        """Registers a new Property to all Items in the Container.

        @param propertyId
                   the ID of the new Property.
        @param type
                   the Data type of the new Property.
        @param defaultValue
                   the value all created Properties are initialized to.
        @return <code>true</code> if the operation succeeded, <code>false</code>
                if not
        """
        return self._container.addContainerProperty(propertyId, typ, defaultValue)


    def addItem(self, itemId=None):
        """Creates a new Item into the Container, assigns it an automatic ID, and
        adds it to the ordering.

        @return the autogenerated ID of the new Item or <code>null</code> if the
                operation failed
        @throws UnsupportedOperationException
                    if the addItem is not supported.
        ---
        Registers a new Item by its ID to the underlying container and to the
        ordering.

        @param itemId
                   the ID of the Item to be created.
        @return the added Item or <code>null</code> if the operation failed
        @throws UnsupportedOperationException
                    if the addItem is not supported.
        """
        if itemId is None:
            idd = self._container.addItem()
            if not self._ordered and idd is not None:
                self.addToOrderWrapper(idd)
            return idd
        else:
            item = self._container.addItem(itemId)
            if not self._ordered and item is not None:
                self.addToOrderWrapper(itemId)
            return item


    def removeAllItems(self):
        """Removes all items from the underlying container and from the ordering.

        @return <code>true</code> if the operation succeeded, otherwise
                <code>false</code>
        @throws UnsupportedOperationException
                    if the removeAllItems is not supported.
        """
        success = self._container.removeAllItems()
        if not self._ordered and success:
            self._first = self._last = None
            self._next.clear()
            self._prev.clear()

        return success


    def removeItem(self, itemId):
        """Removes an Item specified by the itemId from the underlying container and
        from the ordering.

        @param itemId
                   the ID of the Item to be removed.
        @return <code>true</code> if the operation succeeded, <code>false</code>
                if not
        @throws UnsupportedOperationException
                    if the removeItem is not supported.
        """
        success = self._container.removeItem(itemId)
        if not self._ordered and success:
            self.removeFromOrderWrapper(itemId)
        return success


    def removeContainerProperty(self, propertyId):
        """Removes the specified Property from the underlying container and from the
        ordering.
        <p>
        Note : The Property will be removed from all the Items in the Container.
        </p>

        @param propertyId
                   the ID of the Property to remove.
        @return <code>true</code> if the operation succeeded, <code>false</code>
                if not
        @throws UnsupportedOperationException
                    if the removeContainerProperty is not supported.
        """
        return self._container.removeContainerProperty(propertyId)


    def containsId(self, itemId):
        # Does the container contain the specified Item? Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.
        return self._container.containsId(itemId)


    def getItem(self, itemId):
        # Gets the specified Item from the container. Don't add a JavaDoc comment
        # here, we use the default documentation from implemented interface.
        return self._container.getItem(itemId)


    def getItemIds(self):
        # Gets the ID's of all Items stored in the Container Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.
        return self._container.getItemIds()


    def getContainerProperty(self, itemId, propertyId):
        # Gets the Property identified by the given itemId and propertyId from the
        # Container Don't add a JavaDoc comment here, we use the default
        # documentation from implemented interface.
        return self._container.getContainerProperty(itemId, propertyId)


    def getContainerPropertyIds(self):
        # Gets the ID's of all Properties stored in the Container Don't add a
        # JavaDoc comment here, we use the default documentation from implemented
        # interface.
        return self._container.getContainerPropertyIds()


    def getType(self, propertyId):
        # Gets the data type of all Properties identified by the given Property ID.
        # Don't add a JavaDoc comment here, we use the default documentation from
        # implemented interface.
        return self._container.getType(propertyId)


    def size(self):
        # Gets the number of Items in the Container. Don't add a JavaDoc comment
        # here, we use the default documentation from implemented interface.
        return len(self._container)


    def addListener(self, listener):
        # Registers a new Item set change listener for this Container. Don't add a
        # JavaDoc comment here, we use the default documentation from implemented
        # interface.
        # Registers a new Property set change listener for this Container. Don't
        # add a JavaDoc comment here, we use the default documentation from
        # implemented interface.
        if isinstance(listener, ItemSetChangeListener):
            if isinstance(self._container, ItemSetChangeNotifier):
                self._container.addListener( PiggybackListener(listener, self) )  # FIXME: inner class
        else:
            if isinstance(self._container, PropertySetChangeNotifier):
                self._container.addListener( PiggybackListener(listener, self) )  # FIXME: inner class


    def removeListener(self, listener):
        # Removes a Item set change listener from the object. Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.
        # Removes a Property set change listener from the object. Don't add a
        # JavaDoc comment here, we use the default documentation from implemented
        # interface.
        if isinstance(listener, ItemSetChangeListener):
            if isinstance(self._container, ItemSetChangeNotifier):
                self._container.removeListener( PiggybackListener(listener, self) )  # FIXME: inner class
        else:
            if isinstance(self._container, PropertySetChangeNotifier):
                self._container.removeListener( PiggybackListener(listener, self) )  # FIXME: inner class


    def addItemAfter(self, previousItemId, newItemId=None):
        if newItemId is None:
            # If the previous item is not in the container, fail
            if previousItemId is not None and not self.containsId(previousItemId):
                return None
            # Adds the item to container
            idd = self._container.addItem()
            # Puts the new item to its correct place
            if not self._ordered and idd is not None:
                self.addToOrderWrapper(idd, previousItemId)
            return idd
        else:
            # If the previous item is not in the container, fail
            if previousItemId is not None and not self.containsId(previousItemId):
                return None
            # Adds the item to container
            item = self._container.addItem(newItemId)
            # Puts the new item to its correct place
            if not self._ordered and item is not None:
                self.addToOrderWrapper(newItemId, previousItemId)
            return item


class PiggybackListener(Container, PropertySetChangeListener, Container,
                        ItemSetChangeListener):
    """This listener 'piggybacks' on the real listener in order to update the
    wrapper when needed. It proxies equals() and hashCode() to the real
    listener so that the correct listener gets removed.
    """

    def __init__(self, realListener, wrapper):  # FIXME: inner class
        self._listener = realListener
        self._wrapper = wrapper


    def containerItemSetChange(self, event):
        self._wrapper.updateOrderWrapper()
        self._listener.containerItemSetChange(event)


    def containerPropertySetChange(self, event):
        self._wrapper.updateOrderWrapper()
        self._listener.containerPropertySetChange(event)


    def equals(self, obj):
        return (obj == self._listener) \
                or (obj is not None and obj == self._listener)


    def hashCode(self):
        return self._listener.hashCode()
