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

from muntjac.ui.AbstractSplitPanel import AbstractSplitPanel

#from muntjac.terminal.gwt.client.ui.VSplitPanelVertical import VSplitPanelVertical
#from muntjac.ui.ClientWidget import LoadStyle


class VerticalSplitPanel(AbstractSplitPanel):
    """A vertical split panel contains two components and lays them vertically. The
    first component is above the second component.

    <pre>
         +--------------------------+
         |                          |
         |  The first component     |
         |                          |
         +==========================+  <-- splitter
         |                          |
         |  The second component    |
         |                          |
         +--------------------------+
    </pre>
    """

#    CLIENT_WIDGET = VSplitPanelVertical
#    LOAD_STYLE = LoadStyle.EAGER

    def __init__(self):
        super(VerticalSplitPanel, self)()
        self.setSizeFull()
