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

from muntjac.addon.google_maps.overlay.info_window_tab \
    import InfoWindowTab

from muntjac.addon.google_maps.overlay.marker \
    import IMarker


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
