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
from com.vaadin.terminal.gwt.client.VCaption import (VCaption,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.StyleConstants import (StyleConstants,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.VMarginInfo import (VMarginInfo,)
from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
# from com.google.gwt.dom.client.Style import (Style,)
# from com.google.gwt.event.dom.client.DomEvent.Type import (Type,)
# from com.google.gwt.event.shared.EventHandler import (EventHandler,)
# from com.google.gwt.event.shared.HandlerRegistration import (HandlerRegistration,)
# from com.google.gwt.user.client.DOM import (DOM,)
# from com.google.gwt.user.client.Element import (Element,)
# from com.google.gwt.user.client.ui.FlowPanel import (FlowPanel,)
# from com.google.gwt.user.client.ui.SimplePanel import (SimplePanel,)
# from com.google.gwt.user.client.ui.Widget import (Widget,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.HashMap import (HashMap,)
# from java.util.Iterator import (Iterator,)
# from java.util.Set import (Set,)


class VCssLayout(SimplePanel, Paintable, Container):
    TAGNAME = 'csslayout'
    CLASSNAME = 'v-' + TAGNAME
    _panel = FlowPane()
    _margin = DOM.createDiv()



#    private LayoutClickEventHandler clickEventHandler = new LayoutClickEventHandler(
#            this, EventId.LAYOUT_CLICK) {
#
#        @Override
#        protected Paintable getChildComponent(Element element) {
#            return panel.getComponent(element);
#        }
#
#        @Override
#        protected <H extends EventHandler> HandlerRegistration registerHandler(
#                H handler, Type<H> type) {
#            return addDomHandler(handler, type);
#        }
#    };


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

    class FlowPane(FlowPanel):
        _widgetToCaption = dict()
        _client = None

        def __init__(self):
            super(FlowPane, self)()
            self.setStyleName(self.CLASSNAME + '-container')

        def updateRelativeSizes(self):
            for w in self.getChildren():
                if isinstance(w, Paintable):
                    self._client.handleComponentRelativeSize(w)

        def updateFromUIDL(self, uidl, client):
            # for later requests
            self._client = client
            oldWidgets = list()
            _0 = True
            iterator = self
            while True:
                if _0 is True:
                    _0 = False
                if not iterator.hasNext():
                    break
                oldWidgets.add(iterator.next())
            self.clear()
            mapAttribute = None
            if uidl.hasAttribute('css'):
                mapAttribute = uidl.getMapAttribute('css')
            _1 = True
            i = uidl.getChildIterator()
            while True:
                if _1 is True:
                    _1 = False
                if not i.hasNext():
                    break
                r = i.next()
                child = client.getPaintable(r)
                if oldWidgets.contains(child):
                    oldWidgets.remove(child)
                    vCaption = self._widgetToCaption[child]
                    if vCaption is not None:
                        self.add(vCaption)
                        oldWidgets.remove(vCaption)
                self.add(child)
                if mapAttribute is not None and r.getId() in mapAttribute:
                    css = None
                    try:
                        style = child.getElement().getStyle()
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
                                style.setProperty(self.makeCamelCase(rule[0].trim()), rule[1].trim())
                    except Exception, e:
                        VConsole.log('CssLayout encounterd invalid css string: ' + css)
                if not r.getBooleanAttribute('cached'):
                    child.updateFromUIDL(r, client)
            # loop oldWidgetWrappers that where not re-attached and unregister
            # them
            for w in oldWidgets:
                if isinstance(w, Paintable):
                    p = w
                    client.unregisterPaintable(p)
                self._widgetToCaption.remove(w)

        def hasChildComponent(self, component):
            return component.getParent() == self

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
                elif not caption.isAttached():
                    self.insert(caption, self.getWidgetIndex(widget))
                caption.updateCaption(uidl)
            elif caption is not None:
                self.remove(caption)
                self._widgetToCaption.remove(component)

        def getComponent(self, element):
            return Util.getPaintableForElement(self._client, _VCssLayout_this, element)

    _space = None

    def getAllocatedSpace(self, child):
        if self._space is None:

            class _0_(RenderSpace):

                def getWidth(self):
                    if BrowserInfo.get().isIE():
                        width = self.getOffsetWidth()
                        margins = self.margin.getOffsetWidth() - self.panel.getOffsetWidth()
                        return width - margins
                    else:
                        return self.panel.getOffsetWidth()

                def getHeight(self):
                    height = self.getOffsetHeight()
                    margins = self.margin.getOffsetHeight() - self.panel.getOffsetHeight()
                    return height - margins

            _0_ = self._0_(-1, -1)
            self._space = _0_
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
