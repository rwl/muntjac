# -*- coding: utf-8 -*-
from com.vaadin.data.util.AbstractHierarchicalContainerTest import (AbstractHierarchicalContainerTest,)
# from com.vaadin.data.util.ContainerHierarchicalWrapper import (ContainerHierarchicalWrapper,)
# from com.vaadin.data.util.IndexedContainer import (IndexedContainer,)
# from java.util.Collection import (Collection,)


class TestContainerHierarchicalWrapper(AbstractHierarchicalContainerTest):

    def testBasicOperations(self):
        self.testBasicContainerOperations(ContainerHierarchicalWrapper(IndexedContainer()))

    def testHierarchicalContainer(self):
        self.testHierarchicalContainer(ContainerHierarchicalWrapper(IndexedContainer()))

    def testRemoveSubtree(self):
        self.testRemoveHierarchicalWrapperSubtree(ContainerHierarchicalWrapper(IndexedContainer()))

    def testRemoveHierarchicalWrapperSubtree(self, container):
        self.initializeContainer(container)
        # remove root item
        container.removeItemRecursively('org')
        packages = (21 + 3) - 3
        expectedSize = (self.sampleData.length + packages) - 1
        self.validateContainer(container, 'com', 'com.vaadin.util.SerializerHelper', 'com.vaadin.terminal.ApplicationResource', 'blah', True, expectedSize)
        # rootItemIds
        rootIds = container.rootItemIds()
        self.assertEquals(1, len(rootIds))
