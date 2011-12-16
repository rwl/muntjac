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

from pyjamas import DOM

from pyjamas.ui import Event

from pyjamas.ui.ComplexPanel import ComplexPanel

from muntjac.terminal.gwt.client.v_console import VConsole
from muntjac.terminal.gwt.client.container import IContainer
from muntjac.terminal.gwt.client.ui.touch_scroll_delegate import TouchScrollDelegate
from muntjac.terminal.gwt.client.render_space import RenderSpace
from muntjac.terminal.gwt.client.ui.click_event_handler import ClickEventHandler
from muntjac.terminal.gwt.client.container_resized_listener import IContainerResizedListener
from muntjac.terminal.gwt.client.util import Util
from muntjac.terminal.gwt.client.render_information import RenderInformation
from muntjac.terminal.gwt.client.browser_info import BrowserInfo
from muntjac.terminal.gwt.client.ui.v_overlay import VOverlay


class VSplitPanel(ComplexPanel, IContainer, IContainerResizedListener):

    CLASSNAME = 'v-splitpanel'
    SPLITTER_CLICK_EVENT_IDENTIFIER = 'sp_click'
    ORIENTATION_HORIZONTAL = 0
    ORIENTATION_VERTICAL = 1
    _MIN_SIZE = 30

    def __init__(self, orientation=None):
        self.clickEventHandler = SPClickEventHandler()
        self._enabled = False
        self._orientation = self.ORIENTATION_HORIZONTAL
        self._firstChild = None
        self._secondChild = None
        self._wrapper = DOM.createDiv()
        self._firstContainer = DOM.createDiv()
        self._secondContainer = DOM.createDiv()
        self._splitter = DOM.createDiv()
        self._resizing = None
        self._resized = False
        self._origX = None
        self._origY = None
        self._origMouseX = None
        self._origMouseY = None
        self._locked = False
        self._positionReversed = False
        self._componentStyleNames = None
        self._draggingCurtain = None
        self._client = None
        self._width = ''
        self._height = ''
        self._firstRenderSpace = RenderSpace(0, 0, True)
        self._secondRenderSpace = RenderSpace(0, 0, True)
        self._renderInformation = RenderInformation()
        self._id = None
        self._immediate = None
        self._rendering = False
        # The current position of the split handle in either percentages or pixels
        self._position = None
        self.scrolledContainer = None
        self.origScrollTop = None
        self._touchScrollDelegate = None

        self._splitterSize = -1

        if orientation is None:
            orientation = self.ORIENTATION_HORIZONTAL

        self.setElement(DOM.createDiv())

        if orientation == self.ORIENTATION_HORIZONTAL:
            self.setStyleName(self.CLASSNAME + '-horizontal')
        else:
            self.setStyleName(self.CLASSNAME + '-vertical')

        # size below will be overridden in update from uidl, initial size
        # needed to keep IE alive
        self.setWidth(self._MIN_SIZE + 'px')
        self.setHeight(self._MIN_SIZE + 'px')
        self.constructDom()
        self.setOrientation(orientation)
        self.sinkEvents(Event.MOUSEEVENTS)

        class _1_(TouchCancelHandler):

            def onTouchCancel(self, event):
                # TODO When does this actually happen??
                VConsole.log('TOUCH CANCEL')

        _1_ = _1_()
        self.addDomHandler(_1_, TouchCancelEvent.getType())

        class _2_(TouchStartHandler):

            def onTouchStart(self, event):
                target = event.getTouches().get(0).getTarget()
                if VSplitPanel_this._splitter.isOrHasChild(target):
                    VSplitPanel_this.onMouseDown(Event.as_(event.getNativeEvent()))
                else:
                    VSplitPanel_this.getTouchScrollDelegate().onTouchStart(event)

        _2_ = _2_()
        self.addDomHandler(_2_, TouchStartEvent.getType())

        class _3_(TouchMoveHandler):

            def onTouchMove(self, event):
                if VSplitPanel_this._resizing:
                    VSplitPanel_this.onMouseMove(Event.as_(event.getNativeEvent()))

        _3_ = _3_()
        self.addDomHandler(_3_, TouchMoveEvent.getType())

        class _4_(TouchEndHandler):

            def onTouchEnd(self, event):
                if VSplitPanel_this._resizing:
                    VSplitPanel_this.onMouseUp(Event.as_(event.getNativeEvent()))

        _4_ = _4_()
        self.addDomHandler(_4_, TouchEndEvent.getType())


    def getTouchScrollDelegate(self):
        if self._touchScrollDelegate is None:
            self._touchScrollDelegate = TouchScrollDelegate(
                    self._firstContainer, self._secondContainer)
        return self._touchScrollDelegate


    def constructDom(self):
        DOM.appendChild(self._splitter, DOM.createDiv())
        # for styling
        DOM.appendChild(self.getElement(), self._wrapper)
        DOM.setStyleAttribute(self._wrapper, 'position', 'relative')
        DOM.setStyleAttribute(self._wrapper, 'width', '100%')
        DOM.setStyleAttribute(self._wrapper, 'height', '100%')
        DOM.appendChild(self._wrapper, self._secondContainer)
        DOM.appendChild(self._wrapper, self._firstContainer)
        DOM.appendChild(self._wrapper, self._splitter)
        DOM.setStyleAttribute(self._splitter, 'position', 'absolute')
        DOM.setStyleAttribute(self._secondContainer, 'position', 'absolute')
        DOM.setStyleAttribute(self._firstContainer, 'overflow', 'auto')
        DOM.setStyleAttribute(self._secondContainer, 'overflow', 'auto')


    def setOrientation(self, orientation):
        self._orientation = orientation

        if orientation == self.ORIENTATION_HORIZONTAL:
            DOM.setStyleAttribute(self._splitter, 'height', '100%')
            DOM.setStyleAttribute(self._splitter, 'top', '0')
            DOM.setStyleAttribute(self._firstContainer, 'height', '100%')
            DOM.setStyleAttribute(self._secondContainer, 'height', '100%')
        else:
            DOM.setStyleAttribute(self._splitter, 'width', '100%')
            DOM.setStyleAttribute(self._splitter, 'left', '0')
            DOM.setStyleAttribute(self._firstContainer, 'width', '100%')
            DOM.setStyleAttribute(self._secondContainer, 'width', '100%')

        DOM.setElemAttribute(self._firstContainer, 'className',
                self.CLASSNAME + '-first-container')
        DOM.setElemAttribute(self._secondContainer, 'className',
                self.CLASSNAME + '-second-container')


    def updateFromUIDL(self, uidl, client):
        self._client = client
        self._id = uidl.getId()
        self._rendering = True

        self._immediate = uidl.hasAttribute('immediate')

        if client.updateComponent(self, uidl, True):
            self._rendering = False
            return
        self.setEnabled(not uidl.getBooleanAttribute('disabled'))

        self.clickEventHandler.handleEventHandlerRegistration(client)
        if uidl.hasAttribute('style'):
            self._componentStyleNames = \
                    uidl.getStringAttribute('style').split(' ')
        else:
            self._componentStyleNames = []

        self.setLocked(uidl.getBooleanAttribute('locked'))
        self.setPositionReversed(uidl.getBooleanAttribute('reversed'))

        self.setStylenames()

        self._position = uidl.getStringAttribute('position')
        self.setSplitPosition(self._position)

        newFirstChild = client.getPaintable(uidl.getChildUIDL(0))
        newSecondChild = client.getPaintable(uidl.getChildUIDL(1))

        if self._firstChild != newFirstChild:
            if self._firstChild is not None:
                client.unregisterPaintable(self._firstChild)
            self.setFirstWidget(newFirstChild)
        if self._secondChild != newSecondChild:
            if self._secondChild is not None:
                client.unregisterPaintable(self._secondChild)
            self.setSecondWidget(newSecondChild)

        newFirstChild.updateFromUIDL(uidl.getChildUIDL(0), client)
        newSecondChild.updateFromUIDL(uidl.getChildUIDL(1), client)

        self._renderInformation.updateSize(self.getElement())

        if BrowserInfo.get().isIE7():
            # Part III of IE7 hack
            class _5_(Command):

                def execute(self):
                    VSplitPanel_this.iLayout()

            _5_ = _5_()
            Scheduler.get().scheduleDeferred(_5_)

        # This is needed at least for cases like #3458 to take
        # appearing/disappearing scrollbars into account.
        client.runDescendentsLayout(self)

        self._rendering = False


    def remove(self, w):
        removed = super(VSplitPanel, self).remove(w)
        if removed:
            if self._firstChild == w:
                self._firstChild = None
            else:
                self._secondChild = None
        return removed


    def setLocked(self, newValue):
        if self._locked != newValue:
            self._locked = newValue
            self._splitterSize = -1
            self.setStylenames()


    def setPositionReversed(self, reversed):
        if self._positionReversed != reversed:
            if self._orientation == self.ORIENTATION_HORIZONTAL:
                DOM.setStyleAttribute(self._splitter, 'right', '')
                DOM.setStyleAttribute(self._splitter, 'left', '')
            elif self._orientation == self.ORIENTATION_VERTICAL:
                DOM.setStyleAttribute(self._splitter, 'top', '')
                DOM.setStyleAttribute(self._splitter, 'bottom', '')
            self._positionReversed = reversed


    def setSplitPosition(self, pos):
        if pos is None:
            return

        # Convert percentage values to pixels
        if pos.find('%') > 0:
            pos = ((float(pos[:-1]) / 100) * (self.getOffsetWidth() if self._orientation == self.ORIENTATION_HORIZONTAL else self.getOffsetHeight())) + 'px'

        if self._orientation == self.ORIENTATION_HORIZONTAL:
            if self._positionReversed:
                DOM.setStyleAttribute(self._splitter, 'right', pos)
            else:
                DOM.setStyleAttribute(self._splitter, 'left', pos)
        elif self._positionReversed:
            DOM.setStyleAttribute(self._splitter, 'bottom', pos)
        else:
            DOM.setStyleAttribute(self._splitter, 'top', pos)

        self.iLayout()
        self._client.runDescendentsLayout(self)


    def iLayout(self):
        # Calculates absolutely positioned container places/sizes
        if not self.isAttached():
            return

        self._renderInformation.updateSize(self.getElement())

        orientation = self._orientation

        if orientation == self.ORIENTATION_HORIZONTAL:
            wholeSize = DOM.getIntElemAttribute(self._wrapper, 'clientWidth')
            pixelPosition = DOM.getIntElemAttribute(self._splitter,
                    'offsetLeft')

            # reposition splitter in case it is out of box
            if ((pixelPosition > 0
                    and pixelPosition + self.getSplitterSize() > wholeSize)
                    or (self._positionReversed and pixelPosition < 0)):
                pixelPosition = wholeSize - self.getSplitterSize()
                if pixelPosition < 0:
                    pixelPosition = 0
                self.setSplitPosition(pixelPosition + 'px')
                return

            DOM.setStyleAttribute(self._firstContainer, 'width',
                    pixelPosition + 'px')
            secondContainerWidth = (wholeSize - pixelPosition
                    - self.getSplitterSize())

            if secondContainerWidth < 0:
                secondContainerWidth = 0

            DOM.setStyleAttribute(self._secondContainer,
                    'width', secondContainerWidth + 'px')
            DOM.setStyleAttribute(self._secondContainer,
                    'left', pixelPosition + self.getSplitterSize() + 'px')

            contentHeight = self._renderInformation.getRenderedSize().getHeight()
            self._firstRenderSpace.setHeight(contentHeight)
            self._firstRenderSpace.setWidth(pixelPosition)
            self._secondRenderSpace.setHeight(contentHeight)
            self._secondRenderSpace.setWidth(secondContainerWidth)

        elif orientation == self.ORIENTATION_VERTICAL:
            wholeSize = DOM.getIntElemAttribute(self._wrapper,
                    'clientHeight')
            pixelPosition = DOM.getIntElemAttribute(self._splitter,
                    'offsetTop')

            # reposition splitter in case it is out of box
            if ((pixelPosition > 0
                    and pixelPosition + self.getSplitterSize() > wholeSize)
                    or (self._positionReversed and pixelPosition < 0)):
                pixelPosition = wholeSize - self.getSplitterSize()
                if pixelPosition < 0:
                    pixelPosition = 0
                self.setSplitPosition(pixelPosition + 'px')
                return

            DOM.setStyleAttribute(self._firstContainer, 'height',
                    pixelPosition + 'px')
            secondContainerHeight = (wholeSize - pixelPosition
                    - self.getSplitterSize())

            if secondContainerHeight < 0:
                secondContainerHeight = 0

            DOM.setStyleAttribute(self._secondContainer, 'height',
                    secondContainerHeight + 'px')
            DOM.setStyleAttribute(self._secondContainer, 'top',
                    pixelPosition + self.getSplitterSize() + 'px')

            contentWidth = self._renderInformation.getRenderedSize().getWidth()
            self._firstRenderSpace.setHeight(pixelPosition)
            self._firstRenderSpace.setWidth(contentWidth)
            self._secondRenderSpace.setHeight(secondContainerHeight)
            self._secondRenderSpace.setWidth(contentWidth)

        # fixes scrollbars issues on webkit based browsers
        Util.runWebkitOverflowAutoFix(self._secondContainer)
        Util.runWebkitOverflowAutoFix(self._firstContainer)


    def setFirstWidget(self, w):
        if self._firstChild is not None:
            self._firstChild.removeFromParent()
        super(VSplitPanel, self).add(w, self._firstContainer)
        self._firstChild = w


    def setSecondWidget(self, w):
        if self._secondChild is not None:
            self._secondChild.removeFromParent()
        super(VSplitPanel, self).add(w, self._secondContainer)
        self._secondChild = w


    def onBrowserEvent(self, event):
        etype = DOM.eventGetType(event)

        if etype == Event.ONMOUSEMOVE:
            if self._resizing:
                self.onMouseMove(event)
        elif etype == Event.ONMOUSEDOWN:
            self.onMouseDown(event)
        elif etype == Event.ONMOUSEOUT:
            if self._resizing:
                self.showDraggingCurtain()
        elif etype == Event.ONMOUSEUP:
            if self._resizing:
                self.onMouseUp(event)
        elif etype == Event.ONCLICK:
            self._resizing = False

        # Only fire click event listeners if the splitter isn't moved
        if Util.isTouchEvent(event) or (not self._resized):
            super(VSplitPanel, self).onBrowserEvent(event)
        elif DOM.eventGetType(event) == Event.ONMOUSEUP:
            # Reset the resized flag after a mouseup has occured so the next
            # mousedown/mouseup can be interpreted as a click.
            self._resized = False


    def onMouseDown(self, event):
        if self._locked or (not self.isEnabled()):
            return

        trg = event.getEventTarget()
        if (trg == self._splitter) or (trg == DOM.getChild(self._splitter, 0)):
            self._resizing = True
            DOM.setCapture(self.getElement())
            self._origX = DOM.getIntElemAttribute(self._splitter, 'offsetLeft')
            self._origY = DOM.getIntElemAttribute(self._splitter, 'offsetTop')
            self._origMouseX = Util.getTouchOrMouseClientX(event)
            self._origMouseY = Util.getTouchOrMouseClientY(event)
            event.stopPropagation()
            event.preventDefault()


    def onMouseMove(self, event):
        orientation = self._orientation
        if orientation == self.ORIENTATION_HORIZONTAL:
            x = Util.getTouchOrMouseClientX(event)
            self.onHorizontalMouseMove(x)
        #elif orientation == self.ORIENTATION_VERTICAL:
        #    pass
        else:
            y = Util.getTouchOrMouseClientY(event)
            self.onVerticalMouseMove(y)


    def onHorizontalMouseMove(self, x):
        newX = (self._origX + x) - self._origMouseX
        if newX < 0:
            newX = 0

        if newX + self.getSplitterSize() > self.getOffsetWidth():
            newX = self.getOffsetWidth() - self.getSplitterSize()

        if self._position.find('%') > 0:
            pos = newX
            # 100% needs special handling
            if newX + self.getSplitterSize() >= self.getOffsetWidth():
                pos = self.getOffsetWidth()
            # Reversed position
            if self._positionReversed:
                pos = self.getOffsetWidth() - pos
            self._position = ((pos / self.getOffsetWidth()) * 100) + '%'
        elif self._positionReversed:
            self._position = (self.getOffsetWidth() - newX
                    - self.getSplitterSize()) + 'px'
        else:
            self._position = newX + 'px'

        # Reversed position
        if self._origX != newX:
            self._resized = True

        # Reversed position
        if self._positionReversed:
            newX = self.getOffsetWidth() - newX - self.getSplitterSize()

        self.setSplitPosition(newX + 'px')


    def onVerticalMouseMove(self, y):
        newY = (self._origY + y) - self._origMouseY
        if newY < 0:
            newY = 0

        if newY + self.getSplitterSize() > self.getOffsetHeight():
            newY = self.getOffsetHeight() - self.getSplitterSize()

        if self._position.find('%') > 0:
            pos = newY
            # 100% needs special handling
            if newY + self.getSplitterSize() >= self.getOffsetHeight():
                pos = self.getOffsetHeight()
            # Reversed position
            if self._positionReversed:
                pos = self.getOffsetHeight() - pos - self.getSplitterSize()
            self._position = ((pos / self.getOffsetHeight()) * 100) + '%'
        elif self._positionReversed:
            self._position = (self.getOffsetHeight() - newY
                    - self.getSplitterSize()) + 'px'
        else:
            self._position = newY + 'px'

        # Reversed position
        if self._origY != newY:
            self._resized = True

        # Reversed position
        if self._positionReversed:
            newY = self.getOffsetHeight() - newY - self.getSplitterSize()

        self.setSplitPosition(newY + 'px')


    def onMouseUp(self, event):
        DOM.releaseCapture(self.getElement())
        self.hideDraggingCurtain()
        self._resizing = False
        if not Util.isTouchEvent(event):
            self.onMouseMove(event)
        self.updateSplitPositionToServer()


    def showDraggingCurtain(self):
        """Used in FF to avoid losing mouse capture when pointer is moved on
        an iframe.
        """
        if not self.isDraggingCurtainRequired():
            return

        if self._draggingCurtain is None:
            self._draggingCurtain = DOM.createDiv()
            DOM.setStyleAttribute(self._draggingCurtain, 'position',
                    'absolute')
            DOM.setStyleAttribute(self._draggingCurtain, 'top', '0px')
            DOM.setStyleAttribute(self._draggingCurtain, 'left', '0px')
            DOM.setStyleAttribute(self._draggingCurtain, 'width', '100%')
            DOM.setStyleAttribute(self._draggingCurtain, 'height', '100%')
            DOM.setStyleAttribute(self._draggingCurtain, 'zIndex',
                    str(VOverlay.Z_INDEX))
            DOM.appendChild(self._wrapper, self._draggingCurtain)


    def isDraggingCurtainRequired(self):
        """A dragging curtain is required in Gecko and Webkit.

        @return: true if the browser requires a dragging curtain
        """
        return BrowserInfo.get().isGecko() or BrowserInfo.get().isWebkit()


    def hideDraggingCurtain(self):
        """Hides dragging curtain"""
        if self._draggingCurtain is not None:
            DOM.removeChild(self._wrapper, self._draggingCurtain)
            self._draggingCurtain = None


    def getSplitterSize(self):
        if self._splitterSize < 0:
            if self.isAttached():
                orientation = self._orientation
                if orientation == self.ORIENTATION_HORIZONTAL:
                    self._splitterSize = DOM.getIntElemAttribute(
                            self._splitter, 'offsetWidth')
                else:
                    self._splitterSize = DOM.getIntElemAttribute(
                            self._splitter, 'offsetHeight')

        return self._splitterSize


    def setHeight(self, height):
        if self._height == height:
            return

        self._height = height
        super(VSplitPanel, self).setHeight(height)

        if not self._rendering and self._client is not None:
            self.setSplitPosition(self._position)


    def setWidth(self, width):
        if self._width == width:
            return

        self._width = width
        super(VSplitPanel, self).setWidth(width)
        if not self._rendering and self._client is not None:
            self.setSplitPosition(self._position)


    def getAllocatedSpace(self, child):
        if child == self._firstChild:
            return self._firstRenderSpace
        elif child == self._secondChild:
            return self._secondRenderSpace
        return None


    def hasChildComponent(self, component):
        return (component is not None
                and (component == self._firstChild)
                or (component == self._secondChild))


    def replaceChildComponent(self, oldComponent, newComponent):
        if oldComponent == self._firstChild:
            self.setFirstWidget(newComponent)
        elif oldComponent == self._secondChild:
            self.setSecondWidget(newComponent)


    def requestLayout(self, child):
        # content size change might cause change to its available space
        # (scrollbars)
        for paintable in child:
            self._client.handleComponentRelativeSize(paintable)

        if self._height is not None and self._width is not None:
            # If the height and width has been specified the child components
            # cannot make the size of the layout change
            return True

        if self._renderInformation.updateSize(self.getElement()):
            return False
        else:
            return True


    def updateCaption(self, component, uidl):
        # TODO: Implement caption handling
        pass


    def updateSplitPositionToServer(self):
        """Updates the new split position back to server."""
        pos = 0
        if self._position.find('%') > 0:
            pos = round(float(self._position[:len(self._position) - 1]))
        else:
            pos = int(self._position[:len(self._position) - 2])

        self._client.updateVariable(self._id, 'position', pos, self._immediate)


    def setStylenames(self):
        splitterSuffix = '-hsplitter' if self._orientation == self.ORIENTATION_HORIZONTAL else '-vsplitter'
        firstContainerSuffix = '-first-container'
        secondContainerSuffix = '-second-container'
        lockedSuffix = ''
        splitterStyle = self.CLASSNAME + splitterSuffix
        firstStyle = self.CLASSNAME + firstContainerSuffix
        secondStyle = self.CLASSNAME + secondContainerSuffix
        if self._locked:
            splitterStyle = self.CLASSNAME + splitterSuffix + '-locked'
            lockedSuffix = '-locked'

        for i in range(len(self._componentStyleNames)):
            splitterStyle += (' ' + self.CLASSNAME + splitterSuffix + '-'
                    + self._componentStyleNames[i] + lockedSuffix)
            firstStyle += (' ' + self.CLASSNAME + firstContainerSuffix + '-'
                    + self._componentStyleNames[i])
            secondStyle += (' ' + self.CLASSNAME + secondContainerSuffix + '-'
                    + self._componentStyleNames[i])

        DOM.setElemAttribute(self._splitter, 'className', splitterStyle)
        DOM.setElemAttribute(self._firstContainer, 'className', firstStyle)
        DOM.setElemAttribute(self._secondContainer, 'className', secondStyle)


    def setEnabled(self, enabled):
        self._enabled = enabled


    def isEnabled(self):
        return self._enabled


class SPClickEventHandler(ClickEventHandler):

    def __init__(self, sp):
        self._sp = sp


    def registerHandler(self, handler, type):
        if (Event.getEventsSunk(self._sp._splitter)
                & Event.getTypeInt(type.getName()) != 0):
            # If we are already sinking the event for the splitter we do
            # not want to additionally sink it for the root element
            return self.addHandler(handler, type)
        else:
            return self.addDomHandler(handler, type)


    def onContextMenu(self, event):
        target = event.getNativeEvent().getEventTarget()
        if self._sp._splitter.isOrHasChild(target):
            super(_0_, self).onContextMenu(event)


    def fireClick(self, event):
        target = event.getEventTarget()
        if self._sp._splitter.isOrHasChild(target):
            super(_0_, self).fireClick(event)


    def getRelativeToElement(self):
        return None
