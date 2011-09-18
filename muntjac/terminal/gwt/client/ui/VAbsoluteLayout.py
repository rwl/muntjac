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
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
from com.vaadin.terminal.gwt.client.RenderSpace import (RenderSpace,)
# from com.google.gwt.dom.client.DivElement import (DivElement,)
# from com.google.gwt.dom.client.Document import (Document,)
# from com.google.gwt.dom.client.Style import (Style,)
# from com.google.gwt.event.dom.client.DomEvent.Type import (Type,)
# from com.google.gwt.event.shared.EventHandler import (EventHandler,)
# from com.google.gwt.event.shared.HandlerRegistration import (HandlerRegistration,)
# from com.google.gwt.user.client.DOM import (DOM,)
# from com.google.gwt.user.client.Element import (Element,)
# from com.google.gwt.user.client.ui.ComplexPanel import (ComplexPanel,)
# from com.google.gwt.user.client.ui.SimplePanel import (SimplePanel,)
# from com.google.gwt.user.client.ui.Widget import (Widget,)
# from java.util.HashMap import (HashMap,)
# from java.util.HashSet import (HashSet,)
# from java.util.Iterator import (Iterator,)
# from java.util.Map import (Map,)
# from java.util.Map.Entry import (Entry,)
# from java.util.Set import (Set,)


class VAbsoluteLayout(ComplexPanel, Container):
    # Tag name for widget creation
    TAGNAME = 'absolutelayout'
    # Class name, prefix in styling
    CLASSNAME = 'v-absolutelayout'
    _marginElement = None
    canvas = DOM.createDiv()
    # private int excessPixelsHorizontal;
    # private int excessPixelsVertical;
    _previousStyleName = None
    _pidToComponentWrappper = dict()
    client = None
    _rendering = None

