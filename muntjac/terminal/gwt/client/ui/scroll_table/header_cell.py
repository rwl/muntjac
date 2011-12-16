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

from pyjamas.ui import Event
from pyjamas.ui import RootPanel
from pyjamas.ui.Widget import Widget

from muntjac.terminal.gwt.client.browser_info import BrowserInfo
from muntjac.terminal.gwt.client.util import Util


class HeaderCell(Widget):

    def __init__(self, colId, headerText, st):
        self._st = st

        self._td = DOM.createTD()
        self._captionContainer = DOM.createDiv()
        self._sortIndicator = DOM.createDiv()
        self._colResizeWidget = DOM.createDiv()
        self._floatingCopyOfHeaderCell = None
        self._sortable = False
        self._cid = None
        self._dragging = None
        self._dragStartX = None
        self._colIndex = None
        self._originalWidth = None
        self._isResizing = None
        self._headerX = None
        self._moved = None
        self._closestSlot = None
        self._width = -1
        self._naturalWidth = -1
        self._align = st.ALIGN_LEFT
        self._definedWidth = False
        self._expandRatio = 0
        self._sorted = None

        self._cid = colId

        DOM.setElemAttribute(self._colResizeWidget, 'className',
                self._st.CLASSNAME + '-resizer')

        self.setText(headerText)

        DOM.appendChild(self._td, self._colResizeWidget)

        DOM.setElemAttribute(self._sortIndicator, 'className',
                self._st.CLASSNAME + '-sort-indicator')

        DOM.appendChild(self._td, self._sortIndicator)

        DOM.setElemAttribute(self._captionContainer, 'className',
                self._st.CLASSNAME + '-caption-container')

        # ensure no clipping initially (problem on column additions)
        DOM.setStyleAttribute(self._captionContainer, 'overflow', 'visible')

        DOM.appendChild(self._td, self._captionContainer)

        DOM.sinkEvents(self._td, Event.MOUSEEVENTS | Event.TOUCHEVENTS)

        self.setElement(self._td)

        self.setAlign(self._st.ALIGN_LEFT)


    def setSortable(self, b):
        self._sortable = b


    def resizeCaptionContainer(self, rightSpacing):
        """Makes room for the sorting indicator in case the column that the
        header cell belongs to is sorted. This is done by resizing the width
        of the caption container element by the correct amount
        """
        if (BrowserInfo.get().isIE6()
                or self._td.getClassName().contains('-asc')
                or self._td.getClassName().contains('-desc')):
            # Room for the sort indicator is made by subtracting the styled
            # margin and width of the resizer from the width of the caption
            # container.
            captionContainerWidth = (self._width
                    - self._sortIndicator.getOffsetWidth()
                    - self._colResizeWidget.getOffsetWidth()
                    - rightSpacing)
            self._captionContainer.getStyle().setPropertyPx('width',
                    captionContainerWidth)
        else:
            # Set the caption container element as wide as possible when
            # the sorting indicator is not visible.
            self._captionContainer.getStyle().setPropertyPx('width',
                    self._width - rightSpacing)

        # Apply/Remove spacing if defined
        if rightSpacing > 0:
            self._colResizeWidget.getStyle().setMarginLeft(rightSpacing, 'px')#Unit.PX)
        else:
            self._colResizeWidget.getStyle().clearMarginLeft()


    def setNaturalMinimumColumnWidth(self, w):
        self._naturalWidth = w


    def disableAutoWidthCalculation(self):
        self._definedWidth = True
        self._expandRatio = 0


    def setWidth(self, w, ensureDefinedWidth):
        if ensureDefinedWidth:
            self._definedWidth = True
            # on column resize expand ratio becomes zero
            self._expandRatio = 0

        if self._width == -1:
            # go to default mode, clip content if necessary
            DOM.setStyleAttribute(self._captionContainer, 'overflow', '')

        self._width = w
        if w == -1:
            DOM.setStyleAttribute(self._captionContainer, 'width', '')
            self.setWidth('')
        else:
            self._st.tHead.resizeCaptionContainer(self)
            # if we already have tBody, set the header width properly, if
            # not defer it. IE will fail with complex float in table header
            # unless TD width is not explicitly set.
            if self._st._scrollBody is not None:
                tdWidth = self._width + self._st._scrollBody.getCellExtraWidth()
                self.setWidth(tdWidth + 'px')
            else:
                class _8_(Command):

                    def __init__(self, st, hc):
                        self._st = st
                        self._hc = hc

                    def execute(self):
                        tdWidth = self._hc._width + self._st._scrollBody.getCellExtraWidth()
                        self._hc.setWidth(tdWidth + 'px')

                _8_ = _8_()
                Scheduler.get().scheduleDeferred(_8_)


    def setUndefinedWidth(self):
        self._definedWidth = False
        self.setWidth(-1, False)


    def isDefinedWidth(self):
        """Detects if width is fixed by developer on server side or resized to
        current width by user.

        @return: true if defined, false if "natural" width
        """
        return self._definedWidth and self._width >= 0


    def getWidth(self):
        return self._width


    def setText(self, headerText):
        DOM.setInnerHTML(self._captionContainer, headerText)


    def getColKey(self):
        return self._cid


    def setSorted(self, sorted_):
        self._sorted = sorted_
        if sorted_:
            if self._st._sortAscending:
                self.setStyleName(self._st.CLASSNAME + '-header-cell-asc')
            else:
                self.setStyleName(self._st.CLASSNAME + '-header-cell-desc')
        else:
            self.setStyleName(self._st.CLASSNAME + '-header-cell')


    def onBrowserEvent(self, event):
        """Handle column reordering."""
        if self._st._enabled and event is not None:
            if (self._isResizing
                    or (event.getEventTarget() == self._colResizeWidget)):
                if (self._dragging and (event.getTypeInt() == Event.ONMOUSEUP)
                        or (event.getTypeInt() == Event.ONTOUCHEND)):
                    # Handle releasing column header on spacer #5318
                    self.handleCaptionEvent(event)
                else:
                    self.onResizeEvent(event)
            else:
                # Ensure focus before handling caption event. Otherwise
                # variables changed from caption event may be before
                # variables from other components that fire variables when
                # they lose focus.
                if ((event.getTypeInt() == Event.ONMOUSEDOWN)
                        or (event.getTypeInt() == Event.ONTOUCHSTART)):
                    self._st._scrollBodyPanel.setFocus(True)
                self.handleCaptionEvent(event)
                event.stopPropagation()
                event.preventDefault()


    def createFloatingCopy(self):
        self._floatingCopyOfHeaderCell = DOM.createDiv()
        DOM.setInnerHTML(self._floatingCopyOfHeaderCell,
                DOM.getInnerHTML(self._td))
        self._floatingCopyOfHeaderCell = DOM.getChild(
                self._floatingCopyOfHeaderCell, 2)
        DOM.setElemAttribute(self._floatingCopyOfHeaderCell, 'className',
                self._st.CLASSNAME + '-header-drag')
        # otherwise might wrap or be cut if narrow column
        DOM.setStyleAttribute(self._floatingCopyOfHeaderCell, 'width', 'auto')
        self.updateFloatingCopysPosition(DOM.getAbsoluteLeft(self._td),
                DOM.getAbsoluteTop(self._td))
        DOM.appendChild(RootPanel.get().getElement(),
                self._floatingCopyOfHeaderCell)


    def updateFloatingCopysPosition(self, x, y):
        x -= DOM.getIntElemAttribute(self._floatingCopyOfHeaderCell,
                'offsetWidth') / 2
        DOM.setStyleAttribute(self._floatingCopyOfHeaderCell, 'left', x + 'px')
        if y > 0:
            DOM.setStyleAttribute(self._floatingCopyOfHeaderCell, 'top',
                    y + 7 + 'px')


    def hideFloatingCopy(self):
        DOM.removeChild(RootPanel.get().getElement(),
                self._floatingCopyOfHeaderCell)
        self._floatingCopyOfHeaderCell = None


    def fireHeaderClickedEvent(self, event):
        """Fires a header click event after the user has clicked a column
        header cell

        @param event:
                   The click event
        """
        if (self._st.client.hasEventListeners(self._st,
                self._st.HEADER_CLICK_EVENT_ID)):
            details = MouseEventDetails(event)
            self._st.client.updateVariable(self._st.paintableId,
                    'headerClickEvent', str(details), False)
            self._st.client.updateVariable(self._st.paintableId,
                    'headerClickCID', self._cid, True)


    def handleCaptionEvent(self, event):
        etype = DOM.eventGetType(event)
        if etype == Event.ONTOUCHSTART:
            pass
        elif etype == Event.ONMOUSEDOWN:
            if self._st._columnReordering:
                if event.getTypeInt() == Event.ONTOUCHSTART:
                    # prevent using this event in e.g. scrolling
                    event.stopPropagation()
                self._dragging = True
                self._moved = False
                self._colIndex = self._st.getColIndexByKey(self._cid)
                DOM.setCapture(self.getElement())
                self._headerX = self._st.tHead.getAbsoluteLeft()
                event.preventDefault()
                # prevent selecting text &&
                # generated touch events

        elif etype == Event.ONMOUSEUP:
            pass
        elif etype == Event.ONTOUCHEND:
            pass
        elif etype == Event.ONTOUCHCANCEL:
            if self._st._columnReordering:
                self._dragging = False
                DOM.releaseCapture(self.getElement())
                if self._moved:
                    self.hideFloatingCopy()
                    self._st.tHead.removeSlotFocus()
                    if (self._closestSlot != self._colIndex
                            and self._closestSlot != self._colIndex + 1):
                        if self._closestSlot > self._colIndex:
                            self._st.reOrderColumn(self._cid, self._closestSlot - 1)
                        else:
                            self._st.reOrderColumn(self._cid, self._closestSlot)

                if Util.isTouchEvent(event):
                    # Prevent using in e.g. scrolling and prevent generated
                    # events.
                    event.preventDefault()
                    event.stopPropagation()
            if not self._moved:
                # mouse event was a click to header -> sort column
                if self._sortable:
                    if self._st._sortColumn == self._cid:
                        # just toggle order
                        self._st.client.updateVariable(self._st.paintableId, 'sortascending', not self._st._sortAscending, False)
                    else:
                        # set table sorted by this column
                        self._st.client.updateVariable(self._st.paintableId, 'sortcolumn', self._cid, False)
                    # get also cache columns at the same request
                    self._st._scrollBodyPanel.setScrollPosition(0)
                    self._st._firstvisible = 0
                    self._st._rowRequestHandler.setReqFirstRow(0)
                    self._st._rowRequestHandler.setReqRows((2 * self._st._pageLength * self._st._cache_rate) + self._st._pageLength)
                    self._st._rowRequestHandler.deferRowFetch()
                    # some validation +
                    # defer 250ms
                    self._st._rowRequestHandler.cancel()
                    # instead of waiting
                    self._st._rowRequestHandler.run()
                    # run immediately
                self.fireHeaderClickedEvent(event)
                if Util.isTouchEvent(event):
                    # Prevent using in e.g. scrolling and prevent generated
                    # events.
                    event.preventDefault()
                    event.stopPropagation()

        elif etype == Event.ONTOUCHMOVE:
            pass
        elif etype == Event.ONMOUSEMOVE:
            if self._dragging:
                if event.getTypeInt() == Event.ONTOUCHMOVE:
                    # prevent using this event in e.g. scrolling
                    event.stopPropagation()
                if not self._moved:
                    self.createFloatingCopy()
                    self._moved = True
                clientX = Util.getTouchOrMouseClientX(event)
                x = clientX + self._st.tHead.hTableWrapper.getScrollLeft()
                slotX = self._headerX
                self._closestSlot = self._colIndex
                closestDistance = -1
                start = 0
                if self._st.showRowHeaders:
                    start += 1
                visibleCellCount = self._st.tHead.getVisibleCellCount()
                for i in range(start, visibleCellCount + 1):
                    if i > 0:
                        colKey = self._st.getColKeyByIndex(i - 1)
                        slotX += self._st.getColWidth(colKey)

                    dist = self.Math.abs(x - slotX)
                    if (closestDistance == -1) or (dist < closestDistance):
                        closestDistance = dist
                        self._closestSlot = i

                self._st.tHead.focusSlot(self._closestSlot)

                self.updateFloatingCopysPosition(clientX, -1)


    def onResizeEvent(self, event):
        etype = DOM.eventGetType(event)
        if etype == Event.ONMOUSEDOWN:
            self._isResizing = True
            DOM.setCapture(self.getElement())
            self._dragStartX = DOM.eventGetClientX(event)
            self._colIndex = self._st.getColIndexByKey(self._cid)
            self._originalWidth = self.getWidth()
            DOM.eventPreventDefault(event)
        elif etype == Event.ONMOUSEUP:
            self._isResizing = False
            DOM.releaseCapture(self.getElement())
            self._st.tHead.disableAutoColumnWidthCalculation(self)
            # Ensure last header cell is taking into account possible
            # column selector
            lastCell = self._st.tHead.getHeaderCell(
                    self._st.tHead.getVisibleCellCount() - 1)
            self._st.tHead.resizeCaptionContainer(lastCell)
            self._st.triggerLazyColumnAdjustment(True)
            self._st.fireColumnResizeEvent(self._cid, self._originalWidth,
                    self._st.getColWidth(self._cid))
        elif etype == Event.ONMOUSEMOVE:
            if self._isResizing:
                deltaX = DOM.eventGetClientX(event) - self._dragStartX
                if deltaX == 0:
                    return
                self._st.tHead.disableAutoColumnWidthCalculation(self)
                newWidth = self._originalWidth + deltaX
                if newWidth < self.getMinWidth():
                    newWidth = self.getMinWidth()
                self._st.setColWidth(self._colIndex, newWidth, True)
                self._st.triggerLazyColumnAdjustment(False)
                self._st.forceRealignColumnHeaders()


    def getMinWidth(self):
        cellExtraWidth = 0
        if self._st._scrollBody is not None:
            cellExtraWidth += self._st._scrollBody.getCellExtraWidth()
        return cellExtraWidth + self._sortIndicator.getOffsetWidth()


    def getCaption(self):
        return DOM.getInnerText(self._captionContainer)


    def isEnabled(self):
        return self.getParent() is not None


    def setAlign(self, c):
        ALIGN_PREFIX = self._st.CLASSNAME + '-caption-container-align-'
        if self._align != c:
            self._captionContainer.removeClassName(ALIGN_PREFIX + 'center')
            self._captionContainer.removeClassName(ALIGN_PREFIX + 'right')
            self._captionContainer.removeClassName(ALIGN_PREFIX + 'left')

            if c == self._st.ALIGN_CENTER:
                self._captionContainer.addClassName(ALIGN_PREFIX + 'center')
            elif c == self._st.ALIGN_RIGHT:
                self._captionContainer.addClassName(ALIGN_PREFIX + 'right')
            else:
                self._captionContainer.addClassName(ALIGN_PREFIX + 'left')

        self._align = c


    def getAlign(self):
        return self._align


    def getNaturalColumnWidth(self, columnIndex):
        """Detects the natural minimum width for the column of this header
        cell. If column is resized by user or the width is defined by server
        the actual width is returned. Else the natural min width is returned.

        @param columnIndex:
                   column index hint, if -1 (unknown) it will be detected
        """
        if self.isDefinedWidth():
            return self._width
        else:
            if self._naturalWidth < 0:
                # This is recently revealed column. Try to detect a proper
                # value (greater of header and data
                # cols)
                hw = (self._captionContainer.getOffsetWidth()
                        + self._st._scrollBody.getCellExtraWidth())
                if BrowserInfo.get().isGecko() or BrowserInfo.get().isIE7():
                    hw += self._sortIndicator.getOffsetWidth()

                if columnIndex < 0:
                    columnIndex = 0
                    _0 = True
                    it = self._st.tHead
                    while it.hasNext():
                        if it.next() is self:
                            break
                        columnIndex += 1

                cw = self._st._scrollBody.getColWidth(columnIndex)
                self._naturalWidth = hw if hw > cw else cw

            return self._naturalWidth


    def setExpandRatio(self, floatAttribute):
        if floatAttribute != self._expandRatio:
            self._st.triggerLazyColumnAdjustment(False)
        self._expandRatio = floatAttribute


    def getExpandRatio(self):
        return self._expandRatio


    def isSorted(self):
        return self._sorted


class RowHeadersHeaderCell(HeaderCell):
    """HeaderCell that is header cell for row headers.

    Reordering disabled and clicking on it resets sorting.
    """

    def __init__(self, st):
        super(RowHeadersHeaderCell, self)(st._ROW_HEADER_COLUMN_KEY, '')
        self.setStyleName(st.CLASSNAME + '-header-cell-rowheader')


    def handleCaptionEvent(self, event):
        # NOP: RowHeaders cannot be reordered
        # TODO: It'd be nice to reset sorting here
        pass
