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

from muntjac.addon.google_maps.overlay.info_window_tab import InfoWindowTab
from muntjac.addon.google_maps.overlay.marker import IMarker


class BasicMarker(IMarker):

    def __init__(self, Id, latLng, title):
        self._id = Id
        self._latLng = latLng
        self._title = title
        self._visible = True
        self._iconUrl = None
        self._iconAnchor = None
        self._infoWindowContent = None
        self._draggable = True


    def getId(self):
        return self._id


    def setId(self, Id):
        self._id = Id


    def isVisible(self):
        return self._visible


    def setVisible(self, visible):
        self._visible = visible


    def getLatLng(self):
        return self._latLng


    def setLatLng(self, latLng):
        self._latLng = latLng


    def getIconUrl(self):
        return self._iconUrl


    def setIconUrl(self, imageUrl):
        self._iconUrl = imageUrl


    def getIconAnchor(self):
        return self._iconAnchor


    def setIconAnchor(self, iconAnchor):
        self._iconAnchor = iconAnchor


    def getTitle(self):
        return self._title


    def setTitle(self, title):
        self._title = title


    def getInfoWindowContent(self):
        return self._infoWindowContent


    def setInfoWindowContent(self, tabs_or_parent, component=None):
        if component is None:
            tabs = tabs_or_parent
            self._infoWindowContent = tabs
        else:
            parent = tabs_or_parent
            self._infoWindowContent = [InfoWindowTab(parent, component)]


    def isDraggable(self):
        return self._draggable


    def setDraggable(self, draggable):
        self._draggable = draggable
