# -*- coding: utf-8 -*-
from muntjac.demo.sampler.ExampleUtil import (ExampleUtil,)
# from com.vaadin.data.util.HierarchicalContainer import (HierarchicalContainer,)
# from com.vaadin.event.Transferable import (Transferable,)
# from com.vaadin.event.dd.acceptcriteria.AcceptAll import (AcceptAll,)
# from com.vaadin.ui.Tree import (Tree,)
# from com.vaadin.ui.Tree.TreeDragMode import (TreeDragMode,)
# from com.vaadin.ui.Tree.TreeTargetDetails import (TreeTargetDetails,)
# from com.vaadin.ui.VerticalLayout import (VerticalLayout,)
# from java.util.Iterator import (Iterator,)


class DragDropTreeSortingExample(VerticalLayout):

    def __init__(self):
        self.setSpacing(True)
        tree = Tree('Tree sortable using drag\'n\'drop')
        # Populate the tree
        container = ExampleUtil.getHardwareContainer()
        tree.setContainerDataSource(container)
        tree.setItemCaptionPropertyId(ExampleUtil.hw_PROPERTY_NAME)
        tree.setItemIconPropertyId(ExampleUtil.hw_PROPERTY_ICON)
        # Allow all nodes to have children
        for itemId in tree.getItemIds():
            tree.setChildrenAllowed(itemId, True)
        # Expand all nodes
        _0 = True
        it = tree.rootItemIds()
        while True:
            if _0 is True:
                _0 = False
            if not it.hasNext():
                break
            tree.expandItemsRecursively(it.next())
        tree.setDragMode(TreeDragMode.NODE)
        tree.setDropHandler(self.TreeSortDropHandler(tree, container))
        self.addComponent(tree)

    class TreeSortDropHandler(DropHandler):
        _tree = None

        def __init__(self, tree, container):
            """Tree must use {@link HierarchicalContainer}.

            @param tree
            """
            self._tree = tree

        def getAcceptCriterion(self):
            # Alternatively, could use the following criteria to eliminate some
            # checks in drop():
            # new And(IsDataBound.get(), new DragSourceIs(tree));
            return AcceptAll.get()

        def drop(self, dropEvent):
            # Called whenever a drop occurs on the component
            # Make sure the drag source is the same tree
            t = dropEvent.getTransferable()
            # see the comment in getAcceptCriterion()
            if (
                (t.getSourceComponent() != self._tree) or (not isinstance(t, DataBoundTransferable))
            ):
                return
            dropData = dropEvent.getTargetDetails()
            sourceItemId = t.getItemId()
            # FIXME: Why "over", should be "targetItemId" or just
            # "getItemId"
            targetItemId = dropData.getItemIdOver()
            # Location describes on which part of the node the drop took
            # place
            location = dropData.getDropLocation()
            self.moveNode(sourceItemId, targetItemId, location)

        def moveNode(self, sourceItemId, targetItemId, location):
            """Move a node within a tree onto, above or below another node depending
            on the drop location.

            @param sourceItemId
                       id of the item to move
            @param targetItemId
                       id of the item onto which the source node should be moved
            @param location
                       VerticalDropLocation indicating where the source node was
                       dropped relative to the target node
            """
            container = self._tree.getContainerDataSource()
            # Sorting goes as
            # - If dropped ON a node, we append it as a child
            # - If dropped on the TOP part of a node, we move/add it before
            # the node
            # - If dropped on the BOTTOM part of a node, we move/add it
            # after the node
            if location == VerticalDropLocation.MIDDLE:
                if (
                    container.setParent(sourceItemId, targetItemId) and container.hasChildren(targetItemId)
                ):
                    # move first in the container
                    container.moveAfterSibling(sourceItemId, None)
            elif location == VerticalDropLocation.TOP:
                parentId = container.getParent(targetItemId)
                if container.setParent(sourceItemId, parentId):
                    # reorder only the two items, moving source above target
                    container.moveAfterSibling(sourceItemId, targetItemId)
                    container.moveAfterSibling(targetItemId, sourceItemId)
            elif location == VerticalDropLocation.BOTTOM:
                parentId = container.getParent(targetItemId)
                if container.setParent(sourceItemId, parentId):
                    container.moveAfterSibling(sourceItemId, targetItemId)
