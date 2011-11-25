# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
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
