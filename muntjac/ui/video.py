# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

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
