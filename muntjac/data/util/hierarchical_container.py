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

"""A specialized container whose contents can be accessed like it was a
tree-like structure."""

from muntjac.data.container import IContainer, IHierarchical
from muntjac.data.util.indexed_container import IndexedContainer
from muntjac.data.util.abstract_container import AbstractContainer


class HierarchicalContainer(IndexedContainer, IHierarchical, IContainer):
    """A specialized Container whose contents can be accessed like it was a
    tree-like structure.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    """

    def __init__(self):
        super(HierarchicalContainer, self).__init__()

        #: Set of IDs of those contained Items that can't have children.
        self._noChildrenAllowed = set()

        #: Mapping from Item ID to parent Item ID.
        self._parent = dict()

        #: Mapping from Item ID to parent Item ID for items included in
        #  the filtered container.
        self._filteredParent = None

        #: Mapping from Item ID to a list of child IDs.
        self._children = dict()

        #: Mapping from Item ID to a list of child IDs when filtered
        self._filteredChildren = None

        #: List that contains all root elements of the container.
        self._roots = list()

        #: List that contains all filtered root elements of the container.
        self._filteredRoots = None

        #: Determines how filtering of the container is done.
        self._includeParentsWhenFiltering = True

        self._contentChangedEventsDisabled = False

        self._contentsChangedEventPending = None

        self._filterOverride = None


    def areChildrenAllowed(self, itemId):
        # Can the specified Item have any children?
        if itemId in self._noChildrenAllowed:
            return False

        return self.containsId(itemId)


    def getChildren(self, itemId):
        # Gets the IDs of the children of the specified Item.
        if self._filteredChildren is not None:
            c = self._filteredChildren.get(itemId)
        else:
            c = self._children.get(itemId)

        if c is None:
            return None

        return list(c)


    def getParent(self, itemId):
        # Gets the ID of the parent of the specified Item.
        if self._filteredParent is not None:
            return self._filteredParent.get(itemId)

        return self._parent.get(itemId)


    def hasChildren(self, itemId):
        # Is the Item corresponding to the given ID a leaf node?
        if self._filteredChildren is not None:
            return itemId in self._filteredChildren
        else:
            return itemId in self._children


    def isRoot(self, itemId):
        # Is the Item corresponding to the given ID a root node?

        # If the container is filtered the itemId must be among filteredRoots
        # to be a root.
        if self._filteredRoots is not None:
            if itemId not in self._filteredRoots:
                return False
        elif itemId in self._parent:
            return False

        # Container is not filtered
        return self.containsId(itemId)


    def rootItemIds(self):
        # Gets the IDs of the root elements in the container.
        if self._filteredRoots is not None:
            return list(self._filteredRoots)
        else:
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
        # Checks that the item is in the container
        if not self.containsId(itemId):
            return False

        # Updates status
        if childrenAllowed:
            if itemId in self._noChildrenAllowed:
                self._noChildrenAllowed.remove(itemId)
        else:
            self._noChildrenAllowed.add(itemId)

        return True


    def setParent(self, itemId, newParentId):
        """Sets the parent of an Item. The new parent item must exist and be
        able to have children. (C{canHaveChildren(newParentId) == True}). It
        is also possible to detach a node from the hierarchy (and thus make
        it root) by setting the parent C{None}.

        @param itemId:
                   the ID of the item to be set as the child of the Item
                   identified with newParentId.
        @param newParentId:
                   the ID of the Item that's to be the new parent of the Item
                   identified with itemId.
        @return: C{True} if the operation succeeded, C{False} if not
        """
        # Checks that the item is in the container
        if not self.containsId(itemId):
            return False

        # Gets the old parent
        oldParentId = self._parent.get(itemId)

        # Checks if no change is necessary
        if ((newParentId is None and oldParentId is None)
                or (newParentId is not None)
                and (newParentId == oldParentId)):
            return True

        # Making root?
        if newParentId is None:
            # The itemId should become a root so we need to
            # - Remove it from the old parent's children list
            # - Add it as a root
            # - Remove it from the item -> parent list (parent is null for
            # roots)

            # Removes from old parents children list
            l = self._children.get(oldParentId)
            if l is not None:
                l.remove(itemId)
                if len(l) == 0:
                    del self._children[oldParentId]

            # Add to be a root
            self._roots.append(itemId)

            # Updates parent
            del self._parent[itemId]

            if self.hasFilters():
                # Refilter the container if setParent is called when filters
                # are applied. Changing parent can change what is included in
                # the filtered version (if includeParentsWhenFiltering==true).
                self.doFilterContainer(self.hasFilters())

            self.fireItemSetChange()

            return True

        # We get here when the item should not become a root and we need to
        # - Verify the new parent exists and can have children
        # - Check that the new parent is not a child of the selected itemId
        # - Updated the item -> parent mapping to point to the new parent
        # - Remove the item from the roots list if it was a root
        # - Remove the item from the old parent's children list if it was not a
        # root

        # Checks that the new parent exists in container and can have
        # children
        if ((not self.containsId(newParentId))
                or (newParentId in self._noChildrenAllowed)):
            return False

        # Checks that setting parent doesn't result to a loop
        o = newParentId
        while (o is not None) and (o != itemId):
            o = self._parent.get(o)

        if o is not None:
            return False

        # Updates parent
        self._parent[itemId] = newParentId
        pcl = self._children.get(newParentId)
        if pcl is None:
            # Create an empty list for holding children if one were not
            # previously created
            pcl = list()
            self._children[newParentId] = pcl
        pcl.append(itemId)

        # Removes from old parent or root
        if oldParentId is None:
            self._roots.remove(itemId)
        else:
            l = self._children.get(oldParentId)
            if l is not None:
                l.remove(itemId)
                if len(l) == 0:
                    del self._children[oldParentId]

        if self.hasFilters():
            # Refilter the container if setParent is called when filters
            # are applied. Changing parent can change what is included in
            # the filtered version (if includeParentsWhenFiltering==true).
            self.doFilterContainer(self.hasFilters())

        self.fireItemSetChange()

        return True


    def hasFilters(self):
        return self._filteredRoots is not None


    def moveAfterSibling(self, itemId, siblingId):
        """Moves a node (an Item) in the container immediately after a sibling
        node. The two nodes must have the same parent in the container.

        @param itemId:
                   the identifier of the moved node (Item)
        @param siblingId:
                   the identifier of the reference node (Item), after which the
                   other node will be located
        """
        parent2 = self.getParent(itemId)
        if parent2 is None:
            childrenList = self._roots
        else:
            childrenList = self._children.get(parent2)

        if siblingId is None:
            childrenList.remove(itemId)
            childrenList.insert(0, itemId)

        else:
            oldIndex = childrenList.index(itemId)
            indexOfSibling = childrenList.index(siblingId)
            if (indexOfSibling != -1) and (oldIndex != -1):
                if oldIndex > indexOfSibling:
                    newIndex = indexOfSibling + 1
                else:
                    newIndex = indexOfSibling

                del childrenList[oldIndex]
                childrenList.insert(newIndex, itemId)
            else:
                raise ValueError('Given identifiers do not have the '
                        'same parent.')

        self.fireItemSetChange()


    def addItem(self, itemId=None):
        if itemId is None:
            self.disableContentsChangeEvents()
            itemId = super(HierarchicalContainer, self).addItem()
            if itemId is None:
                return None
            if itemId not in self._roots:
                self._roots.append(itemId)
                if self._filteredRoots is not None:
                    if self.passesFilters(itemId):
                        self._filteredRoots.append(itemId)
            self.enableAndFireContentsChangeEvents()
            return itemId
        else:
            self.disableContentsChangeEvents()
            item = super(HierarchicalContainer, self).addItem(itemId)
            if item is None:
                return None
            self._roots.append(itemId)
            if self._filteredRoots is not None:
                if self.passesFilters(itemId):
                    self._filteredRoots.append(itemId)
            self.enableAndFireContentsChangeEvents()
            return item


    def fireItemSetChange(self, event=None):
        if event is not None:
            if self.contentsChangeEventsOn():
                super(HierarchicalContainer, self).fireItemSetChange(event)
            else:
                self._contentsChangedEventPending = True
        else:
            super(HierarchicalContainer, self).fireItemSetChange()


    def contentsChangeEventsOn(self):
        return not self._contentChangedEventsDisabled


    def disableContentsChangeEvents(self):
        self._contentChangedEventsDisabled = True


    def enableAndFireContentsChangeEvents(self):
        self._contentChangedEventsDisabled = False
        if self._contentsChangedEventPending:
            self.fireItemSetChange()
        self._contentsChangedEventPending = False


    def removeAllItems(self):
        self.disableContentsChangeEvents()
        success = super(HierarchicalContainer, self).removeAllItems()

        if success:
            del self._roots[:]
            self._parent.clear()
            self._children.clear()
            self._noChildrenAllowed.clear()
            if self._filteredRoots is not None:
                self._filteredRoots = None

            if self._filteredChildren is not None:
                self._filteredChildren = None

            if self._filteredParent is not None:
                self._filteredParent = None

        self.enableAndFireContentsChangeEvents()

        return success


    def removeItem(self, itemId):
        self.disableContentsChangeEvents()
        success = super(HierarchicalContainer, self).removeItem(itemId)

        if success:
            # Remove from roots if this was a root
            if itemId in self._roots:
                self._roots.remove(itemId)

                # If filtering is enabled we might need to remove it from the
                # filtered list also
                if self._filteredRoots is not None:
                    self._filteredRoots.remove(itemId)

            # Clear the children list. Old children will now become root nodes
            childNodeIds = self._children.pop(itemId, None)
            if childNodeIds is not None:
                if self._filteredChildren is not None:
                    del self._filteredChildren[itemId]

                for childId in childNodeIds:
                    self.setParent(childId, None)

            # Parent of the item that we are removing will contain the item id
            # in its children list
            parentItemId = self._parent.get(itemId)
            if parentItemId is not None:
                c = self._children.get(parentItemId)
                if c is not None:
                    c.remove(itemId)
                    if len(c) == 0:
                        del self._children[parentItemId]

                    # Found in the children list so might also be in the
                    # filteredChildren list
                    if self._filteredChildren is not None:
                        f = self._filteredChildren.get(parentItemId)
                        if f is not None:
                            f.remove(itemId)
                            if len(f) == 0:
                                del self._filteredChildren[parentItemId]

            if itemId in self._parent:
                del self._parent[itemId]

            if self._filteredParent is not None:
                # Item id no longer has a parent as the item id is not in the
                # container.
                del self._filteredParent[itemId]

            if itemId in self._noChildrenAllowed:
                self._noChildrenAllowed.remove(itemId)

        self.enableAndFireContentsChangeEvents()

        return success


    def removeItemRecursively(self, *args):
        """Removes the Item identified by given itemId and all its children
        from the given Container.

        @see: L{removeItem}
        @param args: tuple of the form
                - (itemId)
                  - the identifier of the Item to be removed
                - (container, itemId)
                  - the container where the item is to be removed
                  - the identifier of the Item to be removed
        @return: true if the operation succeeded
        """
        nargs = len(args)
        if nargs == 1:
            itemId, = args
            self.disableContentsChangeEvents()
            removeItemRecursively = self.removeItemRecursively(self, itemId)
            self.enableAndFireContentsChangeEvents()
            return removeItemRecursively
        elif nargs == 2:
            container, itemId = args
            success = True
            children2 = container.getChildren(itemId)
            if children2 is not None:
                arry = list(children2)
                for i in range(len(arry)):
                    removeItemRecursively = self.removeItemRecursively(
                            container, arry[i])
                    if not removeItemRecursively:
                        success = False

            # remove the root of subtree if children where succesfully removed
            if success:
                success = container.removeItem(itemId)

            return success


    def doSort(self):
        super(HierarchicalContainer, self).doSort()
        self._roots.sort(cmp=self.getItemSorter())
        for childList in self._children.values():
            childList.sort(cmp=self.getItemSorter())


    def isIncludeParentsWhenFiltering(self):
        """Used to control how filtering works. @see
        L{setIncludeParentsWhenFiltering} for more information.

        @return: true if all parents for items that match the filter are
                included when filtering, false if only the matching items
                are included
        """
        return self._includeParentsWhenFiltering


    def setIncludeParentsWhenFiltering(self, includeParentsWhenFiltering):
        """Controls how the filtering of the container works. Set this to true
        to make filtering include parents for all matched items in addition to
        the items themselves. Setting this to false causes the filtering to
        only include the matching items and make items with excluded parents
        into root items.

        @param includeParentsWhenFiltering:
                   true to include all parents for items that match the filter,
                   false to only include the matching items
        """
        self._includeParentsWhenFiltering = includeParentsWhenFiltering
        if self._filteredRoots is not None:
            # Currently filtered so needs to be re-filtered
            self.doFilterContainer(True)


    def doFilterContainer(self, hasFilters):
        if not hasFilters:
            # All filters removed
            self._filteredRoots = None
            self._filteredChildren = None
            self._filteredParent = None

            return super(HierarchicalContainer,
                    self).doFilterContainer(hasFilters)

        # Reset data structures
        self._filteredRoots = list()
        self._filteredChildren = dict()
        self._filteredParent = dict()

        if self._includeParentsWhenFiltering:
            # Filter so that parents for items that match the filter are also
            # included
            includedItems = set()
            for rootId in self._roots:
                if self.filterIncludingParents(rootId, includedItems):
                    self._filteredRoots.append(rootId)
                    self.addFilteredChildrenRecursively(rootId, includedItems)

            # includedItemIds now contains all the item ids that should be
            # included. Filter IndexedContainer based on this
            self._filterOverride = includedItems
            super(HierarchicalContainer, self).doFilterContainer(hasFilters)
            self._filterOverride = None

            return True
        else:
            # Filter by including all items that pass the filter and make items
            # with no parent new root items

            # Filter IndexedContainer first so getItemIds return the items that
            # match
            super(HierarchicalContainer, self).doFilterContainer(hasFilters)

            filteredItemIds = set(self.getItemIds())
            for itemId in filteredItemIds:
                itemParent = self._parent.get(itemId)
                if (itemParent is None or itemParent not in filteredItemIds):
                    # Parent is not included or this was a root, in both cases
                    # this should be a filtered root
                    self._filteredRoots.append(itemId)
                else:
                    # Parent is included. Add this to the children list (create
                    # it first if necessary)
                    self.addFilteredChild(itemParent, itemId)

            return True


    def addFilteredChild(self, parentItemId, childItemId):
        """Adds the given childItemId as a filteredChildren for the
        parentItemId and sets it filteredParent.
        """
        parentToChildrenList = self._filteredChildren.get(parentItemId)
        if parentToChildrenList is None:
            parentToChildrenList = list()
            self._filteredChildren[parentItemId] = parentToChildrenList
        self._filteredParent[childItemId] = parentItemId
        parentToChildrenList.append(childItemId)


    def addFilteredChildrenRecursively(self, parentItemId, includedItems):
        """Recursively adds all items in the includedItems list to the
        filteredChildren map in the same order as they are in the children map.
        Starts from parentItemId and recurses down as long as child items that
        should be included are found.

        @param parentItemId:
                   The item id to start recurse from. Not added to a
                   filteredChildren list
        @param includedItems:
                   Set containing the item ids for the items that should be
                   included in the filteredChildren map
        """
        childList = self._children.get(parentItemId)
        if childList is None:
            return

        for childItemId in childList:
            if childItemId in includedItems:
                self.addFilteredChild(parentItemId, childItemId)
                self.addFilteredChildrenRecursively(childItemId, includedItems)


    def filterIncludingParents(self, itemId, includedItems):
        """Scans the itemId and all its children for which items should be
        included when filtering. All items which passes the filters are
        included. Additionally all items that have a child node that should be
        included are also themselves included.

        @return: true if the itemId should be included in the filtered
                container.
        """
        toBeIncluded = self.passesFilters(itemId)

        childList = self._children.get(itemId)
        if childList is not None:
            for childItemId in self._children.get(itemId):
                toBeIncluded = toBeIncluded | self.filterIncludingParents(
                        childItemId, includedItems)
        if toBeIncluded:
            includedItems.add(itemId)

        return toBeIncluded


    def passesFilters(self, itemId):
        if self._filterOverride is not None:
            return itemId in self._filterOverride
        else:
            return super(HierarchicalContainer, self).passesFilters(itemId)
