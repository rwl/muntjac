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


class TooltipInfo(object):
    _title = None
    _errorUidl = None

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            pass # astStmt: [Stmt([]), None]
        elif _1 == 1:
            tooltip, = _0
            self.setTitle(tooltip)
        else:
            raise ARGERROR(0, 1)

    def getTitle(self):
        return self._title

    def setTitle(self, title):
        self._title = title

    def getErrorUidl(self):
        return self._errorUidl

    def setErrorUidl(self, errorUidl):
        self._errorUidl = errorUidl
