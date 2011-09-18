# Copyright (C) 2011 Vaadin Ltd
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

from __pyjamas__ import (ARGERROR,)
# from com.google.gwt.user.client.ui.UIObject import (UIObject,)


class Icon(UIObject):
    CLASSNAME = 'v-icon'
    _client = None
    _myUri = None

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            client, = _0
            self.setElement(self.DOM.createImg())
            self.DOM.setElementProperty(self.getElement(), 'alt', '')
            self.setStyleName(self.CLASSNAME)
            self._client = client
            client.addPngFix(self.getElement())
        elif _1 == 2:
            client, uidlUri = _0
            self.__init__(client)
            self.setUri(uidlUri)
        else:
            raise ARGERROR(1, 2)

    def setUri(self, uidlUri):
        if not (uidlUri == self._myUri):
            # Start sinking onload events, widgets responsibility to react. We
            # must do this BEFORE we set src as IE fires the event immediately
            # if the image is found in cache (#2592).

            self.sinkEvents(self.Event.ONLOAD)
            uri = self._client.translateVaadinUri(uidlUri)
            self.DOM.setElementProperty(self.getElement(), 'src', uri)
            self._myUri = uidlUri
