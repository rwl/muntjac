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

from pyjamas import DOM

from pyjamas.ui import Event

from pyjamas.ui.UIObject import UIObject


class Icon(UIObject):

    CLASSNAME = 'v-icon'

    def __init__(self, client, uidlUri=None):

        self._client = None
        self._myUri = None

        self.setElement(DOM.createImg())
        DOM.setElemAttribute(self.getElement(), 'alt', '')
        self.setStyleName(self.CLASSNAME)
        self._client = client
        client.addPngFix(self.getElement())

        if uidlUri is not None:
            self.setUri(uidlUri)


    def setUri(self, uidlUri):
        if uidlUri != self._myUri:
            # Start sinking onload events, widgets responsibility to react. We
            # must do this BEFORE we set src as IE fires the event immediately
            # if the image is found in cache (#2592).
            self.sinkEvents(Event.ONLOAD)
            uri = self._client.translateVaadinUri(uidlUri)
            DOM.setElemAttribute(self.getElement(), 'src', uri)
            self._myUri = uidlUri
