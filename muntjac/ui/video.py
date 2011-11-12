# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.ui.AbstractMedia import (AbstractMedia,)
from com.vaadin.terminal.gwt.client.ui.VVideo import (VVideo,)


class Video(AbstractMedia):
    """The Video component translates into an HTML5 &lt;video&gt; element and as
    such is only supported in browsers that support HTML5 media markup. Browsers
    that do not support HTML5 display the text or HTML set by calling
    {@link #setAltText(String)}.

    A flash-player fallback can be implemented by setting HTML content allowed (
    {@link #setHtmlContentAllowed(boolean)} and calling
    {@link #setAltText(String)} with the flash player markup. An example of flash
    fallback can be found at the <a href=
    "https://developer.mozilla.org/En/Using_audio_and_video_in_Firefox#Using_Flash"
    >Mozilla Developer Network</a>.

    Multiple sources can be specified. Which of the sources is used is selected
    by the browser depending on which file formats it supports. See <a
    href="http://en.wikipedia.org/wiki/HTML5_video#Table">wikipedia</a> for a
    table of formats supported by different browsers.

    @author Vaadin Ltd
    @since 6.7.0
    """
    _poster = None

    def __init__(self, *args):
        """None
        ---
        @param caption
                   The caption for this video.
        ---
        @param caption
                   The caption for this video.
        @param source
                   The Resource containing the video to play.
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.__init__('', None)
        elif _1 == 1:
            caption, = _0
            self.__init__(caption, None)
        elif _1 == 2:
            caption, source = _0
            self.setCaption(caption)
            self.setSource(source)
            self.setShowControls(True)
        else:
            raise ARGERROR(0, 2)

    def setPoster(self, poster):
        """Sets the poster image, which is shown in place of the video before the
        user presses play.

        @param poster
        """
        self._poster = poster

    def getPoster(self):
        """@return The poster image."""
        return self._poster

    def paintContent(self, target):
        super(Video, self).paintContent(target)
        if self.getPoster() is not None:
            target.addAttribute(VVideo.ATTR_POSTER, self.getPoster())
