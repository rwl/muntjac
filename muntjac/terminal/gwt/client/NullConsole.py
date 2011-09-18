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
from com.vaadin.terminal.gwt.client.Console import (Console,)
# from java.util.Set import (Set,)


class NullConsole(Console):
    """Client side console implementation for non-debug mode that discards all
    messages.
    """

    def dirUIDL(self, u, cnf):
        pass

    def error(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Throwable):
                e, = _0
                self.GWT.log(e.getMessage(), e)
            else:
                msg, = _0
                self.GWT.log(msg)
        else:
            raise ARGERROR(1, 1)

    def log(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Throwable):
                e, = _0
                self.GWT.log(e.getMessage(), e)
            else:
                msg, = _0
                self.GWT.log(msg)
        else:
            raise ARGERROR(1, 1)

    def printObject(self, msg):
        self.GWT.log(str(msg))

    def printLayoutProblems(self, meta, applicationConnection, zeroHeightComponents, zeroWidthComponents):
        pass
