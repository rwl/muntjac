# Copyright (C) 2010 IT Mill Ltd.
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

import logging

from muntjac.event.dd.TargetDetailsImpl import TargetDetailsImpl
from muntjac.terminal.VariableOwner import VariableOwner
from muntjac.terminal.gwt.server.JsonPaintTarget import JsonPaintTarget
from muntjac.event.dd.DragAndDropEvent import DragAndDropEvent
from muntjac.event.TransferableImpl import TransferableImpl
from muntjac.event.dd.DropTarget import DropTarget
from muntjac.event.dd.DragSource import DragSource
from muntjac.terminal.gwt.client.ui.dd.VDragAndDropManager import DragEventType


logger = logging.getLogger(__name__)


class DragAndDropService(VariableOwner):

    def __init__(self, manager):
        self._manager = manager

        self._lastVisitId = None
        self._lastVisitAccepted = False
        self._dragEvent = None
        self._acceptCriterion = None


    def changeVariables(self, source, variables):
        owner = variables.get('dhowner')

        # Validate drop handler owner
        if not isinstance(owner, DropTarget):
            logger.critical('DropHandler owner ' + owner
                    + ' must implement DropTarget')
            return

        # owner cannot be null here

        dropTarget = owner
        self._lastVisitId = variables.get('visitId')

        # request may be dropRequest or request during drag operation
        # (commonly dragover or dragenter)
        dropRequest = self.isDropRequest(variables)
        if dropRequest:
            self.handleDropRequest(dropTarget, variables)
        else:
            self.handleDragRequest(dropTarget, variables)


    def handleDropRequest(self, dropTarget, variables):
        """Handles a drop request from the VDragAndDropManager.

        @param dropTarget
        @param variables
        """
        dropHandler = dropTarget.getDropHandler()
        if dropHandler is None:
            # No dropHandler returned so no drop can be performed.
            logger.info('DropTarget.getDropHandler() returned null '
                    'for owner: ' + dropTarget)
            return

        # Construct the Transferable and the DragDropDetails for the drop
        # operation based on the info passed from the client widgets (drag
        # source for Transferable, drop target for DragDropDetails).
        transferable = self._constructTransferable(dropTarget, variables)
        dropData = self.constructDragDropDetails(dropTarget, variables)

        dropEvent = DragAndDropEvent(transferable, dropData)

        if dropHandler.getAcceptCriterion().accept(dropEvent):
            dropHandler.drop(dropEvent)


    def handleDragRequest(self, dropTarget, variables):
        """Handles a drag/move request from the VDragAndDropManager.

        @param dropTarget
        @param variables
        """
        self._lastVisitId = variables.get('visitId')

        self._acceptCriterion = \
                dropTarget.getDropHandler().getAcceptCriterion()

        # Construct the Transferable and the DragDropDetails for the drag
        # operation based on the info passed from the client widgets (drag
        # source for Transferable, current target for DragDropDetails).
        transferable = self.constructTransferable(dropTarget, variables)
        dragDropDetails = self.constructDragDropDetails(dropTarget, variables)

        self._dragEvent = DragAndDropEvent(transferable, dragDropDetails)

        self._lastVisitAccepted = self._acceptCriterion.accept(self._dragEvent)


    def constructDragDropDetails(self, dropTarget, variables):
        """Construct DragDropDetails based on variables from client drop
        target. Uses DragDropDetailsTranslator if available, otherwise a
        default DragDropDetails implementation is used.

        @param dropTarget
        @param variables
        @return
        """
        rawDragDropDetails = variables.get('evt')

        dropData = dropTarget.translateDropTargetDetails(rawDragDropDetails)

        if dropData is None:
            # Create a default DragDropDetails with all the raw variables
            dropData = TargetDetailsImpl(rawDragDropDetails, dropTarget)

        return dropData


    def isDropRequest(self, variables):
        return self.getRequestType(variables) == DragEventType.DROP


    def getRequestType(self, variables):
        typ = variables.get('type')
        return DragEventType.values().get(typ)


    def _constructTransferable(self, dropHandlerOwner, variables):
        sourceComponent = variables.get('component')

        variables = variables.get('tra')

        transferable = None
        if (sourceComponent is not None
                and isinstance(sourceComponent, DragSource)):
            transferable = sourceComponent.getTransferable(variables)

        if transferable is None:
            transferable = TransferableImpl(sourceComponent, variables)

        return transferable


    def isEnabled(self):
        return True


    def isImmediate(self):
        return True


    def _printJSONResponse(self, outWriter):
        if self._isDirty():
            outWriter.write(', \"dd\":')
            jsonPaintTarget = JsonPaintTarget(self._manager, outWriter, False)
            jsonPaintTarget.startTag('dd')
            jsonPaintTarget.addAttribute('visitId', self._lastVisitId)
            if self._acceptCriterion is not None:
                jsonPaintTarget.addAttribute('accepted',
                        self._lastVisitAccepted)
                self._acceptCriterion.paintResponse(jsonPaintTarget)
            jsonPaintTarget.endTag('dd')
            jsonPaintTarget.close()
            self._lastVisitId = -1
            self._lastVisitAccepted = False
            self._acceptCriterion = None
            self._dragEvent = None


    def _isDirty(self):
        if self._lastVisitId > 0:
            return True
        return False
