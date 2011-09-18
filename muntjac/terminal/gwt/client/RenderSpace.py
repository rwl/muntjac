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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.Util import (Util,)


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
