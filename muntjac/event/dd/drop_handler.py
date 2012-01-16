# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Contains the actual business logic for drag and drop operations."""


class IDropHandler(object):
    """DropHandlers contain the actual business logic for drag and drop
    operations.

    The L{drop} method is used to receive the transferred data and the
    L{getAcceptCriterion} method contains the (possibly client side verifiable)
    criterion whether the dragged data will be handled at all.
    """

    def drop(self, event):
        """Drop method is called when the end user has finished the drag
        operation on a L{DropTarget} and L{DragAndDropEvent} has passed
        L{AcceptCriterion} defined by L{getAcceptCriterion} method. The
        actual business logic of drag and drop operation is implemented
        into this method.

        @param event:
                   the event related to this drop
        """
        raise NotImplementedError


    def getAcceptCriterion(self):
        """Returns the L{AcceptCriterion} used to evaluate whether the
        L{Transferable} will be handed over to L{IDropHandler.drop} method.
        If client side can't verify the L{AcceptCriterion}, the same criteria
        may be tested also prior to actual drop - during the drag operation.

        Based on information from L{AcceptCriterion} components may display
        some hints for the end user whether the drop will be accepted or not.

        Muntjac contains a variety of criteria built in that can be composed
        to more complex criterion. If the build in criteria are not enough,
        developer can use a L{ServerSideCriterion} or build own custom
        criterion with client side counterpart.

        If developer wants to handle everything in the L{drop} method,
        L{AcceptAll} instance can be returned.

        @return: the L{AcceptCriterion}
        """
        raise NotImplementedError
