# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR, POSTINC,)
from com.vaadin.terminal.gwt.client.TooltipInfo import (TooltipInfo,)
from com.vaadin.terminal.gwt.client.ui.dd.DDUtil import (DDUtil,)
from com.vaadin.terminal.gwt.client.VTooltip import (VTooltip,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.VLabel import (VLabel,)
from com.vaadin.terminal.gwt.client.ui.dd.VHasDropHandler import (VHasDropHandler,)
from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
from com.vaadin.terminal.gwt.client.Container import (Container,)
from com.vaadin.terminal.gwt.client.ui.VTextField import (VTextField,)
from com.vaadin.terminal.gwt.client.ui.Table import (Table,)
from com.vaadin.terminal.gwt.client.ui.TouchScrollDelegate import (TouchScrollDelegate,)
from com.vaadin.terminal.gwt.client.RenderSpace import (RenderSpace,)
from com.vaadin.terminal.gwt.client.ui.ActionOwner import (ActionOwner,)
from com.vaadin.terminal.gwt.client.ui.TreeAction import (TreeAction,)
from com.vaadin.terminal.gwt.client.ui.FocusableScrollPanel import (FocusableScrollPanel,)
from com.vaadin.terminal.gwt.client.ui.Action import (Action,)
from com.vaadin.terminal.gwt.client.MouseEventDetails import (MouseEventDetails,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCallback import (VAcceptCallback,)
from com.vaadin.terminal.gwt.client.ui.dd.VTransferable import (VTransferable,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.VEmbedded import (VEmbedded,)
from com.vaadin.terminal.gwt.client.ui.dd.VDragAndDropManager import (VDragAndDropManager,)
from com.vaadin.terminal.gwt.client.ui.dd.VAbstractDropHandler import (VAbstractDropHandler,)
from com.vaadin.terminal.gwt.client.Focusable import (Focusable,)
# from com.google.gwt.core.client.JavaScriptObject import (JavaScriptObject,)
# from com.google.gwt.dom.client.NodeList import (NodeList,)
# from com.google.gwt.dom.client.Style.Display import (Display,)
# from com.google.gwt.dom.client.Style.Visibility import (Visibility,)
# from com.google.gwt.dom.client.TableRowElement import (TableRowElement,)
# from com.google.gwt.dom.client.TableSectionElement import (TableSectionElement,)
# from com.google.gwt.dom.client.Touch import (Touch,)
# from com.google.gwt.event.dom.client.KeyPressEvent import (KeyPressEvent,)
# from com.google.gwt.event.dom.client.KeyPressHandler import (KeyPressHandler,)
# from com.google.gwt.event.dom.client.TouchStartEvent import (TouchStartEvent,)
# from com.google.gwt.event.dom.client.TouchStartHandler import (TouchStartHandler,)
# from com.google.gwt.user.client.ui.Panel import (Panel,)
# from com.google.gwt.user.client.ui.UIObject import (UIObject,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Collection import (Collection,)
# from java.util.HashMap import (HashMap,)
# from java.util.HashSet import (HashSet,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedList import (LinkedList,)
# from java.util.List import (List,)
# from java.util.Set import (Set,)
VScrollTableRow = VScrollTable.VScrollTableBody.VScrollTableRow


class VScrollTable(FlowPanel, Table, ScrollHandler, VHasDropHandler, FocusHandler, BlurHandler, Focusable, ActionOwner):
    """VScrollTable

    VScrollTable is a FlowPanel having two widgets in it: * TableHead component *
    ScrollPanel

    TableHead contains table's header and widgets + logic for resizing,
    reordering and hiding columns.

    ScrollPanel contains VScrollTableBody object which handles content. To save
    some bandwidth and to improve clients responsiveness with loads of data, in
    VScrollTableBody all rows are not necessary rendered. There are "spacers" in
    VScrollTableBody to use the exact same space as non-rendered rows would use.
    This way we can use seamlessly traditional scrollbars and scrolling to fetch
    more rows instead of "paging".

    In VScrollTable we listen to scroll events. On horizontal scrolling we also
    update TableHeads scroll position which has its scrollbars hidden. On
    vertical scroll events we will check if we are reaching the end of area where
    we have rows rendered and

    TODO implement unregistering for child components in Cells
    """
    ATTRIBUTE_PAGEBUFFER_FIRST = 'pb-ft'
    ATTRIBUTE_PAGEBUFFER_LAST = 'pb-l'
    _ROW_HEADER_COLUMN_KEY = '0'
    CLASSNAME = 'v-table'
    CLASSNAME_SELECTION_FOCUS = CLASSNAME + '-focus'
    ITEM_CLICK_EVENT_ID = 'itemClick'
    HEADER_CLICK_EVENT_ID = 'handleHeaderClick'
    FOOTER_CLICK_EVENT_ID = 'handleFooterClick'
    COLUMN_RESIZE_EVENT_ID = 'columnResize'
    COLUMN_REORDER_EVENT_ID = 'columnReorder'
    _CACHE_RATE_DEFAULT = 2
    # The default multi select mode where simple left clicks only selects one
    # item, CTRL+left click selects multiple items and SHIFT-left click selects
    # a range of items.

    _MULTISELECT_MODE_DEFAULT = 0
    # The simple multiselect mode is what the table used to have before
    # ctrl/shift selections were added. That is that when this is set clicking
    # on an item selects/deselects the item and no ctrl/shift selections are
    # available.

    _MULTISELECT_MODE_SIMPLE = 1
    # multiple of pagelength which component will cache when requesting more
    # rows

    _cache_rate = _CACHE_RATE_DEFAULT
    # fraction of pageLenght which can be scrolled without making new request
    _cache_react_rate = 0.75 * _cache_rate
    ALIGN_CENTER = 'c'
    ALIGN_LEFT = 'b'
    ALIGN_RIGHT = 'e'
    _CHARCODE_SPACE = 32
    _firstRowInViewPort = 0
    _pageLength = 15
    _lastRequestedFirstvisible = 0
    # to detect "serverside scroll"
    showRowHeaders = False
    _columnOrder = None
    client = None
    paintableId = None
    _immediate = None
    _nullSelectionAllowed = True
    _selectMode = Table.SELECT_MODE_NONE
    _selectedRowKeys = set()
    # When scrolling and selecting at the same time, the selections are not in
    # sync with the server while retrieving new rows (until key is released).

    _unSyncedselectionsBeforeRowFetch = None
    # These are used when jumping between pages when pressing Home and End
    _selectLastItemInNextRender = False
    _selectFirstItemInNextRender = False
    _focusFirstItemInNextRender = False
    _focusLastItemInNextRender = False
    # The currently focused row
    _focusedRow = None
    # Helper to store selection range start in when using the keyboard
    _selectionRangeStart = None
    # Flag for notifying when the selection has changed and should be sent to
    # the server

    _selectionChanged = False
    # The speed (in pixels) which the scrolling scrolls vertically/horizontally
    _scrollingVelocity = 10
    _scrollingVelocityTimer = None
    _bodyActionKeys = None
    _enableDebug = False

    def SelectionRange(VScrollTable_this, *args, **kwargs):

        class SelectionRange(object):
            """Represents a select range of rows"""
            _startRow = None
            _length = None

            def __init__(self, *args):
                """Constuctor."""
                _0 = args
                _1 = len(args)
                if _1 == 2:
                    if isinstance(_0[1], VScrollTableRow):
                        row1, row2 = _0
                        if row2.isBefore(row1):
                            self._startRow = row2
                            endRow = row1
                        else:
                            self._startRow = row1
                            endRow = row2
                        self._length = (endRow.getIndex() - self._startRow.getIndex()) + 1
                    else:
                        row, length = _0
                        self._startRow = row
                        self._length = length
                else:
                    raise ARGERROR(2, 2)

            # (non-Javadoc)
            # 
            # @see java.lang.Object#toString()

            def toString(self):
                return self._startRow.getKey() + '-' + self._length

            def inRange(self, row):
                return row.getIndex() >= self._startRow.getIndex() and row.getIndex() < self._startRow.getIndex() + self._length

            def split(self, row):
                assert row.isAttached()
                ranges = list(2)
                endOfFirstRange = row.getIndex() - 1
                if not (endOfFirstRange - self._startRow.getIndex() < 0):
                    # create range of first part unless its length is < 1
                    endOfRange = VScrollTable_this._scrollBody.getRowByRowIndex(endOfFirstRange)
                    ranges.add(VScrollTable_this.SelectionRange(self._startRow, endOfRange))
                startOfSecondRange = row.getIndex() + 1
                if not (self.getEndIndex() - startOfSecondRange < 0):
                    # create range of second part unless its length is < 1
                    startOfRange = VScrollTable_this._scrollBody.getRowByRowIndex(startOfSecondRange)
                    ranges.add(VScrollTable_this.SelectionRange(startOfRange, (self.getEndIndex() - startOfSecondRange) + 1))
                return ranges

            def getEndIndex(self):
                return (self._startRow.getIndex() + self._length) - 1

        return SelectionRange(*args, **kwargs)

    _selectedRowRanges = set()
    _initializedAndAttached = False
    # Flag to indicate if a column width recalculation is needed due update.
    _headerChangedDuringUpdate = False
    tHead = TableHead()
    _tFoot = TableFooter()
    _scrollBodyPanel = FocusableScrollPanel(True)

    class navKeyPressHandler(KeyPressHandler):

        def onKeyPress(self, keyPressEvent):
            # This is used for Firefox only, since Firefox auto-repeat
            # works correctly only if we use a key press handler, other
            # browsers handle it correctly when using a key down handler
            if not BrowserInfo.get().isGecko():
                return
            event = keyPressEvent.getNativeEvent()
            if not VScrollTable_this._enabled:
                # Cancel default keyboard events on a disabled Table
                # (prevents scrolling)
                event.preventDefault()
            elif VScrollTable_this._hasFocus:
                # Key code in Firefox/onKeyPress is present only for
                # special keys, otherwise 0 is returned
                keyCode = event.getKeyCode()
                if keyCode == 0 and event.getCharCode() == ' ':
                    # Provide a keyCode for space to be compatible with
                    # FireFox keypress event
                    keyCode = VScrollTable_this._CHARCODE_SPACE
                if (
                    VScrollTable_this.handleNavigation(keyCode, event.getCtrlKey() or event.getMetaKey(), event.getShiftKey())
                ):
                    event.preventDefault()
                VScrollTable_this.startScrollingVelocityTimer()

    class navKeyUpHandler(KeyUpHandler):

        def onKeyUp(self, keyUpEvent):
            event = keyUpEvent.getNativeEvent()
            keyCode = event.getKeyCode()
            if not VScrollTable_this.isFocusable():
                VScrollTable_this.cancelScrollingVelocityTimer()
            elif VScrollTable_this.isNavigationKey(keyCode):
                if (
                    (keyCode == VScrollTable_this.getNavigationDownKey()) or (keyCode == VScrollTable_this.getNavigationUpKey())
                ):
                    # in multiselect mode the server may still have value from
                    # previous page. Clear it unless doing multiselection or
                    # just moving focus.

                    if not event.getShiftKey() and not event.getCtrlKey():
                        VScrollTable_this.instructServerToForgetPreviousSelections()
                    VScrollTable_this.sendSelectedRows()
                VScrollTable_this.cancelScrollingVelocityTimer()
                VScrollTable_this._navKeyDown = False

    class navKeyDownHandler(KeyDownHandler):

        def onKeyDown(self, keyDownEvent):
            event = keyDownEvent.getNativeEvent()
            # This is not used for Firefox
            if BrowserInfo.get().isGecko():
                return
            if not VScrollTable_this._enabled:
                # Cancel default keyboard events on a disabled Table
                # (prevents scrolling)
                event.preventDefault()
            elif VScrollTable_this._hasFocus:
                if (
                    VScrollTable_this.handleNavigation(event.getKeyCode(), event.getCtrlKey() or event.getMetaKey(), event.getShiftKey())
                ):
                    VScrollTable_this._navKeyDown = True
                    event.preventDefault()
                VScrollTable_this.startScrollingVelocityTimer()

    _totalRows = None
    _collapsedColumns = None
    _rowRequestHandler = None
    _scrollBody = None
    _firstvisible = 0
    _sortAscending = None
    _sortColumn = None
    _oldSortColumn = None
    _columnReordering = None
    # This map contains captions and icon urls for actions like: * "33_c" ->
    # "Edit" * "33_i" -> "http://dom.com/edit.png"

    _actionMap = dict()
    _visibleColOrder = None
    _initialContentReceived = False
    _scrollPositionElement = None
    _enabled = None
    _showColHeaders = None
    _showColFooters = None
    # flag to indicate that table body has changed
    _isNewBody = True
    # Read from the "recalcWidths" -attribute. When it is true, the table will
    # recalculate the widths for columns - desirable in some cases. For #1983,
    # marked experimental.

    _recalcWidths = False
    _lazyUnregistryBag = list()
    _height = None
    _width = ''
    _rendering = False
    _hasFocus = False
    _dragmode = None
    _multiselectmode = None
    _tabIndex = None
    _touchScrollDelegate = None
    _lastRenderedHeight = None
    # Values (serverCacheFirst+serverCacheLast) sent by server that tells which
    # rows (indexes) are in the server side cache (page buffer). -1 means
    # unknown. The server side cache row MUST MATCH the client side cache rows.
    # 
    # If the client side cache contains additional rows with e.g. buttons, it
    # will cause out of sync when such a button is pressed.
    # 
    # If the server side cache contains additional rows with e.g. buttons,
    # scrolling in the client will cause empty buttons to be rendered
    # (cached=true request for non-existing components)

    _serverCacheFirst = -1
    _serverCacheLast = -1

    def __init__(self):
        VScrollTable_thisBAA = self
        self.setMultiSelectMode(self._MULTISELECT_MODE_DEFAULT)
        self._scrollBodyPanel.setStyleName(self.CLASSNAME + '-body-wrapper')
        self._scrollBodyPanel.addFocusHandler(self)
        self._scrollBodyPanel.addBlurHandler(self)
        self._scrollBodyPanel.addScrollHandler(self)
        self._scrollBodyPanel.setStyleName(self.CLASSNAME + '-body')
        # Firefox auto-repeat works correctly only if we use a key press
        # handler, other browsers handle it correctly when using a key down
        # handler

        if BrowserInfo.get().isGecko():
            self._scrollBodyPanel.addKeyPressHandler(self.navKeyPressHandler)
        else:
            self._scrollBodyPanel.addKeyDownHandler(self.navKeyDownHandler)
        self._scrollBodyPanel.addKeyUpHandler(self.navKeyUpHandler)
        self._scrollBodyPanel.sinkEvents(Event.TOUCHEVENTS)

        class _3_(TouchStartHandler):

            def onTouchStart(self, event):
                VScrollTable_this.getTouchScrollDelegate().onTouchStart(event)

        _3_ = _3_()
        self._scrollBodyPanel.addDomHandler(_3_, TouchStartEvent.getType())
        self._scrollBodyPanel.sinkEvents(Event.ONCONTEXTMENU)

        class _4_(ContextMenuHandler):

            def onContextMenu(self, event):
                VScrollTable_this.handleBodyContextMenu(event)

        _4_ = _4_()
        self._scrollBodyPanel.addDomHandler(_4_, ContextMenuEvent.getType())
        self.setStyleName(self.CLASSNAME)
        self.add(self.tHead)
        self.add(self._scrollBodyPanel)
        self.add(self._tFoot)
        self._rowRequestHandler = self.RowRequestHandler()

    def getTouchScrollDelegate(self):
        if self._touchScrollDelegate is None:
            self._touchScrollDelegate = TouchScrollDelegate(self._scrollBodyPanel.getElement())
        return self._touchScrollDelegate

    def handleBodyContextMenu(self, event):
        if self._enabled and self._bodyActionKeys is not None:
            left = Util.getTouchOrMouseClientX(event.getNativeEvent())
            top = Util.getTouchOrMouseClientY(event.getNativeEvent())
            top += Window.getScrollTop()
            left += Window.getScrollLeft()
            self.client.getContextMenu().showAt(self, left, top)
            # Only prevent browser context menu if there are action handlers
            # registered
            event.stopPropagation()
            event.preventDefault()

    def fireColumnResizeEvent(self, columnId, originalWidth, newWidth):
        """Fires a column resize event which sends the resize information to the
        server.

        @param columnId
                   The columnId of the column which was resized
        @param originalWidth
                   The width in pixels of the column before the resize event
        @param newWidth
                   The width in pixels of the column after the resize event
        """
        self.client.updateVariable(self.paintableId, 'columnResizeEventColumn', columnId, False)
        self.client.updateVariable(self.paintableId, 'columnResizeEventPrev', originalWidth, False)
        self.client.updateVariable(self.paintableId, 'columnResizeEventCurr', newWidth, self._immediate)

    def sendColumnWidthUpdates(self, columns):
        """Non-immediate variable update of column widths for a collection of
        columns.

        @param columns
                   the columns to trigger the events for.
        """
        newSizes = [None] * len(columns)
        ix = 0
        for cell in columns:
            newSizes[POSTINC(globals(), locals(), 'ix')] = cell.getColKey() + ':' + cell.getWidth()
        self.client.updateVariable(self.paintableId, 'columnWidthUpdates', newSizes, False)

    def moveFocusDown(self, *args):
        """Moves the focus one step down

        @return Returns true if succeeded
        ---
        Moves the focus down by 1+offset rows

        @return Returns true if succeeded, else false if the selection could not
                be move downwards
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            return self.moveFocusDown(0)
        elif _1 == 1:
            offset, = _0
            if self.isSelectable():
                if self._focusedRow is None and self._scrollBody.hasNext():
                    # FIXME should focus first visible from top, not first rendered
                    # ??
                    return self.setRowFocus(self._scrollBody.next())
                else:
                    next = self.getNextRow(self._focusedRow, offset)
                    if next is not None:
                        return self.setRowFocus(next)
            return False
        else:
            raise ARGERROR(0, 1)

    def moveFocusUp(self, *args):
        """Moves the selection one step up

        @return Returns true if succeeded
        ---
        Moves the focus row upwards

        @return Returns true if succeeded, else false if the selection could not
                be move upwards
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            return self.moveFocusUp(0)
        elif _1 == 1:
            offset, = _0
            if self.isSelectable():
                if self._focusedRow is None and self._scrollBody.hasNext():
                    # FIXME logic is exactly the same as in moveFocusDown, should
                    # be the opposite??
                    return self.setRowFocus(self._scrollBody.next())
                else:
                    prev = self.getPreviousRow(self._focusedRow, offset)
                    if prev is not None:
                        return self.setRowFocus(prev)
                    else:
                        VConsole.log('no previous available')
            return False
        else:
            raise ARGERROR(0, 1)

    def selectFocusedRow(self, ctrlSelect, shiftSelect):
        """Selects a row where the current selection head is

        @param ctrlSelect
                   Is the selection a ctrl+selection
        @param shiftSelect
                   Is the selection a shift+selection
        @return Returns truw
        """
        if self._focusedRow is not None:
            # Arrows moves the selection and clears previous selections
            if self.isSelectable() and not ctrlSelect and not shiftSelect:
                self.deselectAll()
                self._focusedRow.toggleSelection()
                self._selectionRangeStart = self._focusedRow
            elif self.isSelectable() and ctrlSelect and not shiftSelect:
                # Ctrl+arrows moves selection head
                self._selectionRangeStart = self._focusedRow
                # No selection, only selection head is moved
            elif self.isMultiSelectModeAny() and not ctrlSelect and shiftSelect:
                # Shift+arrows selection selects a range
                self._focusedRow.toggleShiftSelection(shiftSelect)

    def sendSelectedRows(self, *args):
        """Sends the selection to the server if changed since the last update/visit.
        ---
        Sends the selection to the server if it has been changed since the last
        update/visit.

        @param immediately
                   set to true to immediately send the rows
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.sendSelectedRows(self._immediate)
        elif _1 == 1:
            immediately, = _0
            if not self._selectionChanged:
                return
            # Reset selection changed flag
            self._selectionChanged = False
            # Note: changing the immediateness of this might require changes to
            # "clickEvent" immediateness also.
            if self.isMultiSelectModeDefault():
                # Convert ranges to a set of strings
                ranges = set()
                for range in self._selectedRowRanges:
                    ranges.add(str(range))
                # Send the selected row ranges
                self.client.updateVariable(self.paintableId, 'selectedRanges', list([None] * len(self._selectedRowRanges)), False)
                # clean selectedRowKeys so that they don't contain excess values
                _0 = True
                iterator = self._selectedRowKeys
                while True:
                    if _0 is True:
                        _0 = False
                    if not iterator.hasNext():
                        break
                    key = iterator.next()
                    renderedRowByKey = self.getRenderedRowByKey(key)
                    if renderedRowByKey is not None:
                        for range in self._selectedRowRanges:
                            if range.inRange(renderedRowByKey):
                                iterator.remove()
                    else:
                        # orphaned selected key, must be in a range, ignore
                        iterator.remove()
            # Send the selected rows
            self.client.updateVariable(self.paintableId, 'selected', list([None] * len(self._selectedRowKeys)), immediately)
        else:
            raise ARGERROR(0, 1)

    # Don't send anything if selection has not changed

    def getNavigationUpKey(self):
        """Get the key that moves the selection head upwards. By default it is the
        up arrow key but by overriding this you can change the key to whatever
        you want.

        @return The keycode of the key
        """
        return KeyCodes.KEY_UP

    def getNavigationDownKey(self):
        """Get the key that moves the selection head downwards. By default it is the
        down arrow key but by overriding this you can change the key to whatever
        you want.

        @return The keycode of the key
        """
        return KeyCodes.KEY_DOWN

    def getNavigationLeftKey(self):
        """Get the key that scrolls to the left in the table. By default it is the
        left arrow key but by overriding this you can change the key to whatever
        you want.

        @return The keycode of the key
        """
        return KeyCodes.KEY_LEFT

    def getNavigationRightKey(self):
        """Get the key that scroll to the right on the table. By default it is the
        right arrow key but by overriding this you can change the key to whatever
        you want.

        @return The keycode of the key
        """
        return KeyCodes.KEY_RIGHT

    def getNavigationSelectKey(self):
        """Get the key that selects an item in the table. By default it is the space
        bar key but by overriding this you can change the key to whatever you
        want.

        @return
        """
        return self._CHARCODE_SPACE

    def getNavigationPageUpKey(self):
        """Get the key the moves the selection one page up in the table. By default
        this is the Page Up key but by overriding this you can change the key to
        whatever you want.

        @return
        """
        return KeyCodes.KEY_PAGEUP

    def getNavigationPageDownKey(self):
        """Get the key the moves the selection one page down in the table. By
        default this is the Page Down key but by overriding this you can change
        the key to whatever you want.

        @return
        """
        return KeyCodes.KEY_PAGEDOWN

    def getNavigationStartKey(self):
        """Get the key the moves the selection to the beginning of the table. By
        default this is the Home key but by overriding this you can change the
        key to whatever you want.

        @return
        """
        return KeyCodes.KEY_HOME

    def getNavigationEndKey(self):
        """Get the key the moves the selection to the end of the table. By default
        this is the End key but by overriding this you can change the key to
        whatever you want.

        @return
        """
        # (non-Javadoc)
        # 
        # @see
        # com.vaadin.terminal.gwt.client.Paintable#updateFromUIDL(com.vaadin.terminal
        # .gwt.client.UIDL, com.vaadin.terminal.gwt.client.ApplicationConnection)

        return KeyCodes.KEY_END

    def updateFromUIDL(self, uidl, client):
        self._rendering = True
        if uidl.hasAttribute(self.ATTRIBUTE_PAGEBUFFER_FIRST):
            self._serverCacheFirst = uidl.getIntAttribute(self.ATTRIBUTE_PAGEBUFFER_FIRST)
            self._serverCacheLast = uidl.getIntAttribute(self.ATTRIBUTE_PAGEBUFFER_LAST)
        else:
            self._serverCacheFirst = -1
            self._serverCacheLast = -1
        # We need to do this before updateComponent since updateComponent calls
        # this.setHeight() which will calculate a new body height depending on
        # the space available.

        if uidl.hasAttribute('colfooters'):
            self._showColFooters = uidl.getBooleanAttribute('colfooters')
        self._tFoot.setVisible(self._showColFooters)
        if client.updateComponent(self, uidl, True):
            self._rendering = False
            return
        self._enabled = not uidl.hasAttribute('disabled')
        if BrowserInfo.get().isIE8() and not self._enabled:
            # The disabled shim will not cover the table body if it is relative
            # in IE8. See #7324

            self._scrollBodyPanel.getElement().getStyle().setPosition(Position.STATIC)
        elif BrowserInfo.get().isIE8():
            self._scrollBodyPanel.getElement().getStyle().setPosition(Position.RELATIVE)
        self.client = client
        self.paintableId = uidl.getStringAttribute('id')
        self._immediate = uidl.getBooleanAttribute('immediate')
        previousTotalRows = self._totalRows
        self.updateTotalRows(uidl)
        totalRowsChanged = self._totalRows != previousTotalRows
        self.updateDragMode(uidl)
        self.updateSelectionProperties(uidl)
        if uidl.hasAttribute('alb'):
            self._bodyActionKeys = uidl.getStringArrayAttribute('alb')
        else:
            # Need to clear the actions if the action handlers have been
            # removed
            self._bodyActionKeys = None
        self.setCacheRateFromUIDL(uidl)
        self._recalcWidths = uidl.hasAttribute('recalcWidths')
        if self._recalcWidths:
            self.tHead.clear()
            self._tFoot.clear()
        self.updatePageLength(uidl)
        self.updateFirstVisibleAndScrollIfNeeded(uidl)
        self.showRowHeaders = uidl.getBooleanAttribute('rowheaders')
        self._showColHeaders = uidl.getBooleanAttribute('colheaders')
        self.updateSortingProperties(uidl)
        keyboardSelectionOverRowFetchInProgress = self.selectSelectedRows(uidl)
        self.updateActionMap(uidl)
        self.updateColumnProperties(uidl)
        ac = uidl.getChildByTagName('-ac')
        if ac is None:
            if self._dropHandler is not None:
                # remove dropHandler if not present anymore
                self._dropHandler = None
        else:
            if self._dropHandler is None:
                self._dropHandler = self.VScrollTableDropHandler()
            self._dropHandler.updateAcceptRules(ac)
        partialRowAdditions = uidl.getChildByTagName('prows')
        partialRowUpdates = uidl.getChildByTagName('urows')
        if (partialRowUpdates is not None) or (partialRowAdditions is not None):
            # we may have pending cache row fetch, cancel it. See #2136
            self._rowRequestHandler.cancel()
            self.updateRowsInBody(partialRowUpdates)
            self.addAndRemoveRows(partialRowAdditions)
        else:
            rowData = uidl.getChildByTagName('rows')
            if rowData is not None:
                # we may have pending cache row fetch, cancel it. See #2136
                self._rowRequestHandler.cancel()
                if not self._recalcWidths and self._initializedAndAttached:
                    self.updateBody(rowData, uidl.getIntAttribute('firstrow'), uidl.getIntAttribute('rows'))
                    if self._headerChangedDuringUpdate:
                        self.triggerLazyColumnAdjustment(True)
                    elif (
                        ((not self.isScrollPositionVisible()) or totalRowsChanged) or (self._lastRenderedHeight != self._scrollBody.getOffsetHeight())
                    ):
                        # webkits may still bug with their disturbing scrollbar
                        # bug, see #3457
                        # Run overflow fix for the scrollable area
                        # #6698 - If there's a scroll going on, don't abort it
                        # by changing overflows as the length of the contents
                        # *shouldn't* have changed (unless the number of rows
                        # or the height of the widget has also changed)

                        class _5_(Command):

                            def execute(self):
                                Util.runWebkitOverflowAutoFix(VScrollTable_this._scrollBodyPanel.getElement())

                        _5_ = _5_()
                        Scheduler.get().scheduleDeferred(_5_)
                else:
                    self.initializeRows(uidl, rowData)
        if not self.isSelectable():
            self._scrollBody.addStyleName(self.CLASSNAME + '-body-noselection')
        else:
            self._scrollBody.removeStyleName(self.CLASSNAME + '-body-noselection')
        self.hideScrollPositionAnnotation()
        self.purgeUnregistryBag()
        # selection is no in sync with server, avoid excessive server visits by
        # clearing to flag used during the normal operation
        if not keyboardSelectionOverRowFetchInProgress:
            self._selectionChanged = False
        # This is called when the Home or page up button has been pressed in
        # selectable mode and the next selected row was not yet rendered in the
        # client

        if self._selectFirstItemInNextRender or self._focusFirstItemInNextRender:
            self.selectFirstRenderedRowInViewPort(self._focusFirstItemInNextRender)
            self._selectFirstItemInNextRender = self._focusFirstItemInNextRender = False
        # This is called when the page down or end button has been pressed in
        # selectable mode and the next selected row was not yet rendered in the
        # client

        if self._selectLastItemInNextRender or self._focusLastItemInNextRender:
            self.selectLastRenderedRowInViewPort(self._focusLastItemInNextRender)
            self._selectLastItemInNextRender = self._focusLastItemInNextRender = False
        self._multiselectPending = False
        if self._focusedRow is not None:
            if (
                not self._focusedRow.isAttached() and not self._rowRequestHandler.isRunning()
            ):
                # focused row has been orphaned, can't focus
                self.focusRowFromBody()
        self._tabIndex = uidl.getIntAttribute('tabindex') if uidl.hasAttribute('tabindex') else 0
        self.setProperTabIndex()
        self.resizeSortedColumnForSortIndicator()
        # Remember this to detect situations where overflow hack might be
        # needed during scrolling
        self._lastRenderedHeight = self._scrollBody.getOffsetHeight()
        self._rendering = False
        self._headerChangedDuringUpdate = False

    def initializeRows(self, uidl, rowData):
        if self._scrollBody is not None:
            self._scrollBody.removeFromParent()
            self._lazyUnregistryBag.add(self._scrollBody)
        self._scrollBody = self.createScrollBody()
        self._scrollBody.renderInitialRows(rowData, uidl.getIntAttribute('firstrow'), uidl.getIntAttribute('rows'))
        self._scrollBodyPanel.add(self._scrollBody)
        # New body starts scrolled to the left, make sure the header and footer
        # are also scrolled to the left
        self.tHead.setHorizontalScrollPosition(0)
        self._tFoot.setHorizontalScrollPosition(0)
        self._initialContentReceived = True
        if self.isAttached():
            self.sizeInit()
        self._scrollBody.restoreRowVisibility()

    def updateColumnProperties(self, uidl):
        self.updateColumnOrder(uidl)
        self.updateCollapsedColumns(uidl)
        vc = uidl.getChildByTagName('visiblecolumns')
        if vc is not None:
            self.tHead.updateCellsFromUIDL(vc)
            self._tFoot.updateCellsFromUIDL(vc)
        self.updateHeader(uidl.getStringArrayAttribute('vcolorder'))
        self.updateFooter(uidl.getStringArrayAttribute('vcolorder'))

    def updateCollapsedColumns(self, uidl):
        if uidl.hasVariable('collapsedcolumns'):
            self.tHead.setColumnCollapsingAllowed(True)
            self._collapsedColumns = uidl.getStringArrayVariableAsSet('collapsedcolumns')
        else:
            self.tHead.setColumnCollapsingAllowed(False)

    def updateColumnOrder(self, uidl):
        if uidl.hasVariable('columnorder'):
            self._columnReordering = True
            self._columnOrder = uidl.getStringArrayVariable('columnorder')
        else:
            self._columnReordering = False
            self._columnOrder = None

    def selectSelectedRows(self, uidl):
        keyboardSelectionOverRowFetchInProgress = False
        if uidl.hasVariable('selected'):
            selectedKeys = uidl.getStringArrayVariableAsSet('selected')
            if self._scrollBody is not None:
                iterator = self._scrollBody
                while iterator.hasNext():
                    # Make the focus reflect to the server side state unless we
                    # are currently selecting multiple rows with keyboard.

                    row = iterator.next()
                    selected = row.getKey() in selectedKeys
                    if (
                        not selected and self._unSyncedselectionsBeforeRowFetch is not None and row.getKey() in self._unSyncedselectionsBeforeRowFetch
                    ):
                        selected = True
                        keyboardSelectionOverRowFetchInProgress = True
                    if selected != row.isSelected():
                        row.toggleSelection()
        self._unSyncedselectionsBeforeRowFetch = None
        return keyboardSelectionOverRowFetchInProgress

    def updateSortingProperties(self, uidl):
        self._oldSortColumn = self._sortColumn
        if uidl.hasVariable('sortascending'):
            self._sortAscending = uidl.getBooleanVariable('sortascending')
            self._sortColumn = uidl.getStringVariable('sortcolumn')

    def resizeSortedColumnForSortIndicator(self):
        # Force recalculation of the captionContainer element inside the header
        # cell to accomodate for the size of the sort arrow.
        sortedHeader = self.tHead.getHeaderCell(self._sortColumn)
        if sortedHeader is not None:
            self.tHead.resizeCaptionContainer(sortedHeader)
        # Also recalculate the width of the captionContainer element in the
        # previously sorted header, since this now has more room.
        oldSortedHeader = self.tHead.getHeaderCell(self._oldSortColumn)
        if oldSortedHeader is not None:
            self.tHead.resizeCaptionContainer(oldSortedHeader)

    def updateFirstVisibleAndScrollIfNeeded(self, uidl):
        self._firstvisible = uidl.getIntVariable('firstvisible') if uidl.hasVariable('firstvisible') else 0
        if (
            self._firstvisible != self._lastRequestedFirstvisible and self._scrollBody is not None
        ):
            # received 'surprising' firstvisible from server: scroll there
            self._firstRowInViewPort = self._firstvisible
            self._scrollBodyPanel.setScrollPosition(self.measureRowHeightOffset(self._firstvisible))

    def measureRowHeightOffset(self, rowIx):
        return rowIx * self._scrollBody.getRowHeight()

    def updatePageLength(self, *args):
        """None
        ---
        Determines the pagelength when the table height is fixed.
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            if (not self.isVisible()) or (not self._enabled):
                return
            if self._scrollBody is None:
                return
            if (self._height is None) or (self._height == ''):
                return
            rowHeight = self.Math.round(self._scrollBody.getRowHeight())
            bodyH = self._scrollBodyPanel.getOffsetHeight()
            rowsAtOnce = bodyH / rowHeight
            anotherPartlyVisible = bodyH % rowHeight != 0
            if anotherPartlyVisible:
                rowsAtOnce += 1
            if self._pageLength != rowsAtOnce:
                self._pageLength = rowsAtOnce
                self.client.updateVariable(self.paintableId, 'pagelength', self._pageLength, False)
                if not self._rendering:
                    currentlyVisible = self._scrollBody.lastRendered - self._scrollBody.firstRendered
                    if currentlyVisible < self._pageLength and currentlyVisible < self._totalRows:
                        # shake scrollpanel to fill empty space
                        self._scrollBodyPanel.setScrollPosition(self._scrollTop + 1)
                        self._scrollBodyPanel.setScrollPosition(self._scrollTop - 1)
        elif _1 == 1:
            uidl, = _0
            oldPageLength = self._pageLength
            if uidl.hasAttribute('pagelength'):
                self._pageLength = uidl.getIntAttribute('pagelength')
            else:
                # pagelenght is "0" meaning scrolling is turned off
                self._pageLength = self._totalRows
            if oldPageLength != self._pageLength and self._initializedAndAttached:
                # page length changed, need to update size
                self.sizeInit()
        else:
            raise ARGERROR(0, 1)

    def updateSelectionProperties(self, uidl):
        self.setMultiSelectMode(uidl.getIntAttribute('multiselectmode') if uidl.hasAttribute('multiselectmode') else self._MULTISELECT_MODE_DEFAULT)
        self._nullSelectionAllowed = uidl.getBooleanAttribute('nsa') if uidl.hasAttribute('nsa') else True
        if uidl.hasAttribute('selectmode'):
            if uidl.getBooleanAttribute('readonly'):
                self._selectMode = Table.SELECT_MODE_NONE
            elif uidl.getStringAttribute('selectmode') == 'multi':
                self._selectMode = Table.SELECT_MODE_MULTI
            elif uidl.getStringAttribute('selectmode') == 'single':
                self._selectMode = Table.SELECT_MODE_SINGLE
            else:
                self._selectMode = Table.SELECT_MODE_NONE

    def updateDragMode(self, uidl):
        self._dragmode = uidl.getIntAttribute('dragmode') if uidl.hasAttribute('dragmode') else 0
        if BrowserInfo.get().isIE():
            if self._dragmode > 0:
                self.getElement().setPropertyJSO('onselectstart', self.getPreventTextSelectionIEHack())
            else:
                self.getElement().setPropertyJSO('onselectstart', None)

    def updateTotalRows(self, uidl):
        newTotalRows = uidl.getIntAttribute('totalrows')
        if newTotalRows != self.getTotalRows():
            if self._scrollBody is not None:
                if self.getTotalRows() == 0:
                    self.tHead.clear()
                    self._tFoot.clear()
                self._initializedAndAttached = False
                self._initialContentReceived = False
                self._isNewBody = True
            self.setTotalRows(newTotalRows)

    def setTotalRows(self, newTotalRows):
        self._totalRows = newTotalRows

    def getTotalRows(self):
        return self._totalRows

    def focusRowFromBody(self):
        if len(self._selectedRowKeys) == 1:
            # try to focus a row currently selected and in viewport
            selectedRowKey = self._selectedRowKeys.next()
            if selectedRowKey is not None:
                renderedRow = self.getRenderedRowByKey(selectedRowKey)
                if (renderedRow is None) or (not renderedRow.isInViewPort()):
                    self.setRowFocus(self._scrollBody.getRowByRowIndex(self._firstRowInViewPort))
                else:
                    self.setRowFocus(renderedRow)
        else:
            # multiselect mode
            self.setRowFocus(self._scrollBody.getRowByRowIndex(self._firstRowInViewPort))

    def createScrollBody(self):
        return self.VScrollTableBody()

    def selectLastRenderedRowInViewPort(self, focusOnly):
        """Selects the last row visible in the table

        @param focusOnly
                   Should the focus only be moved to the last row
        """
        index = self._firstRowInViewPort + self.getFullyVisibleRowCount()
        lastRowInViewport = self._scrollBody.getRowByRowIndex(index)
        if lastRowInViewport is None:
            # this should not happen in normal situations (white space at the
            # end of viewport). Select the last rendered as a fallback.
            lastRowInViewport = self._scrollBody.getRowByRowIndex(self._scrollBody.getLastRendered())
            if lastRowInViewport is None:
                return
                # empty table
        self.setRowFocus(lastRowInViewport)
        if not focusOnly:
            self.selectFocusedRow(False, self._multiselectPending)
            self.sendSelectedRows()

    def selectFirstRenderedRowInViewPort(self, focusOnly):
        """Selects the first row visible in the table

        @param focusOnly
                   Should the focus only be moved to the first row
        """
        index = self._firstRowInViewPort
        firstInViewport = self._scrollBody.getRowByRowIndex(index)
        if firstInViewport is None:
            # this should not happen in normal situations
            return
        self.setRowFocus(firstInViewport)
        if not focusOnly:
            self.selectFocusedRow(False, self._multiselectPending)
            self.sendSelectedRows()

    def setCacheRateFromUIDL(self, uidl):
        self.setCacheRate(uidl.getDoubleAttribute('cr') if uidl.hasAttribute('cr') else self._CACHE_RATE_DEFAULT)

    def setCacheRate(self, d):
        if self._cache_rate != d:
            self._cache_rate = d
            self._cache_react_rate = 0.75 * d

    def purgeUnregistryBag(self):
        """Unregisters Paintables in "trashed" HasWidgets (IScrollTableBodys or
        IScrollTableRows). This is done lazily as Table must survive from
        "subtreecaching" logic.
        """
        _0 = True
        iterator = self._lazyUnregistryBag
        while True:
            if _0 is True:
                _0 = False
            if not iterator.hasNext():
                break
            self.client.unregisterChildPaintables(iterator.next())
        self._lazyUnregistryBag.clear()

    def updateActionMap(self, mainUidl):
        actionsUidl = mainUidl.getChildByTagName('actions')
        if actionsUidl is None:
            return
        it = actionsUidl.getChildIterator()
        while it.hasNext():
            action = it.next()
            key = action.getStringAttribute('key')
            caption = action.getStringAttribute('caption')
            self._actionMap.put(key + '_c', caption)
            if action.hasAttribute('icon'):
                # TODO need some uri handling ??
                self._actionMap.put(key + '_i', self.client.translateVaadinUri(action.getStringAttribute('icon')))
            else:
                self._actionMap.remove(key + '_i')

    def getActionCaption(self, actionKey):
        return self._actionMap[actionKey + '_c']

    def getActionIcon(self, actionKey):
        return self._actionMap[actionKey + '_i']

    def updateHeader(self, strings):
        if strings is None:
            return
        visibleCols = len(strings)
        colIndex = 0
        if self.showRowHeaders:
            self.tHead.enableColumn(self._ROW_HEADER_COLUMN_KEY, colIndex)
            visibleCols += 1
            self._visibleColOrder = [None] * visibleCols
            self._visibleColOrder[colIndex] = self._ROW_HEADER_COLUMN_KEY
            colIndex += 1
        else:
            self._visibleColOrder = [None] * visibleCols
            self.tHead.removeCell(self._ROW_HEADER_COLUMN_KEY)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(strings)):
                break
            cid = strings[i]
            self._visibleColOrder[colIndex] = cid
            self.tHead.enableColumn(cid, colIndex)
            colIndex += 1
        self.tHead.setVisible(self._showColHeaders)
        self.setContainerHeight()

    def updateFooter(self, strings):
        """Updates footers.
        <p>
        Update headers whould be called before this method is called!
        </p>

        @param strings
        """
        if strings is None:
            return
        # Add dummy column if row headers are present
        colIndex = 0
        if self.showRowHeaders:
            self._tFoot.enableColumn(self._ROW_HEADER_COLUMN_KEY, colIndex)
            colIndex += 1
        else:
            self._tFoot.removeCell(self._ROW_HEADER_COLUMN_KEY)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(strings)):
                break
            cid = strings[i]
            self._tFoot.enableColumn(cid, colIndex)
            colIndex += 1
        self._tFoot.setVisible(self._showColFooters)

    def updateBody(self, uidl, firstRow, reqRows):
        """@param uidl
                   which contains row data
        @param firstRow
                   first row in data set
        @param reqRows
                   amount of rows in data set
        """
        if (uidl is None) or (reqRows < 1):
            # container is empty, remove possibly existing rows
            if firstRow <= 0:
                while self._scrollBody.getLastRendered() > self._scrollBody.firstRendered:
                    self._scrollBody.unlinkRow(False)
                self._scrollBody.unlinkRow(False)
            return
        self._scrollBody.renderRows(uidl, firstRow, reqRows)
        self.discardRowsOutsideCacheWindow()

    def updateRowsInBody(self, partialRowUpdates):
        if partialRowUpdates is None:
            return
        firstRowIx = partialRowUpdates.getIntAttribute('firsturowix')
        count = partialRowUpdates.getIntAttribute('numurows')
        self._scrollBody.unlinkRows(firstRowIx, count)
        self._scrollBody.insertRows(partialRowUpdates, firstRowIx, count)

    def discardRowsOutsideCacheWindow(self):
        """Updates the internal cache by unlinking rows that fall outside of the
        caching window.
        """
        firstRowToKeep = self._firstRowInViewPort - (self._pageLength * self._cache_rate)
        lastRowToKeep = self._firstRowInViewPort + self._pageLength + (self._pageLength * self._cache_rate)
        self.debug('Client side calculated cache rows to keep: ' + firstRowToKeep + '-' + lastRowToKeep)
        if self._serverCacheFirst != -1:
            firstRowToKeep = self._serverCacheFirst
            lastRowToKeep = self._serverCacheLast
            self.debug('Server cache rows that override: ' + self._serverCacheFirst + '-' + self._serverCacheLast)
            if (
                (firstRowToKeep < self._scrollBody.getFirstRendered()) or (lastRowToKeep > self._scrollBody.getLastRendered())
            ):
                self.debug('*** Server wants us to keep ' + self._serverCacheFirst + '-' + self._serverCacheLast + ' but we only have rows ' + self._scrollBody.getFirstRendered() + '-' + self._scrollBody.getLastRendered() + ' rendered!')
        self.discardRowsOutsideOf(firstRowToKeep, lastRowToKeep)
        self._scrollBody.fixSpacers()
        self._scrollBody.restoreRowVisibility()

    def discardRowsOutsideOf(self, optimalFirstRow, optimalLastRow):
        # firstDiscarded and lastDiscarded are only calculated for debug
        # purposes

        firstDiscarded = -1
        lastDiscarded = -1
        cont = True
        while (
            cont and self._scrollBody.getLastRendered() > optimalFirstRow and self._scrollBody.getFirstRendered() < optimalFirstRow
        ):
            if firstDiscarded == -1:
                firstDiscarded = self._scrollBody.getFirstRendered()
            # removing row from start
            cont = self._scrollBody.unlinkRow(True)
        if firstDiscarded != -1:
            lastDiscarded = self._scrollBody.getFirstRendered() - 1
            self.debug('Discarded rows ' + firstDiscarded + '-' + lastDiscarded)
        firstDiscarded = lastDiscarded = -1
        cont = True
        while cont and self._scrollBody.getLastRendered() > optimalLastRow:
            if lastDiscarded == -1:
                lastDiscarded = self._scrollBody.getLastRendered()
            # removing row from the end
            cont = self._scrollBody.unlinkRow(False)
        if lastDiscarded != -1:
            firstDiscarded = self._scrollBody.getLastRendered() + 1
            self.debug('Discarded rows ' + firstDiscarded + '-' + lastDiscarded)
        self.debug('Now in cache: ' + self._scrollBody.getFirstRendered() + '-' + self._scrollBody.getLastRendered())

    def addAndRemoveRows(self, partialRowAdditions):
        """Inserts rows in the table body or removes them from the table body based
        on the commands in the UIDL.

        @param partialRowAdditions
                   the UIDL containing row updates.
        """
        if partialRowAdditions is None:
            return
        if partialRowAdditions.hasAttribute('hide'):
            self._scrollBody.unlinkAndReindexRows(partialRowAdditions.getIntAttribute('firstprowix'), partialRowAdditions.getIntAttribute('numprows'))
            self._scrollBody.ensureCacheFilled()
        elif partialRowAdditions.hasAttribute('delbelow'):
            self._scrollBody.insertRowsDeleteBelow(partialRowAdditions, partialRowAdditions.getIntAttribute('firstprowix'), partialRowAdditions.getIntAttribute('numprows'))
        else:
            self._scrollBody.insertAndReindexRows(partialRowAdditions, partialRowAdditions.getIntAttribute('firstprowix'), partialRowAdditions.getIntAttribute('numprows'))
        self.discardRowsOutsideCacheWindow()

    def getColIndexByKey(self, colKey):
        """Gives correct column index for given column key ("cid" in UIDL).

        @param colKey
        @return column index of visible columns, -1 if column not visible
        """
        # return 0 if asked for rowHeaders
        if self._ROW_HEADER_COLUMN_KEY == colKey:
            return 0
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(self._visibleColOrder)):
                break
            if self._visibleColOrder[i] == colKey:
                return i
        return -1

    def isMultiSelectModeSimple(self):
        return self._selectMode == Table.SELECT_MODE_MULTI and self._multiselectmode == self._MULTISELECT_MODE_SIMPLE

    def isSingleSelectMode(self):
        return self._selectMode == Table.SELECT_MODE_SINGLE

    def isMultiSelectModeAny(self):
        return self._selectMode == Table.SELECT_MODE_MULTI

    def isMultiSelectModeDefault(self):
        return self._selectMode == Table.SELECT_MODE_MULTI and self._multiselectmode == self._MULTISELECT_MODE_DEFAULT

    def setMultiSelectMode(self, multiselectmode):
        if BrowserInfo.get().isTouchDevice():
            # Always use the simple mode for touch devices that do not have
            # shift/ctrl keys
            self._multiselectmode = self._MULTISELECT_MODE_SIMPLE
        else:
            self._multiselectmode = multiselectmode

    def isSelectable(self):
        return self._selectMode > Table.SELECT_MODE_NONE

    def isCollapsedColumn(self, colKey):
        if self._collapsedColumns is None:
            return False
        if colKey in self._collapsedColumns:
            return True
        return False

    def getColKeyByIndex(self, index):
        return self.tHead.getHeaderCell(index).getColKey()

    def setColWidth(self, colIndex, w, isDefinedWidth):
        hcell = self.tHead.getHeaderCell(colIndex)
        # Make sure that the column grows to accommodate the sort indicator if
        # necessary.
        if w < hcell.getMinWidth():
            w = hcell.getMinWidth()
        # Set header column width
        hcell.setWidth(w, isDefinedWidth)
        # Ensure indicators have been taken into account
        self.tHead.resizeCaptionContainer(hcell)
        # Set body column width
        self._scrollBody.setColWidth(colIndex, w)
        # Set footer column width
        fcell = self._tFoot.getFooterCell(colIndex)
        fcell.setWidth(w, isDefinedWidth)

    def getColWidth(self, colKey):
        return self.tHead.getHeaderCell(colKey).getWidth()

    def getRenderedRowByKey(self, key):
        """Get a rendered row by its key

        @param key
                   The key to search with
        @return
        """
        if self._scrollBody is not None:
            it = self._scrollBody
            r = None
            while it.hasNext():
                r = it.next()
                if r.getKey() == key:
                    return r
        return None

    def getNextRow(self, row, offset):
        """Returns the next row to the given row

        @param row
                   The row to calculate from

        @return The next row or null if no row exists
        """
        it = self._scrollBody
        r = None
        while it.hasNext():
            r = it.next()
            if r == row:
                r = None
                while offset >= 0 and it.hasNext():
                    r = it.next()
                    offset -= 1
                return r
        return None

    def getPreviousRow(self, row, offset):
        """Returns the previous row from the given row

        @param row
                   The row to calculate from
        @return The previous row or null if no row exists
        """
        it = self._scrollBody
        offsetIt = self._scrollBody
        r = None
        prev = None
        while it.hasNext():
            r = it.next()
            if offset < 0:
                prev = offsetIt.next()
            if r == row:
                return prev
            offset -= 1
        return None

    def reOrderColumn(self, columnKey, newIndex):
        oldIndex = self.getColIndexByKey(columnKey)
        # Change header order
        self.tHead.moveCell(oldIndex, newIndex)
        # Change body order
        self._scrollBody.moveCol(oldIndex, newIndex)
        # Change footer order
        self._tFoot.moveCell(oldIndex, newIndex)
        # Build new columnOrder and update it to server Note that columnOrder
        # also contains collapsed columns so we cannot directly build it from
        # cells vector Loop the old columnOrder and append in order to new
        # array unless on moved columnKey. On new index also put the moved key
        # i == index on columnOrder, j == index on newOrder

        oldKeyOnNewIndex = self._visibleColOrder[newIndex]
        if self.showRowHeaders:
            newIndex -= 1
        # add back hidden rows,
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(self._columnOrder)):
                break
            if self._columnOrder[i] == oldKeyOnNewIndex:
                break
                # break loop at target
            if self.isCollapsedColumn(self._columnOrder[i]):
                newIndex += 1
        # finally we can build the new columnOrder for server
        newOrder = [None] * len(self._columnOrder)
        _1 = True
        i = 0
        j = 0
        while True:
            if _1 is True:
                _1 = False
            else:
                i += 1
            if not (j < len(newOrder)):
                break
            if j == newIndex:
                newOrder[j] = columnKey
                j += 1
            if i == len(self._columnOrder):
                break
            if self._columnOrder[i] == columnKey:
                continue
            newOrder[j] = self._columnOrder[i]
            j += 1
        self._columnOrder = newOrder
        # also update visibleColumnOrder
        i = 1 if self.showRowHeaders else 0
        _2 = True
        j = 0
        while True:
            if _2 is True:
                _2 = False
            else:
                j += 1
            if not (j < len(newOrder)):
                break
            cid = newOrder[j]
            if not self.isCollapsedColumn(cid):
                self._visibleColOrder[POSTINC(globals(), locals(), 'i')] = cid
        self.client.updateVariable(self.paintableId, 'columnorder', self._columnOrder, False)
        if self.client.hasEventListeners(self, self.COLUMN_REORDER_EVENT_ID):
            self.client.sendPendingVariableChanges()

    def onAttach(self):
        super(VScrollTable, self).onAttach()
        if self._initialContentReceived:
            self.sizeInit()

    def onDetach(self):
        self._rowRequestHandler.cancel()
        super(VScrollTable, self).onDetach()
        # ensure that scrollPosElement will be detached
        if self._scrollPositionElement is not None:
            parent = DOM.getParent(self._scrollPositionElement)
            if parent is not None:
                DOM.removeChild(parent, self._scrollPositionElement)

    def sizeInit(self):
        """Run only once when component is attached and received its initial
        content. This function:

        * Syncs headers and bodys "natural widths and saves the values.

        * Sets proper width and height

        * Makes deferred request to get some cache rows
        """
        # We will use browsers table rendering algorithm to find proper column
        # widths. If content and header take less space than available, we will
        # divide extra space relatively to each column which has not width set.
        # 
        # Overflow pixels are added to last column.

        headCells = self.tHead
        footCells = self._tFoot
        i = 0
        totalExplicitColumnsWidths = 0
        total = 0
        expandRatioDivider = 0
        widths = [None] * len(self.tHead.visibleCells)
        self.tHead.enableBrowserIntelligence()
        self._tFoot.enableBrowserIntelligence()
        # first loop: collect natural widths
        while headCells.hasNext():
            hCell = headCells.next()
            fCell = footCells.next()
            w = hCell.getWidth()
            if hCell.isDefinedWidth():
                # server has defined column width explicitly
                totalExplicitColumnsWidths += w
            else:
                if hCell.getExpandRatio() > 0:
                    expandRatioDivider += hCell.getExpandRatio()
                    w = 0
                else:
                    # get and store greater of header width and column width,
                    # and
                    # store it as a minimumn natural col width
                    headerWidth = hCell.getNaturalColumnWidth(i)
                    footerWidth = fCell.getNaturalColumnWidth(i)
                    w = headerWidth if headerWidth > footerWidth else footerWidth
                hCell.setNaturalMinimumColumnWidth(w)
                fCell.setNaturalMinimumColumnWidth(w)
            widths[i] = w
            total += w
            i += 1
        self.tHead.disableBrowserIntelligence()
        self._tFoot.disableBrowserIntelligence()
        willHaveScrollbarz = self.willHaveScrollbars()
        # fix "natural" width if width not set
        if (self._width is None) or ('' == self._width):
            w = total
            w += self._scrollBody.getCellExtraWidth() * len(self._visibleColOrder)
            if willHaveScrollbarz:
                w += Util.getNativeScrollbarSize()
            self.setContentWidth(w)
        availW = self._scrollBody.getAvailableWidth()
        if BrowserInfo.get().isIE():
            # Hey IE, are you really sure about this?
            availW = self._scrollBody.getAvailableWidth()
        availW -= self._scrollBody.getCellExtraWidth() * len(self._visibleColOrder)
        if willHaveScrollbarz:
            availW -= Util.getNativeScrollbarSize()
        # TODO refactor this code to be the same as in resize timer
        needsReLayout = False
        if availW > total:
            # natural size is smaller than available space
            extraSpace = availW - total
            totalWidthR = total - totalExplicitColumnsWidths
            checksum = 0
            needsReLayout = True
            if extraSpace == 1:
                # We cannot divide one single pixel so we give it the first
                # undefined column
                headCells = self.tHead
                i = 0
                checksum = availW
                while headCells.hasNext():
                    hc = headCells.next()
                    if not hc.isDefinedWidth():
                        widths[i] += 1
                        break
                    i += 1
            elif expandRatioDivider > 0:
                # visible columns have some active expand ratios, excess
                # space is divided according to them
                headCells = self.tHead
                i = 0
                while headCells.hasNext():
                    hCell = headCells.next()
                    if hCell.getExpandRatio() > 0:
                        w = widths[i]
                        newSpace = self.Math.round(extraSpace * (hCell.getExpandRatio() / expandRatioDivider))
                        w += newSpace
                        widths[i] = w
                    checksum += widths[i]
                    i += 1
            elif totalWidthR > 0:
                # no expand ratios defined, we will share extra space
                # relatively to "natural widths" among those without
                # explicit width
                headCells = self.tHead
                i = 0
                while headCells.hasNext():
                    hCell = headCells.next()
                    if not hCell.isDefinedWidth():
                        w = widths[i]
                        newSpace = self.Math.round((extraSpace * w) / totalWidthR)
                        w += newSpace
                        widths[i] = w
                    checksum += widths[i]
                    i += 1
            if extraSpace > 0 and checksum != availW:
                # There might be in some cases a rounding error of 1px when
                # extra space is divided so if there is one then we give the
                # first undefined column 1 more pixel

                headCells = self.tHead
                i = 0
                while headCells.hasNext():
                    hc = headCells.next()
                    if not hc.isDefinedWidth():
                        widths[i] += availW - checksum
                        break
                    i += 1
        else:
            # bodys size will be more than available and scrollbar will appear
            pass
        # last loop: set possibly modified values or reset if new tBody
        i = 0
        headCells = self.tHead
        while headCells.hasNext():
            hCell = headCells.next()
            if self._isNewBody or (hCell.getWidth() == -1):
                w = widths[i]
                self.setColWidth(i, w, False)
            i += 1
        self._initializedAndAttached = True
        if needsReLayout:
            self._scrollBody.reLayoutComponents()
        self.updatePageLength()
        # Fix "natural" height if height is not set. This must be after width
        # fixing so the components' widths have been adjusted.

        if (self._height is None) or ('' == self._height):
            # We must force an update of the row height as this point as it
            # might have been (incorrectly) calculated earlier

            if self._pageLength == self._totalRows:
                # A hack to support variable height rows when paging is off.
                # Generally this is not supported by scrolltable. We want to
                # show all rows so the bodyHeight should be equal to the table
                # height.

                # int bodyHeight = scrollBody.getOffsetHeight();
                bodyHeight = self._scrollBody.getRequiredHeight()
            else:
                bodyHeight = self.Math.round(self._scrollBody.getRowHeight(True) * self._pageLength)
            needsSpaceForHorizontalSrollbar = total > availW
            if needsSpaceForHorizontalSrollbar:
                bodyHeight += Util.getNativeScrollbarSize()
            self._scrollBodyPanel.setHeight(bodyHeight + 'px')
            Util.runWebkitOverflowAutoFix(self._scrollBodyPanel.getElement())
        self._isNewBody = False
        if self._firstvisible > 0:
            # Deferred due some Firefox oddities. IE & Safari could survive
            # without

            class _6_(Command):

                def execute(self):
                    VScrollTable_this._scrollBodyPanel.setScrollPosition(VScrollTable_this.measureRowHeightOffset(VScrollTable_this._firstvisible))
                    VScrollTable_this._firstRowInViewPort = VScrollTable_this._firstvisible

            _6_ = _6_()
            Scheduler.get().scheduleDeferred(_6_)
        if self._enabled:
            # Do we need cache rows
            if (
                self._scrollBody.getLastRendered() + 1 < self._firstRowInViewPort + self._pageLength + (self._cache_react_rate * self._pageLength)
            ):
                if self._totalRows - 1 > self._scrollBody.getLastRendered():
                    # fetch cache rows
                    firstInNewSet = self._scrollBody.getLastRendered() + 1
                    self._rowRequestHandler.setReqFirstRow(firstInNewSet)
                    lastInNewSet = self._firstRowInViewPort + self._pageLength + (self._cache_rate * self._pageLength)
                    if lastInNewSet > self._totalRows - 1:
                        lastInNewSet = self._totalRows - 1
                    self._rowRequestHandler.setReqRows((lastInNewSet - firstInNewSet) + 1)
                    self._rowRequestHandler.deferRowFetch(1)
        # Ensures the column alignments are correct at initial loading. <br/>
        # (child components widths are correct)

        self._scrollBody.reLayoutComponents()

        class _7_(Command):

            def execute(self):
                Util.runWebkitOverflowAutoFix(VScrollTable_this._scrollBodyPanel.getElement())

        _7_ = _7_()
        Scheduler.get().scheduleDeferred(_7_)

    def willHaveScrollbars(self):
        """Note, this method is not official api although declared as protected.
        Extend at you own risk.

        @return true if content area will have scrollbars visible.
        """
        if not (self._height is not None and not (self._height == '')):
            if self._pageLength < self._totalRows:
                return True
        else:
            fakeheight = self.Math.round(self._scrollBody.getRowHeight() * self._totalRows)
            availableHeight = self._scrollBodyPanel.getElement().getPropertyInt('clientHeight')
            if fakeheight > availableHeight:
                return True
        return False

    def announceScrollPosition(self):
        if self._scrollPositionElement is None:
            self._scrollPositionElement = DOM.createDiv()
            self._scrollPositionElement.setClassName(self.CLASSNAME + '-scrollposition')
            self._scrollPositionElement.getStyle().setPosition(Position.ABSOLUTE)
            self._scrollPositionElement.getStyle().setDisplay(Display.NONE)
            self.getElement().appendChild(self._scrollPositionElement)
        style = self._scrollPositionElement.getStyle()
        style.setMarginLeft((self.getElement().getOffsetWidth() / 2) - 80, Unit.PX)
        style.setMarginTop(-self._scrollBodyPanel.getOffsetHeight(), Unit.PX)
        # indexes go from 1-totalRows, as rowheaders in index-mode indicate
        last = self._firstRowInViewPort + self._pageLength
        if last > self._totalRows:
            last = self._totalRows
        self._scrollPositionElement.setInnerHTML('<span>' + self._firstRowInViewPort + 1 + ' &ndash; ' + last + '...' + '</span>')
        style.setDisplay(Display.BLOCK)

    def hideScrollPositionAnnotation(self):
        if self._scrollPositionElement is not None:
            DOM.setStyleAttribute(self._scrollPositionElement, 'display', 'none')

    def isScrollPositionVisible(self):
        return self._scrollPositionElement is not None and not (self._scrollPositionElement.getStyle().getDisplay() == str(Display.NONE))

    def RowRequestHandler(VScrollTable_this, *args, **kwargs):

        class RowRequestHandler(Timer):
            _reqFirstRow = 0
            _reqRows = 0
            _isRunning = False

            def deferRowFetch(self, *args):
                _0 = args
                _1 = len(args)
                if _1 == 0:
                    self.deferRowFetch(250)
                elif _1 == 1:
                    msec, = _0
                    self._isRunning = True
                    if self._reqRows > 0 and self._reqFirstRow < VScrollTable_this._totalRows:
                        self.schedule(msec)
                        # tell scroll position to user if currently "visible" rows are
                        # not rendered
                        if (
                            VScrollTable_this._totalRows > VScrollTable_this._pageLength and (VScrollTable_this._firstRowInViewPort + VScrollTable_this._pageLength > VScrollTable_this._scrollBody.getLastRendered()) or (VScrollTable_this._firstRowInViewPort < VScrollTable_this._scrollBody.getFirstRendered())
                        ):
                            VScrollTable_this.announceScrollPosition()
                        else:
                            VScrollTable_this.hideScrollPositionAnnotation()
                else:
                    raise ARGERROR(0, 1)

            def isRunning(self):
                return self._isRunning

            def setReqFirstRow(self, reqFirstRow):
                if reqFirstRow < 0:
                    reqFirstRow = 0
                elif reqFirstRow >= VScrollTable_this._totalRows:
                    reqFirstRow = VScrollTable_this._totalRows - 1
                self._reqFirstRow = reqFirstRow

            def setReqRows(self, reqRows):
                self._reqRows = reqRows

            def run(self):
                if (
                    VScrollTable_this.client.hasActiveRequest() or VScrollTable_this._navKeyDown
                ):
                    # if client connection is busy, don't bother loading it more
                    VConsole.log('Postponed rowfetch')
                    self.schedule(250)
                else:
                    firstToBeRendered = VScrollTable_this._scrollBody.firstRendered
                    if self._reqFirstRow < firstToBeRendered:
                        firstToBeRendered = self._reqFirstRow
                    elif (
                        VScrollTable_this._firstRowInViewPort - (VScrollTable_this._cache_rate * VScrollTable_this._pageLength) > firstToBeRendered
                    ):
                        firstToBeRendered = VScrollTable_this._firstRowInViewPort - (VScrollTable_this._cache_rate * VScrollTable_this._pageLength)
                        if firstToBeRendered < 0:
                            firstToBeRendered = 0
                    lastToBeRendered = VScrollTable_this._scrollBody.lastRendered
                    if (self._reqFirstRow + self._reqRows) - 1 > lastToBeRendered:
                        lastToBeRendered = (self._reqFirstRow + self._reqRows) - 1
                    elif (
                        VScrollTable_this._firstRowInViewPort + VScrollTable_this._pageLength + (VScrollTable_this._pageLength * VScrollTable_this._cache_rate) < lastToBeRendered
                    ):
                        lastToBeRendered = VScrollTable_this._firstRowInViewPort + VScrollTable_this._pageLength + (VScrollTable_this._pageLength * VScrollTable_this._cache_rate)
                        if lastToBeRendered >= VScrollTable_this._totalRows:
                            lastToBeRendered = VScrollTable_this._totalRows - 1
                        # due Safari 3.1 bug (see #2607), verify reqrows, original
                        # problem unknown, but this should catch the issue
                        if (self._reqFirstRow + self._reqRows) - 1 > lastToBeRendered:
                            self._reqRows = lastToBeRendered - self._reqFirstRow
                    VScrollTable_this.client.updateVariable(VScrollTable_this.paintableId, 'firstToBeRendered', firstToBeRendered, False)
                    VScrollTable_this.client.updateVariable(VScrollTable_this.paintableId, 'lastToBeRendered', lastToBeRendered, False)
                    # remember which firstvisible we requested, in case the server
                    # has
                    # a differing opinion
                    VScrollTable_this._lastRequestedFirstvisible = VScrollTable_this._firstRowInViewPort
                    VScrollTable_this.client.updateVariable(VScrollTable_this.paintableId, 'firstvisible', VScrollTable_this._firstRowInViewPort, False)
                    VScrollTable_this.client.updateVariable(VScrollTable_this.paintableId, 'reqfirstrow', self._reqFirstRow, False)
                    VScrollTable_this.client.updateVariable(VScrollTable_this.paintableId, 'reqrows', self._reqRows, True)
                    if VScrollTable_this._selectionChanged:
                        VScrollTable_this._unSyncedselectionsBeforeRowFetch = set(VScrollTable_this._selectedRowKeys)
                    self._isRunning = False

            def getReqFirstRow(self):
                return self._reqFirstRow

            def refreshContent(self):
                """Sends request to refresh content at this position."""
                self._isRunning = True
                first = VScrollTable_this._firstRowInViewPort - (VScrollTable_this._pageLength * VScrollTable_this._cache_rate)
                reqRows = (2 * VScrollTable_this._pageLength * VScrollTable_this._cache_rate) + VScrollTable_this._pageLength
                if first < 0:
                    reqRows = reqRows + first
                    first = 0
                self.setReqFirstRow(first)
                self.setReqRows(reqRows)
                self.run()

        return RowRequestHandler(*args, **kwargs)

    def HeaderCell(VScrollTable_this, *args, **kwargs):

        class HeaderCell(Widget):
            _td = DOM.createTD()
            _captionContainer = DOM.createDiv()
            _sortIndicator = DOM.createDiv()
            _colResizeWidget = DOM.createDiv()
            _floatingCopyOfHeaderCell = None
            _sortable = False
            _cid = None
            _dragging = None
            _dragStartX = None
            _colIndex = None
            _originalWidth = None
            _isResizing = None
            _headerX = None
            _moved = None
            _closestSlot = None
            _width = -1
            _naturalWidth = -1
            _align = VScrollTable_this.ALIGN_LEFT
            _definedWidth = False
            _expandRatio = 0
            _sorted = None

            def setSortable(self, b):
                self._sortable = b

            def resizeCaptionContainer(self, rightSpacing):
                """Makes room for the sorting indicator in case the column that the
                header cell belongs to is sorted. This is done by resizing the width
                of the caption container element by the correct amount
                """
                if (
                    (BrowserInfo.get().isIE6() or self._td.getClassName().contains('-asc')) or self._td.getClassName().contains('-desc')
                ):
                    # Room for the sort indicator is made by subtracting the styled
                    # margin and width of the resizer from the width of the caption
                    # container.

                    captionContainerWidth = self._width - self._sortIndicator.getOffsetWidth() - self._colResizeWidget.getOffsetWidth() - rightSpacing
                    self._captionContainer.getStyle().setPropertyPx('width', captionContainerWidth)
                else:
                    # Set the caption container element as wide as possible when
                    # the sorting indicator is not visible.

                    self._captionContainer.getStyle().setPropertyPx('width', self._width - rightSpacing)
                # Apply/Remove spacing if defined
                if rightSpacing > 0:
                    self._colResizeWidget.getStyle().setMarginLeft(rightSpacing, Unit.PX)
                else:
                    self._colResizeWidget.getStyle().clearMarginLeft()

            def setNaturalMinimumColumnWidth(self, w):
                self._naturalWidth = w

            def __init__(self, colId, headerText):
                self._cid = colId
                DOM.setElementProperty(self._colResizeWidget, 'className', VScrollTable_this.CLASSNAME + '-resizer')
                self.setText(headerText)
                DOM.appendChild(self._td, self._colResizeWidget)
                DOM.setElementProperty(self._sortIndicator, 'className', VScrollTable_this.CLASSNAME + '-sort-indicator')
                DOM.appendChild(self._td, self._sortIndicator)
                DOM.setElementProperty(self._captionContainer, 'className', VScrollTable_this.CLASSNAME + '-caption-container')
                # ensure no clipping initially (problem on column additions)
                DOM.setStyleAttribute(self._captionContainer, 'overflow', 'visible')
                DOM.appendChild(self._td, self._captionContainer)
                DOM.sinkEvents(self._td, Event.MOUSEEVENTS | Event.TOUCHEVENTS)
                self.setElement(self._td)
                self.setAlign(VScrollTable_this.ALIGN_LEFT)

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
                    VScrollTable_this.tHead.resizeCaptionContainer(self)
                    # if we already have tBody, set the header width properly, if
                    # not defer it. IE will fail with complex float in table header
                    # unless TD width is not explicitly set.

                    if VScrollTable_this._scrollBody is not None:
                        tdWidth = self._width + VScrollTable_this._scrollBody.getCellExtraWidth()
                        self.setWidth(tdWidth + 'px')
                    else:

                        class _8_(Command):

                            def execute(self):
                                tdWidth = HeaderCell_this._width + VScrollTable_this._scrollBody.getCellExtraWidth()
                                HeaderCell_this.setWidth(tdWidth + 'px')

                        _8_ = _8_()
                        Scheduler.get().scheduleDeferred(_8_)

            def setUndefinedWidth(self):
                self._definedWidth = False
                self.setWidth(-1, False)

            def isDefinedWidth(self):
                """Detects if width is fixed by developer on server side or resized to
                current width by user.

                @return true if defined, false if "natural" width
                """
                return self._definedWidth and self._width >= 0

            def getWidth(self):
                return self._width

            def setText(self, headerText):
                DOM.setInnerHTML(self._captionContainer, headerText)

            def getColKey(self):
                return self._cid

            def setSorted(self, sorted):
                self._sorted = sorted
                if sorted:
                    if VScrollTable_this._sortAscending:
                        self.setStyleName(VScrollTable_this.CLASSNAME + '-header-cell-asc')
                    else:
                        self.setStyleName(VScrollTable_this.CLASSNAME + '-header-cell-desc')
                else:
                    self.setStyleName(VScrollTable_this.CLASSNAME + '-header-cell')

            def onBrowserEvent(self, event):
                """Handle column reordering."""
                if VScrollTable_this._enabled and event is not None:
                    if self._isResizing or (event.getEventTarget() == self._colResizeWidget):
                        if (
                            self._dragging and (event.getTypeInt() == Event.ONMOUSEUP) or (event.getTypeInt() == Event.ONTOUCHEND)
                        ):
                            # Handle releasing column header on spacer #5318
                            self.handleCaptionEvent(event)
                        else:
                            self.onResizeEvent(event)
                    else:
                        # Ensure focus before handling caption event. Otherwise
                        # variables changed from caption event may be before
                        # variables from other components that fire variables when
                        # they lose focus.

                        if (
                            (event.getTypeInt() == Event.ONMOUSEDOWN) or (event.getTypeInt() == Event.ONTOUCHSTART)
                        ):
                            VScrollTable_this._scrollBodyPanel.setFocus(True)
                        self.handleCaptionEvent(event)
                        event.stopPropagation()
                        event.preventDefault()

            def createFloatingCopy(self):
                self._floatingCopyOfHeaderCell = DOM.createDiv()
                DOM.setInnerHTML(self._floatingCopyOfHeaderCell, DOM.getInnerHTML(self._td))
                self._floatingCopyOfHeaderCell = DOM.getChild(self._floatingCopyOfHeaderCell, 2)
                DOM.setElementProperty(self._floatingCopyOfHeaderCell, 'className', VScrollTable_this.CLASSNAME + '-header-drag')
                # otherwise might wrap or be cut if narrow column
                DOM.setStyleAttribute(self._floatingCopyOfHeaderCell, 'width', 'auto')
                self.updateFloatingCopysPosition(DOM.getAbsoluteLeft(self._td), DOM.getAbsoluteTop(self._td))
                DOM.appendChild(RootPanel.get().getElement(), self._floatingCopyOfHeaderCell)

            def updateFloatingCopysPosition(self, x, y):
                x -= DOM.getElementPropertyInt(self._floatingCopyOfHeaderCell, 'offsetWidth') / 2
                DOM.setStyleAttribute(self._floatingCopyOfHeaderCell, 'left', x + 'px')
                if y > 0:
                    DOM.setStyleAttribute(self._floatingCopyOfHeaderCell, 'top', y + 7 + 'px')

            def hideFloatingCopy(self):
                DOM.removeChild(RootPanel.get().getElement(), self._floatingCopyOfHeaderCell)
                self._floatingCopyOfHeaderCell = None

            def fireHeaderClickedEvent(self, event):
                """Fires a header click event after the user has clicked a column header
                cell

                @param event
                           The click event
                """
                if (
                    VScrollTable_this.client.hasEventListeners(VScrollTable_this, VScrollTable_this.HEADER_CLICK_EVENT_ID)
                ):
                    details = MouseEventDetails(event)
                    VScrollTable_this.client.updateVariable(VScrollTable_this.paintableId, 'headerClickEvent', str(details), False)
                    VScrollTable_this.client.updateVariable(VScrollTable_this.paintableId, 'headerClickCID', self._cid, True)

            def handleCaptionEvent(self, event):
                _0 = DOM.eventGetType(event)
                _1 = False
                while True:
                    if _0 == Event.ONTOUCHSTART:
                        _1 = True
                    if (_1 is True) or (_0 == Event.ONMOUSEDOWN):
                        _1 = True
                        if VScrollTable_this._columnReordering:
                            if event.getTypeInt() == Event.ONTOUCHSTART:
                                # prevent using this event in e.g. scrolling
                                event.stopPropagation()
                            self._dragging = True
                            self._moved = False
                            self._colIndex = VScrollTable_this.getColIndexByKey(self._cid)
                            DOM.setCapture(self.getElement())
                            self._headerX = VScrollTable_this.tHead.getAbsoluteLeft()
                            event.preventDefault()
                            # prevent selecting text &&
                            # generated touch events
                        break
                    if (_1 is True) or (_0 == Event.ONMOUSEUP):
                        _1 = True
                    if (_1 is True) or (_0 == Event.ONTOUCHEND):
                        _1 = True
                    if (_1 is True) or (_0 == Event.ONTOUCHCANCEL):
                        _1 = True
                        if VScrollTable_this._columnReordering:
                            self._dragging = False
                            DOM.releaseCapture(self.getElement())
                            if self._moved:
                                self.hideFloatingCopy()
                                VScrollTable_this.tHead.removeSlotFocus()
                                if (
                                    self._closestSlot != self._colIndex and self._closestSlot != self._colIndex + 1
                                ):
                                    if self._closestSlot > self._colIndex:
                                        VScrollTable_this.reOrderColumn(self._cid, self._closestSlot - 1)
                                    else:
                                        VScrollTable_this.reOrderColumn(self._cid, self._closestSlot)
                            if Util.isTouchEvent(event):
                                # Prevent using in e.g. scrolling and prevent generated
                                # events.

                                event.preventDefault()
                                event.stopPropagation()
                        if not self._moved:
                            # mouse event was a click to header -> sort column
                            if self._sortable:
                                if VScrollTable_this._sortColumn == self._cid:
                                    # just toggle order
                                    VScrollTable_this.client.updateVariable(VScrollTable_this.paintableId, 'sortascending', not VScrollTable_this._sortAscending, False)
                                else:
                                    # set table sorted by this column
                                    VScrollTable_this.client.updateVariable(VScrollTable_this.paintableId, 'sortcolumn', self._cid, False)
                                # get also cache columns at the same request
                                VScrollTable_this._scrollBodyPanel.setScrollPosition(0)
                                VScrollTable_this._firstvisible = 0
                                VScrollTable_this._rowRequestHandler.setReqFirstRow(0)
                                VScrollTable_this._rowRequestHandler.setReqRows((2 * VScrollTable_this._pageLength * VScrollTable_this._cache_rate) + VScrollTable_this._pageLength)
                                VScrollTable_this._rowRequestHandler.deferRowFetch()
                                # some validation +
                                # defer 250ms
                                VScrollTable_this._rowRequestHandler.cancel()
                                # instead of waiting
                                VScrollTable_this._rowRequestHandler.run()
                                # run immediately
                            self.fireHeaderClickedEvent(event)
                            if Util.isTouchEvent(event):
                                # Prevent using in e.g. scrolling and prevent generated
                                # events.

                                event.preventDefault()
                                event.stopPropagation()
                            break
                        break
                    if (_1 is True) or (_0 == Event.ONTOUCHMOVE):
                        _1 = True
                    if (_1 is True) or (_0 == Event.ONMOUSEMOVE):
                        _1 = True
                        if self._dragging:
                            if event.getTypeInt() == Event.ONTOUCHMOVE:
                                # prevent using this event in e.g. scrolling
                                event.stopPropagation()
                            if not self._moved:
                                self.createFloatingCopy()
                                self._moved = True
                            clientX = Util.getTouchOrMouseClientX(event)
                            x = clientX + VScrollTable_this.tHead.hTableWrapper.getScrollLeft()
                            slotX = self._headerX
                            self._closestSlot = self._colIndex
                            closestDistance = -1
                            start = 0
                            if VScrollTable_this.showRowHeaders:
                                start += 1
                            visibleCellCount = VScrollTable_this.tHead.getVisibleCellCount()
                            _2 = True
                            i = start
                            while True:
                                if _2 is True:
                                    _2 = False
                                else:
                                    i += 1
                                if not (i <= visibleCellCount):
                                    break
                                if i > 0:
                                    colKey = VScrollTable_this.getColKeyByIndex(i - 1)
                                    slotX += VScrollTable_this.getColWidth(colKey)
                                dist = self.Math.abs(x - slotX)
                                if (closestDistance == -1) or (dist < closestDistance):
                                    closestDistance = dist
                                    self._closestSlot = i
                            VScrollTable_this.tHead.focusSlot(self._closestSlot)
                            self.updateFloatingCopysPosition(clientX, -1)
                        break
                    if True:
                        _1 = True
                        break
                    break

            def onResizeEvent(self, event):
                _0 = DOM.eventGetType(event)
                _1 = False
                while True:
                    if _0 == Event.ONMOUSEDOWN:
                        _1 = True
                        self._isResizing = True
                        DOM.setCapture(self.getElement())
                        self._dragStartX = DOM.eventGetClientX(event)
                        self._colIndex = VScrollTable_this.getColIndexByKey(self._cid)
                        self._originalWidth = self.getWidth()
                        DOM.eventPreventDefault(event)
                        break
                    if (_1 is True) or (_0 == Event.ONMOUSEUP):
                        _1 = True
                        self._isResizing = False
                        DOM.releaseCapture(self.getElement())
                        VScrollTable_this.tHead.disableAutoColumnWidthCalculation(self)
                        # Ensure last header cell is taking into account possible
                        # column selector
                        lastCell = VScrollTable_this.tHead.getHeaderCell(VScrollTable_this.tHead.getVisibleCellCount() - 1)
                        VScrollTable_this.tHead.resizeCaptionContainer(lastCell)
                        VScrollTable_this.triggerLazyColumnAdjustment(True)
                        VScrollTable_this.fireColumnResizeEvent(self._cid, self._originalWidth, VScrollTable_this.getColWidth(self._cid))
                        break
                    if (_1 is True) or (_0 == Event.ONMOUSEMOVE):
                        _1 = True
                        if self._isResizing:
                            deltaX = DOM.eventGetClientX(event) - self._dragStartX
                            if deltaX == 0:
                                return
                            VScrollTable_this.tHead.disableAutoColumnWidthCalculation(self)
                            newWidth = self._originalWidth + deltaX
                            if newWidth < self.getMinWidth():
                                newWidth = self.getMinWidth()
                            VScrollTable_this.setColWidth(self._colIndex, newWidth, True)
                            VScrollTable_this.triggerLazyColumnAdjustment(False)
                            VScrollTable_this.forceRealignColumnHeaders()
                        break
                    if True:
                        _1 = True
                        break
                    break

            def getMinWidth(self):
                cellExtraWidth = 0
                if VScrollTable_this._scrollBody is not None:
                    cellExtraWidth += VScrollTable_this._scrollBody.getCellExtraWidth()
                return cellExtraWidth + self._sortIndicator.getOffsetWidth()

            def getCaption(self):
                return DOM.getInnerText(self._captionContainer)

            def isEnabled(self):
                return self.getParent() is not None

            def setAlign(self, c):
                ALIGN_PREFIX = VScrollTable_this.CLASSNAME + '-caption-container-align-'
                if self._align != c:
                    self._captionContainer.removeClassName(ALIGN_PREFIX + 'center')
                    self._captionContainer.removeClassName(ALIGN_PREFIX + 'right')
                    self._captionContainer.removeClassName(ALIGN_PREFIX + 'left')
                    _0 = c
                    _1 = False
                    while True:
                        if _0 == VScrollTable_this.ALIGN_CENTER:
                            _1 = True
                            self._captionContainer.addClassName(ALIGN_PREFIX + 'center')
                            break
                        if (_1 is True) or (_0 == VScrollTable_this.ALIGN_RIGHT):
                            _1 = True
                            self._captionContainer.addClassName(ALIGN_PREFIX + 'right')
                            break
                        if True:
                            _1 = True
                            self._captionContainer.addClassName(ALIGN_PREFIX + 'left')
                            break
                        break
                self._align = c

            def getAlign(self):
                return self._align

            def getNaturalColumnWidth(self, columnIndex):
                """Detects the natural minimum width for the column of this header cell.
                If column is resized by user or the width is defined by server the
                actual width is returned. Else the natural min width is returned.

                @param columnIndex
                           column index hint, if -1 (unknown) it will be detected

                @return
                """
                if self.isDefinedWidth():
                    return self._width
                else:
                    if self._naturalWidth < 0:
                        # This is recently revealed column. Try to detect a proper
                        # value (greater of header and data
                        # cols)
                        hw = self._captionContainer.getOffsetWidth() + VScrollTable_this._scrollBody.getCellExtraWidth()
                        if BrowserInfo.get().isGecko() or BrowserInfo.get().isIE7():
                            hw += self._sortIndicator.getOffsetWidth()
                        if columnIndex < 0:
                            columnIndex = 0
                            _0 = True
                            it = VScrollTable_this.tHead
                            while True:
                                if _0 is True:
                                    _0 = False
                                else:
                                    columnIndex += 1
                                if not it.hasNext():
                                    break
                                if it.next() is self:
                                    break
                        cw = VScrollTable_this._scrollBody.getColWidth(columnIndex)
                        self._naturalWidth = hw if hw > cw else cw
                    return self._naturalWidth

            def setExpandRatio(self, floatAttribute):
                if floatAttribute != self._expandRatio:
                    VScrollTable_this.triggerLazyColumnAdjustment(False)
                self._expandRatio = floatAttribute

            def getExpandRatio(self):
                return self._expandRatio

            def isSorted(self):
                return self._sorted

        return HeaderCell(*args, **kwargs)

    def RowHeadersHeaderCell(VScrollTable_this, *args, **kwargs):

        class RowHeadersHeaderCell(HeaderCell):
            """HeaderCell that is header cell for row headers.

            Reordering disabled and clicking on it resets sorting.
            """

            def __init__(self):
                super(RowHeadersHeaderCell, self)(VScrollTable_this._ROW_HEADER_COLUMN_KEY, '')
                self.setStyleName(VScrollTable_this.CLASSNAME + '-header-cell-rowheader')

            def handleCaptionEvent(self, event):
                # NOP: RowHeaders cannot be reordered
                # TODO It'd be nice to reset sorting here
                pass

        return RowHeadersHeaderCell(*args, **kwargs)

    def TableHead(VScrollTable_this, *args, **kwargs):

        class TableHead(Panel, ActionOwner):
            _WRAPPER_WIDTH = 900000
            _visibleCells = list()
            _availableCells = dict()
            _div = DOM.createDiv()
            _hTableWrapper = DOM.createDiv()
            _hTableContainer = DOM.createDiv()
            _table = DOM.createTable()
            _headerTableBody = DOM.createTBody()
            _tr = DOM.createTR()
            _columnSelector = DOM.createDiv()
            _focusedSlot = -1
            # public TableHead() {
            # if (BrowserInfo.get().isIE()) {
            # table.setPropertyInt("cellSpacing", 0);
            # }
            # DOM.setStyleAttribute(hTableWrapper, "overflow", "hidden");
            # DOM.setElementProperty(hTableWrapper, "className", CLASSNAME
            # + "-header");
            # // TODO move styles to CSS
            # DOM.setElementProperty(columnSelector, "className", CLASSNAME
            # + "-column-selector");
            # DOM.setStyleAttribute(columnSelector, "display", "none");
            # DOM.appendChild(table, headerTableBody);
            # DOM.appendChild(headerTableBody, tr);
            # DOM.appendChild(hTableContainer, table);
            # DOM.appendChild(hTableWrapper, hTableContainer);
            # DOM.appendChild(div, hTableWrapper);
            # DOM.appendChild(div, columnSelector);
            # setElement(div);
            # setStyleName(CLASSNAME + "-header-wrap");
            # DOM.sinkEvents(columnSelector, Event.ONCLICK);
            # availableCells.put(ROW_HEADER_COLUMN_KEY,
            # new RowHeadersHeaderCell());
            # }
            # public void resizeCaptionContainer(HeaderCell cell) {
            # HeaderCell lastcell = getHeaderCell(visibleCells.size() - 1);
            # // Measure column widths
            # int columnTotalWidth = 0;
            # for (Widget w : visibleCells) {
            # columnTotalWidth += w.getOffsetWidth();
            # }
            # if (cell == lastcell
            # && columnSelector.getOffsetWidth() > 0
            # && columnTotalWidth >= div.getOffsetWidth()
            # - columnSelector.getOffsetWidth()
            # && !hasVerticalScrollbar()) {
            # // Ensure column caption is visible when placed under the column
            # // selector widget by shifting and resizing the caption.
            # int offset = 0;
            # int diff = div.getOffsetWidth() - columnTotalWidth;
            # if (diff < columnSelector.getOffsetWidth() && diff > 0) {
            # // If the difference is less than the column selectors width
            # // then just offset by the
            # // difference
            # offset = columnSelector.getOffsetWidth() - diff;
            # } else {
            # // Else offset by the whole column selector
            # offset = columnSelector.getOffsetWidth();
            # }
            # lastcell.resizeCaptionContainer(offset);
            # } else {
            # cell.resizeCaptionContainer(0);
            # }
            # }
            # @Override
            # public void clear() {
            # for (String cid : availableCells.keySet()) {
            # removeCell(cid);
            # }
            # availableCells.clear();
            # availableCells.put(ROW_HEADER_COLUMN_KEY,
            # new RowHeadersHeaderCell());
            # }
            # public void updateCellsFromUIDL(UIDL uidl) {
            # Iterator<?> it = uidl.getChildIterator();
            # HashSet<String> updated = new HashSet<String>();
            # boolean refreshContentWidths = false;
            # while (it.hasNext()) {
            # final UIDL col = (UIDL) it.next();
            # final String cid = col.getStringAttribute("cid");
            # updated.add(cid);
            # String caption = buildCaptionHtmlSnippet(col);
            # HeaderCell c = getHeaderCell(cid);
            # if (c == null) {
            # c = new HeaderCell(cid, caption);
            # availableCells.put(cid, c);
            # if (initializedAndAttached) {
            # // we will need a column width recalculation
            # initializedAndAttached = false;
            # initialContentReceived = false;
            # isNewBody = true;
            # }
            # } else {
            # c.setText(caption);
            # }
            # if (col.hasAttribute("sortable")) {
            # c.setSortable(true);
            # if (cid.equals(sortColumn)) {
            # c.setSorted(true);
            # } else {
            # c.setSorted(false);
            # }
            # } else {
            # c.setSortable(false);
            # }
            # if (col.hasAttribute("align")) {
            # c.setAlign(col.getStringAttribute("align").charAt(0));
            # } else {
            # c.setAlign(ALIGN_LEFT);
            # }
            # if (col.hasAttribute("width")) {
            # final String widthStr = col.getStringAttribute("width");
            # // Make sure to accomodate for the sort indicator if
            # // necessary.
            # int width = Integer.parseInt(widthStr);
            # if (width < c.getMinWidth()) {
            # width = c.getMinWidth();
            # }
            # if (width != c.getWidth() && scrollBody != null) {
            # // Do a more thorough update if a column is resized from
            # // the server *after* the header has been properly
            # // initialized
            # final int colIx = getColIndexByKey(c.cid);
            # final int newWidth = width;
            # Scheduler.get().scheduleDeferred(
            # new ScheduledCommand() {
            # public void execute() {
            # setColWidth(colIx, newWidth, true);
            # }
            # });
            # refreshContentWidths = true;
            # } else {
            # c.setWidth(width, true);
            # }
            # } else if (recalcWidths) {
            # c.setUndefinedWidth();
            # }
            # if (col.hasAttribute("er")) {
            # c.setExpandRatio(col.getFloatAttribute("er"));
            # }
            # if (col.hasAttribute("collapsed")) {
            # // ensure header is properly removed from parent (case when
            # // collapsing happens via servers side api)
            # if (c.isAttached()) {
            # c.removeFromParent();
            # headerChangedDuringUpdate = true;
            # }
            # }
            # }
            # if (refreshContentWidths) {
            # // Recalculate the column sizings if any column has changed
            # Scheduler.get().scheduleDeferred(new ScheduledCommand() {
            # public void execute() {
            # triggerLazyColumnAdjustment(true);
            # }
            # });
            # }
            # // check for orphaned header cells
            # for (Iterator<String> cit = availableCells.keySet().iterator(); cit
            # .hasNext();) {
            # String cid = cit.next();
            # if (!updated.contains(cid)) {
            # removeCell(cid);
            # cit.remove();
            # // we will need a column width recalculation, since columns
            # // with expand ratios should expand to fill the void.
            # initializedAndAttached = false;
            # initialContentReceived = false;
            # isNewBody = true;
            # }
            # }
            # }

            def enableColumn(self, cid, index):
                c = self.getHeaderCell(cid)
                if (not c.isEnabled()) or (self.getHeaderCell(index) != c):
                    self.setHeaderCell(index, c)
                    if VScrollTable_this._initializedAndAttached:
                        VScrollTable_this._headerChangedDuringUpdate = True

            def getVisibleCellCount(self):
                return len(self._visibleCells)

            def setHorizontalScrollPosition(self, scrollLeft):
                if BrowserInfo.get().isIE6():
                    self._hTableWrapper.getStyle().setPosition(Position.RELATIVE)
                    self._hTableWrapper.getStyle().setLeft(-scrollLeft, Unit.PX)
                else:
                    self._hTableWrapper.setScrollLeft(scrollLeft)

            def setColumnCollapsingAllowed(self, cc):
                if cc:
                    self._columnSelector.getStyle().setDisplay(Display.BLOCK)
                else:
                    self._columnSelector.getStyle().setDisplay(Display.NONE)

            def disableBrowserIntelligence(self):
                self._hTableContainer.getStyle().setWidth(self._WRAPPER_WIDTH, Unit.PX)

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

            def getHeaderCell(self, *args):
                """None
                ---
                Get's HeaderCell by it's column Key.

                Note that this returns HeaderCell even if it is currently collapsed.

                @param cid
                           Column key of accessed HeaderCell
                @return HeaderCell
                """
                _0 = args
                _1 = len(args)
                if _1 == 1:
                    if isinstance(_0[0], int):
                        index, = _0
                        if index >= 0 and index < len(self._visibleCells):
                            return self._visibleCells[index]
                        else:
                            return None
                    else:
                        cid, = _0
                        return self._availableCells[cid]
                else:
                    raise ARGERROR(1, 1)

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
                if self._visibleCells.contains(w):
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
                    DOM.setElementProperty(DOM.getFirstChild(DOM.getChild(self._tr, index - 1)), 'className', VScrollTable_this.CLASSNAME + '-resizer ' + VScrollTable_this.CLASSNAME + '-focus-slot-right')
                else:
                    DOM.setElementProperty(DOM.getFirstChild(DOM.getChild(self._tr, index)), 'className', VScrollTable_this.CLASSNAME + '-resizer ' + VScrollTable_this.CLASSNAME + '-focus-slot-left')
                self._focusedSlot = index

            def removeSlotFocus(self):
                if self._focusedSlot < 0:
                    return
                if self._focusedSlot == 0:
                    DOM.setElementProperty(DOM.getFirstChild(DOM.getChild(self._tr, self._focusedSlot)), 'className', VScrollTable_this.CLASSNAME + '-resizer')
                elif self._focusedSlot > 0:
                    DOM.setElementProperty(DOM.getFirstChild(DOM.getChild(self._tr, self._focusedSlot - 1)), 'className', VScrollTable_this.CLASSNAME + '-resizer')
                self._focusedSlot = -1

            def onBrowserEvent(self, event):
                if VScrollTable_this._enabled:
                    if event.getEventTarget() == self._columnSelector:
                        left = DOM.getAbsoluteLeft(self._columnSelector)
                        top = DOM.getAbsoluteTop(self._columnSelector) + DOM.getElementPropertyInt(self._columnSelector, 'offsetHeight')
                        VScrollTable_this.client.getContextMenu().showAt(self, left, top)

            def onDetach(self):
                super(TableHead, self).onDetach()
                if VScrollTable_this.client is not None:
                    VScrollTable_this.client.getContextMenu().ensureHidden(self)

            class VisibleColumnAction(Action):
                # Returns columns as Action array for column select popup
                _colKey = None
                _collapsed = None
                _currentlyFocusedRow = None

                def __init__(self, colKey):
                    # super(VScrollTable.TableHead.this);
                    self._colKey = colKey
                    self.caption = VScrollTable_this.tHead.getHeaderCell(colKey).getCaption()
                    self._currentlyFocusedRow = VScrollTable_this._focusedRow

                def execute(self):
                    VScrollTable_this.client.getContextMenu().hide()
                    # toggle selected column
                    if self._colKey in VScrollTable_this._collapsedColumns:
                        VScrollTable_this._collapsedColumns.remove(self._colKey)
                    else:
                        VScrollTable_this.tHead.removeCell(self._colKey)
                        VScrollTable_this._collapsedColumns.add(self._colKey)
                        VScrollTable_this.triggerLazyColumnAdjustment(True)
                    # update variable to server
                    VScrollTable_this.client.updateVariable(VScrollTable_this.paintableId, 'collapsedcolumns', list([None] * len(VScrollTable_this._collapsedColumns)), False)
                    # let rowRequestHandler determine proper rows
                    VScrollTable_this._rowRequestHandler.refreshContent()
                    VScrollTable_this.lazyRevertFocusToRow(self._currentlyFocusedRow)

                def setCollapsed(self, b):
                    self._collapsed = b

                def getHTML(self):
                    """Override default method to distinguish on/off columns"""
                    buf = str()
                    if self._collapsed:
                        buf.__add__('<span class=\"v-off\">')
                    else:
                        buf.__add__('<span class=\"v-on\">')
                    buf.__add__(super(VisibleColumnAction, self).getHTML())
                    buf.__add__('</span>')
                    return str(buf)

            def getActions(self):
                if (
                    VScrollTable_this._columnReordering and VScrollTable_this._columnOrder is not None
                ):
                    cols = VScrollTable_this._columnOrder
                else:
                    # if columnReordering is disabled, we need different way to get
                    # all available columns
                    cols = VScrollTable_this._visibleColOrder
                    cols = [None] * (len(VScrollTable_this._visibleColOrder) + len(VScrollTable_this._collapsedColumns))
                    _0 = True
                    i = 0
                    while True:
                        if _0 is True:
                            _0 = False
                        else:
                            i += 1
                        if not (i < len(VScrollTable_this._visibleColOrder)):
                            break
                        cols[i] = VScrollTable_this._visibleColOrder[i]
                    _1 = True
                    it = VScrollTable_this._collapsedColumns
                    while True:
                        if _1 is True:
                            _1 = False
                        if not it.hasNext():
                            break
                        cols[POSTINC(globals(), locals(), 'i')] = it.next()
                actions = [None] * len(cols)
                _2 = True
                i = 0
                while True:
                    if _2 is True:
                        _2 = False
                    else:
                        i += 1
                    if not (i < len(cols)):
                        break
                    cid = cols[i]
                    c = self.getHeaderCell(cid)
                    a = self.VisibleColumnAction(c.getColKey())
                    a.setCaption(c.getCaption())
                    if not c.isEnabled():
                        a.setCollapsed(True)
                    actions[i] = a
                return actions

            def getClient(self):
                return VScrollTable_this.client

            def getPaintableId(self):
                return VScrollTable_this.paintableId

            def getColumnAlignments(self):
                """Returns column alignments for visible columns"""
                it = self._visibleCells
                aligns = [None] * len(self._visibleCells)
                colIndex = 0
                while it.hasNext():
                    aligns[POSTINC(globals(), locals(), 'colIndex')] = it.next().getAlign()
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
                VScrollTable_this.sendColumnWidthUpdates(columns)
                VScrollTable_this.forceRealignColumnHeaders()

        return TableHead(*args, **kwargs)

    def FooterCell(VScrollTable_this, *args, **kwargs):

        class FooterCell(Widget):
            """A cell in the footer"""
            _td = DOM.createTD()
            _captionContainer = DOM.createDiv()
            _align = VScrollTable_this.ALIGN_LEFT
            _width = -1
            _expandRatio = 0
            _cid = None
            _definedWidth = False
            _naturalWidth = -1

            def __init__(self, colId, headerText):
                self._cid = colId
                self.setText(headerText)
                DOM.setElementProperty(self._captionContainer, 'className', VScrollTable_this.CLASSNAME + '-footer-container')
                # ensure no clipping initially (problem on column additions)
                DOM.setStyleAttribute(self._captionContainer, 'overflow', 'visible')
                DOM.sinkEvents(self._captionContainer, Event.MOUSEEVENTS)
                DOM.appendChild(self._td, self._captionContainer)
                DOM.sinkEvents(self._td, Event.MOUSEEVENTS)
                self.setElement(self._td)

            def setText(self, footerText):
                """Sets the text of the footer

                @param footerText
                           The text in the footer
                """
                DOM.setInnerHTML(self._captionContainer, footerText)

            def setAlign(self, c):
                """Set alignment of the text in the cell

                @param c
                           The alignment which can be ALIGN_CENTER, ALIGN_LEFT,
                           ALIGN_RIGHT
                """
                if self._align != c:
                    _0 = c
                    _1 = False
                    while True:
                        if _0 == VScrollTable_this.ALIGN_CENTER:
                            _1 = True
                            DOM.setStyleAttribute(self._captionContainer, 'textAlign', 'center')
                            break
                        if (_1 is True) or (_0 == VScrollTable_this.ALIGN_RIGHT):
                            _1 = True
                            DOM.setStyleAttribute(self._captionContainer, 'textAlign', 'right')
                            break
                        if True:
                            _1 = True
                            DOM.setStyleAttribute(self._captionContainer, 'textAlign', '')
                            break
                        break
                self._align = c

            def getAlign(self):
                """Get the alignment of the text int the cell

                @return Returns either ALIGN_CENTER, ALIGN_LEFT or ALIGN_RIGHT
                """
                return self._align

            def setWidth(self, w, ensureDefinedWidth):
                """Sets the width of the cell

                @param w
                           The width of the cell
                @param ensureDefinedWidth
                           Ensures the the given width is not recalculated
                """
                if ensureDefinedWidth:
                    self._definedWidth = True
                    # on column resize expand ratio becomes zero
                    self._expandRatio = 0
                if self._width == w:
                    return
                if self._width == -1:
                    # go to default mode, clip content if necessary
                    DOM.setStyleAttribute(self._captionContainer, 'overflow', '')
                self._width = w
                if w == -1:
                    DOM.setStyleAttribute(self._captionContainer, 'width', '')
                    self.setWidth('')
                else:
                    # Reduce width with one pixel for the right border since the
                    # footers does not have any spacers between them.

                    borderWidths = 1
                    # Set the container width (check for negative value)
                    if w - borderWidths >= 0:
                        self._captionContainer.getStyle().setPropertyPx('width', w - borderWidths)
                    else:
                        self._captionContainer.getStyle().setPropertyPx('width', 0)
                    # if we already have tBody, set the header width properly, if
                    # not defer it. IE will fail with complex float in table header
                    # unless TD width is not explicitly set.

                    if VScrollTable_this._scrollBody is not None:
                        # Reduce with one since footer does not have any spacers,
                        # instead a 1 pixel border.

                        tdWidth = (self._width + VScrollTable_this._scrollBody.getCellExtraWidth()) - borderWidths
                        self.setWidth(tdWidth + 'px')
                    else:

                        class _9_(Command):

                            def execute(self):
                                borderWidths = 1
                                tdWidth = (FooterCell_this._width + VScrollTable_this._scrollBody.getCellExtraWidth()) - borderWidths
                                FooterCell_this.setWidth(tdWidth + 'px')

                        _9_ = _9_()
                        Scheduler.get().scheduleDeferred(_9_)

            def setUndefinedWidth(self):
                """Sets the width to undefined"""
                self.setWidth(-1, False)

            def isDefinedWidth(self):
                """Detects if width is fixed by developer on server side or resized to
                current width by user.

                @return true if defined, false if "natural" width
                """
                return self._definedWidth and self._width >= 0

            def getWidth(self):
                """Returns the pixels width of the footer cell

                @return The width in pixels
                """
                return self._width

            def setExpandRatio(self, floatAttribute):
                """Sets the expand ratio of the cell

                @param floatAttribute
                           The expand ratio
                """
                self._expandRatio = floatAttribute

            def getExpandRatio(self):
                """Returns the expand ration of the cell

                @return The expand ratio
                """
                return self._expandRatio

            def isEnabled(self):
                """Is the cell enabled?

                @return True if enabled else False
                """
                return self.getParent() is not None

            def onBrowserEvent(self, event):
                """Handle column clicking"""
                if VScrollTable_this._enabled and event is not None:
                    self.handleCaptionEvent(event)
                    if DOM.eventGetType(event) == Event.ONMOUSEUP:
                        VScrollTable_this._scrollBodyPanel.setFocus(True)
                    event.stopPropagation()
                    event.preventDefault()

            def handleCaptionEvent(self, event):
                """Handles a event on the captions

                @param event
                           The event to handle
                """
                if DOM.eventGetType(event) == Event.ONMOUSEUP:
                    self.fireFooterClickedEvent(event)

            def fireFooterClickedEvent(self, event):
                """Fires a footer click event after the user has clicked a column footer
                cell

                @param event
                           The click event
                """
                if (
                    VScrollTable_this.client.hasEventListeners(VScrollTable_this, VScrollTable_this.FOOTER_CLICK_EVENT_ID)
                ):
                    details = MouseEventDetails(event)
                    VScrollTable_this.client.updateVariable(VScrollTable_this.paintableId, 'footerClickEvent', str(details), False)
                    VScrollTable_this.client.updateVariable(VScrollTable_this.paintableId, 'footerClickCID', self._cid, True)

            def getColKey(self):
                """Returns the column key of the column

                @return The column key
                """
                return self._cid

            def getNaturalColumnWidth(self, columnIndex):
                """Detects the natural minimum width for the column of this header cell.
                If column is resized by user or the width is defined by server the
                actual width is returned. Else the natural min width is returned.

                @param columnIndex
                           column index hint, if -1 (unknown) it will be detected

                @return
                """
                if self.isDefinedWidth():
                    return self._width
                else:
                    if self._naturalWidth < 0:
                        # This is recently revealed column. Try to detect a proper
                        # value (greater of header and data
                        # cols)
                        hw = self.getElement().getLastChild().getOffsetWidth() + VScrollTable_this._scrollBody.getCellExtraWidth()
                        if columnIndex < 0:
                            columnIndex = 0
                            _0 = True
                            it = VScrollTable_this.tHead
                            while True:
                                if _0 is True:
                                    _0 = False
                                else:
                                    columnIndex += 1
                                if not it.hasNext():
                                    break
                                if it.next() is self:
                                    break
                        cw = VScrollTable_this._scrollBody.getColWidth(columnIndex)
                        self._naturalWidth = hw if hw > cw else cw
                    return self._naturalWidth

            def setNaturalMinimumColumnWidth(self, w):
                self._naturalWidth = w

        return FooterCell(*args, **kwargs)

    def RowHeadersFooterCell(VScrollTable_this, *args, **kwargs):

        class RowHeadersFooterCell(FooterCell):
            """HeaderCell that is header cell for row headers.

            Reordering disabled and clicking on it resets sorting.
            """

            def __init__(self):
                super(RowHeadersFooterCell, self)(VScrollTable_this._ROW_HEADER_COLUMN_KEY, '')

            def handleCaptionEvent(self, event):
                # NOP: RowHeaders cannot be reordered
                # TODO It'd be nice to reset sorting here
                pass

        return RowHeadersFooterCell(*args, **kwargs)

    def TableFooter(VScrollTable_this, *args, **kwargs):

        class TableFooter(Panel):
            """The footer of the table which can be seen in the bottom of the Table."""
            _WRAPPER_WIDTH = 900000
            _visibleCells = list()
            _availableCells = dict()
            _div = DOM.createDiv()
            _hTableWrapper = DOM.createDiv()
            _hTableContainer = DOM.createDiv()
            _table = DOM.createTable()
            _headerTableBody = DOM.createTBody()
            _tr = DOM.createTR()

            def __init__(self):
                DOM.setStyleAttribute(self._hTableWrapper, 'overflow', 'hidden')
                DOM.setElementProperty(self._hTableWrapper, 'className', VScrollTable_this.CLASSNAME + '-footer')
                DOM.appendChild(self._table, self._headerTableBody)
                DOM.appendChild(self._headerTableBody, self._tr)
                DOM.appendChild(self._hTableContainer, self._table)
                DOM.appendChild(self._hTableWrapper, self._hTableContainer)
                DOM.appendChild(self._div, self._hTableWrapper)
                self.setElement(self._div)
                self.setStyleName(VScrollTable_this.CLASSNAME + '-footer-wrap')
                self._availableCells.put(VScrollTable_this._ROW_HEADER_COLUMN_KEY, VScrollTable_this.RowHeadersFooterCell())

            def clear(self):
                # (non-Javadoc)
                # 
                # @see
                # com.google.gwt.user.client.ui.Panel#remove(com.google.gwt.user.client
                # .ui.Widget)

                for cid in self._availableCells.keys():
                    self.removeCell(cid)
                self._availableCells.clear()
                self._availableCells.put(VScrollTable_this._ROW_HEADER_COLUMN_KEY, VScrollTable_this.RowHeadersFooterCell())

            def remove(self, w):
                # (non-Javadoc)
                # 
                # @see com.google.gwt.user.client.ui.HasWidgets#iterator()

                if self._visibleCells.contains(w):
                    self._visibleCells.remove(w)
                    self.orphan(w)
                    DOM.removeChild(DOM.getParent(w.getElement()), w.getElement())
                    return True
                return False

            def iterator(self):
                return self._visibleCells

            def getFooterCell(self, *args):
                """Gets a footer cell which represents the given columnId

                @param cid
                           The columnId

                @return The cell
                ---
                Gets a footer cell by using a column index

                @param index
                           The index of the column
                @return The Cell
                """
                _0 = args
                _1 = len(args)
                if _1 == 1:
                    if isinstance(_0[0], int):
                        index, = _0
                        if index < len(self._visibleCells):
                            return self._visibleCells[index]
                        else:
                            return None
                    else:
                        cid, = _0
                        return self._availableCells[cid]
                else:
                    raise ARGERROR(1, 1)

            def updateCellsFromUIDL(self, uidl):
                """Updates the cells contents when updateUIDL request is received

                @param uidl
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
                        c = VScrollTable_this.FooterCell(cid, caption)
                        self._availableCells.put(cid, c)
                        if VScrollTable_this._initializedAndAttached:
                            # we will need a column width recalculation
                            VScrollTable_this._initializedAndAttached = False
                            VScrollTable_this._initialContentReceived = False
                            VScrollTable_this._isNewBody = True
                    else:
                        c.setText(caption)
                    if col.hasAttribute('align'):
                        c.setAlign(col.getStringAttribute('align')[0])
                    else:
                        c.setAlign(VScrollTable_this.ALIGN_LEFT)
                    if col.hasAttribute('width'):
                        if VScrollTable_this._scrollBody is None:
                            # Already updated by setColWidth called from
                            # TableHeads.updateCellsFromUIDL in case of a server
                            # side resize
                            width = col.getStringAttribute('width')
                            c.setWidth(int(width), True)
                    elif VScrollTable_this._recalcWidths:
                        c.setUndefinedWidth()
                    if col.hasAttribute('er'):
                        c.setExpandRatio(col.getFloatAttribute('er'))
                    if col.hasAttribute('collapsed'):
                        # ensure header is properly removed from parent (case when
                        # collapsing happens via servers side api)
                        if c.isAttached():
                            c.removeFromParent()
                            VScrollTable_this._headerChangedDuringUpdate = True
                # check for orphaned header cells
                _0 = True
                cit = self._availableCells.keys()
                while True:
                    if _0 is True:
                        _0 = False
                    if not cit.hasNext():
                        break
                    cid = cit.next()
                    if not (cid in updated):
                        self.removeCell(cid)
                        cit.remove()

            def setFooterCell(self, index, cell):
                """Set a footer cell for a specified column index

                @param index
                           The index
                @param cell
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

                @param colKey
                           The columnId to remove
                """
                c = self.getFooterCell(colKey)
                self.remove(c)

            def enableColumn(self, cid, index):
                """Enable a column (Sets the footer cell)

                @param cid
                           The columnId
                @param index
                           The index of the column
                """
                c = self.getFooterCell(cid)
                if (not c.isEnabled()) or (self.getFooterCell(index) != c):
                    self.setFooterCell(index, c)
                    if VScrollTable_this._initializedAndAttached:
                        VScrollTable_this._headerChangedDuringUpdate = True

            def disableBrowserIntelligence(self):
                """Disable browser measurement of the table width"""
                DOM.setStyleAttribute(self._hTableContainer, 'width', self._WRAPPER_WIDTH + 'px')

            def enableBrowserIntelligence(self):
                """Enable browser measurement of the table width"""
                DOM.setStyleAttribute(self._hTableContainer, 'width', '')

            def setHorizontalScrollPosition(self, scrollLeft):
                """Set the horizontal position in the cell in the footer. This is done
                when a horizontal scrollbar is present.

                @param scrollLeft
                           The value of the leftScroll
                """
                if BrowserInfo.get().isIE6():
                    self._hTableWrapper.getStyle().setProperty('position', 'relative')
                    self._hTableWrapper.getStyle().setPropertyPx('left', -scrollLeft)
                else:
                    self._hTableWrapper.setScrollLeft(scrollLeft)

            def moveCell(self, oldIndex, newIndex):
                """Swap cells when the column are dragged

                @param oldIndex
                           The old index of the cell
                @param newIndex
                           The new index of the cell
                """
                hCell = self.getFooterCell(oldIndex)
                cell = hCell.getElement()
                self._visibleCells.remove(oldIndex)
                DOM.removeChild(self._tr, cell)
                DOM.insertChild(self._tr, cell, newIndex)
                self._visibleCells.add(newIndex, hCell)

        return TableFooter(*args, **kwargs)

    def VScrollTableBody(VScrollTable_this, *args, **kwargs):

        class VScrollTableBody(Panel):
            """This Panel can only contain VScrollTableRow type of widgets. This
            "simulates" very large table, keeping spacers which take room of
            unrendered rows.
            """
            DEFAULT_ROW_HEIGHT = 24
            _rowHeight = -1
            _renderedRows = LinkedList()
            # Due some optimizations row height measuring is deferred and initial
            # set of rows is rendered detached. Flag set on when table body has
            # been attached in dom and rowheight has been measured.

            _tBodyMeasurementsDone = False
            _preSpacer = DOM.createDiv()
            _postSpacer = DOM.createDiv()
            _container = DOM.createDiv()
            _tBodyElement = Document.get().createTBodyElement()
            _table = DOM.createTable()
            _firstRendered = None
            _lastRendered = None
            _aligns = None

            def __init__(self):
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
                DOM.setElementProperty(self._table, 'className', VScrollTable_this.CLASSNAME + '-table')
                if BrowserInfo.get().isIE():
                    self._table.setPropertyInt('cellSpacing', 0)
                DOM.setElementProperty(self._preSpacer, 'className', VScrollTable_this.CLASSNAME + '-row-spacer')
                DOM.setElementProperty(self._postSpacer, 'className', VScrollTable_this.CLASSNAME + '-row-spacer')
                self._table.appendChild(self._tBodyElement)
                DOM.appendChild(self._container, self._preSpacer)
                DOM.appendChild(self._container, self._table)
                DOM.appendChild(self._container, self._postSpacer)

            def getAvailableWidth(self):
                availW = VScrollTable_this._scrollBodyPanel.getOffsetWidth() - VScrollTable_this.getBorderWidth()
                return availW

            def renderInitialRows(self, rowData, firstIndex, rows):
                self._firstRendered = firstIndex
                self._lastRendered = (firstIndex + rows) - 1
                it = rowData.getChildIterator()
                self._aligns = VScrollTable_this.tHead.getColumnAlignments()
                while it.hasNext():
                    row = self.createRow(it.next(), self._aligns)
                    self.addRow(row)
                if self.isAttached():
                    self.fixSpacers()

            def renderRows(self, rowData, firstIndex, rows):
                # FIXME REVIEW
                self._aligns = VScrollTable_this.tHead.getColumnAlignments()
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
                    _0 = True
                    i = 0
                    while True:
                        if _0 is True:
                            _0 = False
                        else:
                            i += 1
                        if not (i < rows):
                            break
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
                reactFirstRow = VScrollTable_this._firstRowInViewPort - (VScrollTable_this._pageLength * VScrollTable_this._cache_react_rate)
                reactLastRow = VScrollTable_this._firstRowInViewPort + VScrollTable_this._pageLength + (VScrollTable_this._pageLength * VScrollTable_this._cache_react_rate)
                if reactFirstRow < 0:
                    reactFirstRow = 0
                if reactLastRow >= VScrollTable_this._totalRows:
                    reactLastRow = VScrollTable_this._totalRows - 1
                if self._lastRendered < reactLastRow:
                    # get some cache rows below visible area
                    VScrollTable_this._rowRequestHandler.setReqFirstRow(self._lastRendered + 1)
                    VScrollTable_this._rowRequestHandler.setReqRows(reactLastRow - self._lastRendered)
                    VScrollTable_this._rowRequestHandler.deferRowFetch(1)
                elif VScrollTable_this._scrollBody.getFirstRendered() > reactFirstRow:
                    # Branch for fetching cache above visible area.
                    # 
                    # If cache needed for both before and after visible area, this
                    # will be rendered after-cache is received and rendered. So in
                    # some rare situations the table may make two cache visits to
                    # server.

                    VScrollTable_this._rowRequestHandler.setReqFirstRow(reactFirstRow)
                    VScrollTable_this._rowRequestHandler.setReqRows(self._firstRendered - reactFirstRow)
                    VScrollTable_this._rowRequestHandler.deferRowFetch(1)

            def insertRows(self, rowData, firstIndex, rows):
                """Inserts rows as provided in the rowData starting at firstIndex.

                @param rowData
                @param firstIndex
                @param rows
                           the number of rows
                @return a list of the rows added.
                """
                self._aligns = VScrollTable_this.tHead.getColumnAlignments()
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
                    _0 = True
                    i = 0
                    while True:
                        if _0 is True:
                            _0 = False
                        else:
                            i += 1
                        if not (i < rows):
                            break
                        self.addRowBeforeFirstRendered(rowArray[i])
                        insertedRows.add(rowArray[i])
                        self._firstRendered -= 1
                else:
                    # insert in the middle
                    ix = firstIndex
                    while it.hasNext():
                        row = self.prepareRow(it.next())
                        self.insertRowAt(row, ix)
                        insertedRows.add(row)
                        self._lastRendered += 1
                        ix += 1
                    self.fixSpacers()
                return insertedRows

            def insertAndReindexRows(self, rowData, firstIndex, rows):
                inserted = self.insertRows(rowData, firstIndex, rows)
                actualIxOfFirstRowAfterInserted = (firstIndex + rows) - self._firstRendered
                _0 = True
                ix = actualIxOfFirstRowAfterInserted
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        ix += 1
                    if not (ix < len(self._renderedRows)):
                        break
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

                @param uidl
                """
                row = self.createRow(uidl, self._aligns)
                row.initCellWidths()
                return row

            def createRow(self, uidl, aligns2):
                if uidl.hasAttribute('gen_html'):
                    # This is a generated row.
                    return self.VScrollTableGeneratedRow(uidl, aligns2)
                return self.VScrollTableRow(uidl, aligns2)

            def addRowBeforeFirstRendered(self, row):
                row.setIndex(self._firstRendered - 1)
                if row.isSelected():
                    row.addStyleName('v-selected')
                self._tBodyElement.insertBefore(row.getElement(), self._tBodyElement.getFirstChild())
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
                    self._tBodyElement.insertAfter(row.getElement(), sibling.getElement())
                else:
                    sibling = self.getRowByRowIndex(index)
                    self._tBodyElement.insertBefore(row.getElement(), sibling.getElement())
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
                if (
                    self._firstRendered > firstIndex and self._firstRendered < firstIndex + count
                ):
                    firstIndex = self._firstRendered
                lastIndex = (firstIndex + count) - 1
                if self._lastRendered < lastIndex:
                    lastIndex = self._lastRendered
                _0 = True
                ix = lastIndex
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        ix -= 1
                    if not (ix >= firstIndex):
                        break
                    self.unlinkRowAtActualIndex(self.actualIndex(ix))
                    self._lastRendered -= 1
                self.fixSpacers()

            def unlinkAndReindexRows(self, firstIndex, count):
                self.unlinkRows(firstIndex, count)
                actualFirstIx = firstIndex - self._firstRendered
                _0 = True
                ix = actualFirstIx
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        ix += 1
                    if not (ix < len(self._renderedRows)):
                        break
                    r = self._renderedRows.get(ix)
                    r.setIndex(r.getIndex() - count)
                self.fixSpacers()

            def unlinkAllRowsStartingAt(self, index):
                if self._firstRendered > index:
                    index = self._firstRendered
                _0 = True
                ix = len(self._renderedRows) - 1
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        ix -= 1
                    if not (ix >= index):
                        break
                    self.unlinkRowAtActualIndex(self.actualIndex(ix))
                    self._lastRendered -= 1
                self.fixSpacers()

            def actualIndex(self, index):
                return index - self._firstRendered

            def unlinkRowAtActualIndex(self, index):
                toBeRemoved = self._renderedRows.get(index)
                # Unregister row tooltip
                VScrollTable_this.client.registerTooltip(VScrollTable_this, toBeRemoved.getElement(), None)
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < toBeRemoved.getElement().getChildCount()):
                        break
                    # Unregister cell tooltips
                    td = toBeRemoved.getElement().getChild(i)
                    VScrollTable_this.client.registerTooltip(VScrollTable_this, td, None)
                VScrollTable_this._lazyUnregistryBag.add(toBeRemoved)
                self._tBodyElement.removeChild(toBeRemoved.getElement())
                self.orphan(toBeRemoved)
                self._renderedRows.remove(index)

            def remove(self, w):
                raise self.UnsupportedOperationException()

            def onAttach(self):
                super(VScrollTableBody, self).onAttach()
                self.setContainerHeight()

            def setContainerHeight(self):
                """Fix container blocks height according to totalRows to avoid
                "bouncing" when scrolling
                """
                self.fixSpacers()
                DOM.setStyleAttribute(self._container, 'height', VScrollTable_this.measureRowHeightOffset(VScrollTable_this._totalRows) + 'px')

            def fixSpacers(self):
                prepx = VScrollTable_this.measureRowHeightOffset(self._firstRendered)
                if prepx < 0:
                    prepx = 0
                self._preSpacer.getStyle().setPropertyPx('height', prepx)
                postpx = VScrollTable_this.measureRowHeightOffset(VScrollTable_this._totalRows - 1) - VScrollTable_this.measureRowHeightOffset(self._lastRendered)
                if postpx < 0:
                    postpx = 0
                self._postSpacer.getStyle().setPropertyPx('height', postpx)

            def getRowHeight(self, *args):
                _0 = args
                _1 = len(args)
                if _1 == 0:
                    return self.getRowHeight(False)
                elif _1 == 1:
                    forceUpdate, = _0
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
                            # TODO investigate if this can never happen anymore
                            return self.DEFAULT_ROW_HEIGHT
                        self._tBodyMeasurementsDone = True
                        return self._rowHeight
                else:
                    raise ARGERROR(0, 1)

            def getTableHeight(self):
                return self._table.getOffsetHeight()

            def getColWidth(self, columnIndex):
                """Returns the width available for column content.

                @param columnIndex
                @return
                """
                if self._tBodyMeasurementsDone:
                    if self._renderedRows.isEmpty():
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

                @param colIndex
                @param w
                """
                for row in self._renderedRows:
                    row.setCellWidth(colIndex, w)

            _cellExtraWidth = -1

            def getCellExtraWidth(self):
                """Method to return the space used for cell paddings + border."""
                if self._cellExtraWidth < 0:
                    self.detectExtrawidth()
                return self._cellExtraWidth

            def detectExtrawidth(self):
                rows = self._tBodyElement.getRows()
                if rows.getLength() == 0:
                    # need to temporary add empty row and detect
                    scrollTableRow = self.VScrollTableRow()
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
                        sorted = VScrollTable_this.tHead.getHeaderCell(0).isSorted() if VScrollTable_this.tHead.getHeaderCell(0) is not None else False
                        next.addCell(None, '', VScrollTable_this.ALIGN_LEFT, '', True, sorted)
                        firstTD = item.getCells().getItem(0)
                    wrapper = firstTD.getFirstChildElement()
                    self._cellExtraWidth = firstTD.getOffsetWidth() - wrapper.getOffsetWidth()
                    if noCells:
                        firstTD.getParentElement().removeChild(firstTD)

            def reLayoutComponents(self):
                for w in self:
                    r = w
                    for widget in r:
                        VScrollTable_this.client.handleComponentRelativeSize(widget)

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

        return VScrollTableBody(*args, **kwargs)

    def deselectAll(self):
        """Deselects all items"""
        for w in self._scrollBody:
            row = w
            if row.isSelected():
                row.toggleSelection()
        # still ensure all selects are removed from (not necessary rendered)
        self._selectedRowKeys.clear()
        self._selectedRowRanges.clear()
        # also notify server that it clears all previous selections (the client
        # side does not know about the invisible ones)
        self.instructServerToForgetPreviousSelections()

    def instructServerToForgetPreviousSelections(self):
        """Used in multiselect mode when the client side knows that all selections
        are in the next request.
        """
        self.client.updateVariable(self.paintableId, 'clearSelections', True, False)

    # Only update if visible and enabled

    def setWidth(self, width):
        if self._width == width:
            return
        self._width = width
        if width is not None and not ('' == width):
            super(VScrollTable, self).setWidth(width)
            innerPixels = self.getOffsetWidth() - self.getBorderWidth()
            if innerPixels < 0:
                innerPixels = 0
            self.setContentWidth(innerPixels)
            # readjust undefined width columns
            self.triggerLazyColumnAdjustment(False)
        else:
            # Undefined width
            super(VScrollTable, self).setWidth('')
            # Readjust size of table
            self.sizeInit()
            # readjust undefined width columns
            self.triggerLazyColumnAdjustment(False)
        # setting width may affect wheter the component has scrollbars -> needs
        # scrolling or not

        self.setProperTabIndex()

    _LAZY_COLUMN_ADJUST_TIMEOUT = 300
    # private final Timer lazyAdjustColumnWidths = new Timer() {
    # /**
    # * Check for column widths, and available width, to see if we can fix
    # * column widths "optimally". Doing this lazily to avoid expensive
    # * calculation when resizing is not yet finished.
    # //
    # @Override
    # public void run() {
    # if (scrollBody == null) {
    # // Try again later if we get here before scrollBody has been
    # // initalized
    # triggerLazyColumnAdjustment(false);
    # return;
    # }
    # Iterator<Widget> headCells = tHead.iterator();
    # int usedMinimumWidth = 0;
    # int totalExplicitColumnsWidths = 0;
    # float expandRatioDivider = 0;
    # int colIndex = 0;
    # while (headCells.hasNext()) {
    # final HeaderCell hCell = (HeaderCell) headCells.next();
    # if (hCell.isDefinedWidth()) {
    # totalExplicitColumnsWidths += hCell.getWidth();
    # usedMinimumWidth += hCell.getWidth();
    # } else {
    # usedMinimumWidth += hCell.getNaturalColumnWidth(colIndex);
    # expandRatioDivider += hCell.getExpandRatio();
    # }
    # colIndex++;
    # }
    # int availW = scrollBody.getAvailableWidth();
    # // Hey IE, are you really sure about this?
    # availW = scrollBody.getAvailableWidth();
    # int visibleCellCount = tHead.getVisibleCellCount();
    # availW -= scrollBody.getCellExtraWidth() * visibleCellCount;
    # if (willHaveScrollbars()) {
    # availW -= Util.getNativeScrollbarSize();
    # }
    # int extraSpace = availW - usedMinimumWidth;
    # if (extraSpace < 0) {
    # extraSpace = 0;
    # }
    # int totalUndefinedNaturalWidths = usedMinimumWidth
    # - totalExplicitColumnsWidths;
    # // we have some space that can be divided optimally
    # HeaderCell hCell;
    # colIndex = 0;
    # headCells = tHead.iterator();
    # int checksum = 0;
    # while (headCells.hasNext()) {
    # hCell = (HeaderCell) headCells.next();
    # if (!hCell.isDefinedWidth()) {
    # int w = hCell.getNaturalColumnWidth(colIndex);
    # int newSpace;
    # if (expandRatioDivider > 0) {
    # // divide excess space by expand ratios
    # newSpace = Math.round((w + extraSpace
    # * hCell.getExpandRatio() / expandRatioDivider));
    # } else {
    # if (totalUndefinedNaturalWidths != 0) {
    # // divide relatively to natural column widths
    # newSpace = Math.round(w + (float) extraSpace
    # * (float) w / totalUndefinedNaturalWidths);
    # } else {
    # newSpace = w;
    # }
    # }
    # checksum += newSpace;
    # setColWidth(colIndex, newSpace, false);
    # } else {
    # checksum += hCell.getWidth();
    # }
    # colIndex++;
    # }
    # if (extraSpace > 0 && checksum != availW) {
    # /*
    # * There might be in some cases a rounding error of 1px when
    # * extra space is divided so if there is one then we give the
    # * first undefined column 1 more pixel
    # //
    # headCells = tHead.iterator();
    # colIndex = 0;
    # while (headCells.hasNext()) {
    # HeaderCell hc = (HeaderCell) headCells.next();
    # if (!hc.isDefinedWidth()) {
    # setColWidth(colIndex,
    # hc.getWidth() + availW - checksum, false);
    # break;
    # }
    # colIndex++;
    # }
    # }
    # if ((height == null || "".equals(height))
    # && totalRows == pageLength) {
    # // fix body height (may vary if lazy loading is offhorizontal
    # // scrollbar appears/disappears)
    # int bodyHeight = scrollBody.getRequiredHeight();
    # boolean needsSpaceForHorizontalScrollbar = (availW < usedMinimumWidth);
    # if (needsSpaceForHorizontalScrollbar) {
    # bodyHeight += Util.getNativeScrollbarSize();
    # }
    # int heightBefore = getOffsetHeight();
    # scrollBodyPanel.setHeight(bodyHeight + "px");
    # if (heightBefore != getOffsetHeight()) {
    # Util.notifyParentOfSizeChange(VScrollTable.this, false);
    # }
    # }
    # scrollBody.reLayoutComponents();
    # Scheduler.get().scheduleDeferred(new Command() {
    # public void execute() {
    # Util.runWebkitOverflowAutoFix(scrollBodyPanel.getElement());
    # }
    # });
    # forceRealignColumnHeaders();
    # }
    # };

    def forceRealignColumnHeaders(self):
        if BrowserInfo.get().isIE():
            # IE does not fire onscroll event if scroll position is reverted to
            # 0 due to the content element size growth. Ensure headers are in
            # sync with content manually. Safe to use null event as we don't
            # actually use the event object in listener.

            self.onScroll(None)

    def setContentWidth(self, pixels):
        """helper to set pixel size of head and body part

        @param pixels
        """
        self.tHead.setWidth(pixels + 'px')
        self._scrollBodyPanel.setWidth(pixels + 'px')
        self._tFoot.setWidth(pixels + 'px')

    _borderWidth = -1

    def getBorderWidth(self):
        """@return border left + border right"""
        # Ensures scrollable area is properly sized. This method is used when fixed
        # size is used.

        if self._borderWidth < 0:
            self._borderWidth = Util.measureHorizontalPaddingAndBorder(self._scrollBodyPanel.getElement(), 2)
            if self._borderWidth < 0:
                self._borderWidth = 0
        return self._borderWidth

    _containerHeight = None

    def setContainerHeight(self):
        if self._height is not None and not ('' == self._height):
            self._containerHeight = self.getOffsetHeight()
            self._containerHeight -= self.tHead.getOffsetHeight() if self._showColHeaders else 0
            self._containerHeight -= self._tFoot.getOffsetHeight()
            self._containerHeight -= self.getContentAreaBorderHeight()
            if self._containerHeight < 0:
                self._containerHeight = 0
            self._scrollBodyPanel.setHeight(self._containerHeight + 'px')

    _contentAreaBorderHeight = -1
    _scrollLeft = None
    _scrollTop = None
    _dropHandler = None
    _navKeyDown = None
    _multiselectPending = None

    def getContentAreaBorderHeight(self):
        """@return border top + border bottom of the scrollable area of table"""
        if self._contentAreaBorderHeight < 0:
            if BrowserInfo.get().isIE7() or BrowserInfo.get().isIE6():
                self._contentAreaBorderHeight = Util.measureVerticalBorder(self._scrollBodyPanel.getElement())
            else:
                DOM.setStyleAttribute(self._scrollBodyPanel.getElement(), 'overflow', 'hidden')
                oh = self._scrollBodyPanel.getOffsetHeight()
                ch = self._scrollBodyPanel.getElement().getPropertyInt('clientHeight')
                self._contentAreaBorderHeight = oh - ch
                DOM.setStyleAttribute(self._scrollBodyPanel.getElement(), 'overflow', 'auto')
        return self._contentAreaBorderHeight

    def setHeight(self, height):
        # Overridden due Table might not survive of visibility change (scroll pos
        # lost). Example ITabPanel just set contained components invisible and back
        # when changing tabs.

        self._height = height
        super(VScrollTable, self).setHeight(height)
        self.setContainerHeight()
        if self._initializedAndAttached:
            self.updatePageLength()
        if not self._rendering:
            # Webkit may sometimes get an odd rendering bug (white space
            # between header and body), see bug #3875. Running
            # overflow hack here to shake body element a bit.
            Util.runWebkitOverflowAutoFix(self._scrollBodyPanel.getElement())
        # setting height may affect wheter the component has scrollbars ->
        # needs scrolling or not

        self.setProperTabIndex()

    def setVisible(self, visible):
        if self.isVisible() != visible:
            super(VScrollTable, self).setVisible(visible)
            if self._initializedAndAttached:
                if visible:

                    class _15_(Command):

                        def execute(self):
                            VScrollTable_this._scrollBodyPanel.setScrollPosition(VScrollTable_this.measureRowHeightOffset(VScrollTable_this._firstRowInViewPort))

                    _15_ = _15_()
                    Scheduler.get().scheduleDeferred(_15_)

    def buildCaptionHtmlSnippet(self, uidl):
        """Helper function to build html snippet for column or row headers

        @param uidl
                   possibly with values caption and icon
        @return html snippet containing possibly an icon + caption text
        """
        s = uidl.getStringAttribute('caption') if uidl.hasAttribute('caption') else ''
        if uidl.hasAttribute('icon'):
            s = '<img src=\"' + Util.escapeAttribute(self.client.translateVaadinUri(uidl.getStringAttribute('icon'))) + '\" alt=\"icon\" class=\"v-icon\">' + s
        return s

    def onScroll(self, event):
        """This method has logic which rows needs to be requested from server when
        user scrolls
        """
        self._scrollLeft = self._scrollBodyPanel.getElement().getScrollLeft()
        self._scrollTop = self._scrollBodyPanel.getScrollPosition()
        if not self._initializedAndAttached:
            return
        if not self._enabled:
            self._scrollBodyPanel.setScrollPosition(self.measureRowHeightOffset(self._firstRowInViewPort))
            return
        self._rowRequestHandler.cancel()
        if BrowserInfo.get().isSafari() and event is not None and self._scrollTop == 0:
            # due to the webkitoverflowworkaround, top may sometimes report 0
            # for webkit, although it really is not. Expecting to have the
            # correct
            # value available soon.

            class _16_(Command):

                def execute(self):
                    VScrollTable_this.onScroll(None)

            _16_ = _16_()
            Scheduler.get().scheduleDeferred(_16_)
            return
        # fix headers horizontal scrolling
        self.tHead.setHorizontalScrollPosition(self._scrollLeft)
        # fix footers horizontal scrolling
        self._tFoot.setHorizontalScrollPosition(self._scrollLeft)
        self._firstRowInViewPort = self.calcFirstRowInViewPort()
        if self._firstRowInViewPort > self._totalRows - self._pageLength:
            self._firstRowInViewPort = self._totalRows - self._pageLength
        postLimit = self._firstRowInViewPort + (self._pageLength - 1) + (self._pageLength * self._cache_react_rate)
        if postLimit > self._totalRows - 1:
            postLimit = self._totalRows - 1
        preLimit = self._firstRowInViewPort - (self._pageLength * self._cache_react_rate)
        if preLimit < 0:
            preLimit = 0
        lastRendered = self._scrollBody.getLastRendered()
        firstRendered = self._scrollBody.getFirstRendered()
        if postLimit <= lastRendered and preLimit >= firstRendered:
            # remember which firstvisible we requested, in case the server has
            # a differing opinion
            self._lastRequestedFirstvisible = self._firstRowInViewPort
            self.client.updateVariable(self.paintableId, 'firstvisible', self._firstRowInViewPort, False)
            return
            # scrolled withing "non-react area"
        if (
            (self._firstRowInViewPort - (self._pageLength * self._cache_rate) > lastRendered) or (self._firstRowInViewPort + self._pageLength + (self._pageLength * self._cache_rate) < firstRendered)
        ):
            # need a totally new set
            self._rowRequestHandler.setReqFirstRow(self._firstRowInViewPort - (self._pageLength * self._cache_rate))
            last = (self._firstRowInViewPort + (self._cache_rate * self._pageLength) + self._pageLength) - 1
            if last >= self._totalRows:
                last = self._totalRows - 1
            self._rowRequestHandler.setReqRows((last - self._rowRequestHandler.getReqFirstRow()) + 1)
            self._rowRequestHandler.deferRowFetch()
            return
        if preLimit < firstRendered:
            # need some rows to the beginning of the rendered area
            self._rowRequestHandler.setReqFirstRow(self._firstRowInViewPort - (self._pageLength * self._cache_rate))
            self._rowRequestHandler.setReqRows(firstRendered - self._rowRequestHandler.getReqFirstRow())
            self._rowRequestHandler.deferRowFetch()
            return
        if postLimit > lastRendered:
            # need some rows to the end of the rendered area
            self._rowRequestHandler.setReqFirstRow(lastRendered + 1)
            self._rowRequestHandler.setReqRows((self._firstRowInViewPort + self._pageLength + (self._pageLength * self._cache_rate)) - lastRendered)
            self._rowRequestHandler.deferRowFetch()

    def calcFirstRowInViewPort(self):
        return self.Math.ceil(self._scrollTop / self._scrollBody.getRowHeight())

    def getDropHandler(self):
        return self._dropHandler

    def TableDDDetails(VScrollTable_this, *args, **kwargs):

        class TableDDDetails(object):
            _overkey = -1
            _dropLocation = None
            _colkey = None

            def equals(self, obj):
                # @Override
                # public int hashCode() {
                # return overkey;
                # }
                if isinstance(obj, VScrollTable_this.TableDDDetails):
                    other = obj
                    return self._dropLocation == other.dropLocation and self._overkey == other.overkey and (self._colkey is not None and self._colkey == other.colkey) or (self._colkey is None and other.colkey is None)
                return False

        return TableDDDetails(*args, **kwargs)

    def VScrollTableDropHandler(VScrollTable_this, *args, **kwargs):

        class VScrollTableDropHandler(VAbstractDropHandler):
            _ROWSTYLEBASE = 'v-table-row-drag-'
            _dropDetails = None
            _lastEmphasized = None

            def dragEnter(self, drag):
                self.updateDropDetails(drag)
                super(VScrollTableDropHandler, self).dragEnter(drag)

            def updateDropDetails(self, drag):
                self._dropDetails = VScrollTable_this.TableDDDetails()
                elementOver = drag.getElementOver()
                row = Util.findWidget(elementOver, self.getRowClass())
                if row is not None:
                    self._dropDetails.overkey = row.rowKey
                    tr = row.getElement()
                    element = elementOver
                    while element is not None and element.getParentElement() != tr:
                        element = element.getParentElement()
                    childIndex = DOM.getChildIndex(tr, element)
                    self._dropDetails.colkey = VScrollTable_this.tHead.getHeaderCell(childIndex).getColKey()
                    self._dropDetails.dropLocation = DDUtil.getVerticalDropLocation(row.getElement(), drag.getCurrentGwtEvent(), 0.2)
                drag.getDropDetails().put('itemIdOver', self._dropDetails.overkey + '')
                drag.getDropDetails().put('detail', str(self._dropDetails.dropLocation) if self._dropDetails.dropLocation is not None else None)

            def getRowClass(self):
                # get the row type this way to make dd work in derived
                # implementations
                return VScrollTable_this._scrollBody.next().getClass()

            def dragOver(self, drag):
                oldDetails = self._dropDetails
                self.updateDropDetails(drag)
                if not (oldDetails == self._dropDetails):
                    self.deEmphasis()
                    newDetails = self._dropDetails

                    class cb(VAcceptCallback):

                        def accepted(self, event):
                            if self.newDetails == VScrollTableDropHandler_this._dropDetails:
                                VScrollTableDropHandler_this.dragAccepted(event)
                            # Else new target slot already defined, ignore

                    self.validate(cb, drag)

            def dragLeave(self, drag):
                self.deEmphasis()
                super(VScrollTableDropHandler, self).dragLeave(drag)

            def drop(self, drag):
                self.deEmphasis()
                return super(VScrollTableDropHandler, self).drop(drag)

            def deEmphasis(self):
                UIObject.setStyleName(self.getElement(), VScrollTable_this.CLASSNAME + '-drag', False)
                if self._lastEmphasized is None:
                    return
                for w in VScrollTable_this._scrollBody.renderedRows:
                    row = w
                    if (
                        self._lastEmphasized is not None and row.rowKey == self._lastEmphasized.overkey
                    ):
                        stylename = self._ROWSTYLEBASE + str(self._lastEmphasized.dropLocation).toLowerCase()
                        VScrollTableRow.setStyleName(row.getElement(), stylename, False)
                        self._lastEmphasized = None
                        return

            def emphasis(self, details):
                """TODO needs different drop modes ?? (on cells, on rows), now only
                supports rows
                """
                self.deEmphasis()
                UIObject.setStyleName(self.getElement(), VScrollTable_this.CLASSNAME + '-drag', True)
                # iterate old and new emphasized row
                for w in VScrollTable_this._scrollBody.renderedRows:
                    row = w
                    if details is not None and details.overkey == row.rowKey:
                        stylename = self._ROWSTYLEBASE + str(details.dropLocation).toLowerCase()
                        VScrollTableRow.setStyleName(row.getElement(), stylename, True)
                        self._lastEmphasized = details
                        return

            def dragAccepted(self, drag):
                self.emphasis(self._dropDetails)

            def getPaintable(self):
                return VScrollTable_this

            def getApplicationConnection(self):
                return VScrollTable_this.client

        return VScrollTableDropHandler(*args, **kwargs)

    def getFocusedRow(self):
        return self._focusedRow

    def setRowFocus(self, row):
        """Moves the selection head to a specific row

        @param row
                   The row to where the selection head should move
        @return Returns true if focus was moved successfully, else false
        """
        if not self.isSelectable():
            return False
        # Remove previous selection
        if self._focusedRow is not None and self._focusedRow != row:
            self._focusedRow.removeStyleName(self.CLASSNAME_SELECTION_FOCUS)
        if row is not None:
            # Apply focus style to new selection
            row.addStyleName(self.CLASSNAME_SELECTION_FOCUS)
            # Trying to set focus on already focused row
            if row == self._focusedRow:
                return False
            # Set new focused row
            self._focusedRow = row
            self.ensureRowIsVisible(row)
            return True
        return False

    def ensureRowIsVisible(self, row):
        """Ensures that the row is visible

        @param row
                   The row to ensure is visible
        """
        Util.scrollIntoViewVertically(row.getElement())

    def handleNavigation(self, keycode, ctrl, shift):
        """Handles the keyboard events handled by the table

        @param event
                   The keyboard event received
        @return true iff the navigation event was handled
        """
        if (keycode == KeyCodes.KEY_TAB) or (keycode == KeyCodes.KEY_SHIFT):
            # Do not handle tab key
            return False
        # Down navigation
        if not self.isSelectable() and keycode == self.getNavigationDownKey():
            self._scrollBodyPanel.setScrollPosition(self._scrollBodyPanel.getScrollPosition() + self._scrollingVelocity)
            return True
        elif keycode == self.getNavigationDownKey():
            if self.isMultiSelectModeAny() and self.moveFocusDown():
                self.selectFocusedRow(ctrl, shift)
            elif self.isSingleSelectMode() and not shift and self.moveFocusDown():
                self.selectFocusedRow(ctrl, shift)
            return True
        # Up navigation
        if not self.isSelectable() and keycode == self.getNavigationUpKey():
            self._scrollBodyPanel.setScrollPosition(self._scrollBodyPanel.getScrollPosition() - self._scrollingVelocity)
            return True
        elif keycode == self.getNavigationUpKey():
            if self.isMultiSelectModeAny() and self.moveFocusUp():
                self.selectFocusedRow(ctrl, shift)
            elif self.isSingleSelectMode() and not shift and self.moveFocusUp():
                self.selectFocusedRow(ctrl, shift)
            return True
        if keycode == self.getNavigationLeftKey():
            # Left navigation
            self._scrollBodyPanel.setHorizontalScrollPosition(self._scrollBodyPanel.getHorizontalScrollPosition() - self._scrollingVelocity)
            return True
        elif keycode == self.getNavigationRightKey():
            # Right navigation
            self._scrollBodyPanel.setHorizontalScrollPosition(self._scrollBodyPanel.getHorizontalScrollPosition() + self._scrollingVelocity)
            return True
        # Select navigation
        if self.isSelectable() and keycode == self.getNavigationSelectKey():
            if self.isSingleSelectMode():
                wasSelected = self._focusedRow.isSelected()
                self.deselectAll()
                if (not wasSelected) or (not self._nullSelectionAllowed):
                    self._focusedRow.toggleSelection()
            else:
                self._focusedRow.toggleSelection()
                self.removeRowFromUnsentSelectionRanges(self._focusedRow)
            self.sendSelectedRows()
            return True
        # Page Down navigation
        if keycode == self.getNavigationPageDownKey():
            if self.isSelectable():
                # If selectable we plagiate MSW behaviour: first scroll to the
                # end of current view. If at the end, scroll down one page
                # length and keep the selected row in the bottom part of
                # visible area.

                if not self.isFocusAtTheEndOfTable():
                    lastVisibleRowInViewPort = self._scrollBody.getRowByRowIndex((self._firstRowInViewPort + self.getFullyVisibleRowCount()) - 1)
                    if (
                        lastVisibleRowInViewPort is not None and lastVisibleRowInViewPort != self._focusedRow
                    ):
                        # focused row is not at the end of the table, move
                        # focus and select the last visible row
                        self.setRowFocus(lastVisibleRowInViewPort)
                        self.selectFocusedRow(ctrl, shift)
                        self.sendSelectedRows()
                    else:
                        indexOfToBeFocused = self._focusedRow.getIndex() + self.getFullyVisibleRowCount()
                        if indexOfToBeFocused >= self._totalRows:
                            indexOfToBeFocused = self._totalRows - 1
                        toBeFocusedRow = self._scrollBody.getRowByRowIndex(indexOfToBeFocused)
                        if toBeFocusedRow is not None:
                            # if the next focused row is rendered
                            self.setRowFocus(toBeFocusedRow)
                            self.selectFocusedRow(ctrl, shift)
                            # TODO needs scrollintoview ?
                            self.sendSelectedRows()
                        else:
                            # scroll down by pixels and return, to wait for
                            # new rows, then select the last item in the
                            # viewport
                            self._selectLastItemInNextRender = True
                            self._multiselectPending = shift
                            self.scrollByPagelenght(1)
            else:
                # No selections, go page down by scrolling
                self.scrollByPagelenght(1)
            return True
        # Page Up navigation
        if keycode == self.getNavigationPageUpKey():
            if self.isSelectable():
                # If selectable we plagiate MSW behaviour: first scroll to the
                # end of current view. If at the end, scroll down one page
                # length and keep the selected row in the bottom part of
                # visible area.

                if not self.isFocusAtTheBeginningOfTable():
                    firstVisibleRowInViewPort = self._scrollBody.getRowByRowIndex(self._firstRowInViewPort)
                    if (
                        firstVisibleRowInViewPort is not None and firstVisibleRowInViewPort != self._focusedRow
                    ):
                        # focus is not at the beginning of the table, move
                        # focus and select the first visible row
                        self.setRowFocus(firstVisibleRowInViewPort)
                        self.selectFocusedRow(ctrl, shift)
                        self.sendSelectedRows()
                    else:
                        indexOfToBeFocused = self._focusedRow.getIndex() - self.getFullyVisibleRowCount()
                        if indexOfToBeFocused < 0:
                            indexOfToBeFocused = 0
                        toBeFocusedRow = self._scrollBody.getRowByRowIndex(indexOfToBeFocused)
                        if toBeFocusedRow is not None:
                            # if the next focused row
                            # is rendered
                            self.setRowFocus(toBeFocusedRow)
                            self.selectFocusedRow(ctrl, shift)
                            # TODO needs scrollintoview ?
                            self.sendSelectedRows()
                        else:
                            # unless waiting for the next rowset already
                            # scroll down by pixels and return, to wait for
                            # new rows, then select the last item in the
                            # viewport
                            self._selectFirstItemInNextRender = True
                            self._multiselectPending = shift
                            self.scrollByPagelenght(-1)
            else:
                # No selections, go page up by scrolling
                self.scrollByPagelenght(-1)
            return True
        # Goto start navigation
        if keycode == self.getNavigationStartKey():
            self._scrollBodyPanel.setScrollPosition(0)
            if self.isSelectable():
                if self._focusedRow is not None and self._focusedRow.getIndex() == 0:
                    return False
                else:
                    rowByRowIndex = self._scrollBody.next()
                    if rowByRowIndex.getIndex() == 0:
                        self.setRowFocus(rowByRowIndex)
                        self.selectFocusedRow(ctrl, shift)
                        self.sendSelectedRows()
                    elif ctrl:
                        self._focusFirstItemInNextRender = True
                    else:
                        self._selectFirstItemInNextRender = True
                        self._multiselectPending = shift
                    # first row of table will come in next row fetch
            return True
        # Goto end navigation
        if keycode == self.getNavigationEndKey():
            self._scrollBodyPanel.setScrollPosition(self._scrollBody.getOffsetHeight())
            if self.isSelectable():
                lastRendered = self._scrollBody.getLastRendered()
                if lastRendered + 1 == self._totalRows:
                    rowByRowIndex = self._scrollBody.getRowByRowIndex(lastRendered)
                    if self._focusedRow != rowByRowIndex:
                        self.setRowFocus(rowByRowIndex)
                        self.selectFocusedRow(ctrl, shift)
                        self.sendSelectedRows()
                elif ctrl:
                    self._focusLastItemInNextRender = True
                else:
                    self._selectLastItemInNextRender = True
                    self._multiselectPending = shift
            return True
        return False

    def isFocusAtTheBeginningOfTable(self):
        return self._focusedRow.getIndex() == 0

    def isFocusAtTheEndOfTable(self):
        return self._focusedRow.getIndex() + 1 >= self._totalRows

    def getFullyVisibleRowCount(self):
        return self._scrollBodyPanel.getOffsetHeight() / self._scrollBody.getRowHeight()

    def scrollByPagelenght(self, i):
        # (non-Javadoc)
        # 
        # @see
        # com.google.gwt.event.dom.client.FocusHandler#onFocus(com.google.gwt.event
        # .dom.client.FocusEvent)

        pixels = i * self._scrollBodyPanel.getOffsetHeight()
        newPixels = self._scrollBodyPanel.getScrollPosition() + pixels
        if newPixels < 0:
            newPixels = 0
        # else if too high, NOP (all know browsers accept illegally big
        # values here)
        self._scrollBodyPanel.setScrollPosition(newPixels)

    def onFocus(self, event):
        # (non-Javadoc)
        # 
        # @see
        # com.google.gwt.event.dom.client.BlurHandler#onBlur(com.google.gwt.event
        # .dom.client.BlurEvent)

        if self.isFocusable():
            self._hasFocus = True
            # Focus a row if no row is in focus
            if self._focusedRow is None:
                self.focusRowFromBody()
            else:
                self.setRowFocus(self._focusedRow)

    def onBlur(self, event):
        self._hasFocus = False
        self._navKeyDown = False
        if BrowserInfo.get().isIE():
            # IE sometimes moves focus to a clicked table cell...
            focusedElement = Util.getIEFocusedElement()
            if self.getElement().isOrHasChild(focusedElement):
                # ..in that case, steal the focus back to the focus handler
                self.focus()
                return
        if self.isFocusable():
            # Unfocus any row
            self.setRowFocus(None)

    def removeRowFromUnsentSelectionRanges(self, row):
        """Removes a key from a range if the key is found in a selected range

        @param key
                   The key to remove
        """
        newRanges = None
        _0 = True
        iterator = self._selectedRowRanges
        while True:
            if _0 is True:
                _0 = False
            if not iterator.hasNext():
                break
            range = iterator.next()
            if range.inRange(row):
                # Split the range if given row is in range
                splitranges = range.split(row)
                if newRanges is None:
                    newRanges = list()
                newRanges.addAll(splitranges)
                iterator.remove()
        if newRanges is not None:
            self._selectedRowRanges.addAll(newRanges)

    def isFocusable(self):
        """Can the Table be focused?

        @return True if the table can be focused, else false
        """
        if self._scrollBody is not None and self._enabled:
            return not (not self.hasHorizontalScrollbar() and not self.hasVerticalScrollbar() and not self.isSelectable())
        return False

    def hasHorizontalScrollbar(self):
        return self._scrollBody.getOffsetWidth() > self._scrollBodyPanel.getOffsetWidth()

    def hasVerticalScrollbar(self):
        # (non-Javadoc)
        # 
        # @see com.vaadin.terminal.gwt.client.Focusable#focus()

        return self._scrollBody.getOffsetHeight() > self._scrollBodyPanel.getOffsetHeight()

    def focus(self):
        if self.isFocusable():
            self._scrollBodyPanel.focus()

    def setProperTabIndex(self):
        """Sets the proper tabIndex for scrollBodyPanel (the focusable elemen in the
        component).

        If the component has no explicit tabIndex a zero is given (default
        tabbing order based on dom hierarchy) or -1 if the component does not
        need to gain focus. The component needs no focus if it has no scrollabars
        (not scrollable) and not selectable. Note that in the future shortcut
        actions may need focus.
        """
        storedScrollTop = 0
        storedScrollLeft = 0
        if BrowserInfo.get().getOperaVersion() >= 11:
            # Workaround for Opera scroll bug when changing tabIndex (#6222)
            storedScrollTop = self._scrollBodyPanel.getScrollPosition()
            storedScrollLeft = self._scrollBodyPanel.getHorizontalScrollPosition()
        if self._tabIndex == 0 and not self.isFocusable():
            self._scrollBodyPanel.setTabIndex(-1)
        else:
            self._scrollBodyPanel.setTabIndex(self._tabIndex)
        if BrowserInfo.get().getOperaVersion() >= 11:
            # Workaround for Opera scroll bug when changing tabIndex (#6222)
            self._scrollBodyPanel.setScrollPosition(storedScrollTop)
            self._scrollBodyPanel.setHorizontalScrollPosition(storedScrollLeft)

    def startScrollingVelocityTimer(self):
        if self._scrollingVelocityTimer is None:

            class _18_(Timer):

                def run(self):
                    VScrollTable_this._scrollingVelocity += 1

            _18_ = _18_()
            self._scrollingVelocityTimer = _18_
            self._scrollingVelocityTimer.scheduleRepeating(100)

    def cancelScrollingVelocityTimer(self):
        if self._scrollingVelocityTimer is not None:
            # Remove velocityTimer if it exists and the Table is disabled
            self._scrollingVelocityTimer.cancel()
            self._scrollingVelocityTimer = None
            self._scrollingVelocity = 10

    def isNavigationKey(self, keyCode):
        """@param keyCode
        @return true if the given keyCode is used by the table for navigation
        """
        return (((((((keyCode == self.getNavigationUpKey()) or (keyCode == self.getNavigationLeftKey())) or (keyCode == self.getNavigationRightKey())) or (keyCode == self.getNavigationDownKey())) or (keyCode == self.getNavigationPageUpKey())) or (keyCode == self.getNavigationPageDownKey())) or (keyCode == self.getNavigationEndKey())) or (keyCode == self.getNavigationStartKey())

    def lazyRevertFocusToRow(self, currentlyFocusedRow):

        class _19_(ScheduledCommand):

            def execute(self):
                if self.currentlyFocusedRow is not None:
                    VScrollTable_this.setRowFocus(self.currentlyFocusedRow)
                else:
                    VConsole.log('no row?')
                    VScrollTable_this.focusRowFromBody()
                VScrollTable_this._scrollBody.ensureFocus()

        _19_ = _19_()
        Scheduler.get().scheduleFinally(_19_)

    def getActions(self):
        if self._bodyActionKeys is None:
            return []
        actions = [None] * len(self._bodyActionKeys)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(actions)):
                break
            actionKey = self._bodyActionKeys[i]
            bodyAction = TreeAction(self, None, actionKey)
            bodyAction.setCaption(self.getActionCaption(actionKey))
            bodyAction.setIconUrl(self.getActionIcon(actionKey))
            actions[i] = bodyAction
        return actions

    def getClient(self):
        return self.client

    def getPaintableId(self):
        return self.paintableId

    @classmethod
    def getPreventTextSelectionIEHack(cls):
        """Add this to the element mouse down event by using element.setPropertyJSO
        ("onselectstart",applyDisableTextSelectionIEHack()); Remove it then again
        when the mouse is depressed in the mouse up event.

        @return Returns the JSO preventing text selection
        """
        JS("""
            return function(){ return false; };
    """)
        pass

    def triggerLazyColumnAdjustment(self, now):
        self.lazyAdjustColumnWidths.cancel()
        if now:
            self.lazyAdjustColumnWidths.run()
        else:
            self.lazyAdjustColumnWidths.schedule(self._LAZY_COLUMN_ADJUST_TIMEOUT)

    def debug(self, msg):
        if self._enableDebug:
            VConsole.error(msg)
