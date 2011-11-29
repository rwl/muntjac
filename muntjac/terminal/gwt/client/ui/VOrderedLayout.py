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

from __pyjamas__ import (ARGERROR, POSTDEC, POSTINC,)
from com.vaadin.terminal.gwt.client.ui.AlignmentInfo import (AlignmentInfo,)
from com.vaadin.terminal.gwt.client.RenderSpace import (RenderSpace,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.layout.CellBasedLayout import (CellBasedLayout,)
from com.vaadin.terminal.gwt.client.ui.LayoutClickEventHandler import (LayoutClickEventHandler,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.layout.ChildComponentContainer import (ChildComponentContainer,)
# from com.google.gwt.core.client.JsArrayString import (JsArrayString,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Iterator import (Iterator,)
# from java.util.Set import (Set,)
Size = RenderInformation.Size


class VOrderedLayout(CellBasedLayout):
    CLASSNAME = 'v-orderedlayout'
    _orientation = None
    # Can be removed once OrderedLayout is removed
    _allowOrientationUpdate = False
    # Size of the layout excluding any margins.
    _activeLayoutSize = Size(0, 0)
    _isRendering = False
    _width = ''
    _sizeHasChangedDuringRendering = False
    _expandRatios = None
    _expandRatioSum = None
    _defaultExpandRatio = None
    _alignments = None

    class clickEventHandler(LayoutClickEventHandler):

        def getChildComponent(self, element):
            return VOrderedLayout_this.getComponent(element)

        def registerHandler(self, handler, type):
            return self.addDomHandler(handler, type)

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.__init__(self.CLASSNAME, self.ORIENTATION_VERTICAL)
            self._allowOrientationUpdate = True
        elif _1 == 2:
            className, orientation = _0
            self.setStyleName(className)
            self._orientation = orientation
            self.STYLENAME_SPACING = className + '-spacing'
            self.STYLENAME_MARGIN_TOP = className + '-margin-top'
            self.STYLENAME_MARGIN_RIGHT = className + '-margin-right'
            self.STYLENAME_MARGIN_BOTTOM = className + '-margin-bottom'
            self.STYLENAME_MARGIN_LEFT = className + '-margin-left'
        else:
            raise ARGERROR(0, 2)

    def updateFromUIDL(self, uidl, client):
        self._isRendering = True
        super(VOrderedLayout, self).updateFromUIDL(uidl, client)
        # Only non-cached, visible UIDL:s can introduce changes
        if uidl.getBooleanAttribute('cached') or uidl.getBooleanAttribute('invisible'):
            self._isRendering = False
            return
        self.clickEventHandler.handleEventHandlerRegistration(client)
        if self._allowOrientationUpdate:
            self.handleOrientationUpdate(uidl)
        # IStopWatch w = new IStopWatch("OrderedLayout.updateFromUIDL");
        uidlWidgets = list(uidl.getChildCount())
        relativeSizeComponents = list()
        relativeSizeComponentUIDL = list()
        pos = 0
        _0 = True
        it = uidl.getChildIterator()
        while True:
            if _0 is True:
                _0 = False
            if not it.hasNext():
                break
            childUIDL = it.next()
            child = client.getPaintable(childUIDL)
            widget = child
            # Create container for component
            childComponentContainer = self.getComponentContainer(widget)
            if childComponentContainer is None:
                # This is a new component
                childComponentContainer = self.createChildContainer(widget)
            else:
                # The widget may be null if the same paintable has been
                # rendered in a different component container while this has
                # been invisible. Ensure the childComponentContainer has the
                # widget attached. See e.g. #5372

                childComponentContainer.setWidget(widget)
            self.addOrMoveChild(childComponentContainer, POSTINC(globals(), locals(), 'pos'))
            # Components which are to be expanded in the same orientation as
            # the layout are rendered later when it is clear how much space
            # they can use

            if not Util.isCached(childUIDL):
                relativeSize = Util.parseRelativeSize(childUIDL)
                childComponentContainer.setRelativeSize(relativeSize)
            if childComponentContainer.isComponentRelativeSized(self._orientation):
                relativeSizeComponents.add(childComponentContainer)
                relativeSizeComponentUIDL.add(childUIDL)
            else:
                if self.isDynamicWidth():
                    childComponentContainer.renderChild(childUIDL, client, -1)
                else:
                    childComponentContainer.renderChild(childUIDL, client, self._activeLayoutSize.getWidth())
                if self._sizeHasChangedDuringRendering and Util.isCached(childUIDL):
                    # notify cached relative sized component about size
                    # chance
                    client.handleComponentRelativeSize(childComponentContainer.getWidget())
            uidlWidgets.add(widget)
        # w.mark("Rendering of "
        # + (uidlWidgets.size() - relativeSizeComponents.size())
        # + " absolute size components done");
        # Remove any children after pos. These are the ones that previously
        # were in the layout but have now been removed

        self.removeChildrenAfter(pos)
        # w.mark("Old children removed");
        # Fetch alignments and expand ratio from UIDL
        self.updateAlignmentsAndExpandRatios(uidl, uidlWidgets)
        # w.mark("Alignments and expand ratios updated");
        # Fetch widget sizes from rendered components
        self.updateWidgetSizes()
        # w.mark("Widget sizes updated");
        self.recalculateLayout()
        # w.mark("Layout size calculated (" + activeLayoutSize +
        # ") offsetSize: "
        # + getOffsetWidth() + "," + getOffsetHeight());
        # Render relative size components
        _1 = True
        i = 0
        while True:
            if _1 is True:
                _1 = False
            else:
                i += 1
            if not (i < len(relativeSizeComponents)):
                break
            childComponentContainer = relativeSizeComponents[i]
            childUIDL = relativeSizeComponentUIDL[i]
            if self.isDynamicWidth():
                childComponentContainer.renderChild(childUIDL, client, -1)
            else:
                childComponentContainer.renderChild(childUIDL, client, self._activeLayoutSize.getWidth())
            if Util.isCached(childUIDL):
                # We must update the size of the relative sized component if
                # the expand ratio or something else in the layout changes
                # which affects the size of a relative sized component

                client.handleComponentRelativeSize(childComponentContainer.getWidget())
            # childComponentContainer.updateWidgetSize();
        # w.mark("Rendering of " + (relativeSizeComponents.size())
        # + " relative size components done");
        # Fetch widget sizes for relative size components
        for childComponentContainer in self.widgetToComponentContainer.values():
            # Update widget size from DOM
            childComponentContainer.updateWidgetSize()
        # w.mark("Widget sizes updated");
        # Components with relative size in main direction may affect the layout
        # size in the other direction

        if (
            (self.isHorizontal() and self.isDynamicHeight()) or (self.isVertical() and self.isDynamicWidth())
        ):
            self.layoutSizeMightHaveChanged()
        # w.mark("Layout dimensions updated");
        # Update component spacing
        self.updateContainerMargins()
        # Update component sizes for components with relative size in non-main
        # direction

        if self.updateRelativeSizesInNonMainDirection():
            # Sizes updated - might affect the other dimension so we need to
            # recheck the widget sizes and recalculate layout dimensions
            self.updateWidgetSizes()
            self.layoutSizeMightHaveChanged()
        self.calculateAlignments()
        # w.mark("recalculateComponentSizesAndAlignments done");
        self.setRootSize()
        if BrowserInfo.get().isIE():
            # This should fix the issue with padding not always taken into
            # account for the containers leading to no spacing between
            # elements.

            self.root.getStyle().setProperty('zoom', '1')
        # w.mark("runDescendentsLayout done");
        self._isRendering = False
        self._sizeHasChangedDuringRendering = False

    def layoutSizeMightHaveChanged(self):
        oldSize = Size(self._activeLayoutSize.getWidth(), self._activeLayoutSize.getHeight())
        self.calculateLayoutDimensions()
        # If layout dimension changes we must also update container sizes
        if not (oldSize == self._activeLayoutSize):
            self.calculateContainerSize()

    def updateWidgetSizes(self):
        for childComponentContainer in self.widgetToComponentContainer.values():
            # Update widget size from DOM
            childComponentContainer.updateWidgetSize()

    def recalculateLayout(self):
        # Calculate space for relative size components
        spaceForExpansion = self.calculateLayoutDimensions()
        if not self.widgetToComponentContainer.isEmpty():
            # Divide expansion space between component containers
            self.expandComponentContainers(spaceForExpansion)
            # Update container sizes
            self.calculateContainerSize()

    def expandComponentContainers(self, spaceForExpansion):
        remaining = spaceForExpansion
        for childComponentContainer in self.widgetToComponentContainer.values():
            remaining -= childComponentContainer.expand(self._orientation, spaceForExpansion)
        if remaining > 0:
            # Some left-over pixels due to rounding errors
            # Add one pixel to each container until there are no pixels left
            # FIXME extra pixels should be divided among expanded widgets if
            # such a widgets exists
            widgetIterator = self
            while (
                widgetIterator.hasNext() and POSTDEC(globals(), locals(), 'remaining') > 0
            ):
                childComponentContainer = widgetIterator.next()
                childComponentContainer.expandExtra(self._orientation, 1)

    def handleOrientationUpdate(self, uidl):
        newOrientation = self.ORIENTATION_VERTICAL
        if 'horizontal' == uidl.getStringAttribute('orientation'):
            newOrientation = self.ORIENTATION_HORIZONTAL
        if self._orientation != newOrientation:
            self._orientation = newOrientation
            for childComponentContainer in self.widgetToComponentContainer.values():
                childComponentContainer.setOrientation(self._orientation)

    def updateRelativeSizesInNonMainDirection(self):
        """Updated components with relative height in horizontal layouts and
        components with relative width in vertical layouts. This is only needed
        if the height (horizontal layout) or width (vertical layout) has not been
        specified.
        """
        updateDirection = 1 - self._orientation
        if (
            (updateDirection == self.ORIENTATION_HORIZONTAL and not self.isDynamicWidth()) or (updateDirection == self.ORIENTATION_VERTICAL and not self.isDynamicHeight())
        ):
            return False
        updated = False
        for componentContainer in self.widgetToComponentContainer.values():
            if componentContainer.isComponentRelativeSized(updateDirection):
                self.client.handleComponentRelativeSize(componentContainer.getWidget())
            updated = True
        return updated

    def calculateLayoutDimensions(self):
        summedWidgetWidth = 0
        summedWidgetHeight = 0
        maxWidgetWidth = 0
        maxWidgetHeight = 0
        # Calculate layout dimensions from component dimensions
        for childComponentContainer in self.widgetToComponentContainer.values():
            widgetHeight = 0
            widgetWidth = 0
            if childComponentContainer.isComponentRelativeSized(self._orientation):
                if self._orientation == self.ORIENTATION_HORIZONTAL:
                    widgetHeight = self.getWidgetHeight(childComponentContainer)
                else:
                    widgetWidth = self.getWidgetWidth(childComponentContainer)
            else:
                widgetWidth = self.getWidgetWidth(childComponentContainer)
                widgetHeight = self.getWidgetHeight(childComponentContainer)
            summedWidgetWidth += widgetWidth
            summedWidgetHeight += widgetHeight
            maxWidgetHeight = self.Math.max(maxWidgetHeight, widgetHeight)
            maxWidgetWidth = self.Math.max(maxWidgetWidth, widgetWidth)
        if self.isHorizontal():
            summedWidgetWidth += self.activeSpacing.hSpacing * (len(self.widgetToComponentContainer) - 1)
        else:
            summedWidgetHeight += self.activeSpacing.vSpacing * (len(self.widgetToComponentContainer) - 1)
        layoutSize = self.updateLayoutDimensions(summedWidgetWidth, summedWidgetHeight, maxWidgetWidth, maxWidgetHeight)
        if self.isHorizontal():
            remainingSpace = layoutSize.getWidth() - summedWidgetWidth
        else:
            remainingSpace = layoutSize.getHeight() - summedWidgetHeight
        if remainingSpace < 0:
            remainingSpace = 0
        # ApplicationConnection.getConsole().log(
        # "Layout size: " + activeLayoutSize);
        return remainingSpace

    def getWidgetHeight(self, childComponentContainer):
        s = childComponentContainer.getWidgetSize()
        return s.getHeight() + childComponentContainer.getCaptionHeightAboveComponent()

    def getWidgetWidth(self, childComponentContainer):
        s = childComponentContainer.getWidgetSize()
        widgetWidth = s.getWidth() + childComponentContainer.getCaptionWidthAfterComponent()
        # If the component does not have a specified size in the main direction
        # the caption may determine the space used by the component

        if not childComponentContainer.widgetHasSizeSpecified(self._orientation):
            captionWidth = childComponentContainer.getCaptionRequiredWidth()
            if captionWidth > widgetWidth:
                widgetWidth = captionWidth
        return widgetWidth

    def calculateAlignments(self):
        w = 0
        h = 0
        if self.isHorizontal():
            # HORIZONTAL
            h = self._activeLayoutSize.getHeight()
            if not self.isDynamicWidth():
                w = -1
        else:
            # VERTICAL
            w = self._activeLayoutSize.getWidth()
            if not self.isDynamicHeight():
                h = -1
        for childComponentContainer in self.widgetToComponentContainer.values():
            childComponentContainer.updateAlignments(w, h)

    def calculateContainerSize(self):
        # Container size here means the size the container gets from the
        # component. The expansion size is not include in this but taken
        # separately into account.

        height = 0
        width = 0
        widgetIterator = self
        if self.isHorizontal():
            height = self._activeLayoutSize.getHeight()
            availableWidth = self._activeLayoutSize.getWidth()
            first = True
            while widgetIterator.hasNext():
                childComponentContainer = widgetIterator.next()
                if (
                    not childComponentContainer.isComponentRelativeSized(self.ORIENTATION_HORIZONTAL)
                ):
                    # Only components with non-relative size in the main
                    # direction has a container size

                    width = childComponentContainer.getWidgetSize().getWidth() + childComponentContainer.getCaptionWidthAfterComponent()
                    # If the component does not have a specified size in the
                    # main direction the caption may determine the space used
                    # by the component

                    if not childComponentContainer.widgetHasSizeSpecified(self._orientation):
                        captionWidth = childComponentContainer.getCaptionRequiredWidth()
                        # ApplicationConnection.getConsole().log(
                        # "Component width: " + width
                        # + ", caption width: " + captionWidth);
                        if captionWidth > width:
                            width = captionWidth
                else:
                    width = 0
                if not self.isDynamicWidth():
                    if availableWidth == 0:
                        # Let the overflowing components overflow. IE has
                        # problems with zero sizes.

                        # width = 0;
                        # height = 0;
                        pass
                    elif width > availableWidth:
                        width = availableWidth
                        if not first:
                            width -= self.activeSpacing.hSpacing
                        availableWidth = 0
                    else:
                        availableWidth -= width
                        if not first:
                            availableWidth -= self.activeSpacing.hSpacing
                    first = False
                childComponentContainer.setContainerSize(width, height)
        else:
            width = self._activeLayoutSize.getWidth()
            while widgetIterator.hasNext():
                childComponentContainer = widgetIterator.next()
                if (
                    not childComponentContainer.isComponentRelativeSized(self.ORIENTATION_VERTICAL)
                ):
                    # Only components with non-relative size in the main
                    # direction has a container size

                    height = childComponentContainer.getWidgetSize().getHeight() + childComponentContainer.getCaptionHeightAboveComponent()
                else:
                    height = 0
                childComponentContainer.setContainerSize(width, height)

    def updateLayoutDimensions(self, totalComponentWidth, totalComponentHeight, maxComponentWidth, maxComponentHeight):
        # Only need to calculate dynamic dimensions
        if not self.isDynamicHeight() and not self.isDynamicWidth():
            return self._activeLayoutSize
        activeLayoutWidth = 0
        activeLayoutHeight = 0
        # Update layout dimensions
        if self.isHorizontal():
            # Horizontal
            if self.isDynamicWidth():
                activeLayoutWidth = totalComponentWidth
            if self.isDynamicHeight():
                activeLayoutHeight = maxComponentHeight
        else:
            # Vertical
            if self.isDynamicWidth():
                activeLayoutWidth = maxComponentWidth
            if self.isDynamicHeight():
                activeLayoutHeight = totalComponentHeight
        if self.isDynamicWidth():
            self.setActiveLayoutWidth(activeLayoutWidth)
            self.setOuterLayoutWidth(self._activeLayoutSize.getWidth())
        if self.isDynamicHeight():
            self.setActiveLayoutHeight(activeLayoutHeight)
            self.setOuterLayoutHeight(self._activeLayoutSize.getHeight())
        return self._activeLayoutSize

    def setActiveLayoutWidth(self, activeLayoutWidth):
        if activeLayoutWidth < 0:
            activeLayoutWidth = 0
        self._activeLayoutSize.setWidth(activeLayoutWidth)

    def setActiveLayoutHeight(self, activeLayoutHeight):
        if activeLayoutHeight < 0:
            activeLayoutHeight = 0
        self._activeLayoutSize.setHeight(activeLayoutHeight)

    def setOuterLayoutWidth(self, activeLayoutWidth):
        # Don't call setWidth to avoid triggering all kinds of recalculations
        # Also don't call super.setWidth to avoid messing with the
        # dynamicWidth property
        newPixelWidth = activeLayoutWidth + self.activeMargins.getHorizontal()
        self.getElement().getStyle().setWidth(newPixelWidth, Unit.PX)

    def setOuterLayoutHeight(self, activeLayoutHeight):
        # Don't call setHeight to avoid triggering all kinds of recalculations
        # Also don't call super.setHeight to avoid messing with the
        # dynamicHeight property
        newPixelHeight = activeLayoutHeight + self.activeMargins.getVertical()
        self.getElement().getStyle().setHeight(newPixelHeight, Unit.PX)

    def updateContainerMargins(self):
        """Updates the spacing between components. Needs to be done only when
        components are added/removed.
        """
        firstChildComponent = self.getFirstChildComponentContainer()
        if firstChildComponent is not None:
            firstChildComponent.setMarginLeft(0)
            firstChildComponent.setMarginTop(0)
            for childComponent in self.widgetToComponentContainer.values():
                if childComponent == firstChildComponent:
                    continue
                if self.isHorizontal():
                    childComponent.setMarginLeft(self.activeSpacing.hSpacing)
                else:
                    childComponent.setMarginTop(self.activeSpacing.vSpacing)

    def isHorizontal(self):
        return self._orientation == self.ORIENTATION_HORIZONTAL

    def isVertical(self):
        return self._orientation == self.ORIENTATION_VERTICAL

    def createChildContainer(self, child):
        # Create a container DIV for the child
        childComponent = ChildComponentContainer(child, self._orientation)
        return childComponent

    def getAllocatedSpace(self, child):
        width = 0
        height = 0
        childComponentContainer = self.getComponentContainer(child)
        # WIDTH CALCULATION
        if self.isVertical():
            width = self._activeLayoutSize.getWidth()
            width -= childComponentContainer.getCaptionWidthAfterComponent()
        elif not self.isDynamicWidth():
            # HORIZONTAL
            width = childComponentContainer.getContSize().getWidth()
            width -= childComponentContainer.getCaptionWidthAfterComponent()
        # HEIGHT CALCULATION
        if self.isHorizontal():
            height = self._activeLayoutSize.getHeight()
            height -= childComponentContainer.getCaptionHeightAboveComponent()
        elif not self.isDynamicHeight():
            # VERTICAL
            height = childComponentContainer.getContSize().getHeight()
            height -= childComponentContainer.getCaptionHeightAboveComponent()
        # ApplicationConnection.getConsole().log(
        # "allocatedSpace for " + Util.getSimpleName(child) + ": "
        # + width + "," + height);
        space = RenderSpace(width, height)
        return space

    def recalculateLayoutAndComponentSizes(self):
        self.recalculateLayout()
        if not (self.isDynamicHeight() and self.isDynamicWidth()):
            # First update relative sized components
            for componentContainer in self.widgetToComponentContainer.values():
                self.client.handleComponentRelativeSize(componentContainer.getWidget())
                # Update widget size from DOM
                componentContainer.updateWidgetSize()
        if self.isDynamicHeight():
            # Height is not necessarily correct anymore as the height of
            # components might have changed if the width has changed.

            # Get the new widget sizes from DOM and calculate new container
            # sizes

            self.updateWidgetSizes()
            # Update layout dimensions based on widget sizes
            self.recalculateLayout()
        self.updateRelativeSizesInNonMainDirection()
        self.calculateAlignments()
        self.setRootSize()

    def setRootSize(self):
        self.root.getStyle().setPropertyPx('width', self._activeLayoutSize.getWidth())
        self.root.getStyle().setPropertyPx('height', self._activeLayoutSize.getHeight())

    def requestLayout(self, children):
        for p in children:
            # Update widget size from DOM
            componentContainer = self.getComponentContainer(p)
            # This should no longer be needed (after #2563)
            # if (isDynamicWidth()) {
            # componentContainer.setUnlimitedContainerWidth();
            # } else {
            # componentContainer.setLimitedContainerWidth(activeLayoutSize
            # .getWidth());
            # }
            componentContainer.updateWidgetSize()
            # If this is the result of an caption icon onload event the caption
            # size may have changed

            componentContainer.updateCaptionSize()
        sizeBefore = Size(self._activeLayoutSize.getWidth(), self._activeLayoutSize.getHeight())
        self.recalculateLayoutAndComponentSizes()
        sameSize = sizeBefore == self._activeLayoutSize
        if not sameSize:
            # Must inform child components about possible size updates
            self.client.runDescendentsLayout(self)
        # Automatically propagated upwards if the size has changed
        return sameSize

    def setHeight(self, height):
        sizeBefore = Size(self._activeLayoutSize.getWidth(), self._activeLayoutSize.getHeight())
        super(VOrderedLayout, self).setHeight(height)
        if height is not None and not (height == ''):
            self.setActiveLayoutHeight(self.getOffsetHeight() - self.activeMargins.getVertical())
        if self._isRendering:
            self._sizeHasChangedDuringRendering = True
        else:
            self.recalculateLayoutAndComponentSizes()
            sameSize = sizeBefore == self._activeLayoutSize
            if not sameSize:
                # Must inform child components about possible size updates
                self.client.runDescendentsLayout(self)

    def setWidth(self, width):
        if (self._width == width) or (not self.isVisible()):
            return
        sizeBefore = Size(self._activeLayoutSize.getWidth(), self._activeLayoutSize.getHeight())
        super(VOrderedLayout, self).setWidth(width)
        self._width = width
        if width is not None and not (width == ''):
            self.setActiveLayoutWidth(self.getOffsetWidth() - self.activeMargins.getHorizontal())
        if self._isRendering:
            self._sizeHasChangedDuringRendering = True
        else:
            self.recalculateLayoutAndComponentSizes()
            sameSize = sizeBefore == self._activeLayoutSize
            if not sameSize:
                # Must inform child components about possible size updates
                self.client.runDescendentsLayout(self)
            # If the height changes as a consequence of this we must inform the
            # parent also

            if (
                self.isDynamicHeight() and sizeBefore.getHeight() != self._activeLayoutSize.getHeight()
            ):
                Util.notifyParentOfSizeChange(self, False)

    def updateAlignmentsAndExpandRatios(self, uidl, renderedWidgets):
        self._alignments = uidl.getMapAttribute('alignments')
        # UIDL contains a map of paintable ids to expand ratios
        self._expandRatios = uidl.getMapAttribute('expandRatios')
        self._expandRatioSum = -1.0
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(renderedWidgets)):
                break
            widget = renderedWidgets[i]
            pid = self.client.getPid(widget.getElement())
            container = self.getComponentContainer(widget)
            # Calculate alignment info
            container.setAlignment(self.getAlignment(pid))
            # Update expand ratio
            container.setNormalizedExpandRatio(self.getExpandRatio(pid))

    def getAlignment(self, pid):
        if pid in self._alignments:
            return AlignmentInfo(self._alignments.getInt(pid))
        else:
            return AlignmentInfo.TOP_LEFT

    def getExpandRatio(self, pid):
        if self._expandRatioSum < 0:
            self._expandRatioSum = 0
            keyArray = self._expandRatios.getKeyArray()
            length = len(keyArray)
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < length):
                    break
                self._expandRatioSum += self._expandRatios.getRawNumber(keyArray.get(i))
            if self._expandRatioSum == 0:
                # by default split equally among components
                self._defaultExpandRatio = 1.0 / len(self.widgetToComponentContainer)
            else:
                self._defaultExpandRatio = 0
        if pid in self._expandRatios:
            return self._expandRatios.getRawNumber(pid) / self._expandRatioSum
        else:
            return self._defaultExpandRatio

    def updateCaption(self, component, uidl):
        componentContainer = self.getComponentContainer(component)
        componentContainer.updateCaption(uidl, self.client)
        if not self._isRendering:
            # This was a component-only update and the possible size change
            # must be propagated to the layout

            self.client.captionSizeUpdated(component)

    def getComponent(self, element):
        """Returns the deepest nested child component which contains "element". The
        child component is also returned if "element" is part of its caption.

        @param element
                   An element that is a nested sub element of the root element in
                   this layout
        @return The Paintable which the element is a part of. Null if the element
                belongs to the layout and not to a child.
        """
        return Util.getPaintableForElement(self.client, self, element)
