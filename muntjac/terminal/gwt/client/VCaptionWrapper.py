# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.VCaption import (VCaption,)


class VCaptionWrapper(FlowPanel):
    CLASSNAME = 'v-captionwrapper'
    _caption = None
    _widget = None

    def __init__(self, toBeWrapped, client):
        self._caption = VCaption(toBeWrapped, client)
        self.add(self._caption)
        self._widget = toBeWrapped
        self.add(self._widget)
        self.setStyleName(self.CLASSNAME)

    def updateCaption(self, uidl):
        self._caption.updateCaption(uidl)
        self.setVisible(not uidl.getBooleanAttribute('invisible'))

    def getPaintable(self):
        return self._widget
