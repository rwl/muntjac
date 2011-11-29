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

from __pyjamas__ import (ARGERROR, POSTINC,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.ui.ClickEventHandler import (ClickEventHandler,)
from com.vaadin.terminal.gwt.client.VDebugConsole import (VDebugConsole,)
from com.vaadin.terminal.gwt.client.EventId import (EventId,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.Container import (Container,)
from com.vaadin.terminal.gwt.client.ui.ShortcutActionHandler import (ShortcutActionHandler,)
from com.vaadin.terminal.gwt.client.ui.VView import (VView,)
from com.vaadin.terminal.gwt.client.RenderSpace import (RenderSpace,)
from com.vaadin.terminal.gwt.client.ui.VNotification import (VNotification,)
from com.vaadin.terminal.gwt.client.ui.FocusableScrollPanel import (FocusableScrollPanel,)
from com.vaadin.terminal.gwt.client.ui.VLazyExecutor import (VLazyExecutor,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.VOverlay import (VOverlay,)
from com.vaadin.terminal.gwt.client.Focusable import (Focusable,)
# from com.google.gwt.event.dom.client.BlurEvent import (BlurEvent,)
# from com.google.gwt.event.dom.client.BlurHandler import (BlurHandler,)
# from com.google.gwt.event.dom.client.DomEvent.Type import (Type,)
# from com.google.gwt.event.dom.client.FocusEvent import (FocusEvent,)
# from com.google.gwt.event.dom.client.FocusHandler import (FocusHandler,)
# from com.google.gwt.event.dom.client.KeyDownEvent import (KeyDownEvent,)
# from com.google.gwt.event.dom.client.KeyDownHandler import (KeyDownHandler,)
# from com.google.gwt.event.dom.client.ScrollEvent import (ScrollEvent,)
# from com.google.gwt.event.dom.client.ScrollHandler import (ScrollHandler,)
# from com.google.gwt.event.shared.EventHandler import (EventHandler,)
# from com.google.gwt.event.shared.HandlerRegistration import (HandlerRegistration,)
# from com.google.gwt.user.client.ui.Frame import (Frame,)
# from com.google.gwt.user.client.ui.HasWidgets import (HasWidgets,)
# from com.google.gwt.user.client.ui.RootPanel import (RootPanel,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Arrays import (Arrays,)
# from java.util.Comparator import (Comparator,)
# from java.util.Iterator import (Iterator,)
# from java.util.Set import (Set,)
BeforeShortcutActionListener = ShortcutActionHandler.BeforeShortcutActionListener
ShortcutActionHandlerOwner = ShortcutActionHandler.ShortcutActionHandlerOwner


class VWindow(VOverlay, Container, ShortcutActionHandlerOwner, ScrollHandler, KeyDownHandler, FocusHandler, BlurHandler, BeforeShortcutActionListener, Focusable):
    """"Sub window" component.

    @author IT Mill Ltd
    """
    # Minimum allowed height of a window. This refers to the content area, not
    # the outer borders.

    _MIN_CONTENT_AREA_HEIGHT = 100
    # Minimum allowed width of a window. This refers to the content area, not
    # the outer borders.

    _MIN_CONTENT_AREA_WIDTH = 150
    _windowOrder = list()
    _orderingDefered = None
    CLASSNAME = 'v-window'
    # Difference between offsetWidth and inner width for the content area.
    _contentAreaBorderPadding = -1
    # Pixels used by inner borders and paddings horizontally (calculated only
    # once). This is the difference between the width of the root element and
    # the content area, such that if root element width is set to "XYZpx" the
    # inner width (width-border-padding) of the content area is
    # X-contentAreaRootDifference.

    _contentAreaToRootDifference = -1
    _STACKING_OFFSET_PIXELS = 15
    Z_INDEX = 10000
    _layout = None
    _contents = None
    _header = None
    _footer = None
    _resizeBox = None
    _contentPanel = FocusableScrollPanel()
    _dragging = None
    _startX = None
    _startY = None
    _origX = None
    _origY = None
    _resizing = None
    _origW = None
    _origH = None
    _closeBox = None
    client = None
    _id = None
    _shortcutHandler = None
    # Last known positionx read from UIDL or updated to application connection
    _uidlPositionX = -1
    # Last known positiony read from UIDL or updated to application connection
    _uidlPositionY = -1
    _vaadinModality = False
    _resizable = True
    _draggable = True
    _resizeLazy = False
    _modalityCurtain = None
    _draggingCurtain = None
    _headerText = None
    _closable = True
    _dynamicWidth = False
    _dynamicHeight = False
    _layoutRelativeWidth = False
    _layoutRelativeHeight = False
    # If centered (via UIDL), the window should stay in the centered -mode
    # until a position is received from the server, or the user moves or
    # resizes the window.
    _centered = False
    _renderSpace = RenderSpace(_MIN_CONTENT_AREA_WIDTH, _MIN_CONTENT_AREA_HEIGHT, True)
    _width = None
    _height = None
    _immediate = None
    _wrapper = None
    _wrapper2 = None

    class clickEventHandler(ClickEventHandler):

        def registerHandler(self, handler, type):
            return self.addDomHandler(handler, type)

    _visibilityChangesDisabled = None
    _bringToFrontSequence = -1
    _delayedContentsSizeUpdater = 
    class _1_(ScheduledCommand):

        def execute(self):
            VWindow_this.updateContentsSize()

    _1_ = _1_()
    VLazyExecutor(200, _1_)

    def __init__(self):
        super(VWindow, self)(False, False, True)
        # no autohide, not modal, shadow
        # Different style of shadow for windows
        self.setShadowStyle('window')
        order = len(self._windowOrder)
        self.setWindowOrder(order)
        self._windowOrder.add(self)
        self.constructDOM()
        self.setPopupPosition(order * self._STACKING_OFFSET_PIXELS, order * self._STACKING_OFFSET_PIXELS)
        self._contentPanel.addScrollHandler(self)
        self._contentPanel.addKeyDownHandler(self)
        self._contentPanel.addFocusHandler(self)
        self._contentPanel.addBlurHandler(self)

    def bringToFront(self):
        curIndex = self._windowOrder.index(self)
        if curIndex + 1 < len(self._windowOrder):
            self._windowOrder.remove(self)
            self._windowOrder.add(self)
            _0 = True
            while True:
                if _0 is True:
                    _0 = False
                else:
                    curIndex += 1
                if not (curIndex < len(self._windowOrder)):
                    break
                self._windowOrder[curIndex].setWindowOrder(curIndex)

    def isActive(self):
        """Returns true if this window is the topmost VWindow

        @return
        """
        return self._windowOrder[len(self._windowOrder) - 1] == self

    def setWindowOrder(self, order):
        self.setZIndex(order + self.Z_INDEX)

    def setZIndex(self, zIndex):
        super(VWindow, self).setZIndex(zIndex)
        if self._vaadinModality:
            DOM.setStyleAttribute(self.getModalityCurtain(), 'zIndex', '' + zIndex)

    def getModalityCurtain(self):
        if self._modalityCurtain is None:
            self._modalityCurtain = DOM.createDiv()
            self._modalityCurtain.setClassName(self.CLASSNAME + '-modalitycurtain')
        return self._modalityCurtain

    def constructDOM(self):
        self.setStyleName(self.CLASSNAME)
        self._header = DOM.createDiv()
        DOM.setElementProperty(self._header, 'className', self.CLASSNAME + '-outerheader')
        self._headerText = DOM.createDiv()
        DOM.setElementProperty(self._headerText, 'className', self.CLASSNAME + '-header')
        self._contents = DOM.createDiv()
        DOM.setElementProperty(self._contents, 'className', self.CLASSNAME + '-contents')
        self._footer = DOM.createDiv()
        DOM.setElementProperty(self._footer, 'className', self.CLASSNAME + '-footer')
        self._resizeBox = DOM.createDiv()
        DOM.setElementProperty(self._resizeBox, 'className', self.CLASSNAME + '-resizebox')
        self._closeBox = DOM.createDiv()
        DOM.setElementProperty(self._closeBox, 'className', self.CLASSNAME + '-closebox')
        DOM.appendChild(self._footer, self._resizeBox)
        self._wrapper = DOM.createDiv()
        DOM.setElementProperty(self._wrapper, 'className', self.CLASSNAME + '-wrap')
        self._wrapper2 = DOM.createDiv()
        DOM.setElementProperty(self._wrapper2, 'className', self.CLASSNAME + '-wrap2')
        DOM.appendChild(self._wrapper2, self._closeBox)
        DOM.appendChild(self._wrapper2, self._header)
        DOM.appendChild(self._header, self._headerText)
        DOM.appendChild(self._wrapper2, self._contents)
        DOM.appendChild(self._wrapper2, self._footer)
        DOM.appendChild(self._wrapper, self._wrapper2)
        DOM.appendChild(super(VWindow, self).getContainerElement(), self._wrapper)
        self.sinkEvents(((Event.MOUSEEVENTS | Event.TOUCHEVENTS) | Event.ONCLICK) | Event.ONLOSECAPTURE)
        self.setWidget(self._contentPanel)

    def updateFromUIDL(self, uidl, client):
        self._id = uidl.getId()
        self.client = client
        # Workaround needed for Testing Tools (GWT generates window DOM
        # slightly different in different browsers).
        DOM.setElementProperty(self._closeBox, 'id', self._id + '_window_close')
        if uidl.hasAttribute('invisible'):
            self.hide()
            return
        if not uidl.hasAttribute('cached'):
            if uidl.getBooleanAttribute('modal') != self._vaadinModality:
                self.setVaadinModality(not self._vaadinModality)
            if not self.isAttached():
                self.setVisible(False)
                # hide until possible centering
                self.show()
            if uidl.getBooleanAttribute('resizable') != self._resizable:
                self.setResizable(not self._resizable)
            self._resizeLazy = uidl.hasAttribute(VView.RESIZE_LAZY)
            self.setDraggable(not uidl.hasAttribute('fixedposition'))
            # Caption must be set before required header size is measured. If
            # the caption attribute is missing the caption should be cleared.
            self.setCaption(uidl.getStringAttribute('caption'), uidl.getStringAttribute('icon'))
        self._visibilityChangesDisabled = True
        if client.updateComponent(self, uidl, False):
            return
        self._visibilityChangesDisabled = False
        self.clickEventHandler.handleEventHandlerRegistration(client)
        self._immediate = uidl.hasAttribute('immediate')
        self.setClosable(not uidl.getBooleanAttribute('readonly'))
        # Initialize the position form UIDL
        positionx = uidl.getIntVariable('positionx')
        positiony = uidl.getIntVariable('positiony')
        if (positionx >= 0) or (positiony >= 0):
            if positionx < 0:
                positionx = 0
            if positiony < 0:
                positiony = 0
            self.setPopupPosition(positionx, positiony)
        showingUrl = False
        childIndex = 0
        childUidl = uidl.getChildUIDL(POSTINC(globals(), locals(), 'childIndex'))
        while 'open' == childUidl.getTag():
            # TODO multiple opens with the same target will in practice just
            # open the last one - should we fix that somehow?
            parsedUri = client.translateVaadinUri(childUidl.getStringAttribute('src'))
            if not childUidl.hasAttribute('name'):
                frame = Frame()
                DOM.setStyleAttribute(frame.getElement(), 'width', '100%')
                DOM.setStyleAttribute(frame.getElement(), 'height', '100%')
                DOM.setStyleAttribute(frame.getElement(), 'border', '0px')
                frame.setUrl(parsedUri)
                self._contentPanel.setWidget(frame)
                showingUrl = True
            else:
                target = childUidl.getStringAttribute('name')
                Window.open(parsedUri, target, '')
            childUidl = uidl.getChildUIDL(POSTINC(globals(), locals(), 'childIndex'))
        lo = client.getPaintable(childUidl)
        if self._layout is not None:
            if self._layout != lo:
                # remove old
                client.unregisterPaintable(self._layout)
                self._contentPanel.remove(self._layout)
                # add new
                if not showingUrl:
                    self._contentPanel.setWidget(lo)
                self._layout = lo
        elif not showingUrl:
            self._contentPanel.setWidget(lo)
            self._layout = lo
        self._dynamicWidth = not uidl.hasAttribute('width')
        self._dynamicHeight = not uidl.hasAttribute('height')
        self._layoutRelativeWidth = uidl.hasAttribute('layoutRelativeWidth')
        self._layoutRelativeHeight = uidl.hasAttribute('layoutRelativeHeight')
        if self._dynamicWidth and self._layoutRelativeWidth:
            # Relative layout width, fix window width before rendering (width
            # according to caption)

            self.setNaturalWidth()
        self._layout.updateFromUIDL(childUidl, client)
        if not self._dynamicHeight and self._layoutRelativeWidth:
            # Relative layout width, and fixed height. Must update the size to
            # be able to take scrollbars into account (layout gets narrower
            # space if it is higher than the window) -> only vertical scrollbar

            client.runDescendentsLayout(self)
        # No explicit width is set and the layout does not have relative width
        # so fix the size according to the layout.

        if self._dynamicWidth and not self._layoutRelativeWidth:
            self.setNaturalWidth()
        if self._dynamicHeight and self._layoutRelativeHeight:
            # Prevent resizing until height has been fixed
            self._resizable = False
        # we may have actions and notifications
        if uidl.getChildCount() > 1:
            cnt = uidl.getChildCount()
            _0 = True
            i = 1
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < cnt):
                    break
                childUidl = uidl.getChildUIDL(i)
                if childUidl.getTag() == 'actions':
                    if self._shortcutHandler is None:
                        self._shortcutHandler = ShortcutActionHandler(self._id, client)
                    self._shortcutHandler.updateActionMap(childUidl)
                elif childUidl.getTag() == 'notifications':
                    _1 = True
                    it = childUidl.getChildIterator()
                    while True:
                        if _1 is True:
                            _1 = False
                        if not it.hasNext():
                            break
                        notification = it.next()
                        VNotification.showNotification(client, notification)
        # setting scrollposition must happen after children is rendered
        self._contentPanel.setScrollPosition(uidl.getIntVariable('scrollTop'))
        self._contentPanel.setHorizontalScrollPosition(uidl.getIntVariable('scrollLeft'))
        # Center this window on screen if requested
        # This has to be here because we might not know the content size before
        # everything is painted into the window
        if uidl.getBooleanAttribute('center'):
            # mark as centered - this is unset on move/resize
            self._centered = True
            self.center()
        else:
            # don't try to center the window anymore
            self._centered = False
        self.updateShadowSizeAndPosition()
        self.setVisible(True)
        sizeReduced = False
        # ensure window is not larger than browser window
        if self.getOffsetWidth() > Window.getClientWidth():
            self.setWidth(Window.getClientWidth() + 'px')
            sizeReduced = True
        if self.getOffsetHeight() > Window.getClientHeight():
            self.setHeight(Window.getClientHeight() + 'px')
            sizeReduced = True
        if self._dynamicHeight and self._layoutRelativeHeight:
            # Window height is undefined, layout is 100% high so the layout
            # should define the initial window height but on resize the layout
            # should be as high as the window. We fix the height to deal with
            # this.

            h = self._contents.getOffsetHeight() + self.getExtraHeight()
            w = self.getElement().getOffsetWidth()
            client.updateVariable(self._id, 'height', h, False)
            client.updateVariable(self._id, 'width', w, True)
        if sizeReduced:
            # If we changed the size we need to update the size of the child
            # component if it is relative (#3407)
            client.runDescendentsLayout(self)
        Util.runWebkitOverflowAutoFix(self._contentPanel.getElement())
        client.getView().scrollIntoView(uidl)
        if uidl.hasAttribute('bringToFront'):
            # Focus as a side-efect. Will be overridden by
            # ApplicationConnection if another component was focused by the
            # server side.

            self._contentPanel.focus()
            self._bringToFrontSequence = uidl.getIntAttribute('bringToFront')
            self.deferOrdering()

    @classmethod
    def deferOrdering(cls):
        """Calling this method will defer ordering algorithm, to order windows based
        on servers bringToFront and modality instructions. Non changed windows
        will be left intact.
        """
        if not cls._orderingDefered:
            cls._orderingDefered = True

            class _1_(Command):

                def execute(self):
                    VWindow_this.doServerSideOrdering()

            _1_ = _1_()
            Scheduler.get().scheduleFinally(_1_)

    @classmethod
    def doServerSideOrdering(cls):
        cls._orderingDefered = False
        array = list([None] * len(cls._windowOrder))

        class _2_(Comparator):

            def compare(self, o1, o2):
                # Order by modality, then by bringtofront sequence.
                if o1.vaadinModality and not o2.vaadinModality:
                    return 1
                elif not o1.vaadinModality and o2.vaadinModality:
                    return -1
                elif o1.bringToFrontSequence > o2.bringToFrontSequence:
                    return 1
                elif o1.bringToFrontSequence < o2.bringToFrontSequence:
                    return -1
                else:
                    return 0

        _2_ = _2_()
        Arrays.sort(array, _2_)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(array)):
                break
            w = array[i]
            if (w.bringToFrontSequence != -1) or w.vaadinModality:
                w.bringToFront()
                w.bringToFrontSequence = -1

    def setVisible(self, visible):
        # Visibility with VWindow works differently than with other Paintables
        # in Vaadin. Invisible VWindows are not attached to DOM at all. Flag is
        # used to avoid visibility call from
        # ApplicationConnection.updateComponent();

        if not self._visibilityChangesDisabled:
            super(VWindow, self).setVisible(visible)

    def setDraggable(self, draggable):
        if self._draggable == draggable:
            return
        self._draggable = draggable
        if not self._draggable:
            self._header.getStyle().setProperty('cursor', 'default')
        else:
            self._header.getStyle().setProperty('cursor', '')

    def setNaturalWidth(self):
        # Use max(layout width, window width) i.e layout content width or
        # caption width. We remove the previous set width so the width is
        # allowed to shrink. All widths are measured as outer sizes, i.e. the
        # borderWidth is added to the content.

        DOM.setStyleAttribute(self.getElement(), 'width', '')
        oldHeaderWidth = ''
        # Only for IE6
        if BrowserInfo.get().isIE6():
            # For some reason IE6 has title DIV set to width 100% which
            # interferes with the header measuring. Also IE6 has width set to
            # the contentPanel.

            oldHeaderWidth = self._headerText.getStyle().getProperty('width')
            DOM.setStyleAttribute(self._contentPanel.getElement(), 'width', 'auto')
            DOM.setStyleAttribute(self._contentPanel.getElement(), 'zoom', '1')
            self._headerText.getStyle().setProperty('width', 'auto')
        # Content
        contentWidth = self._contentPanel.getElement().getScrollWidth()
        contentWidth += self.getContentAreaToRootDifference()
        # Window width (caption)
        windowCaptionWidth = self.getOffsetWidth()
        naturalWidth = contentWidth if contentWidth > windowCaptionWidth else windowCaptionWidth
        if BrowserInfo.get().isIE6():
            self._headerText.getStyle().setProperty('width', oldHeaderWidth)
        self.setWidth(naturalWidth + 'px')

    def getContentAreaToRootDifference(self):
        if self._contentAreaToRootDifference < 0:
            self.measure()
        return self._contentAreaToRootDifference

    def measure(self):
        if not self.isAttached():
            return
        self._contentAreaBorderPadding = Util.measureHorizontalPaddingAndBorder(self._contents, 4)
        wrapperPaddingBorder = Util.measureHorizontalPaddingAndBorder(self._wrapper, 0) + Util.measureHorizontalPaddingAndBorder(self._wrapper2, 0)
        self._contentAreaToRootDifference = wrapperPaddingBorder + self._contentAreaBorderPadding

    def setClosable(self, closable):
        """Sets the closable state of the window. Additionally hides/shows the close
        button according to the new state.

        @param closable
                   true if the window can be closed by the user
        """
        if self._closable == closable:
            return
        self._closable = closable
        if closable:
            DOM.setStyleAttribute(self._closeBox, 'display', '')
        else:
            DOM.setStyleAttribute(self._closeBox, 'display', 'none')

    def isClosable(self):
        """Returns the closable state of the sub window. If the sub window is
        closable a decoration (typically an X) is shown to the user. By clicking
        on the X the user can close the window.

        @return true if the sub window is closable
        """
        return self._closable

    def show(self):
        if self._vaadinModality:
            self.showModalityCurtain()
        super(VWindow, self).show()
        self.setFF2CaretFixEnabled(True)
        self.fixFF3OverflowBug()

    def fixFF3OverflowBug(self):
        """Disable overflow auto with FF3 to fix #1837."""
        if BrowserInfo.get().isFF3():

            class _3_(Command):

                def execute(self):
                    DOM.setStyleAttribute(self.getElement(), 'overflow', '')

            _3_ = _3_()
            Scheduler.get().scheduleDeferred(_3_)

    def setFF2CaretFixEnabled(self, enable):
        """Fix "missing cursor" browser bug workaround for FF2 in Windows and Linux.

        Calling this method has no effect on other browsers than the ones based
        on Gecko 1.8

        @param enable
        """
        if BrowserInfo.get().isFF2():
            if enable:

                class _4_(Command):

                    def execute(self):
                        DOM.setStyleAttribute(self.getElement(), 'overflow', 'auto')

                _4_ = _4_()
                Scheduler.get().scheduleDeferred(_4_)
            else:
                DOM.setStyleAttribute(self.getElement(), 'overflow', '')

    def hide(self):
        if self._vaadinModality:
            self.hideModalityCurtain()
        super(VWindow, self).hide()

    def setVaadinModality(self, modality):
        self._vaadinModality = modality
        if self._vaadinModality:
            if self.isAttached():
                self.showModalityCurtain()
            self.deferOrdering()
        elif self._modalityCurtain is not None:
            if self.isAttached():
                self.hideModalityCurtain()
            self._modalityCurtain = None

    def showModalityCurtain(self):
        if BrowserInfo.get().isFF2():
            DOM.setStyleAttribute(self.getModalityCurtain(), 'height', DOM.getElementPropertyInt(RootPanel.getBodyElement(), 'offsetHeight') + 'px')
            DOM.setStyleAttribute(self.getModalityCurtain(), 'position', 'absolute')
        DOM.setStyleAttribute(self.getModalityCurtain(), 'zIndex', '' + self._windowOrder.index(self) + self.Z_INDEX)
        if self.isShowing():
            RootPanel.getBodyElement().insertBefore(self.getModalityCurtain(), self.getElement())
        else:
            DOM.appendChild(RootPanel.getBodyElement(), self.getModalityCurtain())

    def hideModalityCurtain(self):
        # Shows (or hides) an empty div on top of all other content; used when
        # resizing or moving, so that iframes (etc) do not steal event.

        DOM.removeChild(RootPanel.getBodyElement(), self._modalityCurtain)

    def showDraggingCurtain(self, show):
        if show and self._draggingCurtain is None:
            self.setFF2CaretFixEnabled(False)
            # makes FF2 slow
            self._draggingCurtain = DOM.createDiv()
            DOM.setStyleAttribute(self._draggingCurtain, 'position', 'absolute')
            DOM.setStyleAttribute(self._draggingCurtain, 'top', '0px')
            DOM.setStyleAttribute(self._draggingCurtain, 'left', '0px')
            DOM.setStyleAttribute(self._draggingCurtain, 'width', '100%')
            DOM.setStyleAttribute(self._draggingCurtain, 'height', '100%')
            DOM.setStyleAttribute(self._draggingCurtain, 'zIndex', '' + VOverlay.Z_INDEX)
            DOM.appendChild(RootPanel.getBodyElement(), self._draggingCurtain)
        elif not show and self._draggingCurtain is not None:
            self.setFF2CaretFixEnabled(True)
            # makes FF2 slow
            DOM.removeChild(RootPanel.getBodyElement(), self._draggingCurtain)
            self._draggingCurtain = None

    def setResizable(self, resizability):
        self._resizable = resizability
        if resizability:
            DOM.setElementProperty(self._footer, 'className', self.CLASSNAME + '-footer')
            DOM.setElementProperty(self._resizeBox, 'className', self.CLASSNAME + '-resizebox')
        else:
            DOM.setElementProperty(self._footer, 'className', self.CLASSNAME + '-footer ' + self.CLASSNAME + '-footer-noresize')
            DOM.setElementProperty(self._resizeBox, 'className', self.CLASSNAME + '-resizebox ' + self.CLASSNAME + '-resizebox-disabled')

    def setPopupPosition(self, left, top):
        if top < 0:
            # ensure window is not moved out of browser window from top of the
            # screen
            top = 0
        super(VWindow, self).setPopupPosition(left, top)
        if left != self._uidlPositionX and self.client is not None:
            self.client.updateVariable(self._id, 'positionx', left, False)
            self._uidlPositionX = left
        if top != self._uidlPositionY and self.client is not None:
            self.client.updateVariable(self._id, 'positiony', top, False)
            self._uidlPositionY = top

    def setCaption(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            c, = _0
            self.setCaption(c, None)
        elif _1 == 2:
            c, icon = _0
            html = Util.escapeHTML(c)
            if icon is not None:
                icon = self.client.translateVaadinUri(icon)
                html = '<img src=\"' + Util.escapeAttribute(icon) + '\" class=\"v-icon\" />' + html
            DOM.setInnerHTML(self._headerText, html)
        else:
            raise ARGERROR(1, 2)

    def getContainerElement(self):
        # in GWT 1.5 this method is used in PopupPanel constructor
        if self._contents is None:
            return super(VWindow, self).getContainerElement()
        return self._contents

    def onBrowserEvent(self, event):
        bubble = True
        type = event.getTypeInt()
        target = DOM.eventGetTarget(event)
        if self.client is not None and self._header.isOrHasChild(target):
            # Handle window caption tooltips
            self.client.handleTooltipEvent(event, self)
        if self._resizing or (self._resizeBox == target):
            self.onResizeEvent(event)
            bubble = False
        elif self.isClosable() and target == self._closeBox:
            if type == Event.ONCLICK:
                self.onCloseClick()
            bubble = False
        elif self._dragging or (not self._contents.isOrHasChild(target)):
            self.onDragEvent(event)
            bubble = False
        elif type == Event.ONCLICK:
            # clicked inside window, ensure to be on top
            if not self.isActive():
                self.bringToFront()
        # If clicking on other than the content, move focus to the window.
        # After that this windows e.g. gets all keyboard shortcuts.

        if (
            type == Event.ONMOUSEDOWN and not self._contentPanel.getElement().isOrHasChild(target) and target != self._closeBox
        ):
            self._contentPanel.focus()
        if not bubble:
            event.stopPropagation()
        else:
            # Super.onBrowserEvent takes care of Handlers added by the
            # ClickEventHandler
            super(VWindow, self).onBrowserEvent(event)

    def onCloseClick(self):
        self.client.updateVariable(self._id, 'close', True, True)

    def onResizeEvent(self, event):
        if self._resizable:
            _0 = event.getTypeInt()
            _1 = False
            while True:
                if _0 == Event.ONMOUSEDOWN:
                    _1 = True
                if (_1 is True) or (_0 == Event.ONTOUCHSTART):
                    _1 = True
                    if not self.isActive():
                        self.bringToFront()
                    self.showDraggingCurtain(True)
                    if BrowserInfo.get().isIE():
                        DOM.setStyleAttribute(self._resizeBox, 'visibility', 'hidden')
                    self._resizing = True
                    self._startX = Util.getTouchOrMouseClientX(event)
                    self._startY = Util.getTouchOrMouseClientY(event)
                    self._origW = self.getElement().getOffsetWidth()
                    self._origH = self.getElement().getOffsetHeight()
                    DOM.setCapture(self.getElement())
                    event.preventDefault()
                    break
                if (_1 is True) or (_0 == Event.ONMOUSEUP):
                    _1 = True
                if (_1 is True) or (_0 == Event.ONTOUCHEND):
                    _1 = True
                    self.setSize(event, True)
                if (_1 is True) or (_0 == Event.ONTOUCHCANCEL):
                    _1 = True
                    DOM.releaseCapture(self.getElement())
                if (_1 is True) or (_0 == Event.ONLOSECAPTURE):
                    _1 = True
                    self.showDraggingCurtain(False)
                    if BrowserInfo.get().isIE():
                        DOM.setStyleAttribute(self._resizeBox, 'visibility', '')
                    self._resizing = False
                    break
                if (_1 is True) or (_0 == Event.ONMOUSEMOVE):
                    _1 = True
                if (_1 is True) or (_0 == Event.ONTOUCHMOVE):
                    _1 = True
                    if self._resizing:
                        self._centered = False
                        self.setSize(event, False)
                        event.preventDefault()
                    break
                if True:
                    _1 = True
                    event.preventDefault()
                    break
                break

    def cursorInsideBrowserContentArea(self, event):
        """TODO check if we need to support this with touch based devices.

        Checks if the cursor was inside the browser content area when the event
        happened.

        @param event
                   The event to be checked
        @return true, if the cursor is inside the browser content area

                false, otherwise
        """
        if (event.getClientX() < 0) or (event.getClientY() < 0):
            # Outside to the left or above
            return False
        if (
            (event.getClientX() > Window.getClientWidth()) or (event.getClientY() > Window.getClientHeight())
        ):
            # Outside to the right or below
            return False
        return True

    def setSize(self, event, updateVariables):
        if not self.cursorInsideBrowserContentArea(event):
            # Only drag while cursor is inside the browser client area
            return
        w = (Util.getTouchOrMouseClientX(event) - self._startX) + self._origW
        if w < self._MIN_CONTENT_AREA_WIDTH + self.getContentAreaToRootDifference():
            w = self._MIN_CONTENT_AREA_WIDTH + self.getContentAreaToRootDifference()
        h = (Util.getTouchOrMouseClientY(event) - self._startY) + self._origH
        if h < self._MIN_CONTENT_AREA_HEIGHT + self.getExtraHeight():
            h = self._MIN_CONTENT_AREA_HEIGHT + self.getExtraHeight()
        self.setWidth(w + 'px')
        self.setHeight(h + 'px')
        if updateVariables:
            # sending width back always as pixels, no need for unit
            self.client.updateVariable(self._id, 'width', w, False)
            self.client.updateVariable(self._id, 'height', h, self._immediate)
        if updateVariables or (not self._resizeLazy):
            # Resize has finished or is not lazy
            self.updateContentsSize()
        else:
            # Lazy resize - wait for a while before re-rendering contents
            self._delayedContentsSizeUpdater.trigger()

    def updateContentsSize(self):
        # Update child widget dimensions
        if self.client is not None:
            self.client.handleComponentRelativeSize(self._layout)
            self.client.runDescendentsLayout(self._layout)
        Util.runWebkitOverflowAutoFix(self._contentPanel.getElement())

    def setWidth(self, width):
        # Width is set to the out-most element (v-window).
        # 
        # This function should never be called with percentage values (it will
        # throw an exception)

        self._width = width
        if not self.isAttached():
            return
        if width is not None and not ('' == width):
            rootPixelWidth = -1
            if width.find('px') < 0:
                # Convert non-pixel values to pixels by setting the width and
                # then measuring it. Updates the "width" variable with the
                # pixel width.

                DOM.setStyleAttribute(self.getElement(), 'width', width)
                rootPixelWidth = self.getElement().getOffsetWidth()
                width = rootPixelWidth + 'px'
            else:
                rootPixelWidth = int(width[:width.find('px')])
            # "width" now contains the new width in pixels
            if BrowserInfo.get().isIE6():
                self.getElement().getStyle().setProperty('overflow', 'hidden')
            # Apply the new pixel width
            self.getElement().getStyle().setProperty('width', width)
            # Caculate the inner width of the content area
            contentAreaInnerWidth = rootPixelWidth - self.getContentAreaToRootDifference()
            if contentAreaInnerWidth < self._MIN_CONTENT_AREA_WIDTH:
                contentAreaInnerWidth = self._MIN_CONTENT_AREA_WIDTH
                rootWidth = contentAreaInnerWidth + self.getContentAreaToRootDifference()
                DOM.setStyleAttribute(self.getElement(), 'width', rootWidth + 'px')
            # IE6 needs the actual inner content width on the content element,
            # otherwise it won't wrap the content properly (no scrollbars
            # appear, content flows out of window)
            if BrowserInfo.get().isIE6():
                DOM.setStyleAttribute(self._contentPanel.getElement(), 'width', contentAreaInnerWidth + 'px')
            self._renderSpace.setWidth(contentAreaInnerWidth)
            self.updateShadowSizeAndPosition()

    def setHeight(self, height):
        # Height is set to the out-most element (v-window).
        # 
        # This function should never be called with percentage values (it will
        # throw an exception)

        self._height = height
        if not self.isAttached():
            return
        if height is not None and not ('' == height):
            DOM.setStyleAttribute(self.getElement(), 'height', height)
            pixels = self.getElement().getOffsetHeight() - self.getExtraHeight()
            if pixels < self._MIN_CONTENT_AREA_HEIGHT:
                pixels = self._MIN_CONTENT_AREA_HEIGHT
                rootHeight = pixels + self.getExtraHeight()
                DOM.setStyleAttribute(self.getElement(), 'height', rootHeight + 'px')
            self._renderSpace.setHeight(pixels)
            height = pixels + 'px'
            self._contentPanel.getElement().getStyle().setProperty('height', height)
            self.updateShadowSizeAndPosition()

    _extraH = 0

    def getExtraHeight(self):
        self._extraH = self._header.getOffsetHeight() + self._footer.getOffsetHeight()
        return self._extraH

    def onDragEvent(self, event):
        _0 = DOM.eventGetType(event)
        _1 = False
        while True:
            if _0 == Event.ONTOUCHSTART:
                _1 = True
                if len(event.getTouches()) > 1:
                    return
            if (_1 is True) or (_0 == Event.ONMOUSEDOWN):
                _1 = True
                if not self.isActive():
                    self.bringToFront()
                self.beginMovingWindow(event)
                break
            if (_1 is True) or (_0 == Event.ONMOUSEUP):
                _1 = True
            if (_1 is True) or (_0 == Event.ONTOUCHEND):
                _1 = True
            if (_1 is True) or (_0 == Event.ONTOUCHCANCEL):
                _1 = True
            if (_1 is True) or (_0 == Event.ONLOSECAPTURE):
                _1 = True
                self.stopMovingWindow()
                break
            if (_1 is True) or (_0 == Event.ONMOUSEMOVE):
                _1 = True
            if (_1 is True) or (_0 == Event.ONTOUCHMOVE):
                _1 = True
                self.moveWindow(event)
                break
            if True:
                _1 = True
                break
            break

    def moveWindow(self, event):
        if self._dragging:
            self._centered = False
            if self.cursorInsideBrowserContentArea(event):
                # Only drag while cursor is inside the browser client area
                x = (Util.getTouchOrMouseClientX(event) - self._startX) + self._origX
                y = (Util.getTouchOrMouseClientY(event) - self._startY) + self._origY
                self.setPopupPosition(x, y)
            DOM.eventPreventDefault(event)

    def beginMovingWindow(self, event):
        if self._draggable:
            self.showDraggingCurtain(True)
            self._dragging = True
            self._startX = Util.getTouchOrMouseClientX(event)
            self._startY = Util.getTouchOrMouseClientY(event)
            self._origX = DOM.getAbsoluteLeft(self.getElement())
            self._origY = DOM.getAbsoluteTop(self.getElement())
            DOM.setCapture(self.getElement())
            DOM.eventPreventDefault(event)

    def stopMovingWindow(self):
        self._dragging = False
        self.showDraggingCurtain(False)
        DOM.releaseCapture(self.getElement())

    def onEventPreview(self, event):
        if self._dragging:
            self.onDragEvent(event)
            return False
        elif self._resizing:
            self.onResizeEvent(event)
            return False
        elif self._vaadinModality:
            # return false when modal and outside window
            target = event.getEventTarget()
            if DOM.getCaptureElement() is not None:
                # Allow events when capture is set
                return True
            if not DOM.isOrHasChild(self.getElement(), target):
                # not within the modal window, but let's see if it's in the
                # debug window
                w = Util.findWidget(target, None)
                while w is not None:
                    if isinstance(w, VDebugConsole):
                        return True
                        # allow debug-window clicks
                    elif isinstance(w, Paintable):
                        return False
                    w = w.getParent()
                return False
        return True

    def addStyleDependentName(self, styleSuffix):
        # VWindow's getStyleElement() does not return the same element as
        # getElement(), so we need to override this.
        self.setStyleName(self.getElement(), self.getStylePrimaryName() + '-' + styleSuffix, True)

    def onAttach(self):
        super(VWindow, self).onAttach()
        self.setWidth(self._width)
        self.setHeight(self._height)

    def getAllocatedSpace(self, child):
        if child == self._layout:
            return self._renderSpace
        else:
            # Exception ??
            return None

    def hasChildComponent(self, component):
        if component == self._layout:
            return True
        else:
            return False

    def replaceChildComponent(self, oldComponent, newComponent):
        self._contentPanel.setWidget(newComponent)

    def requestLayout(self, child):
        if self._dynamicWidth and not self._layoutRelativeWidth:
            self.setNaturalWidth()
        if self._centered:
            self.center()
        self.updateShadowSizeAndPosition()
        # layout size change may affect its available space (scrollbars)
        self.client.handleComponentRelativeSize(self._layout)
        return True

    def updateCaption(self, component, uidl):
        # NOP, window has own caption, layout captio not rendered
        pass

    def getShortcutActionHandler(self):
        return self._shortcutHandler

    def onScroll(self, event):
        self.client.updateVariable(self._id, 'scrollTop', self._contentPanel.getScrollPosition(), False)
        self.client.updateVariable(self._id, 'scrollLeft', self._contentPanel.getHorizontalScrollPosition(), False)

    def onKeyDown(self, event):
        if self._shortcutHandler is not None:
            self._shortcutHandler.handleKeyboardEvent(Event.as_(event.getNativeEvent()))
            return

    def onBlur(self, event):
        if self.client.hasEventListeners(self, EventId.BLUR):
            self.client.updateVariable(self._id, EventId.BLUR, '', True)

    def onFocus(self, event):
        if self.client.hasEventListeners(self, EventId.FOCUS):
            self.client.updateVariable(self._id, EventId.FOCUS, '', True)

    def onBeforeShortcutAction(self, e):
        # NOP, nothing to update just avoid workaround ( causes excess
        # blur/focus )
        pass

    def focus(self):
        self._contentPanel.focus()
