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

from pyjamas.ui.FlowPanel import FlowPanel

from pyjamas.ui.SimplePanel import SimplePanel

from muntjac.terminal.gwt.client.v_console import VConsole
from muntjac.terminal.gwt.client.paintable import IPaintable
from muntjac.terminal.gwt.client.container import IContainer
from muntjac.terminal.gwt.client.render_space import RenderSpace
from muntjac.terminal.gwt.client.ui.v_margin_info import VMarginInfo
from muntjac.terminal.gwt.client.style_constants import StyleConstants
from muntjac.terminal.gwt.client.util import Util
from muntjac.terminal.gwt.client.v_caption import VCaption
from muntjac.terminal.gwt.client.browser_info import BrowserInfo

from muntjac.terminal.gwt.client.ui.layout_click_event_handler \
    import LayoutClickEventHandler


class VCssLayout(SimplePanel, IPaintable, IContainer):

    TAGNAME = 'csslayout'
    CLASSNAME = 'v-' + TAGNAME

    class clickEventHandler(LayoutClickEventHandler):

        def getChildComponent(self, element):
            return VCssLayout_this._panel.getComponent(element)

        def registerHandler(self, handler, type):
            return self.addDomHandler(handler, type)


    def __init__(self):
        self._panel = FlowPane()
        self._margin = DOM.createDiv()

        self._hasHeight = None
        self._hasWidth = None
        self._rendering = None

        self._space = None

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

        self.setStyleName(self._margin, self.CLASSNAME + '-'
                + StyleConstants.MARGIN_TOP, margins.hasTop())
        self.setStyleName(self._margin, self.CLASSNAME + '-'
                + StyleConstants.MARGIN_RIGHT, margins.hasRight())
        self.setStyleName(self._margin, self.CLASSNAME + '-'
                + StyleConstants.MARGIN_BOTTOM, margins.hasBottom())
        self.setStyleName(self._margin, self.CLASSNAME + '-'
                + StyleConstants.MARGIN_LEFT, margins.hasLeft())
        self.setStyleName(self._margin, self.CLASSNAME + '-' + 'spacing',
                uidl.hasAttribute('spacing'))
        self._panel.updateFromUIDL(uidl, client)
        self._rendering = False


    def hasChildComponent(self, component):
        return self._panel.hasChildComponent(component)


    def replaceChildComponent(self, oldComponent, newComponent):
        self._panel.replaceChildComponent(oldComponent, newComponent)


    def updateCaption(self, component, uidl):
        self._panel.updateCaption(component, uidl)


    def getAllocatedSpace(self, child):
        if self._space is None:

            class _1_(RenderSpace):

                def getWidth(self):
                    if BrowserInfo.get().isIE():
                        width = self.getOffsetWidth()
                        margins = (VCssLayout_this._margin.getOffsetWidth()
                                - VCssLayout_this._panel.getOffsetWidth())
                        return width - margins
                    else:
                        return VCssLayout_this._panel.getOffsetWidth()

                def getHeight(self):
                    height = self.getOffsetHeight()
                    margins = (VCssLayout_this._margin.getOffsetHeight()
                            - VCssLayout_this._panel.getOffsetHeight())
                    return height - margins

            _1_ = _1_()
            self._space = _1_
        return self._space


    def requestLayout(self, children):
        if self.hasSize():
            return True
        else:
            # Size may have changed
            # TODO: optimize this: cache size if not fixed, handle both width
            # and height separately
            return False


    def hasSize(self):
        return self._hasWidth and self._hasHeight


    @classmethod
    def makeCamelCase(cls, cssProperty):
        # TODO this might be cleaner to implement with regexp
        while '-' in cssProperty:
            indexOf = cssProperty.find('-')
            cssProperty = (cssProperty[:indexOf]
                    + str(cssProperty[indexOf + 1]).upper()
                    + (cssProperty[indexOf + 2:]))

        if 'float' == cssProperty:
            if BrowserInfo.get().isIE():
                return 'styleFloat'
            else:
                return 'cssFloat'

        return cssProperty


class FlowPane(FlowPanel):

    def __init__(self, layout):
        self._layout = layout

        self._widgetToCaption = dict()
        self._client = None
        self._lastIndex = None

        super(FlowPane, self)()
        self.setStyleName(self._layout.CLASSNAME + '-container')


    def updateRelativeSizes(self):
        for w in self.getChildren():
            if isinstance(w, IPaintable):
                self._client.handleComponentRelativeSize(w)


    def updateFromUIDL(self, uidl, client):
        # for later requests
        self._client = client

        oldWidgets = set()
        iterator = self
        while iterator.hasNext():
            oldWidgets.add(iterator.next())

        mapAttribute = None
        if uidl.hasAttribute('css'):
            mapAttribute = uidl.getMapAttribute('css')

        self._lastIndex = 0
        i = uidl.getChildIterator()
        while i.hasNext():
            r = i.next()
            child = client.getPaintable(r)
            widget = child
            if widget.getParent() is self:
                oldWidgets.remove(child)
                vCaption = self._widgetToCaption[child]
                if vCaption is not None:
                    self.addOrMove(vCaption, self._lastIndex)
                    self._lastIndex += 1
                    oldWidgets.remove(vCaption)

            self.addOrMove(widget, self._lastIndex)
            self._lastIndex += 1
            if mapAttribute is not None and r.getId() in mapAttribute:
                css = None
                try:
                    style = widget.getElement().getStyle()
                    css = mapAttribute.getString(r.getId())
                    cssRules = css.split(';')
                    for j in range(len(cssRules)):
                        rule = cssRules[j].split(':')
                        if len(rule) == 0:
                            continue
                        else:
                            style.setProperty(self._layout.makeCamelCase(
                                    rule[0].trim()), rule[1].trim())
                except Exception:
                    VConsole.log('CssLayout encounterd invalid css string: '
                            + css)

            if not r.getBooleanAttribute('cached'):
                child.updateFromUIDL(r, client)

        # loop oldWidgetWrappers that where not re-attached and unregister
        # them
        for w in oldWidgets:
            self.remove(w)
            if isinstance(w, IPaintable):
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
        return Util.getPaintableForElement(self._client, self._layout, element)
