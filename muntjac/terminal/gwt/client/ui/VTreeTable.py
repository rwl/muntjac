# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.RenderSpace import (RenderSpace,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.VScrollTable import (VScrollTable,)
from com.vaadin.terminal.gwt.client.ComputedStyle import (ComputedStyle,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
# from com.google.gwt.animation.client.Animation import (Animation,)
# from com.google.gwt.dom.client.SpanElement import (SpanElement,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedList import (LinkedList,)
# from java.util.List import (List,)
VTreeTableRow = VTreeTable.VTreeTableScrollBody.VTreeTableRow


class VTreeTable(VScrollTable):

    class PendingNavigationEvent(object):
        _keycode = None
        _ctrl = None
        _shift = None

        def __init__(self, keycode, ctrl, shift):
            self._keycode = keycode
            self._ctrl = ctrl
            self._shift = shift

        def toString(self):
            string = 'Keyboard event: ' + self._keycode
            if self._ctrl:
                string += ' + ctrl'
            if self._shift:
                string += ' + shift'
            return string

    ATTRIBUTE_HIERARCHY_COLUMN_INDEX = 'hci'
    _collapseRequest = None
    _selectionPending = None
    _colIndexOfHierarchy = None
    _collapsedRowKey = None
    _scrollBody = None
    _animationsEnabled = None
    _pendingNavigationEvents = LinkedList()
    _focusParentResponsePending = None

    def updateFromUIDL(self, uidl, client):
        widget = None
        scrollPosition = 0
        if self._collapseRequest:
            widget = self.getWidget(1)
            scrollPosition = widget.getScrollPosition()
        self._animationsEnabled = uidl.getBooleanAttribute('animate')
        self._colIndexOfHierarchy = uidl.getIntAttribute(self.ATTRIBUTE_HIERARCHY_COLUMN_INDEX) if uidl.hasAttribute(self.ATTRIBUTE_HIERARCHY_COLUMN_INDEX) else 0
        super(VTreeTable, self).updateFromUIDL(uidl, client)
        if self._collapseRequest:
            if self._collapsedRowKey is not None and self._scrollBody is not None:
                row = self.getRenderedRowByKey(self._collapsedRowKey)
                if row is not None:
                    self.setRowFocus(row)
                    self.focus()
            scrollPosition2 = widget.getScrollPosition()
            if scrollPosition != scrollPosition2:
                widget.setScrollPosition(scrollPosition)
            # Triggers row calculations, removes cached rows etc. Basically
            # cleans up state. Be careful if touching this, you will brake
            # pageLength=0 if you remove this.

            self.onScroll(None)
            # Ensure that possibly removed/added scrollbars are considered.
            self.triggerLazyColumnAdjustment(True)
            self._collapseRequest = False
        if uidl.hasAttribute('focusedRow'):
            key = uidl.getStringAttribute('focusedRow')
            self.setRowFocus(self.getRenderedRowByKey(key))
            self._focusParentResponsePending = False
        elif uidl.hasAttribute('clearFocusPending'):
            # Special case to detect a response to a focusParent request that
            # does not return any focusedRow because the selected node has no
            # parent
            self._focusParentResponsePending = False
        while (
            not self._collapseRequest and not self._focusParentResponsePending and not self._pendingNavigationEvents.isEmpty()
        ):
            # Keep replaying any queued events as long as we don't have any
            # potential content changes pending
            event = self._pendingNavigationEvents.removeFirst()
            self.handleNavigation(event.keycode, event.ctrl, event.shift)

    def createScrollBody(self):
        # Overridden to allow animation of expands and collapses of nodes.
        self._scrollBody = self.VTreeTableScrollBody()
        return self._scrollBody

    def addAndRemoveRows(self, partialRowAdditions):
        if partialRowAdditions is None:
            return
        if self._animationsEnabled and self.browserSupportsAnimation():
            if partialRowAdditions.hasAttribute('hide'):
                self._scrollBody.unlinkRowsAnimatedAndUpdateCacheWhenFinished(partialRowAdditions.getIntAttribute('firstprowix'), partialRowAdditions.getIntAttribute('numprows'))
            else:
                self._scrollBody.insertRowsAnimated(partialRowAdditions, partialRowAdditions.getIntAttribute('firstprowix'), partialRowAdditions.getIntAttribute('numprows'))
                self.discardRowsOutsideCacheWindow()
        else:
            super(VTreeTable, self).addAndRemoveRows(partialRowAdditions)

    def browserSupportsAnimation(self):
        bi = BrowserInfo.get()
        return not ((bi.isIE6() or bi.isIE7()) or bi.isSafari4())

    def VTreeTableScrollBody(VTreeTable_this, *args, **kwargs):

        class VTreeTableScrollBody(VScrollTable.VScrollTableBody):
            _identWidth = -1

            def __init__(self):
                super(VTreeTableScrollBody, self)()

            def createRow(self, uidl, aligns2):
                if uidl.hasAttribute('gen_html'):
                    # This is a generated row.
                    return self.VTreeTableGeneratedRow(uidl, aligns2)
                return self.VTreeTableRow(uidl, aligns2)

            def VTreeTableRow(VTreeTableScrollBody_this, *args, **kwargs):

                class VTreeTableRow(VScrollTable.VScrollTableBody.VScrollTableRow):
                    _isTreeCellAdded = False
                    _treeSpacer = None
                    _open = None
                    _depth = None
                    _canHaveChildren = None
                    widgetInHierarchyColumn = None

                    def __init__(self, uidl, aligns2):
                        super(VTreeTableRow, self)(uidl, aligns2)

                    def addCell(self, *args):
                        _0 = args
                        _1 = len(args)
                        if _1 == 5:
                            rowUidl, w, align, style, isSorted = _0
                            super(VTreeTableRow, self).addCell(rowUidl, w, align, style, isSorted)
                            if self.addTreeSpacer(rowUidl):
                                self.widgetInHierarchyColumn = w
                        elif _1 == 7:
                            rowUidl, text, align, style, textIsHTML, isSorted, description = _0
                            super(VTreeTableRow, self).addCell(rowUidl, text, align, style, textIsHTML, isSorted, description)
                            self.addTreeSpacer(rowUidl)
                        else:
                            raise ARGERROR(5, 7)

                    def addTreeSpacer(self, rowUidl):
                        if self.cellShowsTreeHierarchy(self.getElement().getChildCount() - 1):
                            container = self.getElement().getLastChild().getFirstChild()
                            if rowUidl.hasAttribute('icon'):
                                # icons are in first content cell in TreeTable
                                icon = Document.get().createImageElement()
                                icon.setClassName('v-icon')
                                icon.setAlt('icon')
                                icon.setSrc(self.client.translateVaadinUri(rowUidl.getStringAttribute('icon')))
                                container.insertFirst(icon)
                            classname = 'v-treetable-treespacer'
                            if rowUidl.getBooleanAttribute('ca'):
                                self._canHaveChildren = True
                                self._open = rowUidl.getBooleanAttribute('open')
                                classname += ' v-treetable-node-open' if self._open else ' v-treetable-node-closed'
                            self._treeSpacer = Document.get().createSpanElement()
                            self._treeSpacer.setClassName(classname)
                            container.insertFirst(self._treeSpacer)
                            self._depth = rowUidl.getIntAttribute('depth') if rowUidl.hasAttribute('depth') else 0
                            self.setIdent()
                            self._isTreeCellAdded = True
                            return True
                        return False

                    def cellShowsTreeHierarchy(self, curColIndex):
                        if self._isTreeCellAdded:
                            return False
                        return curColIndex == VTreeTable_this._colIndexOfHierarchy + (1 if self.showRowHeaders else 0)

                    def onBrowserEvent(self, event):
                        if (
                            event.getEventTarget() == self._treeSpacer and self._treeSpacer.getClassName().contains('node')
                        ):
                            if event.getTypeInt() == Event.ONMOUSEUP:
                                VTreeTable_this.sendToggleCollapsedUpdate(self.getKey())
                            return
                        super(VTreeTableRow, self).onBrowserEvent(event)

                    def setIdent(self):
                        if VTreeTableScrollBody_this.getIdentWidth() > 0 and self._depth != 0:
                            self._treeSpacer.getStyle().setWidth((self._depth + 1) * VTreeTableScrollBody_this.getIdentWidth(), Unit.PX)

                    def onAttach(self):
                        super(VTreeTableRow, self).onAttach()
                        if VTreeTableScrollBody_this.getIdentWidth() < 0:
                            VTreeTableScrollBody_this.detectIdent(self)

                    def getAllocatedSpace(self, child):
                        if self.widgetInHierarchyColumn == child:
                            hierarchyAndIconWidth = self.getHierarchyAndIconWidth()
                            allocatedSpace = super(VTreeTableRow, self).getAllocatedSpace(child)

                            class _0_(RenderSpace):

                                def getWidth(self):
                                    return self.allocatedSpace.getWidth() - self.hierarchyAndIconWidth

                                def getHeight(self):
                                    return self.allocatedSpace.getHeight()

                            _0_ = _0_()
                            return _0_
                        return super(VTreeTableRow, self).getAllocatedSpace(child)

                    def getHierarchyAndIconWidth(self):
                        consumedSpace = self._treeSpacer.getOffsetWidth()
                        if self._treeSpacer.getParentElement().getChildCount() > 2:
                            # icon next to tree spacer
                            consumedSpace += self._treeSpacer.getNextSibling().getOffsetWidth()
                        return consumedSpace

                return VTreeTableRow(*args, **kwargs)

            class VTreeTableGeneratedRow(VTreeTableRow):
                _spanColumns = None
                _htmlContentAllowed = None

                def __init__(self, uidl, aligns):
                    super(VTreeTableGeneratedRow, self)(uidl, aligns)
                    self.addStyleName('v-table-generated-row')

                def isSpanColumns(self):
                    return self._spanColumns

                def initCellWidths(self):
                    if self._spanColumns:
                        self.setSpannedColumnWidthAfterDOMFullyInited()
                    else:
                        super(VTreeTableGeneratedRow, self).initCellWidths()

                def setSpannedColumnWidthAfterDOMFullyInited(self):
                    # Defer setting width on spanned columns to make sure that
                    # they are added to the DOM before trying to calculate
                    # widths.

                    class _1_(ScheduledCommand):

                        def execute(self):
                            if self.showRowHeaders:
                                VTreeTableGeneratedRow_this.setCellWidth(0, self.tHead.getHeaderCell(0).getWidth())
                                VTreeTableGeneratedRow_this.calcAndSetSpanWidthOnCell(1)
                            else:
                                VTreeTableGeneratedRow_this.calcAndSetSpanWidthOnCell(0)

                    _1_ = _1_()
                    Scheduler.get().scheduleDeferred(_1_)

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
                        super(VTreeTableGeneratedRow, self).addCellsFromUIDL(uidl, aligns, col, visibleColumnIndex)

                def addSpannedCell(self, *args):
                    _0 = args
                    _1 = len(args)
                    if _1 == 6:
                        rowUidl, w, align, style, sorted, colCount = _0
                        td = DOM.createTD()
                        td.setColSpan(colCount)
                        self.initCellWithWidget(w, align, style, sorted, td)
                        td.getStyle().setHeight(self.getRowHeight(), Unit.PX)
                        if self.addTreeSpacer(rowUidl):
                            self.widgetInHierarchyColumn = w
                    elif _1 == 8:
                        rowUidl, text, align, style, textIsHTML, sorted, description, colCount = _0
                        td = DOM.createTD()
                        td.setColSpan(colCount)
                        self.initCellWithText(text, align, style, textIsHTML, sorted, description, td)
                        td.getStyle().setHeight(self.getRowHeight(), Unit.PX)
                        self.addTreeSpacer(rowUidl)
                    else:
                        raise ARGERROR(6, 8)

                # String only content is optimized by not using Label widget

                def setCellWidth(self, cellIx, width):
                    if self.isSpanColumns():
                        if self.showRowHeaders:
                            if cellIx == 0:
                                super(VTreeTableGeneratedRow, self).setCellWidth(0, width)
                            else:
                                # We need to recalculate the spanning TDs width for
                                # every cellIx in order to support column resizing.
                                self.calcAndSetSpanWidthOnCell(1)
                        else:
                            # Same as above.
                            self.calcAndSetSpanWidthOnCell(0)
                    else:
                        super(VTreeTableGeneratedRow, self).setCellWidth(cellIx, width)

                def calcAndSetSpanWidthOnCell(self, cellIx):
                    spanWidth = 0
                    _0 = True
                    ix = 1 if self.showRowHeaders else 0
                    while True:
                        if _0 is True:
                            _0 = False
                        else:
                            ix += 1
                        if not (ix < self.tHead.getVisibleCellCount()):
                            break
                        spanWidth += self.tHead.getHeaderCell(ix).getOffsetWidth()
                    Util.setWidthExcludingPaddingAndBorder(self.getElement().getChild(cellIx), spanWidth, 13, False)

            def getIdentWidth(self):
                return self._identWidth

            def detectIdent(self, vTreeTableRow):
                self._identWidth = vTreeTableRow.treeSpacer.getOffsetWidth()
                if self._identWidth == 0:
                    self._identWidth = -1
                    return
                iterator = self
                while iterator.hasNext():
                    next = iterator.next()
                    next.setIdent()

            def unlinkRowsAnimatedAndUpdateCacheWhenFinished(self, firstIndex, rows):
                rowsToDelete = list()
                _0 = True
                ix = firstIndex
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        ix += 1
                    if not (ix < firstIndex + rows):
                        break
                    row = self.getRowByRowIndex(ix)
                    if row is not None:
                        rowsToDelete.add(row)

                class anim(self.RowCollapseAnimation):

                    def onComplete(self):
                        super(_2_, self).onComplete()
                        # Actually unlink the rows and update the cache after the
                        # animation is done.
                        self.unlinkAndReindexRows(self.firstIndex, self.rows)
                        self.discardRowsOutsideCacheWindow()
                        self.ensureCacheFilled()

                anim.run(150)

            def insertRowsAnimated(self, rowData, firstIndex, rows):
                insertedRows = self.insertAndReindexRows(rowData, firstIndex, rows)
                anim = self.RowExpandAnimation(insertedRows)
                anim.run(150)
                return insertedRows

            class AnimationPreparator(object):
                """Prepares the table for animation by copying the background colors of
                all TR elements to their respective TD elements if the TD element is
                transparent. This is needed, since if TDs have transparent
                backgrounds, the rows sliding behind them are visible.
                """
                _lastItemIx = None

                def __init__(self, lastItemIx):
                    self._lastItemIx = lastItemIx

                def prepareTableForAnimation(self):
                    ix = self._lastItemIx
                    row = None
                    while row = self.getRowByRowIndex(ix) is not None:
                        self.copyTRBackgroundsToTDs(row)
                        ix -= 1

                def copyTRBackgroundsToTDs(self, row):
                    tr = row.getElement()
                    cs = ComputedStyle(tr)
                    backgroundAttachment = cs.getProperty('backgroundAttachment')
                    backgroundClip = cs.getProperty('backgroundClip')
                    backgroundColor = cs.getProperty('backgroundColor')
                    backgroundImage = cs.getProperty('backgroundImage')
                    backgroundOrigin = cs.getProperty('backgroundOrigin')
                    _0 = True
                    ix = 0
                    while True:
                        if _0 is True:
                            _0 = False
                        else:
                            ix += 1
                        if not (ix < tr.getChildCount()):
                            break
                        td = tr.getChild(ix)
                        if not self.elementHasBackground(td):
                            td.getStyle().setProperty('backgroundAttachment', backgroundAttachment)
                            td.getStyle().setProperty('backgroundClip', backgroundClip)
                            td.getStyle().setProperty('backgroundColor', backgroundColor)
                            td.getStyle().setProperty('backgroundImage', backgroundImage)
                            td.getStyle().setProperty('backgroundOrigin', backgroundOrigin)

                def elementHasBackground(self, element):
                    cs = ComputedStyle(element)
                    clr = cs.getProperty('backgroundColor')
                    img = cs.getProperty('backgroundImage')
                    return not ((('rgba(0, 0, 0, 0)' == clr.trim()) or ('transparent' == clr.trim())) or (img is None))

                def restoreTableAfterAnimation(self):
                    ix = self._lastItemIx
                    row = None
                    while row = self.getRowByRowIndex(ix) is not None:
                        self.restoreStyleForTDsInRow(row)
                        ix -= 1

                def restoreStyleForTDsInRow(self, row):
                    tr = row.getElement()
                    _0 = True
                    ix = 0
                    while True:
                        if _0 is True:
                            _0 = False
                        else:
                            ix += 1
                        if not (ix < tr.getChildCount()):
                            break
                        td = tr.getChild(ix)
                        td.getStyle().clearProperty('backgroundAttachment')
                        td.getStyle().clearProperty('backgroundClip')
                        td.getStyle().clearProperty('backgroundColor')
                        td.getStyle().clearProperty('backgroundImage')
                        td.getStyle().clearProperty('backgroundOrigin')

            def RowExpandAnimation(VTreeTableScrollBody_this, *args, **kwargs):

                class RowExpandAnimation(Animation):
                    """Animates row expansion using the GWT animation framework.

                    The idea is as follows:

                    1. Insert all rows normally

                    2. Insert a newly created DIV containing a new TABLE element below
                    the DIV containing the actual scroll table body.

                    3. Clone the rows that were inserted in step 1 and attach the clones
                    to the new TABLE element created in step 2.

                    4. The new DIV from step 2 is absolutely positioned so that the last
                    inserted row is just behind the row that was expanded.

                    5. Hide the contents of the originally inserted rows by setting the
                    DIV.v-table-cell-wrapper to display:none;.

                    6. Set the height of the originally inserted rows to 0.

                    7. The animation loop slides the DIV from step 2 downwards, while at
                    the same pace growing the height of each of the inserted rows from 0
                    to full height. The first inserted row grows from 0 to full and after
                    this the second row grows from 0 to full, etc until all rows are full
                    height.

                    8. Remove the DIV from step 2

                    9. Restore display:block; to the DIV.v-table-cell-wrapper elements.

                    10. DONE
                    """
                    _rows = None
                    _cloneDiv = None
                    _cloneTable = None
                    _preparator = None

                    def __init__(self, rows):
                        self._rows = rows
                        self.buildAndInsertAnimatingDiv()
                        self._preparator = VTreeTableScrollBody_this.AnimationPreparator(rows[0].getIndex() - 1)
                        self._preparator.prepareTableForAnimation()
                        for row in rows:
                            self.cloneAndAppendRow(row)
                            row.addStyleName('v-table-row-animating')
                            self.setCellWrapperDivsToDisplayNone(row)
                            row.setHeight(self.getInitialHeight())

                    def getInitialHeight(self):
                        return '0px'

                    def cloneAndAppendRow(self, row):
                        clonedTR = None
                        clonedTR = row.getElement().cloneNode(True)
                        clonedTR.getStyle().setVisibility(Visibility.VISIBLE)
                        self._cloneTable.appendChild(clonedTR)

                    def getBaseOffset(self):
                        return self._rows[0].getAbsoluteTop() - self._rows[0].getParent().getAbsoluteTop() - (len(self._rows) * self.getRowHeight())

                    def buildAndInsertAnimatingDiv(self):
                        self._cloneDiv = DOM.createDiv()
                        self._cloneDiv.addClassName('v-treetable-animation-clone-wrapper')
                        self._cloneTable = DOM.createTable()
                        self._cloneTable.addClassName('v-treetable-animation-clone')
                        self._cloneDiv.appendChild(self._cloneTable)
                        self.insertAnimatingDiv()

                    def insertAnimatingDiv(self):
                        tableBody = self.getElement()
                        tableBodyParent = tableBody.getParentElement()
                        tableBodyParent.insertAfter(self._cloneDiv, tableBody)

                    def onUpdate(self, progress):
                        self.animateDiv(progress)
                        self.animateRowHeights(progress)

                    def animateDiv(self, progress):
                        offset = self.calculateDivOffset(progress, self.getRowHeight())
                        self._cloneDiv.getStyle().setTop(self.getBaseOffset() + offset, Unit.PX)

                    def animateRowHeights(self, progress):
                        rh = self.getRowHeight()
                        vlh = self.calculateHeightOfAllVisibleLines(progress, rh)
                        ix = 0
                        while ix < len(self._rows):
                            height = vlh if vlh < rh else rh
                            self._rows[ix].setHeight(height + 'px')
                            vlh -= height
                            ix += 1

                    def calculateHeightOfAllVisibleLines(self, progress, rh):
                        return len(self._rows) * rh * progress

                    def calculateDivOffset(self, progress, rh):
                        return progress * len(self._rows) * rh

                    def onComplete(self):
                        self._preparator.restoreTableAfterAnimation()
                        for row in self._rows:
                            self.resetCellWrapperDivsDisplayProperty(row)
                            row.removeStyleName('v-table-row-animating')
                        tableBodyParent = self.getElement().getParentElement()
                        tableBodyParent.removeChild(self._cloneDiv)

                    def setCellWrapperDivsToDisplayNone(self, row):
                        tr = row.getElement()
                        _0 = True
                        ix = 0
                        while True:
                            if _0 is True:
                                _0 = False
                            else:
                                ix += 1
                            if not (ix < tr.getChildCount()):
                                break
                            self.getWrapperDiv(tr, ix).getStyle().setDisplay(Display.NONE)

                    def getWrapperDiv(self, tr, tdIx):
                        td = tr.getChild(tdIx)
                        return td.getChild(0)

                    def resetCellWrapperDivsDisplayProperty(self, row):
                        tr = row.getElement()
                        _0 = True
                        ix = 0
                        while True:
                            if _0 is True:
                                _0 = False
                            else:
                                ix += 1
                            if not (ix < tr.getChildCount()):
                                break
                            self.getWrapperDiv(tr, ix).getStyle().clearProperty('display')

                return RowExpandAnimation(*args, **kwargs)

            class RowCollapseAnimation(RowExpandAnimation):
                """This is the inverse of the RowExpandAnimation and is implemented by
                extending it and overriding the calculation of offsets and heights.
                """
                _rows = None

                def __init__(self, rows):
                    super(RowCollapseAnimation, self)(rows)
                    self._rows = rows

                def getInitialHeight(self):
                    return self.getRowHeight() + 'px'

                def getBaseOffset(self):
                    return self.getRowHeight()

                def calculateHeightOfAllVisibleLines(self, progress, rh):
                    return len(self._rows) * rh * (1 - progress)

                def calculateDivOffset(self, progress, rh):
                    return -super(RowCollapseAnimation, self).calculateDivOffset(progress, rh)

        return VTreeTableScrollBody(*args, **kwargs)

    def buildCaptionHtmlSnippet(self, uidl):
        """Icons rendered into first actual column in TreeTable, not to row header
        cell
        """
        if uidl.getTag() == 'column':
            return super(VTreeTable, self).buildCaptionHtmlSnippet(uidl)
        else:
            s = uidl.getStringAttribute('caption')
            return s

    def handleNavigation(self, keycode, ctrl, shift):
        if self._collapseRequest or self._focusParentResponsePending:
            # Enqueue the event if there might be pending content changes from
            # the server
            if len(self._pendingNavigationEvents) < 10:
                # Only keep 10 keyboard events in the queue
                pendingNavigationEvent = self.PendingNavigationEvent(keycode, ctrl, shift)
                self._pendingNavigationEvents.add(pendingNavigationEvent)
            return True
        focusedRow = self.getFocusedRow()
        if focusedRow is not None:
            if (
                focusedRow.canHaveChildren and (keycode == KeyCodes.KEY_RIGHT and not focusedRow.open) or (keycode == KeyCodes.KEY_LEFT and focusedRow.open)
            ):
                if not ctrl:
                    self.client.updateVariable(self.paintableId, 'selectCollapsed', True, False)
                self.sendSelectedRows(False)
                self.sendToggleCollapsedUpdate(focusedRow.getKey())
                return True
            elif keycode == KeyCodes.KEY_RIGHT and focusedRow.open:
                # already expanded, move selection down if next is on a deeper
                # level (is-a-child)
                body = focusedRow.getParent()
                iterator = body
                next = None
                while iterator.hasNext():
                    next = iterator.next()
                    if next == focusedRow:
                        next = iterator.next()
                        break
                if next is not None:
                    if next.depth > focusedRow.depth:
                        self._selectionPending = True
                        return super(VTreeTable, self).handleNavigation(self.getNavigationDownKey(), ctrl, shift)
                else:
                    # Note, a minor change here for a bit false behavior if
                    # cache rows is disabled + last visible row + no childs for
                    # the node
                    self._selectionPending = True
                    return super(VTreeTable, self).handleNavigation(self.getNavigationDownKey(), ctrl, shift)
            elif keycode == KeyCodes.KEY_LEFT:
                # already collapsed move selection up to parent node
                # do on the server side as the parent is not necessary
                # rendered on the client, could check if parent is visible if
                # a performance issue arises
                self.client.updateVariable(self.paintableId, 'focusParent', focusedRow.getKey(), True)
                # Set flag that we should enqueue navigation events until we
                # get a response to this request
                self._focusParentResponsePending = True
                return True
        return super(VTreeTable, self).handleNavigation(keycode, ctrl, shift)

    def sendToggleCollapsedUpdate(self, rowKey):
        self._collapsedRowKey = rowKey
        self._collapseRequest = True
        self.client.updateVariable(self.paintableId, 'toggleCollapsed', rowKey, True)

    def onBrowserEvent(self, event):
        super(VTreeTable, self).onBrowserEvent(event)
        if event.getTypeInt() == Event.ONKEYUP and self._selectionPending:
            self.sendSelectedRows()

    def sendSelectedRows(self, immediately):
        super(VTreeTable, self).sendSelectedRows(immediately)
        self._selectionPending = False

    def reOrderColumn(self, columnKey, newIndex):
        super(VTreeTable, self).reOrderColumn(columnKey, newIndex)
        # current impl not intelligent enough to survive without visiting the
        # server to redraw content
        self.client.sendPendingVariableChanges()

    def setStyleName(self, style):
        super(VTreeTable, self).setStyleName(style + ' v-treetable')

    def updateTotalRows(self, uidl):
        # Make sure that initializedAndAttached & al are not reset when the
        # totalrows are updated on expand/collapse requests.
        newTotalRows = uidl.getIntAttribute('totalrows')
        self.setTotalRows(newTotalRows)
