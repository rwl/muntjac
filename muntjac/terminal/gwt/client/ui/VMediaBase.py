# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
# from com.google.gwt.dom.client.MediaElement import (MediaElement,)


class VMediaBase(Widget, Paintable):
    ATTR_PAUSE = 'pause'
    ATTR_PLAY = 'play'
    ATTR_MUTED = 'muted'
    ATTR_CONTROLS = 'ctrl'
    ATTR_AUTOPLAY = 'auto'
    TAG_SOURCE = 'src'
    ATTR_RESOURCE = 'res'
    ATTR_RESOURCE_TYPE = 'type'
    ATTR_HTML = 'html'
    ATTR_ALT_TEXT = 'alt'
    _media = None
    client = None

    def setMediaElement(self, element):
        """Sets the MediaElement that is to receive all commands and properties.

        @param element
        """
        self.setElement(element)
        self._media = element

    def updateFromUIDL(self, uidl, client):
        if client.updateComponent(self, uidl, True):
            return
        self.client = client
        self._media.setControls(self.shouldShowControls(uidl))
        self._media.setAutoplay(self.shouldAutoplay(uidl))
        self._media.setMuted(self.isMediaMuted(uidl))
        # Add all sources
        _0 = True
        ix = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                ix += 1
            if not (ix < uidl.getChildCount()):
                break
            child = uidl.getChildUIDL(ix)
            if self.TAG_SOURCE == child.getTag():
                src = Document.get().createElement('source')
                src.setAttribute('src', self.getSourceUrl(child))
                src.setAttribute('type', self.getSourceType(child))
                self._media.appendChild(src)
        self.setAltText(uidl)
        self.evalPauseCommand(uidl)
        self.evalPlayCommand(uidl)

    def shouldShowControls(self, uidl):
        return uidl.getBooleanAttribute(self.ATTR_CONTROLS)

    def shouldAutoplay(self, uidl):
        return uidl.getBooleanAttribute(self.ATTR_AUTOPLAY)

    def isMediaMuted(self, uidl):
        return uidl.getBooleanAttribute(self.ATTR_MUTED)

    def getSourceUrl(self, uidl):
        """@param uidl
        @return the URL of a resource to be used as a source for the media
        """
        url = self.client.translateVaadinUri(uidl.getStringAttribute(self.ATTR_RESOURCE))
        if url is None:
            return ''
        return url

    def getSourceType(self, uidl):
        """@param uidl
        @return the mime type of the media
        """
        return uidl.getStringAttribute(self.ATTR_RESOURCE_TYPE)

    def setAltText(self, uidl):
        alt = uidl.getStringAttribute(self.ATTR_ALT_TEXT)
        if (alt is None) or ('' == alt):
            alt = self.getDefaultAltHtml()
        elif not self.allowHtmlContent(uidl):
            alt = Util.escapeHTML(alt)
        self._media.appendChild(Document.get().createTextNode(alt))

    def allowHtmlContent(self, uidl):
        return uidl.getBooleanAttribute(self.ATTR_HTML)

    def evalPlayCommand(self, uidl):
        if uidl.hasAttribute(self.ATTR_PLAY):
            self._media.play()

    def evalPauseCommand(self, uidl):
        if uidl.hasAttribute(self.ATTR_PAUSE):
            self._media.pause()

    def getDefaultAltHtml(self):
        """@return the default HTML to show users with browsers that do not support
                HTML5 media markup.
        """
        pass
