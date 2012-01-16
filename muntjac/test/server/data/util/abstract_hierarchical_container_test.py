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

import re

from muntjac.test.server.data.util.abstract_container_test import \
    AbstractContainerTest


class AbstractHierarchicalContainerTest(AbstractContainerTest):

    def validateHierarchicalContainer(self, container, expectedFirstItemId,
                expectedLastItemId, itemIdInSet, itemIdNotInSet,
                checkGetItemNull, expectedSize, expectedRootSize,
                rootsHaveChildren):
        """@param container:
                   The container to validate
        @param expectedFirstItemId:
                   Expected first item id
        @param expectedLastItemId:
                   Expected last item id
        @param itemIdInSet:
                   An item id that is in the container
        @param itemIdNotInSet:
                   An item id that is not in the container
        @param checkGetItemNull:
                   true if getItem() should return null for itemIdNotInSet,
                   false to skip the check (container.containsId() is checked
                   in any case)
        @param expectedSize:
                   Expected number of items in the container. Not related to
                   hierarchy.
        @param expectedTraversalSize:
                   Expected number of items found when traversing from the
                   roots down to all available nodes.
        @param expectedRootSize:
                   Expected number of root items
        @param rootsHaveChildren:
                   true if all roots have children, false otherwise (skips
                   some asserts)
        """
        self.validateContainer(container, expectedFirstItemId,
                expectedLastItemId, itemIdInSet, itemIdNotInSet,
                checkGetItemNull, expectedSize)

        # rootItemIds
        rootIds = container.rootItemIds()
        self.assertEquals(expectedRootSize, len(rootIds))

        for rootId in rootIds:
            # All roots must be in container
            self.assertTrue(container.containsId(rootId))

            # All roots must have no parent
            self.assertEquals(container.getParent(rootId), None)

            # all roots must be roots
            self.assertTrue(container.isRoot(rootId))

            if rootsHaveChildren:
                # all roots have children allowed in this case
                self.assertTrue(container.areChildrenAllowed(rootId))

                # all roots have children in this case
                children = container.getChildren(rootId)
                self.assertNotEquals(children, None,
                        rootId + ' should have children')
                self.assertTrue(len(children) > 0,
                        rootId + ' should have children')

                # getParent
                for childId in children:
                    self.assertEquals(container.getParent(childId), rootId)

        # isRoot should return false for unknown items
        self.assertFalse(container.isRoot(itemIdNotInSet))

        # hasChildren should return false for unknown items
        self.assertFalse(container.hasChildren(itemIdNotInSet))

        # areChildrenAllowed should return false for unknown items
        self.assertFalse(container.areChildrenAllowed(itemIdNotInSet))

        # removeItem of unknown items should return false
        self.assertFalse(container.removeItem(itemIdNotInSet))

        self.assertEquals(expectedSize, self.countNodes(container))

        self.validateHierarchy(container)


    def countNodes(self, container, itemId=None):
        if itemId is None:
            totalNodes = 0
            for rootId in container.rootItemIds():
                totalNodes += self.countNodes(container, rootId)
            return totalNodes
        else:
            nodes = 1  # This
            children = container.getChildren(itemId)
            if children is not None:
                for idd in children:
                    nodes += self.countNodes(container, idd)
            return nodes


    def validateHierarchy(self, container, itemId=None, parentId=None):
        if itemId is None and parentId is None:
            for rootId in container.rootItemIds():
                self.validateHierarchy(container, rootId, None)
        else:
            children = container.getChildren(itemId)

            # getParent
            self.assertEquals(container.getParent(itemId), parentId)

            if not container.areChildrenAllowed(itemId):
                # If no children is allowed the item should have no children
                self.assertFalse(container.hasChildren(itemId))
                self.assertTrue((children is None) or (len(children) == 0))

                return
            if children is not None:
                for idd in children:
                    self.validateHierarchy(container, idd, itemId)


    def _testHierarchicalContainer(self, container):
        self.initializeHierarchicalContainer(container)
        packages = 21 + 3
        expectedSize = len(self.sampleData) + packages
        self.validateHierarchicalContainer(container, 'com',
                'org.vaadin.test.LastClass',
                'com.vaadin.terminal.ApplicationResource',
                'blah', True, expectedSize, 2, True)


    def _testHierarchicalSorting(self, container):
        sortable = container

        self.initializeHierarchicalContainer(container)

        # Must be able to sort based on PROP1 and PROP2 for this test
        self.assertTrue(self.FULLY_QUALIFIED_NAME in \
                sortable.getSortableContainerPropertyIds())
        self.assertTrue(self.REVERSE_FULLY_QUALIFIED_NAME in \
                sortable.getSortableContainerPropertyIds())

        sortable.sort([self.FULLY_QUALIFIED_NAME], [True])

        packages = 21 + 3
        expectedSize = len(self.sampleData) + packages
        self.validateHierarchicalContainer(container, 'com',
                'org.vaadin.test.LastClass',
                'com.vaadin.terminal.ApplicationResource',
                'blah', True, expectedSize, 2, True)

        sortable.sort([self.REVERSE_FULLY_QUALIFIED_NAME], [True])

        self.validateHierarchicalContainer(container,
                'com.vaadin.terminal.gwt.server.ApplicationPortlet2',
                'com.vaadin.data.util.ObjectProperty',
                'com.vaadin.terminal.ApplicationResource',
                'blah', True, expectedSize, 2, True)


    def initializeHierarchicalContainer(self, container):
        container.removeAllItems()
        propertyIds = list(container.getContainerPropertyIds())
        for propertyId in propertyIds:
            container.removeContainerProperty(propertyId)

        container.addContainerProperty(self.FULLY_QUALIFIED_NAME, str, '')
        container.addContainerProperty(self.SIMPLE_NAME, str, '')
        container.addContainerProperty(self.REVERSE_FULLY_QUALIFIED_NAME,
                str, None)
        container.addContainerProperty(self.ID_NUMBER, int, None)

        for i in range(len(self.sampleData)):
            idd = self.sampleData[i]

            # Add path as parent
            paths = re.split('\\.', idd)
            path = paths[0]
            # Adds "com" and other items multiple times so should return null
            # for all but the first time
            if container.addItem(path) is not None:
                self.assertTrue(container.setChildrenAllowed(path, False))
                item = container.getItem(path)
                item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(path)
                item.getItemProperty(self.SIMPLE_NAME).setValue(
                        self.getSimpleName(path))
                item.getItemProperty(self.REVERSE_FULLY_QUALIFIED_NAME)\
                        .setValue(self.reverse(path))
                item.getItemProperty(self.ID_NUMBER).setValue(1)

            for j in range(1, len(paths)):
                parent = path
                path = path + '.' + paths[j]

                # Adds "com" and other items multiple times so should return
                # null for all but the first time
                if container.addItem(path) is not None:
                    self.assertTrue(container.setChildrenAllowed(path, False))

                    item = container.getItem(path)
                    item.getItemProperty(self.FULLY_QUALIFIED_NAME)\
                            .setValue(path)
                    item.getItemProperty(self.SIMPLE_NAME).setValue(
                            self.getSimpleName(path))
                    item.getItemProperty(self.REVERSE_FULLY_QUALIFIED_NAME)\
                            .setValue(self.reverse(path))
                    item.getItemProperty(self.ID_NUMBER).setValue(1)

                self.assertTrue(container.setChildrenAllowed(parent, True))
                self.assertTrue(container.setParent(path, parent),
                        'Failed to set ' + parent + ' as parent for ' + path)

            item = container.getItem(idd)
            self.assertNotEquals(item, None)
            parent = idd[:idd.rfind('.')]
            self.assertTrue(container.setParent(idd, parent))
            item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(
                    self.sampleData[i])
            item.getItemProperty(self.SIMPLE_NAME).setValue(self.getSimpleName(
                    self.sampleData[i]))
            item.getItemProperty(self.REVERSE_FULLY_QUALIFIED_NAME).setValue(
                    self.reverse(self.sampleData[i]))
            item.getItemProperty(self.ID_NUMBER).setValue(i % 2)
