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

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

from muntjac.addon.google_maps.overlay.marker_source import IMarkerSource


class BasicMarkerSource(IMarkerSource):

    def __init__(self):
        super(BasicMarkerSource, self).__init__()
        self._markers = list()


    def getMarkers(self):
        return self._markers


    def addMarker(self, newMarker):
        if newMarker in self._markers:
            return False
        self._markers.append(newMarker)
        return True


    def getMarkerJSON(self):
        markerJSON = StringIO()

        for i, marker in enumerate(self._markers):
            markerJSON.write('{\"mid\":\"')
            markerJSON.write(marker.getId())

            markerJSON.write('\",\"lat\":')
            markerJSON.write(marker.getLatLng().y)

            markerJSON.write(',\"lng\":')
            markerJSON.write(marker.getLatLng().x)

            # Escape single and double quotes
            markerJSON.write(',\"title\":\"')
            markerJSON.write(marker.getTitle().replace('\'', "\\'").replace('\"', '\\\\\"'))

            markerJSON.write('\",\"visible\":')
            markerJSON.write(marker.isVisible())

            markerJSON.write(',\"info\":')
            markerJSON.write(marker.getInfoWindowContent() is not None)

            markerJSON.write(',\"draggable\":')
            markerJSON.write(marker.isDraggable())

            if marker.getIconUrl() is not None:
                markerJSON.write(',\"icon\":\"')
                markerJSON.write(marker.getIconUrl() + '\"')

                if marker.getIconAnchor() is not None:
                    markerJSON.write(',\"iconAnchorX\":')
                    markerJSON.write(marker.getIconAnchor().x)

                    markerJSON.write(',\"iconAnchorY\":')
                    markerJSON.write(marker.getIconAnchor().y)
                else:
                    markerJSON.write(',\"iconAnchorX\":')
                    markerJSON.write(marker.getLatLng().x)

                    markerJSON.write(',\"iconAnchorY\":')
                    markerJSON.write(marker.getLatLng().y)

            markerJSON.write('}')

            if i != len(self._markers) - 1:
                markerJSON.write(',')

        try:
            json = ('[' + markerJSON + ']').encode('utf-8')
        except Exception:
            json = ('[' + markerJSON + ']').encode()

        markerJSON.close()

        return json


    def registerEvents(self, map_):
        # This marker source implementation is not interested in map events
        pass


    def getMarker(self, markerId):
        # TODO: The marker collection should be a map...
        for marker in self._markers:
            if str(marker.getId()) == markerId:
                return marker
        return None