#    private LayoutClickEventHandler clickEventHandler = new LayoutClickEventHandler(
#            this, EventId.LAYOUT_CLICK) {
#
#        @Override
#        protected Paintable getChildComponent(Element element) {
#            return getComponent(element);
#        }
#
#        @Override
#        protected <H extends EventHandler> HandlerRegistration registerHandler(
#                H handler, Type<H> type) {
#            return addDomHandler(handler, type);
#        }
#    };

    def __init__(self):
        self.setElement(Document.get().createDivElement())
        self.setStyleName(self.CLASSNAME)
        self._marginElement = Document.get().createDivElement()
        self.canvas.getStyle().setProperty('position', 'relative')
        self.canvas.getStyle().setProperty('overflow', 'hidden')
        self._marginElement.appendChild(self.canvas)
        self.getElement().appendChild(self._marginElement)

    def getAllocatedSpace(self, child):
        # TODO needs some special handling for components with only on edge
        # horizontally or vertically defined
        wrapper = child.getParent()
        if wrapper.left is not None and wrapper.right is not None:
            w = wrapper.getOffsetWidth()
        elif wrapper.right is not None:
            # left == null
            # available width == right edge == offsetleft + width
            w = wrapper.getOffsetWidth() + wrapper.getElement().getOffsetLeft()
        else:
            # left != null && right == null || left == null &&
            # right == null
            # available width == canvas width - offset left
            w = self.canvas.getOffsetWidth() - wrapper.getElement().getOffsetLeft()
        if wrapper.top is not None and wrapper.bottom is not None:
            h = wrapper.getOffsetHeight()
        elif wrapper.bottom is not None:
            # top not defined, available space 0... bottom of wrapper
            h = wrapper.getElement().getOffsetTop() + wrapper.getOffsetHeight()
        else:
            # top defined or both undefined, available space == canvas - top
            h = self.canvas.getOffsetHeight() - wrapper.getElement().getOffsetTop()
        return RenderSpace(w, h)

    def hasChildComponent(self, component):
        _0 = True
        iterator = self._pidToComponentWrappper.entrySet()
        while True:
            if _0 is True:
                _0 = False
            if not iterator.hasNext():
                break
            if iterator.next().getValue().paintable == component:
                return True
        return False

    def replaceChildComponent(self, oldComponent, newComponent):
        for wrapper in self.getChildren():
            w = wrapper
            if w.getWidget() == oldComponent:
                w.setWidget(newComponent)
                return

    def requestLayout(self, children):
        # component inside an absolute panel never affects parent nor the
        # layout
        return True

    def updateCaption(self, component, uidl):
        parent2 = component.getParent()
        parent2.updateCaption(uidl)

    def updateFromUIDL(self, uidl, client):
        self._rendering = True
        self.client = client
        # TODO margin handling
        if client.updateComponent(self, uidl, True):
            self._rendering = False
            return
        self.clickEventHandler.handleEventHandlerRegistration(client)
        unrenderedPids = set(self._pidToComponentWrappper.keys())
        _0 = True
        childIterator = uidl.getChildIterator()
        while True:
            if _0 is True:
                _0 = False
            if not childIterator.hasNext():
                break
            cc = childIterator.next()
            if cc.getTag() == 'cc':
                componentUIDL = cc.getChildUIDL(0)
                unrenderedPids.remove(componentUIDL.getId())
                self.getWrapper(client, componentUIDL).updateFromUIDL(cc)
        for pid in unrenderedPids:
            absoluteWrapper = self._pidToComponentWrappper[pid]
            self._pidToComponentWrappper.remove(pid)
            absoluteWrapper.destroy()
        self._rendering = False

    def getWrapper(self, client, componentUIDL):
        wrapper = self._pidToComponentWrappper[componentUIDL.getId()]
        if wrapper is None:
            wrapper = self.AbsoluteWrapper(client.getPaintable(componentUIDL))
            self._pidToComponentWrappper.put(componentUIDL.getId(), wrapper)
            self.add(wrapper)
        return wrapper

    def add(self, child):
        super(VAbsoluteLayout, self).add(child, self.canvas)

    def setStyleName(self, style):
        super(VAbsoluteLayout, self).setStyleName(style)
        if (
            (self._previousStyleName is None) or (not (self._previousStyleName == style))
        ):
            # excessPixelsHorizontal = -1;
            # excessPixelsVertical = -1;
            pass

    def setWidth(self, width):
        super(VAbsoluteLayout, self).setWidth(width)
        # TODO do this so that canvas gets the sized properly (the area
        # inside marginals)
        self.canvas.getStyle().setProperty('width', width)
        if not self._rendering:
            if BrowserInfo.get().isIE6():
                self.relayoutWrappersForIe6()
            self.relayoutRelativeChildren()

    def relayoutRelativeChildren(self):
        for widget in self.getChildren():
            if isinstance(widget, AbsoluteWrapper):
                w = widget
                self.client.handleComponentRelativeSize(w.getWidget())
                w.updateCaptionPosition()

    def setHeight(self, height):
        super(VAbsoluteLayout, self).setHeight(height)
        # TODO do this so that canvas gets the sized properly (the area
        # inside marginals)
        self.canvas.getStyle().setProperty('height', height)
        if not self._rendering:
            if BrowserInfo.get().isIE6():
                self.relayoutWrappersForIe6()
            self.relayoutRelativeChildren()

    def relayoutWrappersForIe6(self):
        for wrapper in self.getChildren():
            if isinstance(wrapper, AbsoluteWrapper):
                wrapper.ie6Layout()

    class AbsoluteWrapper(SimplePanel):
        _css = None
        _left = None
        _top = None
        _right = None
        _bottom = None
        _zIndex = None
        _paintable = None
        _caption = None

        def __init__(self, paintable):
            self._paintable = paintable
            self.setStyleName(self.CLASSNAME + '-wrapper')

        def updateCaption(self, uidl):
            captionIsNeeded = VCaption.isNeeded(uidl)
            if captionIsNeeded:
                if self._caption is None:
                    self._caption = VCaption(self._paintable, self.client)
                    _VAbsoluteLayout_this.add(self._caption)
                self._caption.updateCaption(uidl)
                self.updateCaptionPosition()
            elif self._caption is not None:
                self._caption.removeFromParent()
                self._caption = None

        def setWidget(self, w):
            # this fixes #5457 (Widget implementation can change on-the-fly)
            self._paintable = w
            super(AbsoluteWrapper, self).setWidget(w)

        def destroy(self):
            if self._caption is not None:
                self._caption.removeFromParent()
            self.client.unregisterPaintable(self._paintable)
            self.removeFromParent()

        def updateFromUIDL(self, componentUIDL):
            self.setPosition(componentUIDL.getStringAttribute('css'))
            if self.getWidget() != self._paintable:
                self.setWidget(self._paintable)
            childUIDL = componentUIDL.getChildUIDL(0)
            self._paintable.updateFromUIDL(childUIDL, self.client)
            if childUIDL.hasAttribute('cached'):
                # child may need relative size adjustment if wrapper details
                # have changed this could be optimized (check if wrapper size
                # has changed)
                self.client.handleComponentRelativeSize(self._paintable)

        def setPosition(self, stringAttribute):
            if (self._css is None) or (not (self._css == stringAttribute)):
                self._css = stringAttribute
                self._top = self._right = self._bottom = self._left = self._zIndex = None
                if not (self._css == ''):
                    properties = self._css.split(';')
                    _0 = True
                    i = 0
                    while True:
                        if _0 is True:
                            _0 = False
                        else:
                            i += 1
                        if not (i < len(properties)):
                            break
                        keyValue = properties[i].split(':')
                        if keyValue[0] == 'left':
                            self._left = keyValue[1]
                        elif keyValue[0] == 'top':
                            self._top = keyValue[1]
                        elif keyValue[0] == 'right':
                            self._right = keyValue[1]
                        elif keyValue[0] == 'bottom':
                            self._bottom = keyValue[1]
                        elif keyValue[0] == 'z-index':
                            self._zIndex = keyValue[1]
                # ensure ne values
                style = self.getElement().getStyle()
                # IE8 dies when nulling zIndex, even in IE7 mode. All other css
                # properties (and even in older IE's) accept null values just
                # fine. Assign empty string instead of null.

                if self._zIndex is not None:
                    style.setProperty('zIndex', self._zIndex)
                else:
                    style.setProperty('zIndex', '')
                style.setProperty('top', self._top)
                style.setProperty('left', self._left)
                style.setProperty('right', self._right)
                style.setProperty('bottom', self._bottom)
                if BrowserInfo.get().isIE6():
                    self.ie6Layout()
            self.updateCaptionPosition()

        def updateCaptionPosition(self):
            if self._caption is not None:
                style = self._caption.getElement().getStyle()
                style.setProperty('position', 'absolute')
                style.setPropertyPx('left', self.getElement().getOffsetLeft())
                style.setPropertyPx('top', self.getElement().getOffsetTop() - self._caption.getHeight())

        def ie6Layout(self):
            # special handling for IE6 is needed, it does not support
            # setting both left/right or top/bottom
            style = self.getElement().getStyle()
            if self._bottom is not None and self._top is not None:
                # define height for wrapper to simulate bottom property
                bottompixels = self.measureForIE6(self._bottom, True)
                VConsole.log('ALB' + bottompixels)
                height = self.canvas.getOffsetHeight() - bottompixels - self.getElement().getOffsetTop()
                VConsole.log('ALB' + height)
                if height < 0:
                    height = 0
                style.setPropertyPx('height', height)
            else:
                # reset possibly existing value
                style.setProperty('height', '')
            if self._left is not None and self._right is not None:
                # define width for wrapper to simulate right property
                rightPixels = self.measureForIE6(self._right, False)
                VConsole.log('ALR' + rightPixels)
                width = self.canvas.getOffsetWidth() - rightPixels - self.getElement().getOffsetLeft()
                VConsole.log('ALR' + width)
                if width < 0:
                    width = 0
                style.setPropertyPx('width', width)
            else:
                # reset possibly existing value
                style.setProperty('width', '')

    _measureElement = None

    def measureForIE6(self, cssLength, vertical):
        if self._measureElement is None:
            self._measureElement = DOM.createDiv()
            self._measureElement.getStyle().setProperty('position', 'absolute')
            self.canvas.appendChild(self._measureElement)
        if vertical:
            self._measureElement.getStyle().setProperty('height', cssLength)
            return self._measureElement.getOffsetHeight()
        else:
            self._measureElement.getStyle().setProperty('width', cssLength)
            return self._measureElement.getOffsetWidth()

    def getComponent(self, element):
        """Returns the deepest nested child component which contains "element". The
        child component is also returned if "element" is part of its caption.

        @param element
                   An element that is a nested sub element of the root element in
                   this layout
        @return The Paintable which the element is a part of. Null if the element
                belongs to the layout and not to a child.
        """
        return Util.getPaintableForElement(self.client, self, element)
