# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (POSTINC,)
from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.Container import (Container,)
from com.vaadin.terminal.gwt.client.RenderSpace import (RenderSpace,)
from com.vaadin.terminal.gwt.client.ui.VMarginInfo import (VMarginInfo,)
from com.vaadin.terminal.gwt.client.StyleConstants import (StyleConstants,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.VCaption import (VCaption,)
from com.vaadin.terminal.gwt.client.ui.LayoutClickEventHandler import (LayoutClickEventHandler,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
# from java.util.Collection import (Collection,)
# from java.util.HashMap import (HashMap,)
# from java.util.HashSet import (HashSet,)
# from java.util.Iterator import (Iterator,)
# from java.util.Set import (Set,)


class VCssLayout(SimplePanel, Paintable, Container):
    TAGNAME = 'csslayout'
    CLASSNAME = 'v-' + TAGNAME
    _panel = FlowPane()
    _margin = DOM.createDiv()

    class clickEventHandler(LayoutClickEventHandler):

        def getChildComponent(self, element):
            return VCssLayout_this._panel.getComponent(element)

        def registerHandler(self, handler, type):
            return self.addDomHandler(handler, type)

    _hasHeight = None
    _hasWidth = None
    _rendering = None

    def __init__(self):
        super(VCssLayout, self)()
        self.getElement().appendChild(self._margin)
        self.setStyleName(self.CLASSNAME)
        self._margin.setClassName(self.CLASSNAME + '-margin')
        self.setWidget(self._panel)

    def getContainerElement(self):
        return self._margin

    def setWidth(self, width):
        super(VCssLayout, self).setWidth(width)
        # panel.setWidth(width);
        self._hasWidth = width is not None and not (width == '')
        if not self._rendering:
            self._panel.updateRelativeSizes()

    def setHeight(self, height):
        super(VCssLayout, self).setHeight(height)
        # panel.setHeight(height);
        self._hasHeight = height is not None and not (height == '')
        if not self._rendering:
            self._panel.updateRelativeSizes()

    def updateFromUIDL(self, uidl, client):
        self._rendering = True
        if client.updateComponent(self, uidl, True):
            self._rendering = False
            return
        self.clickEventHandler.handleEventHandlerRegistration(client)
        margins = VMarginInfo(uidl.getIntAttribute('margins'))
        self.setStyleName(self._margin, self.CLASSNAME + '-' + StyleConstants.MARGIN_TOP, margins.hasTop())
        self.setStyleName(self._margin, self.CLASSNAME + '-' + StyleConstants.MARGIN_RIGHT, margins.hasRight())
        self.setStyleName(self._margin, self.CLASSNAME + '-' + StyleConstants.MARGIN_BOTTOM, margins.hasBottom())
        self.setStyleName(self._margin, self.CLASSNAME + '-' + StyleConstants.MARGIN_LEFT, margins.hasLeft())
        self.setStyleName(self._margin, self.CLASSNAME + '-' + 'spacing', uidl.hasAttribute('spacing'))
        self._panel.updateFromUIDL(uidl, client)
        self._rendering = False

    def hasChildComponent(self, component):
        return self._panel.hasChildComponent(component)

    def replaceChildComponent(self, oldComponent, newComponent):
        self._panel.replaceChildComponent(oldComponent, newComponent)

    def updateCaption(self, component, uidl):
        self._panel.updateCaption(component, uidl)

    def FlowPane(VCssLayout_this, *args, **kwargs):

        class FlowPane(FlowPanel):
            _widgetToCaption = dict()
            _client = None
            _lastIndex = None

            def __init__(self):
                super(FlowPane, self)()
                self.setStyleName(VCssLayout_this.CLASSNAME + '-container')

            def updateRelativeSizes(self):
                for w in self.getChildren():
                    if isinstance(w, Paintable):
                        self._client.handleComponentRelativeSize(w)

            def updateFromUIDL(self, uidl, client):
                # for later requests
                self._client = client
                oldWidgets = set()
                _0 = True
                iterator = self
                while True:
                    if _0 is True:
                        _0 = False
                    if not iterator.hasNext():
                        break
                    oldWidgets.add(iterator.next())
                mapAttribute = None
                if uidl.hasAttribute('css'):
                    mapAttribute = uidl.getMapAttribute('css')
                self._lastIndex = 0
                _1 = True
                i = uidl.getChildIterator()
                while True:
                    if _1 is True:
                        _1 = False
                    if not i.hasNext():
                        break
                    r = i.next()
                    child = client.getPaintable(r)
                    widget = child
                    if widget.getParent() is self:
                        oldWidgets.remove(child)
                        vCaption = self._widgetToCaption[child]
                        if vCaption is not None:
                            self.addOrMove(vCaption, POSTINC(globals(), locals(), 'self._lastIndex'))
                            oldWidgets.remove(vCaption)
                    self.addOrMove(widget, POSTINC(globals(), locals(), 'self._lastIndex'))
                    if mapAttribute is not None and r.getId() in mapAttribute:
                        css = None
                        try:
                            style = widget.getElement().getStyle()
                            css = mapAttribute.getString(r.getId())
                            cssRules = css.split(';')
                            _2 = True
                            j = 0
                            while True:
                                if _2 is True:
                                    _2 = False
                                else:
                                    j += 1
                                if not (j < len(cssRules)):
                                    break
                                rule = cssRules[j].split(':')
                                if len(rule) == 0:
                                    continue
                                else:
                                    style.setProperty(VCssLayout_this.makeCamelCase(rule[0].trim()), rule[1].trim())
                        except Exception, e:
                            VConsole.log('CssLayout encounterd invalid css string: ' + css)
                    if not r.getBooleanAttribute('cached'):
                        child.updateFromUIDL(r, client)
                # loop oldWidgetWrappers that where not re-attached and unregister
                # them
                for w in oldWidgets:
                    self.remove(w)
                    if isinstance(w, Paintable):
                        p = w
                        client.unregisterPaintable(p)
                    vCaption = self._widgetToCaption.remove(w)
                    if vCaption is not None:
                        self.remove(vCaption)

            def addOrMove(self, child, index):
                if child.getParent() is self:
                    currentIndex = self.getWidgetIndex(child)
                    if index == currentIndex:
                        return
                self.insert(child, index)

            def hasChildComponent(self, component):
                return component.getParent() is self

            def replaceChildComponent(self, oldComponent, newComponent):
                caption = self._widgetToCaption[oldComponent]
                if caption is not None:
                    self.remove(caption)
                    self._widgetToCaption.remove(oldComponent)
                index = self.getWidgetIndex(oldComponent)
                if index >= 0:
                    self.remove(oldComponent)
                    self.insert(newComponent, index)

            def updateCaption(self, component, uidl):
                caption = self._widgetToCaption[component]
                if VCaption.isNeeded(uidl):
                    widget = component
                    if caption is None:
                        caption = VCaption(component, self._client)
                        self._widgetToCaption.put(widget, caption)
                        self.insert(caption, self.getWidgetIndex(widget))
                        self._lastIndex += 1
                    elif not caption.isAttached():
                        self.insert(caption, self.getWidgetIndex(widget))
                        self._lastIndex += 1
                    caption.updateCaption(uidl)
                elif caption is not None:
                    self.remove(caption)
                    self._widgetToCaption.remove(component)

            def getComponent(self, element):
                return Util.getPaintableForElement(self._client, VCssLayout_this, element)

        return FlowPane(*args, **kwargs)

    _space = None

    def getAllocatedSpace(self, child):
        if self._space is None:

            class _1_(RenderSpace):

                def getWidth(self):
                    if BrowserInfo.get().isIE():
                        width = self.getOffsetWidth()
                        margins = VCssLayout_this._margin.getOffsetWidth() - VCssLayout_this._panel.getOffsetWidth()
                        return width - margins
                    else:
                        return VCssLayout_this._panel.getOffsetWidth()

                def getHeight(self):
                    height = self.getOffsetHeight()
                    margins = VCssLayout_this._margin.getOffsetHeight() - VCssLayout_this._panel.getOffsetHeight()
                    return height - margins

            _1_ = _1_()
            self._space = _1_
        return self._space

    def requestLayout(self, children):
        if self.hasSize():
            return True
        else:
            # Size may have changed
            # TODO optimize this: cache size if not fixed, handle both width
            # and height separately
            return False

    def hasSize(self):
        return self._hasWidth and self._hasHeight

    @classmethod
    def makeCamelCase(cls, cssProperty):
        # TODO this might be cleaner to implement with regexp
        while cssProperty.contains('-'):
            indexOf = cssProperty.find('-')
            cssProperty = (cssProperty[:indexOf]) + String.valueOf.valueOf(cssProperty[indexOf + 1]).toUpperCase() + (cssProperty[indexOf + 2:])
        if 'float' == cssProperty:
            if BrowserInfo.get().isIE():
                return 'styleFloat'
            else:
                return 'cssFloat'
        return cssProperty
