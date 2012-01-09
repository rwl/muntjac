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


import colorsys

class Color(object):

    BLACK = None
    WHITE = None

    RED = None
    GREEN = None
    BLUE = None

    def __init__(self, r, g, b, a=1.0):
        self._r = self._convert(r)
        self._g = self._convert(g)
        self._b = self._convert(b)
        self._a = self._convert(a)


    def _convert(self, value):
        if isinstance(value, float):
            return int(value * 255)
        else:
            return value

    def getRed(self):
        return self._r

    def getGreen(self):
        return self._g

    def getBlue(self):
        return self._b

    def getAlpha(self):
        return self._a

    def __str__(self):
        return 'rgb(%d,%d,%d)' % (self._r, self._g, self._b)

    def getHSV(self):
        return colorsys.rgb_to_hsv(
                self._r / 255.0,
                self._g / 255.0,
                self._b / 255.0)

Color.BLACK = Color(0.0, 0.0, 0.0)
Color.WHITE = Color(1.0, 1.0, 1.0)
Color.RED   = Color(1.0, 0.0, 0.0)
Color.GREEN = Color(0.0, 1.0, 0.0)
Color.BLUE  = Color(0.0, 0.0, 1.0)
