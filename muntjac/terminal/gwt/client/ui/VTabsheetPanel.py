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

from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.TouchScrollDelegate import (TouchScrollDelegate,)


class VTabsheetPanel(ComplexPanel):
    """A panel that displays all of its child widgets in a 'deck', where only one
    can be visible at a time. It is used by
    {@link com.vaadin.terminal.gwt.client.ui.VTabsheet}.

    This class has the same basic functionality as the GWT DeckPanel
    {@link com.google.gwt.user.client.ui.DeckPanel}, with the exception that it
    doesn't manipulate the child widgets' width and height attributes.
    """
    _visibleWidget = None
    _touchScrollDelegate = None

    def __init__(self):
        """Creates an empty tabsheet panel."""
        self.setElement(self.DOM.createDiv())
        self.sinkEvents(self.Event.TOUCHEVENTS)

        class _0_(TouchStartHandler):

            def onTouchStart(self, event):
                # All container elements needs to be scrollable by one finger.
                # Update the scrollable element list of touch delegate on each
                # touch start.

                childNodes = self.getElement().getChildNodes()
                elements = [None] * childNodes.getLength()
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(elements)):
                        break
                    elements[i] = childNodes.getItem(i)
                self.getTouchScrollDelegate().setElements(elements)
                self.getTouchScrollDelegate().onTouchStart(event)

        _0_ = self._0_()
        self.addDomHandler(_0_, self.TouchStartEvent.getType())

    def getTouchScrollDelegate(self):
        if self._touchScrollDelegate is None:
            self._touchScrollDelegate = TouchScrollDelegate()
        return self._touchScrollDelegate

    def add(self, w):
        """Adds the specified widget to the deck.

        @param w
                   the widget to be added
        """
        el = self.createContainerElement()
        self.DOM.appendChild(self.getElement(), el)
        super(VTabsheetPanel, self).add(w, el)

    def createContainerElement(self):
        el = self.DOM.createDiv()
        self.DOM.setStyleAttribute(el, 'position', 'absolute')
        self.DOM.setStyleAttribute(el, 'overflow', 'auto')
        self.hide(el)
        return el

    def getVisibleWidget(self):
        """Gets the index of the currently-visible widget.

        @return the visible widget's index
        """
        return self.getWidgetIndex(self._visibleWidget)

    def insert(self, w, beforeIndex):
        """Inserts a widget before the specified index.

        @param w
                   the widget to be inserted
        @param beforeIndex
                   the index before which it will be inserted
        @throws IndexOutOfBoundsException
                    if <code>beforeIndex</code> is out of range
        """
        el = self.createContainerElement()
        self.DOM.insertChild(self.getElement(), el, beforeIndex)
        super(VTabsheetPanel, self).insert(w, el, beforeIndex, False)

    def remove(self, w):
        child = w.getElement()
        parent = None
        if child is not None:
            parent = self.DOM.getParent(child)
        removed = super(VTabsheetPanel, self).remove(w)
        if removed:
            if self._visibleWidget == w:
                self._visibleWidget = None
            if parent is not None:
                self.DOM.removeChild(self.getElement(), parent)
        return removed

    def showWidget(self, index):
        """Shows the widget at the specified index. This causes the currently-
        visible widget to be hidden.

        @param index
                   the index of the widget to be shown
        """
        self.checkIndexBoundsForAccess(index)
        newVisible = self.getWidget(index)
        if self._visibleWidget != newVisible:
            if self._visibleWidget is not None:
                self.hide(self.DOM.getParent(self._visibleWidget.getElement()))
            self._visibleWidget = newVisible
            self.unHide(self.DOM.getParent(self._visibleWidget.getElement()))

    def hide(self, e):
        self.DOM.setStyleAttribute(e, 'visibility', 'hidden')
        self.DOM.setStyleAttribute(e, 'top', '-100000px')
        self.DOM.setStyleAttribute(e, 'left', '-100000px')

    def unHide(self, e):
        self.DOM.setStyleAttribute(e, 'top', '0px')
        self.DOM.setStyleAttribute(e, 'left', '0px')
        self.DOM.setStyleAttribute(e, 'visibility', '')

    def fixVisibleTabSize(self, width, height, minWidth):
        if self._visibleWidget is None:
            return
        dynamicHeight = False
        if height < 0:
            height = self._visibleWidget.getOffsetHeight()
            dynamicHeight = True
        if width < 0:
            width = self._visibleWidget.getOffsetWidth()
        if width < minWidth:
            width = minWidth
        wrapperDiv = self._visibleWidget.getElement().getParentElement()
        # width first
        self.getElement().getStyle().setPropertyPx('width', width)
        wrapperDiv.getStyle().setPropertyPx('width', width)
        if dynamicHeight:
            # height of widget might have changed due wrapping
            height = self._visibleWidget.getOffsetHeight()
        # v-tabsheet-tabsheetpanel height
        self.getElement().getStyle().setPropertyPx('height', height)
        # widget wrapper height
        wrapperDiv.getStyle().setPropertyPx('height', height)
        self.runWebkitOverflowAutoFix()

    def runWebkitOverflowAutoFix(self):
        if self._visibleWidget is not None:
            Util.runWebkitOverflowAutoFix(self.DOM.getParent(self._visibleWidget.getElement()))

    def replaceComponent(self, oldComponent, newComponent):
        isVisible = self._visibleWidget == oldComponent
        widgetIndex = self.getWidgetIndex(oldComponent)
        self.remove(oldComponent)
        self.insert(newComponent, widgetIndex)
        if isVisible:
            self.showWidget(widgetIndex)
