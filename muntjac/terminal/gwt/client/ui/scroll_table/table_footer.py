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

from muntjac.terminal.gwt.client.ui.scroll_table.footer_cell import FooterCell
from muntjac.terminal.gwt.client.browser_info import BrowserInfo


class TableFooter(Panel):
    """The footer of the table which can be seen in the bottom of the Table."""

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

        DOM.setStyleAttribute(self._hTableWrapper, 'overflow', 'hidden')
        DOM.setElemAttribute(self._hTableWrapper, 'className',
                self._st.CLASSNAME + '-footer')
        DOM.appendChild(self._table, self._headerTableBody)
        DOM.appendChild(self._headerTableBody, self._tr)
        DOM.appendChild(self._hTableContainer, self._table)
        DOM.appendChild(self._hTableWrapper, self._hTableContainer)
        DOM.appendChild(self._div, self._hTableWrapper)
        self.setElement(self._div)
        self.setStyleName(self._st.CLASSNAME + '-footer-wrap')
        self._availableCells.put(self._st._ROW_HEADER_COLUMN_KEY,
                self._st.RowHeadersFooterCell())


    def clear(self):
        for cid in self._availableCells.keys():
            self.removeCell(cid)
        self._availableCells.clear()
        self._availableCells[self._st._ROW_HEADER_COLUMN_KEY] = \
                self._st.RowHeadersFooterCell()


    def remove(self, w):
        if self._visibleCells.contains(w):
            self._visibleCells.remove(w)
            self.orphan(w)
            DOM.removeChild(DOM.getParent(w.getElement()), w.getElement())
            return True
        return False


    def iterator(self):
        return self._visibleCells


    def getFooterCell(self, index_or_cid):
        """Gets a footer cell by using a column index or the given columnId.

        @param index_or_cid:
                   The columnId or the index of the column
        @return: The Cell
        """
        if isinstance(index_or_cid, int):
            index = index_or_cid
            if index < len(self._visibleCells):
                return self._visibleCells[index]
            else:
                return None
        else:
            cid = index_or_cid
            return self._availableCells[cid]


    def updateCellsFromUIDL(self, uidl):
        """Updates the cells contents when updateUIDL request is received

        @param uidl:
                   The UIDL
        """
        columnIterator = uidl.getChildIterator()
        updated = set()
        while columnIterator.hasNext():
            col = columnIterator.next()
            cid = col.getStringAttribute('cid')
            updated.add(cid)
            caption = col.getStringAttribute('fcaption') if col.hasAttribute('fcaption') else ''
            c = self.getFooterCell(cid)

            if c is None:
                c = FooterCell(cid, caption)
                self._availableCells.put(cid, c)
                if self._st._initializedAndAttached:
                    # we will need a column width recalculation
                    self._st._initializedAndAttached = False
                    self._st._initialContentReceived = False
                    self._st._isNewBody = True
            else:
                c.setText(caption)

            if col.hasAttribute('align'):
                c.setAlign(col.getStringAttribute('align')[0])
            else:
                c.setAlign(self._st.ALIGN_LEFT)

            if col.hasAttribute('width'):
                if self._st._scrollBody is None:
                    # Already updated by setColWidth called from
                    # TableHeads.updateCellsFromUIDL in case of a server
                    # side resize
                    width = col.getStringAttribute('width')
                    c.setWidth(int(width), True)
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

        # check for orphaned header cells
        _0 = True
        cit = self._availableCells.keys()
        while cit.hasNext():
            cid = cit.next()
            if not (cid in updated):
                self.removeCell(cid)
                cit.remove()


    def setFooterCell(self, index, cell):
        """Set a footer cell for a specified column index

        @param index:
                   The index
        @param cell:
                   The footer cell
        """
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


    def removeCell(self, colKey):
        """Remove a cell by using the columnId

        @param colKey:
                   The columnId to remove
        """
        c = self.getFooterCell(colKey)
        self.remove(c)


    def enableColumn(self, cid, index):
        """Enable a column (Sets the footer cell)

        @param cid:
                   The columnId
        @param index:
                   The index of the column
        """
        c = self.getFooterCell(cid)
        if (not c.isEnabled()) or (self.getFooterCell(index) != c):
            self.setFooterCell(index, c)
            if self._st._initializedAndAttached:
                self._st._headerChangedDuringUpdate = True


    def disableBrowserIntelligence(self):
        """Disable browser measurement of the table width"""
        DOM.setStyleAttribute(self._hTableContainer, 'width',
                self._WRAPPER_WIDTH + 'px')


    def enableBrowserIntelligence(self):
        """Enable browser measurement of the table width"""
        DOM.setStyleAttribute(self._hTableContainer, 'width', '')


    def setHorizontalScrollPosition(self, scrollLeft):
        """Set the horizontal position in the cell in the footer. This is done
        when a horizontal scrollbar is present.

        @param scrollLeft:
                   The value of the leftScroll
        """
        if BrowserInfo.get().isIE6():
            self._hTableWrapper.getStyle().setProperty('position', 'relative')
            self._hTableWrapper.getStyle().setPropertyPx('left', -scrollLeft)
        else:
            self._hTableWrapper.setScrollLeft(scrollLeft)


    def moveCell(self, oldIndex, newIndex):
        """Swap cells when the column are dragged

        @param oldIndex:
                   The old index of the cell
        @param newIndex:
                   The new index of the cell
        """
        hCell = self.getFooterCell(oldIndex)
        cell = hCell.getElement()
        self._visibleCells.remove(oldIndex)
        DOM.removeChild(self._tr, cell)
        DOM.insertChild(self._tr, cell, newIndex)
        self._visibleCells.append(newIndex, hCell)
