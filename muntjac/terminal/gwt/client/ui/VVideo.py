# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.VMediaBase import (VMediaBase,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
# from com.google.gwt.dom.client.VideoElement import (VideoElement,)


class VVideo(VMediaBase):
    ATTR_POSTER = 'poster'
    _CLASSNAME = 'v-video'
    _video = None

    def __init__(self):
        self._video = Document.get().createVideoElement()
        self.setMediaElement(self._video)
        self.setStyleName(self._CLASSNAME)
        self.updateDimensionsWhenMetadataLoaded(self.getElement())

    def updateFromUIDL(self, uidl, client):
        if client.updateComponent(self, uidl, True):
            return
        super(VVideo, self).updateFromUIDL(uidl, client)
        self.setPosterFromUIDL(uidl)

    def setPosterFromUIDL(self, uidl):
        if uidl.hasAttribute(self.ATTR_POSTER):
            self._video.setPoster(self.client.translateVaadinUri(uidl.getStringAttribute(self.ATTR_POSTER)))

    def updateDimensionsWhenMetadataLoaded(self, el):
        """Registers a listener that updates the dimensions of the widget when the
        video metadata has been loaded.

        @param el
        """
        JS("""
              var self = @{{self}};
              @{{el}}.addEventListener('loadedmetadata', function(e) {
                  $entry(self.@com.vaadin.terminal.gwt.client.ui.VVideo::updateElementDynamicSize(II)(@{{el}}.videoWidth, @{{el}}.videoHeight));
              }, false);

    """)
        pass

    def updateElementDynamicSize(self, w, h):
        """Updates the dimensions of the widget.

        @param w
        @param h
        """
        self._video.getStyle().setWidth(w, Unit.PX)
        self._video.getStyle().setHeight(h, Unit.PX)
        Util.notifyParentOfSizeChange(self, True)

    def getDefaultAltHtml(self):
        return 'Your browser does not support the <code>video</code> element.'
