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
from com.vaadin.terminal.gwt.client.ApplicationConfiguration import (ApplicationConfiguration,)
from com.vaadin.terminal.gwt.client.ui.VOverlay import (VOverlay,)
from com.vaadin.terminal.gwt.client.ui.VLazyExecutor import (VLazyExecutor,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.VUIDLBrowser import (VUIDLBrowser,)
from com.vaadin.terminal.gwt.client.Console import (Console,)
# from com.google.gwt.core.client.GWT import (GWT,)
# from com.google.gwt.core.client.JsArray import (JsArray,)
# from com.google.gwt.core.client.Scheduler.ScheduledCommand import (ScheduledCommand,)
# from com.google.gwt.dom.client.Style.FontWeight import (FontWeight,)
# from com.google.gwt.event.dom.client.ClickEvent import (ClickEvent,)
# from com.google.gwt.event.dom.client.ClickHandler import (ClickHandler,)
# from com.google.gwt.event.shared.UmbrellaException import (UmbrellaException,)
# from com.google.gwt.http.client.Request import (Request,)
# from com.google.gwt.http.client.RequestBuilder import (RequestBuilder,)
# from com.google.gwt.http.client.RequestCallback import (RequestCallback,)
# from com.google.gwt.http.client.RequestException import (RequestException,)
# from com.google.gwt.http.client.Response import (Response,)
# from com.google.gwt.http.client.UrlBuilder import (UrlBuilder,)
# from com.google.gwt.user.client.Cookies import (Cookies,)
# from com.google.gwt.user.client.DOM import (DOM,)
# from com.google.gwt.user.client.Element import (Element,)
# from com.google.gwt.user.client.Event import (Event,)
# from com.google.gwt.user.client.EventPreview import (EventPreview,)
# from com.google.gwt.user.client.Window import (Window,)
# from com.google.gwt.user.client.Window.Location import (Location,)
# from com.google.gwt.user.client.ui.Button import (Button,)
# from com.google.gwt.user.client.ui.CheckBox import (CheckBox,)
# from com.google.gwt.user.client.ui.FlowPanel import (FlowPanel,)
# from com.google.gwt.user.client.ui.HTML import (HTML,)
# from com.google.gwt.user.client.ui.HorizontalPanel import (HorizontalPanel,)
# from com.google.gwt.user.client.ui.Label import (Label,)
# from com.google.gwt.user.client.ui.Panel import (Panel,)
# from com.google.gwt.user.client.ui.Tree import (Tree,)
# from com.google.gwt.user.client.ui.TreeItem import (TreeItem,)
# from com.google.gwt.user.client.ui.VerticalPanel import (VerticalPanel,)
# from com.google.gwt.user.client.ui.Widget import (Widget,)
# from java.util.LinkedList import (LinkedList,)
# from java.util.List import (List,)
# from java.util.Set import (Set,)


class VDebugConsole(VOverlay, Console):
    """A helper console for client side development. The debug console can also be
    used to resolve layout issues, inspect the communication between browser and
    the server, start GWT dev mode and restart application.

    <p>
    This implementation is used vaadin is in debug mode (see manual) and
    developer appends "?debug" query parameter to url. Debug information can also
    be shown on browsers internal console only, by appending "?debug=quiet" query
    parameter.
    <p>
    This implementation can be overridden with GWT deferred binding.
    """
    _POS_COOKIE_NAME = 'VDebugConsolePos'
    _caption = DOM.createDiv()
    _panel = None
    _clear = Button('Clear console')
    _restart = Button('Restart app')
    _forceLayout = Button('Force layout')
    _analyzeLayout = Button('Analyze layouts')
    _savePosition = Button('Save pos')
    _hostedMode = CheckBox('GWT dev mode ')
    _autoScroll = CheckBox('Autoscroll ')
    _actions = None
    _collapsed = False
    _resizing = None
    _startX = None
    _startY = None
    _initialW = None
    _initialH = None
    _moving = False
    _origTop = None
    _origLeft = None
    _help = 'Drag=move, shift-drag=resize, doubleclick=min/max.' + 'Use debug=quiet to log only to browser console.'

    def __init__(self):
        super(VDebugConsole, self)(False, False)

    class dragpreview(EventPreview):

        def onEventPreview(self, event):
            self.onBrowserEvent(event)
            return False

    _quietMode = None

    def onBrowserEvent(self, event):
        super(VDebugConsole, self).onBrowserEvent(event)
        _0 = DOM.eventGetType(event)
        _1 = False
        while True:
            if _0 == Event.ONMOUSEDOWN:
                _1 = True
                if DOM.eventGetShiftKey(event):
                    self._resizing = True
                    DOM.setCapture(self.getElement())
                    self._startX = DOM.eventGetScreenX(event)
                    self._startY = DOM.eventGetScreenY(event)
                    self._initialW = _VDebugConsole_this.getOffsetWidth()
                    self._initialH = _VDebugConsole_this.getOffsetHeight()
                    DOM.eventCancelBubble(event, True)
                    DOM.eventPreventDefault(event)
                    DOM.addEventPreview(self.dragpreview)
                elif DOM.eventGetTarget(event) == self._caption:
                    self._moving = True
                    self._startX = DOM.eventGetScreenX(event)
                    self._startY = DOM.eventGetScreenY(event)
                    self._origTop = self.getAbsoluteTop()
                    self._origLeft = self.getAbsoluteLeft()
                    DOM.eventCancelBubble(event, True)
                    DOM.eventPreventDefault(event)
                    DOM.addEventPreview(self.dragpreview)
                break
            if (_1 is True) or (_0 == Event.ONMOUSEMOVE):
                _1 = True
                if self._resizing:
                    deltaX = self._startX - DOM.eventGetScreenX(event)
                    detalY = self._startY - DOM.eventGetScreenY(event)
                    w = self._initialW - deltaX
                    if w < 30:
                        w = 30
                    h = self._initialH - detalY
                    if h < 40:
                        h = 40
                    _VDebugConsole_this.setPixelSize(w, h)
                    DOM.eventCancelBubble(event, True)
                    DOM.eventPreventDefault(event)
                elif self._moving:
                    deltaX = self._startX - DOM.eventGetScreenX(event)
                    detalY = self._startY - DOM.eventGetScreenY(event)
                    left = self._origLeft - deltaX
                    if left < 0:
                        left = 0
                    top = self._origTop - detalY
                    if top < 0:
                        top = 0
                    _VDebugConsole_this.setPopupPosition(left, top)
                    DOM.eventCancelBubble(event, True)
                    DOM.eventPreventDefault(event)
                break
            if (_1 is True) or (_0 == Event.ONLOSECAPTURE):
                _1 = True
            if (_1 is True) or (_0 == Event.ONMOUSEUP):
                _1 = True
                if self._resizing:
                    DOM.releaseCapture(self.getElement())
                    self._resizing = False
                elif self._moving:
                    DOM.releaseCapture(self.getElement())
                    self._moving = False
                DOM.removeEventPreview(self.dragpreview)
                break
            if (_1 is True) or (_0 == Event.ONDBLCLICK):
                _1 = True
                if DOM.eventGetTarget(event) == self._caption:
                    if self._collapsed:
                        self._panel.setVisible(True)
                        self.setToDefaultSizeAndPos()
                    else:
                        self._panel.setVisible(False)
                        self.setPixelSize(120, 20)
                        self.setPopupPosition(Window.getClientWidth() - 125, Window.getClientHeight() - 25)
                    self._collapsed = not self._collapsed
                break
            if True:
                _1 = True
                break
            break

    def setToDefaultSizeAndPos(self):
        cookie = Cookies.getCookie(self._POS_COOKIE_NAME)
        autoScrollValue = False
        if cookie is not None:
            split = cookie.split(',')
            left = int(split[0])
            top = int(split[1])
            width = int(split[2])
            height = int(split[3])
            autoScrollValue = Boolean.valueOf.valueOf(split[4])
        else:
            width = 400
            height = 150
            top = Window.getClientHeight() - 160
            left = Window.getClientWidth() - 410
        self.setPixelSize(width, height)
        self.setPopupPosition(left, top)
        self._autoScroll.setValue(autoScrollValue)

    def setPixelSize(self, width, height):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.gwt.client.Console#log(java.lang.String)

        if height < 20:
            height = 20
        if width < 2:
            width = 2
        self._panel.setHeight((height - 20) + 'px')
        self._panel.setWidth((width - 2) + 'px')

    def log(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Throwable):
                e, = _0
                if isinstance(e, UmbrellaException):
                    ue = e
                    for t in ue.getCauses():
                        self.log(t)
                    return
                self.log(Util.getSimpleName(e) + ': ' + e.getMessage())
                GWT.log(e.getMessage(), e)
            else:
                msg, = _0
                if msg is None:
                    msg = 'null'
                # remoteLog(msg);
                self.logToDebugWindow(msg, False)
                GWT.log(msg)
                self.consoleLog(msg)
        else:
            raise ARGERROR(1, 1)

    _msgQueue = LinkedList()

    class doSend(ScheduledCommand):

        def execute(self):
            if not self.msgQueue.isEmpty():
                requestBuilder = RequestBuilder(RequestBuilder.POST, self.getRemoteLogUrl())
                # TODO Auto-generated catch block
                try:
                    requestData = ''
                    for str in self.msgQueue:
                        requestData += str
                        requestData += '\n'

                    class _2_(RequestCallback):

                        def onResponseReceived(self, request, response):
                            # TODO Auto-generated method stub
                            pass

                        def onError(self, request, exception):
                            # TODO Auto-generated method stub
                            pass

                    _2_ = self._2_()
                    requestBuilder.sendRequest(requestData, _2_)
                except RequestException, e:
                    e.printStackTrace()
                self.msgQueue.clear()

    _sendToRemoteLog = VLazyExecutor(350, doSend)

    def getRemoteLogUrl(self):
        return 'http://sun-vehje.local:8080/remotelog/'

    def remoteLog(self, msg):
        self._msgQueue.add(msg)
        self._sendToRemoteLog.trigger()

    def logToDebugWindow(self, msg, error):
        """Logs the given message to the debug window.

        @param msg
                   The message to log. Must not be null.
        """
        if error:
            row = self.createErrorHtml(msg)
        else:
            row = HTML(msg)
        self._panel.add(row)
        if self._autoScroll.getValue():
            row.getElement().scrollIntoView()

    def createErrorHtml(self, msg):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.gwt.client.Console#error(java.lang.String)

        html = HTML(msg)
        html.getElement().getStyle().setColor('#f00')
        html.getElement().getStyle().setFontWeight(FontWeight.BOLD)
        return html

    def error(self, *args):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.gwt.client.Console#printObject(java.lang.
        # Object)

        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Throwable):
                e, = _0
                if isinstance(e, UmbrellaException):
                    ue = e
                    for t in ue.getCauses():
                        self.error(t)
                    return
                self.error(Util.getSimpleName(e) + ': ' + e.getMessage())
                GWT.log(e.getMessage(), e)
            else:
                msg, = _0
                if msg is None:
                    msg = 'null'
                self.logToDebugWindow(msg, True)
                GWT.log(msg)
                self.consoleErr(msg)
        else:
            raise ARGERROR(1, 1)

    def printObject(self, msg):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.gwt.client.Console#dirUIDL(com.vaadin
        # .terminal.gwt.client.UIDL)

        if msg is None:
            str = 'null'
        else:
            str = str(msg)
        self._panel.add(Label(str))
        self.consoleLog(str)

    def dirUIDL(self, u, conf):
        if self._panel.isAttached():
            self._panel.add(VUIDLBrowser(u, conf))
        self.consoleDir(u)
        # consoleLog(u.getChildrenAsXML());

    @classmethod
    def consoleDir(cls, u):
        # -{
        #          if($wnd.console && $wnd.console.log) {
        #              if($wnd.console.dir) {
        #                  $wnd.console.dir(u);
        #              } else {
        #                  $wnd.console.log(u);
        #              }
        #          }
        #
        #     }-

        pass

    @classmethod
    def consoleLog(cls, msg):
        # -{
        #          if($wnd.console && $wnd.console.log) {
        #              $wnd.console.log(msg);
        #          }
        #      }-

        pass

    @classmethod
    def consoleErr(cls, msg):
        # -{
        #          if($wnd.console) {
        #              if ($wnd.console.error)
        #                  $wnd.console.error(msg);
        #              else if ($wnd.console.log)
        #                  $wnd.console.log(msg);
        #          }
        #      }-

        pass


