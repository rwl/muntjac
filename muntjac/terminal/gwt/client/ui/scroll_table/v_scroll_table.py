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

from __pyjamas__ import JS

from pyjamas import DOM, Window

from pyjamas.Timer import Timer

from pyjamas.ui import RootPanel
from pyjamas.ui import Event, KeyboardListener
from pyjamas.ui import FlowPanel

from pyjamas.ui.Widget import Widget
from pyjamas.ui.Panel import Panel

from muntjac.terminal.gwt.client.tooltip_info import TooltipInfo
from muntjac.terminal.gwt.client.ui.dd.dd_util import DDUtil
from muntjac.terminal.gwt.client.v_tooltip import VTooltip
from muntjac.terminal.gwt.client.util import Util
from muntjac.terminal.gwt.client.ui.v_label import VLabel
from muntjac.terminal.gwt.client.ui.dd.v_has_drop_handler import VHasDropHandler
from muntjac.terminal.gwt.client.v_console import VConsole
from muntjac.terminal.gwt.client.container import Container
from muntjac.terminal.gwt.client.ui.v_text_field import VTextField
from muntjac.terminal.gwt.client.ui.table import Table
from muntjac.terminal.gwt.client.ui.touch_scroll_delegate import TouchScrollDelegate
from muntjac.terminal.gwt.client.render_space import RenderSpace
from muntjac.terminal.gwt.client.ui.action_owner import ActionOwner
from muntjac.terminal.gwt.client.ui.tree_action import TreeAction
from muntjac.terminal.gwt.client.ui.focusable_scroll_panel import FocusableScrollPanel
from muntjac.terminal.gwt.client.ui.action import Action
from muntjac.terminal.gwt.client.mouse_event_details import MouseEventDetails
from muntjac.terminal.gwt.client.ui.dd.v_accept_callback import VAcceptCallback
from muntjac.terminal.gwt.client.ui.dd.v_transferable import VTransferable
from muntjac.terminal.gwt.client.browser_info import BrowserInfo
from muntjac.terminal.gwt.client.ui.v_embedded import VEmbedded
from muntjac.terminal.gwt.client.ui.dd.v_drag_and_drop_manager import VDragAndDropManager
from muntjac.terminal.gwt.client.ui.dd.v_abstract_drop_handler import VAbstractDropHandler
from muntjac.terminal.gwt.client.focusable import IFocusable
import math
from muntjac.terminal.gwt.client.ui.scroll_table.v_scroll_table_body import VScrollTableRow
from gwt.ui.UIObject import UIObject


