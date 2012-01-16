# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

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
