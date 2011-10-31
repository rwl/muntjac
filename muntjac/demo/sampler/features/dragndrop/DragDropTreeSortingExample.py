
from muntjac.demo.sampler.ExampleUtil import ExampleUtil
from muntjac.api import VerticalLayout, Tree
from muntjac.ui.tree import TreeDragMode
from muntjac.event.dd.drop_handler import IDropHandler
from muntjac.event.dd.acceptcriteria.accept_all import AcceptAll
from muntjac.event.data_bound_transferable import DataBoundTransferable

from muntjac.terminal.gwt.client.ui.dd.vertical_drop_location import \
    VerticalDropLocation


class DragDropTreeSortingExample(VerticalLayout):

    def __init__(self):
        super(DragDropTreeSortingExample, self).__init__()

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
        for idd in tree.rootItemIds():
            tree.expandItemsRecursively(idd)

        tree.setDragMode(TreeDragMode.NODE)
        tree.setDropHandler(TreeSortDropHandler(tree, container))

        self.addComponent(tree)


class TreeSortDropHandler(IDropHandler):

    def __init__(self, tree, container):
        """Tree must use L{HierarchicalContainer}.

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
        if (t.getSourceComponent() != self._tree
                or (not isinstance(t, DataBoundTransferable))):
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
        """Move a node within a tree onto, above or below another node
        depending on the drop location.

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
            if (container.setParent(sourceItemId, targetItemId)
                    and container.hasChildren(targetItemId)):
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
