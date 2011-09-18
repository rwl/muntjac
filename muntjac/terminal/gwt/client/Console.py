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
# from java.util.Set import (Set,)


class Console(object):

    def log(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Throwable):
                e, = _0
            else:
                msg, = _0
        else:
            raise ARGERROR(1, 1)

    def error(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Throwable):
                e, = _0
            else:
                msg, = _0
        else:
            raise ARGERROR(1, 1)

    def printObject(self, msg):
        pass

    def dirUIDL(self, u, cnf):
        pass

    def printLayoutProblems(self, meta, applicationConnection, zeroHeightComponents, zeroWidthComponents):
        pass