#    public void printLayoutProblems(ValueMap meta, ApplicationConnection ac,
#            Set<Paintable> zeroHeightComponents,
#            Set<Paintable> zeroWidthComponents) {
#        JsArray<ValueMap> valueMapArray = meta
#                .getJSValueMapArray("invalidLayouts");
#        int size = valueMapArray.length();
#        panel.add(new HTML("<div>************************</di>"
#                + "<h4>Layouts analyzed on server, total top level problems: "
#                + size + " </h4>"));
#        if (size > 0) {
#            Tree tree = new Tree();
#
#            // Position relative does not work here in IE7
#            DOM.setStyleAttribute(tree.getElement(), "position", "");
#
#            TreeItem root = new TreeItem("Root problems");
#            for (int i = 0; i < size; i++) {
#                printLayoutError(valueMapArray.get(i), root, ac);
#            }
#            panel.add(tree);
#            tree.addItem(root);
#
#        }
#        if (zeroHeightComponents.size() > 0 || zeroWidthComponents.size() > 0) {
#            panel.add(new HTML("<h4> Client side notifications</h4>"
#                    + " <em>The following relative sized components were "
#                    + "rendered to a zero size container on the client side."
#                    + " Note that these are not necessarily invalid "
#                    + "states, but reported here as they might be.</em>"));
#            if (zeroHeightComponents.size() > 0) {
#                panel.add(new HTML(
#                        "<p><strong>Vertically zero size:</strong><p>"));
#                printClientSideDetectedIssues(zeroHeightComponents, ac);
#            }
#            if (zeroWidthComponents.size() > 0) {
#                panel.add(new HTML(
#                        "<p><strong>Horizontally zero size:</strong><p>"));
#                printClientSideDetectedIssues(zeroWidthComponents, ac);
#            }
#        }
#        log("************************");
#    }
#
#    private void printClientSideDetectedIssues(
#            Set<Paintable> zeroHeightComponents, ApplicationConnection ac) {
#        for (final Paintable paintable : zeroHeightComponents) {
#            final Container layout = Util.getLayout((Widget) paintable);
#
#            VerticalPanel errorDetails = new VerticalPanel();
#            errorDetails.add(new Label("" + Util.getSimpleName(paintable)
#                    + " inside " + Util.getSimpleName(layout)));
#            final CheckBox emphasisInUi = new CheckBox(
#                    "Emphasize components parent in UI (the actual component is not visible)");
#            emphasisInUi.addClickHandler(new ClickHandler() {
#                public void onClick(ClickEvent event) {
#                    if (paintable != null) {
#                        Element element2 = ((Widget) layout).getElement();
#                        Widget.setStyleName(element2, "invalidlayout",
#                                emphasisInUi.getValue());
#                    }
#                }
#            });
#            errorDetails.add(emphasisInUi);
#            panel.add(errorDetails);
#        }
#    }
#
#    private void printLayoutError(ValueMap valueMap, TreeItem parent,
#            final ApplicationConnection ac) {
#        final String pid = valueMap.getString("id");
#        final Paintable paintable = ac.getPaintable(pid);
#
#        TreeItem errorNode = new TreeItem();
#        VerticalPanel errorDetails = new VerticalPanel();
#        errorDetails.add(new Label(Util.getSimpleName(paintable) + " id: "
#                + pid));
#        if (valueMap.containsKey("heightMsg")) {
#            errorDetails.add(new Label("Height problem: "
#                    + valueMap.getString("heightMsg")));
#        }
#        if (valueMap.containsKey("widthMsg")) {
#            errorDetails.add(new Label("Width problem: "
#                    + valueMap.getString("widthMsg")));
#        }
#        final CheckBox emphasisInUi = new CheckBox("Emphasize component in UI");
#        emphasisInUi.addClickHandler(new ClickHandler() {
#            public void onClick(ClickEvent event) {
#                if (paintable != null) {
#                    Element element2 = ((Widget) paintable).getElement();
#                    Widget.setStyleName(element2, "invalidlayout",
#                            emphasisInUi.getValue());
#                }
#            }
#        });
#        errorDetails.add(emphasisInUi);
#        errorNode.setWidget(errorDetails);
#        if (valueMap.containsKey("subErrors")) {
#            HTML l = new HTML(
#                    "<em>Expand this node to show problems that may be dependent on this problem.</em>");
#            errorDetails.add(l);
#            JsArray<ValueMap> suberrors = valueMap
#                    .getJSValueMapArray("subErrors");
#            for (int i = 0; i < suberrors.length(); i++) {
#                ValueMap value = suberrors.get(i);
#                printLayoutError(value, errorNode, ac);
#            }
#
#        }
#        parent.addItem(errorNode);
#    }

    def init(self):
        self._panel = FlowPanel()
        if not self._quietMode:
            DOM.appendChild(self.getContainerElement(), self._caption)
            self.setWidget(self._panel)
            self._caption.setClassName('v-debug-console-caption')
            self.setStyleName('v-debug-console')
            DOM.setStyleAttribute(self.getElement(), 'zIndex', 20000 + '')
            DOM.setStyleAttribute(self.getElement(), 'overflow', 'hidden')
            self.sinkEvents(Event.ONDBLCLICK)
            self.sinkEvents(Event.MOUSEEVENTS)
            self._panel.setStyleName('v-debug-console-content')
            self._caption.setInnerHTML('Debug window')
            self._caption.setTitle(self._help)
            self.show()
            self.setToDefaultSizeAndPos()
            self._actions = HorizontalPanel()
            self._actions.add(self._clear)
            self._actions.add(self._restart)
            self._actions.add(self._forceLayout)
            self._actions.add(self._analyzeLayout)
            self._actions.add(self._savePosition)
            self._savePosition.setTitle('Saves the position and size of debug console to a cookie')
            self._actions.add(self._autoScroll)
            self._actions.add(self._hostedMode)
            if Location.getParameter('gwt.codesvr') is not None:
                self._hostedMode.setValue(True)

            class _4_(ClickHandler):

                def onClick(self, event):
                    if self.hostedMode.getValue():
                        self.addHMParameter()
                    else:
                        self.removeHMParameter()

                def addHMParameter(self):
                    createUrlBuilder = Location.createUrlBuilder()
                    createUrlBuilder.setParameter('gwt.codesvr', 'localhost:9997')
                    Location.assign(createUrlBuilder.buildString())

                def removeHMParameter(self):
                    createUrlBuilder = Location.createUrlBuilder()
                    createUrlBuilder.removeParameter('gwt.codesvr')
                    Location.assign(createUrlBuilder.buildString())

            _4_ = self._4_()
            self._hostedMode.addClickHandler(_4_)
            self._autoScroll.setTitle('Automatically scroll so that new messages are visible')
            self._panel.add(self._actions)
            self._panel.add(HTML('<i>' + self._help + '</i>'))

            class _5_(ClickHandler):

                def onClick(self, event):
                    width = self.panel.getOffsetWidth()
                    height = self.panel.getOffsetHeight()
                    self.panel = FlowPanel()
                    self.panel.setPixelSize(width, height)
                    self.panel.setStyleName('v-debug-console-content')
                    self.panel.add(self.actions)
                    self.setWidget(self.panel)

            _5_ = self._5_()
            self._clear.addClickHandler(_5_)

            class _6_(ClickHandler):

                def onClick(self, event):
                    queryString = Window.Location.getQueryString()
                    if queryString is not None and queryString.contains('restartApplications'):
                        Window.Location.reload()
                    else:
                        url = Location.getHref()
                        separator = '?'
                        if url.contains('?'):
                            separator = '&'
                        if not url.contains('restartApplication'):
                            url += separator
                            url += 'restartApplication'
                        if not ('' == Location.getHash()):
                            hash = Location.getHash()
                            url = url.replace(hash, '') + hash
                        Window.Location.replace(url)

            _6_ = self._6_()
            self._restart.addClickHandler(_6_)

            class _7_(ClickHandler):

                def onClick(self, event):
                    # TODO for each client in appconf force layout
                    # VDebugConsole.this.client.forceLayout();
                    pass

            _7_ = self._7_()
            self._forceLayout.addClickHandler(_7_)

            class _8_(ClickHandler):

                def onClick(self, event):
                    runningApplications = ApplicationConfiguration.getRunningApplications()
                    for applicationConnection in runningApplications:
                        applicationConnection.analyzeLayouts()

            _8_ = self._8_()
            self._analyzeLayout.addClickHandler(_8_)
            self._analyzeLayout.setTitle('Analyzes currently rendered view and ' + 'reports possible common problems in usage of relative sizes.' + 'Will cause server visit/rendering of whole screen and loss of' + ' all non committed variables form client side.')

            class _9_(ClickHandler):

                def onClick(self, event):
                    pos = self.getAbsoluteLeft() + ',' + self.getAbsoluteTop() + ',' + self.getOffsetWidth() + ',' + self.getOffsetHeight() + ',' + self.autoScroll.getValue()
                    Cookies.setCookie(self.POS_COOKIE_NAME, pos)

            _9_ = self._9_()
            self._savePosition.addClickHandler(_9_)
        self.log('Starting Vaadin client side engine. Widgetset: ' + GWT.getModuleName())
        self.log('Widget set is built on version: ' + ApplicationConfiguration.VERSION)
        self.logToDebugWindow('<div class=\"v-theme-version v-theme-version-' + ApplicationConfiguration.VERSION.replaceAll('\\.', '_') + '\">Warning: widgetset version ' + ApplicationConfiguration.VERSION + ' does not seem to match theme version </div>', True)

    def setQuietMode(self, quietDebugMode):
        self._quietMode = quietDebugMode
