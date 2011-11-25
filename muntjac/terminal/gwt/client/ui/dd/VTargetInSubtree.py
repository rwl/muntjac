# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
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
