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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.ui.Table import (Table,)
from com.vaadin.terminal.gwt.client.ui.VScrollTable import (VScrollTable,)
# from com.google.gwt.user.client.ui.Button import (Button,)
# from com.google.gwt.user.client.ui.Grid import (Grid,)
# from com.google.gwt.user.client.ui.HorizontalPanel import (HorizontalPanel,)
# from com.google.gwt.user.client.ui.Label import (Label,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.HashMap import (HashMap,)
# from java.util.Iterator import (Iterator,)
# from java.util.Set import (Set,)
HeaderCell = VScrollTable.HeaderCell


class VTablePaging(Composite, Table, Paintable, ClickHandler):
    """TODO make this work (just an early prototype). We may want to have paging
    style table which will be much lighter than VScrollTable is.
    """
    _tBody = Grid()
    _nextPage = Button('&gt;')
    _prevPage = Button('&lt;')
    _firstPage = Button('&lt;&lt;')
    _lastPage = Button('&gt;&gt;')
    _pageLength = 15
    _rowHeaders = False
    _client = None
    _id = None
    _immediate = False
    _selectMode = Table.SELECT_MODE_NONE
    _selectedRowKeys = list()
    _totalRows = None
    _visibleColumns = dict()
    _rows = None
    _firstRow = None
    _sortAscending = True
    _pager = None
    rowKeysToTableRows = dict()

    def __init__(self):
        self._tBody.setStyleName('itable-tbody')
        panel = VerticalPanel()
        self._pager = HorizontalPanel()
        self._pager.add(self._firstPage)
        self._firstPage.addClickHandler(self)
        self._pager.add(self._prevPage)
        self._prevPage.addClickHandler(self)
        self._pager.add(self._nextPage)
        self._nextPage.addClickHandler(self)
        self._pager.add(self._lastPage)
        self._lastPage.addClickHandler(self)
        panel.add(self._pager)
        panel.add(self._tBody)
        self.initWidget(panel)

    def updateFromUIDL(self, uidl, client):
        if client.updateComponent(self, uidl, True):
            return
        self._client = client
        self._id = uidl.getStringAttribute('id')
        self._immediate = uidl.getBooleanAttribute('immediate')
        self._totalRows = uidl.getIntAttribute('totalrows')
        self._pageLength = uidl.getIntAttribute('pagelength')
        self._firstRow = uidl.getIntAttribute('firstrow')
        self._rows = uidl.getIntAttribute('rows')
        if uidl.hasAttribute('selectmode'):
            if uidl.getStringAttribute('selectmode') == 'multi':
                self._selectMode = Table.SELECT_MODE_MULTI
            else:
                self._selectMode = Table.SELECT_MODE_SINGLE
            if uidl.hasAttribute('selected'):
                selectedKeys = uidl.getStringArrayVariableAsSet('selected')
                self._selectedRowKeys.clear()
                _0 = True
                it = selectedKeys
                while True:
                    if _0 is True:
                        _0 = False
                    if not it.hasNext():
                        break
                    self._selectedRowKeys.add(it.next())
        if uidl.hasVariable('sortascending'):
            self._sortAscending = uidl.getBooleanVariable('sortascending')
        if uidl.hasAttribute('rowheaders'):
            self._rowHeaders = True
        rowData = None
        visibleColumns = None
        _1 = True
        it = uidl.getChildIterator()
        while True:
            if _1 is True:
                _1 = False
            if not it.hasNext():
                break
            c = it.next()
            if c.getTag() == 'rows':
                rowData = c
            elif c.getTag() == 'actions':
                self.updateActionMap(c)
            elif c.getTag() == 'visiblecolumns':
                visibleColumns = c
        self._tBody.resize(self._rows + 1, uidl.getIntAttribute('cols') + (1 if self._rowHeaders else 0))
        self.updateHeader(visibleColumns)
        self.updateBody(rowData)
        self.updatePager()

    def updateHeader(self, c):
        it = c.getChildIterator()
        self._visibleColumns.clear()
        colIndex = 1 if self._rowHeaders else 0
        while it.hasNext():
            col = it.next()
            cid = col.getStringAttribute('cid')
            if not col.hasAttribute('collapsed'):
                self._tBody.setWidget(0, colIndex, self.HeaderCell(cid, col.getStringAttribute('caption')))
            colIndex += 1

    def updateActionMap(self, c):
        # TODO Auto-generated method stub
        pass

    def updateBody(self, uidl):
        """Updates row data from uidl. UpdateFromUIDL delegates updating tBody to
        this method.

        Updates may be to different part of tBody, depending on update type. It
        can be initial row data, scroll up, scroll down...

        @param uidl
                   which contains row data
        """
        it = uidl.getChildIterator()
        curRowIndex = 1
        while it.hasNext():
            rowUidl = it.next()
            row = self.TableRow(curRowIndex, String.valueOf.valueOf(rowUidl.getIntAttribute('key')), rowUidl.hasAttribute('selected'))
            colIndex = 0
            if self._rowHeaders:
                self._tBody.setWidget(curRowIndex, colIndex, self.BodyCell(row, rowUidl.getStringAttribute('caption')))
                colIndex += 1
            cells = rowUidl.getChildIterator()
            while cells.hasNext():
                cell = cells.next()
                if isinstance(cell, str):
                    self._tBody.setWidget(curRowIndex, colIndex, self.BodyCell(row, cell))
                else:
                    cellContent = self._client.getPaintable(cell)
                    bodyCell = self.BodyCell(row)
                    bodyCell.setWidget(cellContent)
                    self._tBody.setWidget(curRowIndex, colIndex, bodyCell)
                colIndex += 1
            curRowIndex += 1

    def updatePager(self):
        if self._pageLength == 0:
            self._pager.setVisible(False)
            return
        if self.isFirstPage():
            self._firstPage.setEnabled(False)
            self._prevPage.setEnabled(False)
        else:
            self._firstPage.setEnabled(True)
            self._prevPage.setEnabled(True)
        if self.hasNextPage():
            self._nextPage.setEnabled(True)
            self._lastPage.setEnabled(True)
        else:
            self._nextPage.setEnabled(False)
            self._lastPage.setEnabled(False)

    def hasNextPage(self):
        if self._firstRow + self._rows + 1 > self._totalRows:
            return False
        return True

    def isFirstPage(self):
        if self._firstRow == 0:
            return True
        return False

    def onClick(self, event):
        sender = event.getSource()
        if isinstance(sender, Button):
            if sender == self._firstPage:
                self._client.updateVariable(self._id, 'firstvisible', 0, True)
            elif sender == self._nextPage:
                self._client.updateVariable(self._id, 'firstvisible', self._firstRow + self._pageLength, True)
            elif sender == self._prevPage:
                newFirst = self._firstRow - self._pageLength
                if newFirst < 0:
                    newFirst = 0
                self._client.updateVariable(self._id, 'firstvisible', newFirst, True)
            elif sender == self._lastPage:
                self._client.updateVariable(self._id, 'firstvisible', self._totalRows - self._pageLength, True)
        if isinstance(sender, self.HeaderCell):
            hCell = sender
            self._client.updateVariable(self._id, 'sortcolumn', hCell.getCid(), False)
            self._client.updateVariable(self._id, 'sortascending', False if self._sortAscending else True, True)

    class HeaderCell(HTML):
        _cid = None

        def getCid(self):
            return self._cid

        def setCid(self, pid):
            self._cid = pid

        def __init__(self, pid, caption):
            super(HeaderCell, self)()
            self._cid = pid
            self.addClickHandler(VTablePaging_this)
            self.setText(caption)
            # TODO remove debug color
            DOM.setStyleAttribute(self.getElement(), 'color', 'brown')
            DOM.setStyleAttribute(self.getElement(), 'font-weight', 'bold')

    def BodyCell(VTablePaging_this, *args, **kwargs):

        class BodyCell(SimplePanel):
            """Abstraction of table cell content. In needs to know on which row it is in
            case of context click.

            @author mattitahvonen
            """
            _row = None

            def __init__(self, *args):
                _0 = args
                _1 = len(args)
                if _1 == 1:
                    row, = _0
                    super(BodyCell, self)()
                    self.sinkEvents(Event.BUTTON_LEFT | Event.BUTTON_RIGHT)
                    self._row = row
                elif _1 == 2:
                    row2, textContent = _0
                    super(BodyCell, self)()
                    self.sinkEvents(Event.BUTTON_LEFT | Event.BUTTON_RIGHT)
                    self._row = row2
                    self.setWidget(Label(textContent))
                else:
                    raise ARGERROR(1, 2)

            def onBrowserEvent(self, event):
                print 'CEll event: ' + str(event)
                _0 = DOM.eventGetType(event)
                _1 = False
                while True:
                    if _0 == Event.BUTTON_RIGHT:
                        _1 = True
                        self._row.showContextMenu(event)
                        Window.alert('context menu un-implemented')
                        DOM.eventCancelBubble(event, True)
                        break
                    if (_1 is True) or (_0 == Event.BUTTON_LEFT):
                        _1 = True
                        if VTablePaging_this._selectMode > Table.SELECT_MODE_NONE:
                            self._row.toggleSelected()
                        break
                    if True:
                        _1 = True
                        break
                    break
                super(BodyCell, self).onBrowserEvent(event)

        return BodyCell(*args, **kwargs)

    def TableRow(VTablePaging_this, *args, **kwargs):

        class TableRow(object):
            _key = None
            _rowIndex = None
            _selected = False

            def __init__(self, rowIndex, rowKey, selected):
                VTablePaging_this.rowKeysToTableRows.put(rowKey, self)
                self._rowIndex = rowIndex
                self._key = rowKey
                self.setSelected(selected)

            def setSelected(self, sel):
                """This method is used to set row status. Does not change value on
                server.

                @param selected
                """
                self._selected = sel
                if self._selected:
                    VTablePaging_this._selectedRowKeys.add(self._key)
                    DOM.setStyleAttribute(VTablePaging_this._tBody.getRowFormatter().getElement(self._rowIndex), 'background', 'yellow')
                else:
                    VTablePaging_this._selectedRowKeys.remove(self._key)
                    DOM.setStyleAttribute(VTablePaging_this._tBody.getRowFormatter().getElement(self._rowIndex), 'background', 'transparent')

            def setContextMenuOptions(self, options):
                pass

            def toggleSelected(self):
                """Toggles rows select state. Also updates state to server according to
                tables immediate flag.
                """
                if self._selected:
                    self.setSelected(False)
                else:
                    if VTablePaging_this._selectMode == Table.SELECT_MODE_SINGLE:
                        VTablePaging_this.deselectAll()
                    self.setSelected(True)
                VTablePaging_this._client.updateVariable(VTablePaging_this._id, 'selected', list([None] * len(VTablePaging_this._selectedRowKeys)), VTablePaging_this._immediate)

            def showContextMenu(self, event):
                """Shows context menu for this row.

                @param event
                           Event which triggered context menu. Correct place for
                           context menu can be determined with it.
                """
                print 'TODO: Show context menu'

        return TableRow(*args, **kwargs)

    def deselectAll(self):
        keys = list(self._selectedRowKeys)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(keys)):
                break
            tableRow = self.rowKeysToTableRows[keys[i]]
            if tableRow is not None:
                tableRow.setSelected(False)
        # still ensure all selects are removed from
        self._selectedRowKeys.clear()

    def add(self, w):
        # TODO Auto-generated method stub
        pass

    def clear(self):
        # TODO Auto-generated method stub
        pass

    def iterator(self):
        # TODO Auto-generated method stub
        return None

    def remove(self, w):
        # TODO Auto-generated method stub
        return False
