# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.ui.AbstractComponent import (AbstractComponent,)
from com.vaadin.terminal.gwt.client.ui.VMediaBase import (VMediaBase,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Arrays import (Arrays,)
# from java.util.Collections import (Collections,)
# from java.util.List import (List,)


class AbstractMedia(AbstractComponent):
    """Abstract base class for the HTML5 media components.

    @author Vaadin Ltd
    """
    _sources = list()
    _showControls = None
    _altText = None
    _htmlContentAllowed = None
    _autoplay = None
    _muted = None
    _pause = None
    _play = None

    def setSource(self, source):
        """Sets a single media file as the source of the media component.

        @param source
        """
        self._sources.clear()
        self.addSource(source)

    def addSource(self, source):
        """Adds an alternative media file to the sources list. Which of the sources
        is used is selected by the browser depending on which file formats it
        supports. See <a
        href="http://en.wikipedia.org/wiki/HTML5_video#Table">wikipedia</a> for a
        table of formats supported by different browsers.

        @param source
        """
        if source is not None:
            self._sources.add(source)
            self.requestRepaint()

    def setSources(self, *sources):
        """Set multiple sources at once. Which of the sources is used is selected by
        the browser depending on which file formats it supports. See <a
        href="http://en.wikipedia.org/wiki/HTML5_video#Table">wikipedia</a> for a
        table of formats supported by different browsers.

        @param sources
        """
        self._sources.addAll(Arrays.asList(sources))
        self.requestRepaint()

    def getSources(self):
        """@return The sources pointed to in this media."""
        return Collections.unmodifiableList(self._sources)

    def setShowControls(self, showControls):
        """Sets whether or not the browser should show native media controls.

        @param showControls
        """
        self._showControls = showControls
        self.requestRepaint()

    def isShowControls(self):
        """@return true if the browser is to show native media controls."""
        return self._showControls

    def setAltText(self, text):
        """Sets the alternative text to be displayed if the browser does not support
        HTML5. This text is rendered as HTML if
        {@link #setHtmlContentAllowed(boolean)} is set to true. With HTML
        rendering, this method can also be used to implement fallback to a
        flash-based player, see the <a href=
        "https://developer.mozilla.org/En/Using_audio_and_video_in_Firefox#Using_Flash"
        >Mozilla Developer Network</a> for details.

        @param text
        """
        self._altText = text
        self.requestRepaint()

    def getAltText(self):
        """@return The text/html that is displayed when a browser doesn't support
                HTML5.
        """
        return self._altText

    def setHtmlContentAllowed(self, htmlContentAllowed):
        """Set whether the alternative text ({@link #setAltText(String)}) is
        rendered as HTML or not.

        @param htmlContentAllowed
        """
        self._htmlContentAllowed = htmlContentAllowed
        self.requestRepaint()

    def isHtmlContentAllowed(self):
        """@return true if the alternative text ({@link #setAltText(String)}) is to
                be rendered as HTML.
        """
        return self._htmlContentAllowed

    def setAutoplay(self, autoplay):
        """Sets whether the media is to automatically start playback when enough
        data has been loaded.

        @param autoplay
        """
        self._autoplay = autoplay
        self.requestRepaint()

    def isAutoplay(self):
        """@return true if the media is set to automatically start playback."""
        return self._autoplay

    def setMuted(self, muted):
        """Set whether to mute the audio or not.

        @param muted
        """
        self._muted = muted
        self.requestRepaint()

    def isMuted(self):
        """@return true if the audio is muted."""
        return self._muted

    def pause(self):
        """Pauses the media."""
        # cancel any possible play command
        self._play = False
        self._pause = True
        self.requestRepaint()

    def play(self):
        """Starts playback of the media."""
        # cancel any possible pause command.
        self._pause = False
        self._play = True
        self.requestRepaint()

    def paintContent(self, target):
        super(AbstractMedia, self).paintContent(target)
        target.addAttribute(VMediaBase.ATTR_CONTROLS, self.isShowControls())
        if self.getAltText() is not None:
            target.addAttribute(VMediaBase.ATTR_ALT_TEXT, self.getAltText())
        target.addAttribute(VMediaBase.ATTR_HTML, self.isHtmlContentAllowed())
        target.addAttribute(VMediaBase.ATTR_AUTOPLAY, self.isAutoplay())
        for r in self.getSources():
            target.startTag(VMediaBase.TAG_SOURCE)
            target.addAttribute(VMediaBase.ATTR_RESOURCE, r)
            target.addAttribute(VMediaBase.ATTR_RESOURCE_TYPE, r.getMIMEType())
            target.endTag(VMediaBase.TAG_SOURCE)
        target.addAttribute(VMediaBase.ATTR_MUTED, self.isMuted())
        if self._play:
            target.addAttribute(VMediaBase.ATTR_PLAY, True)
            self._play = False
        if self._pause:
            target.addAttribute(VMediaBase.ATTR_PAUSE, True)
            self._pause = False
