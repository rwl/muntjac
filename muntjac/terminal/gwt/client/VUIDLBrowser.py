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

from com.google.gwt.dom.client.Style import (Unit,)
from com.vaadin.terminal.gwt.client.ApplicationConfiguration import (ApplicationConfiguration,)
from com.vaadin.terminal.gwt.client.ui.VView import (VView,)
from com.vaadin.terminal.gwt.client.ui.VUnknownComponent import (VUnknownComponent,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.VWindow import (VWindow,)
# from com.google.gwt.dom.client.Document import (Document,)
# from com.google.gwt.dom.client.Element import (Element,)
# from com.google.gwt.dom.client.Style import (Style,)
# from com.google.gwt.dom.client.Style.Position import (Position,)
# from com.google.gwt.dom.client.Style.Unit import (Unit,)
# from com.google.gwt.event.dom.client.MouseOutEvent import (MouseOutEvent,)
# from com.google.gwt.event.dom.client.MouseOutHandler import (MouseOutHandler,)
# from com.google.gwt.event.logical.shared.OpenEvent import (OpenEvent,)
# from com.google.gwt.event.logical.shared.OpenHandler import (OpenHandler,)
# from com.google.gwt.event.logical.shared.SelectionEvent import (SelectionEvent,)
# from com.google.gwt.event.logical.shared.SelectionHandler import (SelectionHandler,)
# from com.google.gwt.user.client.ui.RootPanel import (RootPanel,)
# from java.util.Iterator import (Iterator,)
# from java.util.List import (List,)
# from java.util.Set import (Set,)


class VUIDLBrowser(Tree, MouseOutHandler):
    _uidl = None
    _conf = None

    def __init__(self, uidl, conf):
        self._conf = conf
        self._uidl = uidl
        self.DOM.setStyleAttribute(self.getElement(), 'position', '')
        root = self.UIDLItem(self._uidl, conf)
        self.addItem(root)

        class _0_(OpenHandler):

            def onOpen(self, event):
                item = event.getTarget()
                if item.getChildCount() == 1 and item.getChild(0).getText() == 'LOADING':
                    item.dir()

        _0_ = self._0_()
        self.addOpenHandler(_0_)

        class _1_(SelectionHandler):

            def onSelection(self, event):
                item = event.getSelectedItem()
                if not isinstance(item, UIDLItem):
                    # e.g. "variables" and its sub items are not UIDLItems
                    return
                selectedItem = item
                runningApplications = ApplicationConfiguration.getRunningApplications()
                # TODO this does not work properly with multiple application on
                # same
                # host page
                for applicationConnection in runningApplications:
                    paintable = applicationConnection.getPaintable(selectedItem.uidl.getId())
                    self.highlight(paintable)

        _1_ = self._1_()
        self.addSelectionHandler(_1_)
        self.addMouseOutHandler(_VUIDLBrowser_this)

    def isKeyboardNavigationEnabled(self, currentItem):
        return False

    class UIDLItem(TreeItem):
        _uidl = None

        def __init__(self, uidl, conf):
            self._uidl = uidl
            try:
                name = uidl.getTag()
                # NOP
                try:
                    int(name)
                    name = self.getNodeName(uidl, conf, name)
                except Exception, e:
                    pass # astStmt: [Stmt([]), None]
                self.setText(name)
                self.addItem('LOADING')
            except Exception, e:
                self.setText(str(uidl))

        def getNodeName(self, uidl, conf, name):
            widgetClassByDecodedTag = conf.getWidgetClassByEncodedTag(name)
            if widgetClassByDecodedTag == VUnknownComponent:
                return conf.getUnknownServerClassNameByEncodedTagName(name) + '(NO CLIENT IMPLEMENTATION FOUND)'
            elif widgetClassByDecodedTag == VView and uidl.hasAttribute('sub'):
                return 'com.vaadin.terminal.gwt.ui.VWindow'
            else:
                return widgetClassByDecodedTag.getName()

        def dir(self):
            temp = self.getChild(0)
            self.removeItem(temp)
            nodeName = self._uidl.getTag()
            # NOP
            try:
                int(nodeName)
                nodeName = self.getNodeName(self._uidl, self.conf, nodeName)
            except Exception, e:
                pass # astStmt: [Stmt([]), None]
            attributeNames = self._uidl.getAttributeNames()
            for name in attributeNames:
                if self._uidl.isMapAttribute(name):
                    try:
                        map = self._uidl.getMapAttribute(name)
                        keyArray = map.getKeyArray()
                        nodeName += ' ' + name + '=' + '{'
                        _0 = True
                        i = 0
                        while True:
                            if _0 is True:
                                _0 = False
                            else:
                                i += 1
                            if not (i < len(keyArray)):
                                break
                            nodeName += keyArray.get(i) + ':' + map.getAsString(keyArray.get(i)) + ','
                        nodeName += '}'
                    except Exception, e:
                        pass # astStmt: [Stmt([]), None]
                else:
                    value = self._uidl.getAttribute(name)
                    nodeName += ' ' + name + '=' + value
            self.setText(nodeName)
            # Ignored, no variables
            try:
                tmp = None
                variableNames = self._uidl.getVariableNames()
                for name in variableNames:
                    value = ''
                    try:
                        value = self._uidl.getVariable(name)
                    except Exception, e:
                        try:
                            stringArrayAttribute = self._uidl.getStringArrayAttribute(name)
                            value = str(stringArrayAttribute)
                        except Exception, e2:
                            try:
                                intVal = self._uidl.getIntVariable(name)
                                value = String.valueOf.valueOf(intVal)
                            except Exception, e3:
                                value = 'unknown'
                    if tmp is None:
                        tmp = self.TreeItem('variables')
                    tmp.addItem(name + '=' + value)
                if tmp is not None:
                    self.addItem(tmp)
            except Exception, e:
                pass # astStmt: [Stmt([]), None]
            i = self._uidl.getChildIterator()
            while i.hasNext():
                child = i.next()
                try:
                    c = child
                    childItem = self.UIDLItem(c, self.conf)
                    self.addItem(childItem)
                except Exception, e:
                    self.addItem(str(child))

    v_highlight = Document.get().createDivElement()
    style = v_highlight.getStyle()
    style.setPosition(Position.ABSOLUTE)
    style.setZIndex(VWindow.Z_INDEX + 1000)
    style.setBackgroundColor('red')
    style.setOpacity(0.2)
    if BrowserInfo.get().isIE():
        style.setProperty('filter', 'alpha(opacity=20)')

    @classmethod
    def highlight(cls, paintable):
        w = paintable
        if w is not None:
            style = cls.v_highlight.getStyle()
            style.setTop(w.getAbsoluteTop(), Unit.PX)
            style.setLeft(w.getAbsoluteLeft(), Unit.PX)
            style.setWidth(w.getOffsetWidth(), Unit.PX)
            style.setHeight(w.getOffsetHeight(), Unit.PX)
            RootPanel.getBodyElement().appendChild(cls.v_highlight)

    @classmethod
    def deHiglight(cls):
        if cls.v_highlight.getParentElement() is not None:
            cls.v_highlight.getParentElement().removeChild(cls.v_highlight)

    def onMouseOut(self, event):
        self.deHiglight()
