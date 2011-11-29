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

from muntjac.terminal.gwt.client.ui.click_event_handler import ClickEventHandler
from muntjac.terminal.gwt.client.mouse_event_details import MouseEventDetails


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
        parameters['mouseDetails'] = mouseDetails.serialize()
        parameters['component'] = childComponent
        client.updateVariable(pid, self.clickEventIdentifier, parameters, True)
