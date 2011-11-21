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
