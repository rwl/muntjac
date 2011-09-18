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

from com.vaadin.ui.Alignment import (Alignment,)
from com.vaadin.ui.Layout import (AlignmentHandler,)
# from com.vaadin.ui.Layout.AlignmentHandler import (AlignmentHandler,)
# from java.io.Serializable import (Serializable,)
# from java.util.HashMap import (HashMap,)
# from java.util.Map import (Map,)


class AlignmentUtils(Serializable):
    """Helper class for setting alignments using a short notation.

    Supported notation is:

    t,top for top alignment

    m,middle for vertical center alignment

    b,bottom for bottom alignment

    l,left for left alignment

    c,center for horizontal center alignment

    r,right for right alignment

    @deprecated {@code AlignmentUtils} has been replaced by {@link Alignment}.
    """
    _horizontalMask = (AlignmentHandler.ALIGNMENT_LEFT | AlignmentHandler.ALIGNMENT_HORIZONTAL_CENTER) | AlignmentHandler.ALIGNMENT_RIGHT
    _verticalMask = (AlignmentHandler.ALIGNMENT_TOP | AlignmentHandler.ALIGNMENT_VERTICAL_CENTER) | AlignmentHandler.ALIGNMENT_BOTTOM
    _alignmentStrings = dict()

    @classmethod
    def addMapping(cls, alignment, *values):
        for s in values:
            cls._alignmentStrings.put(s, alignment)

    addMapping(AlignmentHandler.ALIGNMENT_TOP, 't', 'top')
    addMapping(AlignmentHandler.ALIGNMENT_BOTTOM, 'b', 'bottom')
    addMapping(AlignmentHandler.ALIGNMENT_VERTICAL_CENTER, 'm', 'middle')
    addMapping(AlignmentHandler.ALIGNMENT_LEFT, 'l', 'left')
    addMapping(AlignmentHandler.ALIGNMENT_RIGHT, 'r', 'right')
    addMapping(AlignmentHandler.ALIGNMENT_HORIZONTAL_CENTER, 'c', 'center')

    @classmethod
    def setComponentAlignment(cls, parent, component, alignment):
        """Set the alignment for the component using short notation

        @param parent
        @param component
        @param alignment
                   String containing one or two alignment strings. If short
                   notation "r","t",etc is used valid strings include
                   "r","rt","tr","t". If the longer notation is used the
                   alignments should be separated by a space e.g.
                   "right","right top","top right","top". It is valid to mix
                   short and long notation but they must be separated by a space
                   e.g. "r top".
        @throws IllegalArgumentException
        """
        if (alignment is None) or (len(alignment) == 0):
            raise cls.IllegalArgumentException('alignment for setComponentAlignment() cannot be null or empty')
        currentAlignment = parent.getComponentAlignment(component).getBitMask()
        if len(alignment) == 1:
            # Use short form "t","l",...
            currentAlignment = cls.parseAlignment(alignment[:1], currentAlignment)
        elif len(alignment) == 2:
            # Use short form "tr","lb",...
            currentAlignment = cls.parseAlignment(alignment[:1], currentAlignment)
            currentAlignment = cls.parseAlignment(alignment[1:2], currentAlignment)
        else:
            # Alignments are separated by space
            strings = alignment.split(' ')
            if len(strings) > 2:
                raise cls.IllegalArgumentException('alignment for setComponentAlignment() should not contain more than 2 alignments')
            for alignmentString in strings:
                currentAlignment = cls.parseAlignment(alignmentString, currentAlignment)
        horizontalAlignment = currentAlignment & cls._horizontalMask
        verticalAlignment = currentAlignment & cls._verticalMask
        parent.setComponentAlignment(component, Alignment(horizontalAlignment + verticalAlignment))

    @classmethod
    def parseAlignment(cls, alignmentString, alignment):
        """Parse alignmentString which contains one alignment (horizontal or
        vertical) and return and updated version of the passed alignment where
        the alignment in one direction has been changed. If the passed
        alignmentString is unknown an exception is thrown

        @param alignmentString
        @param alignment
        @return
        @throws IllegalArgumentException
        """
        parsed = cls._alignmentStrings[alignmentString.toLowerCase()]
        if parsed is None:
            raise cls.IllegalArgumentException('Could not parse alignment string \'' + alignmentString + '\'')
        if parsed & cls._horizontalMask != 0:
            # Get the vertical alignment from the current alignment
            vertical = alignment & cls._verticalMask
            # Add the parsed horizontal alignment
            alignment = vertical | parsed
        else:
            # Get the horizontal alignment from the current alignment
            horizontal = alignment & cls._horizontalMask
            # Add the parsed vertical alignment
            alignment = horizontal | parsed
        return alignment
