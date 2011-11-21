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

from unittest import TestCase
from muntjac.ui.tree import IExpandListener, ICollapseListener, Tree


class TestTreeListeners(TestCase, IExpandListener, ICollapseListener):

    def setUp(self):
        TestCase.setUp(self)

        self._expandCalled = 0
        self._collapseCalled = 0
        self._lastExpanded = 0
        self._lastCollapsed = 0


    def testExpandListener(self):
        tree = self.createTree(10, 20, False)
        tree.addListener(self, IExpandListener)
        rootIds = list(tree.rootItemIds())

        self.assertEquals(10, len(rootIds))
        self.assertEquals(10 + (10 * 20) + 10, len(tree))

        # Expanding should send one expand event for the root item id
        tree.expandItem(rootIds[0])
        self.assertEquals(1, self._expandCalled)
        self.assertEquals(rootIds[0], self._lastExpanded)

        # Expand should send one event for each expanded item id.
        # In this case root + child 4
        self._expandCalled = 0
        tree.expandItemsRecursively(rootIds[1])
        self.assertEquals(2, self._expandCalled)
        c = list(tree.getChildren(rootIds[1]))

        self.assertEquals(c[4], self._lastExpanded)

        # Expanding an already expanded item should send no expand event
        self._expandCalled = 0
        tree.expandItem(rootIds[0])
        self.assertEquals(0, self._expandCalled)


    def createTree(self, rootItems, children, expand):
        """Creates a tree with "rootItems" roots, each with "children"
        children, each with 1 child.
        """
        tree = Tree()

        for i in range(rootItems):
            rootId = 'root ' + str(i)
            tree.addItem(rootId)
            if expand:
                tree.expandItemsRecursively(rootId)
            else:
                tree.collapseItemsRecursively(rootId)

            for j in range(children):
                childId = 'child ' + str(i) + '/' + str(j)
                tree.addItem(childId)
                tree.setParent(childId, rootId)
                tree.setChildrenAllowed(childId, False)
                if j == 4:
                    tree.setChildrenAllowed(childId, True)
                    grandChildId = tree.addItem()
                    tree.setParent(grandChildId, childId)
                    tree.setChildrenAllowed(grandChildId, False)
                    if expand:
                        tree.expandItemsRecursively(childId)
                    else:
                        tree.collapseItemsRecursively(childId)

        return tree


    def testCollapseListener(self):
        tree = self.createTree(7, 15, True)
        tree.addListener(self, ICollapseListener)

        rootIds = list(tree.rootItemIds())
        self.assertEquals(7, len(rootIds))
        self.assertEquals(7 + (7 * 15) + 7, len(tree))

        # Expanding should send one expand event for the root item id
        tree.collapseItem(rootIds[0])
        self.assertEquals(1, self._collapseCalled)
        self.assertEquals(rootIds[0], self._lastCollapsed)

        # Collapse sends one event for each collapsed node.
        # In this case root + child 4
        self._collapseCalled = 0
        tree.collapseItemsRecursively(rootIds[1])
        self.assertEquals(2, self._collapseCalled)
        c = list(tree.getChildren(rootIds[1]))
        self.assertEquals(c[4], self._lastCollapsed)

        # Collapsing an already expanded item should send no expand event
        self._collapseCalled = 0
        tree.collapseItem(rootIds[0])
        self.assertEquals(0, self._collapseCalled)


    def nodeExpand(self, event):
        self._lastExpanded = event.getItemId()
        self._expandCalled += 1


    def nodeCollapse(self, event):
        self._lastCollapsed = event.getItemId()
        self._collapseCalled += 1
