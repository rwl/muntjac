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
except ImportError:
    from StringIO import StringIO

from muntjac.ui.abstract_component \
    import AbstractComponent

from muntjac.terminal.download_stream \
    import DownloadStream

from muntjac.addon.google_maps.overlay.polygon \
    import Polygon

from muntjac.addon.google_maps.overlay.basic_marker_source \
    import BasicMarkerSource


class MapControl(object):

    SmallMapControl = 'SmallMapControl'
    HierarchicalMapTypeControl = 'HierarchicalMapTypeControl'
    LargeMapControl = 'LargeMapControl'
    MapTypeControl = 'MapTypeControl'
    MenuMapTypeControl = 'MenuMapTypeControl'
    OverviewMapControl = 'OverviewMapControl'
    ScaleControl = 'ScaleControl'
    SmallZoomControl = 'SmallZoomControl'


class GoogleMap(AbstractComponent):
    """Server side component for the VGoogleMap widget."""

    def __init__(self, application, apiKey_or_center=None, zoom=None,
                apiKey=None):
        """Construct a new instance of the map with given parameters.

        @param application:
                   L{Application} owning this instance.
        @param apiKey_or_center:
                   the API key to be used for Google Maps or the center of
                   the map as a 2-tuple
        @param zoom:
                   initial zoom level of the map
        @param apiKey:
                   the API key to be used for Google Maps
        """
        self._center = None

        self._boundsNE = None

        self._boundsSW = None

        self._zoom = None

        self._moveListeners = list()

        self._mapClickListeners = list()

        self._markerListeners = list()

        self._markerMovedListeners = list()

        self._markerSource = None

        self._clickedMarker = None

        self._closeInfoWindow = False

        self._overlays = dict()

        self._scrollWheelZoomEnabled = True

        self._clearMapTypes = False

        self._controls = list()

        self._mapTypes = list()

        self._mapTypesChanged = False

        self._reportMapBounds = False

        self._markerResource = \
                MarkerApplicationResource(self, self._markerSource)

        self._apiKey = ''
        self._clientLogLevel = 0

        application.addResource(self.markerResource)

        if apiKey_or_center is None:
            # Greewich Royal Observatory
            self._center = (-0.001475, 51.477811)
            self._zoom = 14
        elif zoom is None:
            self._apiKey = apiKey_or_center
            # Greewich Royal Observatory
            self._center = (-0.001475, 51.477811)
            self._zoom = 14
        elif apiKey is None:
            self._center = apiKey_or_center
            self._zoom = zoom
        else:
            self._apiKey = apiKey
            self._center = apiKey_or_center
            self._zoom = zoom


    def paintContent(self, target):
        super(GoogleMap, self).paintContent(target)
        target.addVariable(self, 'center_lat', self._center.y)
        target.addVariable(self, 'center_lng', self._center.x)
        target.addVariable(self, 'zoom', self._zoom)
        target.addVariable(self, 'swze', self._scrollWheelZoomEnabled)
        target.addAttribute('apikey', self._apiKey)
        target.addAttribute('loglevel', self._clientLogLevel)

        for control in self._controls:
            target.addAttribute(control.name(), True)

        # TODO: this feels like a kludge, but unsure how to implement correctly
        if self._clickedMarker is not None:
            target.addAttribute('marker', str(self._clickedMarker.getId()))
            target.startTag('tabs')
            tabs = self._clickedMarker.getInfoWindowContent()
            for i in range(len(tabs)):
                target.startTag('tab')
                if len(tabs) > 1:
                    target.addAttribute('selected', tabs[i].isSelected())
                    target.addAttribute('label', tabs[i].getLabel())

                tabs[i].getContent().paint(target)

                target.endTag('tab')

            target.endTag('tabs')

            self._clickedMarker = None
        elif self._markerSource is not None:
            target.addAttribute('markerRes', self.markerResource)

        if self._closeInfoWindow:
            target.addAttribute('closeInfoWindow', True)
            self._closeInfoWindow = False

        target.startTag('overlays')

        for poly in self._overlays.values():
            target.startTag('o')
            target.addAttribute('id', poly.getId())

            # Encode polyline points as a string attribute
            sb = StringIO()
            points = poly.getPoints()
            for i in range(len(points)):
                if i > 0:
                    sb.write(' ')
                sb.write('' + points[i][1] + ',' + points[i][0])

            target.addAttribute('points', sb.getvalue())
            sb.close()

            target.addAttribute('color', poly.getColor())
            target.addAttribute('weight', poly.getWeight())
            target.addAttribute('opacity', poly.getOpacity())
            target.addAttribute('clickable', poly.isClickable())

            if isinstance(poly, Polygon):
                polygon = poly
                target.addAttribute('fillcolor', polygon.getFillColor())
                target.addAttribute('fillopacity', polygon.getFillOpacity())

            target.endTag('o')

        target.endTag('overlays')

        if self._clearMapTypes:
            target.addAttribute('clearMapTypes', True)
            self._clearMapTypes = False

        if self._mapTypesChanged:
            target.startTag('mapTypes')

            for mapType in self._mapTypes:
                mapType.paintContent(target)

            target.endTag('mapTypes')

            self._mapTypesChanged = False

        if self._reportMapBounds:
            target.addAttribute('reportBounds', True)
            self._reportMapBounds = False


    def changeVariables(self, source, variables):
        """Receive and handle events and other variable changes from the
        client.
        """
        super(GoogleMap, self).changeVariables(source, variables)

        if 'click_pos' in variables:
            self.fireClickEvent(variables.get('click_pos'))
            self.requestRepaint()

        moveEvent = False
        intVar = variables['zoom']
        if intVar is not None:
            self._zoom = intVar
            moveEvent = True

        stringVar = variables.get('center')
        if stringVar is not None and not (stringVar.trim() == ''):
            self._center = GoogleMap.strToLL(stringVar)
            moveEvent = True

        stringVar = variables.get('bounds_ne')
        if stringVar is not None and not (stringVar.trim() == ''):
            self._boundsNE = GoogleMap.strToLL(stringVar)
            moveEvent = True

        stringVar = variables.get('bounds_sw')
        if stringVar is not None and not (stringVar.trim() == ''):
            self._boundsSW = GoogleMap.strToLL(stringVar)
            moveEvent = True

        if moveEvent:
            self.fireMoveEvent()

        if 'marker' in variables:
            self._clickedMarker = self._markerSource.getMarker(
                    str(variables['marker']))
            if self._clickedMarker is not None:
                self.fireMarkerClickedEvent(self._clickedMarker)
                if self._clickedMarker.getInfoWindowContent() is not None:
                    self.requestRepaint()

        if 'markerMovedId' in variables:
            markerID = str(variables['markerMovedId']).replace('\"', '')
            markers = self._markerSource.getMarkers()

            for mark in markers:
                if mark.getId() == int(markerID):

                    lat = float(str(variables['markerMovedLat']))
                    lng = float(str(variables['markerMovedLong']))
                    mark.getLatLng().setLocation(lng, lat)

                    self.fireMarkerMovedEvent(mark)
                    break


    def fireMoveEvent(self):
        for listener in self._moveListeners:
            listener.mapMoved(self._zoom, self._center, self._boundsNE,
                    self._boundsSW)


    def fireClickEvent(self, obj):
        clickPos = GoogleMap.strToLL(str(obj))
        for listener in self._mapClickListeners:
            listener.mapClicked(clickPos)


    def fireMarkerClickedEvent(self, clickedMarker):
        for m in self._markerListeners:
            m.markerClicked(clickedMarker)


    def fireMarkerMovedEvent(self, movedMarker):
        for m in self._markerMovedListeners:
            m.markerMoved(movedMarker)



    def addListener(self, listener, iface=None):
        """Register a new map listener.

        @param listener:
                   new L{IMapClickListener}, L{IMapMoveListener},
                   L{IMarkerMovedListener} or L{IMarkerClickListener}
                   to register

        NOTE!! The marker that is clicked MUST have some information window
        content! This is due to the implementation of the Widget, as the marker
        click events do not propagate if there is not a information window
        opened.
        """
        if isinstance(listener, MapClickListener):
            if not self._mapClickListeners.contains(listener):
                self._mapClickListeners.add(listener)
        elif isinstance(listener, MapMoveListener):
            if not self._moveListeners.contains(listener):
                self._moveListeners.add(listener)
        elif isinstance(listener, MarkerClickListener):
            if not self._markerListeners.contains(listener):
                self._markerListeners.add(listener)
        else:
            if not self._markerMovedListeners.contains(listener):
                self._markerMovedListeners.add(listener)


    def removeListener(self, listener, iface=None):
        """Remove a map listener.

        @param listener:
                   L{IMapClickListener}, L{IMapMoveListener},
                   L{IMarkerMovedListener} or L{IMarkerClickListener}
                   to remove
        """
        if isinstance(listener, MapClickListener):
            if self._mapClickListeners.contains(listener):
                self._mapClickListeners.remove(listener)
        elif isinstance(listener, MapMoveListener):
            if self._moveListeners.contains(listener):
                self._moveListeners.remove(listener)
        elif isinstance(listener, MarkerClickListener):
            if self._markerListeners.contains(listener):
                self._markerListeners.remove(listener)
        else:
            if self._markerMovedListeners.contains(listener):
                self._markerMovedListeners.remove(listener)


    def getCenter(self):
        """Get current center coordinates of the map.
        """
        return self._center


    def setCenter(self, center):
        """Set the current center coordinates of the map. This method can be
        used to pan the map programmatically.

        @param center:
                   the new center coordinates
        """
        self._center = center
        self.requestRepaint()


    def getZoom(self):
        """Get the current zoom level of the map.

        @return: the current zoom level
        """
        return self._zoom


    def setZoom(self, zoom):
        """Set the zoom level of the map. This method can be used to zoom the
        map programmatically.
        """
        self._zoom = zoom
        self.requestRepaint()


    def setClientLogLevel(self, level):
        """Set the level of verbosity the client side uses for tracing or
        displaying error messages.
        """
        self._clientLogLevel = level
        self.requestRepaint()


    def getClientLogLevel(self):
        """Get the level of verbosity the client side uses for tracing or
        displaying error messages.
        """
        return self._clientLogLevel


    def getBoundsNE(self):
        """Get the coordinates of the north-east corner of the map.
        """
        return self._boundsNE


    def getBoundsSW(self):
        """Get the coordinates of the south-west corner of the map.
        """
        return self._boundsSW


    def setMarkerSource(self, markerSource):
        """Set the L{MarkerSource} for the map.
        """
        self._markerSource = markerSource


    def closeInfoWindow(self):
        """Close the currently open info window, if any."""
        self._closeInfoWindow = True
        self.requestRepaint()


    def addPolyOverlay(self, overlay):
        """Add a new {@link PolyOverlay} to the map. Does nothing if the
        overlay already exist on the map.

        @param overlay:
                   L{PolyOverlay} to add

        @return: True if the overlay was added.
        """
        if not (overlay.getId() in self._overlays):
            self._overlays[overlay.getId()] = overlay
            self.requestRepaint()
            return True
        return False


    def updateOverlay(self, overlay):
        """Update a L{PolyOverlay} on the map. Does nothing if the overlay
        does not exist on the map.

        @param overlay:
                   L{PolyOverlay} to update

        @return: True if the overlay was updated.
        """
        if overlay.getId() in self._overlays:
            self._overlays[overlay.getId()] = overlay
            self.requestRepaint()
            return True
        return False


    def removeOverlay(self, overlay):
        """Remove a L{PolyOverlay} from the map. Does nothing if the overlay
        does not exist on the map.

        @param overlay:
                   L{PolyOverlay} to remove

        @return: True if the overlay was removed.
        """
        if overlay.getId() in self._overlays:
            del self._overlays[overlay.getId()]
            self.requestRepaint()
            return True
        return False


    def getOverlays(self):
        """Get the collection of L{PolyOverlay}s currently in the map.

        @return: a list of overlays.
        """
        return self._overlays.values()


    @classmethod
    def strToLL(cls, latLngStr):
        if latLngStr is None:
            return None

        nums = latLngStr.split(', ')
        if len(nums) != 2:
            return None

        lat = float(nums[0][1:])
        lng = float(nums[1][:len(nums[1]) - 1])
        return (lng, lat)


    def addMarker(self, marker):
        """Add a Marker to the current MarkerSource. If the map has no marker
        source a new L{BasicMarkerSource} is created.

        @param marker:
                   Marker to add
        """
        if self._markerSource is None:
            self._markerSource = BasicMarkerSource()
        self._markerSource.addMarker(marker)
        self.requestRepaint()


    def removeMarker(self, marker):
        """Removes the marker from the map
        """
        if self._markerSource is not None:
            self._markerSource.getMarkers().remove(marker)
            self.requestRepaint()


    def removeAllMarkers(self):
        if self._markerSource is not None:
            self._markerSource.getMarkers().clear()
            self.requestRepaint()


    def setScrollWheelZoomEnabled(self, isEnabled):
        self._scrollWheelZoomEnabled = isEnabled


    def isScrollWheelZoomEnabled(self):
        return self._scrollWheelZoomEnabled


    def addControl(self, control):
        if control not in self._controls:
            self._controls.append(control)
            return True
        return False


    def hasControl(self, control):
        return control in self._controls


    def removeControl(self, control):
        if control in self._controls:
            self._controls.remove(control)
            return True
        return False


    def addMapType(self, name, minZoom, maxZoom, copyright, tileUrl, isPng,
                opacity):
        self._mapTypes.append(CustomMapType(name, minZoom, maxZoom, copyright,
                tileUrl, isPng, opacity))
        self._mapTypesChanged = True
        self.requestRepaint()


    def clearMapTypes(self):
        self._mapTypes.clear()
        self._clearMapTypes = True
        self.requestRepaint()


    def reportMapBounds(self):
        self._reportMapBounds = True
        self.requestRepaint()


