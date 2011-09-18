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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.data.Container import (Container, Hierarchical, ItemSetChangeListener, ItemSetChangeNotifier, PropertySetChangeListener, PropertySetChangeNotifier,)
from com.vaadin.data.util.HierarchicalContainer import (HierarchicalContainer,)
# from java.io.Serializable import (Serializable,)
# from java.util.HashSet import (HashSet,)
# from java.util.LinkedHashSet import (LinkedHashSet,)


class ContainerHierarchicalWrapper(Container, Hierarchical, Container, ItemSetChangeNotifier, Container, PropertySetChangeNotifier):
    """<p>
    A wrapper class for adding external hierarchy to containers not implementing
    the {@link com.vaadin.data.Container.Hierarchical} interface.
    </p>

    <p>
    If the wrapped container is changed directly (that is, not through the
    wrapper), and does not implement Container.ItemSetChangeNotifier and/or
    Container.PropertySetChangeNotifier the hierarchy information must be updated
    with the {@link #updateHierarchicalWrapper()} method.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # The wrapped container
    _container = None
    # Set of IDs of those contained Items that can't have children.
    _noChildrenAllowed = None
    # Mapping from Item ID to parent Item ID
    _parent = None
    # Mapping from Item ID to a list of child IDs
    _children = None
    # List that contains all root elements of the container.
    _roots = None
    # Is the wrapped container hierarchical by itself ?
    _hierarchical = None

    class ListedItemsFirstComparator(Comparator, Serializable):
        """A comparator that sorts the listed items before other items. Otherwise,
        the order is undefined.
        """
        _itemIds = None

        def __init__(self, itemIds):
            self._itemIds = itemIds

        def compare(self, o1, o2):
            if o1 == o2:
                return 0
            for id in self._itemIds:
                if id == o1:
                    return -1
                elif id == o2:
                    return 1
            return 0

    def __init__(self, toBeWrapped):
        """Constructs a new hierarchical wrapper for an existing Container. Works
        even if the to-be-wrapped container already implements the
        <code>Container.Hierarchical</code> interface.

        @param toBeWrapped
                   the container that needs to be accessed hierarchically
        @see #updateHierarchicalWrapper()
        """
        self._container = toBeWrapped
        self._hierarchical = isinstance(self._container, Container.Hierarchical)
        # Check arguments
        if self._container is None:
            raise self.NullPointerException('Null can not be wrapped')
        # Create initial order if needed
        if not self._hierarchical:
            self._noChildrenAllowed = set()
            self._parent = dict()
            self._children = dict()
            self._roots = LinkedHashSet(self._container.getItemIds())
        self.updateHierarchicalWrapper()

    def updateHierarchicalWrapper(self):
        """Updates the wrapper's internal hierarchy data to include all Items in the
        underlying container. If the contents of the wrapped container change
        without the wrapper's knowledge, this method needs to be called to update
        the hierarchy information of the Items.
        """
        if not self._hierarchical:
            # Recreate hierarchy and data structures if missing
            if (
                (((self._noChildrenAllowed is None) or (self._parent is None)) or (self._children is None)) or (self._roots is None)
            ):
                # Check that the hierarchy is up-to-date
                self._noChildrenAllowed = set()
                self._parent = dict()
                self._children = dict()
                self._roots = LinkedHashSet(self._container.getItemIds())
            else:
                # ensure order of root and child lists is same as in wrapped
                # container
                itemIds = self._container.getItemIds()
                basedOnOrderFromWrappedContainer = self.ListedItemsFirstComparator(itemIds)
                # Calculate the set of all items in the hierarchy
                s = set()
                s.addAll(self._parent.keys())
                s.addAll(self._children.keys())
                s.addAll(self._roots)
                # Remove unnecessary items
                _0 = True
                i = s
                while True:
                    if _0 is True:
                        _0 = False
                    if not i.hasNext():
                        break
                    id = i.next()
                    if not self._container.containsId(id):
                        self.removeFromHierarchyWrapper(id)
                # Add all the missing items
                ids = self._container.getItemIds()
                _1 = True
                i = ids
                while True:
                    if _1 is True:
                        _1 = False
                    if not i.hasNext():
                        break
                    id = i.next()
                    if not (id in s):
                        self.addToHierarchyWrapper(id)
                        s.add(id)
                array = list(self._roots)
                self.Arrays.sort(array, basedOnOrderFromWrappedContainer)
                self._roots = LinkedHashSet()
                _2 = True
                i = 0
                while True:
                    if _2 is True:
                        _2 = False
                    else:
                        i += 1
                    if not (i < len(array)):
                        break
                    self._roots.add(array[i])
                for object in self._children.keys():
                    object2 = self._children[object]
                    Collections.sort(object2, basedOnOrderFromWrappedContainer)

    def removeFromHierarchyWrapper(self, itemId):
        """Removes the specified Item from the wrapper's internal hierarchy
        structure.
        <p>
        Note : The Item is not removed from the underlying Container.
        </p>

        @param itemId
                   the ID of the item to remove from the hierarchy.
        """
        oprhanedChildren = self._children.remove(itemId)
        if oprhanedChildren is not None:
            for object in oprhanedChildren:
                # make orphaned children root nodes
                self.setParent(object, None)
        self._roots.remove(itemId)
        p = self._parent[itemId]
        if p is not None:
            c = self._children[p]
            if c is not None:
                c.remove(itemId)
        self._parent.remove(itemId)
        self._noChildrenAllowed.remove(itemId)

    def addToHierarchyWrapper(self, itemId):
        """Adds the specified Item specified to the internal hierarchy structure.
        The new item is added as a root Item. The underlying container is not
        modified.

        @param itemId
                   the ID of the item to add to the hierarchy.
        """
        # Can the specified Item have any children? Don't add a JavaDoc comment
        # here, we use the default documentation from implemented interface.

        self._roots.add(itemId)

    def areChildrenAllowed(self, itemId):
        # If the wrapped container implements the method directly, use it
        # Gets the IDs of the children of the specified Item. Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        if self._hierarchical:
            return self._container.areChildrenAllowed(itemId)
        if itemId in self._noChildrenAllowed:
            return False
        return self.containsId(itemId)

    def getChildren(self, itemId):
        # If the wrapped container implements the method directly, use it
        # Gets the ID of the parent of the specified Item. Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        if self._hierarchical:
            return self._container.getChildren(itemId)
        c = self._children[itemId]
        if c is None:
            return None
        return Collections.unmodifiableCollection(c)

    def getParent(self, itemId):
        # If the wrapped container implements the method directly, use it
        # Is the Item corresponding to the given ID a leaf node? Don't add a
        # JavaDoc comment here, we use the default documentation from implemented
        # interface.

        if self._hierarchical:
            return self._container.getParent(itemId)
        return self._parent[itemId]

    def hasChildren(self, itemId):
        # If the wrapped container implements the method directly, use it
        # Is the Item corresponding to the given ID a root node? Don't add a
        # JavaDoc comment here, we use the default documentation from implemented
        # interface.

        if self._hierarchical:
            return self._container.hasChildren(itemId)
        return self._children[itemId] is not None

    def isRoot(self, itemId):
        # If the wrapped container implements the method directly, use it
        # Gets the IDs of the root elements in the container. Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        if self._hierarchical:
            return self._container.isRoot(itemId)
        if itemId in self._parent:
            return False
        return self.containsId(itemId)

    def rootItemIds(self):
        # If the wrapped container implements the method directly, use it
        if self._hierarchical:
            return self._container.rootItemIds()
        return Collections.unmodifiableCollection(self._roots)

    def setChildrenAllowed(self, itemId, childrenAllowed):
        """<p>
        Sets the given Item's capability to have children. If the Item identified
        with the itemId already has children and the areChildrenAllowed is false
        this method fails and <code>false</code> is returned; the children must
        be first explicitly removed with
        {@link #setParent(Object itemId, Object newParentId)} or
        {@link com.vaadin.data.Container#removeItem(Object itemId)}.
        </p>

        @param itemId
                   the ID of the Item in the container whose child capability is
                   to be set.
        @param childrenAllowed
                   the boolean value specifying if the Item can have children or
                   not.
        @return <code>true</code> if the operation succeeded, <code>false</code>
                if not
        """
        # If the wrapped container implements the method directly, use it
        if self._hierarchical:
            return self._container.setChildrenAllowed(itemId, childrenAllowed)
        # Check that the item is in the container
        if not self.containsId(itemId):
            return False
        # Update status
        if childrenAllowed:
            self._noChildrenAllowed.remove(itemId)
        else:
            self._noChildrenAllowed.add(itemId)
        return True

    def setParent(self, itemId, newParentId):
        """<p>
        Sets the parent of an Item. The new parent item must exist and be able to
        have children. (<code>canHaveChildren(newParentId) == true</code>). It is
        also possible to detach a node from the hierarchy (and thus make it root)
        by setting the parent <code>null</code>.
        </p>

        @param itemId
                   the ID of the item to be set as the child of the Item
                   identified with newParentId.
        @param newParentId
                   the ID of the Item that's to be the new parent of the Item
                   identified with itemId.
        @return <code>true</code> if the operation succeeded, <code>false</code>
                if not
        """
        # If the wrapped container implements the method directly, use it
        if self._hierarchical:
            return self._container.setParent(itemId, newParentId)
        # Check that the item is in the container
        if not self.containsId(itemId):
            return False
        # Get the old parent
        oldParentId = self._parent[itemId]
        # Check if no change is necessary
        if (
            (newParentId is None and oldParentId is None) or (newParentId is not None and newParentId == oldParentId)
        ):
            return True
        # Making root
        if newParentId is None:
            # Remove from old parents children list
            l = self._children[oldParentId]
            if l is not None:
                l.remove(itemId)
                if l.isEmpty():
                    self._children.remove(itemId)
            # Add to be a root
            self._roots.add(itemId)
            # Update parent
            self._parent.remove(itemId)
            return True
        # Check that the new parent exists in container and can have
        # children
        if (
            (not self.containsId(newParentId)) or (newParentId in self._noChildrenAllowed)
        ):
            return False
        # Check that setting parent doesn't result to a loop
        o = newParentId
        while o is not None and not (o == itemId):
            o = self._parent[o]
        if o is not None:
            return False
        # Update parent
        self._parent.put(itemId, newParentId)
        pcl = self._children[newParentId]
        if pcl is None:
            pcl = LinkedList()
            self._children.put(newParentId, pcl)
        pcl.add(itemId)
        # Remove from old parent or root
        if oldParentId is None:
            self._roots.remove(itemId)
        else:
            l = self._children[oldParentId]
            if l is not None:
                l.remove(itemId)
                if l.isEmpty():
                    self._children.remove(oldParentId)
        return True

    def addItem(self, *args):
        """Creates a new Item into the Container, assigns it an automatic ID, and
        adds it to the hierarchy.

        @return the autogenerated ID of the new Item or <code>null</code> if the
                operation failed
        @throws UnsupportedOperationException
                    if the addItem is not supported.
        ---
        Adds a new Item by its ID to the underlying container and to the
        hierarchy.

        @param itemId
                   the ID of the Item to be created.
        @return the added Item or <code>null</code> if the operation failed.
        @throws UnsupportedOperationException
                    if the addItem is not supported.
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            id = self._container.addItem()
            if not self._hierarchical and id is not None:
                self.addToHierarchyWrapper(id)
            return id
        elif _1 == 1:
            itemId, = _0
            if itemId is None:
                raise self.NullPointerException('Container item id can not be null')
            item = self._container.addItem(itemId)
            if not self._hierarchical and item is not None:
                self.addToHierarchyWrapper(itemId)
            return item
        else:
            raise ARGERROR(0, 1)

    # Null ids are not accepted

    def removeAllItems(self):
        """Removes all items from the underlying container and from the hierarcy.

        @return <code>true</code> if the operation succeeded, <code>false</code>
                if not
        @throws UnsupportedOperationException
                    if the removeAllItems is not supported.
        """
        success = self._container.removeAllItems()
        if not self._hierarchical and success:
            self._roots.clear()
            self._parent.clear()
            self._children.clear()
            self._noChildrenAllowed.clear()
        return success

    def removeItem(self, itemId):
        """Removes an Item specified by the itemId from the underlying container and
        from the hierarchy.

        @param itemId
                   the ID of the Item to be removed.
        @return <code>true</code> if the operation succeeded, <code>false</code>
                if not
        @throws UnsupportedOperationException
                    if the removeItem is not supported.
        """
        success = self._container.removeItem(itemId)
        if not self._hierarchical and success:
            self.removeFromHierarchyWrapper(itemId)
        return success

    def removeItemRecursively(self, itemId):
        """Removes the Item identified by given itemId and all its children.

        @see #removeItem(Object)
        @param itemId
                   the identifier of the Item to be removed
        @return true if the operation succeeded
        """
        return HierarchicalContainer.removeItemRecursively(self, itemId)

    def addContainerProperty(self, propertyId, type, defaultValue):
        """Adds a new Property to all Items in the Container.

        @param propertyId
                   the ID of the new Property.
        @param type
                   the Data type of the new Property.
        @param defaultValue
                   the value all created Properties are initialized to.
        @return <code>true</code> if the operation succeeded, <code>false</code>
                if not
        @throws UnsupportedOperationException
                    if the addContainerProperty is not supported.
        """
        return self._container.addContainerProperty(propertyId, type, defaultValue)

    def removeContainerProperty(self, propertyId):
        """Removes the specified Property from the underlying container and from the
        hierarchy.
        <p>
        Note : The Property will be removed from all Items in the Container.
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

        return len(self._container)

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

    class PiggybackListener(Container, PropertySetChangeListener, Container, ItemSetChangeListener):
        """This listener 'piggybacks' on the real listener in order to update the
        wrapper when needed. It proxies equals() and hashCode() to the real
        listener so that the correct listener gets removed.
        """
        _listener = None

        def __init__(self, realListener):
            self._listener = realListener

        def containerItemSetChange(self, event):
            self.updateHierarchicalWrapper()
            self._listener.containerItemSetChange(event)

        def containerPropertySetChange(self, event):
            self.updateHierarchicalWrapper()
            self._listener.containerPropertySetChange(event)

        def equals(self, obj):
            return (obj == self._listener) or (obj is not None and obj == self._listener)

        def hashCode(self):
            return self._listener.hashCode()
