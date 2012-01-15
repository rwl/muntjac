# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

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
    @version: @VERSION@
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
