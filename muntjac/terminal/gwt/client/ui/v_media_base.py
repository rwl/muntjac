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

from pyjamas.ui.Widget import Widget

from muntjac.terminal.gwt.client.paintable import IPaintable
from muntjac.terminal.gwt.client.util import Util


class VMediaBase(Widget, IPaintable):

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

    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)

        self._media = None
        self.client = None


    def setMediaElement(self, element):
        """Sets the MediaElement that is to receive all commands and
        properties.
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
        for ix in range(uidl.getChildCount()):
            child = uidl.getChildUIDL(ix)
            if self.TAG_SOURCE == child.getTag():
                src = DOM.createElement('source')
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
        """@return: the URL of a resource to be used as a source for the media
        """
        url = self.client.translateVaadinUri(
                uidl.getStringAttribute(self.ATTR_RESOURCE))

        if url is None:
            return ''

        return url


    def getSourceType(self, uidl):
        """@return: the mime type of the media
        """
        return uidl.getStringAttribute(self.ATTR_RESOURCE_TYPE)


    def setAltText(self, uidl):
        alt = uidl.getStringAttribute(self.ATTR_ALT_TEXT)

        if (alt is None) or ('' == alt):
            alt = self.getDefaultAltHtml()
        elif not self.allowHtmlContent(uidl):
            alt = Util.escapeHTML(alt)

        self._media.appendChild(DOM.createTextNode(alt))


    def allowHtmlContent(self, uidl):
        return uidl.getBooleanAttribute(self.ATTR_HTML)


    def evalPlayCommand(self, uidl):
        if uidl.hasAttribute(self.ATTR_PLAY):
            self._media.play()


    def evalPauseCommand(self, uidl):
        if uidl.hasAttribute(self.ATTR_PAUSE):
            self._media.pause()


    def getDefaultAltHtml(self):
        """@return: the default HTML to show users with browsers that do not
                support HTML5 media markup.
        """
        pass
