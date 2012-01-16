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

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from muntjac.addon.google_maps.overlay.marker_source \
    import IMarkerSource


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
            markerJSON.write(str(marker.getId()))

            markerJSON.write('\",\"lat\":')
            markerJSON.write(str(marker.getLatLng()[1]))

            markerJSON.write(',\"lng\":')
            markerJSON.write(str(marker.getLatLng()[0]))

            # Escape single and double quotes
            markerJSON.write(',\"title\":\"')
            markerJSON.write(marker.getTitle().replace('\'', "\\'").replace('\"', '\\\\\"'))

            markerJSON.write('\",\"visible\":')
            markerJSON.write('true' if marker.isVisible() else 'false')

            markerJSON.write(',\"info\":')
            markerJSON.write('true' if marker.getInfoWindowContent() is not None else 'false')

            markerJSON.write(',\"draggable\":')
            markerJSON.write('true' if marker.isDraggable() else 'false')

            if marker.getIconUrl() is not None:
                markerJSON.write(',\"icon\":\"')
                markerJSON.write(marker.getIconUrl() + '\"')

                if marker.getIconAnchor() is not None:
                    markerJSON.write(',\"iconAnchorX\":')
                    markerJSON.write(str(marker.getIconAnchor()[0]))

                    markerJSON.write(',\"iconAnchorY\":')
                    markerJSON.write(str(marker.getIconAnchor()[1]))
                else:
                    markerJSON.write(',\"iconAnchorX\":')
                    markerJSON.write(str(marker.getLatLng()[0]))

                    markerJSON.write(',\"iconAnchorY\":')
                    markerJSON.write(str(marker.getLatLng()[1]))

            markerJSON.write('}')

            if i != len(self._markers) - 1:
                markerJSON.write(',')

        try:
            json = ('[' + markerJSON.getvalue() + ']').encode('utf-8')
        except Exception:
            json = ('[' + markerJSON.getvalue() + ']').encode()

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
