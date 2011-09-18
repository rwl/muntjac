# Copyright (C) 2011 Vaadin Ltd
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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.ui.Layout import (Layout, MarginHandler, MarginInfo,)
from com.vaadin.ui.AbstractComponentContainer import (AbstractComponentContainer,)
from com.vaadin.terminal.gwt.client.MouseEventDetails import (MouseEventDetails,)
from com.vaadin.terminal.gwt.client.EventId import (EventId,)
# from com.vaadin.ui.Layout.MarginHandler import (MarginHandler,)
# from java.util.Map import (Map,)


class AbstractLayout(AbstractComponentContainer, Layout, MarginHandler):
    """An abstract class that defines default implementation for the {@link Layout}
    interface.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 5.0
    """
    _CLICK_EVENT = EventId.LAYOUT_CLICK
    margins = MarginInfo(False)
    # (non-Javadoc)
    # 
    # @see com.vaadin.ui.Layout#setMargin(boolean)

    def setMargin(self, *args):
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.Layout.MarginHandler#getMargin()

        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], MarginInfo):
                marginInfo, = _0
                self.margins.setMargins(marginInfo)
                self.requestRepaint()
            else:
                enabled, = _0
                self.margins.setMargins(enabled)
                self.requestRepaint()
        elif _1 == 4:
            topEnabled, rightEnabled, bottomEnabled, leftEnabled = _0
            self.margins.setMargins(topEnabled, rightEnabled, bottomEnabled, leftEnabled)
            self.requestRepaint()
        else:
            raise ARGERROR(1, 4)

    def getMargin(self):
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.Layout.MarginHandler#setMargin(MarginInfo)

        return self.margins

    # (non-Javadoc)
    # 
    # @see com.vaadin.ui.Layout#setMargin(boolean, boolean, boolean, boolean)

    # (non-Javadoc)
    # 
    # @see com.vaadin.ui.AbstractComponent#paintContent(com.vaadin
    # .terminal.PaintTarget)

    def paintContent(self, target):
        # Add margin info. Defaults to false.
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.AbstractComponent#changeVariables(java.lang.Object,
        # java.util.Map)

        target.addAttribute('margins', self.margins.getBitMask())

    def changeVariables(self, source, variables):
        super(AbstractLayout, self).changeVariables(source, variables)
        # not all subclasses use these events
        if isinstance(self, LayoutClickNotifier) and self._CLICK_EVENT in variables:
            self.fireClick(variables[self._CLICK_EVENT])

    def fireClick(self, parameters):
        """Fire a layout click event.

        Note that this method is only used by the subclasses that implement
        {@link LayoutClickNotifier}, and can be overridden for custom click event
        firing.

        @param parameters
                   The parameters received from the client side implementation
        """
        mouseDetails = MouseEventDetails.deSerialize(parameters['mouseDetails'])
        clickedComponent = parameters['component']
        childComponent = clickedComponent
        while childComponent is not None and childComponent.getParent() != self:
            childComponent = childComponent.getParent()
        self.fireEvent(self.LayoutClickEvent(self, mouseDetails, clickedComponent, childComponent))
