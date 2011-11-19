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

from muntjac.ui.abstract_media import AbstractMedia
from muntjac.terminal.gwt.client.ui.v_video import VVideo


class Video(AbstractMedia):
    """The Video component translates into an HTML5 C{<video>} element and as
    such is only supported in browsers that support HTML5 media markup.
    Browsers that do not support HTML5 display the text or HTML set by calling
    L{setAltText}.

    A flash-player fallback can be implemented by setting HTML content allowed
    (L{setHtmlContentAllowed} and calling L{setAltText} with the flash player
    markup. An example of flash fallback can be found at the <a href=
    "https://developer.mozilla.org/En/Using_audio_and_video_in_Firefox#Using_Flash"
    >Mozilla Developer Network</a>.

    Multiple sources can be specified. Which of the sources is used is selected
    by the browser depending on which file formats it supports. See <a
    href="http://en.wikipedia.org/wiki/HTML5_video#Table">wikipedia</a> for a
    table of formats supported by different browsers.

    @author: Vaadin Ltd
    @author: Richard Lincoln
    """

    CLIENT_WIDGET = None #CLientWidget(VVideo)

    def __init__(self, caption='', source=None):
        """@param caption:
                   The caption for this video.
        @param source:
                   The resource containing the video to play.
        """
        self._poster = None

        self.setCaption(caption)
        self.setSource(source)
        self.setShowControls(True)


    def setPoster(self, poster):
        """Sets the poster image, which is shown in place of the video before
        the user presses play.
        """
        self._poster = poster


    def getPoster(self):
        """@return The poster image."""
        return self._poster


    def paintContent(self, target):
        super(Video, self).paintContent(target)
        if self.getPoster() is not None:
            target.addAttribute(VVideo.ATTR_POSTER, self.getPoster())
