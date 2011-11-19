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
