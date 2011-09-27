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

from datetime import datetime

from muntjac.ui.DateField import DateField
from muntjac.data.Property import Property


class InlineDateField(DateField):
    """A date entry component, which displays the actual date selector inline.

    @see DateField
    @see PopupDateField
    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 5.0
    """

    def __init__(self, *args):
        nargs = len(args)
        if nargs == 0:
            super(InlineDateField, self)()
        elif nargs == 1:
            if isinstance(args[0], Property):
                dataSource, = args
                super(InlineDateField, self)(dataSource)
            else:
                caption, = args
                super(InlineDateField, self)(caption)
        elif nargs == 2:
            if isinstance(args[1], datetime):
                caption, value = args
                super(InlineDateField, self)(caption, value)
            else:
                caption, dataSource = args
                super(InlineDateField, self)(caption, dataSource)
        else:
            raise ValueError, 'too many arguments'
