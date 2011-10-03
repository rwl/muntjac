# Copyright (C) 2010 IT Mill Ltd.
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


class IScrollable(object):
    """This interface is implemented by all visual objects that can be
    scrolled. The unit of scrolling is pixel.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def getScrollLeft(self):
        """Gets scroll left offset.

        Scrolling offset is the number of pixels this scrollable has been
        scrolled right.

        @return Horizontal scrolling position in pixels.
        """
        raise NotImplementedError


    def setScrollLeft(self, pixelsScrolled):
        """Sets scroll left offset.

        Scrolling offset is the number of pixels this scrollable has been
        scrolled right.

        @param pixelsScrolled
                   the xOffset.
        """
        raise NotImplementedError


    def getScrollTop(self):
        """Gets scroll top offset.

        Scrolling offset is the number of pixels this scrollable has been
        scrolled down.

        @return Vertical scrolling position in pixels.
        """
        raise NotImplementedError


    def setScrollTop(self, pixelsScrolled):
        """Sets scroll top offset.

        Scrolling offset is the number of pixels this scrollable has been
        scrolled down.

        @param pixelsScrolled
                   the yOffset.
        """
        raise NotImplementedError


    def isScrollable(self):
        """Is the scrolling enabled.

        Enabling scrolling allows the user to scroll the scrollable view
        interactively

        @return <code>true</code> if the scrolling is allowed, otherwise
                <code>false</code>.
        """
        raise NotImplementedError


    def setScrollable(self, isScrollingEnabled):
        """Enables or disables scrolling..

        Enabling scrolling allows the user to scroll the scrollable view
        interactively

        @param isScrollingEnabled
                   true if the scrolling is allowed.
        """
        raise NotImplementedError
