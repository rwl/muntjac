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

from __pyjamas__ import (ARGERROR, PREINC,)
from com.vaadin.terminal.gwt.client.ui.ClickEventHandler import (ClickEventHandler,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
from com.vaadin.terminal.gwt.client.ui.ShortcutActionHandler import (ShortcutActionHandler,)
from com.vaadin.terminal.gwt.client.Container import (Container,)
from com.vaadin.terminal.gwt.client.ui.VTextField import (VTextField,)
from com.vaadin.terminal.gwt.client.RenderSpace import (RenderSpace,)
from com.vaadin.terminal.gwt.client.ui.VNotification import (VNotification,)
from com.vaadin.terminal.gwt.client.ApplicationConnection import (ApplicationConnection,)
from com.vaadin.terminal.gwt.client.ui.VLazyExecutor import (VLazyExecutor,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.Focusable import (Focusable,)
# from com.google.gwt.event.logical.shared.ResizeEvent import (ResizeEvent,)
# from com.google.gwt.event.logical.shared.ResizeHandler import (ResizeHandler,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.HashSet import (HashSet,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedHashSet import (LinkedHashSet,)
# from java.util.Set import (Set,)
ShortcutActionHandlerOwner = ShortcutActionHandler.ShortcutActionHandlerOwner


class VView(SimplePanel, Container, ResizeHandler, Window.ClosingHandler, ShortcutActionHandlerOwner, Focusable):
    _CLASSNAME = 'v-view'
    NOTIFICATION_HTML_CONTENT_NOT_ALLOWED = 'useplain'
    _theme = None
    _layout = None
    _subWindows = LinkedHashSet()
    _id = None
    _actionHandler = None
    # stored width for IE resize optimization
    _width = None
    # stored height for IE resize optimization
    _height = None
    _connection = None
    # We are postponing resize process with IE. IE bugs with scrollbars in some
    # situations, that causes false onWindowResized calls. With Timer we will
    # give IE some time to decide if it really wants to keep current size
    # (scrollbars).

    _resizeTimer = None
    _scrollTop = None
    _scrollLeft = None
    _rendering = None
    _scrollable = None
    _immediate = None
    _resizeLazy = False
    RESIZE_LAZY = 'rL'
    # Reference to the parent frame/iframe. Null if there is no parent (i)frame
    # or if the application and parent frame are in different domains.

    _parentFrame = None

    class clickEventHandler(ClickEventHandler):

        def registerHandler(self, handler, type):
            return self.addDomHandler(handler, type)

    _delayedResizeExecutor = 
    class _1_(ScheduledCommand):

        def execute(self):
            VView_this.windowSizeMaybeChanged(Window.getClientWidth(), Window.getClientHeight())

    _1_ = _1_()
    VLazyExecutor(200, _1_)

    def __init__(self):
        super(VView, self)()
        self.setStyleName(self._CLASSNAME)
        # Allow focusing the view by using the focus() method, the view
        # should not be in the document focus flow
        self.getElement().setTabIndex(-1)

    def windowSizeMaybeChanged(self, newWidth, newHeight):
        """Called when the window might have been resized.

        @param newWidth
                   The new width of the window
        @param newHeight
                   The new height of the window
        """
        changed = False
        if self._width != newWidth:
            self._width = newWidth
            changed = True
            VConsole.log('New window width: ' + self._width)
        if self._height != newHeight:
            self._height = newHeight
            changed = True
            VConsole.log('New window height: ' + self._height)
        if changed:
            VConsole.log('Running layout functions due to window resize')
            self._connection.runDescendentsLayout(VView_this)
            Util.runWebkitOverflowAutoFix(self.getElement())
            self.sendClientResized()

    def getTheme(self):
        return self._theme

    @classmethod
    def reloadHostPage(cls):
        """Used to reload host page on theme changes."""
        JS("""
         $wnd.location.reload();
     """)
        pass

    @classmethod
    def eval(cls, script):
        """Evaluate the given script in the browser document.

        @param script
                   Script to be executed.
        """
        JS("""
      try {
         if (@{{script}} == null) return;
         $wnd.eval(@{{script}});
      } catch (e) {
      }
    """)
        pass

    def isEmbedded(self):
        """Returns true if the body is NOT generated, i.e if someone else has made
        the page that we're running in. Otherwise we're in charge of the whole
        page.

        @return true if we're running embedded
        """
        return not self.getElement().getOwnerDocument().getBody().getClassName().contains(ApplicationConnection.GENERATED_BODY_CLASSNAME)

    def updateFromUIDL(self, uidl, client):
        self._rendering = True
        self._id = uidl.getId()
        firstPaint = self._connection is None
        self._connection = client
        self._immediate = uidl.hasAttribute('immediate')
        self._resizeLazy = uidl.hasAttribute(self.RESIZE_LAZY)
        newTheme = uidl.getStringAttribute('theme')
        if self._theme is not None and not (newTheme == self._theme):
            # Complete page refresh is needed due css can affect layout
            # calculations etc
            self.reloadHostPage()
        else:
            self._theme = newTheme
        if uidl.hasAttribute('style'):
            self.setStyleName(self.getStylePrimaryName() + ' ' + uidl.getStringAttribute('style'))
        if uidl.hasAttribute('name'):
            client.setWindowName(uidl.getStringAttribute('name'))
        self.clickEventHandler.handleEventHandlerRegistration(client)
        if not self.isEmbedded():
            # only change window title if we're in charge of the whole page
            self.com.google.gwt.user.client.Window.setTitle(uidl.getStringAttribute('caption'))
        # Process children
        childIndex = 0
        # Open URL:s
        isClosed = False
        # was this window closed?
        while (
            childIndex < uidl.getChildCount() and 'open' == uidl.getChildUIDL(childIndex).getTag()
        ):
            open = uidl.getChildUIDL(childIndex)
            url = client.translateVaadinUri(open.getStringAttribute('src'))
            target = open.getStringAttribute('name')
            if target is None:
                # source will be opened to this browser window, but we may have
                # to finish rendering this window in case this is a download
                # (and window stays open).

                class _1_(Command):

                    def execute(self):
                        VView_this.goTo(self.url)

                _1_ = _1_()
                Scheduler.get().scheduleDeferred(_1_)
            elif '_self' == target:
                # This window is closing (for sure). Only other opens are
                # relevant in this change. See #3558, #2144
                isClosed = True
                self.goTo(url)
            else:
                if open.hasAttribute('border'):
                    if open.getStringAttribute('border') == 'minimal':
                        options = 'menubar=yes,location=no,status=no'
                    else:
                        options = 'menubar=no,location=no,status=no'
                else:
                    options = 'resizable=yes,menubar=yes,toolbar=yes,directories=yes,location=yes,scrollbars=yes,status=yes'
                if open.hasAttribute('width'):
                    w = open.getIntAttribute('width')
                    options += ',width=' + w
                if open.hasAttribute('height'):
                    h = open.getIntAttribute('height')
                    options += ',height=' + h
                Window.open(url, target, options)
            childIndex += 1
        if isClosed:
            # don't render the content, something else will be opened to this
            # browser view
            self._rendering = False
            return
        # Draw this application level window
        childUidl = uidl.getChildUIDL(childIndex)
        lo = client.getPaintable(childUidl)
        if self._layout is not None:
            if self._layout != lo:
                # remove old
                client.unregisterPaintable(self._layout)
                # add new
                self.setWidget(lo)
                self._layout = lo
        else:
            self.setWidget(lo)
            self._layout = lo
        self._layout.updateFromUIDL(childUidl, client)
        if not childUidl.getBooleanAttribute('cached'):
            self.updateParentFrameSize()
        # Save currently open subwindows to track which will need to be closed
        removedSubWindows = set(self._subWindows)
        # Handle other UIDL children
        while (
            childUidl = uidl.getChildUIDL(PREINC(globals(), locals(), 'childIndex')) is not None
        ):
            tag = childUidl.getTag().intern()
            if tag == 'actions':
                if self._actionHandler is None:
                    self._actionHandler = ShortcutActionHandler(self._id, client)
                self._actionHandler.updateActionMap(childUidl)
            elif tag == 'execJS':
                script = childUidl.getStringAttribute('script')
                self.eval(script)
            elif tag == 'notifications':
                _0 = True
                it = childUidl.getChildIterator()
                while True:
                    if _0 is True:
                        _0 = False
                    if not it.hasNext():
                        break
                    notification = it.next()
                    VNotification.showNotification(client, notification)
            else:
                # subwindows
                w = client.getPaintable(childUidl)
                if self._subWindows.contains(w):
                    removedSubWindows.remove(w)
                else:
                    self._subWindows.add(w)
                w.updateFromUIDL(childUidl, client)
        # Close old windows which where not in UIDL anymore
        _1 = True
        rem = removedSubWindows
        while True:
            if _1 is True:
                _1 = False
            if not rem.hasNext():
                break
            w = rem.next()
            client.unregisterPaintable(w)
            self._subWindows.remove(w)
            w.hide()
        if uidl.hasAttribute('focused'):
            # set focused component when render phase is finished

            class _2_(Command):

                def execute(self):
                    toBeFocused = self.uidl.getPaintableAttribute('focused', VView_this._connection)
                    # Two types of Widgets can be focused, either implementing
                    # GWT HasFocus of a thinner Vaadin specific Focusable
                    # interface.

                    if isinstance(toBeFocused, self.com.google.gwt.user.client.ui.Focusable):
                        toBeFocusedWidget = toBeFocused
                        toBeFocusedWidget.setFocus(True)
                    elif isinstance(toBeFocused, Focusable):
                        toBeFocused.focus()
                    else:
                        VConsole.log('Could not focus component')

            _2_ = _2_()
            Scheduler.get().scheduleDeferred(_2_)
        # Add window listeners on first paint, to prevent premature
        # variablechanges
        if firstPaint:
            Window.addWindowClosingHandler(self)
            Window.addResizeHandler(self)
        self.onResize()
        # finally set scroll position from UIDL
        if uidl.hasVariable('scrollTop'):
            self._scrollable = True
            self._scrollTop = uidl.getIntVariable('scrollTop')
            DOM.setElementPropertyInt(self.getElement(), 'scrollTop', self._scrollTop)
            self._scrollLeft = uidl.getIntVariable('scrollLeft')
            DOM.setElementPropertyInt(self.getElement(), 'scrollLeft', self._scrollLeft)
        else:
            self._scrollable = False
        # Safari workaround must be run after scrollTop is updated as it sets
        # scrollTop using a deferred command.
        if BrowserInfo.get().isSafari():
            Util.runWebkitOverflowAutoFix(self.getElement())
        self.scrollIntoView(uidl)
        self._rendering = False

    def scrollIntoView(self, uidl):
        """Tries to scroll paintable referenced from given UIDL snippet to be
        visible.

        @param uidl
        """
        if uidl.hasAttribute('scrollTo'):

            class _3_(Command):

                def execute(self):
                    paintable = self.uidl.getPaintableAttribute('scrollTo', VView_this._connection)
                    paintable.getElement().scrollIntoView()

            _3_ = _3_()
            Scheduler.get().scheduleDeferred(_3_)

    def onBrowserEvent(self, event):
        super(VView, self).onBrowserEvent(event)
        type = DOM.eventGetType(event)
        if type == Event.ONKEYDOWN and self._actionHandler is not None:
            self._actionHandler.handleKeyboardEvent(event)
            return
        elif self._scrollable and type == Event.ONSCROLL:
            self.updateScrollPosition()

    def updateScrollPosition(self):
        """Updates scroll position from DOM and saves variables to server."""
        # (non-Javadoc)
        # 
        # @see
        # com.google.gwt.event.logical.shared.ResizeHandler#onResize(com.google
        # .gwt.event.logical.shared.ResizeEvent)

        oldTop = self._scrollTop
        oldLeft = self._scrollLeft
        self._scrollTop = DOM.getElementPropertyInt(self.getElement(), 'scrollTop')
        self._scrollLeft = DOM.getElementPropertyInt(self.getElement(), 'scrollLeft')
        if self._connection is not None and not self._rendering:
            if oldTop != self._scrollTop:
                self._connection.updateVariable(self._id, 'scrollTop', self._scrollTop, False)
            if oldLeft != self._scrollLeft:
                self._connection.updateVariable(self._id, 'scrollLeft', self._scrollLeft, False)

    def onResize(self, *args):
        """None
        ---
        Called when a resize event is received.
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            lazy = (self._resizeLazy or (BrowserInfo.get().isIE() and BrowserInfo.get().getIEVersion() <= 8)) or BrowserInfo.get().isFF3()
            if lazy:
                self._delayedResizeExecutor.trigger()
            else:
                self.windowSizeMaybeChanged(Window.getClientWidth(), Window.getClientHeight())
        elif _1 == 1:
            event, = _0
            self.onResize()
        else:
            raise ARGERROR(0, 1)

    # IE (pre IE9 at least) will give us some false resize events due to
    # problems with scrollbars. Firefox 3 might also produce some extra
    # events. We postpone both the re-layouting and the server side event
    # for a while to deal with these issues.
    # 
    # We may also postpone these events to avoid slowness when resizing the
    # browser window. Constantly recalculating the layout causes the resize
    # operation to be really slow with complex layouts.

    def sendClientResized(self):
        """Send new dimensions to the server."""
        self._connection.updateVariable(self._id, 'height', self._height, False)
        self._connection.updateVariable(self._id, 'width', self._width, self._immediate)

    @classmethod
    def goTo(cls, url):
        JS("""
       $wnd.location = @{{url}};
     """)
        pass

    def onWindowClosing(self, event):
        # Change focus on this window in order to ensure that all state is
        # collected from textfields
        # TODO this is a naive hack, that only works with text fields and may
        # cause some odd issues. Should be replaced with a decent solution, see
        # also related BeforeShortcutActionListener interface. Same interface
        # might be usable here.
        VTextField.flushChangesFromFocusedTextField()
        # Send the closing state to server
        self._connection.updateVariable(self._id, 'close', True, False)
        self._connection.sendPendingVariableChangesSync()

    class myRenderSpace(RenderSpace):
        _excessHeight = -1
        _excessWidth = -1

        def getHeight(self):
            return self.getElement().getOffsetHeight() - self.getExcessHeight()

        def getExcessHeight(self):
            if self._excessHeight < 0:
                self.detectExcessSize()
            return self._excessHeight

        def detectExcessSize(self):
            # TODO define that iview cannot be themed and decorations should
            # get to parent element, then get rid of this expensive and error
            # prone function
            overflow = self.getElement().getStyle().getProperty('overflow')
            self.getElement().getStyle().setProperty('overflow', 'hidden')
            if (
                BrowserInfo.get().isIE() and self.getElement().getPropertyInt('clientWidth') == 0
            ):
                # can't detect possibly themed border/padding width in some
                # situations (with some layout configurations), use empty div
                # to measure width properly
                div = Document.get().createDivElement()
                div.setInnerHTML('&nbsp;')
                div.getStyle().setProperty('overflow', 'hidden')
                div.getStyle().setProperty('height', '1px')
                self.getElement().appendChild(div)
                self._excessWidth = self.getElement().getOffsetWidth() - div.getOffsetWidth()
                self.getElement().removeChild(div)
            else:
                self._excessWidth = self.getElement().getOffsetWidth() - self.getElement().getPropertyInt('clientWidth')
            self._excessHeight = self.getElement().getOffsetHeight() - self.getElement().getPropertyInt('clientHeight')
            self.getElement().getStyle().setProperty('overflow', overflow)

        def getWidth(self):
            w = self.getRealWidth()
            if w < 10 and BrowserInfo.get().isIE7():
                # Overcome an IE7 bug #3295
                Util.shakeBodyElement()
                w = self.getRealWidth()
            return w

        def getRealWidth(self):
            if VView_this._connection.getConfiguration().isStandalone():
                return self.getElement().getOffsetWidth() - self.getExcessWidth()
            # If not running standalone, there might be multiple Vaadin apps
            # that won't shrink with the browser window as the components have
            # calculated widths (#3125)
            # Find all Vaadin applications on the page
            vaadinApps = list()
            VView_this.loadAppIdListFromDOM(vaadinApps)
            # Store original styles here so they can be restored
            originalDisplays = list(len(vaadinApps))
            ownAppId = VView_this._connection.getConfiguration().getRootPanelId()
            # Set display: none for all Vaadin apps
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(vaadinApps)):
                    break
                appId = vaadinApps[i]
                if appId == ownAppId:
                    # Only hide the contents of current application
                    targetElement = VView_this._layout.getElement()
                else:
                    # Hide everything for other applications
                    targetElement = Document.get().getElementById(appId)
                layoutStyle = targetElement.getStyle()
                originalDisplays.add(i, layoutStyle.getDisplay())
                layoutStyle.setDisplay(Display.NONE)
            w = self.getElement().getOffsetWidth() - self.getExcessWidth()
            # Then restore the old display style before returning
            _1 = True
            i = 0
            while True:
                if _1 is True:
                    _1 = False
                else:
                    i += 1
                if not (i < len(vaadinApps)):
                    break
                appId = vaadinApps[i]
                if appId == ownAppId:
                    targetElement = VView_this._layout.getElement()
                else:
                    targetElement = Document.get().getElementById(appId)
                layoutStyle = targetElement.getStyle()
                originalDisplay = originalDisplays[i]
                if len(originalDisplay) == 0:
                    layoutStyle.clearDisplay()
                else:
                    layoutStyle.setProperty('display', originalDisplay)
            return w

        def getExcessWidth(self):
            if self._excessWidth < 0:
                self.detectExcessSize()
            return self._excessWidth

        def getScrollbarSize(self):
            return Util.getNativeScrollbarSize()

    @classmethod
    def loadAppIdListFromDOM(cls, list):
        JS("""
         var j;
         for(j in $wnd.vaadin.vaadinConfigurations) {
            @{{list}}.@java.util.Collection::add(Ljava/lang/Object;)(j);
         }
     """)
        pass

    def getAllocatedSpace(self, child):
        return self.myRenderSpace

    def hasChildComponent(self, component):
        return component is not None and component == self._layout

    def replaceChildComponent(self, oldComponent, newComponent):
        # TODO This is untested as no layouts require this
        if oldComponent != self._layout:
            return
        self.setWidget(newComponent)
        self._layout = newComponent

    def requestLayout(self, child):
        # Can never propagate further and we do not want need to re-layout the
        # layout which has caused this request.

        self.updateParentFrameSize()
        # layout size change may affect its available space (scrollbars)
        self._connection.handleComponentRelativeSize(self._layout)
        return True

    def updateParentFrameSize(self):
        if self._parentFrame is None:
            return
        childHeight = Util.getRequiredHeight(self.getWidget().getElement())
        childWidth = Util.getRequiredWidth(self.getWidget().getElement())
        self._parentFrame.getStyle().setPropertyPx('width', childWidth)
        self._parentFrame.getStyle().setPropertyPx('height', childHeight)

    @classmethod
    def getParentFrame(cls):
        JS("""
        try {
            var frameElement = $wnd.frameElement;
            if (frameElement == null) {
                return null;
            }
            if (frameElement.getAttribute("autoResize") == "true") {
                return frameElement;
            }
        } catch (e) {
        }
        return null;
    """)
        pass

    def updateCaption(self, component, uidl):
        # NOP Subwindows never draw caption for their first child (layout)
        pass

    def getSubWindowList(self):
        """Return an iterator for current subwindows. This method is meant for
        testing purposes only.

        @return
        """
        windows = list(len(self._subWindows))
        for widget in self._subWindows:
            windows.add(widget)
        return windows

    def init(self, rootPanelId, applicationConnection):
        DOM.sinkEvents(self.getElement(), Event.ONKEYDOWN | Event.ONSCROLL)
        # iview is focused when created so element needs tabIndex
        # 1 due 0 is at the end of natural tabbing order
        DOM.setElementProperty(self.getElement(), 'tabIndex', '1')
        root = RootPanel.get(rootPanelId)
        # Remove the v-app-loading or any splash screen added inside the div by
        # the user
        root.getElement().setInnerHTML('')
        # For backwards compatibility with static index pages only.
        # No longer added by AbstractApplicationServlet/Portlet
        root.removeStyleName('v-app-loading')
        root.add(self)
        if applicationConnection.getConfiguration().isStandalone():
            # set focus to iview element by default to listen possible keyboard
            # shortcuts. For embedded applications this is unacceptable as we
            # don't want to steal focus from the main page nor we don't want
            # side-effects from focusing (scrollIntoView).
            self.getElement().focus()
        self._parentFrame = self.getParentFrame()

    def getShortcutActionHandler(self):
        return self._actionHandler

    def focus(self):
        self.getElement().focus()
