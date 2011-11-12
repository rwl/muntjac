# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.data.Container import (Container,)
# from java.util.Collection import (Collection,)
# from java.util.Hashtable import (Hashtable,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedList import (LinkedList,)


class ContainerOrderedWrapper(Container.Ordered, Container.ItemSetChangeNotifier, Container.PropertySetChangeNotifier):
    """<p>
    A wrapper class for adding external ordering to containers not implementing
    the {@link com.vaadin.data.Container.Ordered} interface.
    </p>

    <p>
    If the wrapped container is changed directly (that is, not through the
    wrapper), and does not implement Container.ItemSetChangeNotifier and/or
    Container.PropertySetChangeNotifier the hierarchy information must be updated
    with the {@link #updateOrderWrapper()} method.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # The wrapped container
    _container = None
    # Ordering information, ie. the mapping from Item ID to the next item ID
    _next = None
    # Reverse ordering information for convenience and performance reasons.
    _prev = None
    # ID of the first Item in the container.
    _first = None
    # ID of the last Item in the container.
    _last = None
    # Is the wrapped container ordered by itself, ie. does it implement the
    # Container.Ordered interface by itself? If it does, this class will use
    # the methods of the underlying container directly.

    _ordered = False
    # The last known size of the wrapped container. Used to check whether items
    # have been added or removed to the wrapped container, when the wrapped
    # container does not send ItemSetChangeEvents.

    _lastKnownSize = -1

    def __init__(self, toBeWrapped):
        """Constructs a new ordered wrapper for an existing Container. Works even if
        the to-be-wrapped container already implements the Container.Ordered
        interface.

        @param toBeWrapped
                   the container whose contents need to be ordered.
        """
        self._container = toBeWrapped
        self._ordered = isinstance(self._container, Container.Ordered)
        # Checks arguments
        if self._container is None:
            raise self.NullPointerException('Null can not be wrapped')
        # Creates initial order if needed
        self.updateOrderWrapper()

    def removeFromOrderWrapper(self, id):
        """Removes the specified Item from the wrapper's internal hierarchy
        structure.
        <p>
        Note : The Item is not removed from the underlying Container.
        </p>

        @param id
                   the ID of the Item to be removed from the ordering.
        """
        if id is not None:
            pid = self._prev[id]
            nid = self._next[id]
            if self._first == id:
                self._first = nid
            if self._last == id:
                self._first = pid
            if nid is not None:
                self._prev.put(nid, pid)
            if pid is not None:
                self._next.put(pid, nid)
            self._next.remove(id)
            self._prev.remove(id)

    def addToOrderWrapper(self, *args):
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
        # Adds the if to tail
        _0 = args
        _1 = len(args)
        if _1 == 1:
            id, = _0
            if self._last is not None:
                self._next.put(self._last, id)
                self._prev.put(id, self._last)
                self._last = id
            else:
                self._first = self._last = id
        elif _1 == 2:
            id, previousItemId = _0
            if (self._last == previousItemId) or (self._last is None):
                self.addToOrderWrapper(id)
            elif previousItemId is None:
                self._next.put(id, self._first)
                self._prev.put(self._first, id)
                self._first = id
            else:
                self._prev.put(id, previousItemId)
                self._next.put(id, self._next[previousItemId])
                self._prev.put(self._next[previousItemId], id)
                self._next.put(previousItemId, id)
        else:
            raise ARGERROR(1, 2)

    def updateOrderWrapper(self):
        """Updates the wrapper's internal ordering information to include all Items
        in the underlying container.
        <p>
        Note : If the contents of the wrapped container change without the
        wrapper's knowledge, this method needs to be called to update the
        ordering information of the Items.
        </p>
        """
        # Gets the first item stored in the ordered container Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        if not self._ordered:
            ids = self._container.getItemIds()
            # Recreates ordering if some parts of it are missing
            if (
                (((self._next is None) or (self._first is None)) or (self._last is None)) or (self._prev is not None)
            ):
                self._first = None
                self._last = None
                self._next = dict()
                self._prev = dict()
            # Filter out all the missing items
            l = LinkedList(self._next.keys())
            _0 = True
            i = l
            while True:
                if _0 is True:
                    _0 = False
                if not i.hasNext():
                    break
                id = i.next()
                if not self._container.containsId(id):
                    self.removeFromOrderWrapper(id)
            # Adds missing items
            _1 = True
            i = ids
            while True:
                if _1 is True:
                    _1 = False
                if not i.hasNext():
                    break
                id = i.next()
                if not (id in self._next):
                    self.addToOrderWrapper(id)

    def firstItemId(self):
        # Tests if the given item is the first item in the container Don't add a
        # JavaDoc comment here, we use the default documentation from implemented
        # interface.

        if self._ordered:
            return self._container.firstItemId()
        return self._first

    def isFirstId(self, itemId):
        # Tests if the given item is the last item in the container Don't add a
        # JavaDoc comment here, we use the default documentation from implemented
        # interface.

        if self._ordered:
            return self._container.isFirstId(itemId)
        return self._first is not None and self._first == itemId

    def isLastId(self, itemId):
        # Gets the last item stored in the ordered container Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        if self._ordered:
            return self._container.isLastId(itemId)
        return self._last is not None and self._last == itemId

    def lastItemId(self):
        # Gets the item that is next from the specified item. Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        if self._ordered:
            return self._container.lastItemId()
        return self._last

    def nextItemId(self, itemId):
        # Gets the item that is previous from the specified item. Don't add a
        # JavaDoc comment here, we use the default documentation from implemented
        # interface.

        if self._ordered:
            return self._container.nextItemId(itemId)
        if itemId is None:
            return None
        return self._next[itemId]

    def prevItemId(self, itemId):
        if self._ordered:
            return self._container.prevItemId(itemId)
        if itemId is None:
            return None
        return self._prev[itemId]

    def addContainerProperty(self, propertyId, type, defaultValue):
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
        return self._container.addContainerProperty(propertyId, type, defaultValue)

    def addItem(self, *args):
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
        _0 = args
        _1 = len(args)
        if _1 == 0:
            id = self._container.addItem()
            if not self._ordered and id is not None:
                self.addToOrderWrapper(id)
            return id
        elif _1 == 1:
            itemId, = _0
            item = self._container.addItem(itemId)
            if not self._ordered and item is not None:
                self.addToOrderWrapper(itemId)
            return item
        else:
            raise ARGERROR(0, 1)

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
        # Does the container contain the specified Item? Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        return self._container.removeContainerProperty(propertyId)

    def containsId(self, itemId):
        # Gets the specified Item from the container. Don't add a JavaDoc comment
        # here, we use the default documentation from implemented interface.

        return self._container.containsId(itemId)

    def getItem(self, itemId):
        # Gets the ID's of all Items stored in the Container Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        return self._container.getItem(itemId)

    def getItemIds(self):
        # Gets the Property identified by the given itemId and propertyId from the
        # Container Don't add a JavaDoc comment here, we use the default
        # documentation from implemented interface.

        return self._container.getItemIds()

    def getContainerProperty(self, itemId, propertyId):
        # Gets the ID's of all Properties stored in the Container Don't add a
        # JavaDoc comment here, we use the default documentation from implemented
        # interface.

        return self._container.getContainerProperty(itemId, propertyId)

    def getContainerPropertyIds(self):
        # Gets the data type of all Properties identified by the given Property ID.
        # Don't add a JavaDoc comment here, we use the default documentation from
        # implemented interface.

        return self._container.getContainerPropertyIds()

    def getType(self, propertyId):
        # Gets the number of Items in the Container. Don't add a JavaDoc comment
        # here, we use the default documentation from implemented interface.

        return self._container.getType(propertyId)

    def size(self):
        # Registers a new Item set change listener for this Container. Don't add a
        # JavaDoc comment here, we use the default documentation from implemented
        # interface.

        newSize = len(self._container)
        if (
            self._lastKnownSize != -1 and newSize != self._lastKnownSize and not isinstance(self._container, Container.ItemSetChangeNotifier)
        ):
            # Update the internal cache when the size of the container changes
            # and the container is incapable of sending ItemSetChangeEvents
            self.updateOrderWrapper()
        self._lastKnownSize = newSize
        return newSize

    def addListener(self, *args):
        # Removes a Item set change listener from the object. Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Container.ItemSetChangeListener):
                listener, = _0
                if isinstance(self._container, Container.ItemSetChangeNotifier):
                    self._container.addListener(self.PiggybackListener(listener))
            else:
                listener, = _0
                if isinstance(self._container, Container.PropertySetChangeNotifier):
                    self._container.addListener(self.PiggybackListener(listener))
        else:
            raise ARGERROR(1, 1)

    def removeListener(self, *args):
        # Registers a new Property set change listener for this Container. Don't
        # add a JavaDoc comment here, we use the default documentation from
        # implemented interface.

        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Container.ItemSetChangeListener):
                listener, = _0
                if isinstance(self._container, Container.ItemSetChangeNotifier):
                    self._container.removeListener(self.PiggybackListener(listener))
            else:
                listener, = _0
                if isinstance(self._container, Container.PropertySetChangeNotifier):
                    self._container.removeListener(self.PiggybackListener(listener))
        else:
            raise ARGERROR(1, 1)

    # Removes a Property set change listener from the object. Don't add a
    # JavaDoc comment here, we use the default documentation from implemented
    # interface.

    # (non-Javadoc)
    # 
    # @see com.vaadin.data.Container.Ordered#addItemAfter(java.lang.Object,
    # java.lang.Object)

    def addItemAfter(self, *args):
        # If the previous item is not in the container, fail
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.Container.Ordered#addItemAfter(java.lang.Object)

        _0 = args
        _1 = len(args)
        if _1 == 1:
            previousItemId, = _0
            if previousItemId is not None and not self.containsId(previousItemId):
                return None
            # Adds the item to container
            id = self._container.addItem()
            # Puts the new item to its correct place
            if not self._ordered and id is not None:
                self.addToOrderWrapper(id, previousItemId)
            return id
        elif _1 == 2:
            previousItemId, newItemId = _0
            if previousItemId is not None and not self.containsId(previousItemId):
                return None
            # Adds the item to container
            item = self._container.addItem(newItemId)
            # Puts the new item to its correct place
            if not self._ordered and item is not None:
                self.addToOrderWrapper(newItemId, previousItemId)
            return item
        else:
            raise ARGERROR(1, 2)

    # If the previous item is not in the container, fail

    def PiggybackListener(ContainerOrderedWrapper_this, *args, **kwargs):

        class PiggybackListener(Container.PropertySetChangeListener, Container.ItemSetChangeListener):
            """This listener 'piggybacks' on the real listener in order to update the
            wrapper when needed. It proxies equals() and hashCode() to the real
            listener so that the correct listener gets removed.
            """
            _listener = None

            def __init__(self, realListener):
                self._listener = realListener

            def containerItemSetChange(self, event):
                ContainerOrderedWrapper_this.updateOrderWrapper()
                self._listener.containerItemSetChange(event)

            def containerPropertySetChange(self, event):
                ContainerOrderedWrapper_this.updateOrderWrapper()
                self._listener.containerPropertySetChange(event)

            def equals(self, obj):
                return (obj == self._listener) or (obj is not None and obj == self._listener)

            def hashCode(self):
                return self._listener.hashCode()

        return PiggybackListener(*args, **kwargs)
