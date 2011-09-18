# Copyright (C) 2011 Vaadin Ltd
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

# from java.io.Serializable import (Serializable,)


class Scrollable(Serializable):
    """<p>
    This interface is implemented by all visual objects that can be scrolled. The
    unit of scrolling is pixel.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """

    def getScrollLeft(self):
        """Gets scroll left offset.

        <p>
        Scrolling offset is the number of pixels this scrollable has been
        scrolled right.
        </p>

        @return Horizontal scrolling position in pixels.
        """
        pass

    def setScrollLeft(self, pixelsScrolled):
        """Sets scroll left offset.

        <p>
        Scrolling offset is the number of pixels this scrollable has been
        scrolled right.
        </p>

        @param pixelsScrolled
                   the xOffset.
        """
        pass

    def getScrollTop(self):
        """Gets scroll top offset.

        <p>
        Scrolling offset is the number of pixels this scrollable has been
        scrolled down.
        </p>

        @return Vertical scrolling position in pixels.
        """
        pass

    def setScrollTop(self, pixelsScrolled):
        """Sets scroll top offset.

        <p>
        Scrolling offset is the number of pixels this scrollable has been
        scrolled down.
        </p>

        @param pixelsScrolled
                   the yOffset.
        """
        pass

    def isScrollable(self):
        """Is the scrolling enabled.

        <p>
        Enabling scrolling allows the user to scroll the scrollable view
        interactively
        </p>

        @return <code>true</code> if the scrolling is allowed, otherwise
                <code>false</code>.
        """
        pass

    def setScrollable(self, isScrollingEnabled):
        """Enables or disables scrolling..

        <p>
        Enabling scrolling allows the user to scroll the scrollable view
        interactively
        </p>

        @param isScrollingEnabled
                   true if the scrolling is allowed.
        """
        pass
