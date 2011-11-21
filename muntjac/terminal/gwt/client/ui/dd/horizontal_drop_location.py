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


class HorizontalDropLocation(object):

    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    CENTER = 'CENTER'

    _values = [LEFT, RIGHT, CENTER]

    @classmethod
    def values(cls):
        return cls._enum_values[:]

    @classmethod
    def valueOf(cls, name):
        for v in cls._values:
            if v.lower() == name.lower():
                return v
        else:
            return None
