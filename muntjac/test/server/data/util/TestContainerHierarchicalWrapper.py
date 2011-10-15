# Copyright (C) 2010 IT Mill Ltd.
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
