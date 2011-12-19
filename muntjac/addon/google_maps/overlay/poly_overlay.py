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
