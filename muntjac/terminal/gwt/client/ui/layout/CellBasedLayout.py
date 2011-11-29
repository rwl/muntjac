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

from __pyjamas__ import (POSTDEC,)
from com.vaadin.terminal.gwt.client.Container import (Container,)
from com.vaadin.terminal.gwt.client.ui.VMarginInfo import (VMarginInfo,)
from com.vaadin.terminal.gwt.client.ui.layout.Margins import (Margins,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
# from com.google.gwt.dom.client.Node import (Node,)
# from com.google.gwt.dom.client.NodeList import (NodeList,)
# from com.google.gwt.dom.client.Style import (Style,)
# from com.google.gwt.user.client.ui.ComplexPanel import (ComplexPanel,)
# from java.util.HashMap import (HashMap,)
# from java.util.Iterator import (Iterator,)
# from java.util.Map import (Map,)


class CellBasedLayout(ComplexPanel, Container):
    widgetToComponentContainer = dict()
    client = None
    root = None
    ORIENTATION_VERTICAL = 0
    ORIENTATION_HORIZONTAL = 1
    activeMargins = Margins(0, 0, 0, 0)
    activeMarginsInfo = VMarginInfo(-1)
    spacingEnabled = False
    spacingFromCSS = Spacing(12, 12)
    activeSpacing = Spacing(0, 0)
    _dynamicWidth = None
    _dynamicHeight = None
    _clearElement = Document.get().createDivElement()
    _lastStyleName = ''
    _marginsNeedsRecalculation = False
    STYLENAME_SPACING = ''
    STYLENAME_MARGIN_TOP = ''
    STYLENAME_MARGIN_RIGHT = ''
    STYLENAME_MARGIN_BOTTOM = ''
    STYLENAME_MARGIN_LEFT = ''

    class Spacing(object):
        hSpacing = 0
        vSpacing = 0

        def __init__(self, hSpacing, vSpacing):
            self.hSpacing = hSpacing
            self.vSpacing = vSpacing

        def toString(self):
            return 'Spacing [hSpacing=' + self.hSpacing + ',vSpacing=' + self.vSpacing + ']'

    def __init__(self):
        super(CellBasedLayout, self)()
        self.setElement(Document.get().createDivElement())
        self.getElement().getStyle().setProperty('overflow', 'hidden')
        if BrowserInfo.get().isIE():
            self.getElement().getStyle().setProperty('position', 'relative')
            self.getElement().getStyle().setProperty('zoom', '1')
        self.root = Document.get().createDivElement()
        self.root.getStyle().setProperty('overflow', 'hidden')
        if BrowserInfo.get().isIE():
            self.root.getStyle().setProperty('position', 'relative')
        self.getElement().appendChild(self.root)
        style = self._clearElement.getStyle()
        style.setProperty('width', '0px')
        style.setProperty('height', '0px')
        style.setProperty('clear', 'both')
        style.setProperty('overflow', 'hidden')
        self.root.appendChild(self._clearElement)

    def hasChildComponent(self, component):
        return component in self.widgetToComponentContainer

    def updateFromUIDL(self, uidl, client):
        self.client = client
        # Only non-cached UIDL:s can introduce changes
        if uidl.getBooleanAttribute('cached'):
            return
        # Margin and spacind detection depends on classNames and must be set
        # before setting size. Here just update the details from UIDL and from
        # overridden setStyleName run actual margin detections.

        self.updateMarginAndSpacingInfo(uidl)
        # This call should be made first. Ensure correct implementation, handle
        # size etc.

        if client.updateComponent(self, uidl, True):
            return
        self.handleDynamicDimensions(uidl)

    def setStyleName(self, styleName):
        super(CellBasedLayout, self).setStyleName(styleName)
        if (
            (self.isAttached() and self._marginsNeedsRecalculation) or (not (self._lastStyleName == styleName))
        ):
            self.measureMarginsAndSpacing()
            self._lastStyleName = styleName
            self._marginsNeedsRecalculation = False

    def setWidth(self, width):
        super(CellBasedLayout, self).setWidth(width)
        # Ensure the the dynamic width stays up to date even if size is altered
        # only on client side.

        if (width is None) or (width == ''):
            self._dynamicWidth = True
        else:
            self._dynamicWidth = False

    def handleDynamicDimensions(self, uidl):
        w = uidl.getStringAttribute('width') if uidl.hasAttribute('width') else ''
        h = uidl.getStringAttribute('height') if uidl.hasAttribute('height') else ''
        if w == '':
            self._dynamicWidth = True
        else:
            self._dynamicWidth = False
        if h == '':
            self._dynamicHeight = True
        else:
            self._dynamicHeight = False

    def setHeight(self, height):
        super(CellBasedLayout, self).setHeight(height)
        # Ensure the the dynamic height stays up to date even if size is
        # altered only on client side.

        if (height is None) or (height == ''):
            self._dynamicHeight = True
        else:
            self._dynamicHeight = False

    def addOrMoveChild(self, childComponent, position):
        if childComponent.getParent() is self:
            if self.getWidgetIndex(childComponent) != position:
                # Detach from old position child.
                childComponent.removeFromParent()
                # Logical attach.
                self.getChildren().insert(childComponent, position)
                self.root.insertBefore(childComponent.getElement(), self.root.getChildNodes().getItem(position))
                self.adopt(childComponent)
        else:
            self.widgetToComponentContainer.put(childComponent.getWidget(), childComponent)
            # Logical attach.
            self.getChildren().insert(childComponent, position)
            # avoid inserts (they are slower than appends)
            insert = True
            if len(self.widgetToComponentContainer) == position:
                insert = False
            if insert:
                self.root.insertBefore(childComponent.getElement(), self.root.getChildNodes().getItem(position))
            else:
                self.root.insertBefore(childComponent.getElement(), self._clearElement)
            # Adopt.
            self.adopt(childComponent)

    def getComponentContainer(self, child):
        return self.widgetToComponentContainer[child]

    def isDynamicWidth(self):
        return self._dynamicWidth

    def isDynamicHeight(self):
        return self._dynamicHeight

    def updateMarginAndSpacingInfo(self, uidl):
        if not uidl.hasAttribute('invisible'):
            bitMask = uidl.getIntAttribute('margins')
            if self.activeMarginsInfo.getBitMask() != bitMask:
                self.activeMarginsInfo = VMarginInfo(bitMask)
                self._marginsNeedsRecalculation = True
            spacing = uidl.getBooleanAttribute('spacing')
            if spacing != self.spacingEnabled:
                self._marginsNeedsRecalculation = True
                self.spacingEnabled = spacing

    _measurement = None
    _measurement2 = None
    _measurement3 = None
    _helper = None
    _helper = Document.get().createDivElement()
    _helper.setInnerHTML('<div style=\"position:absolute;top:0;left:0;height:0;visibility:hidden;overflow:hidden;\">' + '<div style=\"width:0;height:0;visibility:hidden;overflow:hidden;\">' + '</div></div>' + '<div style=\"position:absolute;height:0;overflow:hidden;\"></div>')
    childNodes = _helper.getChildNodes()
    _measurement = childNodes.getItem(0)
    _measurement2 = _measurement.getFirstChildElement()
    _measurement3 = childNodes.getItem(1)

    def measureMarginsAndSpacing(self):
        if not self.isAttached():
            return False
        # Measure spacing (actually CSS padding)
        self._measurement3.setClassName(self.STYLENAME_SPACING + ('-on' if self.spacingEnabled else '-off'))
        sn = self.getStylePrimaryName() + '-margin'
        if self.activeMarginsInfo.hasTop():
            sn += ' ' + self.STYLENAME_MARGIN_TOP
        if self.activeMarginsInfo.hasBottom():
            sn += ' ' + self.STYLENAME_MARGIN_BOTTOM
        if self.activeMarginsInfo.hasLeft():
            sn += ' ' + self.STYLENAME_MARGIN_LEFT
        if self.activeMarginsInfo.hasRight():
            sn += ' ' + self.STYLENAME_MARGIN_RIGHT
        # Measure top and left margins (actually CSS padding)
        self._measurement.setClassName(sn)
        self.root.appendChild(self._helper)
        self.activeSpacing.vSpacing = self._measurement3.getOffsetHeight()
        self.activeSpacing.hSpacing = self._measurement3.getOffsetWidth()
        self.activeMargins.setMarginTop(self._measurement2.getOffsetTop())
        self.activeMargins.setMarginLeft(self._measurement2.getOffsetLeft())
        self.activeMargins.setMarginRight(self._measurement.getOffsetWidth() - self.activeMargins.getMarginLeft())
        self.activeMargins.setMarginBottom(self._measurement.getOffsetHeight() - self.activeMargins.getMarginTop())
        # ApplicationConnection.getConsole().log("Margins: " + activeMargins);
        # ApplicationConnection.getConsole().log("Spacing: " + activeSpacing);
        # Util.alert("Margins: " + activeMargins);
        self.root.removeChild(self._helper)
        # apply margin
        style = self.root.getStyle()
        style.setPropertyPx('marginLeft', self.activeMargins.getMarginLeft())
        style.setPropertyPx('marginRight', self.activeMargins.getMarginRight())
        style.setPropertyPx('marginTop', self.activeMargins.getMarginTop())
        style.setPropertyPx('marginBottom', self.activeMargins.getMarginBottom())
        return True

    def getFirstChildComponentContainer(self):
        size = len(self.getChildren())
        if size < 1:
            return None
        return self.getChildren().get(0)

    def removeChildrenAfter(self, pos):
        # Remove all children after position "pos" but leave the clear element
        # in place
        toRemove = len(self.getChildren()) - pos
        while POSTDEC(globals(), locals(), 'toRemove') > 0:
            # flag to not if widget has been moved and rendered elsewhere
            relocated = False
            child = self.getChildren().get(pos)
            widget = child.getWidget()
            if widget is None:
                # a rare case where child component has been relocated and
                # rendered elsewhere
                # clean widgetToComponentContainer map by iterating the correct
                # mapping
                iterator = self.widgetToComponentContainer.keys()
                while iterator.hasNext():
                    key = iterator.next()
                    if self.widgetToComponentContainer[key] == child:
                        widget = key
                        relocated = True
                        break
                if widget is None:
                    raise self.NullPointerException()
            # ChildComponentContainer remove =
            self.widgetToComponentContainer.remove(widget)
            self.remove(child)
            if not relocated:
                p = widget
                self.client.unregisterPaintable(p)

    def replaceChildComponent(self, oldComponent, newComponent):
        componentContainer = self.widgetToComponentContainer.remove(oldComponent)
        if componentContainer is None:
            return
        componentContainer.setWidget(newComponent)
        self.client.unregisterPaintable(oldComponent)
        self.widgetToComponentContainer.put(newComponent, componentContainer)
