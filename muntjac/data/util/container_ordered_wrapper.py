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

from muntjac.data.container \
    import IOrdered, IItemSetChangeNotifier, IPropertySetChangeNotifier,\
    IItemSetChangeListener, IPropertySetChangeListener, IItemSetChangeEvent,\
    IPropertySetChangeEvent


class ContainerOrderedWrapper(IOrdered, IItemSetChangeNotifier,
            IPropertySetChangeNotifier):
    """A wrapper class for adding external ordering to containers not
    implementing the L{IOrdered} interface.

    If the wrapped container is changed directly (that is, not through the
    wrapper), and does not implement Container.ItemSetChangeNotifier and/or
    PropertySetChangeNotifier the hierarchy information must be updated with
    the L{updateOrderWrapper} method.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, toBeWrapped):
        """Constructs a new ordered wrapper for an existing Container. Works even if
        the to-be-wrapped container already implements the Container.Ordered
        interface.

        @param toBeWrapped
                   the container whose contents need to be ordered.
        """
        #: The wrapped container
        self._container = toBeWrapped

        #: Ordering information, ie. the mapping from Item ID to the next
        #  item ID
        self._next = None

        #: Reverse ordering information for convenience and performance
        #  reasons.
        self._prev = None

        #: ID of the first Item in the container.
        self._first = None

        #: ID of the last Item in the container.
        self._last = None

        #: Is the wrapped container ordered by itself, ie. does it implement
        #  the IOrdered interface by itself? If it does, this class will use
        #  the methods of the underlying container directly.
        self._ordered = False

        #: The last known size of the wrapped container. Used to check whether
        #  items have been added or removed to the wrapped container, when the
        #  wrapped container does not send ItemSetChangeEvents.
        self._lastKnownSize = -1

        self._ordered = isinstance(self._container, IOrdered)

        # Checks arguments
        if self._container is None:
            raise ValueError, 'Null can not be wrapped'

        # Creates initial order if needed
        self.updateOrderWrapper()


    def removeFromOrderWrapper(self, idd):
        """Removes the specified Item from the wrapper's internal hierarchy
        structure.

        Note : The Item is not removed from the underlying Container.

        @param idd:
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

        @param idd
                   the ID of the Item to be added to the ordering.
        ---
        Registers the specified Item after the specified itemId in the wrapper's
        internal ordering. The underlying container is not modified. Given item
        idd must be in the container, or must be null.

        @param idd
                   the ID of the Item to be added to the ordering.
        @param previousItemId
                   the Id of the previous item.
        """
        # Adds the if to tail

        if previousItemId == None:
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
                self._next[idd] = self._next[previousItemId]
                self._prev[self._next.get(previousItemId)] = idd
                self._next[previousItemId] = idd


    def updateOrderWrapper(self):
        """Updates the wrapper's internal ordering information to include all
        Items in the underlying container.

        Note: If the contents of the wrapped container change without the
        wrapper's knowledge, this method needs to be called to update the
        ordering information of the Items.
        """
        # Gets the first item stored in the ordered container.
        if not self._ordered:
            ids = self._container.getItemIds()
            # Recreates ordering if some parts of it are missing
            if (self._next is None or self._first is None
                    or self._last is None or self._prev is not None):
                self._first = None
                self._last = None
                self._next = dict()
                self._prev = dict()

            # Filter out all the missing items
            for idd in self._next:
                if not self._container.containsId(idd):
                    self.removeFromOrderWrapper(idd)

            # Adds missing items
            for idd in ids:
                if idd not in self._next:
                    self.addToOrderWrapper(idd)


    def firstItemId(self):
        # Tests if the given item is the first item in the container.
        if self._ordered:
            return self._container.firstItemId()
        return self._first


    def isFirstId(self, itemId):
        # Tests if the given item is the last item in the container.
        if self._ordered:
            return self._container.isFirstId(itemId)
        return self._first is not None and self._first == itemId


    def isLastId(self, itemId):
        # Gets the last item stored in the ordered container.
        if self._ordered:
            return self._container.isLastId(itemId)
        return self._last is not None and self._last == itemId


    def lastItemId(self):
        # Gets the item that is next from the specified item.
        if self._ordered:
            return self._container.lastItemId()
        return self._last


    def nextItemId(self, itemId):
        # Gets the item that is previous from the specified item.
        if self._ordered:
            return self._container.nextItemId(itemId)

        if itemId is None:
            return None

        return self._next.get(itemId)


    def prevItemId(self, itemId):
        if self._ordered:
            return self._container.prevItemId(itemId)

        if itemId is None:
            return None

        return self._prev.get(itemId)


    def addContainerProperty(self, propertyId, typ, defaultValue):
        """Registers a new Property to all Items in the Container.

        @param propertyId:
                   the ID of the new Property.
        @param typ:
                   the Data type of the new Property.
        @param defaultValue:
                   the value all created Properties are initialized to.
        @return: C{True} if the operation succeeded, C{False} if not
        """
        return self._container.addContainerProperty(propertyId, typ,
                defaultValue)


    def addItem(self, itemId=None):
        """Creates a new Item into the Container, assigns it an automatic ID,
        and adds it to the ordering. Alternatively, registers a new Item by
        its ID to the underlying container and to the ordering.

        @param itemId:
                   the ID of the Item to be created.
        @return:
                   C{None} if the operation failed
        @raise NotImplementedError:
                   if the addItem is not supported.
        """
        if itemId is None:
            idd = self._container.addItem()
            if not self._ordered and (idd is not None):
                self.addToOrderWrapper(idd)
            return idd
        else:
            item = self._container.addItem(itemId)
            if not self._ordered and (item is not None):
                self.addToOrderWrapper(itemId)
            return item


    def removeAllItems(self):
        """Removes all items from the underlying container and from the
        ordering.

        @return: C{True} if the operation succeeded, otherwise C{False}
        @raise NotImplementedError:
                    if the removeAllItems is not supported.
        """
        success = self._container.removeAllItems()
        if (not self._ordered) and success:
            self._first = self._last = None
            self._next.clear()
            self._prev.clear()
        return success


    def removeItem(self, itemId):
        """Removes an Item specified by the itemId from the underlying
        container and from the ordering.

        @param itemId:
                   the ID of the Item to be removed.
        @return: C{True} if the operation succeeded, C{False} if not
        @raise NotImplementedError:
                   if the removeItem is not supported.
        """
        success = self._container.removeItem(itemId)
        if not self._ordered and success:
            self.removeFromOrderWrapper(itemId)
        return success


    def removeContainerProperty(self, propertyId):
        """Removes the specified Property from the underlying container and
        from the ordering.

        Note: The Property will be removed from all the Items in the Container.

        @param propertyId:
                   the ID of the Property to remove.
        @return: C{True} if the operation succeeded, C{False} if not
        @raise NotImplementedError:
                   if the removeContainerProperty is not supported.
        """
        return self._container.removeContainerProperty(propertyId)


    def containsId(self, itemId):
        # Does the container contain the specified Item?
        return self._container.containsId(itemId)


    def getItem(self, itemId):
        # Gets the specified Item from the container.
        return self._container.getItem(itemId)


    def getItemIds(self):
        # Gets the ID's of all Items stored in the Container
        return self._container.getItemIds()


    def getContainerProperty(self, itemId, propertyId):
        # Gets the Property identified by the given itemId and propertyId
        # from the Container.
        return self._container.getContainerProperty(itemId, propertyId)


    def getContainerPropertyIds(self):
        # Gets the ID's of all Properties stored in the Container
        return self._container.getContainerPropertyIds()


    def getType(self, propertyId):
        # Gets the data type of all Properties identified by the given
        # Property ID.
        return self._container.getType(propertyId)


    def size(self):
        # Gets the number of Items in the Container.
        newSize = len(self._container)
        if (self._lastKnownSize != -1 and newSize != self._lastKnownSize
                and not isinstance(self._container, IItemSetChangeNotifier)):
            # Update the internal cache when the size of the container changes
            # and the container is incapable of sending ItemSetChangeEvents
            self.updateOrderWrapper()
        self._lastKnownSize = newSize
        return newSize


    def __len__(self):
        return self.size()


    def addListener(self, listener, iface=None):
        if (isinstance(listener, IItemSetChangeListener) and
                (iface is None or issubclass(iface, IItemSetChangeListener))):
            # Registers a new Item set change listener for this Container.
            if isinstance(self._container, IItemSetChangeNotifier):
                pl = PiggybackListener(listener, self)
                self._container.addListener(pl, IItemSetChangeListener)

        if (isinstance(listener, IPropertySetChangeListener) and
                (iface is None or
                        issubclass(iface, IPropertySetChangeListener))):
            # Registers a new Property set change listener for this Container.
            if isinstance(self._container, IPropertySetChangeNotifier):
                pl = PiggybackListener(listener, self)
                self._container.addListener(pl, IPropertySetChangeListener)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, IItemSetChangeEvent):
            # Registers a new Item set change listener for this Container.
            if isinstance(self._container, IItemSetChangeNotifier):
                pl = PiggybackListener(callback, self, *args)
                self._container.addListener(pl, IItemSetChangeListener)

        elif issubclass(eventType, IPropertySetChangeEvent):
            # Registers a new Property set change listener for this Container.
            if isinstance(self._container, IPropertySetChangeNotifier):
                pl = PiggybackListener(callback, self, *args)
                self._container.addListener(pl, IPropertySetChangeListener)

        else:
            super(ContainerOrderedWrapper, self).addCallback(callback,
                    eventType, *args)


    def removeListener(self, listener, iface=None):
        if (isinstance(listener, IItemSetChangeListener) and
                (iface is None or issubclass(iface, IItemSetChangeListener))):
            # Removes a Item set change listener from the object.
            if isinstance(self._container, IItemSetChangeNotifier):
                pl = PiggybackListener(listener, self)
                self._container.removeListener(pl, IItemSetChangeListener)


        if (isinstance(listener, IPropertySetChangeListener) and
            (iface is None or issubclass(iface, IPropertySetChangeListener))):
            # Removes a Property set change listener from the object.
            if isinstance(self._container, IPropertySetChangeNotifier):
                pl = PiggybackListener(listener, self)
                self._container.removeListener(pl, IPropertySetChangeListener)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, IItemSetChangeEvent):
            # Removes a Item set change listener from the object.
            if isinstance(self._container, IItemSetChangeNotifier):
                pl = PiggybackListener(callback, self)
                self._container.removeListener(pl, IItemSetChangeListener)

        elif issubclass(eventType, IPropertySetChangeEvent):
            # Removes a Property set change listener from the object.
            if isinstance(self._container, IPropertySetChangeNotifier):
                pl = PiggybackListener(callback, self)
                self._container.removeListener(pl, IPropertySetChangeListener)

        else:
            super(ContainerOrderedWrapper, self).removeCallback(callback,
                    eventType)


    def addItemAfter(self, previousItemId, newItemId=None):
        # If the previous item is not in the container, fail

        if newItemId == None:
            if ((previousItemId is not None)
                    and not self.containsId(previousItemId)):
                return None

            # Adds the item to container
            idd = self._container.addItem()

            # Puts the new item to its correct place
            if not self._ordered and idd is not None:
                self.addToOrderWrapper(idd, previousItemId)

            return idd
        else:
            if ((previousItemId is not None)
                    and not self.containsId(previousItemId)):
                return None

            # Adds the item to container
            item = self._container.addItem(newItemId)

            # Puts the new item to its correct place
            if not self._ordered and item is not None:
                self.addToOrderWrapper(newItemId, previousItemId)

            return item


class PiggybackListener(IPropertySetChangeListener, IItemSetChangeListener):
    """This listener 'piggybacks' on the real listener in order to update the
    wrapper when needed. It proxies __eq__() and __hash__() to the real
    listener so that the correct listener gets removed.
    """

    def __init__(self, realListener, wrapper, *args):
        self._listener = realListener
        self._wrapper = wrapper
        self._args = args


    def containerItemSetChange(self, event):
        self._wrapper.updateOrderWrapper()
        if isinstance(self._listener, IItemSetChangeListener):
            self._listener.containerItemSetChange(event)
        else:
            self._listener(event, *self._args)


    def containerPropertySetChange(self, event):
        self._wrapper.updateOrderWrapper()
        if isinstance(self._listener, IPropertySetChangeListener):
            self._listener.containerPropertySetChange(event)
        else:
            self._listener(event, *self._args)


    def __eq__(self, obj):
        return ((obj == self._listener)
                or (obj is not None and obj == self._listener))


    def __hash__(self):
        return hash(self._listener)
