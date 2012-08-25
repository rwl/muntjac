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
