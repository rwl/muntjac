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

"""A wrapper class for adding external hierarchy to containers not
implementing the IHierarchical interface."""

from muntjac.data.container import \
    (IContainer, IHierarchical, IItemSetChangeListener, IItemSetChangeNotifier,
     IPropertySetChangeListener, IPropertySetChangeNotifier,
     IItemSetChangeEvent, IPropertySetChangeEvent)

from muntjac.data.util.hierarchical_container import HierarchicalContainer


class ContainerHierarchicalWrapper(IHierarchical, IContainer,
            IItemSetChangeNotifier, IPropertySetChangeNotifier):
    """A wrapper class for adding external hierarchy to containers not
    implementing the L{IHierarchical} interface.

    If the wrapped container is changed directly (that is, not through the
    wrapper), and does not implement IItemSetChangeNotifier and/or
    IPropertySetChangeNotifier the hierarchy information must be updated
    with the L{updateHierarchicalWrapper} method.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    """

    def __init__(self, toBeWrapped):
        """Constructs a new hierarchical wrapper for an existing Container.
        Works even if the to-be-wrapped container already implements the
        C{IHierarchical} interface.

        @param toBeWrapped:
                   the container that needs to be accessed hierarchically
        @see: L{updateHierarchicalWrapper}
        """
        super(ContainerHierarchicalWrapper, self).__init__()

        #: The wrapped container
        self._container = None

        #: Set of IDs of those contained Items that can't have children.
        self._noChildrenAllowed = None

        #: Mapping from Item ID to parent Item ID
        self._parent = None

        #: Mapping from Item ID to a list of child IDs
        self._children = None

        #: List that contains all root elements of the container.
        self._roots = None

        #: Is the wrapped container hierarchical by itself ?
        self._hierarchical = None

        self._container = toBeWrapped
        self._hierarchical = isinstance(self._container, IHierarchical)

        # Check arguments
        if self._container is None:
            raise ValueError, 'Null can not be wrapped'

        # Create initial order if needed
        if not self._hierarchical:
            self._noChildrenAllowed = set()
            self._parent = dict()
            self._children = dict()
            self._roots = set(self._container.getItemIds())

        self.updateHierarchicalWrapper()


    def updateHierarchicalWrapper(self):
        """Updates the wrapper's internal hierarchy data to include all Items
        in the underlying container. If the contents of the wrapped container
        change without the wrapper's knowledge, this method needs to be called
        to update the hierarchy information of the Items.
        """
        if not self._hierarchical:

            # Recreate hierarchy and data structures if missing
            if (self._noChildrenAllowed is None or self._parent is None
                    or self._children is None or self._roots is None):
                # Check that the hierarchy is up-to-date
                self._noChildrenAllowed = set()
                self._parent = dict()
                self._children = dict()
                self._roots = set(self._container.getItemIds())

            else:

                # ensure order of root and child lists is same as in wrapped
                # container
                itemIds = self._container.getItemIds()
                basedOnOrderFromWrappedContainer = \
                        ListedItemsFirstComparator(itemIds)

                # Calculate the set of all items in the hierarchy
                s = set()
                s = s.union(self._parent.keys())
                s = s.union(self._children.keys())
                s = s.union(self._roots)

                # Remove unnecessary items
                for idd in s:
                    if not self._container.containsId(idd):
                        self.removeFromHierarchyWrapper(idd)

                # Add all the missing items
                ids = self._container.getItemIds()
                for idd in ids:
                    if not (idd in s):
                        self.addToHierarchyWrapper(idd)
                        s.add(idd)

                arry = list(self._roots)
                arry.sort(cmp=basedOnOrderFromWrappedContainer)
                self._roots = set()
                for a in arry:
                    self._roots.add(a)

                for obj in self._children.keys():
                    object2 = self._children[obj]
                    object2.sort(cmp=basedOnOrderFromWrappedContainer)


    def removeFromHierarchyWrapper(self, itemId):
        """Removes the specified Item from the wrapper's internal hierarchy
        structure.

        Note : The Item is not removed from the underlying Container.

        @param itemId:
                   the ID of the item to remove from the hierarchy.
        """
        oprhanedChildren = self._children.pop(itemId, None)
        if oprhanedChildren is not None:
            for obj in oprhanedChildren:
                # make orphaned children root nodes
                self.setParent(obj, None)

        if itemId in self._roots:
            self._roots.remove(itemId)

        p = self._parent.get(itemId)
        if p is not None:
            c = self._children.get(p)
            if c is not None:
                c.remove(itemId)

        if itemId in self._parent:
            del self._parent[itemId]

        if itemId in self._noChildrenAllowed:
            self._noChildrenAllowed.remove(itemId)


    def addToHierarchyWrapper(self, itemId):
        """Adds the specified Item specified to the internal hierarchy
        structure. The new item is added as a root Item. The underlying
        container is not modified.

        @param itemId:
                   the ID of the item to add to the hierarchy.
        """
        self._roots.add(itemId)


    def areChildrenAllowed(self, itemId):
        # Can the specified Item have any children?

        # If the wrapped container implements the method directly, use it
        if self._hierarchical:
            return self._container.areChildrenAllowed(itemId)

        if itemId in self._noChildrenAllowed:
            return False

        return self.containsId(itemId)


    def getChildren(self, itemId):
        # Gets the IDs of the children of the specified Item.

        # If the wrapped container implements the method directly, use it
        if self._hierarchical:
            return self._container.getChildren(itemId)

        c = self._children.get(itemId)
        if c is None:
            return None

        return list(c)


    def getParent(self, itemId):
        # Gets the ID of the parent of the specified Item.

        # If the wrapped container implements the method directly, use it
        if self._hierarchical:
            return self._container.getParent(itemId)

        return self._parent.get(itemId)


    def hasChildren(self, itemId):
        # Is the Item corresponding to the given ID a leaf node?

        # If the wrapped container implements the method directly, use it
        if self._hierarchical:
            return self._container.hasChildren(itemId)

        return self._children.get(itemId) is not None


    def isRoot(self, itemId):
        # Is the Item corresponding to the given ID a root node?

        # If the wrapped container implements the method directly, use it
        if self._hierarchical:
            return self._container.isRoot(itemId)

        if itemId in self._parent:
            return False

        return self.containsId(itemId)


    def rootItemIds(self):
        # Gets the IDs of the root elements in the container.

        # If the wrapped container implements the method directly, use it
        if self._hierarchical:
            return self._container.rootItemIds()

        return list(self._roots)


    def setChildrenAllowed(self, itemId, childrenAllowed):
        """Sets the given Item's capability to have children. If the Item
        identified with the itemId already has children and the
        areChildrenAllowed is false this method fails and C{False}
        is returned; the children must be first explicitly removed with
        L{setParent} or L{IContainer.removeItem}.

        @param itemId:
                   the ID of the Item in the container whose child capability
                   is to be set.
        @param childrenAllowed:
                   the boolean value specifying if the Item can have children
                   or not.
        @return: C{True} if the operation succeeded, C{False} if not
        """
        # If the wrapped container implements the method directly, use it
        if self._hierarchical:
            return self._container.setChildrenAllowed(itemId, childrenAllowed)

        # Check that the item is in the container
        if not self.containsId(itemId):
            return False

        # Update status
        if childrenAllowed:
            if itemId in self._noChildrenAllowed:
                self._noChildrenAllowed.remove(itemId)
        else:
            self._noChildrenAllowed.add(itemId)

        return True


    def setParent(self, itemId, newParentId):
        """Sets the parent of an Item. The new parent item must exist and be
        able to have children.
        (C{canHaveChildren(newParentId) == True}). It is also
        possible to detach a node from the hierarchy (and thus make it root)
        by setting the parent C{None}.

        @param itemId:
                   the ID of the item to be set as the child of the Item
                   identified with newParentId.
        @param newParentId:
                   the ID of the Item that's to be the new parent of the Item
                   identified with itemId.
        @return: C{True} if the operation succeeded, C{False} if not
        """
        # If the wrapped container implements the method directly, use it
        if self._hierarchical:
            return self._container.setParent(itemId, newParentId)

        # Check that the item is in the container
        if not self.containsId(itemId):
            return False

        # Get the old parent
        oldParentId = self._parent.get(itemId)

        # Check if no change is necessary
        if ((newParentId is None and oldParentId is None)
                or (newParentId is not None and newParentId == oldParentId)):
            return True

        # Making root
        if newParentId is None:

            # Remove from old parents children list
            l = self._children.get(oldParentId)
            if l is not None:
                l.remove(itemId)
                if len(l) == 0:
                    del self._children[itemId]

            # Add to be a root
            self._roots.add(itemId)

            # Update parent
            self._parent.remove(itemId)

            return True

        # Check that the new parent exists in container and can have
        # children
        if ((not self.containsId(newParentId))
                or (newParentId in self._noChildrenAllowed)):
            return False

        # Check that setting parent doesn't result to a loop
        o = newParentId
        while o is not None and not (o == itemId):
            o = self._parent.get(o)

        if o is not None:
            return False

        # Update parent
        self._parent[itemId] = newParentId
        pcl = self._children.get(newParentId)
        if pcl is None:
            pcl = list()
            self._children[newParentId] = pcl
        pcl.append(itemId)

        # Remove from old parent or root
        if oldParentId is None:
            self._roots.remove(itemId)
        else:
            l = self._children.get(oldParentId)
            if l is not None:
                l.remove(itemId)
                if len(l) == 0:
                    self._children.remove(oldParentId)

        return True


    def addItem(self, itemId=None):
        """Adds a new Item by its ID to the underlying container and to the
        hierarchy. Creates a new Item into the Container, assigns it an
        automatic ID, and adds it to the hierarchy if C{itemId} is C{None}.

        @param itemId:
                   the ID of the Item to be created.
        @return: the added Item or C{None} if the operation failed.
        @raise NotImplementedError:
                    if the addItem is not supported.
        """
        if itemId is None:
            idd = self._container.addItem()
            if not self._hierarchical and idd is not None:
                self.addToHierarchyWrapper(idd)
            return idd
        else:
            item = self._container.addItem(itemId)
            if not self._hierarchical and item is not None:
                self.addToHierarchyWrapper(itemId)
            return item


    def removeAllItems(self):
        """Removes all items from the underlying container and from the
        hierarchy.

        @return: C{True} if the operation succeeded, C{False} if not
        @raise NotImplementedError:
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
        """Removes an Item specified by the itemId from the underlying
        container and from the hierarchy.

        @param itemId:
                   the ID of the Item to be removed.
        @return: C{True} if the operation succeeded, C{False} if not
        @raise NotImplementedError:
                    if the removeItem is not supported.
        """
        success = self._container.removeItem(itemId)

        if not self._hierarchical and success:
            self.removeFromHierarchyWrapper(itemId)

        return success


    def removeItemRecursively(self, itemId):
        """Removes the Item identified by given itemId and all its children.

        @see: L{removeItem}
        @param itemId:
                   the identifier of the Item to be removed
        @return: true if the operation succeeded
        """
        dummy = HierarchicalContainer()
        return HierarchicalContainer.removeItemRecursively(dummy, self, itemId)


    def addContainerProperty(self, propertyId, typ, defaultValue):
        """Adds a new Property to all Items in the Container.

        @param propertyId:
                   the ID of the new Property.
        @param typ:
                   the Data type of the new Property.
        @param defaultValue:
                   the value all created Properties are initialized to.
        @return: C{True} if the operation succeeded, C{False} if not
        @raise NotImplementedError:
                    if the addContainerProperty is not supported.
        """
        return self._container.addContainerProperty(propertyId, typ,
                defaultValue)


    def removeContainerProperty(self, propertyId):
        """Removes the specified Property from the underlying container and
        from the hierarchy.

        Note: The Property will be removed from all Items in the Container.

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
        # from the Container
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
        return len(self._container)


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
            super(ContainerHierarchicalWrapper, self).addCallback(callback,
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
            super(ContainerHierarchicalWrapper, self).removeCallback(callback,
                    eventType)


class PiggybackListener(IContainer, IPropertySetChangeListener,
            IItemSetChangeListener):
    """This listener 'piggybacks' on the real listener in order to update the
    wrapper when needed. It proxies equals() and hashCode() to the real
    listener so that the correct listener gets removed.
    """

    def __init__(self, realListener, wrapper, *args):
        self._listener = realListener
        self._wrapper = wrapper
        self._args = args


    def containerItemSetChange(self, event):
        self._wrapper.updateHierarchicalWrapper()
        if isinstance(self._listener, IItemSetChangeListener):
            self._listener.containerItemSetChange(event)
        else:
            self._listener(event, *self._args)


    def containerPropertySetChange(self, event):
        self._wrapper.updateHierarchicalWrapper()
        if isinstance(self._listener, IPropertySetChangeListener):
            self._listener.containerPropertySetChange(event)
        else:
            self._listener(event, *self._args)


    def __eq__(self, obj):
        return (obj is not None and obj == self._listener)


    def __hash__(self):
        return hash(self._listener)


class ListedItemsFirstComparator(object):
    """A comparator that sorts the listed items before other items.
    Otherwise, the order is undefined.
    """

    def __init__(self, itemIds):
        self._itemIds = itemIds


    def __call__(self, o1, o2):
        return self.compare(o1, o2)


    def compare(self, o1, o2):
        if o1 == o2:
            return 0
        for idd in self._itemIds:
            if idd == o1:
                return -1
            elif idd == o2:
                return 1
        return 0
