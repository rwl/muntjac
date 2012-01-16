# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""wraps drop target related information about DragAndDropEvent."""


class ITargetDetails(object):
    """ITargetDetails wraps drop target related information about
    L{DragAndDropEvent}.

    When a ITargetDetails object is used in L{DropHandler} it is often
    preferable to cast the ITargetDetails to an implementation provided by
    DropTarget like L{TreeTargetDetails}. They often provide a better typed,
    drop target specific API.
    """

    def getData(self, key):
        """Gets target data associated with the given string key

        @return: The data associated with the key
        """
        raise NotImplementedError


    def getTarget(self):
        """@return: the drop target on which the L{DragAndDropEvent}
        happened."""
        raise NotImplementedError
