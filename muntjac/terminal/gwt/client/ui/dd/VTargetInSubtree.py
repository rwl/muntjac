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

from com.vaadin.terminal.gwt.client.ui.VTree import (VTree,)
from com.vaadin.terminal.gwt.client.ui.dd.VDragAndDropManager import (VDragAndDropManager,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterion import (VAcceptCriterion,)
TreeNode = VTree.TreeNode


class VTargetInSubtree(VAcceptCriterion):

    def accept(self, drag, configuration):
        tree = VDragAndDropManager.get().getCurrentDropHandler().getPaintable()
        treeNode = tree.getNodeByKey(drag.getDropDetails().get('itemIdOver'))
        if treeNode is not None:
            parent2 = treeNode
            depth = configuration.getIntAttribute('depth')
            if depth < 0:
                depth = Integer.MAX_VALUE.MAX_VALUE
            searchedKey = configuration.getStringAttribute('key')
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i <= depth and isinstance(parent2, TreeNode)):
                    break
                if searchedKey == parent2.key:
                    return True
                # panel -> next level node
                parent2 = parent2.getParent().getParent()
        return False
