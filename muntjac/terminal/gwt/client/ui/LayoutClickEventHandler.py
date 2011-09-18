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

from com.vaadin.terminal.gwt.client.MouseEventDetails import (MouseEventDetails,)
from com.vaadin.terminal.gwt.client.ui.ClickEventHandler import (ClickEventHandler,)
# from java.util.HashMap import (HashMap,)
# from java.util.Map import (Map,)


class LayoutClickEventHandler(ClickEventHandler):

    def __init__(self, paintable, clickEventIdentifier):
        super(LayoutClickEventHandler, self)(paintable, clickEventIdentifier)

    def getChildComponent(self, element):
        pass

    def fireClick(self, event):
        client = self.getApplicationConnection()
        pid = self.getApplicationConnection().getPid(self.paintable)
        mouseDetails = MouseEventDetails(event, self.getRelativeToElement())
        childComponent = self.getChildComponent(event.getEventTarget())
        parameters = dict()
        parameters.put('mouseDetails', mouseDetails.serialize())
        parameters.put('component', childComponent)
        client.updateVariable(pid, self.clickEventIdentifier, parameters, True)
