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

from muntjac.ui.OrderedLayout import OrderedLayout

#from muntjac.terminal.gwt.client.ui.VFormLayout import VFormLayout
#from muntjac.ui.ClientWidget import LoadStyle


class FormLayout(OrderedLayout):
    """FormLayout is used by {@link Form} to layout fields. It may also be used
    separately without {@link Form}.

    FormLayout is a close relative to vertical {@link OrderedLayout}, but in
    FormLayout caption is rendered on left side of component. Required and
    validation indicators are between captions and fields.

    FormLayout does not currently support some advanced methods from
    OrderedLayout like setExpandRatio and setComponentAlignment.

    FormLayout by default has component spacing on. Also margin top and margin
    bottom are by default on.
    """

#    CLIENT_WIDGET = VFormLayout
#    LOAD_STYLE = LoadStyle.EAGER

    def __init__(self):
        super(FormLayout, self)()
        self.setSpacing(True)
        self.setMargin(True, False, True, False)
