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

"""Defines the default implementation of the ILayout interface."""

from muntjac.ui.layout import ILayout, IMarginHandler, MarginInfo
from muntjac.ui.abstract_component_container import AbstractComponentContainer
from muntjac.terminal.gwt.client.mouse_event_details import MouseEventDetails
from muntjac.terminal.gwt.client.event_id import EventId
from muntjac.event.layout_events import ILayoutClickNotifier, LayoutClickEvent


class AbstractLayout(AbstractComponentContainer, ILayout, IMarginHandler):
    """An abstract class that defines default implementation for the
    L{ILayout} interface.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    _CLICK_EVENT = EventId.LAYOUT_CLICK

    def __init__(self):
        super(AbstractLayout, self).__init__()

        self.margins = MarginInfo(False)


    def setMargin(self, *args):
        nargs = len(args)
        if nargs == 1:
            if isinstance(args[0], MarginInfo):
                marginInfo, = args
                self.margins.setMargins(marginInfo)
                self.requestRepaint()
            else:
                enabled, = args
                self.margins.setMargins(enabled)
                self.requestRepaint()
        elif nargs == 4:
            topEnabled, rightEnabled, bottomEnabled, leftEnabled = args
            self.margins.setMargins(topEnabled, rightEnabled,
                    bottomEnabled, leftEnabled)
            self.requestRepaint()
        else:
            raise ValueError, 'invalid number of arguments'


    def getMargin(self):
        return self.margins


    def paintContent(self, target):
        # Add margin info. Defaults to false.
        target.addAttribute('margins', int( self.margins.getBitMask() ))


    def changeVariables(self, source, variables):
        super(AbstractLayout, self).changeVariables(source, variables)
        # not all subclasses use these events
        if (isinstance(self, ILayoutClickNotifier)
                and self._CLICK_EVENT in variables):
            self.fireClick( variables.get(self._CLICK_EVENT) )


    def fireClick(self, parameters):
        """Fire a layout click event.

        Note that this method is only used by the subclasses that
        implement L{LayoutClickNotifier}, and can be overridden
        for custom click event firing.

        @param parameters:
                   The parameters received from the client side
                   implementation
        """
        mouseDetails = MouseEventDetails.deSerialize(
                parameters.get('mouseDetails'))

        clickedComponent = parameters.get('component')

        childComponent = clickedComponent
        while (childComponent is not None
                and childComponent.getParent() != self):
            childComponent = childComponent.getParent()

        self.fireEvent(LayoutClickEvent(self, mouseDetails,
                clickedComponent, childComponent))
