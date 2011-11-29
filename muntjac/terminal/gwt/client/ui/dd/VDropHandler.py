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
