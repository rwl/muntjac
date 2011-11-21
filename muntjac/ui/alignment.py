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

"""Defines a class containing information about alignment of a component."""

from muntjac.terminal.gwt.client.ui.alignment_info import Bits


class Alignment(object):
    """Class containing information about alignment of a component. Use
    the pre-instantiated classes.
    """

    TOP_RIGHT = None  # see below
    TOP_LEFT = None
    TOP_CENTER = None
    MIDDLE_RIGHT = None
    MIDDLE_LEFT = None
    MIDDLE_CENTER = None
    BOTTOM_RIGHT = None
    BOTTOM_LEFT = None
    BOTTOM_CENTER = None

    def __init__(self, bitMask):
        self._bitMask = bitMask


    def getBitMask(self):
        """Returns a bitmask representation of the alignment value. Used
        internally by terminal.

        @return: the bitmask representation of the alignment value
        """
        return self._bitMask


    def isTop(self):
        """Checks if component is aligned to the top of the available space.

        @return: true if aligned top
        """
        return (self._bitMask & Bits.ALIGNMENT_TOP) == Bits.ALIGNMENT_TOP


    def isBottom(self):
        """Checks if component is aligned to the bottom of the available
        space.

        @return: true if aligned bottom
        """
        return (self._bitMask & Bits.ALIGNMENT_BOTTOM) == \
                Bits.ALIGNMENT_BOTTOM


    def isLeft(self):
        """Checks if component is aligned to the left of the available
        space.

        @return: true if aligned left
        """
        return (self._bitMask & Bits.ALIGNMENT_LEFT) == Bits.ALIGNMENT_LEFT


    def isRight(self):
        """Checks if component is aligned to the right of the available space.

        @return: true if aligned right
        """
        return (self._bitMask & Bits.ALIGNMENT_RIGHT) == Bits.ALIGNMENT_RIGHT


    def isMiddle(self):
        """Checks if component is aligned middle (vertically center) of the
        available space.

        @return: true if aligned bottom
        """
        return (self._bitMask & Bits.ALIGNMENT_VERTICAL_CENTER) == \
                Bits.ALIGNMENT_VERTICAL_CENTER


    def isCenter(self):
        """Checks if component is aligned center (horizontally) of the
        available space.

        @return: true if aligned center
        """
        return (self._bitMask & Bits.ALIGNMENT_HORIZONTAL_CENTER) == \
                Bits.ALIGNMENT_HORIZONTAL_CENTER


    def getVerticalAlignment(self):
        """Returns string representation of vertical alignment.

        @return: vertical alignment as CSS value
        """
        if self.isBottom():
            return 'bottom'
        elif self.isMiddle():
            return 'middle'
        return 'top'


    def getHorizontalAlignment(self):
        """Returns string representation of horizontal alignment.

        @return: horizontal alignment as CSS value
        """
        if self.isRight():
            return 'right'
        elif self.isCenter():
            return 'center'
        return 'left'


    def __eq__(self, obj):
        if self == obj:
            return True

        if (obj is None) or (obj.__class__ != self.__class__):
            return False

        return self._bitMask == obj.bitMask


    def __hash__(self):
        return self._bitMask


    def __str__(self):
        return str(self._bitMask)


Alignment.TOP_RIGHT = Alignment((Bits.ALIGNMENT_TOP +
        Bits.ALIGNMENT_RIGHT))

Alignment.TOP_LEFT = Alignment((Bits.ALIGNMENT_TOP +
        Bits.ALIGNMENT_LEFT))

Alignment.TOP_CENTER = Alignment((Bits.ALIGNMENT_TOP +
        Bits.ALIGNMENT_HORIZONTAL_CENTER))

Alignment.MIDDLE_RIGHT = Alignment((Bits.ALIGNMENT_VERTICAL_CENTER +
        Bits.ALIGNMENT_RIGHT))

Alignment.MIDDLE_LEFT = Alignment((Bits.ALIGNMENT_VERTICAL_CENTER +
        Bits.ALIGNMENT_LEFT))

Alignment.MIDDLE_CENTER = Alignment((Bits.ALIGNMENT_VERTICAL_CENTER +
        Bits.ALIGNMENT_HORIZONTAL_CENTER))

Alignment.BOTTOM_RIGHT = Alignment((Bits.ALIGNMENT_BOTTOM +
        Bits.ALIGNMENT_RIGHT))

Alignment.BOTTOM_LEFT = Alignment((Bits.ALIGNMENT_BOTTOM +
        Bits.ALIGNMENT_LEFT))

Alignment.BOTTOM_CENTER = Alignment((Bits.ALIGNMENT_BOTTOM +
        Bits.ALIGNMENT_HORIZONTAL_CENTER))