class VScrollTable(FlowPanel, Table, IFocusable, ActionOwner, VHasDropHandler):
        #ScrollHandler, FocusHandler, BlurHandler):
    """VScrollTable is a FlowPanel having two widgets in it: * TableHead
    component * ScrollPanel

    TableHead contains table's header and widgets + logic for resizing,
    reordering and hiding columns.

    ScrollPanel contains VScrollTableBody object which handles content. To
    save some bandwidth and to improve clients responsiveness with loads of
    data, in VScrollTableBody all rows are not necessary rendered. There are
    "spacers" in VScrollTableBody to use the exact same space as non-rendered
    rows would use. This way we can use seamlessly traditional scrollbars and
    scrolling to fetch more rows instead of "paging".

    In VScrollTable we listen to scroll events. On horizontal scrolling we
    also update TableHeads scroll position which has its scrollbars hidden.
    On vertical scroll events we will check if we are reaching the end of area
    where we have rows rendered and

    TODO: implement unregistering for child components in Cells
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

    ALIGN_CENTER = 'c'
    ALIGN_LEFT = 'b'
    ALIGN_RIGHT = 'e'
    _CHARCODE_SPACE = 32

    _LAZY_COLUMN_ADJUST_TIMEOUT = 300

    def __init__(self):

        self.navKeyPressHandler = NavKeyPressHandler()
        self.navKeyUpHandler = NavKeyUpHandler()
        self.navKeyDownHandler = NavKeyDownHandler()

        # multiple of pagelength which component will cache when requesting more
        # rows
        self._cache_rate = self._CACHE_RATE_DEFAULT

        # fraction of pageLenght which can be scrolled without making new request
        self._cache_react_rate = 0.75 * self._cache_rate

        self._firstRowInViewPort = 0
        self._pageLength = 15
        self._lastRequestedFirstvisible = 0  # to detect "serverside scroll"
        self.showRowHeaders = False
        self._columnOrder = None
        self.client = None
        self.paintableId = None
        self._immediate = None
        self._nullSelectionAllowed = True
        self._selectMode = Table.SELECT_MODE_NONE
        self._selectedRowKeys = set()

        # When scrolling and selecting at the same time, the selections are not in
        # sync with the server while retrieving new rows (until key is released).
        self._unSyncedselectionsBeforeRowFetch = None

        # These are used when jumping between pages when pressing Home and End
        self._selectLastItemInNextRender = False
        self._selectFirstItemInNextRender = False
        self._focusFirstItemInNextRender = False
        self._focusLastItemInNextRender = False

        # The currently focused row
        self._focusedRow = None

        # Helper to store selection range start in when using the keyboard
        self._selectionRangeStart = None

        # Flag for notifying when the selection has changed and should be sent to
        # the server
        self._selectionChanged = False

        # The speed (in pixels) which the scrolling scrolls vertically/horizontally
        self._scrollingVelocity = 10
        self._scrollingVelocityTimer = None
        self._bodyActionKeys = None
        self._enableDebug = False

        self._selectedRowRanges = set()
        self._initializedAndAttached = False
        # Flag to indicate if a column width recalculation is needed due update.
        self._headerChangedDuringUpdate = False
        self.tHead = TableHead()
        self._tFoot = TableFooter()
        self._scrollBodyPanel = FocusableScrollPanel(True)

        self._totalRows = None
        self._collapsedColumns = None
        self._rowRequestHandler = None
        self._scrollBody = None
        self._firstvisible = 0
        self._sortAscending = None
        self._sortColumn = None
        self._oldSortColumn = None
        self._columnReordering = None

        # This map contains captions and icon urls for actions like: * "33_c" ->
        # "Edit" * "33_i" -> "http://dom.com/edit.png"
        self._actionMap = dict()
        self._visibleColOrder = None
        self._initialContentReceived = False
        self._scrollPositionElement = None
        self._enabled = None
        self._showColHeaders = None
        self._showColFooters = None

        # flag to indicate that table body has changed
        self._isNewBody = True

        # Read from the "recalcWidths" -attribute. When it is true, the table will
        # recalculate the widths for columns - desirable in some cases. For #1983,
        # marked experimental.
        self._recalcWidths = False
        self._lazyUnregistryBag = list()
        self._height = None
        self._width = ''
        self._rendering = False
        self._hasFocus = False
        self._dragmode = None
        self._multiselectmode = None
        self._tabIndex = None
        self._touchScrollDelegate = None
        self._lastRenderedHeight = None

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
        self._serverCacheFirst = -1
        self._serverCacheLast = -1

        self._borderWidth = -1
        self._containerHeight = None
        self._contentAreaBorderHeight = -1
        self._scrollLeft = None
        self._scrollTop = None
        self._dropHandler = None
        self._navKeyDown = None
        self._multiselectPending = None

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

            def __init__(self, st):
                self._st = st

            def onTouchStart(self, event):
                self._st.getTouchScrollDelegate().onTouchStart(event)

        _3_ = _3_()
        self._scrollBodyPanel.addDomHandler(_3_, TouchStartEvent.getType())
        self._scrollBodyPanel.sinkEvents(Event.ONCONTEXTMENU)

        class _4_(ContextMenuHandler):

            def __init__(self, st):
                self._st = st

            def onContextMenu(self, event):
                self._st.handleBodyContextMenu(event)

        _4_ = _4_()
        self._scrollBodyPanel.addDomHandler(_4_, ContextMenuEvent.getType())

        self.setStyleName(self.CLASSNAME)

        self.add(self.tHead)
        self.add(self._scrollBodyPanel)
        self.add(self._tFoot)

        self._rowRequestHandler = RowRequestHandler()

        self.lazyAdjustColumnWidths = LazyAdjustColumnWidths()


    def getTouchScrollDelegate(self):
        if self._touchScrollDelegate is None:
            self._touchScrollDelegate = TouchScrollDelegate(
                    self._scrollBodyPanel.getElement())
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
        """Fires a column resize event which sends the resize information to
        the server.

        @param columnId:
                   The columnId of the column which was resized
        @param originalWidth:
                   The width in pixels of the column before the resize event
        @param newWidth:
                   The width in pixels of the column after the resize event
        """
        self.client.updateVariable(self.paintableId, 'columnResizeEventColumn',
                columnId, False)
        self.client.updateVariable(self.paintableId, 'columnResizeEventPrev',
                originalWidth, False)
        self.client.updateVariable(self.paintableId, 'columnResizeEventCurr',
                newWidth, self._immediate)


    def sendColumnWidthUpdates(self, columns):
        """Non-immediate variable update of column widths for a collection
        of columns.

        @param columns:
                   the columns to trigger the events for.
        """
        newSizes = [None] * len(columns)
        ix = 0
        for cell in columns:
            newSizes[ix] = cell.getColKey() + ':' + cell.getWidth()
            ix += 1
        self.client.updateVariable(self.paintableId, 'columnWidthUpdates',
                newSizes, False)


    def moveFocusDown(self, offset=0):
        """Moves the focus down by 1+offset rows

        @return: Returns true if succeeded, else false if the selection could
                 not be move downwards
        """
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


    def moveFocusUp(self, offset=0):
        """Moves the focus row upwards by 1+offset rows

        @return: Returns true if succeeded, else false if the selection could
                 not be move upwards
        """
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


    def selectFocusedRow(self, ctrlSelect, shiftSelect):
        """Selects a row where the current selection head is

        @param ctrlSelect:
                   Is the selection a ctrl+selection
        @param shiftSelect:
                   Is the selection a shift+selection
        @return: Returns true
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


    def sendSelectedRows(self, immediately=None):
        """Sends the selection to the server if it has been changed since the
        last update/visit.

        @param immediately:
                   set to true to immediately send the rows
        """
        if immediately is None:
            immediately = self._immediate

        # Don't send anything if selection has not changed
        if not self._selectionChanged:
            return

        # Reset selection changed flag
        self._selectionChanged = False

        # Note: changing the immediateness of this might require changes to
        # "clickEvent" immediateness also.
        if self.isMultiSelectModeDefault():
            # Convert ranges to a set of strings
            ranges = set()
            for r in self._selectedRowRanges:
                ranges.add(str(r))

            # Send the selected row ranges
            self.client.updateVariable(self.paintableId, 'selectedRanges',
                    list(self._selectedRowRanges), False)

            # clean selectedRowKeys so that they don't contain excess values
            iterator = self._selectedRowKeys
            while iterator.hasNext():
                key = iterator.next()
                renderedRowByKey = self.getRenderedRowByKey(key)
                if renderedRowByKey is not None:
                    for r in self._selectedRowRanges:
                        if r.inRange(renderedRowByKey):
                            iterator.remove()
                else:
                    # orphaned selected key, must be in a range, ignore
                    iterator.remove()

        # Send the selected rows
        self.client.updateVariable(self.paintableId, 'selected',
                list(self._selectedRowKeys), immediately)


    def getNavigationUpKey(self):
        """Get the key that moves the selection head upwards. By default it
        is the up arrow key but by overriding this you can change the key to
        whatever you want.

        @return: The keycode of the key
        """
        return KeyboardListener.KEY_UP


    def getNavigationDownKey(self):
        """Get the key that moves the selection head downwards. By default it
        is the down arrow key but by overriding this you can change the key to
        whatever you want.

        @return: The keycode of the key
        """
        return KeyboardListener.KEY_DOWN


    def getNavigationLeftKey(self):
        """Get the key that scrolls to the left in the table. By default it is
        the left arrow key but by overriding this you can change the key to
        whatever you want.

        @return: The keycode of the key
        """
        return KeyboardListener.KEY_LEFT


    def getNavigationRightKey(self):
        """Get the key that scroll to the right on the table. By default it is
        the right arrow key but by overriding this you can change the key to
        whatever you want.

        @return: The keycode of the key
        """
        return KeyboardListener.KEY_RIGHT


    def getNavigationSelectKey(self):
        """Get the key that selects an item in the table. By default it is the
        space bar key but by overriding this you can change the key to whatever
        you want.
        """
        return self._CHARCODE_SPACE


    def getNavigationPageUpKey(self):
        """Get the key the moves the selection one page up in the table. By
        default this is the Page Up key but by overriding this you can change
        the key to whatever you want.
        """
        return KeyboardListener.KEY_PAGEUP


    def getNavigationPageDownKey(self):
        """Get the key the moves the selection one page down in the table. By
        default this is the Page Down key but by overriding this you can change
        the key to whatever you want.
        """
        return KeyboardListener.KEY_PAGEDOWN


    def getNavigationStartKey(self):
        """Get the key the moves the selection to the beginning of the table.
        By default this is the Home key but by overriding this you can change
        the key to whatever you want.
        """
        return KeyboardListener.KEY_HOME


    def getNavigationEndKey(self):
        """Get the key the moves the selection to the end of the table. By
        default this is the End key but by overriding this you can change the
        key to whatever you want.
        """
        return KeyboardListener.KEY_END


    def updateFromUIDL(self, uidl, client):
        self._rendering = True

        if uidl.hasAttribute(self.ATTRIBUTE_PAGEBUFFER_FIRST):
            self._serverCacheFirst = uidl.getIntAttribute(
                    self.ATTRIBUTE_PAGEBUFFER_FIRST)
            self._serverCacheLast = uidl.getIntAttribute(
                    self.ATTRIBUTE_PAGEBUFFER_LAST)
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
            self._scrollBodyPanel.getElement().getStyle().setPosition(
                    'static')#Position.STATIC)
        elif BrowserInfo.get().isIE8():
            self._scrollBodyPanel.getElement().getStyle().setPosition(
                    'relative')#Position.RELATIVE)

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
                self._dropHandler = VScrollTableDropHandler()
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
                    self.updateBody(rowData, uidl.getIntAttribute('firstrow'),
                            uidl.getIntAttribute('rows'))
                    if self._headerChangedDuringUpdate:
                        self.triggerLazyColumnAdjustment(True)
                    elif ((not self.isScrollPositionVisible())
                            or totalRowsChanged
                            or (self._lastRenderedHeight
                                    != self._scrollBody.getOffsetHeight())):
                        # webkits may still bug with their disturbing scrollbar
                        # bug, see #3457
                        # Run overflow fix for the scrollable area
                        # #6698 - If there's a scroll going on, don't abort it
                        # by changing overflows as the length of the contents
                        # *shouldn't* have changed (unless the number of rows
                        # or the height of the widget has also changed)
                        class _5_(Command):

                            def __init__(self):
                                self._st = st

                            def execute(self):
                                Util.runWebkitOverflowAutoFix(
                                    self._st._scrollBodyPanel.getElement())

                        _5_ = _5_()
                        Scheduler.get().scheduleDeferred(_5_)
                else:
                    self.initializeRows(uidl, rowData)

        if not self.isSelectable():
            self._scrollBody.addStyleName(self.CLASSNAME
                    + '-body-noselection')
        else:
            self._scrollBody.removeStyleName(self.CLASSNAME
                    + '-body-noselection')

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
            self.selectFirstRenderedRowInViewPort(
                    self._focusFirstItemInNextRender)
            self._selectFirstItemInNextRender = False
            self._focusFirstItemInNextRender = False

        # This is called when the page down or end button has been pressed in
        # selectable mode and the next selected row was not yet rendered in the
        # client
        if self._selectLastItemInNextRender or self._focusLastItemInNextRender:
            self.selectLastRenderedRowInViewPort(
                    self._focusLastItemInNextRender)
            self._selectLastItemInNextRender = False
            self._focusLastItemInNextRender = False

        self._multiselectPending = False

        if self._focusedRow is not None:
            if (not self._focusedRow.isAttached()
                    and not self._rowRequestHandler.isRunning()):
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

        self._scrollBody.renderInitialRows(rowData,
                uidl.getIntAttribute('firstrow'),
                uidl.getIntAttribute('rows'))
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
            self._collapsedColumns = uidl.getStringArrayVariableAsSet(
                    'collapsedcolumns')
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
                    if (not selected
                            and self._unSyncedselectionsBeforeRowFetch is not None
                            and row.getKey() in self._unSyncedselectionsBeforeRowFetch):
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

        if (self._firstvisible != self._lastRequestedFirstvisible
                and self._scrollBody is not None):
            # received 'surprising' firstvisible from server: scroll there
            self._firstRowInViewPort = self._firstvisible
            self._scrollBodyPanel.setScrollPosition(
                    self.measureRowHeightOffset(self._firstvisible))


    def measureRowHeightOffset(self, rowIx):
        return rowIx * self._scrollBody.getRowHeight()


    def updatePageLength(self, uidl=None):
        """Determines the pagelength when the table height is fixed.
        """
        if uidl is None:
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
                self.client.updateVariable(self.paintableId, 'pagelength',
                        self._pageLength, False)
                if not self._rendering:
                    currentlyVisible = (self._scrollBody.lastRendered
                            - self._scrollBody.firstRendered)
                    if (currentlyVisible < self._pageLength
                            and currentlyVisible < self._totalRows):
                        # shake scrollpanel to fill empty space
                        self._scrollBodyPanel.setScrollPosition(
                                self._scrollTop + 1)
                        self._scrollBodyPanel.setScrollPosition(
                                self._scrollTop - 1)
        else:
            oldPageLength = self._pageLength
            if uidl.hasAttribute('pagelength'):
                self._pageLength = uidl.getIntAttribute('pagelength')
            else:
                # pagelenght is "0" meaning scrolling is turned off
                self._pageLength = self._totalRows
            if ((oldPageLength != self._pageLength)
                    and self._initializedAndAttached):
                # page length changed, need to update size
                self.sizeInit()


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
                self.getElement().setPropertyJSO('onselectstart',
                        self.getPreventTextSelectionIEHack())
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
                    self.setRowFocus(self._scrollBody.getRowByRowIndex(
                            self._firstRowInViewPort))
                else:
                    self.setRowFocus(renderedRow)
        else:
            # multiselect mode
            self.setRowFocus(self._scrollBody.getRowByRowIndex(
                    self._firstRowInViewPort))


    def createScrollBody(self):
        return VScrollTableBody()


    def selectLastRenderedRowInViewPort(self, focusOnly):
        """Selects the last row visible in the table

        @param focusOnly:
                   Should the focus only be moved to the last row
        """
        index = self._firstRowInViewPort + self.getFullyVisibleRowCount()
        lastRowInViewport = self._scrollBody.getRowByRowIndex(index)
        if lastRowInViewport is None:
            # this should not happen in normal situations (white space at the
            # end of viewport). Select the last rendered as a fallback.
            lastRowInViewport = self._scrollBody.getRowByRowIndex(
                    self._scrollBody.getLastRendered())
            if lastRowInViewport is None:
                return  # empty table

        self.setRowFocus(lastRowInViewport)
        if not focusOnly:
            self.selectFocusedRow(False, self._multiselectPending)
            self.sendSelectedRows()


    def selectFirstRenderedRowInViewPort(self, focusOnly):
        """Selects the first row visible in the table

        @param focusOnly:
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
        iterator = self._lazyUnregistryBag
        while iterator.hasNext():
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
            self._actionMap[key + '_c'] = caption
            if action.hasAttribute('icon'):
                # TODO: need some uri handling ??
                self._actionMap[key + '_i'] = self.client.translateVaadinUri(
                        action.getStringAttribute('icon'))
            else:
                del self._actionMap[key + '_i']


    def getActionCaption(self, actionKey):
        return self._actionMap.get(actionKey + '_c')


    def getActionIcon(self, actionKey):
        return self._actionMap.get(actionKey + '_i')


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

        for cid in strings:
            self._visibleColOrder[colIndex] = cid
            self.tHead.enableColumn(cid, colIndex)
            colIndex += 1

        self.tHead.setVisible(self._showColHeaders)
        self.setContainerHeight()


    def updateFooter(self, strings):
        """Updates footers.

        Update headers whould be called before this method is called!
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

        for cid in strings:
            self._tFoot.enableColumn(cid, colIndex)
            colIndex += 1

        self._tFoot.setVisible(self._showColFooters)


    def updateBody(self, uidl, firstRow, reqRows):
        """@param uidl:
                   which contains row data
        @param firstRow:
                   first row in data set
        @param reqRows:
                   amount of rows in data set
        """
        if (uidl is None) or (reqRows < 1):
            # container is empty, remove possibly existing rows
            if firstRow <= 0:
                while (self._scrollBody.getLastRendered()
                        > self._scrollBody.firstRendered):
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
        """Updates the internal cache by unlinking rows that fall outside of
        the caching window.
        """
        firstRowToKeep = (self._firstRowInViewPort
                - (self._pageLength * self._cache_rate))
        lastRowToKeep = (self._firstRowInViewPort + self._pageLength
                + (self._pageLength * self._cache_rate))
        self.debug('Client side calculated cache rows to keep: '
                + firstRowToKeep + '-' + lastRowToKeep)

        if self._serverCacheFirst != -1:
            firstRowToKeep = self._serverCacheFirst
            lastRowToKeep = self._serverCacheLast
            self.debug('Server cache rows that override: '
                    + self._serverCacheFirst + '-' + self._serverCacheLast)

            if ((firstRowToKeep < self._scrollBody.getFirstRendered())
                    or (lastRowToKeep > self._scrollBody.getLastRendered())):
                self.debug('*** Server wants us to keep '
                        + self._serverCacheFirst + '-' + self._serverCacheLast
                        + ' but we only have rows '
                        + self._scrollBody.getFirstRendered() + '-'
                        + self._scrollBody.getLastRendered() + ' rendered!')
        self.discardRowsOutsideOf(firstRowToKeep, lastRowToKeep)
        self._scrollBody.fixSpacers()
        self._scrollBody.restoreRowVisibility()


    def discardRowsOutsideOf(self, optimalFirstRow, optimalLastRow):
        # firstDiscarded and lastDiscarded are only calculated for debug
        # purposes
        firstDiscarded = -1
        lastDiscarded = -1
        cont = True
        while (cont and self._scrollBody.getLastRendered() > optimalFirstRow
                and self._scrollBody.getFirstRendered() < optimalFirstRow):
            if firstDiscarded == -1:
                firstDiscarded = self._scrollBody.getFirstRendered()

            # removing row from start
            cont = self._scrollBody.unlinkRow(True)

        if firstDiscarded != -1:
            lastDiscarded = self._scrollBody.getFirstRendered() - 1
            self.debug('Discarded rows ' + firstDiscarded + '-'
                    + lastDiscarded)

        firstDiscarded = lastDiscarded = -1

        cont = True
        while cont and self._scrollBody.getLastRendered() > optimalLastRow:
            if lastDiscarded == -1:
                lastDiscarded = self._scrollBody.getLastRendered()

            # removing row from the end
            cont = self._scrollBody.unlinkRow(False)

        if lastDiscarded != -1:
            firstDiscarded = self._scrollBody.getLastRendered() + 1
            self.debug('Discarded rows ' + firstDiscarded + '-'
                    + lastDiscarded)

        self.debug('Now in cache: ' + self._scrollBody.getFirstRendered()
                + '-' + self._scrollBody.getLastRendered())


    def addAndRemoveRows(self, partialRowAdditions):
        """Inserts rows in the table body or removes them from the table body
        based on the commands in the UIDL.

        @param partialRowAdditions:
                   the UIDL containing row updates.
        """
        if partialRowAdditions is None:
            return

        if partialRowAdditions.hasAttribute('hide'):
            self._scrollBody.unlinkAndReindexRows(
                    partialRowAdditions.getIntAttribute('firstprowix'),
                    partialRowAdditions.getIntAttribute('numprows'))
            self._scrollBody.ensureCacheFilled()
        elif partialRowAdditions.hasAttribute('delbelow'):
            self._scrollBody.insertRowsDeleteBelow(partialRowAdditions,
                    partialRowAdditions.getIntAttribute('firstprowix'),
                    partialRowAdditions.getIntAttribute('numprows'))
        else:
            self._scrollBody.insertAndReindexRows(partialRowAdditions,
                    partialRowAdditions.getIntAttribute('firstprowix'),
                    partialRowAdditions.getIntAttribute('numprows'))
        self.discardRowsOutsideCacheWindow()


    def getColIndexByKey(self, colKey):
        """Gives correct column index for given column key ("cid" in UIDL).

        @return: column index of visible columns, -1 if column not visible
        """
        # return 0 if asked for rowHeaders
        if self._ROW_HEADER_COLUMN_KEY == colKey:
            return 0

        for i in range(len(self._visibleColOrder)):
            if self._visibleColOrder[i] == colKey:
                return i
        return -1


    def isMultiSelectModeSimple(self):
        return (self._selectMode == Table.SELECT_MODE_MULTI
                and self._multiselectmode == self._MULTISELECT_MODE_SIMPLE)


    def isSingleSelectMode(self):
        return self._selectMode == Table.SELECT_MODE_SINGLE


    def isMultiSelectModeAny(self):
        return self._selectMode == Table.SELECT_MODE_MULTI


    def isMultiSelectModeDefault(self):
        return (self._selectMode == Table.SELECT_MODE_MULTI
                and self._multiselectmode == self._MULTISELECT_MODE_DEFAULT)


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

        @param key:
                   The key to search with
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

        @param row:
                   The row to calculate from
        @return: The next row or null if no row exists
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

        @param row:
                   The row to calculate from
        @return: The previous row or null if no row exists
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
        for i in range(len(self._columnOrder)):
            if self._columnOrder[i] == oldKeyOnNewIndex:
                break  # break loop at target

            if self.isCollapsedColumn(self._columnOrder[i]):
                newIndex += 1

        # finally we can build the new columnOrder for server
        newOrder = [None] * len(self._columnOrder)
        j = 0
        for i in range(len(newOrder)):
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
        for j in range(len(newOrder)):
            cid = newOrder[j]
            if not self.isCollapsedColumn(cid):
                self._visibleColOrder[i] = cid
                i += 1

        self.client.updateVariable(self.paintableId, 'columnorder',
                self._columnOrder, False)
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

        # TODO: refactor this code to be the same as in resize timer
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
                        newSpace = round(extraSpace *
                                (hCell.getExpandRatio() / expandRatioDivider))
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
                        newSpace = round((extraSpace * w) / totalWidthR)
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
                bodyHeight = round(self._scrollBody.getRowHeight(True)
                        * self._pageLength)

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

                def __init__(self, st):
                    self._st = st

                def execute(self):
                    self._st._scrollBodyPanel.setScrollPosition(
                            self._st.measureRowHeightOffset(
                                    self._st._firstvisible))
                    self._st._firstRowInViewPort = self._st._firstvisible

            _6_ = _6_()
            Scheduler.get().scheduleDeferred(_6_)

        if self._enabled:
            # Do we need cache rows
            if (self._scrollBody.getLastRendered() + 1
                    < self._firstRowInViewPort + self._pageLength
                            + (self._cache_react_rate * self._pageLength)):
                if self._totalRows - 1 > self._scrollBody.getLastRendered():
                    # fetch cache rows
                    firstInNewSet = self._scrollBody.getLastRendered() + 1
                    self._rowRequestHandler.setReqFirstRow(firstInNewSet)
                    lastInNewSet = (self._firstRowInViewPort + self._pageLength
                            + (self._cache_rate * self._pageLength))
                    if lastInNewSet > self._totalRows - 1:
                        lastInNewSet = self._totalRows - 1
                    self._rowRequestHandler.setReqRows(
                            (lastInNewSet - firstInNewSet) + 1)
                    self._rowRequestHandler.deferRowFetch(1)

        # Ensures the column alignments are correct at initial loading. <br/>
        # (child components widths are correct)
        self._scrollBody.reLayoutComponents()

        class _7_(Command):

            def __init__(self, st):
                self._st = st

            def execute(self):
                Util.runWebkitOverflowAutoFix(
                        self._st._scrollBodyPanel.getElement())

        _7_ = _7_()
        Scheduler.get().scheduleDeferred(_7_)


    def willHaveScrollbars(self):
        """Note, this method is not official api although declared as
        protected. Extend at you own risk.

        @return: true if content area will have scrollbars visible.
        """
        if not (self._height is not None and not (self._height == '')):
            if self._pageLength < self._totalRows:
                return True
        else:
            fakeheight = round(self._scrollBody.getRowHeight()
                    * self._totalRows)
            availableHeight = self._scrollBodyPanel.getElement().getPropertyInt(
                    'clientHeight')
            if fakeheight > availableHeight:
                return True

        return False


    def announceScrollPosition(self):
        if self._scrollPositionElement is None:
            self._scrollPositionElement = DOM.createDiv()
            self._scrollPositionElement.setClassName(self.CLASSNAME
                    + '-scrollposition')
            self._scrollPositionElement.getStyle().setPosition('absolute')#Position.ABSOLUTE)
            self._scrollPositionElement.getStyle().setDisplay('none')#Display.NONE)
            self.getElement().appendChild(self._scrollPositionElement)

        style = self._scrollPositionElement.getStyle()
        style.setMarginLeft((self.getElement().getOffsetWidth() / 2) - 80, 'px')#Unit.PX)
        style.setMarginTop(-self._scrollBodyPanel.getOffsetHeight(), 'px')#Unit.PX)

        # indexes go from 1-totalRows, as rowheaders in index-mode indicate
        last = self._firstRowInViewPort + self._pageLength
        if last > self._totalRows:
            last = self._totalRows

        self._scrollPositionElement.setInnerHTML('<span>'
                + self._firstRowInViewPort + 1 + ' &ndash; '
                + last + '...' + '</span>')
        style.setDisplay('block')#Display.BLOCK)


    def hideScrollPositionAnnotation(self):
        if self._scrollPositionElement is not None:
            DOM.setStyleAttribute(self._scrollPositionElement, 'display',
                    'none')


    def isScrollPositionVisible(self):
        return self._scrollPositionElement is not None and not (self._scrollPositionElement.getStyle().getDisplay() == 'none')#Display.NONE))


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


    def getBorderWidth(self):
        """@return border left + border right"""
        # Ensures scrollable area is properly sized. This method is used when fixed
        # size is used.

        if self._borderWidth < 0:
            self._borderWidth = Util.measureHorizontalPaddingAndBorder(
                    self._scrollBodyPanel.getElement(), 2)
            if self._borderWidth < 0:
                self._borderWidth = 0
        return self._borderWidth


    def setContainerHeight(self):
        if self._height is not None and not ('' == self._height):
            self._containerHeight = self.getOffsetHeight()
            self._containerHeight -= \
                    self.tHead.getOffsetHeight() if self._showColHeaders else 0
            self._containerHeight -= self._tFoot.getOffsetHeight()
            self._containerHeight -= self.getContentAreaBorderHeight()
            if self._containerHeight < 0:
                self._containerHeight = 0
            self._scrollBodyPanel.setHeight(self._containerHeight + 'px')


    def getContentAreaBorderHeight(self):
        """@return: border top + border bottom of the scrollable area of
        table"""
        if self._contentAreaBorderHeight < 0:
            if BrowserInfo.get().isIE7() or BrowserInfo.get().isIE6():
                self._contentAreaBorderHeight = Util.measureVerticalBorder(
                        self._scrollBodyPanel.getElement())
            else:
                DOM.setStyleAttribute(self._scrollBodyPanel.getElement(),
                        'overflow', 'hidden')
                oh = self._scrollBodyPanel.getOffsetHeight()
                ch = self._scrollBodyPanel.getElement().getPropertyInt(
                        'clientHeight')
                self._contentAreaBorderHeight = oh - ch
                DOM.setStyleAttribute(self._scrollBodyPanel.getElement(),
                        'overflow', 'auto')
        return self._contentAreaBorderHeight


    def setHeight(self, height):
        # Overridden due Table might not survive of visibility change (scroll
        # pos lost). Example ITabPanel just set contained components invisible
        # and back when changing tabs.
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

        @param uidl:
                   possibly with values caption and icon
        @return: html snippet containing possibly an icon + caption text
        """
        s = uidl.getStringAttribute('caption') if uidl.hasAttribute('caption') else ''
        if uidl.hasAttribute('icon'):
            s = '<img src=\"' + Util.escapeAttribute(self.client.translateVaadinUri(uidl.getStringAttribute('icon'))) + '\" alt=\"icon\" class=\"v-icon\">' + s
        return s


    def onScroll(self, event):
        """This method has logic which rows needs to be requested from server
        when user scrolls
        """
        self._scrollLeft = self._scrollBodyPanel.getElement().getScrollLeft()
        self._scrollTop = self._scrollBodyPanel.getScrollPosition()

        if not self._initializedAndAttached:
            return

        if not self._enabled:
            self._scrollBodyPanel.setScrollPosition(self.measureRowHeightOffset(self._firstRowInViewPort))
            return

        self._rowRequestHandler.cancel()

        if (BrowserInfo.get().isSafari() and event is not None
                and self._scrollTop == 0):
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

        postLimit = (self._firstRowInViewPort + (self._pageLength - 1)
                + (self._pageLength * self._cache_react_rate))

        if postLimit > self._totalRows - 1:
            postLimit = self._totalRows - 1

        preLimit = (self._firstRowInViewPort
                - (self._pageLength * self._cache_react_rate))
        if preLimit < 0:
            preLimit = 0

        lastRendered = self._scrollBody.getLastRendered()
        firstRendered = self._scrollBody.getFirstRendered()

        if postLimit <= lastRendered and preLimit >= firstRendered:
            # remember which firstvisible we requested, in case the server has
            # a differing opinion
            self._lastRequestedFirstvisible = self._firstRowInViewPort
            self.client.updateVariable(self.paintableId, 'firstvisible',
                    self._firstRowInViewPort, False)
            return  # scrolled withing "non-react area"

        if ((self._firstRowInViewPort
                - (self._pageLength * self._cache_rate) > lastRendered)
                or (self._firstRowInViewPort + self._pageLength
                        + (self._pageLength * self._cache_rate) < firstRendered)):
            # need a totally new set
            self._rowRequestHandler.setReqFirstRow(self._firstRowInViewPort
                    - (self._pageLength * self._cache_rate))

            last = (self._firstRowInViewPort + (self._cache_rate * self._pageLength) + self._pageLength) - 1
            if last >= self._totalRows:
                last = self._totalRows - 1

            self._rowRequestHandler.setReqRows((last
                    - self._rowRequestHandler.getReqFirstRow()) + 1)
            self._rowRequestHandler.deferRowFetch()
            return

        if preLimit < firstRendered:
            # need some rows to the beginning of the rendered area
            self._rowRequestHandler.setReqFirstRow(self._firstRowInViewPort
                    - (self._pageLength * self._cache_rate))
            self._rowRequestHandler.setReqRows(firstRendered
                    - self._rowRequestHandler.getReqFirstRow())
            self._rowRequestHandler.deferRowFetch()
            return

        if postLimit > lastRendered:
            # need some rows to the end of the rendered area
            self._rowRequestHandler.setReqFirstRow(lastRendered + 1)
            self._rowRequestHandler.setReqRows((self._firstRowInViewPort
                    + self._pageLength + (self._pageLength * self._cache_rate))
                            - lastRendered)
            self._rowRequestHandler.deferRowFetch()


    def calcFirstRowInViewPort(self):
        return math.ceil(self._scrollTop / self._scrollBody.getRowHeight())


    def getDropHandler(self):
        return self._dropHandler


    def getFocusedRow(self):
        return self._focusedRow


    def setRowFocus(self, row):
        """Moves the selection head to a specific row

        @param row:
                   The row to where the selection head should move
        @return: Returns true if focus was moved successfully, else false
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

        @param row:
                   The row to ensure is visible
        """
        Util.scrollIntoViewVertically(row.getElement())


    def handleNavigation(self, keycode, ctrl, shift):
        """Handles the keyboard events handled by the table

        @param event:
                   The keyboard event received
        @return: true iff the navigation event was handled
        """
        if ((keycode == KeyboardListener.KEY_TAB)
                or (keycode == KeyboardListener.KEY_SHIFT)):
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
                    lastVisibleRowInViewPort = \
                        self._scrollBody.getRowByRowIndex(
                                (self._firstRowInViewPort
                                        + self.getFullyVisibleRowCount()) - 1)

                    if (lastVisibleRowInViewPort is not None
                            and lastVisibleRowInViewPort != self._focusedRow):
                        # focused row is not at the end of the table, move
                        # focus and select the last visible row
                        self.setRowFocus(lastVisibleRowInViewPort)
                        self.selectFocusedRow(ctrl, shift)
                        self.sendSelectedRows()
                    else:
                        indexOfToBeFocused = (self._focusedRow.getIndex()
                                + self.getFullyVisibleRowCount())

                        if indexOfToBeFocused >= self._totalRows:
                            indexOfToBeFocused = self._totalRows - 1

                        toBeFocusedRow = self._scrollBody.getRowByRowIndex(
                                indexOfToBeFocused)

                        if toBeFocusedRow is not None:
                            # if the next focused row is rendered
                            self.setRowFocus(toBeFocusedRow)
                            self.selectFocusedRow(ctrl, shift)
                            # TODO: needs scrollintoview ?
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
                    firstVisibleRowInViewPort = \
                            self._scrollBody.getRowByRowIndex(
                                    self._firstRowInViewPort)

                    if (firstVisibleRowInViewPort is not None
                            and firstVisibleRowInViewPort != self._focusedRow):
                        # focus is not at the beginning of the table, move
                        # focus and select the first visible row
                        self.setRowFocus(firstVisibleRowInViewPort)
                        self.selectFocusedRow(ctrl, shift)
                        self.sendSelectedRows()
                    else:
                        indexOfToBeFocused = (self._focusedRow.getIndex()
                                - self.getFullyVisibleRowCount())

                        if indexOfToBeFocused < 0:
                            indexOfToBeFocused = 0

                        toBeFocusedRow = self._scrollBody.getRowByRowIndex(
                                indexOfToBeFocused)

                        if toBeFocusedRow is not None:
                            # if the next focused row
                            # is rendered
                            self.setRowFocus(toBeFocusedRow)
                            self.selectFocusedRow(ctrl, shift)
                            # TODO: needs scrollintoview ?
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
                if (self._focusedRow is not None
                        and self._focusedRow.getIndex() == 0):
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
            self._scrollBodyPanel.setScrollPosition(
                    self._scrollBody.getOffsetHeight())

            if self.isSelectable():
                lastRendered = self._scrollBody.getLastRendered()
                if lastRendered + 1 == self._totalRows:
                    rowByRowIndex = \
                            self._scrollBody.getRowByRowIndex(lastRendered)

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
        return (self._scrollBodyPanel.getOffsetHeight()
                / self._scrollBody.getRowHeight())


    def scrollByPagelenght(self, i):
        pixels = i * self._scrollBodyPanel.getOffsetHeight()
        newPixels = self._scrollBodyPanel.getScrollPosition() + pixels
        if newPixels < 0:
            newPixels = 0
        # else if too high, NOP (all know browsers accept illegally big
        # values here)
        self._scrollBodyPanel.setScrollPosition(newPixels)


    def onFocus(self, event):
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

        @param key:
                   The key to remove
        """
        newRanges = None
        iterator = self._selectedRowRanges
        while iterator.hasNext():
            range = iterator.next()
            if range.inRange(row):
                # Split the range if given row is in range
                splitranges = range.split(row)
                if newRanges is None:
                    newRanges = list()
                newRanges.extend(splitranges)
                iterator.remove()

        if newRanges is not None:
            self._selectedRowRanges.addAll(newRanges)


    def isFocusable(self):
        """Can the Table be focused?

        @return: True if the table can be focused, else false
        """
        if self._scrollBody is not None and self._enabled:
            return not (not self.hasHorizontalScrollbar()
                    and not self.hasVerticalScrollbar()
                    and not self.isSelectable())
        return False


    def hasHorizontalScrollbar(self):
        return (self._scrollBody.getOffsetWidth()
                > self._scrollBodyPanel.getOffsetWidth())


    def hasVerticalScrollbar(self):
        return (self._scrollBody.getOffsetHeight()
                > self._scrollBodyPanel.getOffsetHeight())


    def focus(self):
        if self.isFocusable():
            self._scrollBodyPanel.focus()


    def setProperTabIndex(self):
        """Sets the proper tabIndex for scrollBodyPanel (the focusable elemen
        in the component).

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
        return ((keyCode == self.getNavigationUpKey())
                or (keyCode == self.getNavigationLeftKey())
                or (keyCode == self.getNavigationRightKey())
                or (keyCode == self.getNavigationDownKey())
                or (keyCode == self.getNavigationPageUpKey())
                or (keyCode == self.getNavigationPageDownKey())
                or (keyCode == self.getNavigationEndKey())
                or (keyCode == self.getNavigationStartKey()))


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
        for i in range(len(actions)):
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
        """Add this to the element mouse down event by using
        element.setPropertyJSO
        ("onselectstart",applyDisableTextSelectionIEHack()); Remove it
        then again when the mouse is depressed in the mouse up event.

        @return: Returns the JSO preventing text selection
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
            self.lazyAdjustColumnWidths.schedule(
                    self._LAZY_COLUMN_ADJUST_TIMEOUT)


    def debug(self, msg):
        if self._enableDebug:
            VConsole.error(msg)


