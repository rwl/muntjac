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
from com.vaadin.event.dd.TargetDetails import (TargetDetails,)
# from java.util.HashMap import (HashMap,)
# from java.util.Map import (Map,)


class TargetDetailsImpl(TargetDetails):
    """A HashMap backed implementation of {@link TargetDetails} for terminal
    implementation and for extension.

    @since 6.3
    """
    _data = dict()
    _dropTarget = None

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            rawDropData, = _0
            self._data.putAll(rawDropData)
        elif _1 == 2:
            rawDropData, dropTarget = _0
            self.__init__(rawDropData)
            self._dropTarget = dropTarget
        else:
            raise ARGERROR(1, 2)

    def getData(self, key):
        return self._data[key]

    def setData(self, key, value):
        return self._data.put(key, value)

    def getTarget(self):
        return self._dropTarget
