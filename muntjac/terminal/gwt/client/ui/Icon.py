# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)


class Icon(UIObject):
    CLASSNAME = 'v-icon'
    _client = None
    _myUri = None

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            client, = _0
            self.setElement(DOM.createImg())
            DOM.setElementProperty(self.getElement(), 'alt', '')
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

            self.sinkEvents(Event.ONLOAD)
            uri = self._client.translateVaadinUri(uidlUri)
            DOM.setElementProperty(self.getElement(), 'src', uri)
            self._myUri = uidlUri
