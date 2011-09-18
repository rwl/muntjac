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
from com.vaadin.ui.ComponentContainer import (ComponentContainer,)
from com.vaadin.terminal.gwt.client.ui.VMarginInfo import (VMarginInfo,)
# from java.io.Serializable import (Serializable,)


class Layout(ComponentContainer, Serializable):
    """Extension to the {@link ComponentContainer} interface which adds the
    layouting control to the elements in the container. This is required by the
    various layout components to enable them to place other components in
    specific locations in the UI.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """

    def setMargin(self, *args):
        """Enable layout margins. Affects all four sides of the layout. This will
        tell the client-side implementation to leave extra space around the
        layout. The client-side implementation decides the actual amount, and it
        can vary between themes.

        @param enabled
        ---
        Enable specific layout margins. This will tell the client-side
        implementation to leave extra space around the layout in specified edges,
        clockwise from top (top, right, bottom, left). The client-side
        implementation decides the actual amount, and it can vary between themes.

        @param top
        @param right
        @param bottom
        @param left
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            enabled, = _0
        elif _1 == 4:
            top, right, bottom, left = _0
        else:
            raise ARGERROR(1, 4)

    class AlignmentHandler(Serializable):
        """AlignmentHandler is most commonly an advanced {@link Layout} that can
        align its components.
        """
        # Contained component should be aligned horizontally to the left.
        # 
        # @deprecated Use of {@link Alignment} class and its constants

        ALIGNMENT_LEFT = self.Bits.ALIGNMENT_LEFT
        # Contained component should be aligned horizontally to the right.
        # 
        # @deprecated Use of {@link Alignment} class and its constants

        ALIGNMENT_RIGHT = self.Bits.ALIGNMENT_RIGHT
        # Contained component should be aligned vertically to the top.
        # 
        # @deprecated Use of {@link Alignment} class and its constants

        ALIGNMENT_TOP = self.Bits.ALIGNMENT_TOP
        # Contained component should be aligned vertically to the bottom.
        # 
        # @deprecated Use of {@link Alignment} class and its constants

        ALIGNMENT_BOTTOM = self.Bits.ALIGNMENT_BOTTOM
        # Contained component should be horizontally aligned to center.
        # 
        # @deprecated Use of {@link Alignment} class and its constants

        ALIGNMENT_HORIZONTAL_CENTER = self.Bits.ALIGNMENT_HORIZONTAL_CENTER
        # Contained component should be vertically aligned to center.
        # 
        # @deprecated Use of {@link Alignment} class and its constants

        ALIGNMENT_VERTICAL_CENTER = self.Bits.ALIGNMENT_VERTICAL_CENTER

        def setComponentAlignment(self, *args):
            """Set alignment for one contained component in this layout. Alignment
            is calculated as a bit mask of the two passed values.

            @deprecated Use {@link #setComponentAlignment(Component, Alignment)}
                        instead

            @param childComponent
                       the component to align within it's layout cell.
            @param horizontalAlignment
                       the horizontal alignment for the child component (left,
                       center, right). Use ALIGNMENT constants.
            @param verticalAlignment
                       the vertical alignment for the child component (top,
                       center, bottom). Use ALIGNMENT constants.
            ---
            Set alignment for one contained component in this layout. Use
            predefined alignments from Alignment class.

            Example: <code>
                 layout.setComponentAlignment(myComponent, Alignment.TOP_RIGHT);
            </code>

            @param childComponent
                       the component to align within it's layout cell.
            @param alignment
                       the Alignment value to be set
            """
            _0 = args
            _1 = len(args)
            if _1 == 2:
                childComponent, alignment = _0
            elif _1 == 3:
                childComponent, horizontalAlignment, verticalAlignment = _0
            else:
                raise ARGERROR(2, 3)

        def getComponentAlignment(self, childComponent):
            """Returns the current Alignment of given component.

            @param childComponent
            @return the {@link Alignment}
            """
            pass

    class SpacingHandler(Serializable):
        """This type of layout supports automatic addition of space between its
        components.
        """

        def setSpacing(self, enabled):
            """Enable spacing between child components within this layout.

            <p>
            <strong>NOTE:</strong> This will only affect the space between
            components, not the space around all the components in the layout
            (i.e. do not confuse this with the cellspacing attribute of a HTML
            Table). Use {@link #setMargin(boolean)} to add space around the
            layout.
            </p>

            <p>
            See the reference manual for more information about CSS rules for
            defining the amount of spacing to use.
            </p>

            @param enabled
                       true if spacing should be turned on, false if it should be
                       turned off
            """
            pass

        def isSpacingEnabled(self):
            """@return true if spacing between child components within this layout
                    is enabled, false otherwise
            @deprecated Use {@link #isSpacing()} instead.
            """
            pass

        def isSpacing(self):
            """@return true if spacing between child components within this layout
                    is enabled, false otherwise
            """
            pass

    class MarginHandler(Serializable):
        """This type of layout supports automatic addition of margins (space around
        its components).
        """

        def setMargin(self, marginInfo):
            """Enable margins for this layout.

            <p>
            <strong>NOTE:</strong> This will only affect the space around the
            components in the layout, not space between the components in the
            layout. Use {@link #setSpacing(boolean)} to add space between the
            components in the layout.
            </p>

            <p>
            See the reference manual for more information about CSS rules for
            defining the size of the margin.
            </p>

            @param marginInfo
                       MarginInfo object containing the new margins.
            """
            pass

        def getMargin(self):
            """@return MarginInfo containing the currently enabled margins."""
            pass

    class MarginInfo(VMarginInfo, Serializable):

        def __init__(self, *args):
            _0 = args
            _1 = len(args)
            if _1 == 1:
                enabled, = _0
                super(MarginInfo, self)(enabled, enabled, enabled, enabled)
            elif _1 == 4:
                top, right, bottom, left = _0
                super(MarginInfo, self)(top, right, bottom, left)
            else:
                raise ARGERROR(1, 4)
