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

from com.vaadin.terminal.gwt.client.ui.VMediaBase import (VMediaBase,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
# from com.google.gwt.dom.client.AudioElement import (AudioElement,)


class VAudio(VMediaBase):
    _CLASSNAME = 'v-audio'
    _audio = None

    def __init__(self):
        self._audio = Document.get().createAudioElement()
        self.setMediaElement(self._audio)
        self.setStyleName(self._CLASSNAME)

    def updateFromUIDL(self, uidl, client):
        if client.updateComponent(self, uidl, True):
            return
        super(VAudio, self).updateFromUIDL(uidl, client)
        style = self._audio.getStyle()
        # Make sure that the controls are not clipped if visible.
        if (
            self.shouldShowControls(uidl) and (style.getHeight() is None) or ('' == style.getHeight())
        ):
            if BrowserInfo.get().isChrome():
                style.setHeight(32, Unit.PX)
            else:
                style.setHeight(25, Unit.PX)

    def getDefaultAltHtml(self):
        return 'Your browser does not support the <code>audio</code> element.'
