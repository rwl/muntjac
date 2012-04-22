# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Helper for TreeTable."""

from muntjac.data.util.container_ordered_wrapper import ContainerOrderedWrapper
from muntjac.data.container import IHierarchical


class HierarchicalContainerOrderedWrapper(ContainerOrderedWrapper,
            IHierarchical):
    """Helper for TreeTable. Does the same thing as ContainerOrderedWrapper
    to fit into table but retains Hierarchical feature."""

    def __init__(self, toBeWrapped):
        super(HierarchicalContainerOrderedWrapper, self).__init__(toBeWrapped)
        self._hierarchical = toBeWrapped


    def areChildrenAllowed(self, itemId):
        return self._hierarchical.areChildrenAllowed(itemId)


    def getChildren(self, itemId):
        return self._hierarchical.getChildren(itemId)


    def getParent(self, itemId):
        return self._hierarchical.getParent(itemId)


    def hasChildren(self, itemId):
        return self._hierarchical.hasChildren(itemId)


    def isRoot(self, itemId):
        return self._hierarchical.isRoot(itemId)


    def rootItemIds(self):
        return self._hierarchical.rootItemIds()


    def setChildrenAllowed(self, itemId, areChildrenAllowed):
        return self._hierarchical.setChildrenAllowed(itemId, areChildrenAllowed)


    def setParent(self, itemId, newParentId):
        return self._hierarchical.setParent(itemId, newParentId)
