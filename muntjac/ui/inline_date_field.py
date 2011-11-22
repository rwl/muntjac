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

"""Defines a date entry component, which displays the actual date selector
inline."""

from datetime import datetime

from muntjac.ui.date_field import DateField
from muntjac.data.property import IProperty


class InlineDateField(DateField):
    """A date entry component, which displays the actual date selector inline.

    @see: L{DateField}
    @see: L{PopupDateField}
    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.1
    """

    CLIENT_WIDGET = None #ClientWidget(VDateFieldCalendar)

    def __init__(self, *args):
        nargs = len(args)
        if nargs == 0:
            super(InlineDateField, self).__init__()
        elif nargs == 1:
            if isinstance(args[0], IProperty):
                dataSource, = args
                super(InlineDateField, self).__init__(dataSource)
            else:
                caption, = args
                super(InlineDateField, self).__init__(caption)
        elif nargs == 2:
            if isinstance(args[1], datetime):
                caption, value = args
                super(InlineDateField, self).__init__(caption, value)
            else:
                caption, dataSource = args
                super(InlineDateField, self).__init__(caption, dataSource)
        else:
            raise ValueError, 'too many arguments'
