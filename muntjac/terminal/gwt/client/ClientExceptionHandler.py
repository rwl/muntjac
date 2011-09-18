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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)


class ClientExceptionHandler(object):

    @classmethod
    def displayError(cls, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Throwable):
                e, = _0
                cls.displayError(e.getClass().getName() + ': ' + e.getMessage())
                cls.GWT.log(e.getMessage(), e)
            else:
                msg, = _0
                VConsole.error(msg)
                cls.GWT.log(msg)
        elif _1 == 2:
            msg, e = _0
            cls.displayError(msg)
            cls.displayError(e)
        else:
            raise ARGERROR(1, 2)
