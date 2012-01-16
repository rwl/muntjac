# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

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
    @version: 1.1.0
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
