# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

"""Defines an extension to the C{IComponentContainer} interface which adds the
layouting control to the elements in the container."""

from muntjac.ui.component_container import IComponentContainer

from muntjac.terminal.gwt.client.ui.v_margin_info import VMarginInfo
from muntjac.terminal.gwt.client.ui.alignment_info import Bits


class ILayout(IComponentContainer):
    """Extension to the L{IComponentContainer} interface which adds the
    layouting control to the elements in the container. This is required by
    the various layout components to enable them to place other components in
    specific locations in the UI.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def setMargin(self, *args):
        """Enable layout margins. Affects all four sides of the layout. This
        will tell the client-side implementation to leave extra space around
        the layout. The client-side implementation decides the actual amount,
        and it can vary between themes.

        Alternatively, enable specific layout margins. This will tell the
        client-side implementation to leave extra space around the layout in
        specified edges, clockwise from top (top, right, bottom, left). The
        client-side implementation decides the actual amount, and it can vary
        between themes.

        @param args: tuple of the form
            - (enabled)
            - (top, right, bottom, left)
        """
        raise NotImplementedError


class IAlignmentHandler(object):
    """IAlignmentHandler is most commonly an advanced L{ILayout} that
    can align its components.
    """

    #: Contained component should be aligned horizontally to the left.
    #
    # @deprecated: Use of L{Alignment} class and its constants
    ALIGNMENT_LEFT = Bits.ALIGNMENT_LEFT

    #: Contained component should be aligned horizontally to the right.
    #
    # @deprecated: Use of L{Alignment} class and its constants
    ALIGNMENT_RIGHT = Bits.ALIGNMENT_RIGHT

    #: Contained component should be aligned vertically to the top.
    #
    # @deprecated: Use of L{Alignment} class and its constants
    ALIGNMENT_TOP = Bits.ALIGNMENT_TOP

    #: Contained component should be aligned vertically to the bottom.
    #
    # @deprecated: Use of L{Alignment} class and its constants
    ALIGNMENT_BOTTOM = Bits.ALIGNMENT_BOTTOM

    #: Contained component should be horizontally aligned to center.
    #
    # @deprecated: Use of L{Alignment} class and its constants
    ALIGNMENT_HORIZONTAL_CENTER = Bits.ALIGNMENT_HORIZONTAL_CENTER

    #: Contained component should be vertically aligned to center.
    #
    # @deprecated: Use of L{Alignment} class and its constants
    ALIGNMENT_VERTICAL_CENTER = Bits.ALIGNMENT_VERTICAL_CENTER


    def setComponentAlignment(self, *args):
        """Set alignment for one contained component in this layout. Alignment
        is calculated as a bit mask of the two passed values or predefined
        alignments from Alignment class.

        Example::
             layout.setComponentAlignment(myComponent, Alignment.TOP_RIGHT)

        @deprecated: Use L{setComponentAlignment} instead

        @param args: tuple of the form
            - (childComponent, horizontalAlignment, verticalAlignment)
              1. the component to align within it's layout cell.
              2. the horizontal alignment for the child component (left,
                 center, right). Use ALIGNMENT constants.
              3. the vertical alignment for the child component (top,
                 center, bottom). Use ALIGNMENT constants.
            - (childComponent, alignment)
              1. the component to align within it's layout cell.
              2. the Alignment value to be set
        """
        raise NotImplementedError


    def getComponentAlignment(self, childComponent):
        """Returns the current Alignment of given component.

        @return: the L{Alignment}
        """
        raise NotImplementedError


class ISpacingHandler(object):
    """This type of layout supports automatic addition of space between its
    components.
    """

    def setSpacing(self, enabled):
        """Enable spacing between child components within this layout.

        B{NOTE:} This will only affect the space between
        components, not the space around all the components in the layout
        (i.e. do not confuse this with the cellspacing attribute of a HTML
        Table). Use L{setMargin} to add space around the layout.

        See the reference manual for more information about CSS rules for
        defining the amount of spacing to use.

        @param enabled:
                   true if spacing should be turned on, false if it should be
                   turned off
        """
        raise NotImplementedError


    def isSpacingEnabled(self):
        """@return: true if spacing between child components within this layout
                    is enabled, false otherwise
        @deprecated: Use L{isSpacing} instead.
        """
        raise NotImplementedError


    def isSpacing(self):
        """@return: true if spacing between child components within this layout
                    is enabled, false otherwise
        """
        raise NotImplementedError


class IMarginHandler(object):
    """This type of layout supports automatic addition of margins (space around
    its components).
    """

    def setMargin(self, marginInfo):
        """Enable margins for this layout.

        B{NOTE:} This will only affect the space around the
        components in the layout, not space between the components in the
        layout. Use L{setSpacing} to add space between the components in
        the layout.

        See the reference manual for more information about CSS rules for
        defining the size of the margin.

        @param marginInfo:
                   MarginInfo object containing the new margins.
        """
        raise NotImplementedError


    def getMargin(self):
        """@return: MarginInfo containing the currently enabled margins."""
        raise NotImplementedError


class MarginInfo(VMarginInfo):

    def __init__(self, *args):
        super(MarginInfo, self).__init__(*args)
