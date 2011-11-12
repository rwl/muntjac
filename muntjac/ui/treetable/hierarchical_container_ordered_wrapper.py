# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.data.util.ContainerOrderedWrapper import (ContainerOrderedWrapper,)
# from java.util.Collection import (Collection,)
Hierarchical = Container.Hierarchical


class HierarchicalContainerOrderedWrapper(ContainerOrderedWrapper, Hierarchical):
    # Helper for TreeTable. Does the same thing as ContainerOrderedWrapper
    # to fit into table but retains Hierarchical feature.

    _hierarchical = None

    def __init__(self, toBeWrapped):
        super(HierarchicalContainerOrderedWrapper, self)(toBeWrapped)
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
