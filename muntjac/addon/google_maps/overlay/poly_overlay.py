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


class PolyOverlay(object):

    def __init__(self, Id, points, color='#ffffff', weight=1, opacity=1.0,
                clickable=False):
        self._id = Id
        self._points = points
        self._color = color
        self._weight = weight
        self._opacity = opacity
        self._clickable = clickable

    def getId(self):
        return self._id

    def setId(self, Id):
        self._id = Id

    def getPoints(self):
        return self._points

    def setPoints(self, points):
        self._points = points

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color

    def getWeight(self):
        return self._weight

    def setWeight(self, weight):
        self._weight = weight

    def getOpacity(self):
        return self._opacity

    def setOpacity(self, opacity):
        self._opacity = opacity

    def isClickable(self):
        return self._clickable

    def setClickable(self, clickable):
        self._clickable = clickable
