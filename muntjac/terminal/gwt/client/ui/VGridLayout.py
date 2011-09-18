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

from __pyjamas__ import (POSTINC,)
from com.vaadin.terminal.gwt.client.Container import (Container,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.layout.CellBasedLayout import (CellBasedLayout,)
from com.vaadin.terminal.gwt.client.StyleConstants import (StyleConstants,)
from com.vaadin.terminal.gwt.client.ui.layout.ChildComponentContainer import (ChildComponentContainer,)
from com.vaadin.terminal.gwt.client.ui.VMarginInfo import (VMarginInfo,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.RenderSpace import (RenderSpace,)
from com.vaadin.terminal.gwt.client.ui.AlignmentInfo import (AlignmentInfo,)
# from com.google.gwt.dom.client.DivElement import (DivElement,)
# from com.google.gwt.dom.client.Document import (Document,)
# from com.google.gwt.event.dom.client.DomEvent.Type import (Type,)
# from com.google.gwt.event.shared.EventHandler import (EventHandler,)
# from com.google.gwt.event.shared.HandlerRegistration import (HandlerRegistration,)
# from com.google.gwt.user.client.Element import (Element,)
# from com.google.gwt.user.client.ui.AbsolutePanel import (AbsolutePanel,)
# from com.google.gwt.user.client.ui.SimplePanel import (SimplePanel,)
# from com.google.gwt.user.client.ui.Widget import (Widget,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.HashMap import (HashMap,)
# from java.util.HashSet import (HashSet,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedList import (LinkedList,)
# from java.util.List import (List,)
# from java.util.Set import (Set,)


class VGridLayout(SimplePanel, Paintable, Container):
    CLASSNAME = 'v-gridlayout'
    _margin = Document.get().createDivElement()
    _canvas = AbsolutePanel()
    _client = None
    widgetToComponentContainer = dict()
    _paintableToCell = dict()
    _spacingPixelsHorizontal = None
    _spacingPixelsVertical = None
    _columnWidths = None
    _rowHeights = None
    _height = None
    _width = None
    _colExpandRatioArray = None
    _rowExpandRatioArray = None
    _minColumnWidths = None
    _minRowHeights = None
    _rendering = None
    _nonRenderedWidgets = None
    _sizeChangedDuringRendering = False


#    private LayoutClickEventHandler clickEventHandler = new LayoutClickEventHandler(
#            this, EventId.LAYOUT_CLICK) {
#
#        @Override
#        protected Paintable getChildComponent(Element element) {
#            return getComponent(element);
#        }
#
#        @Override
#        protected <H extends EventHandler> HandlerRegistration registerHandler(
#                H handler, Type<H> type) {
#            return addDomHandler(handler, type);
#        }
#    };

    def __init__(self):
        super(VGridLayout, self)()
        self.getElement().appendChild(self._margin)
        self.setStyleName(self.CLASSNAME)
        self.setWidget(self._canvas)

    def getContainerElement(self):
        return self._margin

    def getColumnWidths(self):
        """Returns the column widths measured in pixels

        @return
        """
        return self._columnWidths

    def getRowHeights(self):
        """Returns the row heights measured in pixels

        @return
        """
        return self._rowHeights

    def getHorizontalSpacing(self):
        """Returns the spacing between the cells horizontally in pixels

        @return
        """
        return self._spacingPixelsHorizontal

    def getVerticalSpacing(self):
        """Returns the spacing between the cells vertically in pixels

        @return
        """
        return self._spacingPixelsVertical

    def updateFromUIDL(self, uidl, client):
        self._rendering = True
        self._client = client
        if client.updateComponent(self, uidl, True):
            self._rendering = False
            return
        self.clickEventHandler.handleEventHandlerRegistration(client)
        self._canvas.setWidth('0px')
        self.handleMargins(uidl)
        self.detectSpacing(uidl)
        cols = uidl.getIntAttribute('w')
        rows = uidl.getIntAttribute('h')
        self._columnWidths = [None] * cols
        self._rowHeights = [None] * rows
        if self._cells is None:
            self._cells = [None] * rows
        elif (len(self._cells) != cols) or (self._cells[0].length != rows):
            newCells = [None] * rows
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(self._cells)):
                    break
                _1 = True
                j = 0
                while True:
                    if _1 is True:
                        _1 = False
                    else:
                        j += 1
                    if not (j < self._cells[i].length):
                        break
                    if i < cols and j < rows:
                        newCells[i][j] = self._cells[i][j]
            self._cells = newCells
        self._nonRenderedWidgets = self.widgetToComponentContainer.clone()
        alignments = uidl.getIntArrayAttribute('alignments')
        alignmentIndex = 0
        pendingCells = LinkedList()
        relativeHeighted = LinkedList()
        _2 = True
        i = uidl.getChildIterator()
        while True:
            if _2 is True:
                _2 = False
            if not i.hasNext():
                break
            r = i.next()
            if 'gr' == r.getTag():
                _3 = True
                j = r.getChildIterator()
                while True:
                    if _3 is True:
                        _3 = False
                    if not j.hasNext():
                        break
                    c = j.next()
                    if 'gc' == c.getTag():
                        cell = self.getCell(c)
                        if cell.hasContent():
                            rendered = cell.renderIfNoRelativeWidth()
                            cell.alignment = alignments[POSTINC(globals(), locals(), 'alignmentIndex')]
                            if not rendered:
                                pendingCells.add(cell)
                            if cell.colspan > 1:
                                self.storeColSpannedCell(cell)
                            elif rendered:
                                # strore non-colspanned widths to columnWidth
                                # array
                                if self._columnWidths[cell.col] < cell.getWidth():
                                    self._columnWidths[cell.col] = cell.getWidth()
                            if cell.hasRelativeHeight():
                                relativeHeighted.add(cell)
        self.distributeColSpanWidths()
        self._colExpandRatioArray = uidl.getIntArrayAttribute('colExpand')
        self._rowExpandRatioArray = uidl.getIntArrayAttribute('rowExpand')
        self._minColumnWidths = self.cloneArray(self._columnWidths)
        self.expandColumns()
        self.renderRemainingComponentsWithNoRelativeHeight(pendingCells)
        self.detectRowHeights()
        self.expandRows()
        self.renderRemainingComponents(pendingCells)
        for cell in relativeHeighted:
            # rendering done above so cell.cc should not be null
            widget2 = cell.cc.getWidget()
            client.handleComponentRelativeSize(widget2)
            cell.cc.updateWidgetSize()
        self.layoutCells()
        # clean non rendered components
        for w in self._nonRenderedWidgets.keys():
            childComponentContainer = self.widgetToComponentContainer[w]
            self._paintableToCell.remove(w)
            self.widgetToComponentContainer.remove(w)
            childComponentContainer.removeFromParent()
            client.unregisterPaintable(w)
        self._nonRenderedWidgets = None
        self._rendering = False
        self._sizeChangedDuringRendering = False

    @classmethod
    def cloneArray(cls, toBeCloned):
        clone = [None] * len(toBeCloned)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(clone)):
                break
            clone[i] = toBeCloned[i] * 1
        return clone

    def expandRows(self):
        if not ('' == self._height):
            usedSpace = self._minRowHeights[0]
            _0 = True
            i = 1
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(self._minRowHeights)):
                    break
                usedSpace += self._spacingPixelsVertical + self._minRowHeights[i]
            availableSpace = self.getOffsetHeight() - self._marginTopAndBottom
            excessSpace = availableSpace - usedSpace
            distributed = 0
            if excessSpace > 0:
                _1 = True
                i = 0
                while True:
                    if _1 is True:
                        _1 = False
                    else:
                        i += 1
                    if not (i < len(self._rowHeights)):
                        break
                    ew = (excessSpace * self._rowExpandRatioArray[i]) / 1000
                    self._rowHeights[i] = self._minRowHeights[i] + ew
                    distributed += ew
                excessSpace -= distributed
                c = 0
                while excessSpace > 0:
                    self._rowHeights[c % len(self._rowHeights)] += 1
                    excessSpace -= 1
                    c += 1

    def setHeight(self, height):
        super(VGridLayout, self).setHeight(height)
        if not (height == self._height):
            self._height = height
            if self._rendering:
                self._sizeChangedDuringRendering = True
            else:
                self.expandRows()
                self.layoutCells()
                for c in self._paintableToCell.keys():
                    self._client.handleComponentRelativeSize(c)

    def setWidth(self, width):
        super(VGridLayout, self).setWidth(width)
        if not (width == self._width):
            self._width = width
            if self._rendering:
                self._sizeChangedDuringRendering = True
            else:
                oldWidths = self.cloneArray(self._columnWidths)
                self.expandColumns()
                heightChanged = False
                dirtyRows = None
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(oldWidths)):
                        break
                    if self._columnWidths[i] != oldWidths[i]:
                        column = self._cells[i]
                        _1 = True
                        j = 0
                        while True:
                            if _1 is True:
                                _1 = False
                            else:
                                j += 1
                            if not (j < len(column)):
                                break
                            c = column[j]
                            if c is not None and c.cc is not None and c.widthCanAffectHeight():
                                c.cc.setContainerSize(c.getAvailableWidth(), c.getAvailableHeight())
                                self._client.handleComponentRelativeSize(c.cc.getWidget())
                                c.cc.updateWidgetSize()
                                newHeight = c.getHeight()
                                if (
                                    self._columnWidths[i] < oldWidths[i] and newHeight > self._minRowHeights[j] and c.rowspan == 1
                                ):
                                    # The width of this column was reduced and
                                    # this affected the height. The height is
                                    # now greater than the previously
                                    # calculated minHeight for the row.

                                    self._minRowHeights[j] = newHeight
                                    if newHeight > self._rowHeights[j]:
                                        # The new height is greater than the
                                        # previously calculated rowHeight -> we
                                        # need to recalculate heights later on

                                        self._rowHeights[j] = newHeight
                                        heightChanged = True
                                elif newHeight < self._minRowHeights[j]:
                                    # The new height of the component is less
                                    # than the previously calculated min row
                                    # height. The min row height may be
                                    # affected and must thus be recalculated

                                    if dirtyRows is None:
                                        dirtyRows = set()
                                    dirtyRows.add(j)
                if dirtyRows is not None:
                    # flag indicating that there is a potential row shrinking
                    rowMayShrink = False
                    for rowIndex in dirtyRows:
                        oldMinimum = self._minRowHeights[rowIndex]
                        newMinimum = 0
                        _2 = True
                        colIndex = 0
                        while True:
                            if _2 is True:
                                _2 = False
                            else:
                                colIndex += 1
                            if not (colIndex < len(self._columnWidths)):
                                break
                            cell = self._cells[colIndex][rowIndex]
                            if (
                                cell is not None and not cell.hasRelativeHeight() and cell.getHeight() > newMinimum
                            ):
                                newMinimum = cell.getHeight()
                        if newMinimum < oldMinimum:
                            self._minRowHeights[rowIndex] = self._rowHeights[rowIndex] = newMinimum
                            rowMayShrink = True
                    if rowMayShrink:
                        self.distributeRowSpanHeights()
                        self._minRowHeights = self.cloneArray(self._rowHeights)
                        heightChanged = True
                self.layoutCells()
                for c in self._paintableToCell.keys():
                    self._client.handleComponentRelativeSize(c)
                if heightChanged and '' == self._height:
                    Util.notifyParentOfSizeChange(self, False)

    def expandColumns(self):
        if not ('' == self._width):
            usedSpace = self._minColumnWidths[0]
            _0 = True
            i = 1
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(self._minColumnWidths)):
                    break
                usedSpace += self._spacingPixelsHorizontal + self._minColumnWidths[i]
            self._canvas.setWidth('')
            availableSpace = self._canvas.getOffsetWidth()
            excessSpace = availableSpace - usedSpace
            distributed = 0
            if excessSpace > 0:
                _1 = True
                i = 0
                while True:
                    if _1 is True:
                        _1 = False
                    else:
                        i += 1
                    if not (i < len(self._columnWidths)):
                        break
                    ew = (excessSpace * self._colExpandRatioArray[i]) / 1000
                    self._columnWidths[i] = self._minColumnWidths[i] + ew
                    distributed += ew
                excessSpace -= distributed
                c = 0
                while excessSpace > 0:
                    self._columnWidths[c % len(self._columnWidths)] += 1
                    excessSpace -= 1
                    c += 1

    def layoutCells(self):
        x = 0
        y = 0
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(self._cells)):
                break
            y = 0
            _1 = True
            j = 0
            while True:
                if _1 is True:
                    _1 = False
                else:
                    j += 1
                if not (j < self._cells[i].length):
                    break
                cell = self._cells[i][j]
                if cell is not None:
                    cell.layout(x, y)
                y += self._rowHeights[j] + self._spacingPixelsVertical
            x += self._columnWidths[i] + self._spacingPixelsHorizontal
        if self.isUndefinedWidth():
            self._canvas.setWidth((x - self._spacingPixelsHorizontal) + 'px')
        else:
            # main element defines width
            self._canvas.setWidth('')
        if self.isUndefinedHeight():
            canvasHeight = y - self._spacingPixelsVertical
        else:
            canvasHeight = self.getOffsetHeight() - self._marginTopAndBottom
            if canvasHeight < 0:
                canvasHeight = 0
        self._canvas.setHeight(canvasHeight + 'px')

    def isUndefinedHeight(self):
        return '' == self._height

    def isUndefinedWidth(self):
        return '' == self._width

    def renderRemainingComponents(self, pendingCells):
        for cell in pendingCells:
            cell.render()

    def detectRowHeights(self):
        # collect min rowheight from non-rowspanned cells
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(self._cells)):
                break
            _1 = True
            j = 0
            while True:
                if _1 is True:
                    _1 = False
                else:
                    j += 1
                if not (j < self._cells[i].length):
                    break
                cell = self._cells[i][j]
                if cell is not None:
                    # Setting fixing container width may in some situations
                    # affect height. Example: Label with wrapping text without
                    # or with relative width.

                    if cell.cc is not None and cell.widthCanAffectHeight():
                        cell.cc.setWidth(cell.getAvailableWidth() + 'px')
                        cell.cc.updateWidgetSize()
                    if cell.rowspan == 1:
                        if not cell.hasRelativeHeight() and self._rowHeights[j] < cell.getHeight():
                            self._rowHeights[j] = cell.getHeight()
                    else:
                        self.storeRowSpannedCell(cell)
        self.distributeRowSpanHeights()
        self._minRowHeights = self.cloneArray(self._rowHeights)

    def storeRowSpannedCell(self, cell):
        l = None
        for list in self._rowSpans:
            if list.span < cell.rowspan:
                continue
            else:
                # insert before this
                l = list
                break
        if l is None:
            l = self.SpanList(cell.rowspan)
            self._rowSpans.add(l)
        elif l.span != cell.rowspan:
            newL = self.SpanList(cell.rowspan)
            self._rowSpans.add(self._rowSpans.index(l), newL)
            l = newL
        l.cells.add(cell)

    def renderRemainingComponentsWithNoRelativeHeight(self, pendingCells):
        _0 = True
        iterator = pendingCells
        while True:
            if _0 is True:
                _0 = False
            if not iterator.hasNext():
                break
            cell = iterator.next()
            if not cell.hasRelativeHeight():
                cell.render()
                iterator.remove()

    def distributeColSpanWidths(self):
        """Iterates colspanned cells, ensures cols have enough space to accommodate
        them
        """
        for list in self._colSpans:
            for cell in list.cells:
                # cells with relative content may return non 0 here if on
                # subsequent renders
                width = 0 if cell.hasRelativeWidth() else cell.getWidth()
                allocated = self._columnWidths[cell.col]
                _0 = True
                i = 1
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < cell.colspan):
                        break
                    allocated += self._spacingPixelsHorizontal + self._columnWidths[cell.col + i]
                if allocated < width:
                    # columnWidths needs to be expanded due colspanned cell
                    neededExtraSpace = width - allocated
                    spaceForColunms = neededExtraSpace / cell.colspan
                    _1 = True
                    i = 0
                    while True:
                        if _1 is True:
                            _1 = False
                        else:
                            i += 1
                        if not (i < cell.colspan):
                            break
                        col = cell.col + i
                        self._columnWidths[col] += spaceForColunms
                        neededExtraSpace -= spaceForColunms
                    if neededExtraSpace > 0:
                        _2 = True
                        i = 0
                        while True:
                            if _2 is True:
                                _2 = False
                            else:
                                i += 1
                            if not (i < cell.colspan):
                                break
                            col = cell.col + i
                            self._columnWidths[col] += 1
                            neededExtraSpace -= 1
                            if neededExtraSpace == 0:
                                break

    def distributeRowSpanHeights(self):
        """Iterates rowspanned cells, ensures rows have enough space to accommodate
        them
        """
        for list in self._rowSpans:
            for cell in list.cells:
                # cells with relative content may return non 0 here if on
                # subsequent renders
                height = 0 if cell.hasRelativeHeight() else cell.getHeight()
                allocated = self._rowHeights[cell.row]
                _0 = True
                i = 1
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < cell.rowspan):
                        break
                    allocated += self._spacingPixelsVertical + self._rowHeights[cell.row + i]
                if allocated < height:
                    # columnWidths needs to be expanded due colspanned cell
                    neededExtraSpace = height - allocated
                    spaceForColunms = neededExtraSpace / cell.rowspan
                    _1 = True
                    i = 0
                    while True:
                        if _1 is True:
                            _1 = False
                        else:
                            i += 1
                        if not (i < cell.rowspan):
                            break
                        row = cell.row + i
                        self._rowHeights[row] += spaceForColunms
                        neededExtraSpace -= spaceForColunms
                    if neededExtraSpace > 0:
                        _2 = True
                        i = 0
                        while True:
                            if _2 is True:
                                _2 = False
                            else:
                                i += 1
                            if not (i < cell.rowspan):
                                break
                            row = cell.row + i
                            self._rowHeights[row] += 1
                            neededExtraSpace -= 1
                            if neededExtraSpace == 0:
                                break

    _colSpans = LinkedList()
    _rowSpans = LinkedList()
    _marginTopAndBottom = None

    class SpanList(object):
        span = None
        _cells = LinkedList()

        def __init__(self, span):
            self.span = span

    def storeColSpannedCell(self, cell):
        l = None
        for list in self._colSpans:
            if list.span < cell.colspan:
                continue
            else:
                # insert before this
                l = list
                break
        if l is None:
            l = self.SpanList(cell.colspan)
            self._colSpans.add(l)
        elif l.span != cell.colspan:
            newL = self.SpanList(cell.colspan)
            self._colSpans.add(self._colSpans.index(l), newL)
            l = newL
        l.cells.add(cell)

    def detectSpacing(self, uidl):
        spacingmeter = Document.get().createDivElement()
        spacingmeter.setClassName(self.CLASSNAME + '-' + 'spacing-' + ('on' if uidl.getBooleanAttribute('spacing') else 'off'))
        spacingmeter.getStyle().setProperty('width', '0')
        spacingmeter.getStyle().setProperty('height', '0')
        self._canvas.getElement().appendChild(spacingmeter)
        self._spacingPixelsHorizontal = spacingmeter.getOffsetWidth()
        self._spacingPixelsVertical = spacingmeter.getOffsetHeight()
        self._canvas.getElement().removeChild(spacingmeter)

    def handleMargins(self, uidl):
        margins = VMarginInfo(uidl.getIntAttribute('margins'))
        styles = self.CLASSNAME + '-margin'
        if margins.hasTop():
            styles += ' ' + self.CLASSNAME + '-' + StyleConstants.MARGIN_TOP
        if margins.hasRight():
            styles += ' ' + self.CLASSNAME + '-' + StyleConstants.MARGIN_RIGHT
        if margins.hasBottom():
            styles += ' ' + self.CLASSNAME + '-' + StyleConstants.MARGIN_BOTTOM
        if margins.hasLeft():
            styles += ' ' + self.CLASSNAME + '-' + StyleConstants.MARGIN_LEFT
        self._margin.setClassName(styles)
        self._marginTopAndBottom = self._margin.getOffsetHeight() - self._canvas.getOffsetHeight()

    def hasChildComponent(self, component):
        return component in self._paintableToCell

    def replaceChildComponent(self, oldComponent, newComponent):
        componentContainer = self.widgetToComponentContainer.remove(oldComponent)
        if componentContainer is None:
            return
        componentContainer.setWidget(newComponent)
        self.widgetToComponentContainer.put(newComponent, componentContainer)
        self._paintableToCell.put(newComponent, self._paintableToCell[oldComponent])

    def updateCaption(self, component, uidl):
        cc = self.widgetToComponentContainer[component]
        if cc is not None:
            cc.updateCaption(uidl, self._client)
        if not self._rendering:
            # ensure rel size details are updated
            self._paintableToCell[component].updateRelSizeStatus(uidl)
            # This was a component-only update and the possible size change
            # must be propagated to the layout

            self._client.captionSizeUpdated(component)

    def requestLayout(self, changedChildren):
        needsLayout = False
        reDistributeColSpanWidths = False
        reDistributeRowSpanHeights = False
        offsetHeight = self._canvas.getOffsetHeight()
        offsetWidth = self._canvas.getOffsetWidth()
        if ('' == self._width) or ('' == self._height):
            needsLayout = True
        dirtyColumns = list()
        dirtyRows = list()
        for paintable in changedChildren:
            cell = self._paintableToCell[paintable]
            if (not cell.hasRelativeHeight()) or (not cell.hasRelativeWidth()):
                # cell sizes will only stay still if only relatively
                # sized components
                # check if changed child affects min col widths
                assert cell.cc is not None
                cell.cc.setWidth('')
                cell.cc.setHeight('')
                cell.cc.updateWidgetSize()
                # If this is the result of an caption icon onload event the
                # caption size may have changed

                cell.cc.updateCaptionSize()
                width = cell.getWidth()
                allocated = self._columnWidths[cell.col]
                _0 = True
                i = 1
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < cell.colspan):
                        break
                    allocated += self._spacingPixelsHorizontal + self._columnWidths[cell.col + i]
                if allocated < width:
                    needsLayout = True
                    if cell.colspan == 1:
                        # do simple column width expansion
                        self._columnWidths[cell.col] = self._minColumnWidths[cell.col] = width
                    else:
                        # mark that col span expansion is needed
                        reDistributeColSpanWidths = True
                elif allocated != width:
                    # size is smaller thant allocated, column might
                    # shrink
                    dirtyColumns.add(cell.col)
                height = cell.getHeight()
                allocated = self._rowHeights[cell.row]
                _1 = True
                i = 1
                while True:
                    if _1 is True:
                        _1 = False
                    else:
                        i += 1
                    if not (i < cell.rowspan):
                        break
                    allocated += self._spacingPixelsVertical + self._rowHeights[cell.row + i]
                if allocated < height:
                    needsLayout = True
                    if cell.rowspan == 1:
                        # do simple row expansion
                        self._rowHeights[cell.row] = self._minRowHeights[cell.row] = height
                    else:
                        # mark that row span expansion is needed
                        reDistributeRowSpanHeights = True
                elif allocated != height:
                    # size is smaller than allocated, row might shrink
                    dirtyRows.add(cell.row)
        if len(dirtyColumns) > 0:
            for colIndex in dirtyColumns:
                colW = 0
                _2 = True
                i = 0
                while True:
                    if _2 is True:
                        _2 = False
                    else:
                        i += 1
                    if not (i < len(self._rowHeights)):
                        break
                    cell = self._cells[colIndex][i]
                    if (
                        cell is not None and cell.getChildUIDL() is not None and not cell.hasRelativeWidth() and cell.colspan == 1
                    ):
                        width = cell.getWidth()
                        if width > colW:
                            colW = width
                self._minColumnWidths[colIndex] = colW
            needsLayout = True
            # ensure colspanned columns have enough space
            self._columnWidths = self.cloneArray(self._minColumnWidths)
            self.distributeColSpanWidths()
            reDistributeColSpanWidths = False
        if reDistributeColSpanWidths:
            self.distributeColSpanWidths()
        if len(dirtyRows) > 0:
            needsLayout = True
            for rowIndex in dirtyRows:
                # recalculate min row height
                rowH = self._minRowHeights[rowIndex] = 0
                # loop all columns on row rowIndex
                _3 = True
                i = 0
                while True:
                    if _3 is True:
                        _3 = False
                    else:
                        i += 1
                    if not (i < len(self._columnWidths)):
                        break
                    cell = self._cells[i][rowIndex]
                    if (
                        cell is not None and cell.getChildUIDL() is not None and not cell.hasRelativeHeight() and cell.rowspan == 1
                    ):
                        h = cell.getHeight()
                        if h > rowH:
                            rowH = h
                self._minRowHeights[rowIndex] = rowH
            # TODO could check only some row spans
            self._rowHeights = self.cloneArray(self._minRowHeights)
            self.distributeRowSpanHeights()
            reDistributeRowSpanHeights = False
        if reDistributeRowSpanHeights:
            self.distributeRowSpanHeights()
        if needsLayout:
            self.expandColumns()
            self.expandRows()
            self.layoutCells()
            # loop all relative sized components and update their size
            _4 = True
            i = 0
            while True:
                if _4 is True:
                    _4 = False
                else:
                    i += 1
                if not (i < len(self._cells)):
                    break
                _5 = True
                j = 0
                while True:
                    if _5 is True:
                        _5 = False
                    else:
                        j += 1
                    if not (j < self._cells[i].length):
                        break
                    cell = self._cells[i][j]
                    if (
                        cell is not None and cell.cc is not None and cell.hasRelativeHeight() or cell.hasRelativeWidth()
                    ):
                        self._client.handleComponentRelativeSize(cell.cc.getWidget())
        if (
            (self._canvas.getOffsetHeight() != offsetHeight) or (self._canvas.getOffsetWidth() != offsetWidth)
        ):
            return False
        else:
            return True

    def getAllocatedSpace(self, child):
        cell = self._paintableToCell[child]
        assert cell is not None
        return cell.getAllocatedSpace()

    _cells = None

    class Cell(object):
        """Private helper class."""
        _relHeight = False
        _relWidth = False
        _widthCanAffectHeight = False

        def __init__(self, c):
            self.row = c.getIntAttribute('y')
            self.col = c.getIntAttribute('x')
            self.setUidl(c)

        def widthCanAffectHeight(self):
            return self._widthCanAffectHeight

        def hasRelativeHeight(self):
            return self._relHeight

        def getAllocatedSpace(self):
            return RenderSpace(self.getAvailableWidth() - self._cc.getCaptionWidthAfterComponent(), self.getAvailableHeight() - self._cc.getCaptionHeightAboveComponent())

        def hasContent(self):
            return self._childUidl is not None

        def getAvailableWidth(self):
            """@return total of spanned cols"""
            width = self.columnWidths[self.col]
            _0 = True
            i = 1
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < self._colspan):
                    break
                width += self.spacingPixelsHorizontal + self.columnWidths[self.col + i]
            return width

        def getAvailableHeight(self):
            """@return total of spanned rows"""
            height = self.rowHeights[self.row]
            _0 = True
            i = 1
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < self._rowspan):
                    break
                height += self.spacingPixelsVertical + self.rowHeights[self.row + i]
            return height

        def layout(self, x, y):
            if self._cc is not None and self._cc.isAttached():
                self.canvas.setWidgetPosition(self._cc, x, y)
                self._cc.setContainerSize(self.getAvailableWidth(), self.getAvailableHeight())
                self._cc.setAlignment(AlignmentInfo(self._alignment))
                self._cc.updateAlignments(self.getAvailableWidth(), self.getAvailableHeight())

        def getWidth(self):
            if self._cc is not None:
                w = self._cc.getWidgetSize().getWidth() + self._cc.getCaptionWidthAfterComponent()
                return w
            else:
                return 0

        def getHeight(self):
            if self._cc is not None:
                return self._cc.getWidgetSize().getHeight() + self._cc.getCaptionHeightAboveComponent()
            else:
                return 0

        def renderIfNoRelativeWidth(self):
            if self._childUidl is None:
                return False
            if not self.hasRelativeWidth():
                self.render()
                return True
            else:
                return False

        def hasRelativeWidth(self):
            return self._relWidth

        def render(self):
            assert self._childUidl is not None
            paintable = self.client.getPaintable(self._childUidl)
            assert paintable is not None
            if (self._cc is None) or (self._cc.getWidget() != paintable):
                if paintable in self.widgetToComponentContainer:
                    # Component moving from one place to another
                    self._cc = self.widgetToComponentContainer[paintable]
                    self._cc.setWidth('')
                    self._cc.setHeight('')
                    # Widget might not be set if moving from another component
                    # and this layout has been hidden when moving out, see
                    # #5372

                    self._cc.setWidget(paintable)
                else:
                    # A new component
                    self._cc = ChildComponentContainer(paintable, CellBasedLayout.ORIENTATION_VERTICAL)
                    self.widgetToComponentContainer.put(paintable, self._cc)
                    self._cc.setWidth('')
                    self.canvas.add(self._cc, 0, 0)
                self.paintableToCell.put(paintable, self)
            self._cc.renderChild(self._childUidl, self.client, -1)
            if self.sizeChangedDuringRendering and Util.isCached(self._childUidl):
                self.client.handleComponentRelativeSize(self._cc.getWidget())
            self._cc.updateWidgetSize()
            self.nonRenderedWidgets.remove(paintable)

        def getChildUIDL(self):
            return self._childUidl

        row = None
        col = None
        _colspan = 1
        _rowspan = 1
        _childUidl = None
        _alignment = None
        # may be null after setUidl() if content has vanished or changed, set
        # in render()
        _cc = None

        def setUidl(self, c):
            # Set cell width
            self._colspan = c.getIntAttribute('w') if c.hasAttribute('w') else 1
            # Set cell height
            self._rowspan = c.getIntAttribute('h') if c.hasAttribute('h') else 1
            # ensure we will lose reference to old cells, now overlapped by
            # this cell
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < self._colspan):
                    break
                _1 = True
                j = 0
                while True:
                    if _1 is True:
                        _1 = False
                    else:
                        j += 1
                    if not (j < self._rowspan):
                        break
                    if (i > 0) or (j > 0):
                        self.cells[self.col + i][self.row + j] = None
            c = c.getChildUIDL(0)
            # we are interested about childUidl
            if self._childUidl is not None:
                if c is None:
                    # content has vanished, old content will be removed from
                    # canvas later during the render phase
                    self._cc = None
                elif (
                    self._cc is not None and self._cc.getWidget() != self.client.getPaintable(c)
                ):
                    # content has changed
                    self._cc = None
                    paintable = self.client.getPaintable(c)
                    if paintable in self.widgetToComponentContainer:
                        # cc exist for this component (moved) use that for this
                        # cell
                        self._cc = self.widgetToComponentContainer[paintable]
                        self._cc.setWidth('')
                        self._cc.setHeight('')
                        self.paintableToCell.put(paintable, self)
            self._childUidl = c
            self.updateRelSizeStatus(c)

        def updateRelSizeStatus(self, uidl):
            if uidl is not None and not uidl.getBooleanAttribute('cached'):
                if (
                    uidl.hasAttribute('height') and uidl.getStringAttribute('height').contains('%')
                ):
                    self._relHeight = True
                else:
                    self._relHeight = False
                if uidl.hasAttribute('width'):
                    self._widthCanAffectHeight = self._relWidth = uidl.getStringAttribute('width').contains('%')
                    if uidl.hasAttribute('height'):
                        self._widthCanAffectHeight = False
                else:
                    self._widthCanAffectHeight = not uidl.hasAttribute('height')
                    self._relWidth = False

    def getCell(self, c):
        row = c.getIntAttribute('y')
        col = c.getIntAttribute('x')
        cell = self._cells[col][row]
        if cell is None:
            cell = self.Cell(c)
            self._cells[col][row] = cell
        else:
            cell.setUidl(c)
        return cell

    def getComponent(self, element):
        """Returns the deepest nested child component which contains "element". The
        child component is also returned if "element" is part of its caption.

        @param element
                   An element that is a nested sub element of the root element in
                   this layout
        @return The Paintable which the element is a part of. Null if the element
                belongs to the layout and not to a child.
        """
        return Util.getPaintableForElement(self._client, self, element)
