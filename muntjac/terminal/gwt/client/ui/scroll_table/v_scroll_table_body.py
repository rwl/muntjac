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
from pyjamas.ui.Panel import Panel

from muntjac.terminal.gwt.client.util import Util
from muntjac.terminal.gwt.client.browser_info import BrowserInfo

class VScrollTableBody(Panel):
    """This Panel can only contain VScrollTableRow type of widgets. This
    "simulates" very large table, keeping spacers which take room of
    unrendered rows.
    """

    DEFAULT_ROW_HEIGHT = 24

    def __init__(self, st):
        self._st = st

        self._rowHeight = -1
        self._renderedRows = list()

        # Due some optimizations row height measuring is deferred and initial
        # set of rows is rendered detached. Flag set on when table body has
        # been attached in dom and rowheight has been measured.
        self._tBodyMeasurementsDone = False
        self._preSpacer = DOM.createDiv()
        self._postSpacer = DOM.createDiv()
        self._container = DOM.createDiv()
        self._tBodyElement = Document.get().createTBodyElement()
        self._table = DOM.createTable()
        self._firstRendered = None
        self._lastRendered = None
        self._aligns = None

        self._cellExtraWidth = -1

        self.constructDOM()
        self.setElement(self._container)


    def getRowByRowIndex(self, indexInTable):
        internalIndex = indexInTable - self._firstRendered
        if internalIndex >= 0 and internalIndex < len(self._renderedRows):
            return self._renderedRows.get(internalIndex)
        else:
            return None


    def getRequiredHeight(self):
        """@return the height of scrollable body, subpixels ceiled."""
        return self._preSpacer.getOffsetHeight() + self._postSpacer.getOffsetHeight() + Util.getRequiredHeight(self._table)


    def constructDOM(self):
        DOM.setElemAttribute(self._table, 'className',
                self._st.CLASSNAME + '-table')

        if BrowserInfo.get().isIE():
            self._table.setPropertyInt('cellSpacing', 0)

        DOM.setElemAttribute(self._preSpacer, 'className',
                self._st.CLASSNAME + '-row-spacer')

        DOM.setElemAttribute(self._postSpacer, 'className',
                self._st.CLASSNAME + '-row-spacer')

        self._table.appendChild(self._tBodyElement)
        DOM.appendChild(self._container, self._preSpacer)
        DOM.appendChild(self._container, self._table)
        DOM.appendChild(self._container, self._postSpacer)


    def getAvailableWidth(self):
        availW = (self._st._scrollBodyPanel.getOffsetWidth()
                - self._st.getBorderWidth())
        return availW


    def renderInitialRows(self, rowData, firstIndex, rows):
        self._firstRendered = firstIndex
        self._lastRendered = (firstIndex + rows) - 1
        it = rowData.getChildIterator()
        self._aligns = self._st.tHead.getColumnAlignments()
        while it.hasNext():
            row = self.createRow(it.next(), self._aligns)
            self.addRow(row)
        if self.isAttached():
            self.fixSpacers()


    def renderRows(self, rowData, firstIndex, rows):
        # FIXME: review
        self._aligns = self._st.tHead.getColumnAlignments()
        it = rowData.getChildIterator()
        if firstIndex == self._lastRendered + 1:
            while it.hasNext():
                row = self.prepareRow(it.next())
                self.addRow(row)
                self._lastRendered += 1
            self.fixSpacers()
        elif firstIndex + rows == self._firstRendered:
            rowArray = [None] * rows
            i = rows
            while it.hasNext():
                i -= 1
                rowArray[i] = self.prepareRow(it.next())

            for i in range(rows):
                self.addRowBeforeFirstRendered(rowArray[i])
                self._firstRendered -= 1
        else:
            # completely new set of rows
            while self._lastRendered + 1 > self._firstRendered:
                self.unlinkRow(False)

            row = self.prepareRow(it.next())
            self._firstRendered = firstIndex
            self._lastRendered = firstIndex - 1
            self.addRow(row)
            self._lastRendered += 1
            self.setContainerHeight()
            self.fixSpacers()
            while it.hasNext():
                self.addRow(self.prepareRow(it.next()))
                self._lastRendered += 1

            self.fixSpacers()

        # this may be a new set of rows due content change,
        # ensure we have proper cache rows
        self.ensureCacheFilled()


    def ensureCacheFilled(self):
        reactFirstRow = (self._st._firstRowInViewPort
                - (self._st._pageLength * self._st._cache_react_rate))
        reactLastRow = (self._st._firstRowInViewPort + self._st._pageLength
                + (self._st._pageLength * self._st._cache_react_rate))

        if reactFirstRow < 0:
            reactFirstRow = 0

        if reactLastRow >= self._st._totalRows:
            reactLastRow = self._st._totalRows - 1

        if self._lastRendered < reactLastRow:
            # get some cache rows below visible area
            self._st._rowRequestHandler.setReqFirstRow(self._lastRendered + 1)
            self._st._rowRequestHandler.setReqRows(reactLastRow
                    - self._lastRendered)
            self._st._rowRequestHandler.deferRowFetch(1)
        elif self._st._scrollBody.getFirstRendered() > reactFirstRow:
            # Branch for fetching cache above visible area.
            #
            # If cache needed for both before and after visible area, this
            # will be rendered after-cache is received and rendered. So in
            # some rare situations the table may make two cache visits to
            # server.
            self._st._rowRequestHandler.setReqFirstRow(reactFirstRow)
            self._st._rowRequestHandler.setReqRows(self._firstRendered
                    - reactFirstRow)
            self._st._rowRequestHandler.deferRowFetch(1)


    def insertRows(self, rowData, firstIndex, rows):
        """Inserts rows as provided in the rowData starting at firstIndex.

        @param rowData:
        @param firstIndex:
        @param rows:
                   the number of rows
        @return: a list of the rows added.
        """
        self._aligns = self._st.tHead.getColumnAlignments()
        it = rowData.getChildIterator()
        insertedRows = list()
        if firstIndex == self._lastRendered + 1:
            while it.hasNext():
                row = self.prepareRow(it.next())
                self.addRow(row)
                insertedRows.add(row)
                self._lastRendered += 1
            self.fixSpacers()
        elif firstIndex + rows == self._firstRendered:
            rowArray = [None] * rows
            i = rows
            while it.hasNext():
                i -= 1
                rowArray[i] = self.prepareRow(it.next())
            for i in range(rows):
                self.addRowBeforeFirstRendered(rowArray[i])
                insertedRows.append(rowArray[i])
                self._firstRendered -= 1
        else:
            # insert in the middle
            ix = firstIndex
            while it.hasNext():
                row = self.prepareRow(it.next())
                self.insertRowAt(row, ix)
                insertedRows.append(row)
                self._lastRendered += 1
                ix += 1
            self.fixSpacers()
        return insertedRows


    def insertAndReindexRows(self, rowData, firstIndex, rows):
        inserted = self.insertRows(rowData, firstIndex, rows)
        actualIxOfFirstRowAfterInserted = ((firstIndex + rows)
                - self._firstRendered)

        for ix in range(actualIxOfFirstRowAfterInserted,
                        len(self._renderedRows)):
            r = self._renderedRows.get(ix)
            r.setIndex(r.getIndex() + rows)
        self.fixSpacers()
        return inserted


    def insertRowsDeleteBelow(self, rowData, firstIndex, rows):
        self.unlinkAllRowsStartingAt(firstIndex)
        self.insertRows(rowData, firstIndex, rows)


    def prepareRow(self, uidl):
        """This method is used to instantiate new rows for this table. It
        automatically sets correct widths to rows cells and assigns correct
        client reference for child widgets.

        This method can be called only after table has been initialized
        """
        row = self.createRow(uidl, self._aligns)
        row.initCellWidths()
        return row


    def createRow(self, uidl, aligns2):
        if uidl.hasAttribute('gen_html'):
            # This is a generated row.
            return VScrollTableGeneratedRow(uidl, aligns2)
        return VScrollTableRow(uidl, aligns2)


    def addRowBeforeFirstRendered(self, row):
        row.setIndex(self._firstRendered - 1)
        if row.isSelected():
            row.addStyleName('v-selected')
        self._tBodyElement.insertBefore(row.getElement(),
                self._tBodyElement.getFirstChild())
        self.adopt(row)
        self._renderedRows.add(0, row)


    def addRow(self, row):
        row.setIndex(self._firstRendered + len(self._renderedRows))
        if row.isSelected():
            row.addStyleName('v-selected')
        self._tBodyElement.appendChild(row.getElement())
        self.adopt(row)
        self._renderedRows.add(row)


    def insertRowAt(self, row, index):
        row.setIndex(index)
        if row.isSelected():
            row.addStyleName('v-selected')

        if index > 0:
            sibling = self.getRowByRowIndex(index - 1)
            self._tBodyElement.insertAfter(row.getElement(),
                    sibling.getElement())
        else:
            sibling = self.getRowByRowIndex(index)
            self._tBodyElement.insertBefore(row.getElement(),
                    sibling.getElement())

        self.adopt(row)
        actualIx = index - self._firstRendered
        self._renderedRows.add(actualIx, row)


    def iterator(self):
        return self._renderedRows


    def unlinkRow(self, fromBeginning):
        """@return false if couldn't remove row"""
        if self._lastRendered - self._firstRendered < 0:
            return False

        if fromBeginning:
            actualIx = 0
            self._firstRendered += 1
        else:
            actualIx = len(self._renderedRows) - 1
            self._lastRendered -= 1

        if actualIx >= 0:
            self.unlinkRowAtActualIndex(actualIx)
            self.fixSpacers()
            return True

        return False


    def unlinkRows(self, firstIndex, count):
        if count < 1:
            return

        if (self._firstRendered > firstIndex
                and self._firstRendered < firstIndex + count):
            firstIndex = self._firstRendered

        lastIndex = (firstIndex + count) - 1

        if self._lastRendered < lastIndex:
            lastIndex = self._lastRendered

        for ix in range(lastIndex, firstIndex, -1):
            self.unlinkRowAtActualIndex(self.actualIndex(ix))
            self._lastRendered -= 1

        self.fixSpacers()


    def unlinkAndReindexRows(self, firstIndex, count):
        self.unlinkRows(firstIndex, count)
        actualFirstIx = firstIndex - self._firstRendered
        for ix in range(actualFirstIx, len(self._renderedRows)):
            r = self._renderedRows.get(ix)
            r.setIndex(r.getIndex() - count)
        self.fixSpacers()


    def unlinkAllRowsStartingAt(self, index):
        if self._firstRendered > index:
            index = self._firstRendered

        for ix in range(len(self._renderedRows) - 1, index, -1):
            self.unlinkRowAtActualIndex(self.actualIndex(ix))
            self._lastRendered -= 1

        self.fixSpacers()


    def actualIndex(self, index):
        return index - self._firstRendered


    def unlinkRowAtActualIndex(self, index):
        toBeRemoved = self._renderedRows.get(index)

        # Unregister row tooltip
        self._st.client.registerTooltip(self._st, toBeRemoved.getElement(),
                None)

        for i in range(toBeRemoved.getElement().getChildCount()):
            # Unregister cell tooltips
            td = toBeRemoved.getElement().getChild(i)
            self._st.client.registerTooltip(self._st, td, None)

        self._st._lazyUnregistryBag.add(toBeRemoved)
        self._tBodyElement.removeChild(toBeRemoved.getElement())
        self.orphan(toBeRemoved)
        self._renderedRows.remove(index)


    def remove(self, w):
        raise NotImplementedError


    def onAttach(self):
        super(VScrollTableBody, self).onAttach()
        self.setContainerHeight()


    def setContainerHeight(self):
        """Fix container blocks height according to totalRows to avoid
        "bouncing" when scrolling
        """
        self.fixSpacers()
        DOM.setStyleAttribute(self._container, 'height',
                self._st.measureRowHeightOffset(self._st._totalRows) + 'px')


    def fixSpacers(self):
        prepx = self._st.measureRowHeightOffset(self._firstRendered)
        if prepx < 0:
            prepx = 0
        self._preSpacer.getStyle().setPropertyPx('height', prepx)
        postpx = (self._st.measureRowHeightOffset(self._st._totalRows - 1)
                - self._st.measureRowHeightOffset(self._lastRendered))
        if postpx < 0:
            postpx = 0
        self._postSpacer.getStyle().setPropertyPx('height', postpx)


    def getRowHeight(self, forceUpdate=False):
        if self._tBodyMeasurementsDone and not forceUpdate:
            return self._rowHeight
        else:
            if self._tBodyElement.getRows().getLength() > 0:
                tableHeight = self.getTableHeight()
                rowCount = self._tBodyElement.getRows().getLength()
                self._rowHeight = tableHeight / rowCount
            elif self.isAttached():
                # measure row height by adding a dummy row
                scrollTableRow = self.VScrollTableRow()
                self._tBodyElement.appendChild(scrollTableRow.getElement())
                self.getRowHeight(forceUpdate)
                self._tBodyElement.removeChild(scrollTableRow.getElement())
            else:
                # TODO: investigate if this can never happen anymore
                return self.DEFAULT_ROW_HEIGHT
            self._tBodyMeasurementsDone = True
            return self._rowHeight


    def getTableHeight(self):
        return self._table.getOffsetHeight()


    def getColWidth(self, columnIndex):
        """Returns the width available for column content.
        """
        if self._tBodyMeasurementsDone:
            if len(self._renderedRows) == 0:
                # no rows yet rendered
                return 0
            for row in self._renderedRows:
                if not isinstance(row, self.VScrollTableGeneratedRow):
                    tr = row.getElement()
                    wrapperdiv = tr.getCells().getItem(columnIndex).getFirstChildElement()
                    return wrapperdiv.getOffsetWidth()
            return 0
        else:
            return 0


    def setColWidth(self, colIndex, w):
        """Sets the content width of a column.

        Due IE limitation, we must set the width to a wrapper elements inside
        table cells (with overflow hidden, which does not work on td
        elements).

        To get this work properly crossplatform, we will also set the width
        of td.
        """
        for row in self._renderedRows:
            row.setCellWidth(colIndex, w)


    def getCellExtraWidth(self):
        """Method to return the space used for cell paddings + border."""
        if self._cellExtraWidth < 0:
            self.detectExtrawidth()
        return self._cellExtraWidth


    def detectExtrawidth(self):
        rows = self._tBodyElement.getRows()
        if rows.getLength() == 0:
            # need to temporary add empty row and detect
            scrollTableRow = VScrollTableRow()
            self._tBodyElement.appendChild(scrollTableRow.getElement())
            self.detectExtrawidth()
            self._tBodyElement.removeChild(scrollTableRow.getElement())
        else:
            noCells = False
            item = rows.getItem(0)
            firstTD = item.getCells().getItem(0)
            if firstTD is None:
                # content is currently empty, we need to add a fake cell
                # for measuring
                noCells = True
                next = self.next()
                sorted = self._st.tHead.getHeaderCell(0).isSorted() if self._st.tHead.getHeaderCell(0) is not None else False
                next.addCell(None, '', self._st.ALIGN_LEFT, '', True, sorted)
                firstTD = item.getCells().getItem(0)
            wrapper = firstTD.getFirstChildElement()
            self._cellExtraWidth = firstTD.getOffsetWidth() - wrapper.getOffsetWidth()
            if noCells:
                firstTD.getParentElement().removeChild(firstTD)


    def reLayoutComponents(self):
        for w in self:
            for widget in w:
                self._st.client.handleComponentRelativeSize(widget)


    def getLastRendered(self):
        return self._lastRendered


    def getFirstRendered(self):
        return self._firstRendered


    def moveCol(self, oldIndex, newIndex):
        # loop all rows and move given index to its new place
        rows = self
        while rows.hasNext():
            row = rows.next()
            td = DOM.getChild(row.getElement(), oldIndex)
            if td is not None:
                DOM.removeChild(row.getElement(), td)
                DOM.insertChild(row.getElement(), td, newIndex)


    def restoreRowVisibility(self):
        """Restore row visibility which is set to "none" when the row is
        rendered (due a performance optimization).
        """
        for row in self._renderedRows:
            row.getElement().getStyle().setProperty('visibility', '')


    def VScrollTableRow(VScrollTableBody_this, *args, **kwargs):

        class VScrollTableRow(Panel, ActionOwner, Container):
            _TOUCHSCROLL_TIMEOUT = 70
            _DRAGMODE_MULTIROW = 2
            childWidgets = list()
            _selected = False
            rowKey = None
            _pendingComponentPaints = None
            _actionKeys = None
            _rowElement = None
            _mDown = None
            _index = None
            _touchStart = None
            _ROW_CLASSNAME_EVEN = VScrollTable_this.CLASSNAME + '-row'
            _ROW_CLASSNAME_ODD = VScrollTable_this.CLASSNAME + '-row-odd'
            _TOUCH_CONTEXT_MENU_TIMEOUT = 500
            _contextTouchTimeout = None
            _touchStartY = None
            _touchStartX = None

            def __init__(self, *args):
                """None
                ---
                Add a dummy row, used for measurements if Table is empty.
                """
                _0 = args
                _1 = len(args)
                if _1 == 0:
                    self.__init__(0)
                    self.addStyleName(VScrollTable_this.CLASSNAME + '-row')
                    self.addCell(None, '_', 'b', '', True, False)
                elif _1 == 1:
                    rowKey, = _0
                    self.rowKey = rowKey
                    self._rowElement = Document.get().createTRElement()
                    self.setElement(self._rowElement)
                    DOM.sinkEvents(self.getElement(), (((Event.MOUSEEVENTS | Event.TOUCHEVENTS) | Event.ONDBLCLICK) | Event.ONCONTEXTMENU) | VTooltip.TOOLTIP_EVENTS)
                elif _1 == 2:
                    uidl, aligns = _0
                    self.__init__(uidl.getIntAttribute('key'))
                    # Rendering the rows as hidden improves Firefox and Safari
                    # performance drastically.

                    self.getElement().getStyle().setProperty('visibility', 'hidden')
                    rowStyle = uidl.getStringAttribute('rowstyle')
                    if rowStyle is not None:
                        self.addStyleName(VScrollTable_this.CLASSNAME + '-row-' + rowStyle)
                    rowDescription = uidl.getStringAttribute('rowdescr')
                    if rowDescription is not None and not (rowDescription == ''):
                        info = TooltipInfo(rowDescription)
                        VScrollTable_this.client.registerTooltip(VScrollTable_this, self._rowElement, info)
                    else:
                        # Remove possibly previously set tooltip
                        VScrollTable_this.client.registerTooltip(VScrollTable_this, self._rowElement, None)
                    VScrollTable_this.tHead.getColumnAlignments()
                    col = 0
                    visibleColumnIndex = -1
                    # row header
                    if VScrollTable_this.showRowHeaders:
                        sorted = VScrollTable_this.tHead.getHeaderCell(col).isSorted()
                        self.addCell(uidl, VScrollTable_this.buildCaptionHtmlSnippet(uidl), aligns[POSTINC(globals(), locals(), 'col')], 'rowheader', True, sorted)
                        visibleColumnIndex += 1
                    if uidl.hasAttribute('al'):
                        self._actionKeys = uidl.getStringArrayAttribute('al')
                    self.addCellsFromUIDL(uidl, aligns, col, visibleColumnIndex)
                    if uidl.hasAttribute('selected') and not self.isSelected():
                        self.toggleSelection()
                else:
                    raise ARGERROR(0, 2)

            def initCellWidths(self):
                cells = VScrollTable_this.tHead.getVisibleCellCount()
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < cells):
                        break
                    w = VScrollTable_this.getColWidth(VScrollTable_this.getColKeyByIndex(i))
                    if w < 0:
                        w = 0
                    self.setCellWidth(i, w)

            def setCellWidth(self, cellIx, width):
                cell = DOM.getChild(self.getElement(), cellIx)
                cell.getFirstChildElement().getStyle().setPropertyPx('width', width)
                cell.getStyle().setPropertyPx('width', width)

            def addCellsFromUIDL(self, uidl, aligns, col, visibleColumnIndex):
                cells = uidl.getChildIterator()
                while cells.hasNext():
                    cell = cells.next()
                    visibleColumnIndex += 1
                    columnId = VScrollTable_this._visibleColOrder[visibleColumnIndex]
                    style = ''
                    if uidl.hasAttribute('style-' + columnId):
                        style = uidl.getStringAttribute('style-' + columnId)
                    description = None
                    if uidl.hasAttribute('descr-' + columnId):
                        description = uidl.getStringAttribute('descr-' + columnId)
                    sorted = VScrollTable_this.tHead.getHeaderCell(col).isSorted()
                    if isinstance(cell, str):
                        self.addCell(uidl, str(cell), aligns[POSTINC(globals(), locals(), 'col')], style, self.isRenderHtmlInCells(), sorted, description)
                    else:
                        cellContent = VScrollTable_this.client.getPaintable(cell)
                        self.addCell(uidl, cellContent, aligns[POSTINC(globals(), locals(), 'col')], style, sorted)
                        self.paintComponent(cellContent, cell)

            def isRenderHtmlInCells(self):
                """Overriding this and returning true causes all text cells to be
                rendered as HTML.

                @return always returns false in the default implementation
                """
                return False

            def isInViewPort(self):
                """Detects whether row is visible in tables viewport.

                @return
                """
                absoluteTop = self.getAbsoluteTop()
                scrollPosition = VScrollTable_this._scrollBodyPanel.getScrollPosition()
                if absoluteTop < scrollPosition:
                    return False
                maxVisible = (scrollPosition + VScrollTable_this._scrollBodyPanel.getOffsetHeight()) - self.getOffsetHeight()
                if absoluteTop > maxVisible:
                    return False
                return True

            def isBefore(self, row1):
                """Makes a check based on indexes whether the row is before the
                compared row.

                @param row1
                @return true if this rows index is smaller than in the row1
                """
                return self.getIndex() < row1.getIndex()

            def setIndex(self, indexInWholeTable):
                """Sets the index of the row in the whole table. Currently used just
                to set even/odd classname

                @param indexInWholeTable
                """
                self._index = indexInWholeTable
                isOdd = indexInWholeTable % 2 == 0
                # Inverted logic to be backwards compatible with earlier 6.4.
                # It is very strange because rows 1,3,5 are considered "even"
                # and 2,4,6 "odd".
                # First remove any old styles so that both styles aren't
                # applied when indexes are updated.
                self.removeStyleName(self._ROW_CLASSNAME_ODD)
                self.removeStyleName(self._ROW_CLASSNAME_EVEN)
                if not isOdd:
                    self.addStyleName(self._ROW_CLASSNAME_ODD)
                else:
                    self.addStyleName(self._ROW_CLASSNAME_EVEN)

            def getIndex(self):
                return self._index

            def paintComponent(self, p, uidl):
                if self.isAttached():
                    p.updateFromUIDL(uidl, VScrollTable_this.client)
                else:
                    if self._pendingComponentPaints is None:
                        self._pendingComponentPaints = LinkedList()
                    self._pendingComponentPaints.add(uidl)

            def onAttach(self):
                super(VScrollTableRow, self).onAttach()
                if self._pendingComponentPaints is not None:
                    for uidl in self._pendingComponentPaints:
                        paintable = VScrollTable_this.client.getPaintable(uidl)
                        paintable.updateFromUIDL(uidl, VScrollTable_this.client)

            def onDetach(self):
                super(VScrollTableRow, self).onDetach()
                VScrollTable_this.client.getContextMenu().ensureHidden(self)

            def getKey(self):
                return String.valueOf.valueOf(self.rowKey)

            def addCell(self, *args):
                _0 = args
                _1 = len(args)
                if _1 == 5:
                    rowUidl, w, align, style, sorted = _0
                    td = DOM.createTD()
                    self.initCellWithWidget(w, align, style, sorted, td)
                elif _1 == 6:
                    rowUidl, text, align, style, textIsHTML, sorted = _0
                    self.addCell(rowUidl, text, align, style, textIsHTML, sorted, None)
                elif _1 == 7:
                    rowUidl, text, align, style, textIsHTML, sorted, description = _0
                    td = DOM.createTD()
                    self.initCellWithText(text, align, style, textIsHTML, sorted, description, td)
                else:
                    raise ARGERROR(5, 7)

            # String only content is optimized by not using Label widget

            def initCellWithText(self, text, align, style, textIsHTML, sorted, description, td):
                container = DOM.createDiv()
                className = VScrollTable_this.CLASSNAME + '-cell-content'
                if style is not None and not (style == ''):
                    className += ' ' + VScrollTable_this.CLASSNAME + '-cell-content-' + style
                if sorted:
                    className += ' ' + VScrollTable_this.CLASSNAME + '-cell-content-sorted'
                td.setClassName(className)
                container.setClassName(VScrollTable_this.CLASSNAME + '-cell-wrapper')
                if textIsHTML:
                    container.setInnerHTML(text)
                else:
                    container.setInnerText(text)
                if align != VScrollTable_this.ALIGN_LEFT:
                    _0 = align
                    _1 = False
                    while True:
                        if _0 == VScrollTable_this.ALIGN_CENTER:
                            _1 = True
                            container.getStyle().setProperty('textAlign', 'center')
                            break
                        if (_1 is True) or (_0 == VScrollTable_this.ALIGN_RIGHT):
                            _1 = True
                        if True:
                            _1 = True
                            container.getStyle().setProperty('textAlign', 'right')
                            break
                        break
                if description is not None and not (description == ''):
                    info = TooltipInfo(description)
                    VScrollTable_this.client.registerTooltip(VScrollTable_this, td, info)
                else:
                    # Remove possibly previously set tooltip
                    VScrollTable_this.client.registerTooltip(VScrollTable_this, td, None)
                td.appendChild(container)
                self.getElement().appendChild(td)

            def initCellWithWidget(self, w, align, style, sorted, td):
                container = DOM.createDiv()
                className = VScrollTable_this.CLASSNAME + '-cell-content'
                if style is not None and not (style == ''):
                    className += ' ' + VScrollTable_this.CLASSNAME + '-cell-content-' + style
                if sorted:
                    className += ' ' + VScrollTable_this.CLASSNAME + '-cell-content-sorted'
                td.setClassName(className)
                container.setClassName(VScrollTable_this.CLASSNAME + '-cell-wrapper')
                # TODO most components work with this, but not all (e.g.
                # Select)
                # Old comment: make widget cells respect align.
                # text-align:center for IE, margin: auto for others
                if align != VScrollTable_this.ALIGN_LEFT:
                    _0 = align
                    _1 = False
                    while True:
                        if _0 == VScrollTable_this.ALIGN_CENTER:
                            _1 = True
                            container.getStyle().setProperty('textAlign', 'center')
                            break
                        if (_1 is True) or (_0 == VScrollTable_this.ALIGN_RIGHT):
                            _1 = True
                        if True:
                            _1 = True
                            container.getStyle().setProperty('textAlign', 'right')
                            break
                        break
                td.appendChild(container)
                self.getElement().appendChild(td)
                # ensure widget not attached to another element (possible tBody
                # change)
                w.removeFromParent()
                container.appendChild(w.getElement())
                self.adopt(w)
                self.childWidgets.add(w)

            def iterator(self):
                return self.childWidgets

            def remove(self, w):
                if self.childWidgets.contains(w):
                    self.orphan(w)
                    DOM.removeChild(DOM.getParent(w.getElement()), w.getElement())
                    self.childWidgets.remove(w)
                    return True
                else:
                    return False

            def handleClickEvent(self, event, targetTdOrTr):
                if (
                    VScrollTable_this.client.hasEventListeners(VScrollTable_this, VScrollTable_this.ITEM_CLICK_EVENT_ID)
                ):
                    doubleClick = DOM.eventGetType(event) == Event.ONDBLCLICK
                    # This row was clicked
                    VScrollTable_this.client.updateVariable(VScrollTable_this.paintableId, 'clickedKey', '' + self.rowKey, False)
                    if self.getElement() == targetTdOrTr.getParentElement():
                        # A specific column was clicked
                        childIndex = DOM.getChildIndex(self.getElement(), targetTdOrTr)
                        colKey = None
                        colKey = VScrollTable_this.tHead.getHeaderCell(childIndex).getColKey()
                        VScrollTable_this.client.updateVariable(VScrollTable_this.paintableId, 'clickedColKey', colKey, False)
                    details = MouseEventDetails(event)
                    imm = True
                    if (
                        VScrollTable_this._immediate and event.getButton() == Event.BUTTON_LEFT and not doubleClick and VScrollTable_this.isSelectable() and not self.isSelected()
                    ):
                        # A left click when the table is selectable and in
                        # immediate mode on a row that is not currently
                        # selected will cause a selection event to be fired
                        # after this click event. By making the click event
                        # non-immediate we avoid sending two separate messages
                        # to the server.

                        imm = False
                    VScrollTable_this.client.updateVariable(VScrollTable_this.paintableId, 'clickEvent', str(details), imm)

            def handleTooltips(self, event, target):
                # React on click that occur on content cells only
                if target.hasTagName('TD'):
                    # Table cell (td)
                    container = target.getFirstChildElement()
                    widget = container.getFirstChildElement()
                    containsWidget = False
                    for w in self.childWidgets:
                        if widget == w.getElement():
                            containsWidget = True
                            break
                    if not containsWidget:
                        # Only text nodes has tooltips
                        if (
                            VScrollTable_this.client.getTooltipTitleInfo(VScrollTable_this, target) is not None
                        ):
                            # Cell has description, use it
                            VScrollTable_this.client.handleTooltipEvent(event, VScrollTable_this, target)
                        else:
                            # Cell might have row description, use row
                            # description
                            VScrollTable_this.client.handleTooltipEvent(event, VScrollTable_this, target.getParentElement())
                else:
                    # Table row (tr)
                    VScrollTable_this.client.handleTooltipEvent(event, VScrollTable_this, target)

            def onBrowserEvent(self, event):
                if VScrollTable_this._enabled:
                    type = event.getTypeInt()
                    targetTdOrTr = self.getEventTargetTdOrTr(event)
                    if type == Event.ONCONTEXTMENU:
                        self.showContextMenu(event)
                        if (
                            VScrollTable_this._enabled and (self._actionKeys is not None) or VScrollTable_this.client.hasEventListeners(VScrollTable_this, VScrollTable_this.ITEM_CLICK_EVENT_ID)
                        ):
                            # Prevent browser context menu only if there are
                            # action handlers or item click listeners
                            # registered
                            event.stopPropagation()
                            event.preventDefault()
                        return
                    targetCellOrRowFound = targetTdOrTr is not None
                    if targetCellOrRowFound:
                        self.handleTooltips(event, targetTdOrTr)
                    _0 = type
                    _1 = False
                    while True:
                        if _0 == Event.ONDBLCLICK:
                            _1 = True
                            if targetCellOrRowFound:
                                self.handleClickEvent(event, targetTdOrTr)
                            break
                        if (_1 is True) or (_0 == Event.ONMOUSEUP):
                            _1 = True
                            if targetCellOrRowFound:
                                self._mDown = False
                                self.handleClickEvent(event, targetTdOrTr)
                                if event.getButton() == Event.BUTTON_LEFT and VScrollTable_this.isSelectable():
                                    # Ctrl+Shift click
                                    if (
                                        event.getCtrlKey() or event.getMetaKey() and event.getShiftKey() and VScrollTable_this.isMultiSelectModeDefault()
                                    ):
                                        self.toggleShiftSelection(False)
                                        VScrollTable_this.setRowFocus(self)
                                        # Ctrl click
                                    elif (
                                        event.getCtrlKey() or event.getMetaKey() and VScrollTable_this.isMultiSelectModeDefault()
                                    ):
                                        wasSelected = self.isSelected()
                                        self.toggleSelection()
                                        VScrollTable_this.setRowFocus(self)
                                        # next possible range select must start on
                                        # this row

                                        VScrollTable_this._selectionRangeStart = self
                                        if wasSelected:
                                            VScrollTable_this.removeRowFromUnsentSelectionRanges(self)
                                    elif (
                                        event.getCtrlKey() or event.getMetaKey() and VScrollTable_this.isSingleSelectMode()
                                    ):
                                        # Ctrl (or meta) click (Single selection)
                                        if (
                                            (not self.isSelected()) or (self.isSelected() and VScrollTable_this._nullSelectionAllowed)
                                        ):
                                            if not self.isSelected():
                                                VScrollTable_this.deselectAll()
                                            self.toggleSelection()
                                            VScrollTable_this.setRowFocus(self)
                                    elif event.getShiftKey() and VScrollTable_this.isMultiSelectModeDefault():
                                        # Shift click
                                        self.toggleShiftSelection(True)
                                    else:
                                        # click
                                        currentlyJustThisRowSelected = len(VScrollTable_this._selectedRowKeys) == 1 and self.getKey() in VScrollTable_this._selectedRowKeys
                                        if not currentlyJustThisRowSelected:
                                            if (
                                                VScrollTable_this.isSingleSelectMode() or VScrollTable_this.isMultiSelectModeDefault()
                                            ):
                                                # For default multi select mode
                                                # (ctrl/shift) and for single
                                                # select mode we need to clear the
                                                # previous selection before
                                                # selecting a new one when the user
                                                # clicks on a row. Only in
                                                # multiselect/simple mode the old
                                                # selection should remain after a
                                                # normal click.

                                                VScrollTable_this.deselectAll()
                                            self.toggleSelection()
                                        elif (
                                            VScrollTable_this.isSingleSelectMode() or VScrollTable_this.isMultiSelectModeSimple() and VScrollTable_this._nullSelectionAllowed
                                        ):
                                            self.toggleSelection()
                                        # else NOP to avoid excessive server
                                        # visits (selection is removed with
                                        # CTRL/META click)

                                        VScrollTable_this._selectionRangeStart = self
                                        VScrollTable_this.setRowFocus(self)
                                    # Remove IE text selection hack
                                    if BrowserInfo.get().isIE():
                                        event.getEventTarget().setPropertyJSO('onselectstart', None)
                                    VScrollTable_this.sendSelectedRows()
                            break
                        if (_1 is True) or (_0 == Event.ONTOUCHEND):
                            _1 = True
                        if (_1 is True) or (_0 == Event.ONTOUCHCANCEL):
                            _1 = True
                            if self._touchStart is not None:
                                # Touch has not been handled as neither context or
                                # drag start, handle it as a click.

                                Util.simulateClickFromTouchEvent(self._touchStart, self)
                                self._touchStart = None
                            if self._contextTouchTimeout is not None:
                                self._contextTouchTimeout.cancel()
                            break
                        if (_1 is True) or (_0 == Event.ONTOUCHMOVE):
                            _1 = True
                            if self.isSignificantMove(event):
                                # TODO figure out scroll delegate don't eat events
                                # if row is selected. Null check for active
                                # delegate is as a workaround.

                                if (
                                    VScrollTable_this._dragmode != 0 and self._touchStart is not None and TouchScrollDelegate.getActiveScrollDelegate() is None
                                ):
                                    self.startRowDrag(self._touchStart, type, targetTdOrTr)
                                if self._contextTouchTimeout is not None:
                                    self._contextTouchTimeout.cancel()
                                # Avoid clicks and drags by clearing touch start
                                # flag.

                                self._touchStart = None
                            break
                        if (_1 is True) or (_0 == Event.ONTOUCHSTART):
                            _1 = True
                            self._touchStart = event
                            # save position to fields, touches in events are same
                            # isntance during the operation.
                            touch = event.getChangedTouches().get(0)
                            self._touchStartX = touch.getClientX()
                            self._touchStartY = touch.getClientY()
                            # Prevent simulated mouse events.
                            self._touchStart.preventDefault()
                            if (VScrollTable_this._dragmode != 0) or (self._actionKeys is not None):


                                class _10_(Timer):

                                    def run(self):
                                        activeScrollDelegate = TouchScrollDelegate.getActiveScrollDelegate()
                                        if activeScrollDelegate is not None and not activeScrollDelegate.isMoved():
                                            # scrolling hasn't started. Cancel
                                            # scrolling and let row handle this as
                                            # drag start or context menu.

                                            activeScrollDelegate.stopScrolling()
                                        else:
                                            # Scrolled or scrolling, clear touch
                                            # start to indicate that row shouldn't
                                            # handle touch move/end events.

                                            VScrollTableRow_this._touchStart = None


                                _10_ = _10_()
                                _10_.schedule(self._TOUCHSCROLL_TIMEOUT)
                                if self._contextTouchTimeout is None and self._actionKeys is not None:

                                    class _11_(Timer):

                                        def run(self):
                                            if VScrollTableRow_this._touchStart is not None:
                                                VScrollTableRow_this.showContextMenu(VScrollTableRow_this._touchStart)
                                                VScrollTableRow_this._touchStart = None

                                    _11_ = _11_()
                                    self._contextTouchTimeout = _11_
                                self._contextTouchTimeout.cancel()
                                self._contextTouchTimeout.schedule(self._TOUCH_CONTEXT_MENU_TIMEOUT)
                            break
                        if (_1 is True) or (_0 == Event.ONMOUSEDOWN):
                            _1 = True
                            if targetCellOrRowFound:
                                VScrollTable_this.setRowFocus(self)
                                VScrollTableBody_this.ensureFocus()
                                if (
                                    VScrollTable_this._dragmode != 0 and event.getButton() == NativeEvent.BUTTON_LEFT
                                ):
                                    self.startRowDrag(event, type, targetTdOrTr)
                                elif (
                                    (event.getCtrlKey() or event.getShiftKey()) or (event.getMetaKey() and VScrollTable_this.isMultiSelectModeDefault())
                                ):
                                    # Prevent default text selection in Firefox
                                    event.preventDefault()
                                    # Prevent default text selection in IE
                                    if BrowserInfo.get().isIE():
                                        event.getEventTarget().setPropertyJSO('onselectstart', VScrollTable_this.getPreventTextSelectionIEHack())
                                    event.stopPropagation()
                            break
                        if (_1 is True) or (_0 == Event.ONMOUSEOUT):
                            _1 = True
                            if targetCellOrRowFound:
                                self._mDown = False
                            break
                        if True:
                            _1 = True
                            break
                        break
                super(VScrollTableRow, self).onBrowserEvent(event)

            def isSignificantMove(self, event):
                if self._touchStart is None:
                    # no touch start
                    return False
                # TODO calculate based on real distance instead of separate
                # axis checks

                touch = event.getChangedTouches().get(0)
                if (
                    self.Math.abs(touch.getClientX() - self._touchStartX) > TouchScrollDelegate.SIGNIFICANT_MOVE_THRESHOLD
                ):
                    return True
                if (
                    self.Math.abs(touch.getClientY() - self._touchStartY) > TouchScrollDelegate.SIGNIFICANT_MOVE_THRESHOLD
                ):
                    return True
                return False

            def startRowDrag(self, event, type, targetTdOrTr):
                self._mDown = True
                transferable = VTransferable()
                transferable.setDragSource(VScrollTable_this)
                transferable.setData('itemId', '' + self.rowKey)
                cells = self._rowElement.getCells()
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < cells.getLength()):
                        break
                    if cells.getItem(i).isOrHasChild(targetTdOrTr):
                        headerCell = VScrollTable_this.tHead.getHeaderCell(i)
                        transferable.setData('propertyId', headerCell.cid)
                        break
                ev = VDragAndDropManager.get().startDrag(transferable, event, True)
                if (
                    VScrollTable_this._dragmode == self._DRAGMODE_MULTIROW and VScrollTable_this.isMultiSelectModeAny() and '' + self.rowKey in VScrollTable_this._selectedRowKeys
                ):
                    ev.createDragImage(VScrollTable_this._scrollBody.tBodyElement, True)
                    dragImage = ev.getDragImage()
                    i = 0
                    _1 = True
                    iterator = VScrollTable_this._scrollBody
                    while True:
                        if _1 is True:
                            _1 = False
                        if not iterator.hasNext():
                            break
                        next = iterator.next()
                        child = dragImage.getChild(POSTINC(globals(), locals(), 'i'))
                        if not ('' + next.rowKey in VScrollTable_this._selectedRowKeys):
                            child.getStyle().setVisibility(Visibility.HIDDEN)
                else:
                    ev.createDragImage(self.getElement(), True)
                if type == Event.ONMOUSEDOWN:
                    event.preventDefault()
                event.stopPropagation()

            def getEventTargetTdOrTr(self, event):
                """Finds the TD that the event interacts with. Returns null if the
                target of the event should not be handled. If the event target is
                the row directly this method returns the TR element instead of
                the TD.

                @param event
                @return TD or TR element that the event targets (the actual event
                        target is this element or a child of it)
                """
                eventTarget = event.getEventTarget()
                widget = Util.findWidget(eventTarget, None)
                thisTrElement = self.getElement()
                if widget is not self:
                    # This is a workaround to make Labels, read only TextFields
                    # and Embedded in a Table clickable (see #2688). It is
                    # really not a fix as it does not work with a custom read
                    # only components (not extending VLabel/VEmbedded).

                    while widget is not None and widget.getParent() is not self:
                        widget = widget.getParent()
                    if (
                        not isinstance(widget, VLabel) and not isinstance(widget, VEmbedded) and not (isinstance(widget, VTextField) and widget.isReadOnly())
                    ):
                        return None
                if eventTarget == thisTrElement:
                    # This was a click on the TR element
                    return thisTrElement
                # Iterate upwards until we find the TR element
                element = eventTarget
                while element is not None and element.getParentElement() != thisTrElement:
                    element = element.getParentElement()
                return element

            def showContextMenu(self, event):
                if VScrollTable_this._enabled and self._actionKeys is not None:
                    # Show context menu if there are registered action handlers
                    left = Util.getTouchOrMouseClientX(event)
                    top = Util.getTouchOrMouseClientY(event)
                    top += Window.getScrollTop()
                    left += Window.getScrollLeft()
                    VScrollTable_this.client.getContextMenu().showAt(self, left, top)

            def isSelected(self):
                """Has the row been selected?

                @return Returns true if selected, else false
                """
                return self._selected

            def toggleSelection(self):
                """Toggle the selection of the row"""
                self._selected = not self._selected
                VScrollTable_this._selectionChanged = True
                if self._selected:
                    VScrollTable_this._selectedRowKeys.add(String.valueOf.valueOf(self.rowKey))
                    self.addStyleName('v-selected')
                else:
                    self.removeStyleName('v-selected')
                    VScrollTable_this._selectedRowKeys.remove(String.valueOf.valueOf(self.rowKey))

            def toggleShiftSelection(self, deselectPrevious):
                """Is called when a user clicks an item when holding SHIFT key down.
                This will select a new range from the last focused row

                @param deselectPrevious
                           Should the previous selected range be deselected
                """
                # Ensures that we are in multiselect mode and that we have a
                # previous selection which was not a deselection

                # (non-Javadoc)
                #
                # @see com.vaadin.terminal.gwt.client.ui.IActionOwner#getActions ()

                if VScrollTable_this.isSingleSelectMode():
                    # No previous selection found
                    VScrollTable_this.deselectAll()
                    self.toggleSelection()
                    return
                # Set the selectable range
                endRow = self
                startRow = VScrollTable_this._selectionRangeStart
                if startRow is None:
                    startRow = VScrollTable_this._focusedRow
                    # If start row is null then we have a multipage selection
                    # from
                    # above
                    if startRow is None:
                        startRow = VScrollTable_this._scrollBody.next()
                        VScrollTable_this.setRowFocus(endRow)
                # Deselect previous items if so desired
                if deselectPrevious:
                    VScrollTable_this.deselectAll()
                # we'll ensure GUI state from top down even though selection
                # was the opposite way
                if not startRow.isBefore(endRow):
                    tmp = startRow
                    startRow = endRow
                    endRow = tmp
                range = VScrollTable_this.SelectionRange(startRow, endRow)
                for w in VScrollTable_this._scrollBody:
                    row = w
                    if range.inRange(row):
                        if not row.isSelected():
                            row.toggleSelection()
                        VScrollTable_this._selectedRowKeys.add(row.getKey())
                # Add range
                if startRow != endRow:
                    VScrollTable_this._selectedRowRanges.add(range)

            def getActions(self):
                if self._actionKeys is None:
                    return []
                actions = [None] * len(self._actionKeys)
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(actions)):
                        break
                    actionKey = self._actionKeys[i]

                    class a(TreeAction):

                        def execute(self):
                            super(_12_, self).execute()
                            VScrollTable_this.lazyRevertFocusToRow(VScrollTableRow_this)

                    a.setCaption(VScrollTable_this.getActionCaption(actionKey))
                    a.setIconUrl(VScrollTable_this.getActionIcon(actionKey))
                    actions[i] = a
                return actions

            def getClient(self):
                return VScrollTable_this.client

            def getPaintableId(self):
                return VScrollTable_this.paintableId

            def getAllocatedSpace(self, child):
                w = 0
                i = self.getColIndexOf(child)
                headerCell = VScrollTable_this.tHead.getHeaderCell(i)
                if headerCell is not None:
                    if VScrollTable_this._initializedAndAttached:
                        w = headerCell.getWidth()
                    else:
                        # header offset width is not absolutely correct value,
                        # but a best guess (expecting similar content in all
                        # columns ->
                        # if one component is relative width so are others)
                        w = headerCell.getOffsetWidth() - VScrollTableBody_this.getCellExtraWidth()

                class _13_(RenderSpace):

                    def getHeight(self):
                        return VScrollTableBody_this.getRowHeight()

                _13_ = _13_()
                return _13_

            def getColIndexOf(self, child):
                widgetCell = child.getElement().getParentElement().getParentElement()
                cells = self._rowElement.getCells()
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < cells.getLength()):
                        break
                    if cells.getItem(i) == widgetCell:
                        return i
                return -1

            def hasChildComponent(self, component):
                return self.childWidgets.contains(component)

            def replaceChildComponent(self, oldComponent, newComponent):
                parentElement = oldComponent.getElement().getParentElement()
                index = self.childWidgets.index(oldComponent)
                oldComponent.removeFromParent()
                parentElement.appendChild(newComponent.getElement())
                self.childWidgets.add(index, newComponent)
                self.adopt(newComponent)

            def requestLayout(self, children):
                # row size should never change and system wouldn't event
                # survive as this is a kind of fake paitable
                return True

            def updateCaption(self, component, uidl):
                # NOP, not rendered
                pass

            def updateFromUIDL(self, uidl, client):
                # Should never be called,
                # Component container interface faked here to get layouts
                # render properly
                pass

        return VScrollTableRow(*args, **kwargs)

    class VScrollTableGeneratedRow(VScrollTableRow):
        _spanColumns = None
        _htmlContentAllowed = None

        def __init__(self, uidl, aligns):
            super(VScrollTableGeneratedRow, self)(uidl, aligns)
            self.addStyleName('v-table-generated-row')

        def isSpanColumns(self):
            return self._spanColumns

        def initCellWidths(self):
            if self._spanColumns:
                self.setSpannedColumnWidthAfterDOMFullyInited()
            else:
                super(VScrollTableGeneratedRow, self).initCellWidths()

        def setSpannedColumnWidthAfterDOMFullyInited(self):
            # Defer setting width on spanned columns to make sure that
            # they are added to the DOM before trying to calculate
            # widths.

            class _14_(ScheduledCommand):

                def execute(self):
                    if VScrollTable_this.showRowHeaders:
                        VScrollTableGeneratedRow_this.setCellWidth(0, VScrollTable_this.tHead.getHeaderCell(0).getWidth())
                        VScrollTableGeneratedRow_this.calcAndSetSpanWidthOnCell(1)
                    else:
                        VScrollTableGeneratedRow_this.calcAndSetSpanWidthOnCell(0)

            _14_ = _14_()
            Scheduler.get().scheduleDeferred(_14_)

        def isRenderHtmlInCells(self):
            return self._htmlContentAllowed

        def addCellsFromUIDL(self, uidl, aligns, col, visibleColumnIndex):
            self._htmlContentAllowed = uidl.getBooleanAttribute('gen_html')
            self._spanColumns = uidl.getBooleanAttribute('gen_span')
            cells = uidl.getChildIterator()
            if self._spanColumns:
                colCount = uidl.getChildCount()
                if cells.hasNext():
                    cell = cells.next()
                    if isinstance(cell, str):
                        self.addSpannedCell(uidl, str(cell), aligns[0], '', self._htmlContentAllowed, False, None, colCount)
                    else:
                        self.addSpannedCell(uidl, cell, aligns[0], '', False, colCount)
            else:
                super(VScrollTableGeneratedRow, self).addCellsFromUIDL(uidl, aligns, col, visibleColumnIndex)

        def addSpannedCell(self, *args):
            _0 = args
            _1 = len(args)
            if _1 == 6:
                rowUidl, w, align, style, sorted, colCount = _0
                td = DOM.createTD()
                td.setColSpan(colCount)
                self.initCellWithWidget(w, align, style, sorted, td)
            elif _1 == 8:
                rowUidl, text, align, style, textIsHTML, sorted, description, colCount = _0
                td = DOM.createTD()
                td.setColSpan(colCount)
                self.initCellWithText(text, align, style, textIsHTML, sorted, description, td)
            else:
                raise ARGERROR(6, 8)

        # String only content is optimized by not using Label widget

        def setCellWidth(self, cellIx, width):
            if self.isSpanColumns():
                if VScrollTable_this.showRowHeaders:
                    if cellIx == 0:
                        super(VScrollTableGeneratedRow, self).setCellWidth(0, width)
                    else:
                        # We need to recalculate the spanning TDs width for
                        # every cellIx in order to support column resizing.
                        self.calcAndSetSpanWidthOnCell(1)
                else:
                    # Same as above.
                    self.calcAndSetSpanWidthOnCell(0)
            else:
                super(VScrollTableGeneratedRow, self).setCellWidth(cellIx, width)

        def calcAndSetSpanWidthOnCell(self, cellIx):
            spanWidth = 0
            _0 = True
            ix = 1 if VScrollTable_this.showRowHeaders else 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    ix += 1
                if not (ix < VScrollTable_this.tHead.getVisibleCellCount()):
                    break
                spanWidth += VScrollTable_this.tHead.getHeaderCell(ix).getOffsetWidth()
            Util.setWidthExcludingPaddingAndBorder(self.getElement().getChild(cellIx), spanWidth, 13, False)

    def ensureFocus(self):
        """Ensure the component has a focus.

        TODO the current implementation simply always calls focus for the
        component. In case the Table at some point implements focus/blur
        listeners, this method needs to be evolved to conditionally call
        focus only if not currently focused.
        """
        if not VScrollTable_this._hasFocus:
            VScrollTable_this._scrollBodyPanel.setFocus(True)