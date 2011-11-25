# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@


class VDropHandler(object):
    """Vaadin Widgets that want to receive something via drag and drop implement
    this interface.
    """

    def dragEnter(self, dragEvent):
        """Called by DragAndDropManager when a drag operation is in progress and the
        cursor enters the area occupied by this Paintable.

        @param dragEvent
                   DragEvent which contains the transferable and other
                   information for the operation
        """
        pass

    def dragLeave(self, dragEvent):
        """Called by DragAndDropManager when a drag operation is in progress and the
        cursor leaves the area occupied by this Paintable.

        @param dragEvent
                   DragEvent which contains the transferable and other
                   information for the operation
        """
        pass

    def drop(self, drag):
        """Called by DragAndDropManager when a drag operation was in progress and a
        drop was performed on this Paintable.


        @param dragEvent
                   DragEvent which contains the transferable and other
                   information for the operation

        @return true if the Tranferrable of this drag event needs to be sent to
                the server, false if drop is rejected or no server side event
                should be sent
        """
        pass

    def dragOver(self, currentDrag):
        """When drag is over current drag handler.

        With drag implementation by {@link VDragAndDropManager} will be called
        when mouse is moved. HTML5 implementations call this continuously even
        though mouse is not moved.

        @param currentDrag
        """
        pass

    def getPaintable(self):
        """Returns the Paintable into which this DragHandler is associated"""
        pass

    def getApplicationConnection(self):
        """Returns the application connection to which this {@link VDropHandler}
        belongs to. DragAndDropManager uses this fucction to send Transferable to
        server side.
        """
        pass
