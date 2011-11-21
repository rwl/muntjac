# Copyright (C) 2011 Vaadin Ltd.
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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

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
