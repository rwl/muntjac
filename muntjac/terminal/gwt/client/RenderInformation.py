# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.RenderSpace import (RenderSpace,)


class RenderInformation(object):
    """Contains size information about a rendered container and its content area.

    @author Artur Signell
    """
    _contentArea = RenderSpace()
    _renderedSize = Size(-1, -1)

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
        newSize = self.Size(element.getOffsetWidth(), element.getOffsetHeight())
        if newSize == self._renderedSize:
            return False
        else:
            self._renderedSize = newSize
            return True

    def toString(self):
        return 'RenderInformation [contentArea=' + self._contentArea + ',renderedSize=' + self._renderedSize + ']'

    class FloatSize(object):
        _width = None
        _height = None

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

    def Size(RenderInformation_this, *args, **kwargs):

        class Size(object):
            _width = None
            _height = None

            def equals(self, obj):
                if not isinstance(obj, RenderInformation_this.Size):
                    return False
                other = obj
                return other.width == self._width and other.height == self._height

            def hashCode(self):
                return (self._width << 8) | self._height

            def __init__(self, *args):
                _0 = args
                _1 = len(args)
                if _1 == 0:
                    pass # astStmt: [Stmt([]), None]
                elif _1 == 2:
                    width, height = _0
                    self._height = height
                    self._width = width
                else:
                    raise ARGERROR(0, 2)

            def getWidth(self):
                return self._width

            def setWidth(self, width):
                self._width = width

            def getHeight(self):
                return self._height

            def setHeight(self, height):
                self._height = height

            def toString(self):
                return 'Size [width=' + self._width + ',height=' + self._height + ']'

        return Size(*args, **kwargs)
