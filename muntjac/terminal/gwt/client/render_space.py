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

from muntjac.terminal.gwt.client.util import Util
from muntjac.terminal.gwt.client.render_information import Size


class RenderSpace(Size):
    """Contains information about render area."""

    def __init__(self, width=None, height=None, useNativeScrollbarSize=False):
        self._scrollBarSize = 0
        super(RenderSpace, self).__init__(width, height)

        if useNativeScrollbarSize:
            self._scrollBarSize = Util.getNativeScrollbarSize()


    def getHeight(self):
        """Returns pixels available vertically for contained widget,
        including possible scrollbars.
        """
        return super(RenderSpace, self).getHeight()


    def getWidth(self):
        """Returns pixels available horizontally for contained widget,
        including possible scrollbars.
        """
        return super(RenderSpace, self).getWidth()


    def getScrollbarSize(self):
        """In case containing block has oveflow: auto, this method must
        return number of pixels used by scrollbar. Returning zero means
        either that no scrollbar will be visible.
        """
        return self._scrollBarSize
