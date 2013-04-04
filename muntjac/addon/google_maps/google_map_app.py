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

from random \
    import random, randint, getrandbits

from muntjac.api \
    import Application, Window, Label, GridLayout, Button

from muntjac.ui.button \
    import IClickListener

from muntjac.ui.window \
    import Notification

from muntjac.addon.google_maps.google_map \
    import GoogleMap, MapControl, IMarkerClickListener, \
    IMarkerMovedListener, IMapMoveListener

from muntjac.addon.google_maps.overlay.basic_marker \
    import BasicMarker

from muntjac.addon.google_maps.overlay.polygon \
    import Polygon


class GoogleMapWidgetApp(Application):

    def init(self):
#        super(GoogleMapWidgetApp, self).__init__()

        self.setMainWindow(Window('Google Map add-on demo'))

        # Create a new map instance centered on the IT Mill offices
        self._googleMap = GoogleMap(self, (22.3, 60.4522), 8)

        self._googleMap.setWidth('640px')
        self._googleMap.setHeight('480px')

        # Create a marker at the IT Mill offices
        self._mark1 = BasicMarker(1L, (22.3, 60.4522), 'Test marker 1')
        self._mark2 = BasicMarker(2L, (22.4, 60.4522), 'Test marker 2')
        self._mark3 = BasicMarker(4L, (22.6, 60.4522), 'Test marker 3')
        self._mark4 = BasicMarker(5L, (22.7, 60.4522), 'Test marker 4')

        l = MarkerClickListener(self)
        self._googleMap.addListener(l, IMarkerClickListener)

        # Marker with information window pupup
        self._mark5 = BasicMarker(6L, (22.8, 60.4522), 'Marker 5')
        self._mark5.setInfoWindowContent(self._googleMap,
                Label('Hello Marker 5!'))

        content = Label('Hello Marker 2!')
        content.setWidth('60px')
        self._mark2.setInfoWindowContent(self._googleMap, content)

        self._googleMap.addMarker(self._mark1)
        self._googleMap.addMarker(self._mark2)
        self._googleMap.addMarker(self._mark3)
        self._googleMap.addMarker(self._mark4)
        self._googleMap.addMarker(self._mark5)
        self.getMainWindow().getContent().addComponent(self._googleMap)

        # Add a Marker click listener to catch marker click events.
        # Note, works only if marker has information window content
        l = MarkerClickListener2(self)
        self._googleMap.addListener(l, IMarkerClickListener)

        # Add a MarkerMovedListener to catch events when a marker is dragged to
        # a new location
        l = MarkerMovedListener(self)
        self._googleMap.addListener(l, IMarkerMovedListener)

        l = MapMoveListener(self)
        self._googleMap.addListener(l, IMapMoveListener)

        self._googleMap.addControl(MapControl.MapTypeControl)

        self.addTestButtons()  # Add buttons that trigger tests map features


    def addTestButtons(self):
        grid = GridLayout(4, 1)
        grid.setSpacing(True)
        self.getMainWindow().addComponent(grid)

        l = DraggabilityClickListener(self)
        grid.addComponent(Button('Toggle marker 3 draggability', l))

        l = VisibilityClickListener(self)
        grid.addComponent(Button('Toggle marker 4 visibility', l))

        l = RandomizeClickListener(self)
        grid.addComponent(Button('Randomize Marker 5 location', l))

        l = UpdateClickListener(self)
        grid.addComponent(Button('Update marker 5 title', l))

        l = RemoveClickListener(self)
        grid.addComponent(Button('Remove \"Test marker2\"', l))

        l = AddClickListener(self)
        grid.addComponent(Button('Add \"Test marker2\"', l))

        l = ToggleMarkerClickListener(self)
        grid.addComponent(Button('Toggle marker 1 icon', l))

        l = ToggleLoggingClickListener(self)
        grid.addComponent(Button('Toggle client logging', l))

        # Popup test
        l = PopupClickListener(self)
        grid.addComponent(Button('Open a map in a popup', l))

        l = ResizeClickListener(self)
        grid.addComponent(Button('Resize map', l))

        l = DrawClickListener(self)
        grid.addComponent(Button('Draw polygon', l))

        l = RemovePolygonClickListener(self)
        grid.addComponent(Button('Remove first polygon', l))


class _MapListener(object):

    def __init__(self, app):
        self._app = app


class MarkerClickListener(_MapListener, IMarkerClickListener):

    def markerClicked(self, clickedMarker):
        if (clickedMarker.getIconUrl() is not None
                and 'green' in clickedMarker.getIconUrl()):
            clickedMarker.setIconUrl('VAADIN/themes/reindeer/icon/red.png')
        else:
            clickedMarker.setIconUrl('VAADIN/themes/reindeer/icon/green.png')
        self._app._googleMap.requestRepaint()


class MarkerClickListener2(_MapListener, IMarkerClickListener):

    def markerClicked(self, clickedMarker):
        self._app.getMainWindow().showNotification('Marker '
                + clickedMarker.getTitle() + ' clicked',
                Notification.TYPE_TRAY_NOTIFICATION)