class SelectionRange(object):
    """Represents a select range of rows"""

    def __init__(self, row1, row2_or_length, st):
        """Constuctor."""
        self._st = st

        self._startRow = None
        self._length = None

        if isinstance(row2_or_length, VScrollTableRow):
            row2 = row2_or_length
            if row2.isBefore(row1):
                self._startRow = row2
                endRow = row1
            else:
                self._startRow = row1
                endRow = row2
            self._length = (endRow.getIndex() - self._startRow.getIndex()) + 1
        else:
            row, length = row1, row2_or_length
            self._startRow = row
            self._length = length


    def toString(self):
        return self._startRow.getKey() + '-' + self._length

    def __str__(self):
        return self.toString()


    def inRange(self, row):
        return (row.getIndex() >= self._startRow.getIndex()
                and row.getIndex() < self._startRow.getIndex() + self._length)


    def split(self, row):
        assert row.isAttached()
        ranges = list()
        endOfFirstRange = row.getIndex() - 1

        if not (endOfFirstRange - self._startRow.getIndex() < 0):
            # create range of first part unless its length is < 1
            endOfRange = self._st._scrollBody.getRowByRowIndex(endOfFirstRange)
            ranges.append(SelectionRange(self._startRow, endOfRange, self._st))

        startOfSecondRange = row.getIndex() + 1

        if not (self.getEndIndex() - startOfSecondRange < 0):
            # create range of second part unless its length is < 1
            startOfRange = self._st._scrollBody.getRowByRowIndex(
                    startOfSecondRange)
            ranges.append(self._st.SelectionRange(startOfRange,
                    (self.getEndIndex() - startOfSecondRange) + 1))

        return ranges


    def getEndIndex(self):
        return (self._startRow.getIndex() + self._length) - 1


