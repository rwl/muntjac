# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.data.util.abstract_hierarchical_container_test \
    import AbstractHierarchicalContainerTest

from muntjac.data.util.container_hierarchical_wrapper import \
    ContainerHierarchicalWrapper

from muntjac.data.util.indexed_container import IndexedContainer


class TestContainerHierarchicalWrapper(AbstractHierarchicalContainerTest):

    def testBasicOperations(self):
        container = ContainerHierarchicalWrapper(IndexedContainer())
        self._testBasicContainerOperations(container)


    def testHierarchicalContainer(self):
        container = ContainerHierarchicalWrapper(IndexedContainer())
        self._testHierarchicalContainer(container)


    def testRemoveSubtree(self):
        container = ContainerHierarchicalWrapper(IndexedContainer())
        self._testRemoveHierarchicalWrapperSubtree(container)


    def _testRemoveHierarchicalWrapperSubtree(self, container):
        self.initializeHierarchicalContainer(container)

        # remove root item
        container.removeItemRecursively('org')

        packages = (21 + 3) - 3
        expectedSize = (len(self.sampleData) + packages) - 1

        self.validateContainer(container, 'com',
                'com.vaadin.util.SerializerHelper',
                'com.vaadin.terminal.ApplicationResource',
                'blah', True, expectedSize)

        # rootItemIds
        rootIds = container.rootItemIds()
        self.assertEquals(1, len(rootIds))