class MarkerMovedListener(_MapListener, IMarkerMovedListener):

    def markerMoved(self, movedMarker):
        self._app.getMainWindow().showNotification('Marker '
                + movedMarker.getTitle() + ' moved to '
                + str(movedMarker.getLatLng()),
                Notification.TYPE_TRAY_NOTIFICATION)


class MapMoveListener(_MapListener, IMapMoveListener):

    def mapMoved(self, newZoomLevel, newCenter, boundsNE, boundsSW):
        self._app.getMainWindow().showNotification('Zoom ' + str(newZoomLevel)
                + ' center ' + str(newCenter) + ' bounds ' + str(boundsNE)
                + '/' + str(boundsSW), Notification.TYPE_TRAY_NOTIFICATION)


class DraggabilityClickListener(_MapListener, IClickListener):

    def buttonClick(self, event):
        self._app._mark3.setDraggable(not self._app._mark3.isDraggable())
        self._app._googleMap.requestRepaint()


class VisibilityClickListener(_MapListener, IClickListener):

    def buttonClick(self, event):
        self._app._mark4.setVisible(not self._app._mark4.isVisible())
        self._app._googleMap.requestRepaint()


class RandomizeClickListener(_MapListener, IClickListener):

    def buttonClick(self, event):
        self._app._mark5.setLatLng((22.8 + (random() / 10),
                60.4522 + (random() / 10)))
        self._app._googleMap.requestRepaint()


class UpdateClickListener(_MapListener, IClickListener):

    def buttonClick(self, event):
        chars = str('.*^"\'')
        self._app._mark5.setTitle(self._app._mark5.getTitle()
                + chars[randint(0, len(chars) - 1)])
        self._app._googleMap.requestRepaint()


class RemoveClickListener(_MapListener, IClickListener):

    def buttonClick(self, event):
        self._app._googleMap.removeMarker(self._app._mark2)


class AddClickListener(_MapListener, IClickListener):

    def buttonClick(self, event):
        self._app._googleMap.addMarker(self._app._mark2)


class ToggleMarkerClickListener(_MapListener, IClickListener):

    def buttonClick(self, event):
        if self._app._mark1.getIconUrl() is None:
            self._app._mark1.setIconUrl(
                    'http://bits.ohloh.net/attachments/18966/v_med.gif')
            self._app._mark1.setIconAnchor(None)
        elif self._app._mark1.getIconAnchor() is None:
            self._app._mark1.setIconAnchor((-20, -20))
        else:
            self._app._mark1.setIconUrl(None)
            self._app._mark1.setIconAnchor(None)
        self._app._googleMap.requestRepaint()


class ToggleLoggingClickListener(_MapListener, IClickListener):

    def buttonClick(self, event):
        if self._app._googleMap.getClientLogLevel() == 0:
            self._app._googleMap.setClientLogLevel(1)
            self._app.getMainWindow().showNotification(
                    'Client logging enabled',
                    Notification.TYPE_TRAY_NOTIFICATION)
        else:
            self._app._googleMap.setClientLogLevel(0)
            self._app.getMainWindow().showNotification(
                    'Client logging disabled',
                    Notification.TYPE_TRAY_NOTIFICATION)


class PopupClickListener(_MapListener, IClickListener):

    def buttonClick(self, event):
        app = self._app#event.getButton().getApplication()

        map2 = GoogleMap(app, (22.3, 60.4522), 8)
        map2.setHeight('240px')
        map2.setWidth('240px')

        w = Window('popup')
        w.addComponent(map2)
        w.setHeight('300px')
        w.setWidth('300px')
        app.getMainWindow().addWindow(w)


class ResizeClickListener(_MapListener, IClickListener):

    def buttonClick(self, event):
        if self._app._googleMap.getHeight() == 200:
            self._app._googleMap.setWidth('640px')
            self._app._googleMap.setHeight('480px')
        else:
            self._app._googleMap.setHeight('200px')
            self._app._googleMap.setWidth('200px')


class DrawClickListener(_MapListener, IClickListener):

    def buttonClick(self, event):
        # Location of Vaadin Ltd offices
        c = (22.3, 60.4522)
        delta = 0.75
        corners = [(c[0] - delta, c[1] + delta), (c[0] + delta, c[1] + delta),
                   (c[0] + delta, c[1] - delta), (c[0] - delta, c[1] - delta),
                   (c[0] - delta, c[1] + delta)]
        poly = Polygon(getrandbits(48), corners, '#f04040', 5, 0.8,
                '#1010ff', 0.2, False)
        self._app._googleMap.addPolyOverlay(poly)


class RemovePolygonClickListener(_MapListener, IClickListener):

    def buttonClick(self, event):
        overlays = self._app._googleMap.getOverlays()
        if len(overlays) > 0:
            self._app._googleMap.removeOverlay(overlays[-1])
            self._app.getMainWindow().showNotification('Overlay removed',
                    Notification.TYPE_TRAY_NOTIFICATION)
        else:
            self._app.getMainWindow().showNotification('No overlays to remove',
                    Notification.TYPE_TRAY_NOTIFICATION)


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(GoogleMapWidgetApp, nogui=True, forever=True, debug=True)
