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

# from com.vaadin.ui.Tree import (Tree,)
# from com.vaadin.ui.Tree.CollapseEvent import (CollapseEvent,)
# from com.vaadin.ui.Tree.CollapseListener import (CollapseListener,)
# from com.vaadin.ui.Tree.ExpandEvent import (ExpandEvent,)
# from com.vaadin.ui.Tree.ExpandListener import (ExpandListener,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.List import (List,)
# from junit.framework.TestCase import (TestCase,)


class TestListeners(TestCase, ExpandListener, CollapseListener):
    _expandCalled = None
    _collapseCalled = None
    _lastExpanded = None
    _lastCollapsed = None

    def setUp(self):
        self._expandCalled = 0

    def testExpandListener(self):
        tree = self.createTree(10, 20, False)
        tree.addListener(self)
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
        """Creates a tree with "rootItems" roots, each with "children" children,
        each with 1 child.

        @param rootItems
        @param children
        @param expand
        @return
        """
        tree = Tree()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < rootItems):
                break
            rootId = 'root ' + i
            tree.addItem(rootId)
            if expand:
                tree.expandItemsRecursively(rootId)
            else:
                tree.collapseItemsRecursively(rootId)
            _1 = True
            j = 0
            while True:
                if _1 is True:
                    _1 = False
                else:
                    j += 1
                if not (j < children):
                    break
                childId = 'child ' + i + '/' + j
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
        tree.addListener(self)
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
