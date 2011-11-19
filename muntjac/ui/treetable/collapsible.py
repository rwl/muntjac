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

from muntjac.data import container


class ICollapsible(container.IHierarchical, container.IOrdered):
    """Container needed by large lazy loading hierarchies displayed in
    TreeTable.

    Container of this type gets notified when a subtree is opened/closed
    in a component displaying its content. This allows container to lazy
    load subtrees and release memory when a sub-tree is no longer displayed.

    Methods from L{IOrdered} (and from L{IIndexed} if implemented) are
    expected to work as in "preorder" of the currently visible hierarchy.
    This means for example that the return value of size method changes
    when subtree is collapsed/expanded. In other words items in collapsed
    sub trees should be "ignored" by container when the container is accessed
    with methods introduced in L{IOrdered} or L{IIndexed}. From the accessors
    point of view, items in collapsed subtrees don't exist.
    """

    def setCollapsed(self, itemId, collapsed):
        """Collapsing the L{Item} indicated by C{itemId} hides all
        children, and their respective children, from the L{Container}.

        If called on a leaf L{Item}, this method does nothing.

        @param itemId:
                   the identifier of the collapsed L{Item}
        @param collapsed:
                   True if you want to collapse the children below
                   this L{Item}. False if you want to uncollapse the
                   children.
        """
        raise NotImplementedError


    def isCollapsed(self, itemId):
        """Checks whether the L{Item}, identified by C{itemId} is
        collapsed or not.

        If an L{Item} is "collapsed" its children are not included in
        methods used to list Items in this container.

        @param itemId:
                   The L{Item}'s identifier that is to be checked.
        @return: C{True} iff the L{Item} identified by C{itemId} is
                 currently collapsed, otherwise C{False}.
        """
        raise NotImplementedError
