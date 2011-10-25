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

from muntjac.ui.abstract_ordered_layout import AbstractOrderedLayout


class HorizontalLayout(AbstractOrderedLayout):
    """Horizontal layout

    <code>HorizontalLayout</code> is a component container, which shows
    the subcomponents in the order of their addition (horizontally).

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 5.3
    """

    CLIENT_WIDGET = None #ClientWidget(VHorizontalLayout, LoadStyle.EAGER)

    def __init__(self):
        super(HorizontalLayout, self).__init__()