class NavKeyPressHandler(KeyPressHandler):

    def __init__(self, st):
        self._st = st

    def onKeyPress(self, keyPressEvent):
        # This is used for Firefox only, since Firefox auto-repeat
        # works correctly only if we use a key press handler, other
        # browsers handle it correctly when using a key down handler
        if not BrowserInfo.get().isGecko():
            return

        event = keyPressEvent.getNativeEvent()

        if not self._st._enabled:
            # Cancel default keyboard events on a disabled Table
            # (prevents scrolling)
            event.preventDefault()

        elif self._st._hasFocus:
            # Key code in Firefox/onKeyPress is present only for
            # special keys, otherwise 0 is returned
            keyCode = event.getKeyCode()
            if keyCode == 0 and event.getCharCode() == ' ':
                # Provide a keyCode for space to be compatible with
                # FireFox keypress event
                keyCode = self._st._CHARCODE_SPACE
            if (self._st.handleNavigation(keyCode,
                    event.getCtrlKey() or event.getMetaKey(),
                    event.getShiftKey())):
                event.preventDefault()
            self._st.startScrollingVelocityTimer()


class NavKeyUpHandler(KeyUpHandler):

    def __init__(self, st):
        self._st = st

    def onKeyUp(self, keyUpEvent):
        event = keyUpEvent.getNativeEvent()
        keyCode = event.getKeyCode()
        if not self._st.isFocusable():
            self._st.cancelScrollingVelocityTimer()
        elif self._st.isNavigationKey(keyCode):
            if ((keyCode == self._st.getNavigationDownKey())
                    or (keyCode == self._st.getNavigationUpKey())):
                # in multiselect mode the server may still have value from
                # previous page. Clear it unless doing multiselection or
                # just moving focus.
                if not event.getShiftKey() and not event.getCtrlKey():
                    self._st.instructServerToForgetPreviousSelections()
                self._st.sendSelectedRows()
            self._st.cancelScrollingVelocityTimer()
            self._st._navKeyDown = False


