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

"""Defines a panel that contains two components and lays them out
horizontally."""

from muntjac.ui.abstract_split_panel import AbstractSplitPanel


class HorizontalSplitPanel(AbstractSplitPanel):
    """A horizontal split panel contains two components and lays them
    horizontally. The first component is on the left side::

         +---------------------++----------------------+
         |                     ||                      |
         | The first component || The second component |
         |                     ||                      |
         +---------------------++----------------------+

                               ^
                               |
                         the splitter

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.0
    """

    CLIENT_WIDGET = None #ClientWidget(VSplitPanelHorizontal, LoadStyle.EAGER)

    def __init__(self):
        super(HorizontalSplitPanel, self).__init__()
        self.setSizeFull()
