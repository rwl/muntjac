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
from com.vaadin.terminal.gwt.client.Container import (Container,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.RenderInformation import (RenderInformation,)
from com.vaadin.terminal.gwt.client.ui.TouchScrollDelegate import (TouchScrollDelegate,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
from com.vaadin.terminal.gwt.client.RenderSpace import (RenderSpace,)
from com.vaadin.terminal.gwt.client.ContainerResizedListener import (ContainerResizedListener,)
from com.vaadin.terminal.gwt.client.ui.VOverlay import (VOverlay,)
# from com.google.gwt.core.client.Scheduler import (Scheduler,)
# from com.google.gwt.dom.client.NativeEvent import (NativeEvent,)
# from com.google.gwt.dom.client.Node import (Node,)
# from com.google.gwt.event.dom.client.DomEvent.Type import (Type,)
# from com.google.gwt.event.dom.client.TouchCancelEvent import (TouchCancelEvent,)
# from com.google.gwt.event.dom.client.TouchCancelHandler import (TouchCancelHandler,)
# from com.google.gwt.event.dom.client.TouchEndEvent import (TouchEndEvent,)
# from com.google.gwt.event.dom.client.TouchEndHandler import (TouchEndHandler,)
# from com.google.gwt.event.dom.client.TouchMoveEvent import (TouchMoveEvent,)
# from com.google.gwt.event.dom.client.TouchMoveHandler import (TouchMoveHandler,)
# from com.google.gwt.event.dom.client.TouchStartEvent import (TouchStartEvent,)
# from com.google.gwt.event.dom.client.TouchStartHandler import (TouchStartHandler,)
# from com.google.gwt.event.shared.EventHandler import (EventHandler,)
# from com.google.gwt.event.shared.HandlerRegistration import (HandlerRegistration,)
# from com.google.gwt.user.client.Command import (Command,)
# from com.google.gwt.user.client.DOM import (DOM,)
# from com.google.gwt.user.client.Element import (Element,)
# from com.google.gwt.user.client.Event import (Event,)
# from com.google.gwt.user.client.ui.ComplexPanel import (ComplexPanel,)
# from com.google.gwt.user.client.ui.Widget import (Widget,)
# from java.util.Set import (Set,)


class VSplitPanel(ComplexPanel, Container, ContainerResizedListener):
    _enabled = False
    CLASSNAME = 'v-splitpanel'
    SPLITTER_CLICK_EVENT_IDENTIFIER = 'sp_click'



#    private ClickEventHandler clickEventHandler = new ClickEventHandler(this,
#            SPLITTER_CLICK_EVENT_IDENTIFIER) {
#
#        @Override
#        protected <H extends EventHandler> HandlerRegistration registerHandler(
#                H handler, Type<H> type) {
#            if ((Event.getEventsSunk(splitter) & Event.getTypeInt(type
#                    .getName())) != 0) {
#                // If we are already sinking the event for the splitter we do
#                // not want to additionally sink it for the root element
#                return addHandler(handler, type);
#            } else {
#                return addDomHandler(handler, type);
#            }
#        }
#
#        @Override
#        public void onContextMenu(
#                com.google.gwt.event.dom.client.ContextMenuEvent event) {
#            Element target = event.getNativeEvent().getEventTarget().cast();
#            if (splitter.isOrHasChild(target)) {
#                super.onContextMenu(event);
#            }
#        };
#
#        @Override
#        protected void fireClick(NativeEvent event) {
#            Element target = event.getEventTarget().cast();
#            if (splitter.isOrHasChild(target)) {
#                super.fireClick(event);
#            }
#        }
#
#        @Override
#        protected Element getRelativeToElement() {
#            return null;
#        }
#
#    };

    ORIENTATION_HORIZONTAL = 0
    ORIENTATION_VERTICAL = 1
    _MIN_SIZE = 30
    _orientation = ORIENTATION_HORIZONTAL
    _firstChild = None
    _secondChild = None
    _wrapper = DOM.createDiv()
    _firstContainer = DOM.createDiv()
    _secondContainer = DOM.createDiv()
    _splitter = DOM.createDiv()
    _resizing = None
    _resized = False
    _origX = None
    _origY = None
    _origMouseX = None
    _origMouseY = None
    _locked = False
    _positionReversed = False
    _componentStyleNames = None
    _draggingCurtain = None
    _client = None
    _width = ''
    _height = ''
    _firstRenderSpace = RenderSpace(0, 0, True)
    _secondRenderSpace = RenderSpace(0, 0, True)
    _renderInformation = RenderInformation()
    _id = None
    _immediate = None
    _rendering = False
    # The current position of the split handle in either percentages or pixels
    _position = None
    scrolledContainer = None
    origScrollTop = None
    _touchScrollDelegate = None

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.__init__(self.ORIENTATION_HORIZONTAL)
        elif _1 == 1:
            orientation, = _0
            self.setElement(DOM.createDiv())
            _0 = orientation
            _1 = False
            while True:
                if _0 == self.ORIENTATION_HORIZONTAL:
                    _1 = True
                    self.setStyleName(self.CLASSNAME + '-horizontal')
                    break
                if (_1 is True) or (_0 == self.ORIENTATION_VERTICAL):
                    _1 = True
                if True:
                    _1 = True
                    self.setStyleName(self.CLASSNAME + '-vertical')
                    break
                break
            # size below will be overridden in update from uidl, initial size
            # needed to keep IE alive
            self.setWidth(self._MIN_SIZE + 'px')
            self.setHeight(self._MIN_SIZE + 'px')
            self.constructDom()
            self.setOrientation(orientation)
            self.sinkEvents(Event.MOUSEEVENTS)

            class _0_(TouchCancelHandler):

                def onTouchCancel(self, event):
                    # TODO When does this actually happen??
                    VConsole.log('TOUCH CANCEL')

            _0_ = self._0_()
            self.addDomHandler(_0_, TouchCancelEvent.getType())

            class _1_(TouchStartHandler):

                def onTouchStart(self, event):
                    target = event.getTouches().get(0).getTarget()
                    if self.splitter.isOrHasChild(target):
                        self.onMouseDown(Event.as_(event.getNativeEvent()))
                    else:
                        self.getTouchScrollDelegate().onTouchStart(event)

            _1_ = self._1_()
            self.addDomHandler(_1_, TouchStartEvent.getType())

            class _2_(TouchMoveHandler):

                def onTouchMove(self, event):
                    if self.resizing:
                        self.onMouseMove(Event.as_(event.getNativeEvent()))

            _2_ = self._2_()
            self.addDomHandler(_2_, TouchMoveEvent.getType())

            class _3_(TouchEndHandler):

                def onTouchEnd(self, event):
                    if self.resizing:
                        self.onMouseUp(Event.as_(event.getNativeEvent()))

            _3_ = self._3_()
            self.addDomHandler(_3_, TouchEndEvent.getType())
        else:
            raise ARGERROR(0, 1)

    def getTouchScrollDelegate(self):
        if self._touchScrollDelegate is None:
            self._touchScrollDelegate = TouchScrollDelegate(self._firstContainer, self._secondContainer)
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
        DOM.setElementProperty(self._firstContainer, 'className', self.CLASSNAME + '-first-container')
        DOM.setElementProperty(self._secondContainer, 'className', self.CLASSNAME + '-second-container')

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
            self._componentStyleNames = uidl.getStringAttribute('style').split(' ')
        else:
            self._componentStyleNames = [None] * 0
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

            class _4_(Command):

                def execute(self):
                    self.iLayout()

            _4_ = self._4_()
            Scheduler.get().scheduleDeferred(_4_)
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
        # Calculates absolutely positioned container places/sizes (non-Javadoc)
        #
        # @see com.vaadin.terminal.gwt.client.NeedsLayout#layout()

        if pos is None:
            return
        # Convert percentage values to pixels
        if pos.find('%') > 0:
            pos = ((self.float(pos[:-1]) / 100) * (self.getOffsetWidth() if self._orientation == self.ORIENTATION_HORIZONTAL else self.getOffsetHeight())) + 'px'
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
        if not self.isAttached():
            return
        self._renderInformation.updateSize(self.getElement())
        _0 = self._orientation
        _1 = False
        while True:
            if _0 == self.ORIENTATION_HORIZONTAL:
                _1 = True
                wholeSize = DOM.getElementPropertyInt(self._wrapper, 'clientWidth')
                pixelPosition = DOM.getElementPropertyInt(self._splitter, 'offsetLeft')
                # reposition splitter in case it is out of box
                if (
                    (pixelPosition > 0 and pixelPosition + self.getSplitterSize() > wholeSize) or (self._positionReversed and pixelPosition < 0)
                ):
                    pixelPosition = wholeSize - self.getSplitterSize()
                    if pixelPosition < 0:
                        pixelPosition = 0
                    self.setSplitPosition(pixelPosition + 'px')
                    return
                DOM.setStyleAttribute(self._firstContainer, 'width', pixelPosition + 'px')
                secondContainerWidth = wholeSize - pixelPosition - self.getSplitterSize()
                if secondContainerWidth < 0:
                    secondContainerWidth = 0
                DOM.setStyleAttribute(self._secondContainer, 'width', secondContainerWidth + 'px')
                DOM.setStyleAttribute(self._secondContainer, 'left', pixelPosition + self.getSplitterSize() + 'px')
                contentHeight = self._renderInformation.getRenderedSize().getHeight()
                self._firstRenderSpace.setHeight(contentHeight)
                self._firstRenderSpace.setWidth(pixelPosition)
                self._secondRenderSpace.setHeight(contentHeight)
                self._secondRenderSpace.setWidth(secondContainerWidth)
                break
            if (_1 is True) or (_0 == self.ORIENTATION_VERTICAL):
                _1 = True
                wholeSize = DOM.getElementPropertyInt(self._wrapper, 'clientHeight')
                pixelPosition = DOM.getElementPropertyInt(self._splitter, 'offsetTop')
                # reposition splitter in case it is out of box
                if (
                    (pixelPosition > 0 and pixelPosition + self.getSplitterSize() > wholeSize) or (self._positionReversed and pixelPosition < 0)
                ):
                    pixelPosition = wholeSize - self.getSplitterSize()
                    if pixelPosition < 0:
                        pixelPosition = 0
                    self.setSplitPosition(pixelPosition + 'px')
                    return
                DOM.setStyleAttribute(self._firstContainer, 'height', pixelPosition + 'px')
                secondContainerHeight = wholeSize - pixelPosition - self.getSplitterSize()
                if secondContainerHeight < 0:
                    secondContainerHeight = 0
                DOM.setStyleAttribute(self._secondContainer, 'height', secondContainerHeight + 'px')
                DOM.setStyleAttribute(self._secondContainer, 'top', pixelPosition + self.getSplitterSize() + 'px')
                contentWidth = self._renderInformation.getRenderedSize().getWidth()
                self._firstRenderSpace.setHeight(pixelPosition)
                self._firstRenderSpace.setWidth(contentWidth)
                self._secondRenderSpace.setHeight(secondContainerHeight)
                self._secondRenderSpace.setWidth(contentWidth)
                break
            break
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
        _0 = DOM.eventGetType(event)
        _1 = False
        while True:
            if _0 == Event.ONMOUSEMOVE:
                _1 = True
                if self._resizing:
                    self.onMouseMove(event)
                break
            if (_1 is True) or (_0 == Event.ONMOUSEDOWN):
                _1 = True
                self.onMouseDown(event)
                break
            if (_1 is True) or (_0 == Event.ONMOUSEOUT):
                _1 = True
                if self._resizing:
                    self.showDraggingCurtain()
                break
            if (_1 is True) or (_0 == Event.ONMOUSEUP):
                _1 = True
                if self._resizing:
                    self.onMouseUp(event)
                break
            if (_1 is True) or (_0 == Event.ONCLICK):
                _1 = True
                self._resizing = False
                break
            break
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
            self._origX = DOM.getElementPropertyInt(self._splitter, 'offsetLeft')
            self._origY = DOM.getElementPropertyInt(self._splitter, 'offsetTop')
            self._origMouseX = Util.getTouchOrMouseClientX(event)
            self._origMouseY = Util.getTouchOrMouseClientY(event)
            event.stopPropagation()
            event.preventDefault()

    def onMouseMove(self, event):
        _0 = self._orientation
        _1 = False
        while True:
            if _0 == self.ORIENTATION_HORIZONTAL:
                _1 = True
                x = Util.getTouchOrMouseClientX(event)
                self.onHorizontalMouseMove(x)
                break
            if (_1 is True) or (_0 == self.ORIENTATION_VERTICAL):
                _1 = True
            if True:
                _1 = True
                y = Util.getTouchOrMouseClientY(event)
                self.onVerticalMouseMove(y)
                break
            break

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
            self._position = (self.getOffsetWidth() - newX - self.getSplitterSize()) + 'px'
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
            self._position = (self.getOffsetHeight() - newY - self.getSplitterSize()) + 'px'
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
        """Used in FF to avoid losing mouse capture when pointer is moved on an
        iframe.
        """
        if not self.isDraggingCurtainRequired():
            return
        if self._draggingCurtain is None:
            self._draggingCurtain = DOM.createDiv()
            DOM.setStyleAttribute(self._draggingCurtain, 'position', 'absolute')
            DOM.setStyleAttribute(self._draggingCurtain, 'top', '0px')
            DOM.setStyleAttribute(self._draggingCurtain, 'left', '0px')
            DOM.setStyleAttribute(self._draggingCurtain, 'width', '100%')
            DOM.setStyleAttribute(self._draggingCurtain, 'height', '100%')
            DOM.setStyleAttribute(self._draggingCurtain, 'zIndex', '' + VOverlay.Z_INDEX)
            DOM.appendChild(self._wrapper, self._draggingCurtain)

    def isDraggingCurtainRequired(self):
        """A dragging curtain is required in Gecko and Webkit.

        @return true if the browser requires a dragging curtain
        """
        return BrowserInfo.get().isGecko() or BrowserInfo.get().isWebkit()

    def hideDraggingCurtain(self):
        """Hides dragging curtain"""
        if self._draggingCurtain is not None:
            DOM.removeChild(self._wrapper, self._draggingCurtain)
            self._draggingCurtain = None

    _splitterSize = -1

    def getSplitterSize(self):
        if self._splitterSize < 0:
            if self.isAttached():
                _0 = self._orientation
                _1 = False
                while True:
                    if _0 == self.ORIENTATION_HORIZONTAL:
                        _1 = True
                        self._splitterSize = DOM.getElementPropertyInt(self._splitter, 'offsetWidth')
                        break
                    if True:
                        _1 = True
                        self._splitterSize = DOM.getElementPropertyInt(self._splitter, 'offsetHeight')
                        break
                    break
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
        return component is not None and (component == self._firstChild) or (component == self._secondChild)

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
        # TODO Implement caption handling
        pass

    def updateSplitPositionToServer(self):
        """Updates the new split position back to server."""
        pos = 0
        if self._position.find('%') > 0:
            pos = Float.valueOf.valueOf(self._position[:len(self._position) - 1]).intValue()
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
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(self._componentStyleNames)):
                break
            splitterStyle += ' ' + self.CLASSNAME + splitterSuffix + '-' + self._componentStyleNames[i] + lockedSuffix
            firstStyle += ' ' + self.CLASSNAME + firstContainerSuffix + '-' + self._componentStyleNames[i]
            secondStyle += ' ' + self.CLASSNAME + secondContainerSuffix + '-' + self._componentStyleNames[i]
        DOM.setElementProperty(self._splitter, 'className', splitterStyle)
        DOM.setElementProperty(self._firstContainer, 'className', firstStyle)
        DOM.setElementProperty(self._secondContainer, 'className', secondStyle)

    def setEnabled(self, enabled):
        self._enabled = enabled

    def isEnabled(self):
        return self._enabled
