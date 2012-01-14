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

from muntjac.addon.google_maps.overlay.poly_overlay \
    import PolyOverlay


class Polygon(PolyOverlay):

    def __init__(self, Id, points, strokeColor='#ffffff', strokeWeight=1,
                strokeOpacity=1.0, fillColor='#777777', fillOpacity=0.2,
                clickable=False):
        super(Polygon, self).__init__(Id, points, strokeColor, strokeWeight,
                strokeOpacity, clickable)
        self._fillColor = fillColor
        self._fillOpacity = fillOpacity


    def getFillColor(self):
        return self._fillColor


    def setFillColor(self, fillColor):
        self._fillColor = fillColor


    def getFillOpacity(self):
        return self._fillOpacity


    def setFillOpacity(self, fillOpacity):
        self._fillOpacity = fillOpacity