class NavKeyDownHandler(KeyDownHandler):

    def __init__(self, st):
        self._st = st

    def onKeyDown(self, keyDownEvent):
        event = keyDownEvent.getNativeEvent()
        # This is not used for Firefox
        if BrowserInfo.get().isGecko():
            return

        if not self._st._enabled:
            # Cancel navKeyPressHandlerdefault keyboard events on a disabled Table
            # (prevents scrolling)
            event.preventDefault()
        elif self._st._hasFocus:
            if (self._st.handleNavigation(event.getKeyCode(),
                    event.getCtrlKey() or event.getMetaKey(),
                    event.getShiftKey())):
                self._st._navKeyDown = True
                event.preventDefault()
            self._st.startScrollingVelocityTimer()


class RowRequestHandler(Timer):

    def __init__(self, st):
        self._st = st

        self._reqFirstRow = 0
        self._reqRows = 0
        self._isRunning = False


    def deferRowFetch(self, msec=250):
        self._isRunning = True
        if self._reqRows > 0 and self._reqFirstRow < self._st._totalRows:
            self.schedule(msec)
            # tell scroll position to user if currently "visible" rows are
            # not rendered
            if (self._st._totalRows > self._st._pageLength
                    and (self._st._firstRowInViewPort + self._st._pageLength
                            > self._st._scrollBody.getLastRendered())
                    or (self._st._firstRowInViewPort
                            < self._st._scrollBody.getFirstRendered())):
                self._st.announceScrollPosition()
            else:
                self._st.hideScrollPositionAnnotation()


    def isRunning(self):
        return self._isRunning


    def setReqFirstRow(self, reqFirstRow):
        if reqFirstRow < 0:
            reqFirstRow = 0
        elif reqFirstRow >= self._st._totalRows:
            reqFirstRow = self._st._totalRows - 1
        self._reqFirstRow = reqFirstRow


    def setReqRows(self, reqRows):
        self._reqRows = reqRows


    def run(self):
        if (self._st.client.hasActiveRequest() or self._st._navKeyDown):
            # if client connection is busy, don't bother loading it more
            VConsole.log('Postponed rowfetch')
            self.schedule(250)
        else:
            firstToBeRendered = self._st._scrollBody.firstRendered
            if self._reqFirstRow < firstToBeRendered:
                firstToBeRendered = self._reqFirstRow
            elif (self._st._firstRowInViewPort - (self._st._cache_rate
                    * self._st._pageLength) > firstToBeRendered):
                firstToBeRendered = (self._st._firstRowInViewPort
                        - (self._st._cache_rate * self._st._pageLength))
                if firstToBeRendered < 0:
                    firstToBeRendered = 0

            lastToBeRendered = self._st._scrollBody.lastRendered

            if (self._reqFirstRow + self._reqRows) - 1 > lastToBeRendered:
                lastToBeRendered = (self._reqFirstRow + self._reqRows) - 1
            elif (self._st._firstRowInViewPort + self._st._pageLength
                  + (self._st._pageLength * self._st._cache_rate)
                        < lastToBeRendered):
                lastToBeRendered = (self._st._firstRowInViewPort
                        + self._st._pageLength + (self._st._pageLength
                                * self._st._cache_rate))

                if lastToBeRendered >= self._st._totalRows:
                    lastToBeRendered = self._st._totalRows - 1

                # due Safari 3.1 bug (see #2607), verify reqrows, original
                # problem unknown, but this should catch the issue
                if (self._reqFirstRow + self._reqRows) - 1 > lastToBeRendered:
                    self._reqRows = lastToBeRendered - self._reqFirstRow

            self._st.client.updateVariable(self._st.paintableId,
                    'firstToBeRendered', firstToBeRendered, False)

            self._st.client.updateVariable(self._st.paintableId,
                    'lastToBeRendered', lastToBeRendered, False)

            # remember which firstvisible we requested, in case the server
            # has a differing opinion
            self._st._lastRequestedFirstvisible = self._st._firstRowInViewPort
            self._st.client.updateVariable(self._st.paintableId,
                    'firstvisible', self._st._firstRowInViewPort, False)
            self._st.client.updateVariable(self._st.paintableId,
                    'reqfirstrow', self._reqFirstRow, False)
            self._st.client.updateVariable(self._st.paintableId,
                    'reqrows', self._reqRows, True)
            if self._st._selectionChanged:
                self._st._unSyncedselectionsBeforeRowFetch = \
                        set(self._st._selectedRowKeys)
            self._isRunning = False


    def getReqFirstRow(self):
        return self._reqFirstRow


    def refreshContent(self):
        """Sends request to refresh content at this position."""
        self._isRunning = True
        first = (self._st._firstRowInViewPort
                - (self._st._pageLength * self._st._cache_rate))
        reqRows = ((2 * self._st._pageLength * self._st._cache_rate)
                + self._st._pageLength)

        if first < 0:
            reqRows = reqRows + first
            first = 0

        self.setReqFirstRow(first)
        self.setReqRows(reqRows)
        self.run()



