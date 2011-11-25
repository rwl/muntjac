# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.ApplicationConfiguration import (ApplicationConfiguration,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.VLazyExecutor import (VLazyExecutor,)
from com.vaadin.terminal.gwt.client.SimpleTree import (SimpleTree,)
from com.vaadin.terminal.gwt.client.VUIDLBrowser import (VUIDLBrowser,)
from com.vaadin.terminal.gwt.client.ui.VOverlay import (VOverlay,)
from com.vaadin.terminal.gwt.client.Console import (Console,)
# from com.google.gwt.core.client.Scheduler.ScheduledCommand import (ScheduledCommand,)
# from com.google.gwt.dom.client.Style import (Style,)
# from com.google.gwt.dom.client.Style.FontWeight import (FontWeight,)
# from com.google.gwt.dom.client.Style.Overflow import (Overflow,)
# from com.google.gwt.dom.client.Style.Position import (Position,)
# from com.google.gwt.dom.client.Style.Unit import (Unit,)
# from com.google.gwt.event.dom.client.ClickEvent import (ClickEvent,)
# from com.google.gwt.event.dom.client.ClickHandler import (ClickHandler,)
# from com.google.gwt.event.dom.client.KeyCodes import (KeyCodes,)
# from com.google.gwt.event.shared.HandlerRegistration import (HandlerRegistration,)
# from com.google.gwt.event.shared.UmbrellaException import (UmbrellaException,)
# from com.google.gwt.http.client.UrlBuilder import (UrlBuilder,)
# from com.google.gwt.user.client.Cookies import (Cookies,)
# from com.google.gwt.user.client.Event.NativePreviewEvent import (NativePreviewEvent,)
# from com.google.gwt.user.client.Event.NativePreviewHandler import (NativePreviewHandler,)
# from com.google.gwt.user.client.EventPreview import (EventPreview,)
# from com.google.gwt.user.client.Window.Location import (Location,)
# from com.google.gwt.user.client.ui.Button import (Button,)
# from com.google.gwt.user.client.ui.CheckBox import (CheckBox,)
# from com.google.gwt.user.client.ui.HorizontalPanel import (HorizontalPanel,)
# from com.google.gwt.user.client.ui.Label import (Label,)
# from com.google.gwt.user.client.ui.Panel import (Panel,)
# from com.google.gwt.user.client.ui.RootPanel import (RootPanel,)
# from com.google.gwt.user.client.ui.VerticalPanel import (VerticalPanel,)
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

    def HighlightModeHandler(VDebugConsole_this, *args, **kwargs):

        class HighlightModeHandler(NativePreviewHandler):
            _label = None

            def __init__(self, label):
                self._label = label

            def onPreviewNativeEvent(self, event):
                if (
                    event.getTypeInt() == Event.ONKEYDOWN and event.getNativeEvent().getKeyCode() == KeyCodes.KEY_ESCAPE
                ):
                    VDebugConsole_this._highlightModeRegistration.removeHandler()
                    VUIDLBrowser.deHiglight()
                    return
                if event.getTypeInt() == Event.ONMOUSEMOVE:
                    VUIDLBrowser.deHiglight()
                    eventTarget = Util.getElementFromPoint(event.getNativeEvent().getClientX(), event.getNativeEvent().getClientY())
                    if self.getElement().isOrHasChild(eventTarget):
                        return
                    for a in ApplicationConfiguration.getRunningApplications():
                        paintable = Util.getPaintableForElement(a, a.getView(), eventTarget)
                        if paintable is None:
                            paintable = Util.getPaintableForElement(a, RootPanel.get(), eventTarget)
                        if paintable is not None:
                            pid = a.getPid(paintable)
                            VUIDLBrowser.highlight(paintable)
                            self._label.setText('Currently focused  :' + paintable.getClass() + ' ID:' + pid)
                            event.cancel()
                            event.consume()
                            event.getNativeEvent().stopPropagation()
                            return
                if event.getTypeInt() == Event.ONCLICK:
                    VUIDLBrowser.deHiglight()
                    event.cancel()
                    event.consume()
                    event.getNativeEvent().stopPropagation()
                    VDebugConsole_this._highlightModeRegistration.removeHandler()
                    eventTarget = Util.getElementFromPoint(event.getNativeEvent().getClientX(), event.getNativeEvent().getClientY())
                    for a in ApplicationConfiguration.getRunningApplications():
                        paintable = Util.getPaintableForElement(a, a.getView(), eventTarget)
                        if paintable is None:
                            paintable = Util.getPaintableForElement(a, RootPanel.get(), eventTarget)
                        if paintable is not None:
                            a.highlightComponent(paintable)
                            return
                event.cancel()

        return HighlightModeHandler(*args, **kwargs)

    _POS_COOKIE_NAME = 'VDebugConsolePos'
    _highlightModeRegistration = None
    _caption = DOM.createDiv()
    _panel = None
    _clear = Button('C')
    _restart = Button('R')
    _forceLayout = Button('FL')
    _analyzeLayout = Button('AL')
    _savePosition = Button('S')
    _highlight = Button('H')
    _hostedMode = CheckBox('GWT')
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
    _help = 'Drag title=move, shift-drag=resize, doubleclick title=min/max.' + 'Use debug=quiet to log only to browser console.'

    def __init__(self):
        super(VDebugConsole, self)(False, False)
        self.getElement().getStyle().setOverflow(Overflow.HIDDEN)
        self._clear.setTitle('Clear console')
        self._restart.setTitle('Restart app')
        self._forceLayout.setTitle('Force layout')
        self._analyzeLayout.setTitle('Analyze layouts')
        self._savePosition.setTitle('Save pos')

    class dragpreview(EventPreview):

        def onEventPreview(self, event):
            VDebugConsole_this.onBrowserEvent(event)
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
                    self._initialW = VDebugConsole_this.getOffsetWidth()
                    self._initialH = VDebugConsole_this.getOffsetHeight()
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
                    VDebugConsole_this.setPixelSize(w, h)
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
                    VDebugConsole_this.setPopupPosition(left, top)
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
        self.getElement().getStyle().setWidth(width, Unit.PX)

    def log(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], BaseException):
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
            if not VDebugConsole_this._msgQueue.isEmpty():
                requestBuilder = RequestBuilder(RequestBuilder.POST, VDebugConsole_this.getRemoteLogUrl())
                # TODO Auto-generated catch block
                try:
                    requestData = ''
                    for str in VDebugConsole_this._msgQueue:
                        requestData += str
                        requestData += '\n'

                    class _2_(RequestCallback):

                        def onResponseReceived(self, request, response):
                            # TODO Auto-generated method stub
                            pass

                        def onError(self, request, exception):
                            # TODO Auto-generated method stub
                            pass

                    _2_ = _2_()
                    requestBuilder.sendRequest(requestData, _2_)
                except RequestException, e:
                    e.printStackTrace()
                VDebugConsole_this._msgQueue.clear()

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
            if isinstance(_0[0], BaseException):
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
            vuidlBrowser = VUIDLBrowser(u, conf)
            vuidlBrowser.setText('Response:')
            self._panel.add(vuidlBrowser)
        self.consoleDir(u)
        # consoleLog(u.getChildrenAsXML());

    @classmethod
    def consoleDir(cls, u):
        JS("""
         if($wnd.console && $wnd.console.log) {
             if($wnd.console.dir) {
                 $wnd.console.dir(@{{u}});
             } else {
                 $wnd.console.log(@{{u}});
             }
         }

    """)
        pass

    @classmethod
    def consoleLog(cls, msg):
        JS("""
         if($wnd.console && $wnd.console.log) {
             $wnd.console.log(@{{msg}});
         }
     """)
        pass

    @classmethod
    def consoleErr(cls, msg):
        JS("""
         if($wnd.console) {
             if ($wnd.console.error)
                 $wnd.console.error(@{{msg}});
             else if ($wnd.console.log)
                 $wnd.console.log(@{{msg}});
         }
     """)
        pass

    def printLayoutProblems(self, meta, ac, zeroHeightComponents, zeroWidthComponents):
        valueMapArray = meta.getJSValueMapArray('invalidLayouts')
        size = len(valueMapArray)
        self._panel.add(HTML('<div>************************</di>' + '<h4>Layouts analyzed on server, total top level problems: ' + size + ' </h4>'))
        if size > 0:
            root = SimpleTree('Root problems')
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < size):
                    break
                self.printLayoutError(valueMapArray.get(i), root, ac)
            self._panel.add(root)
        if (len(zeroHeightComponents) > 0) or (len(zeroWidthComponents) > 0):
            self._panel.add(HTML('<h4> Client side notifications</h4>' + ' <em>The following relative sized components were ' + 'rendered to a zero size container on the client side.' + ' Note that these are not necessarily invalid ' + 'states, but reported here as they might be.</em>'))
            if len(zeroHeightComponents) > 0:
                self._panel.add(HTML('<p><strong>Vertically zero size:</strong><p>'))
                self.printClientSideDetectedIssues(zeroHeightComponents, ac)
            if len(zeroWidthComponents) > 0:
                self._panel.add(HTML('<p><strong>Horizontally zero size:</strong><p>'))
                self.printClientSideDetectedIssues(zeroWidthComponents, ac)
        self.log('************************')

    def printClientSideDetectedIssues(self, zeroHeightComponents, ac):
        for paintable in zeroHeightComponents:
            layout = Util.getLayout(paintable)
            errorDetails = VerticalPanel()
            errorDetails.add(Label('' + Util.getSimpleName(paintable) + ' inside ' + Util.getSimpleName(layout)))
            emphasisInUi = CheckBox('Emphasize components parent in UI (the actual component is not visible)')

            class _4_(ClickHandler):

                def onClick(self, event):
                    if self.paintable is not None:
                        element2 = self.layout.getElement()
                        Widget.setStyleName(element2, 'invalidlayout', self.emphasisInUi.getValue())

            _4_ = _4_()
            emphasisInUi.addClickHandler(_4_)
            errorDetails.add(emphasisInUi)
            self._panel.add(errorDetails)

    def printLayoutError(self, valueMap, root, ac):
        pid = valueMap.getString('id')
        paintable = ac.getPaintable(pid)
        errorNode = SimpleTree()
        errorDetails = VerticalPanel()
        errorDetails.add(Label(Util.getSimpleName(paintable) + ' id: ' + pid))
        if 'heightMsg' in valueMap:
            errorDetails.add(Label('Height problem: ' + valueMap.getString('heightMsg')))
        if 'widthMsg' in valueMap:
            errorDetails.add(Label('Width problem: ' + valueMap.getString('widthMsg')))
        emphasisInUi = CheckBox('Emphasize component in UI')

        class _5_(ClickHandler):

            def onClick(self, event):
                if self.paintable is not None:
                    element2 = self.paintable.getElement()
                    Widget.setStyleName(element2, 'invalidlayout', self.emphasisInUi.getValue())

        _5_ = _5_()
        emphasisInUi.addClickHandler(_5_)
        errorDetails.add(emphasisInUi)
        errorNode.add(errorDetails)
        if 'subErrors' in valueMap:
            l = HTML('<em>Expand this node to show problems that may be dependent on this problem.</em>')
            errorDetails.add(l)
            suberrors = valueMap.getJSValueMapArray('subErrors')
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(suberrors)):
                    break
                value = suberrors.get(i)
                self.printLayoutError(value, errorNode, ac)
        root.add(errorNode)

    def init(self):
        self._panel = FlowPanel()
        if not self._quietMode:
            DOM.appendChild(self.getContainerElement(), self._caption)
            self.setWidget(self._panel)
            self._caption.setClassName('v-debug-console-caption')
            self.setStyleName('v-debug-console')
            self.getElement().getStyle().setZIndex(20000)
            self.getElement().getStyle().setOverflow(Overflow.HIDDEN)
            self.sinkEvents(Event.ONDBLCLICK)
            self.sinkEvents(Event.MOUSEEVENTS)
            self._panel.setStyleName('v-debug-console-content')
            self._caption.setInnerHTML('Debug window')
            self._caption.getStyle().setHeight(25, Unit.PX)
            self._caption.setTitle(self._help)
            self.show()
            self.setToDefaultSizeAndPos()
            self._actions = HorizontalPanel()
            style = self._actions.getElement().getStyle()
            style.setPosition(Position.ABSOLUTE)
            style.setBackgroundColor('#666')
            style.setLeft(135, Unit.PX)
            style.setHeight(25, Unit.PX)
            style.setTop(0, Unit.PX)
            self._actions.add(self._clear)
            self._actions.add(self._restart)
            self._actions.add(self._forceLayout)
            self._actions.add(self._analyzeLayout)
            self._actions.add(self._highlight)
            self._highlight.setTitle('Select a component and print details about it to the server log and client side console.')
            self._actions.add(self._savePosition)
            self._savePosition.setTitle('Saves the position and size of debug console to a cookie')
            self._actions.add(self._autoScroll)
            self._actions.add(self._hostedMode)
            if Location.getParameter('gwt.codesvr') is not None:
                self._hostedMode.setValue(True)

            class _6_(ClickHandler):

                def onClick(self, event):
                    if VDebugConsole_this._hostedMode.getValue():
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

            _6_ = _6_()
            self._hostedMode.addClickHandler(_6_)
            self._autoScroll.setTitle('Automatically scroll so that new messages are visible')
            self._panel.add(self._actions)
            self._panel.add(HTML('<i>' + self._help + '</i>'))

            class _7_(ClickHandler):

                def onClick(self, event):
                    width = VDebugConsole_this._panel.getOffsetWidth()
                    height = VDebugConsole_this._panel.getOffsetHeight()
                    VDebugConsole_this._panel = FlowPanel()
                    VDebugConsole_this._panel.setPixelSize(width, height)
                    VDebugConsole_this._panel.setStyleName('v-debug-console-content')
                    VDebugConsole_this._panel.add(VDebugConsole_this._actions)
                    self.setWidget(VDebugConsole_this._panel)

            _7_ = _7_()
            self._clear.addClickHandler(_7_)

            class _8_(ClickHandler):

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

            _8_ = _8_()
            self._restart.addClickHandler(_8_)

            class _9_(ClickHandler):

                def onClick(self, event):
                    # TODO for each client in appconf force layout
                    # VDebugConsole.this.client.forceLayout();
                    pass

            _9_ = _9_()
            self._forceLayout.addClickHandler(_9_)

            class _10_(ClickHandler):

                def onClick(self, event):
                    runningApplications = ApplicationConfiguration.getRunningApplications()
                    for applicationConnection in runningApplications:
                        applicationConnection.analyzeLayouts()

            _10_ = _10_()
            self._analyzeLayout.addClickHandler(_10_)
            self._analyzeLayout.setTitle('Analyzes currently rendered view and ' + 'reports possible common problems in usage of relative sizes.' + 'Will cause server visit/rendering of whole screen and loss of' + ' all non committed variables form client side.')

            class _11_(ClickHandler):

                def onClick(self, event):
                    pos = self.getAbsoluteLeft() + ',' + self.getAbsoluteTop() + ',' + self.getOffsetWidth() + ',' + self.getOffsetHeight() + ',' + VDebugConsole_this._autoScroll.getValue()
                    Cookies.setCookie(VDebugConsole_this._POS_COOKIE_NAME, pos)

            _11_ = _11_()
            self._savePosition.addClickHandler(_11_)

            class _12_(ClickHandler):

                def onClick(self, event):
                    label = Label('--')
                    VDebugConsole_this.log('<i>Use mouse to select a component or click ESC to exit highlight mode.</i>')
                    VDebugConsole_this._panel.add(label)
                    VDebugConsole_this._highlightModeRegistration = Event.addNativePreviewHandler(VDebugConsole_this.HighlightModeHandler(label))

            _12_ = _12_()
            self._highlight.addClickHandler(_12_)
        self.log('Starting Vaadin client side engine. Widgetset: ' + GWT.getModuleName())
        self.log('Widget set is built on version: ' + ApplicationConfiguration.VERSION)
        self.logToDebugWindow('<div class=\"v-theme-version v-theme-version-' + ApplicationConfiguration.VERSION.replaceAll('\\.', '_') + '\">Warning: widgetset version ' + ApplicationConfiguration.VERSION + ' does not seem to match theme version </div>', True)

    def setQuietMode(self, quietDebugMode):
        self._quietMode = quietDebugMode
