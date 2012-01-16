# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""An interface for components supporting drop operations."""

from muntjac.ui.component import IComponent


class IDropTarget(IComponent):
    """IDropTarget is an interface for components supporting drop operations. A
    component that wants to receive drop events should implement this interface
    and provide a L{DropHandler} which will handle the actual drop event.
    """

    def getDropHandler(self):
        """@return: the drop handler that will receive the dragged data or null
                if drops are not currently accepted
        """
        raise NotImplementedError


    def translateDropTargetDetails(self, clientVariables):
        """Called before the L{DragAndDropEvent} is passed to
        L{DropHandler}. Implementation may for example translate the drop
        target details provided by the client side (drop target) to meaningful
        server side values. If null is returned the terminal implementation
        will automatically create a L{TargetDetails} with raw client side data.

        @see: DragSource#getTransferable(Map)

        @param clientVariables:
                   data passed from the DropTargets client side counterpart.
        @return: A DropTargetDetails object with the translated data or null to
                use a default implementation.
        """
        raise NotImplementedError