class TableDDDetails(object):
    _overkey = -1
    _dropLocation = None
    _colkey = None

    def equals(self, obj):
        # @Override
        # public int hashCode() {
        # return overkey;
        # }
        if isinstance(obj, TableDDDetails):
            other = obj
            return (self._dropLocation == other.dropLocation
                    and self._overkey == other.overkey
                    and (self._colkey is not None and self._colkey == other.colkey)
                    or (self._colkey is None and other.colkey is None))
        return False


class VScrollTableDropHandler(VAbstractDropHandler):

    _ROWSTYLEBASE = 'v-table-row-drag-'

    def __init__(self, st):
        self._st = st

        _dropDetails = None
        _lastEmphasized = None


    def dragEnter(self, drag):
        self.updateDropDetails(drag)
        super(VScrollTableDropHandler, self).dragEnter(drag)


    def updateDropDetails(self, drag):
        self._dropDetails = TableDDDetails()
        elementOver = drag.getElementOver()
        row = Util.findWidget(elementOver, self.getRowClass())
        if row is not None:
            self._dropDetails.overkey = row.rowKey
            tr = row.getElement()
            element = elementOver
            while element is not None and element.getParentElement() != tr:
                element = element.getParentElement()
            childIndex = DOM.getChildIndex(tr, element)
            self._dropDetails.colkey = self._st.tHead.getHeaderCell(
                    childIndex).getColKey()
            self._dropDetails.dropLocation = DDUtil.getVerticalDropLocation(
                    row.getElement(), drag.getCurrentGwtEvent(), 0.2)

        drag.getDropDetails()['itemIdOver'] = str(self._dropDetails.overkey)
        drag.getDropDetails()['detail'] = str(self._dropDetails.dropLocation) if self._dropDetails.dropLocation is not None else None


    def getRowClass(self):
        # get the row type this way to make dd work in derived
        # implementations
        return self._st._scrollBody.next().__class__


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
        UIObject.setStyleName(self.getElement(),
                self._st.CLASSNAME + '-drag', False)

        if self._lastEmphasized is None:
            return

        for w in self._st._scrollBody.renderedRows:
            row = w
            if (self._lastEmphasized is not None
                    and row.rowKey == self._lastEmphasized.overkey):
                stylename = (self._ROWSTYLEBASE
                        + str(self._lastEmphasized.dropLocation).lower())
                VScrollTableRow.setStyleName(row.getElement(), stylename,
                        False)
                self._lastEmphasized = None
                return


    def emphasis(self, details):
        """TODO: needs different drop modes ?? (on cells, on rows), now only
        supports rows
        """
        self.deEmphasis()
        UIObject.setStyleName(self.getElement(), self._st.CLASSNAME + '-drag',
                True)

        # iterate old and new emphasized row
        for w in self._st._scrollBody.renderedRows:
            row = w
            if details is not None and details.overkey == row.rowKey:
                stylename = (self._ROWSTYLEBASE
                        + str(details.dropLocation).lower())
                VScrollTableRow.setStyleName(row.getElement(), stylename, True)
                self._lastEmphasized = details
                return


    def dragAccepted(self, drag):
        self.emphasis(self._dropDetails)


    def getPaintable(self):
        return self._st

    def getApplicationConnection(self):
        return self._st.client


