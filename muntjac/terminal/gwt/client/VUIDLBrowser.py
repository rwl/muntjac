# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.ui.VWindow import (VWindow,)
from com.vaadin.terminal.gwt.client.ui.VView import (VView,)
from com.vaadin.terminal.gwt.client.ApplicationConfiguration import (ApplicationConfiguration,)
from com.vaadin.terminal.gwt.client.UIDL import (UIDL,)
from com.vaadin.terminal.gwt.client.ui.VUnknownComponent import (VUnknownComponent,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.SimpleTree import (SimpleTree,)
from com.vaadin.terminal.gwt.client.ValueMap import (ValueMap,)
# from com.google.gwt.dom.client.Document import (Document,)
# from com.google.gwt.dom.client.Element import (Element,)
# from com.google.gwt.event.dom.client.MouseOutEvent import (MouseOutEvent,)
# from com.google.gwt.event.dom.client.MouseOutHandler import (MouseOutHandler,)
# from java.util.Iterator import (Iterator,)
# from java.util.List import (List,)
# from java.util.Set import (Set,)


class VUIDLBrowser(SimpleTree):
    _HELP = 'Shift click handle to open recursively. Click components to hightlight them on client side. Shift click components to highlight them also on the server side.'
    _conf = None
    _highlightedPid = None

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 2:
            if isinstance(_0[0], UIDL):
                uidl, conf = _0
                self._conf = conf
                root = self.UIDLItem(uidl, conf)
                self.add(root)
            else:
                u, conf = _0
                self._conf = conf
                valueMap = u.getValueMap('meta')
                if 'hl' in valueMap:
                    self._highlightedPid = valueMap.getString('hl')
                keySet = u.getKeySet()
                for key in keySet:
                    if key == 'changes':
                        jsValueMapArray = u.getJSValueMapArray('changes')
                        _0 = True
                        i = 0
                        while True:
                            if _0 is True:
                                _0 = False
                            else:
                                i += 1
                            if not (i < len(jsValueMapArray)):
                                break
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
        else:
            raise ARGERROR(2, 2)

    def UIDLItem(VUIDLBrowser_this, *args, **kwargs):

        class UIDLItem(SimpleTree):
            _uidl = None

            def __init__(self, uidl, conf):
                self.setTitle(VUIDLBrowser_this._HELP)
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

                class _0_(MouseOutHandler):

                    def onMouseOut(self, event):
                        VUIDLBrowser_this.deHiglight()

                _0_ = _0_()
                self.addDomHandler(_0_, MouseOutEvent.getType())

            def getNodeName(self, uidl, conf, name):
                widgetClassByDecodedTag = conf.getWidgetClassByEncodedTag(name)
                if widgetClassByDecodedTag == VUnknownComponent:
                    return conf.getUnknownServerClassNameByEncodedTagName(name) + '(NO CLIENT IMPLEMENTATION FOUND)'
                elif widgetClassByDecodedTag == VView and uidl.hasAttribute('sub'):
                    return 'com.vaadin.terminal.gwt.ui.VWindow'
                else:
                    return widgetClassByDecodedTag.getName()

            def open(self, recursive):
                if (
                    self.getWidgetCount() == 1 and self.getWidget(0).getElement().getInnerText() == 'LOADING'
                ):
                    self.dir()
                super(UIDLItem, self).open(recursive)

            def select(self, event):
                runningApplications = ApplicationConfiguration.getRunningApplications()
                # TODO this does not work properly with multiple application on
                # same
                # host page
                for applicationConnection in runningApplications:
                    paintable = applicationConnection.getPaintable(self._uidl.getId())
                    VUIDLBrowser_this.highlight(paintable)
                    if event is not None and event.getNativeEvent().getShiftKey():
                        applicationConnection.highlightComponent(paintable)
                super(UIDLItem, self).select(event)

            def dir(self):
                self.remove(0)
                nodeName = self._uidl.getTag()
                # NOP
                try:
                    int(nodeName)
                    nodeName = self.getNodeName(self._uidl, VUIDLBrowser_this._conf, nodeName)
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
                            tmp = SimpleTree('variables')
                        tmp.addItem(name + '=' + value)
                    if tmp is not None:
                        self.add(tmp)
                except Exception, e:
                    pass # astStmt: [Stmt([]), None]
                i = self._uidl.getChildIterator()
                while i.hasNext():
                    child = i.next()
                    try:
                        c = child
                        childItem = VUIDLBrowser_this.UIDLItem(c, VUIDLBrowser_this._conf)
                        self.add(childItem)
                    except Exception, e:
                        self.addItem(str(child))
                if (
                    VUIDLBrowser_this._highlightedPid is not None and VUIDLBrowser_this._highlightedPid == self._uidl.getId()
                ):
                    self.getElement().getStyle().setBackgroundColor('#fdd')

                    class _1_(ScheduledCommand):

                        def execute(self):
                            self.getElement().scrollIntoView()

                    _1_ = _1_()
                    Scheduler.get().scheduleDeferred(_1_)

        return UIDLItem(*args, **kwargs)

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
            style = cls.highlight.getStyle()
            style.setTop(w.getAbsoluteTop(), Unit.PX)
            style.setLeft(w.getAbsoluteLeft(), Unit.PX)
            style.setWidth(w.getOffsetWidth(), Unit.PX)
            style.setHeight(w.getOffsetHeight(), Unit.PX)
            RootPanel.getBodyElement().appendChild(cls.v_highlight)

    @classmethod
    def deHiglight(cls):
        if cls.highlight.getParentElement() is not None:
            cls.highlight.getParentElement().removeChild(cls.v_highlight)
