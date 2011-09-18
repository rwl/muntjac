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

from com.vaadin.terminal.gwt.client.Container import (Container,)
from com.vaadin.terminal.gwt.client.Focusable import (Focusable,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.RenderInformation import (RenderInformation,)
from com.vaadin.terminal.gwt.client.ui.Icon import (Icon,)
from com.vaadin.terminal.gwt.client.ui.TouchScrollDelegate import (TouchScrollDelegate,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.RenderSpace import (RenderSpace,)
from com.vaadin.terminal.gwt.client.ui.ShortcutActionHandler import (ShortcutActionHandler, ShortcutActionHandlerOwner,)
# from com.google.gwt.dom.client.DivElement import (DivElement,)
# from com.google.gwt.dom.client.Document import (Document,)
# from com.google.gwt.event.dom.client.DomEvent.Type import (Type,)
# from com.google.gwt.event.dom.client.TouchStartEvent import (TouchStartEvent,)
# from com.google.gwt.event.dom.client.TouchStartHandler import (TouchStartHandler,)
# from com.google.gwt.event.shared.EventHandler import (EventHandler,)
# from com.google.gwt.event.shared.HandlerRegistration import (HandlerRegistration,)
# from com.google.gwt.user.client.DOM import (DOM,)
# from com.google.gwt.user.client.Element import (Element,)
# from com.google.gwt.user.client.Event import (Event,)
# from com.google.gwt.user.client.ui.SimplePanel import (SimplePanel,)
# from com.google.gwt.user.client.ui.Widget import (Widget,)
# from com.vaadin.terminal.gwt.client.ui.ShortcutActionHandler.ShortcutActionHandlerOwner import (ShortcutActionHandlerOwner,)
# from java.util.Set import (Set,)


class VPanel(SimplePanel, Container, ShortcutActionHandlerOwner, Focusable):
    CLICK_EVENT_IDENTIFIER = 'click'
    CLASSNAME = 'v-panel'
    _client = None
    _id = None
    _captionNode = DOM.createDiv()
    _captionText = DOM.createSpan()
    _icon = None
    _bottomDecoration = DOM.createDiv()
    _contentNode = DOM.createDiv()
    _errorIndicatorElement = None
    _height = None
    _layout = None
    _shortcutHandler = None
    _width = ''
    _geckoCaptionMeter = None
    _scrollTop = None
    _scrollLeft = None
    _renderInformation = RenderInformation()
    _borderPaddingHorizontal = -1
    _borderPaddingVertical = -1
    _captionPaddingHorizontal = -1
    _captionMarginLeft = -1
    _rendering = None
    _contentMarginLeft = -1
    _previousStyleName = None



#    private ClickEventHandler clickEventHandler = new ClickEventHandler(this,
#            CLICK_EVENT_IDENTIFIER) {
#
#        @Override
#        protected <H extends EventHandler> HandlerRegistration registerHandler(
#                H handler, Type<H> type) {
#            return addDomHandler(handler, type);
#        }
#    };
#    private TouchScrollDelegate touchScrollDelegate;
#
#    public VPanel() {
#        super();
#        DivElement captionWrap = Document.get().createDivElement();
#        captionWrap.appendChild(captionNode);
#        captionNode.appendChild(captionText);
#
#        captionWrap.setClassName(CLASSNAME + "-captionwrap");
#        captionNode.setClassName(CLASSNAME + "-caption");
#        contentNode.setClassName(CLASSNAME + "-content");
#        bottomDecoration.setClassName(CLASSNAME + "-deco");
#
#        getElement().appendChild(captionWrap);
#
#        /*
#         * Make contentNode focusable only by using the setFocus() method. This
#         * behaviour can be changed by invoking setTabIndex() in the serverside
#         * implementation
#         */
#        contentNode.setTabIndex(-1);
#
#        getElement().appendChild(contentNode);
#
#        getElement().appendChild(bottomDecoration);
#        setStyleName(CLASSNAME);
#        DOM.sinkEvents(getElement(), Event.ONKEYDOWN);
#        DOM.sinkEvents(contentNode, Event.ONSCROLL | Event.TOUCHEVENTS);
#        contentNode.getStyle().setProperty("position", "relative");
#        getElement().getStyle().setProperty("overflow", "hidden");
#        addHandler(new TouchStartHandler() {
#            public void onTouchStart(TouchStartEvent event) {
#                getTouchScrollDelegate().onTouchStart(event);
#            }
#        }, TouchStartEvent.getType());
#    }


    def setFocus(self, focus):
        """Sets the keyboard focus on the Panel

        @param focus
                   Should the panel have focus or not.
        """
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.gwt.client.Focusable#focus()

        if focus:
            self.getContainerElement().focus()
        else:
            self.getContainerElement().blur()

    def focus(self):
        self.setFocus(True)

    def getContainerElement(self):
        return self._contentNode

    def setCaption(self, text):
        DOM.setInnerHTML(self._captionText, text)

    def updateFromUIDL(self, uidl, client):
        self._rendering = True
        if not uidl.hasAttribute('cached'):
            # Handle caption displaying and style names, prior generics.
            # Affects size
            # calculations
            # Restore default stylenames
            self._contentNode.setClassName(self.CLASSNAME + '-content')
            self._bottomDecoration.setClassName(self.CLASSNAME + '-deco')
            self._captionNode.setClassName(self.CLASSNAME + '-caption')
            hasCaption = False
            if (
                uidl.hasAttribute('caption') and not (uidl.getStringAttribute('caption') == '')
            ):
                self.setCaption(uidl.getStringAttribute('caption'))
                hasCaption = True
            else:
                self.setCaption('')
                self._captionNode.setClassName(self.CLASSNAME + '-nocaption')
            # Add proper stylenames for all elements. This way we can prevent
            # unwanted CSS selector inheritance.
            if uidl.hasAttribute('style'):
                styles = uidl.getStringAttribute('style').split(' ')
                captionBaseClass = self.CLASSNAME + ('-caption' if hasCaption else '-nocaption')
                contentBaseClass = self.CLASSNAME + '-content'
                decoBaseClass = self.CLASSNAME + '-deco'
                captionClass = captionBaseClass
                contentClass = contentBaseClass
                decoClass = decoBaseClass
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(styles)):
                        break
                    captionClass += ' ' + captionBaseClass + '-' + styles[i]
                    contentClass += ' ' + contentBaseClass + '-' + styles[i]
                    decoClass += ' ' + decoBaseClass + '-' + styles[i]
                self._captionNode.setClassName(captionClass)
                self._contentNode.setClassName(contentClass)
                self._bottomDecoration.setClassName(decoClass)
        # Ensure correct implementation
        if client.updateComponent(self, uidl, False):
            self._rendering = False
            return
        self.clickEventHandler.handleEventHandlerRegistration(client)
        self._client = client
        self._id = uidl.getId()
        self.setIconUri(uidl, client)
        self.handleError(uidl)
        # Render content
        layoutUidl = uidl.getChildUIDL(0)
        newLayout = client.getPaintable(layoutUidl)
        if newLayout != self._layout:
            if self._layout is not None:
                client.unregisterPaintable(self._layout)
            self.setWidget(newLayout)
            self._layout = newLayout
        self._layout.updateFromUIDL(layoutUidl, client)
        # We may have actions attached to this panel
        if uidl.getChildCount() > 1:
            cnt = uidl.getChildCount()
            _1 = True
            i = 1
            while True:
                if _1 is True:
                    _1 = False
                else:
                    i += 1
                if not (i < cnt):
                    break
                childUidl = uidl.getChildUIDL(i)
                if childUidl.getTag() == 'actions':
                    if self._shortcutHandler is None:
                        self._shortcutHandler = ShortcutActionHandler(self._id, client)
                    self._shortcutHandler.updateActionMap(childUidl)
        if (
            uidl.hasVariable('scrollTop') and uidl.getIntVariable('scrollTop') != self._scrollTop
        ):
            self._scrollTop = uidl.getIntVariable('scrollTop')
            self._contentNode.setScrollTop(self._scrollTop)
            # re-read the actual scrollTop in case invalid value was set
            # (scrollTop != 0 when no scrollbar exists, other values would be
            # caught by scroll listener), see #3784
            self._scrollTop = self._contentNode.getScrollTop()
        if (
            uidl.hasVariable('scrollLeft') and uidl.getIntVariable('scrollLeft') != self._scrollLeft
        ):
            self._scrollLeft = uidl.getIntVariable('scrollLeft')
            self._contentNode.setScrollLeft(self._scrollLeft)
            # re-read the actual scrollTop in case invalid value was set
            # (scrollTop != 0 when no scrollbar exists, other values would be
            # caught by scroll listener), see #3784
            self._scrollLeft = self._contentNode.getScrollLeft()
        # Must be run after scrollTop is set as Webkit overflow fix re-sets the
        # scrollTop
        self.runHacks(False)
        # And apply tab index
        if uidl.hasVariable('tabindex'):
            self._contentNode.setTabIndex(uidl.getIntVariable('tabindex'))
        self._rendering = False

    def setStyleName(self, style):
        if not (style == self._previousStyleName):
            super(VPanel, self).setStyleName(style)
            self.detectContainerBorders()
            self._previousStyleName = style

    def handleError(self, uidl):
        if uidl.hasAttribute('error'):
            if self._errorIndicatorElement is None:
                self._errorIndicatorElement = DOM.createSpan()
                DOM.setElementProperty(self._errorIndicatorElement, 'className', 'v-errorindicator')
                DOM.sinkEvents(self._errorIndicatorElement, Event.MOUSEEVENTS)
                self.sinkEvents(Event.MOUSEEVENTS)
            DOM.insertBefore(self._captionNode, self._errorIndicatorElement, self._captionText)
        elif self._errorIndicatorElement is not None:
            DOM.removeChild(self._captionNode, self._errorIndicatorElement)
            self._errorIndicatorElement = None

    def setIconUri(self, uidl, client):
        iconUri = uidl.getStringAttribute('icon') if uidl.hasAttribute('icon') else None
        if iconUri is None:
            if self._icon is not None:
                DOM.removeChild(self._captionNode, self._icon.getElement())
                self._icon = None
        else:
            if self._icon is None:
                self._icon = Icon(client)
                DOM.insertChild(self._captionNode, self._icon.getElement(), 0)
            self._icon.setUri(iconUri)

    def runHacks(self, runGeckoFix):
        if (
            BrowserInfo.get().isIE6() and self._width is not None and not (self._width == '')
        ):
            # IE6 requires overflow-hidden elements to have a width specified
            # so we calculate the width of the content and caption nodes when
            # no width has been specified.

            # Fixes #1923 VPanel: Horizontal scrollbar does not appear in IE6
            # with wide content

            # Caption must be shrunk for parent measurements to return correct
            # result in IE6

            DOM.setStyleAttribute(self._captionNode, 'width', '1px')
            parentPadding = Util.measureHorizontalPaddingAndBorder(self.getElement(), 0)
            parentWidthExcludingPadding = self.getElement().getOffsetWidth() - parentPadding
            Util.setWidthExcludingPaddingAndBorder(self._captionNode, parentWidthExcludingPadding - self.getCaptionMarginLeft(), 26, False)
            contentMarginLeft = self.getContentMarginLeft()
            Util.setWidthExcludingPaddingAndBorder(self._contentNode, parentWidthExcludingPadding - contentMarginLeft, 2, False)
        if (
            BrowserInfo.get().isIE() or BrowserInfo.get().isFF2() and (self._width is None) or (self._width == '')
        ):
            # IE and FF2 needs width to be specified for the root DIV so we
            # calculate that from the sizes of the caption and layout

            captionWidth = self._captionText.getOffsetWidth() + self.getCaptionMarginLeft() + self.getCaptionPaddingHorizontal()
            layoutWidth = self._layout.getOffsetWidth() + self.getContainerBorderWidth()
            width = layoutWidth
            if captionWidth > width:
                width = captionWidth
            if BrowserInfo.get().isIE7():
                Util.setWidthExcludingPaddingAndBorder(self._captionNode, width - self.getCaptionMarginLeft(), 26, False)
            super(VPanel, self).setWidth(width + 'px')
        if runGeckoFix and BrowserInfo.get().isGecko():
            # workaround for #1764
            if (width is None) or (width == ''):
                if self._geckoCaptionMeter is None:
                    self._geckoCaptionMeter = DOM.createDiv()
                    DOM.appendChild(self._captionNode, self._geckoCaptionMeter)
                captionWidth = DOM.getElementPropertyInt(self._captionText, 'offsetWidth')
                availWidth = DOM.getElementPropertyInt(self._geckoCaptionMeter, 'offsetWidth')
                if captionWidth == availWidth:
                    # Caption width defines panel width -> Gecko based browsers
                    # somehow fails to float things right, without the
                    # "noncode" below

                    self.setWidth(self.getOffsetWidth() + 'px')
                else:
                    DOM.setStyleAttribute(self._captionNode, 'width', '')
        self._client.runDescendentsLayout(self)
        Util.runWebkitOverflowAutoFix(self._contentNode)

    def onBrowserEvent(self, event):
        super(VPanel, self).onBrowserEvent(event)
        target = DOM.eventGetTarget(event)
        type = DOM.eventGetType(event)
        if type == Event.ONKEYDOWN and self._shortcutHandler is not None:
            self._shortcutHandler.handleKeyboardEvent(event)
            return
        if type == Event.ONSCROLL:
            newscrollTop = DOM.getElementPropertyInt(self._contentNode, 'scrollTop')
            newscrollLeft = DOM.getElementPropertyInt(self._contentNode, 'scrollLeft')
            if (
                self._client is not None and (newscrollLeft != self._scrollLeft) or (newscrollTop != self._scrollTop)
            ):
                self._scrollLeft = newscrollLeft
                self._scrollTop = newscrollTop
                self._client.updateVariable(self._id, 'scrollTop', self._scrollTop, False)
                self._client.updateVariable(self._id, 'scrollLeft', self._scrollLeft, False)
        elif self._captionNode.isOrHasChild(target):
            if self._client is not None:
                self._client.handleTooltipEvent(event, self)

    def getTouchScrollDelegate(self):
        if self.touchScrollDelegate is None:
            self.touchScrollDelegate = TouchScrollDelegate(self._contentNode)
        return self.touchScrollDelegate

    def setHeight(self, height):
        self._height = height
        super(VPanel, self).setHeight(height)
        if height is not None and not ('' == height):
            targetHeight = self.getOffsetHeight()
            containerHeight = targetHeight - self._captionNode.getParentElement().getOffsetHeight() - self._bottomDecoration.getOffsetHeight() - self.getContainerBorderHeight()
            if containerHeight < 0:
                containerHeight = 0
            DOM.setStyleAttribute(self._contentNode, 'height', containerHeight + 'px')
        else:
            DOM.setStyleAttribute(self._contentNode, 'height', '')
        if not self._rendering:
            self.runHacks(True)

    def getCaptionMarginLeft(self):
        if self._captionMarginLeft < 0:
            self.detectContainerBorders()
        return self._captionMarginLeft

    def getContentMarginLeft(self):
        if self._contentMarginLeft < 0:
            self.detectContainerBorders()
        return self._contentMarginLeft

    def getCaptionPaddingHorizontal(self):
        if self._captionPaddingHorizontal < 0:
            self.detectContainerBorders()
        return self._captionPaddingHorizontal

    def getContainerBorderHeight(self):
        if self._borderPaddingVertical < 0:
            self.detectContainerBorders()
        return self._borderPaddingVertical

    def setWidth(self, width):
        if self._width == width:
            return
        self._width = width
        super(VPanel, self).setWidth(width)
        if not self._rendering:
            self.runHacks(True)
            if self._height == '':
                # Width change may affect height
                Util.updateRelativeChildrenAndSendSizeUpdateEvent(self._client, self)

    def getContainerBorderWidth(self):
        if self._borderPaddingHorizontal < 0:
            self.detectContainerBorders()
        return self._borderPaddingHorizontal

    def detectContainerBorders(self):
        DOM.setStyleAttribute(self._contentNode, 'overflow', 'hidden')
        self._borderPaddingHorizontal = Util.measureHorizontalBorder(self._contentNode)
        self._borderPaddingVertical = Util.measureVerticalBorder(self._contentNode)
        DOM.setStyleAttribute(self._contentNode, 'overflow', 'auto')
        self._captionPaddingHorizontal = Util.measureHorizontalPaddingAndBorder(self._captionNode, 26)
        self._captionMarginLeft = Util.measureMarginLeft(self._captionNode)
        self._contentMarginLeft = Util.measureMarginLeft(self._contentNode)

    def hasChildComponent(self, component):
        if component is not None and component == self._layout:
            return True
        else:
            return False

    def replaceChildComponent(self, oldComponent, newComponent):
        # TODO This is untested as no layouts require this
        if oldComponent != self._layout:
            return
        self.setWidget(newComponent)
        self._layout = newComponent

    def getAllocatedSpace(self, child):
        w = 0
        h = 0
        if self._width is not None and not (self._width == ''):
            w = self.getOffsetWidth() - self.getContainerBorderWidth()
            if w < 0:
                w = 0
        if self._height is not None and not (self._height == ''):
            h = self._contentNode.getOffsetHeight() - self.getContainerBorderHeight()
            if h < 0:
                h = 0
        return RenderSpace(w, h, True)

    def requestLayout(self, child):
        # content size change might cause change to its available space
        # (scrollbars)
        self._client.handleComponentRelativeSize(self._layout)
        if (
            self._height is not None and self._height != '' and self._width is not None and self._width != ''
        ):
            # If the height and width has been specified the child components
            # cannot make the size of the layout change

            return True
        self.runHacks(False)
        return not self._renderInformation.updateSize(self.getElement())

    def updateCaption(self, component, uidl):
        # NOP: layouts caption, errors etc not rendered in Panel
        pass

    def onAttach(self):
        super(VPanel, self).onAttach()
        self.detectContainerBorders()

    def getShortcutActionHandler(self):
        return self._shortcutHandler
