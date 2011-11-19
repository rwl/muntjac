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

"""Implementation of ITargetDetails for terminal implementation and
extension."""

from muntjac.event.dd.target_details import ITargetDetails


class TargetDetailsImpl(ITargetDetails):
    """A HashMap backed implementation of L{ITargetDetails} for terminal
    implementation and for extension.
    """

    def __init__(self, rawDropData, dropTarget=None):
        self._data = dict()

        self._data.update(rawDropData)
        self._dropTarget = dropTarget


    def getData(self, key):
        return self._data.get(key)


    def setData(self, key, value):
        if key in self._data:
            return self._data[key]
        else:
            self._data[key] = value
            return None


    def getTarget(self):
        return self._dropTarget