class LazyAdjustColumnWidths(Timer):

    def __init__(self, st):
        self._st = st

    def run(self):
        """Check for column widths, and available width, to see if we can fix
        column widths "optimally". Doing this lazily to avoid expensive
        calculation when resizing is not yet finished.
        """
        if self._st._scrollBody is None:
            # Try again later if we get here before scrollBody has been
            # initalized
            self._st.triggerLazyColumnAdjustment(False)
            return

        headCells = self._st.tHead
        usedMinimumWidth = 0
        totalExplicitColumnsWidths = 0
        expandRatioDivider = 0
        colIndex = 0

        while headCells.hasNext():
            hCell = headCells.next()
            if hCell.isDefinedWidth():
                totalExplicitColumnsWidths += hCell.getWidth()
                usedMinimumWidth += hCell.getWidth()
            else:
                usedMinimumWidth += hCell.getNaturalColumnWidth(colIndex)
                expandRatioDivider += hCell.getExpandRatio()
            colIndex += 1

        availW = self._st._scrollBody.getAvailableWidth()
        # Hey IE, are you really sure about this?
        availW = self._st._scrollBody.getAvailableWidth()
        visibleCellCount = self._st.tHead.getVisibleCellCount()
        availW -= self._st._scrollBody.getCellExtraWidth() * visibleCellCount

        if self._st.willHaveScrollbars():
            availW -= Util.getNativeScrollbarSize()

        extraSpace = availW - usedMinimumWidth
        if extraSpace < 0:
            extraSpace = 0

        totalUndefinedNaturalWidths = (usedMinimumWidth
                - totalExplicitColumnsWidths)

        # we have some space that can be divided optimally
        colIndex = 0
        headCells = self._st.tHead
        checksum = 0
        while headCells.hasNext():
            hCell = headCells.next()
            if not hCell.isDefinedWidth():
                w = hCell.getNaturalColumnWidth(colIndex)
                if expandRatioDivider > 0:
                    # divide excess space by expand ratios
                    newSpace = round(w
                            + ((extraSpace * hCell.getExpandRatio())
                                    / expandRatioDivider))
                elif totalUndefinedNaturalWidths != 0:
                    # divide relatively to natural column widths
                    newSpace = round(w
                            + ((extraSpace * w) / totalUndefinedNaturalWidths))
                else:
                    newSpace = w

                checksum += newSpace
                self._st.setColWidth(colIndex, newSpace, False)
            else:
                checksum += hCell.getWidth()

            colIndex += 1

        if extraSpace > 0 and checksum != availW:
            # There might be in some cases a rounding error of 1px when
            # extra space is divided so if there is one then we give the
            # first undefined column 1 more pixel
            headCells = self._st.tHead
            colIndex = 0
            while headCells.hasNext():
                hc = headCells.next()
                if not hc.isDefinedWidth():
                    self._st.setColWidth(colIndex,
                            (hc.getWidth() + availW) - checksum, False)
                    break
                colIndex += 1

        if ((self._st._height is None) or ('' == self._st._height)
                and self._st._totalRows == self._st._pageLength):
            # fix body height (may vary if lazy loading is offhorizontal
            # scrollbar appears/disappears)
            bodyHeight = self._st._scrollBody.getRequiredHeight()
            needsSpaceForHorizontalScrollbar = availW < usedMinimumWidth
            if needsSpaceForHorizontalScrollbar:
                bodyHeight += Util.getNativeScrollbarSize()
            heightBefore = self.getOffsetHeight()
            self._st._scrollBodyPanel.setHeight(bodyHeight + 'px')
            if heightBefore != self.getOffsetHeight():
                # Util.notifyParentOfSizeChange(VScrollTable.this, false);
                pass
        self._st._scrollBody.reLayoutComponents()

        class _18_(Command):

            def execute(self):
                Util.runWebkitOverflowAutoFix(
                        self._st._scrollBodyPanel.getElement())

        _18_ = _18_()
        Scheduler.get().scheduleDeferred(_18_)
        VScrollTable_this.forceRealignColumnHeaders()
