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

from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
from com.vaadin.terminal.gwt.client.ui.AlignmentInfo import (AlignmentInfo,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.layout.CellBasedLayout import (CellBasedLayout,)
from com.vaadin.terminal.gwt.client.VCaption import (VCaption,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
# from com.google.gwt.dom.client.DivElement import (DivElement,)
# from com.google.gwt.dom.client.Document import (Document,)
# from com.google.gwt.dom.client.Element import (Element,)
# from com.google.gwt.dom.client.TableElement import (TableElement,)
# from com.google.gwt.user.client.ui.Panel import (Panel,)
# from com.google.gwt.user.client.ui.Widget import (Widget,)
# from java.util.Iterator import (Iterator,)
# from java.util.NoSuchElementException import (NoSuchElementException,)
Size = RenderInformation.Size


class ChildComponentContainer(Panel):
    # Size of the container DIV excluding any margins and also excluding the
    # expansion amount (containerExpansion)

    _contSize = Size(0, 0)
    # Size of the widget inside the container DIV
    _widgetSize = Size(0, 0)
    # Size of the caption
    _captionRequiredWidth = 0
    _captionWidth = 0
    _captionHeight = 0
    # Padding added to the container when it is larger than the component.
    _containerExpansion = Size(0, 0)
    _expandRatio = None
    # private int containerMarginLeft = 0;
    _containerMarginTop = 0
    _alignment = AlignmentInfo.TOP_LEFT
    _alignmentLeftOffsetForWidget = 0
    _alignmentLeftOffsetForCaption = 0
    # Top offset for implementing alignment. Top offset is set to the container
    # DIV as it otherwise would have to be set to either the Caption or the
    # Widget depending on whether there is a caption and where the caption is
    # located.

    _alignmentTopOffset = 0
    # private Margins alignmentOffset = new Margins(0, 0, 0, 0);
    _caption = None
    _containerDIV = None
    _widgetDIV = None
    _widget = None
    _relativeSize = None

    def __init__(self, widget, orientation):
        super(ChildComponentContainer, self)()
        self._containerDIV = Document.get().createDivElement()
        self._widgetDIV = Document.get().createDivElement()
        if BrowserInfo.get().isFF2():
            # Style style = widgetDIV.getStyle();
            # FF2 chokes on some floats very easily. Measuring size escpecially
            # becomes terribly slow
            tableEl = Document.get().createTableElement()
            tableEl.setInnerHTML('<tbody><tr><td><div></div></td></tr></tbody>')
            div = tableEl.getFirstChildElement().getFirstChildElement().getFirstChildElement().getFirstChildElement()
            tableEl.setCellPadding(0)
            tableEl.setCellSpacing(0)
            tableEl.setBorder(0)
            div.getStyle().setProperty('padding', '0')
            self.setElement(tableEl)
            self._containerDIV = div
        else:
            self.setFloat(self._widgetDIV, 'left')
            self.setElement(self._containerDIV)
            self._containerDIV.getStyle().setProperty('height', '0')
            self._containerDIV.getStyle().setProperty('width', '0px')
            self._containerDIV.getStyle().setProperty('overflow', 'hidden')
        if BrowserInfo.get().isIE():
            # IE requires position: relative on overflow:hidden elements if
            # they should hide position:relative elements. Without this e.g. a
            # 1000x1000 Panel inside an 500x500 OrderedLayout will not be
            # clipped but fully shown.

            self._containerDIV.getStyle().setProperty('position', 'relative')
            self._widgetDIV.getStyle().setProperty('position', 'relative')
        self._containerDIV.appendChild(self._widgetDIV)
        self.setOrientation(orientation)
        self.setWidget(widget)

    def setWidget(self, w):
        # Validate
        if w == self._widget:
            return
        # Detach new child.
        if w is not None:
            w.removeFromParent()
        # Remove old child.
        if self._widget is not None:
            self.remove(self._widget)
        # Logical attach.
        self._widget = w
        if w is not None:
            # Physical attach.
            self._widgetDIV.appendChild(self._widget.getElement())
            self.adopt(w)

    @classmethod
    def setFloat(cls, div, floatString):
        if BrowserInfo.get().isIE():
            div.getStyle().setProperty('styleFloat', floatString)
            # IE requires display:inline for margin-left to work together
            # with float:left
            if floatString == 'left':
                div.getStyle().setProperty('display', 'inline')
            else:
                div.getStyle().setProperty('display', 'block')
        else:
            div.getStyle().setProperty('cssFloat', floatString)

    def setOrientation(self, orientation):
        if orientation == CellBasedLayout.ORIENTATION_HORIZONTAL:
            self.setFloat(self.getElement(), 'left')
        else:
            self.setFloat(self.getElement(), '')
        self.setHeight('0px')
        # setWidth("0px");
        self._contSize.setHeight(0)
        self._contSize.setWidth(0)
        # containerMarginLeft = 0;
        self._containerMarginTop = 0
        self._containerDIV.getStyle().setProperty('paddingLeft', '0')
        self._containerDIV.getStyle().setProperty('paddingTop', '0')
        self._containerExpansion.setHeight(0)
        self._containerExpansion.setWidth(0)
        # Clear old alignments
        self.clearAlignments()

    def renderChild(self, childUIDL, client, fixedWidth):
        # Must remove width specification from container before rendering to
        # allow components to grow in horizontal direction.
        # 
        # For fixed width layouts we specify the width directly so that height
        # is automatically calculated correctly (e.g. for Labels).

        # This should no longer be needed (after #2563) as all components are
        # such that they can be rendered inside a 0x0 DIV.
        # 
        # The exception seems to be complex components (Tree and Table) on
        # Opera (#3444).

        if fixedWidth < 0 and BrowserInfo.get().isOpera():
            self.setUnlimitedContainerWidth()
        self._widget.updateFromUIDL(childUIDL, client)

    def setUnlimitedContainerWidth(self):
        self.setLimitedContainerWidth(1000000)

    def setLimitedContainerWidth(self, width):
        self._containerDIV.getStyle().setProperty('width', width + 'px')

    def updateWidgetSize(self):
        # Widget wrapper includes margin which the widget offsetWidth/Height
        # does not include

        w = Util.getRequiredWidth(self._widgetDIV)
        h = Util.getRequiredHeight(self._widgetDIV)
        self._widgetSize.setWidth(w)
        self._widgetSize.setHeight(h)
        # ApplicationConnection.getConsole().log(
        # Util.getSimpleName(widget) + " size is " + w + "," + h);

    def setMarginLeft(self, marginLeft):
        # containerMarginLeft = marginLeft;
        self._containerDIV.getStyle().setPropertyPx('paddingLeft', marginLeft)

    def setMarginTop(self, marginTop):
        self._containerMarginTop = marginTop
        self._containerDIV.getStyle().setPropertyPx('paddingTop', marginTop + self._alignmentTopOffset)
        self.updateContainerDOMSize()

    def updateAlignments(self, parentWidth, parentHeight):
        if parentHeight == -1:
            parentHeight = self._contSize.getHeight()
        if parentWidth == -1:
            parentWidth = self._contSize.getWidth()
        self._alignmentTopOffset = self.calculateVerticalAlignmentTopOffset(parentHeight)
        self.calculateHorizontalAlignment(parentWidth)
        self.applyAlignments()

    def applyAlignments(self):
        # Update top margin to take alignment into account
        self.setMarginTop(self._containerMarginTop)
        if self._caption is not None:
            self._caption.getElement().getStyle().setPropertyPx('marginLeft', self._alignmentLeftOffsetForCaption)
        self._widgetDIV.getStyle().setPropertyPx('marginLeft', self._alignmentLeftOffsetForWidget)

    def getCaptionRequiredWidth(self):
        if self._caption is None:
            return 0
        return self._captionRequiredWidth

    def getCaptionWidth(self):
        if self._caption is None:
            return 0
        return self._captionWidth

    def getCaptionHeight(self):
        if self._caption is None:
            return 0
        return self._captionHeight

    def getCaptionWidthAfterComponent(self):
        if (
            (self._caption is None) or (not self._caption.shouldBePlacedAfterComponent())
        ):
            return 0
        return self.getCaptionWidth()

    def getCaptionHeightAboveComponent(self):
        if (self._caption is None) or self._caption.shouldBePlacedAfterComponent():
            return 0
        return self.getCaptionHeight()

    def calculateVerticalAlignmentTopOffset(self, emptySpace):
        if self._alignment.isTop():
            return 0
        if self._caption is not None:
            if self._caption.shouldBePlacedAfterComponent():
                # Take into account the rare case that the caption on the right
                # side of the component AND is higher than the component

                emptySpace -= self.Math.max(self._widgetSize.getHeight(), self._caption.getHeight())
            else:
                emptySpace -= self._widgetSize.getHeight()
                emptySpace -= self.getCaptionHeight()
        else:
            # There is no caption and thus we do not need to take anything but
            # the widget into account

            emptySpace -= self._widgetSize.getHeight()
        top = 0
        if self._alignment.isVerticalCenter():
            top = emptySpace / 2
        elif self._alignment.isBottom():
            top = emptySpace
        if top < 0:
            top = 0
        return top

    def calculateHorizontalAlignment(self, emptySpace):
        self._alignmentLeftOffsetForCaption = 0
        self._alignmentLeftOffsetForWidget = 0
        if self._alignment.isLeft():
            return
        captionSpace = emptySpace
        widgetSpace = emptySpace
        if self._caption is not None:
            # There is a caption
            if self._caption.shouldBePlacedAfterComponent():
                # The caption is after component. In this case the caption
                # needs no alignment.

                captionSpace = 0
                widgetSpace -= self._widgetSize.getWidth()
                widgetSpace -= self.getCaptionWidth()
            else:
                # The caption is above the component. Caption and widget needs
                # separate alignment offsets.

                widgetSpace -= self._widgetSize.getWidth()
                captionSpace -= self.getCaptionWidth()
        else:
            # There is no caption and thus we do not need to take anything but
            # the widget into account

            captionSpace = 0
            widgetSpace -= self._widgetSize.getWidth()
        if self._alignment.isHorizontalCenter():
            self._alignmentLeftOffsetForCaption = captionSpace / 2
            self._alignmentLeftOffsetForWidget = widgetSpace / 2
        elif self._alignment.isRight():
            self._alignmentLeftOffsetForCaption = captionSpace
            self._alignmentLeftOffsetForWidget = widgetSpace
        if self._alignmentLeftOffsetForCaption < 0:
            self._alignmentLeftOffsetForCaption = 0
        if self._alignmentLeftOffsetForWidget < 0:
            self._alignmentLeftOffsetForWidget = 0

    def setAlignment(self, alignmentInfo):
        self._alignment = alignmentInfo

    def getWidgetSize(self):
        return self._widgetSize

    def updateCaption(self, uidl, client):
        if VCaption.isNeeded(uidl):
            # We need a caption
            newCaption = self._caption
            if newCaption is None:
                newCaption = VCaption(self._widget, client)
                # Set initial height to avoid Safari flicker
                newCaption.setHeight('18px')
                # newCaption.setHeight(newCaption.getHeight()); // This might
                # be better... ??
                if BrowserInfo.get().isIE():
                    # Must attach caption here so IE sends an immediate onload
                    # event for images coming from the cache

                    self.setCaption(newCaption)
            positionChanged = newCaption.updateCaption(uidl)
            if (newCaption != self._caption) or positionChanged:
                self.setCaption(newCaption)
        elif self._caption is not None:
            self.remove(self._caption)
        # Caption is not needed
        self.updateCaptionSize()
        if self._relativeSize is None:
            # relativeSize may be null if component is updated via independent
            # update, after it has initially been hidden. See #4608
            # 
            # It might also change in which case there would be similar issues.
            # 
            # Yes, it is an ugly hack. Don't come telling me about it.

            self.setRelativeSize(Util.parseRelativeSize(uidl))

    def updateCaptionSize(self):
        self._captionWidth = 0
        self._captionHeight = 0
        if self._caption is not None:
            self._captionWidth = self._caption.getRenderedWidth()
            self._captionHeight = self._caption.getHeight()
            self._captionRequiredWidth = self._caption.getRequiredWidth()
            # ApplicationConnection.getConsole().log(
            # "Caption rendered width: " + captionWidth +
            # ", caption required width: " + captionRequiredWidth +
            # ", caption height: " + captionHeight);

    def setCaption(self, newCaption):
        # Validate
        # if (newCaption == caption) {
        # return;
        # }
        # Detach new child.
        if newCaption is not None:
            newCaption.removeFromParent()
        # Remove old child.
        if self._caption is not None and newCaption != self._caption:
            self.remove(self._caption)
        # Logical attach.
        self._caption = newCaption
        if self._caption is not None:
            # Physical attach.
            if self._caption.shouldBePlacedAfterComponent():
                Util.setFloat(self._caption.getElement(), 'left')
                self._containerDIV.appendChild(self._caption.getElement())
            else:
                Util.setFloat(self._caption.getElement(), '')
                self._containerDIV.insertBefore(self._caption.getElement(), self._widgetDIV)
            self.adopt(self._caption)

    def remove(self, child):
        # Validate
        if child != self._caption and child != self._widget:
            return False
        # Orphan
        self.orphan(child)
        # Physical && Logical Detach
        if child == self._caption:
            self._containerDIV.removeChild(child.getElement())
            self._caption = None
        else:
            self._widgetDIV.removeChild(child.getElement())
            self._widget = None
        return True

    def iterator(self):
        return self.ChildComponentContainerIterator()

    def ChildComponentContainerIterator(ChildComponentContainer_this, *args, **kwargs):

        class ChildComponentContainerIterator(Iterator):
            _id = 0

            def hasNext(self):
                return self._id < len(ChildComponentContainer_this)

            def next(self):
                w = self.get(self._id)
                self._id += 1
                return w

            def get(self, i):
                if i == 0:
                    if ChildComponentContainer_this._widget is not None:
                        return ChildComponentContainer_this._widget
                    elif ChildComponentContainer_this._caption is not None:
                        return ChildComponentContainer_this._caption
                    else:
                        raise NoSuchElementException()
                elif i == 1:
                    if (
                        ChildComponentContainer_this._widget is not None and ChildComponentContainer_this._caption is not None
                    ):
                        return ChildComponentContainer_this._caption
                    else:
                        raise NoSuchElementException()
                else:
                    raise NoSuchElementException()

            def remove(self):
                toRemove = self._id - 1
                if toRemove == 0:
                    if ChildComponentContainer_this._widget is not None:
                        ChildComponentContainer_this.remove(ChildComponentContainer_this._widget)
                    elif ChildComponentContainer_this._caption is not None:
                        ChildComponentContainer_this.remove(ChildComponentContainer_this._caption)
                    else:
                        raise self.IllegalStateException()
                elif toRemove == 1:
                    if (
                        ChildComponentContainer_this._widget is not None and ChildComponentContainer_this._caption is not None
                    ):
                        ChildComponentContainer_this.remove(ChildComponentContainer_this._caption)
                    else:
                        raise self.IllegalStateException()
                else:
                    raise self.IllegalStateException()
                self._id -= 1

        return ChildComponentContainerIterator(*args, **kwargs)

    def size(self):
        if self._widget is not None:
            if self._caption is not None:
                return 2
            else:
                return 1
        elif self._caption is not None:
            return 1
        else:
            return 0

    def getWidget(self):
        return self._widget

    def widgetHasSizeSpecified(self, orientation):
        """Return true if the size of the widget has been specified in the selected
        orientation.

        @return
        """
        if orientation == CellBasedLayout.ORIENTATION_HORIZONTAL:
            size = self._widget.getElement().getStyle().getProperty('width')
        else:
            size = self._widget.getElement().getStyle().getProperty('height')
        return size is not None and not (size == '')

    def isComponentRelativeSized(self, orientation):
        if self._relativeSize is None:
            return False
        if orientation == CellBasedLayout.ORIENTATION_HORIZONTAL:
            return self._relativeSize.getWidth() >= 0
        else:
            return self._relativeSize.getHeight() >= 0

    def setRelativeSize(self, relativeSize):
        self._relativeSize = relativeSize

    def getContSize(self):
        return self._contSize

    def clearAlignments(self):
        self._alignmentLeftOffsetForCaption = 0
        self._alignmentLeftOffsetForWidget = 0
        self._alignmentTopOffset = 0
        self.applyAlignments()

    def setNormalizedExpandRatio(self, expandRatio):
        """Sets the normalized expand ratio of this slot. The fraction that this
        slot will use of "excess space".

        @param expandRatio
        """
        self._expandRatio = expandRatio

    def expand(self, orientation, spaceForExpansion):
        expansionAmount = spaceForExpansion * self._expandRatio
        if orientation == CellBasedLayout.ORIENTATION_HORIZONTAL:
            # HORIZONTAL
            self._containerExpansion.setWidth(expansionAmount)
        else:
            # VERTICAL
            self._containerExpansion.setHeight(expansionAmount)
        return expansionAmount

    def expandExtra(self, orientation, extra):
        if orientation == CellBasedLayout.ORIENTATION_HORIZONTAL:
            # HORIZONTAL
            self._containerExpansion.setWidth(self._containerExpansion.getWidth() + extra)
        else:
            # VERTICAL
            self._containerExpansion.setHeight(self._containerExpansion.getHeight() + extra)

    def setContainerSize(self, widgetAndCaptionWidth, widgetAndCaptionHeight):
        containerWidth = widgetAndCaptionWidth
        containerWidth += self._containerExpansion.getWidth()
        containerHeight = widgetAndCaptionHeight
        containerHeight += self._containerExpansion.getHeight()
        # ApplicationConnection.getConsole().log(
        # "Setting container size for " + Util.getSimpleName(widget)
        # + " to " + containerWidth + "," + containerHeight);
        if containerWidth < 0:
            VConsole.log('containerWidth should never be negative: ' + containerWidth)
            containerWidth = 0
        if containerHeight < 0:
            VConsole.log('containerHeight should never be negative: ' + containerHeight)
            containerHeight = 0
        self._contSize.setWidth(containerWidth)
        self._contSize.setHeight(containerHeight)
        self.updateContainerDOMSize()

    def updateContainerDOMSize(self):
        width = self._contSize.getWidth()
        height = self._contSize.getHeight() - self._alignmentTopOffset
        if width < 0:
            width = 0
        if height < 0:
            height = 0
        self.setWidth(width + 'px')
        self.setHeight(height + 'px')
        # Also update caption max width
        if self._caption is not None:
            if self._caption.shouldBePlacedAfterComponent():
                self._caption.setMaxWidth(self._captionWidth)
            else:
                self._caption.setMaxWidth(width)
            self._captionWidth = self._caption.getRenderedWidth()
            # Remove initial height
            self._caption.setHeight('')
