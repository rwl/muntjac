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

"""Defines an interface implemented by all visual objects that can be
scrolled."""


class IScrollable(object):
    """This interface is implemented by all visual objects that can be
    scrolled programmatically from the server-side, or for which it is
    possible to know the scroll position on the server-side.. The unit
    of scrolling is pixel.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.3
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
