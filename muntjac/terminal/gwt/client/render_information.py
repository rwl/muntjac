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

from muntjac.terminal.gwt.client.render_space import RenderSpace


class RenderInformation(object):
    """Contains size information about a rendered container and its
    content area.

    @author: Artur Signell
    @author: Richard Lincoln
    """

    def __init__(self):
        self._contentArea = RenderSpace()
        self._renderedSize = Size(-1, -1)


    def setContentAreaWidth(self, w):
        self._contentArea.setWidth(w)


    def setContentAreaHeight(self, h):
        self._contentArea.setHeight(h)


    def getContentAreaSize(self):
        return self._contentArea


    def getRenderedSize(self):
        return self._renderedSize


    def updateSize(self, element):
        """Update the size of the widget.

        @param widget

        @return true if the size has changed since last update
        """
        newSize = Size(element.getOffsetWidth(), element.getOffsetHeight())
        if newSize == self._renderedSize:
            return False
        else:
            self._renderedSize = newSize
            return True


    def __str__(self):
        return ('RenderInformation [contentArea=' + self._contentArea
                + ',renderedSize=' + self._renderedSize + ']')


class FloatSize(object):

    def __init__(self, width, height):
        self._width = width
        self._height = height


    def getWidth(self):
        return self._width


    def setWidth(self, width):
        self._width = width


    def getHeight(self):
        return self._height


    def setHeight(self, height):
        self._height = height


class Size(object):

    def __init__(self, width=None, height=None):
        self._width = width
        self._height = height


    def __eq__(self, obj):
        if not isinstance(obj, Size):
            return False
        other = obj
        return other.width == self._width and other.height == self._height


    def __hash__(self):
        return (self._width << 8) | self._height


    def getWidth(self):
        return self._width


    def setWidth(self, width):
        self._width = width


    def getHeight(self):
        return self._height


    def setHeight(self, height):
        self._height = height


    def __str__(self):
        return 'Size [width=' + self._width + ',height=' + self._height + ']'
