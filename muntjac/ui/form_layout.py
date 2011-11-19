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

"""Used by C{Form} to layout fields."""

from muntjac.ui.ordered_layout import OrderedLayout


class FormLayout(OrderedLayout):
    """FormLayout is used by L{Form} to layout fields. It may also be
    used separately without L{Form}.

    FormLayout is a close relative to vertical L{OrderedLayout}, but
    in FormLayout caption is rendered on left side of component. Required
    and validation indicators are between captions and fields.

    FormLayout does not currently support some advanced methods from
    OrderedLayout like setExpandRatio and setComponentAlignment.

    FormLayout by default has component spacing on. Also margin top and
    margin bottom are by default on.
    """

    CLIENT_WIDGET = None #ClientWidget(VFormLayout, LoadStyle.EAGER)

    def __init__(self):
        super(FormLayout, self).__init__()
        self.setSpacing(True)
        self.setMargin(True, False, True, False)