class MarkerApplicationResource(ApplicationResource):

    def __init__(self, gmap, markerSource):
        self._gmap = gmap
        self._markerSource = markerSource

    def getApplication(self):
        return self._gmap.getApplication()

    def getBufferSize(self):
        return len(self._markerSource.getMarkerJSON())

    def getCacheTime(self):
        return -1

    def getFilename(self):
        return "markersource.txt"

    def getStream(self):
        return DownloadStream(StringIO(self._markerSource.getMarkerJSON()),
                self.getMIMEType(), self.getFilename())

    def getMIMEType(self):
        return "text/plain"



class IMapMoveListener(object):
    """Interface for listening map move and zoom events.

    @author: Henri Muurimaa
    @author: Richard Lincoln
    """

    def mapMoved(self, newZoomLevel, newCenter, boundsNE, boundsSW):
        """Handle a MapMoveEvent.

        @param newZoomLevel:
                   New zoom level
        @param newCenter:
                   New center coordinates
        @param boundsNE:
                   Coordinates of the north-east corner of the map
        @param boundsSW:
                   Coordinates of the south-west corner of the map
        """
        raise NotImplementedError


class IMapClickListener(object):
    """Interface for listening map click events.

    @author Henri Muurimaa
    """

    def mapClicked(self, clickPos):
        """Handle a MapClickEvent.

        @param clickPos:
                   coordinates of the click event.
        """
        raise NotImplementedError


