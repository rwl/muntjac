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

"""Defines an interface implemented by all visual objects that can be
scrolled."""


class IScrollable(object):
    """This interface is implemented by all visual objects that can be
    scrolled programmatically from the server-side, or for which it is
    possible to know the scroll position on the server-side.. The unit
    of scrolling is pixel.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def getScrollLeft(self):
        """Gets scroll left offset.

        Scrolling offset is the number of pixels this scrollable has been
        scrolled right.

        @return: Horizontal scrolling position in pixels.
        """
        raise NotImplementedError


    def setScrollLeft(self, pixelsScrolled):
        """Sets scroll left offset.

        Scrolling offset is the number of pixels this scrollable has been
        scrolled right.

        The method only has effect if programmatic scrolling is enabled for
        the scrollable. Some implementations may require enabling programmatic
        before this method can be used. See L{setScrollable} for more
        information.

        @param pixelsScrolled:
                   the xOffset.
        """
        raise NotImplementedError


    def getScrollTop(self):
        """Gets scroll top offset.

        Scrolling offset is the number of pixels this scrollable has been
        scrolled down.

        @return: Vertical scrolling position in pixels.
        """
        raise NotImplementedError


    def setScrollTop(self, pixelsScrolled):
        """Sets scroll top offset.

        Scrolling offset is the number of pixels this scrollable has been
        scrolled down.

        The method only has effect if programmatic scrolling is enabled for
        the scrollable. Some implementations may require enabling programmatic
        before this method can be used. See L{setScrollable} for more
        information.

        The scrolling position is limited by the current height of the content
        area. If the position is below the height, it is scrolled to the
        bottom. However, if the same response also adds height to the content
        area, scrolling to bottom only scrolls to the bottom of the previous
        content area.

        @param pixelsScrolled:
                   the yOffset.
        """
        raise NotImplementedError


    def isScrollable(self):
        """Is programmatic scrolling enabled.

        Whether programmatic scrolling with L{setScrollLeft} and
        L{setScrollTop} is enabled.

        @return: C{True} if the scrolling is enabled, otherwise C{False}.
        """
        raise NotImplementedError


    def setScrollable(self, isScrollingEnabled):
        """Enables or disables programmatic scrolling.

        Enables setting the scroll position with L{setScrollLeft} and
        L{setScrollTop}. Implementations of the interface may have
        programmatic scrolling disabled by default, in which case you
        need to enable it to use the mentioned methods.

        Notice that this does <i>not</i> control whether scroll bars are
        shown for a scrollable component. That normally happens automatically
        when the content grows too big for the component, relying on the
        "overflow: auto" property in CSS.

        @param isScrollingEnabled:
                   true if the scrolling is allowed.
        """
        raise NotImplementedError
