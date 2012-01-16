# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

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
