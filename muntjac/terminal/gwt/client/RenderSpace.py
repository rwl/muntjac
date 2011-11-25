# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.RenderInformation import (RenderInformation,)
Size = RenderInformation.Size


class RenderSpace(Size):
    """Contains information about render area."""
    _scrollBarSize = 0

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            pass # astStmt: [Stmt([]), None]
        elif _1 == 2:
            width, height = _0
            super(RenderSpace, self)(width, height)
        elif _1 == 3:
            width, height, useNativeScrollbarSize = _0
            super(RenderSpace, self)(width, height)
            if useNativeScrollbarSize:
                self._scrollBarSize = Util.getNativeScrollbarSize()
        else:
            raise ARGERROR(0, 3)

    def getHeight(self):
        """Returns pixels available vertically for contained widget, including
        possible scrollbars.
        """
        return super(RenderSpace, self).getHeight()

    def getWidth(self):
        """Returns pixels available horizontally for contained widget, including
        possible scrollbars.
        """
        return super(RenderSpace, self).getWidth()

    def getScrollbarSize(self):
        """In case containing block has oveflow: auto, this method must return
        number of pixels used by scrollbar. Returning zero means either that no
        scrollbar will be visible.
        """
        return self._scrollBarSize