class IMarkerClickListener(object):
    """Interface for listening marker click events.
    """

    def markerClicked(self, clickedMarker):
        """Handle a MarkerClickEvent.

        @param clickedMarker:
                   the marker that was clicked.
        """
        raise NotImplementedError


class IMarkerMovedListener(object):
    """Interface for listening marker move events.
    """

    def markerMoved(self, movedMarker):
        """Handle a MarkerMovedEvent.

        @param movedMarker:
                   the marker that was moved.
        """
        raise NotImplementedError


class CustomMapType(object):

    def __init__(self, name, minZoom, maxZoom, copyright, tileUrl, isPng,
                opacity):
        self._name = name
        self._minZoom = minZoom
        self._maxZoom = maxZoom
        self._copyright = copyright
        self._tileUrl = tileUrl
        self._isPng = isPng
        self._opacity = opacity


    def paintContent(self, target):
        target.startTag('maptype')
        target.addAttribute('name', self._name)
        target.addAttribute('minZoom', self._minZoom)
        target.addAttribute('maxZoom', self._maxZoom)
        target.addAttribute('copyright', self._copyright)
        target.addAttribute('tileUrl', self._tileUrl)
        target.addAttribute('isPng', self._isPng)
        target.addAttribute('opacity', self._opacity)
        target.endTag('maptype')


    def getOpacity(self):
        return self._opacity


    def getTileUrl(self):
        return self._tileUrl


    def isPng(self):
        return self._isPng


    def getMinZoom(self):
        return self._minZoom


    def getMaxZoom(self):
        return self._maxZoom


    def getCopyright(self):
        return self._copyright
