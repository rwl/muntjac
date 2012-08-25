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
