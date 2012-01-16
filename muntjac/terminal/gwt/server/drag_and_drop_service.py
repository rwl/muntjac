# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

import logging

from muntjac.event.dd.target_details_impl import TargetDetailsImpl
from muntjac.terminal.variable_owner import IVariableOwner
from muntjac.terminal.gwt.server.json_paint_target import JsonPaintTarget
from muntjac.event.dd.drag_and_drop_event import DragAndDropEvent
from muntjac.event.transferable_impl import TransferableImpl
from muntjac.event.dd.drop_target import IDropTarget
from muntjac.event.dd.drag_source import IDragSource
from muntjac.terminal.gwt.client.ui.dd.v_drag_and_drop_manager import DragEventType


logger = logging.getLogger(__name__)


class DragAndDropService(IVariableOwner):

    def __init__(self, manager):
        self._manager = manager

        self._lastVisitId = None
        self._lastVisitAccepted = False
        self._dragEvent = None
        self._acceptCriterion = None


    def changeVariables(self, source, variables):
        owner = variables.get('dhowner')

        # Validate drop handler owner
        if not isinstance(owner, IDropTarget):
            logger.critical('DropHandler owner ' + owner
                    + ' must implement IDropTarget')
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
        """
        dropHandler = dropTarget.getDropHandler()
        if dropHandler is None:
            # No dropHandler returned so no drop can be performed.
            logger.info('IDropTarget.getDropHandler() returned null '
                    'for owner: ' + dropTarget)
            return

        # Construct the Transferable and the DragDropDetails for the drop
        # operation based on the info passed from the client widgets (drag
        # source for Transferable, drop target for DragDropDetails).
        transferable = self.constructTransferable(dropTarget, variables)
        dropData = self.constructDragDropDetails(dropTarget, variables)

        dropEvent = DragAndDropEvent(transferable, dropData)

        if dropHandler.getAcceptCriterion().accept(dropEvent):
            dropHandler.drop(dropEvent)


    def handleDragRequest(self, dropTarget, variables):
        """Handles a drag/move request from the VDragAndDropManager.
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
        typ = int( variables.get('type') )
        return DragEventType.values()[typ]


    def constructTransferable(self, dropHandlerOwner, variables):
        sourceComponent = variables.get('component')

        variables = variables.get('tra')

        transferable = None
        if (sourceComponent is not None
                and isinstance(sourceComponent, IDragSource)):
            transferable = sourceComponent.getTransferable(variables)

        if transferable is None:
            transferable = TransferableImpl(sourceComponent, variables)

        return transferable


    def isEnabled(self):
        return True


    def isImmediate(self):
        return True


    def printJSONResponse(self, outWriter):
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
