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

from pyjamas.ui.Panel import Panel

from muntjac.terminal.gwt.client.browser_info import BrowserInfo
from muntjac.terminal.gwt.client.ui.action_owner import ActionOwner

from muntjac.terminal.gwt.client.ui.scroll_table.header_cell \
    import RowHeadersHeaderCell, HeaderCell


class TableHead(Panel, ActionOwner):

    _WRAPPER_WIDTH = 900000

    def __init__(self, st):
        self._st = st

        self._visibleCells = list()
        self._availableCells = dict()
        self._div = DOM.createDiv()
        self._hTableWrapper = DOM.createDiv()
        self._hTableContainer = DOM.createDiv()
        self._table = DOM.createTable()
        self._headerTableBody = DOM.createTBody()
        self._tr = DOM.createTR()
        self._columnSelector = DOM.createDiv()
        self._focusedSlot = -1

        if BrowserInfo.get().isIE():
            self._table.setPropertyInt('cellSpacing', 0)

        DOM.setStyleAttribute(self._hTableWrapper, 'overflow', 'hidden')
        DOM.setElemAttribute(self._hTableWrapper, 'className',
                self._st.CLASSNAME + '-header')

        # TODO: move styles to CSS
        DOM.setElemAttribute(self._columnSelector, 'className',
                self._st.CLASSNAME + '-column-selector')
        DOM.setStyleAttribute(self._columnSelector, 'display', 'none')

        DOM.appendChild(self._table, self._headerTableBody)
        DOM.appendChild(self._headerTableBody, self._tr)
        DOM.appendChild(self._hTableContainer, self._table)
        DOM.appendChild(self._hTableWrapper, self._hTableContainer)
        DOM.appendChild(self._div, self._hTableWrapper)
        DOM.appendChild(self._div, self._columnSelector)
        self.setElement(self._div)

        self.setStyleName(self._st.CLASSNAME + '-header-wrap')

        DOM.sinkEvents(self._columnSelector, Event.ONCLICK)

        self._availableCells[self._st._ROW_HEADER_COLUMN_KEY] = \
                self._st.RowHeadersHeaderCell()


    def resizeCaptionContainer(self, cell):
        lastcell = self.getHeaderCell(len(self._visibleCells) - 1)

        # Measure column widths
        columnTotalWidth = 0
        for w in self._visibleCells:
            columnTotalWidth += w.getOffsetWidth()

        if (cell == lastcell and self._columnSelector.getOffsetWidth() > 0
                and columnTotalWidth >= self._div.getOffsetWidth() - self._columnSelector.getOffsetWidth()
                and not self._st.hasVerticalScrollbar()):
            # Ensure column caption is visible when placed under the column
            # selector widget by shifting and resizing the caption.
            offset = 0
            diff = self._div.getOffsetWidth() - columnTotalWidth
            if diff < self._columnSelector.getOffsetWidth() and diff > 0:
                # If the difference is less than the column selectors width
                # then just offset by the
                # difference
                offset = self._columnSelector.getOffsetWidth() - diff
            else:
                # Else offset by the whole column selector
                offset = self._columnSelector.getOffsetWidth()

            lastcell.resizeCaptionContainer(offset)
        else:
            cell.resizeCaptionContainer(0)


    def clear(self):
        for cid in self._availableCells.keys():
            self.removeCell(cid)

        self._availableCells.clear()
        self._availableCells[self._st._ROW_HEADER_COLUMN_KEY] = \
                RowHeadersHeaderCell()


    def updateCellsFromUIDL(self, uidl):
        it = uidl.getChildIterator()
        updated = set()
        refreshContentWidths = False
        while it.hasNext():
            col = it.next()
            cid = col.getStringAttribute('cid')
            updated.add(cid)

            caption = self._st.buildCaptionHtmlSnippet(col)
            c = self.getHeaderCell(cid)
            if c is None:
                c = HeaderCell(cid, caption)
                self._availableCells[cid] = c
                if self._st._initializedAndAttached:
                    # we will need a column width recalculation
                    self._st._initializedAndAttached = False
                    self._st._initialContentReceived = False
                    self._st._isNewBody = True
            else:
                c.setText(caption)

            if col.hasAttribute('sortable'):
                c.setSortable(True)
                if cid == self._st._sortColumn:
                    c.setSorted(True)
                else:
                    c.setSorted(False)
            else:
                c.setSortable(False)

            if col.hasAttribute('align'):
                c.setAlign(col.getStringAttribute('align')[0])
            else:
                c.setAlign(self._st.ALIGN_LEFT)

            if col.hasAttribute('width'):
                widthStr = col.getStringAttribute('width')
                # Make sure to accomodate for the sort indicator if
                # necessary.
                width = int(widthStr)
                if width < c.getMinWidth():
                    width = c.getMinWidth()

                if width != c.getWidth() and self._st._scrollBody is not None:
                    # Do a more thorough update if a column is resized from
                    # the server *after* the header has been properly
                    # initialized
                    colIx = self._st.getColIndexByKey(c.cid)
                    newWidth = width

                    class _9_(ScheduledCommand):

                        def execute(self):
                            self._st.setColWidth(self.colIx, self.newWidth,
                                    True)

                    _9_ = _9_()
                    Scheduler.get().scheduleDeferred(_9_)
                    refreshContentWidths = True
                else:
                    c.setWidth(width, True)

            elif self._st._recalcWidths:
                c.setUndefinedWidth()

            if col.hasAttribute('er'):
                c.setExpandRatio(col.getFloatAttribute('er'))

            if col.hasAttribute('collapsed'):
                # ensure header is properly removed from parent (case when
                # collapsing happens via servers side api)
                if c.isAttached():
                    c.removeFromParent()
                    self._st._headerChangedDuringUpdate = True

        if refreshContentWidths:
            # Recalculate the column sizings if any column has changed

            class _10_(ScheduledCommand):

                def execute(self):
                    self._st.triggerLazyColumnAdjustment(True)

            _10_ = _10_()
            Scheduler.get().scheduleDeferred(_10_)

        # check for orphaned header cells
        cit = self._availableCells.keys()
        while cit.hasNext():
            cid = cit.next()
            if not (cid in updated):
                self.removeCell(cid)
                cit.remove()
                # we will need a column width recalculation, since columns
                # with expand ratios should expand to fill the void.
                self._st._initializedAndAttached = False
                self._st._initialContentReceived = False
                self._st._isNewBody = True


    def enableColumn(self, cid, index):
        c = self.getHeaderCell(cid)
        if (not c.isEnabled()) or (self.getHeaderCell(index) != c):
            self.setHeaderCell(index, c)
            if self._st._initializedAndAttached:
                self._st._headerChangedDuringUpdate = True


    def getVisibleCellCount(self):
        return len(self._visibleCells)


    def setHorizontalScrollPosition(self, scrollLeft):
        if BrowserInfo.get().isIE6():
            self._hTableWrapper.getStyle().setPosition('relative')#Position.RELATIVE)
            self._hTableWrapper.getStyle().setLeft(-scrollLeft, 'px')#Unit.PX)
        else:
            self._hTableWrapper.setScrollLeft(scrollLeft)


    def setColumnCollapsingAllowed(self, cc):
        if cc:
            self._columnSelector.getStyle().setDisplay('block')#Display.BLOCK)
        else:
            self._columnSelector.getStyle().setDisplay('none')#Display.NONE)


    def disableBrowserIntelligence(self):
        self._hTableContainer.getStyle().setWidth(self._WRAPPER_WIDTH, 'px')#Unit.PX)


    def enableBrowserIntelligence(self):
        self._hTableContainer.getStyle().clearWidth()


    def setHeaderCell(self, index, cell):
        if cell.isEnabled():
            # we're moving the cell
            DOM.removeChild(self._tr, cell.getElement())
            self.orphan(cell)
            self._visibleCells.remove(cell)
        if index < len(self._visibleCells):
            # insert to right slot
            DOM.insertChild(self._tr, cell.getElement(), index)
            self.adopt(cell)
            self._visibleCells.add(index, cell)
        elif index == len(self._visibleCells):
            # simply append
            DOM.appendChild(self._tr, cell.getElement())
            self.adopt(cell)
            self._visibleCells.add(cell)
        else:
            raise RuntimeError('Header cells must be appended in order')


    def getHeaderCell(self, index_or_cid):
        """Get's HeaderCell by it's column Key.

        Note that this returns HeaderCell even if it is currently collapsed.

        @param index_or_cid:
                   Column key of accessed HeaderCell
        @return: HeaderCell
        """
        if isinstance(index_or_cid, int):
            index = index_or_cid
            if index >= 0 and index < len(self._visibleCells):
                return self._visibleCells[index]
            else:
                return None
        else:
            cid = index_or_cid
            return self._availableCells.get(cid)


    def moveCell(self, oldIndex, newIndex):
        hCell = self.getHeaderCell(oldIndex)
        cell = hCell.getElement()
        self._visibleCells.remove(oldIndex)
        DOM.removeChild(self._tr, cell)
        DOM.insertChild(self._tr, cell, newIndex)
        self._visibleCells.add(newIndex, hCell)


    def iterator(self):
        return self._visibleCells


    def remove(self, w):
        if w in self._visibleCells:
            self._visibleCells.remove(w)
            self.orphan(w)
            DOM.removeChild(DOM.getParent(w.getElement()), w.getElement())
            return True
        return False


    def removeCell(self, colKey):
        c = self.getHeaderCell(colKey)
        self.remove(c)


    def focusSlot(self, index):
        self.removeSlotFocus()
        if index > 0:
            DOM.setElemAttribute(DOM.getFirstChild(DOM.getChild(self._tr,
                    index - 1)), 'className',
                    self._st.CLASSNAME + '-resizer ' + self._st.CLASSNAME + '-focus-slot-right')
        else:
            DOM.setElemAttribute(DOM.getFirstChild(DOM.getChild(self._tr,
                    index)),
                    'className',
                    self._st.CLASSNAME + '-resizer ' + self._st.CLASSNAME + '-focus-slot-left')
        self._focusedSlot = index


    def removeSlotFocus(self):
        if self._focusedSlot < 0:
            return

        if self._focusedSlot == 0:
            DOM.setElemAttribute(DOM.getFirstChild(DOM.getChild(self._tr,
                    self._focusedSlot)),
                    'className', self._st.CLASSNAME + '-resizer')
        elif self._focusedSlot > 0:
            DOM.setElemAttribute(DOM.getFirstChild(DOM.getChild(self._tr,
                    self._focusedSlot - 1)),
                    'className', self._st.CLASSNAME + '-resizer')
        self._focusedSlot = -1


    def onBrowserEvent(self, event):
        if self._st._enabled:
            if event.getEventTarget() == self._columnSelector:
                left = DOM.getAbsoluteLeft(self._columnSelector)
                top = (DOM.getAbsoluteTop(self._columnSelector)
                        + DOM.getIntElemAttribute(self._columnSelector,
                                'offsetHeight'))
                self._st.client.getContextMenu().showAt(self, left, top)


    def onDetach(self):
        super(TableHead, self).onDetach()
        if self._st.client is not None:
            self._st.client.getContextMenu().ensureHidden(self)


    class VisibleColumnAction(Action):

        def __init__(self, colKey, th):
            super(VisibleColumnAction, self).__init__(th)

            self._colKey = colKey
            self._collapsed = None
            self.caption = self._st.tHead.getHeaderCell(colKey).getCaption()
            self._currentlyFocusedRow = self._st._focusedRow


        def execute(self):
            self._st.client.getContextMenu().hide()
            # toggle selected column
            if self._colKey in self._st._collapsedColumns:
                self._st._collapsedColumns.remove(self._colKey)
            else:
                self._st.tHead.removeCell(self._colKey)
                self._st._collapsedColumns.add(self._colKey)
                self._st.triggerLazyColumnAdjustment(True)

            # update variable to server
            self._st.client.updateVariable(self._st.paintableId,
                    'collapsedcolumns',
                    list(self._st._collapsedColumns),
                    False)

            # let rowRequestHandler determine proper rows
            self._st._rowRequestHandler.refreshContent()
            self._st.lazyRevertFocusToRow(self._currentlyFocusedRow)


        def setCollapsed(self, b):
            self._collapsed = b


        def getHTML(self):
            """Override default method to distinguish on/off columns"""
            buf = str()
            if self._collapsed:
                buf += '<span class=\"v-off\">'
            else:
                buf += '<span class=\"v-on\">'
            buf += super(VisibleColumnAction, self).getHTML()
            buf += '</span>'
            return buf


    def getActions(self):
        # Returns columns as Action array for column select popup
        if (self._st._columnReordering and self._st._columnOrder is not None):
            cols = self._st._columnOrder
        else:
            # if columnReordering is disabled, we need different way to get
            # all available columns
            cols = self._st._visibleColOrder
            cols = [None] * (len(self._st._visibleColOrder)
                    + len(self._st._collapsedColumns))

            for i in range(len(self._st._visibleColOrder)):
                cols[i] = self._st._visibleColOrder[i]

            it = self._st._collapsedColumns
            while it.hasNext():
                cols[i] = it.next()
                i += 1

        actions = [None] * len(cols)
        for i in range(len(cols)):
            cid = cols[i]
            c = self.getHeaderCell(cid)
            a = self.VisibleColumnAction(c.getColKey())
            a.setCaption(c.getCaption())
            if not c.isEnabled():
                a.setCollapsed(True)
            actions[i] = a

        return actions


    def getClient(self):
        return self._st.client


    def getPaintableId(self):
        return self._st.paintableId


    def getColumnAlignments(self):
        """Returns column alignments for visible columns"""
        it = self._visibleCells
        aligns = [None] * len(self._visibleCells)
        colIndex = 0
        while it.hasNext():
            aligns[colIndex] = it.next().getAlign()
            colIndex += 1
        return aligns


    def disableAutoColumnWidthCalculation(self, source):
        """Disables the automatic calculation of all column widths by forcing
        the widths to be "defined" thus turning off expand ratios and such.
        """
        for cell in self._availableCells.values():
            cell.disableAutoWidthCalculation()

        # fire column resize events for all columns but the source of the
        # resize action, since an event will fire separately for this.
        columns = list(self._availableCells.values())
        columns.remove(source)
        self._st.sendColumnWidthUpdates(columns)
        self._st.forceRealignColumnHeaders()
