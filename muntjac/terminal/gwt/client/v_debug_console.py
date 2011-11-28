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

from __pyjamas__ import JS

import pygwt as GWT

from pyjamas import DOM, Window, Cookies, Location

from pyjamas.ui import Event, HTML, RootPanel

from pyjamas.ui.Button import Button
from pyjamas.ui.CheckBox import CheckBox
from pyjamas.ui.Label import Label
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.Widget import Widget
from pyjamas.ui.FlowPanel import FlowPanel
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.KeyboardListener import KEY_ESCAPE

from muntjac.terminal.gwt.client.application_configuration \
    import ApplicationConfiguration

from muntjac.terminal.gwt.client.util import Util
from muntjac.terminal.gwt.client.console import IConsole
from muntjac.terminal.gwt.client.simple_tree import SimpleTree
from muntjac.terminal.gwt.client.v_uidl_browser import VUIDLBrowser
from muntjac.terminal.gwt.client.ui.v_overlay import VOverlay
from muntjac.terminal.gwt.client.ui.v_lazy_executor import VLazyExecutor


class VDebugConsole(VOverlay, IConsole):
    """A helper console for client side development. The debug console can also
    be used to resolve layout issues, inspect the communication between browser
    and the server, start GWT dev mode and restart application.

    This implementation is used vaadin is in debug mode (see manual) and
    developer appends "?debug" query parameter to url. Debug information can
    also be shown on browsers internal console only, by appending
    "?debug=quiet" query parameter.

    This implementation can be overridden with GWT deferred binding.
    """

    _POS_COOKIE_NAME = 'VDebugConsolePos'

    _help = ('Drag title=move, shift-drag=resize, doubleclick title=min/max.'
            + 'Use debug=quiet to log only to browser console.')

    def __init__(self):
        self._highlightModeRegistration = None

        self._caption = DOM.createDiv()

        self._panel = None

        self._clear = Button('C')

        self._restart = Button('R')

        self._forceLayout = Button('FL')

        self._analyzeLayout = Button('AL')

        self._savePosition = Button('S')

        self._highlight = Button('H')

        self._hostedMode = CheckBox('GWT')

        self._autoScroll = CheckBox('Autoscroll ')

        self._actions = None

        self._collapsed = False

        self._resizing = None

        self._startX = None

        self._startY = None

        self._initialW = None

        self._initialH = None

        self._moving = False

        self._origTop = None

        self._origLeft = None

        super(VDebugConsole, self)(False, False)

        self.getElement().getStyle().setOverflow('hidden')

        self._clear.setTitle('Clear console')

        self._restart.setTitle('Restart app')

        self._forceLayout.setTitle('Force layout')

        self._analyzeLayout.setTitle('Analyze layouts')

        self._savePosition.setTitle('Save pos')

        self._dragpreview = DragPreview(self)

        self._quietMode = None

        self._msgQueue = list()

        self.doSend = DoSend()

        self._sendToRemoteLog = VLazyExecutor(350, self.doSend)


    def onBrowserEvent(self, event):
        super(VDebugConsole, self).onBrowserEvent(event)
        etype = DOM.eventGetType(event)
        if etype == Event.ONMOUSEDOWN:
            if DOM.eventGetShiftKey(event):
                self._resizing = True
                DOM.setCapture(self.getElement())
                self._startX = DOM.eventGetScreenX(event)
                self._startY = DOM.eventGetScreenY(event)
                self._initialW = self.getOffsetWidth()
                self._initialH = self.getOffsetHeight()
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

        elif etype == Event.ONMOUSEMOVE:
            if self._resizing:
                deltaX = self._startX - DOM.eventGetScreenX(event)
                detalY = self._startY - DOM.eventGetScreenY(event)
                w = self._initialW - deltaX
                if w < 30:
                    w = 30
                h = self._initialH - detalY
                if h < 40:
                    h = 40
                self.setPixelSize(w, h)
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
                self.setPopupPosition(left, top)
                DOM.eventCancelBubble(event, True)
                DOM.eventPreventDefault(event)

        elif etype == Event.ONLOSECAPTURE:
            pass
        elif etype == Event.ONMOUSEUP:
            if self._resizing:
                DOM.releaseCapture(self.getElement())
                self._resizing = False
            elif self._moving:
                DOM.releaseCapture(self.getElement())
                self._moving = False
            DOM.removeEventPreview(self.dragpreview)

        elif etype == Event.ONDBLCLICK:
            if DOM.eventGetTarget(event) == self._caption:
                if self._collapsed:
                    self._panel.setVisible(True)
                    self.setToDefaultSizeAndPos()
                else:
                    self._panel.setVisible(False)
                    self.setPixelSize(120, 20)
                    self.setPopupPosition(Window.getClientWidth()
                            - 125, Window.getClientHeight() - 25)
                self._collapsed = not self._collapsed


    def setToDefaultSizeAndPos(self):
        cookie = Cookies.getCookie(self._POS_COOKIE_NAME)
        autoScrollValue = False
        if cookie is not None:
            split = cookie.split(',')
            left = int(split[0])
            top = int(split[1])
            width = int(split[2])
            height = int(split[3])
            autoScrollValue = bool(split[4])
        else:
            width = 400
            height = 150
            top = Window.getClientHeight() - 160
            left = Window.getClientWidth() - 410
        self.setPixelSize(width, height)
        self.setPopupPosition(left, top)
        self._autoScroll.setValue(autoScrollValue)


    def setPixelSize(self, width, height):
        if height < 20:
            height = 20

        if width < 2:
            width = 2

        self._panel.setHeight((height - 20) + 'px')
        self._panel.setWidth((width - 2) + 'px')
        self.getElement().getStyle().setWidth(width, 'px')


    def log(self, e_or_msg):
        if isinstance(e_or_msg, BaseException):
            e = e_or_msg
            if isinstance(e, UmbrellaException):
                ue = e
                for t in ue.getCauses():
                    self.log(t)
                return
            self.log(Util.getSimpleName(e) + ': ' + e.getMessage())
            GWT.log(e.getMessage(), e)
        else:
            msg = e_or_msg
            if msg is None:
                msg = 'null'
            # remoteLog(msg);
            self.logToDebugWindow(msg, False)
            GWT.log(msg)
            self.consoleLog(msg)


    def getRemoteLogUrl(self):
        return 'http://sun-vehje.local:8080/remotelog/'


    def remoteLog(self, msg):
        self._msgQueue.add(msg)
        self._sendToRemoteLog.trigger()


    def logToDebugWindow(self, msg, error):
        """Logs the given message to the debug window.

        @param msg:
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
        html = HTML(msg)
        html.getElement().getStyle().setColor('#f00')
        html.getElement().getStyle().setFontWeight('bold')
        return html


    def error(self, e_or_msg):
        if isinstance(e_or_msg, BaseException):
            e = e_or_msg
            if isinstance(e, UmbrellaException):
                ue = e
                for t in ue.getCauses():
                    self.error(t)
                return
            self.error(Util.getSimpleName(e) + ': ' + e.getMessage())
            GWT.log(e.getMessage(), e)
        else:
            msg = e_or_msg
            if msg is None:
                msg = 'null'
            self.logToDebugWindow(msg, True)
            GWT.log(msg)
            self.consoleErr(msg)


    def printObject(self, msg):
        if msg is None:
            string = 'null'
        else:
            string = string(msg)
        self._panel.add(Label(string))
        self.consoleLog(string)


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


    def printLayoutProblems(self, meta, ac, zeroHeightComponents,
                zeroWidthComponents):
        valueMapArray = meta.getJSValueMapArray('invalidLayouts')
        size = len(valueMapArray)
        self._panel.add(HTML('<div>************************</di>'
                + '<h4>Layouts analyzed on server, total top level problems: '
                + size + ' </h4>'))
        if size > 0:
            root = SimpleTree('Root problems')

            for i in range(size):
                self.printLayoutError(valueMapArray.get(i), root, ac)

            self._panel.add(root)

        if (len(zeroHeightComponents) > 0) or (len(zeroWidthComponents) > 0):
            self._panel.add(HTML('<h4> Client side notifications</h4>'
                    + ' <em>The following relative sized components were '
                    + 'rendered to a zero size container on the client side.'
                    + ' Note that these are not necessarily invalid '
                    + 'states, but reported here as they might be.</em>'))
            if len(zeroHeightComponents) > 0:
                self._panel.add(HTML(
                        '<p><strong>Vertically zero size:</strong><p>'))
                self.printClientSideDetectedIssues(zeroHeightComponents, ac)

            if len(zeroWidthComponents) > 0:
                self._panel.add(HTML(
                        '<p><strong>Horizontally zero size:</strong><p>'))
                self.printClientSideDetectedIssues(zeroWidthComponents, ac)

        self.log('************************')


    def printClientSideDetectedIssues(self, zeroHeightComponents, ac):
        for paintable in zeroHeightComponents:
            layout = Util.getLayout(paintable)

            errorDetails = VerticalPanel()
            errorDetails.add(Label(Util.getSimpleName(paintable)
                    + ' inside ' + Util.getSimpleName(layout)))
            emphasisInUi = CheckBox(
                    'Emphasize components parent in UI (the actual component is not visible)')

            class PrintHandler(ClickHandler):

                def onClick(self, event):
                    if self.paintable is not None:
                        element2 = self.layout.getElement()
                        Widget.setStyleName(element2, 'invalidlayout',
                                self.emphasisInUi.getValue())

            emphasisInUi.addClickHandler(PrintHandler())
            errorDetails.add(emphasisInUi)
            self._panel.add(errorDetails)


    def printLayoutError(self, valueMap, root, ac):
        pid = valueMap.getString('id')
        paintable = ac.getPaintable(pid)

        errorNode = SimpleTree()
        errorDetails = VerticalPanel()
        errorDetails.add(Label(Util.getSimpleName(paintable) + ' id: ' + pid))

        if 'heightMsg' in valueMap:
            errorDetails.add(Label('Height problem: '
                    + valueMap.getString('heightMsg')))

        if 'widthMsg' in valueMap:
            errorDetails.add(Label('Width problem: '
                    + valueMap.getString('widthMsg')))

        emphasisInUi = CheckBox('Emphasize component in UI')

        class PrintLayoutHandler(ClickHandler):

            def onClick(self, event):
                if self.paintable is not None:
                    element2 = self.paintable.getElement()
                    Widget.setStyleName(element2, 'invalidlayout',
                            self.emphasisInUi.getValue())

        emphasisInUi.addClickHandler(PrintLayoutHandler())
        errorDetails.add(emphasisInUi)
        errorNode.add(errorDetails)
        if 'subErrors' in valueMap:
            l = HTML('<em>Expand this node to show problems that may be dependent on this problem.</em>')
            errorDetails.add(l)
            suberrors = valueMap.getJSValueMapArray('subErrors')
            for value in suberrors:
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
            self.getElement().getStyle().setOverflow('hidden')
            self.sinkEvents(Event.ONDBLCLICK)
            self.sinkEvents(Event.MOUSEEVENTS)
            self._panel.setStyleName('v-debug-console-content')
            self._caption.setInnerHTML('Debug window')
            self._caption.getStyle().setHeight(25, 'px')
            self._caption.setTitle(self._help)
            self.show()
            self.setToDefaultSizeAndPos()
            self._actions = HorizontalPanel()
            style = self._actions.getElement().getStyle()
            style.setPosition('absolute')
            style.setBackgroundColor('#666')
            style.setLeft(135, 'px')
            style.setHeight(25, 'px')
            style.setTop(0, 'px')
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

            class ModeHandler(ClickHandler):

                def __init__(self, console):
                    self._console = console

                def onClick(self, event):
                    if self._console._hostedMode.getValue():
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

            self._hostedMode.addClickHandler(ModeHandler(self))
            self._autoScroll.setTitle('Automatically scroll so that new messages are visible')
            self._panel.add(self._actions)
            self._panel.add(HTML('<i>' + self._help + '</i>'))

            class ClearHandler(ClickHandler):

                def __init__(self, console):
                    self._console = console

                def onClick(self, event):
                    width = self._console._panel.getOffsetWidth()
                    height = self._console._panel.getOffsetHeight()
                    self._console._panel = FlowPanel()
                    self._console._panel.setPixelSize(width, height)
                    self._console._panel.setStyleName('v-debug-console-content')
                    self._console._panel.add(self._console._actions)
                    self.setWidget(self._console._panel)

            self._clear.addClickHandler(ClearHandler(self))

            class RestartHandler(ClickHandler):

                def onClick(self, event):
                    queryString = Location.getQueryString()
                    if (queryString is not None
                            and 'restartApplications' in queryString):
                        Location.reload()
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
                        Location.replace(url)

            self._restart.addClickHandler(RestartHandler())

            class ForceHandler(ClickHandler):

                def onClick(self, event):
                    # TODO for each client in appconf force layout
                    # VDebugConsole.this.client.forceLayout();
                    pass

            self._forceLayout.addClickHandler(ForceHandler())

            class AnalyseHandler(ClickHandler):

                def onClick(self, event):
                    runningApplications = ApplicationConfiguration.getRunningApplications()
                    for applicationConnection in runningApplications:
                        applicationConnection.analyzeLayouts()

            self._analyzeLayout.addClickHandler(AnalyseHandler())
            self._analyzeLayout.setTitle('Analyzes currently rendered view and '
                    + 'reports possible common problems in usage of relative sizes.'
                    + 'Will cause server visit/rendering of whole screen and loss of'
                    + ' all non committed variables form client side.')

            class SaveHandler(ClickHandler):

                def __init__(self, console):
                    self._console = console

                def onClick(self, event):
                    pos = self.getAbsoluteLeft() + ',' + self.getAbsoluteTop()
                            + ',' + self.getOffsetWidth() + ','
                            + self.getOffsetHeight() + ','
                            + self._console._autoScroll.getValue()
                    Cookies.setCookie(VDebugConsole_this._POS_COOKIE_NAME, pos)

            self._savePosition.addClickHandler(SaveHandler(self))

            class HighlightHandler(ClickHandler):

                def __init__(self, console):
                    self._console = console

                def onClick(self, event):
                    label = Label('--')
                    self._console.log('<i>Use mouse to select a component or click ESC to exit highlight mode.</i>')
                    self._console._panel.add(label)
                    self._console._highlightModeRegistration = \
                            Event.addNativePreviewHandler(
                                    self._console.HighlightModeHandler(label,
                                                                       self))

            self._highlight.addClickHandler(HighlightHandler(self))

        self.log('Starting Vaadin client side engine. Widgetset: '
                + GWT.getModuleName())
        self.log('Widget set is built on version: '
                + ApplicationConfiguration.VERSION)
        self.logToDebugWindow('<div class=\"v-theme-version v-theme-version-'
                + ApplicationConfiguration.VERSION.replaceAll('\\.', '_')
                + '\">Warning: widgetset version ' + ApplicationConfiguration.VERSION
                + ' does not seem to match theme version </div>', True)


    def setQuietMode(self, quietDebugMode):
        self._quietMode = quietDebugMode


class HighlightModeHandler(NativePreviewHandler):

    def __init__(self, label, console):
        self._label = label
        self._console = console


    def onPreviewNativeEvent(self, event):
        if (event.getTypeInt() == Event.ONKEYDOWN
                and event.getNativeEvent().getKeyCode() == KEY_ESCAPE):
            self._console._highlightModeRegistration.removeHandler()
            VUIDLBrowser.deHiglight()
            return

        if event.getTypeInt() == Event.ONMOUSEMOVE:
            VUIDLBrowser.deHiglight()
            eventTarget = Util.getElementFromPoint(
                    event.getNativeEvent().getClientX(),
                    event.getNativeEvent().getClientY())

            if self.getElement().isOrHasChild(eventTarget):
                return

            for a in ApplicationConfiguration.getRunningApplications():
                paintable = Util.getPaintableForElement(a, a.getView(),
                        eventTarget)

                if paintable is None:
                    paintable = Util.getPaintableForElement(a,
                            RootPanel.get(), eventTarget)

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
            self._console._highlightModeRegistration.removeHandler()
            eventTarget = Util.getElementFromPoint(
                    event.getNativeEvent().getClientX(),
                    event.getNativeEvent().getClientY())

            for a in ApplicationConfiguration.getRunningApplications():
                paintable = Util.getPaintableForElement(a, a.getView(),
                        eventTarget)
                if paintable is None:
                    paintable = Util.getPaintableForElement(a, RootPanel.get(),
                            eventTarget)
                if paintable is not None:
                    a.highlightComponent(paintable)
                    return

        event.cancel()


class DragPreview(EventPreview):

    def __init__(self, console):
        self._console = console

    def onEventPreview(self, event):
        self._console.onBrowserEvent(event)
        return False


class DoSend(ScheduledCommand):

    def __init__(self, console):
        self._console = console

    def execute(self):
        if len(self._console._msgQueue) > 0:
            requestBuilder = RequestBuilder(RequestBuilder.POST,
                    self._console.getRemoteLogUrl())
            # TODO Auto-generated catch block
            try:
                requestData = ''
                for str in self._console._msgQueue:
                    requestData += str
                    requestData += '\n'

                class SendCallback(RequestCallback):

                    def onResponseReceived(self, request, response):
                        pass

                    def onError(self, request, exception):
                        pass

                requestBuilder.sendRequest(requestData, SendCallback())
            except RequestException, e:
                e.printStackTrace()

            self._console._msgQueue.clear()
