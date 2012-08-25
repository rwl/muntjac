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
