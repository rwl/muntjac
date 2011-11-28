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

from pyjamas.ui import RootPanel

from muntjac.terminal.gwt.client.application_configuration \
    import ApplicationConfiguration

from muntjac.terminal.gwt.client.ui.v_window import VWindow
from muntjac.terminal.gwt.client.ui.v_view import VView
from muntjac.terminal.gwt.client.ui.v_unknown_component import VUnknownComponent
from muntjac.terminal.gwt.client.uidl import UIDL
from muntjac.terminal.gwt.client.browser_info import BrowserInfo
from muntjac.terminal.gwt.client.simple_tree import SimpleTree


class VUIDLBrowser(SimpleTree):

    _HELP = 'Shift click handle to open recursively. Click components to hightlight them on client side. Shift click components to highlight them also on the server side.'

    v_highlight = DOM.createDivElement()
    style = v_highlight.getStyle()
    style.setPosition('absolute')
    style.setZIndex(VWindow.Z_INDEX + 1000)
    style.setBackgroundColor('red')
    style.setOpacity(0.2)
    if BrowserInfo.get().isIE():
        style.setProperty('filter', 'alpha(opacity=20)')

    def __init__(self, u, conf):
        self._conf = None
        self._highlightedPid = None

        if isinstance(u, UIDL):
            self._conf = conf
            root = self.UIDLItem(u, conf)
            self.add(root)
        else:
            self._conf = conf
            valueMap = u.getValueMap('meta')
            if 'hl' in valueMap:
                self._highlightedPid = valueMap.getString('hl')
            keySet = u.getKeySet()
            for key in keySet:
                if key == 'changes':
                    jsValueMapArray = u.getJSValueMapArray('changes')
                    for i in range(len(jsValueMapArray)):
                        uidl = jsValueMapArray.get(i)
                        change = self.UIDLItem(uidl, conf)
                        change.setTitle('change ' + i)
                        self.add(change)
                elif key == 'meta':
                    pass
                else:
                    # TODO consider pretty printing other request data
                    # addItem(key + " : " + u.getAsString(key));
                    pass

            self.open(self._highlightedPid is not None)
            self.setTitle(self._HELP)


    @classmethod
    def highlight(cls, paintable):
        w = paintable
        if w is not None:
            style = cls.highlight.getStyle()
            style.setTop(w.getAbsoluteTop(), 'px')
            style.setLeft(w.getAbsoluteLeft(), 'px')
            style.setWidth(w.getOffsetWidth(), 'px')
            style.setHeight(w.getOffsetHeight(), 'px')
            RootPanel.getBodyElement().appendChild(cls.v_highlight)

    @classmethod
    def deHiglight(cls):
        if cls.highlight.getParentElement() is not None:
            cls.highlight.getParentElement().removeChild(cls.v_highlight)


class UIDLItem(SimpleTree):

    def __init__(self, uidl, conf, browser):
        self._browser = browser
        self.setTitle(self._browser._HELP)
        self._uidl = uidl
        try:
            name = uidl.getTag()
            try:
                int(name)
                name = self.getNodeName(uidl, conf, name)
            except Exception:
                pass  # NOP
            self.setText(name)
            self.addItem('LOADING')
        except Exception:
            self.setText(str(uidl))

        class MouseHandler(MouseOutHandler):

            def __init__(self, browser):
                self._browser = browser

            def onMouseOut(self, event):
                self._browser.deHiglight()

        self.addDomHandler(MouseHandler(self._browser), MouseOutEvent.getType())


    def getNodeName(self, uidl, conf, name):
        widgetClassByDecodedTag = conf.getWidgetClassByEncodedTag(name)
        if widgetClassByDecodedTag == VUnknownComponent:
            return (conf.getUnknownServerClassNameByEncodedTagName(name)
                    + '(NO CLIENT IMPLEMENTATION FOUND)')
        elif widgetClassByDecodedTag == VView and uidl.hasAttribute('sub'):
            return 'com.vaadin.terminal.gwt.ui.VWindow'
        else:
            return widgetClassByDecodedTag.getName()


    def open(self, recursive):
        if (self.getWidgetCount() == 1
                and self.getWidget(0).getElement().getInnerText() == 'LOADING'):
            self.dir()
        super(UIDLItem, self).open(recursive)


    def select(self, event):
        runningApplications = ApplicationConfiguration.getRunningApplications()
        # TODO this does not work properly with multiple application on
        # same host page
        for applicationConnection in runningApplications:
            paintable = applicationConnection.getPaintable(self._uidl.getId())
            self.highlight(paintable)
            if event is not None and event.getNativeEvent().getShiftKey():
                applicationConnection.highlightComponent(paintable)
        super(UIDLItem, self).select(event)


    def dir(self):
        self.remove(0)

        nodeName = self._uidl.getTag()
        try:
            int(nodeName)
            nodeName = self.getNodeName(self._uidl, self._conf, nodeName)
        except Exception:
            pass  # NOP

        attributeNames = self._uidl.getAttributeNames()
        for name in attributeNames:
            if self._uidl.isMapAttribute(name):
                try:
                    _map = self._uidl.getMapAttribute(name)
                    keyArray = _map.getKeyArray()
                    nodeName += ' ' + name + '=' + '{'
                    for i in range(len(keyArray)):
                        nodeName += (keyArray.get(i) + ':'
                                + _map.getAsString(keyArray.get(i)) + ',')
                    nodeName += '}'
                except Exception:
                    pass
            else:
                value = self._uidl.getAttribute(name)
                nodeName += ' ' + name + '=' + value

        self.setText(nodeName)

        try:
            tmp = None
            variableNames = self._uidl.getVariableNames()
            for name in variableNames:
                value = ''
                try:
                    value = self._uidl.getVariable(name)
                except Exception:
                    try:
                        stringArrayAttribute = \
                                self._uidl.getStringArrayAttribute(name)
                        value = str(stringArrayAttribute)
                    except Exception:
                        try:
                            intVal = self._uidl.getIntVariable(name)
                            value = str(intVal)
                        except Exception:
                            value = 'unknown'
                if tmp is None:
                    tmp = SimpleTree('variables')
                tmp.addItem(name + '=' + value)
            if tmp is not None:
                self.add(tmp)
        except Exception:
            pass  # Ignored, no variables

        i = self._uidl.getChildIterator()
        while i.hasNext():
            child = i.next()
            try:
                c = child
                childItem = UIDLItem(c, self._browser._conf,self._browser)
                self.add(childItem)

            except Exception:
                self.addItem(str(child))
        if (self._browser._highlightedPid is not None
                    and self._browser._highlightedPid == self._uidl.getId()):
            self.getElement().getStyle().setBackgroundColor('#fdd')

            class DirCommand(ScheduledCommand):

                def execute(self):
                    self.getElement().scrollIntoView()

            Scheduler.get().scheduleDeferred(DirCommand())
