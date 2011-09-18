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

from __pyjamas__ import (ARGERROR, POSTINC,)
from com.vaadin.ui.Alignment import (Alignment,)
from com.vaadin.ui.AbstractLayout import (AbstractLayout,)
from com.vaadin.ui.Layout import (AlignmentHandler, Layout, SpacingHandler,)
from com.vaadin.ui.AlignmentUtils import (AlignmentUtils,)
from com.vaadin.terminal.gwt.client.EventId import (EventId,)
# from java.io.Serializable import (Serializable,)
# from java.util.Collections import (Collections,)
# from java.util.HashMap import (HashMap,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedList import (LinkedList,)
# from java.util.Map import (Map,)
# from java.util.Map.Entry import (Entry,)


class GridLayout(AbstractLayout, Layout, AlignmentHandler, Layout, SpacingHandler, LayoutClickNotifier):
    """<p>
    A container that consists of components with certain coordinates (cell
    position) on a grid. It also maintains cursor for adding component in left to
    right, top to bottom order.
    </p>

    <p>
    Each component in a <code>GridLayout</code> uses a certain
    {@link GridLayout.Area area} (column1,row1,column2,row2) from the grid. One
    should not add components that would overlap with the existing components
    because in such case an {@link OverlapsException} is thrown. Adding component
    with cursor automatically extends the grid by increasing the grid height.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    _CLICK_EVENT = EventId.LAYOUT_CLICK
    # Initial grid columns.
    _cols = 0
    # Initial grid rows.
    _rows = 0
    # Cursor X position: this is where the next component with unspecified x,y
    # is inserted

    _cursorX = 0
    # Cursor Y position: this is where the next component with unspecified x,y
    # is inserted

    _cursorY = 0
    # Contains all items that are placed on the grid. These are components with
    # grid area definition.

    _areas = LinkedList()
    # Mapping from components to their respective areas.
    _components = LinkedList()
    # Mapping from components to alignments (horizontal + vertical).
    _componentToAlignment = dict()
    # Is spacing between contained components enabled. Defaults to false.
    _spacing = False
    _ALIGNMENT_DEFAULT = Alignment.TOP_LEFT
    # Has there been rows inserted or deleted in the middle of the layout since
    # the last paint operation.

    _structuralChange = False
    _columnExpandRatio = dict()
    _rowExpandRatio = dict()

    def __init__(self, *args):
        """Constructor for grid of given size (number of cells). Note that grid's
        final size depends on the items that are added into the grid. Grid grows
        if you add components outside the grid's area.

        @param columns
                   Number of columns in the grid.
        @param rows
                   Number of rows in the grid.
        ---
        Constructs an empty grid layout that is extended as needed.
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.__init__(1, 1)
        elif _1 == 2:
            columns, rows = _0
            self.setColumns(columns)
            self.setRows(rows)
        else:
            raise ARGERROR(0, 2)

    def addComponent(self, *args):
        """<p>
        Adds a component with a specified area to the grid. The area the new
        component should take is defined by specifying the upper left corner
        (column1, row1) and the lower right corner (column2, row2) of the area.
        </p>

        <p>
        If the new component overlaps with any of the existing components already
        present in the grid the operation will fail and an
        {@link OverlapsException} is thrown.
        </p>

        @param c
                   the component to be added.
        @param column1
                   the column of the upper left corner of the area <code>c</code>
                   is supposed to occupy.
        @param row1
                   the row of the upper left corner of the area <code>c</code> is
                   supposed to occupy.
        @param column2
                   the column of the lower right corner of the area
                   <code>c</code> is supposed to occupy.
        @param row2
                   the row of the lower right corner of the area <code>c</code>
                   is supposed to occupy.
        @throws OverlapsException
                    if the new component overlaps with any of the components
                    already in the grid.
        @throws OutOfBoundsException
                    if the cells are outside the grid area.
        ---
        Adds the component into this container to cells column1,row1 (NortWest
        corner of the area.) End coordinates (SouthEast corner of the area) are
        the same as column1,row1. Component width and height is 1.

        @param c
                   the component to be added.
        @param column
                   the column index.
        @param row
                   the row index.
        @throws OverlapsException
                    if the new component overlaps with any of the components
                    already in the grid.
        @throws OutOfBoundsException
                    if the cell is outside the grid area.
        ---
        Adds the component into this container to the cursor position. If the
        cursor position is already occupied, the cursor is moved forwards to find
        free position. If the cursor goes out from the bottom of the grid, the
        grid is automatically extended.

        @param c
                   the component to be added.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            component, = _0
            done = False
            while not done:
                try:
                    area = self.Area(component, self._cursorX, self._cursorY, self._cursorX, self._cursorY)
                    self.checkExistingOverlaps(area)
                    done = True
                except OverlapsException, e:
                    self.space()
            # Extends the grid if needed
            self._cols = self._cursorX + 1 if self._cursorX >= self._cols else self._cols
            self._rows = self._cursorY + 1 if self._cursorY >= self._rows else self._rows
            self.addComponent(component, self._cursorX, self._cursorY)
        elif _1 == 3:
            c, column, row = _0
            self.addComponent(c, column, row, column, row)
        elif _1 == 5:
            component, column1, row1, column2, row2 = _0
            if component is None:
                raise self.NullPointerException('Component must not be null')
            # Checks that the component does not already exist in the container
            if self._components.contains(component):
                raise self.IllegalArgumentException('Component is already in the container')
            # Creates the area
            area = self.Area(component, column1, row1, column2, row2)
            # Checks the validity of the coordinates
            if (column2 < column1) or (row2 < row1):
                raise self.IllegalArgumentException('Illegal coordinates for the component')
            if (
                (((column1 < 0) or (row1 < 0)) or (column2 >= self._cols)) or (row2 >= self._rows)
            ):
                raise self.OutOfBoundsException(area)
            # Checks that newItem does not overlap with existing items
            self.checkExistingOverlaps(area)
            # Inserts the component to right place at the list
            # Respect top-down, left-right ordering
            # component.setParent(this);
            i = self._areas
            index = 0
            done = False
            while not done and i.hasNext():
                existingArea = i.next()
                if (
                    (existingArea.row1 >= row1 and existingArea.column1 > column1) or (existingArea.row1 > row1)
                ):
                    self._areas.add(index, area)
                    self._components.add(index, component)
                    done = True
                index += 1
            if not done:
                self._areas.addLast(area)
                self._components.addLast(component)
            # Attempt to add to super
            # update cursor position, if it's within this area; use first position
            # outside this area, even if it's occupied
            try:
                super(GridLayout, self).addComponent(component)
            except IllegalArgumentException, e:
                self._areas.remove(area)
                self._components.remove(component)
                raise e
            if (
                self._cursorX >= column1 and self._cursorX <= column2 and self._cursorY >= row1 and self._cursorY <= row2
            ):
                # cursor within area
                self._cursorX = column2 + 1
                # one right of area
                if self._cursorX >= self._cols:
                    # overflowed columns
                    self._cursorX = 0
                    # first col
                    # move one row down, or one row under the area
                    self._cursorY = (row2 if column1 == 0 else row1) + 1
                else:
                    self._cursorY = row1
            self.requestRepaint()
        else:
            raise ARGERROR(1, 5)

    def checkExistingOverlaps(self, area):
        """Tests if the given area overlaps with any of the items already on the
        grid.

        @param area
                   the Area to be checked for overlapping.
        @throws OverlapsException
                    if <code>area</code> overlaps with any existing area.
        """
        _0 = True
        i = self._areas
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            existingArea = i.next()
            if existingArea.overlaps(area):
                # Component not added, overlaps with existing component
                raise self.OverlapsException(existingArea)

    def newLine(self):
        """Force the next component to be added to the beginning of the next line.
        By calling this function user can ensure that no more components are
        added to the right of the previous component.

        @see #space()
        """
        self._cursorX = 0
        self._cursorY += 1

    def space(self):
        """Moves the cursor forwards by one. If the cursor goes out of the right
        grid border, move it to next line.

        @see #newLine()
        """
        self._cursorX += 1
        if self._cursorX >= self._cols:
            self._cursorX = 0
            self._cursorY += 1

    # Finds first available place from the grid

    def removeComponent(self, *args):
        """Removes the given component from this container.

        @param c
                   the component to be removed.
        ---
        Removes the component specified with it's cell index.

        @param column
                   the Component's column.
        @param row
                   the Component's row.
        """
        # Check that the component is contained in the container
        _0 = args
        _1 = len(args)
        if _1 == 1:
            component, = _0
            if (component is None) or (not self._components.contains(component)):
                return
            area = None
            _0 = True
            i = self._areas
            while True:
                if _0 is True:
                    _0 = False
                if not (area is None and i.hasNext()):
                    break
                a = i.next()
                if a.getComponent() == component:
                    area = a
            self._components.remove(component)
            if area is not None:
                self._areas.remove(area)
            self._componentToAlignment.remove(component)
            super(GridLayout, self).removeComponent(component)
            self.requestRepaint()
        elif _1 == 2:
            column, row = _0
            _0 = True
            i = self._areas
            while True:
                if _0 is True:
                    _0 = False
                if not i.hasNext():
                    break
                area = i.next()
                if area.getColumn1() == column and area.getRow1() == row:
                    self.removeComponent(area.getComponent())
                    return
        else:
            raise ARGERROR(1, 2)

    # Finds the area

    def getComponentIterator(self):
        """Gets an Iterator to the component container contents. Using the Iterator
        it's possible to step through the contents of the container.

        @return the Iterator of the components inside the container.
        """
        return Collections.unmodifiableCollection(self._components)

    def getComponentCount(self):
        """Gets the number of contained components. Consistent with the iterator
        returned by {@link #getComponentIterator()}.

        @return the number of contained components
        """
        return len(self._components)

    def paintContent(self, target):
        """Paints the contents of this component.

        @param target
                   the Paint Event.
        @throws PaintException
                    if the paint operation failed.
        """
        super(GridLayout, self).paintContent(target)
        # TODO refactor attribute names in future release.
        target.addAttribute('h', self._rows)
        target.addAttribute('w', self._cols)
        target.addAttribute('structuralChange', self._structuralChange)
        self._structuralChange = False
        if self._spacing:
            target.addAttribute('spacing', self._spacing)
        # Area iterator
        areaiterator = self._areas
        # Current item to be processed (fetch first item)
        area = areaiterator.next() if areaiterator.hasNext() else None
        # Collects rowspan related information here
        cellUsed = dict()
        # Empty cell collector
        emptyCells = 0
        alignmentsArray = [None] * len(self._components)
        columnExpandRatioArray = [None] * self._cols
        rowExpandRatioArray = [None] * self._rows
        realColExpandRatioSum = 0
        colSum = self.getExpandRatioSum(self._columnExpandRatio)
        if colSum == 0:
            # no columns has been expanded, all cols have same expand
            # rate
            equalSize = 1 / self._cols
            myRatio = self.Math.round(equalSize * 1000)
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < self._cols):
                    break
                columnExpandRatioArray[i] = myRatio
            realColExpandRatioSum = myRatio * self._cols
        else:
            _1 = True
            i = 0
            while True:
                if _1 is True:
                    _1 = False
                else:
                    i += 1
                if not (i < self._cols):
                    break
                myRatio = self.Math.round((self.getColumnExpandRatio(i) / colSum) * 1000)
                columnExpandRatioArray[i] = myRatio
                realColExpandRatioSum += myRatio
        equallyDividedRows = False
        realRowExpandRatioSum = 0
        rowSum = self.getExpandRatioSum(self._rowExpandRatio)
        if rowSum == 0:
            # no rows have been expanded
            equallyDividedRows = True
            equalSize = 1 / self._rows
            myRatio = self.Math.round(equalSize * 1000)
            _2 = True
            i = 0
            while True:
                if _2 is True:
                    _2 = False
                else:
                    i += 1
                if not (i < self._rows):
                    break
                rowExpandRatioArray[i] = myRatio
            realRowExpandRatioSum = myRatio * self._rows
        index = 0
        # Iterates every applicable row
        _3 = True
        cury = 0
        while True:
            if _3 is True:
                _3 = False
            else:
                cury += 1
            if not (cury < self._rows):
                break
            target.startTag('gr')
            if not equallyDividedRows:
                myRatio = self.Math.round((self.getRowExpandRatio(cury) / rowSum) * 1000)
                rowExpandRatioArray[cury] = myRatio
                realRowExpandRatioSum += myRatio
            # Iterates every applicable column
            _4 = True
            curx = 0
            while True:
                if _4 is True:
                    _4 = False
                else:
                    curx += 1
                if not (curx < self._cols):
                    break
                # Checks if current item is located at curx,cury
                if area is not None and area.row1 == cury and area.column1 == curx:
                    # First check if empty cell needs to be rendered
                    if emptyCells > 0:
                        target.startTag('gc')
                        target.addAttribute('x', curx - emptyCells)
                        target.addAttribute('y', cury)
                        if emptyCells > 1:
                            target.addAttribute('w', emptyCells)
                        target.endTag('gc')
                        emptyCells = 0
                    # Now proceed rendering current item
                    cols = (area.column2 - area.column1) + 1
                    rows = (area.row2 - area.row1) + 1
                    target.startTag('gc')
                    target.addAttribute('x', curx)
                    target.addAttribute('y', cury)
                    if cols > 1:
                        target.addAttribute('w', cols)
                    if rows > 1:
                        target.addAttribute('h', rows)
                    area.getComponent().paint(target)
                    alignmentsArray[POSTINC(globals(), locals(), 'index')] = String.valueOf.valueOf(self.getComponentAlignment(area.getComponent()).getBitMask())
                    target.endTag('gc')
                    # Fetch next item
                    if areaiterator.hasNext():
                        area = areaiterator.next()
                    else:
                        area = None
                    # Updates the cellUsed if rowspan needed
                    if rows > 1:
                        spannedx = curx
                        _5 = True
                        j = 1
                        while True:
                            if _5 is True:
                                _5 = False
                            else:
                                j += 1
                            if not (j <= cols):
                                break
                            cellUsed.put(int(spannedx), int((cury + rows) - 1))
                            spannedx += 1
                    # Skips the current item's spanned columns
                    if cols > 1:
                        curx += cols - 1
                elif int(curx) in cellUsed:
                    # Current column contains already an item,
                    # check if rowspan affects at current x,y position
                    rowspanDepth = cellUsed[int(curx)].intValue()
                    if rowspanDepth >= cury:
                        # ignore cell
                        # Check if empty cell needs to be rendered
                        if emptyCells > 0:
                            target.startTag('gc')
                            target.addAttribute('x', curx - emptyCells)
                            target.addAttribute('y', cury)
                            if emptyCells > 1:
                                target.addAttribute('w', emptyCells)
                            target.endTag('gc')
                            emptyCells = 0
                    else:
                        # empty cell is needed
                        emptyCells += 1
                        cellUsed.remove(Integer.valueOf.valueOf(curx))
                else:
                    # empty cell is needed
                    emptyCells += 1
                # Checks against cellUsed, render space or ignore cell
            # iterates every column
            # Last column handled of current row
            # Checks if empty cell needs to be rendered
            if emptyCells > 0:
                target.startTag('gc')
                target.addAttribute('x', cols - emptyCells)
                target.addAttribute('y', cury)
                if emptyCells > 1:
                    target.addAttribute('w', emptyCells)
                target.endTag('gc')
                emptyCells = 0
            target.endTag('gr')
        # iterates every row
        # Last row handled
        # correct possible rounding error
        if len(rowExpandRatioArray) > 0:
            rowExpandRatioArray[0] -= realRowExpandRatioSum - 1000
        if len(columnExpandRatioArray) > 0:
            columnExpandRatioArray[0] -= realColExpandRatioSum - 1000
        target.addAttribute('colExpand', columnExpandRatioArray)
        target.addAttribute('rowExpand', rowExpandRatioArray)
        # Add child component alignment info to layout tag
        target.addAttribute('alignments', alignmentsArray)

    def getExpandRatioSum(self, ratioMap):
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.Layout.AlignmentHandler#getComponentAlignment(com
        # .vaadin.ui.Component)

        sum = 0
        _0 = True
        iterator = ratioMap.entrySet()
        while True:
            if _0 is True:
                _0 = False
            if not iterator.hasNext():
                break
            sum += iterator.next().getValue()
        return sum

    def getComponentAlignment(self, childComponent):
        alignment = self._componentToAlignment[childComponent]
        if alignment is None:
            return self._ALIGNMENT_DEFAULT
        else:
            return alignment

    class Area(Serializable):
        """This class defines an area on a grid. An Area is defined by the cells of
        its upper left corner (column1,row1) and lower right corner
        (column2,row2).

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """
        # The column of the upper left corner cell of the area.
        _column1 = None
        # The row of the upper left corner cell of the area.
        _row1 = None
        # The column of the lower right corner cell of the area.
        _column2 = None
        # The row of the lower right corner cell of the area.
        _row2 = None
        # Component painted on the area.
        _component = None

        def __init__(self, component, column1, row1, column2, row2):
            """<p>
            Construct a new area on a grid.
            </p>

            @param component
                       the component connected to the area.
            @param column1
                       The column of the upper left corner cell of the area
                       <code>c</code> is supposed to occupy.
            @param row1
                       The row of the upper left corner cell of the area
                       <code>c</code> is supposed to occupy.
            @param column2
                       The column of the lower right corner cell of the area
                       <code>c</code> is supposed to occupy.
            @param row2
                       The row of the lower right corner cell of the area
                       <code>c</code> is supposed to occupy.
            @throws OverlapsException
                        if the new component overlaps with any of the components
                        already in the grid
            """
            self._column1 = column1
            self._row1 = row1
            self._column2 = column2
            self._row2 = row2
            self._component = component

        def overlaps(self, other):
            """Tests if the given Area overlaps with an another Area.

            @param other
                       the Another Area that's to be tested for overlap with this
                       area.
            @return <code>true</code> if <code>other</code> overlaps with this
                    area, <code>false</code> if it doesn't.
            """
            return self._column1 <= other.getColumn2() and self._row1 <= other.getRow2() and self._column2 >= other.getColumn1() and self._row2 >= other.getRow1()

        def getComponent(self):
            """Gets the component connected to the area.

            @return the Component.
            """
            return self._component

        def setComponent(self, newComponent):
            """Sets the component connected to the area.

            <p>
            This function only sets the value in the datastructure and does not
            send any events or set parents.
            </p>

            @param newComponent
                       the new connected overriding the existing one.
            """
            self._component = newComponent

        def getX1(self):
            """@deprecated Use getColumn1() instead.

            @see com.vaadin.ui.GridLayout#getColumn1()
            """
            return self.getColumn1()

        def getColumn1(self):
            """Gets the column of the top-left corner cell.

            @return the column of the top-left corner cell.
            """
            return self._column1

        def getX2(self):
            """@deprecated Use getColumn2() instead.

            @see com.vaadin.ui.GridLayout#getColumn2()
            """
            return self.getColumn2()

        def getColumn2(self):
            """Gets the column of the bottom-right corner cell.

            @return the column of the bottom-right corner cell.
            """
            return self._column2

        def getY1(self):
            """@deprecated Use getRow1() instead.

            @see com.vaadin.ui.GridLayout#getRow1()
            """
            return self.getRow1()

        def getRow1(self):
            """Gets the row of the top-left corner cell.

            @return the row of the top-left corner cell.
            """
            return self._row1

        def getY2(self):
            """@deprecated Use getRow2() instead.

            @see com.vaadin.ui.GridLayout#getRow2()
            """
            return self.getRow2()

        def getRow2(self):
            """Gets the row of the bottom-right corner cell.

            @return the row of the bottom-right corner cell.
            """
            return self._row2

    class OverlapsException(java.lang.RuntimeException):
        """Gridlayout does not support laying components on top of each other. An
        <code>OverlapsException</code> is thrown when a component already exists
        (even partly) at the same space on a grid with the new component.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """
        _existingArea = None

        def __init__(self, existingArea):
            """Constructs an <code>OverlapsException</code>.

            @param existingArea
            """
            self._existingArea = existingArea

        def getMessage(self):
            sb = self.StringBuilder()
            component = self._existingArea.getComponent()
            sb.append(component)
            sb.append('( type = ')
            sb.append(component.getClass().getName())
            if component.getCaption() is not None:
                sb.append(', caption = \"')
                sb.append(component.getCaption())
                sb.append('\"')
            sb.append(')')
            sb.append(' is already added to ')
            sb.append(self._existingArea.column1)
            sb.append(',')
            sb.append(self._existingArea.column1)
            sb.append(',')
            sb.append(self._existingArea.row1)
            sb.append(',')
            sb.append(self._existingArea.row2)
            sb.append('(column1, column2, row1, row2).')
            return str(sb)

        def getArea(self):
            """Gets the area .

            @return the existing area.
            """
            return self._existingArea

    class OutOfBoundsException(java.lang.RuntimeException):
        """An <code>Exception</code> object which is thrown when an area exceeds the
        bounds of the grid.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """
        _areaOutOfBounds = None

        def __init__(self, areaOutOfBounds):
            """Constructs an <code>OoutOfBoundsException</code> with the specified
            detail message.

            @param areaOutOfBounds
            """
            self._areaOutOfBounds = areaOutOfBounds

        def getArea(self):
            """Gets the area that is out of bounds.

            @return the area out of Bound.
            """
            return self._areaOutOfBounds

    def setColumns(self, columns):
        """Sets the number of columns in the grid. The column count can not be
        reduced if there are any areas that would be outside of the shrunk grid.

        @param columns
                   the new number of columns in the grid.
        """
        # The the param
        if columns < 1:
            raise self.IllegalArgumentException('The number of columns and rows in the grid must be at least 1')
        # In case of no change
        if self._cols == columns:
            return
        # Checks for overlaps
        if self._cols > columns:
            _0 = True
            i = self._areas
            while True:
                if _0 is True:
                    _0 = False
                if not i.hasNext():
                    break
                area = i.next()
                if area.column2 >= columns:
                    raise self.OutOfBoundsException(area)
        self._cols = columns
        self.requestRepaint()

    def getColumns(self):
        """Get the number of columns in the grid.

        @return the number of columns in the grid.
        """
        return self._cols

    def setRows(self, rows):
        """Sets the number of rows in the grid. The number of rows can not be
        reduced if there are any areas that would be outside of the shrunk grid.

        @param rows
                   the new number of rows in the grid.
        """
        # The the param
        if rows < 1:
            raise self.IllegalArgumentException('The number of columns and rows in the grid must be at least 1')
        # In case of no change
        if self._rows == rows:
            return
        # Checks for overlaps
        if self._rows > rows:
            _0 = True
            i = self._areas
            while True:
                if _0 is True:
                    _0 = False
                if not i.hasNext():
                    break
                area = i.next()
                if area.row2 >= rows:
                    raise self.OutOfBoundsException(area)
        self._rows = rows
        self.requestRepaint()

    def getRows(self):
        """Get the number of rows in the grid.

        @return the number of rows in the grid.
        """
        return self._rows

    def getCursorX(self):
        """Gets the current cursor x-position. The cursor position points the
        position for the next component that is added without specifying its
        coordinates (grid cell). When the cursor position is occupied, the next
        component will be added to first free position after the cursor.

        @return the grid column the Cursor is on.
        """
        return self._cursorX

    def setCursorX(self, cursorX):
        """Sets the current cursor x-position. This is usually handled automatically
        by GridLayout.

        @param cursorX
        """
        self._cursorX = cursorX

    def getCursorY(self):
        """Gets the current cursor y-position. The cursor position points the
        position for the next component that is added without specifying its
        coordinates (grid cell). When the cursor position is occupied, the next
        component will be added to first free position after the cursor.

        @return the grid row the Cursor is on.
        """
        return self._cursorY

    def setCursorY(self, cursorY):
        """Sets the current cursor y-position. This is usually handled automatically
        by GridLayout.

        @param cursorY
        """
        # Documented in superclass
        self._cursorY = cursorY

    def replaceComponent(self, oldComponent, newComponent):
        # Gets the locations
        # Removes all components from this container.
        # 
        # @see com.vaadin.ui.ComponentContainer#removeAllComponents()

        oldLocation = None
        newLocation = None
        _0 = True
        i = self._areas
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            location = i.next()
            component = location.getComponent()
            if component == oldComponent:
                oldLocation = location
            if component == newComponent:
                newLocation = location
        if oldLocation is None:
            self.addComponent(newComponent)
        elif newLocation is None:
            self.removeComponent(oldComponent)
            self.addComponent(newComponent, oldLocation.getColumn1(), oldLocation.getRow1(), oldLocation.getColumn2(), oldLocation.getRow2())
        else:
            oldLocation.setComponent(newComponent)
            newLocation.setComponent(oldComponent)
            self.requestRepaint()

    def removeAllComponents(self):
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.Layout.AlignmentHandler#setComponentAlignment(com
        # .vaadin.ui.Component, int, int)

        super(GridLayout, self).removeAllComponents()
        self._componentToAlignment = dict()
        self._cursorX = 0
        self._cursorY = 0

    def setComponentAlignment(self, *args):
        """None
        ---
        Sets the component alignment using a short hand string notation.

        @deprecated Replaced by
                    {@link #setComponentAlignment(Component, Alignment)}

        @param component
                   A child component in this layout
        @param alignment
                   A short hand notation described in {@link AlignmentUtils}
        """
        _0 = args
        _1 = len(args)
        if _1 == 2:
            if isinstance(_0[1], Alignment):
                childComponent, alignment = _0
                self._componentToAlignment.put(childComponent, alignment)
                self.requestRepaint()
            else:
                component, alignment = _0
                AlignmentUtils.setComponentAlignment(self, component, alignment)
        elif _1 == 3:
            childComponent, horizontalAlignment, verticalAlignment = _0
            self._componentToAlignment.put(childComponent, Alignment(horizontalAlignment + verticalAlignment))
            self.requestRepaint()
        else:
            raise ARGERROR(2, 3)

    # (non-Javadoc)
    # 
    # @see com.vaadin.ui.Layout.SpacingHandler#setSpacing(boolean)

    def setSpacing(self, enabled):
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.Layout.SpacingHandler#isSpacing()

        self._spacing = enabled
        self.requestRepaint()

    def isSpacingEnabled(self):
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.Layout.SpacingHandler#isSpacing()

        return self._spacing

    def isSpacing(self):
        return self._spacing

    def insertRow(self, row):
        """Inserts an empty row at the chosen position in the grid.

        @param row
                   Number of the row the new row will be inserted before
        """
        if row > self._rows:
            raise self.IllegalArgumentException('Cannot insert row at ' + row + ' in a gridlayout with height ' + self._rows)
        _0 = True
        i = self._areas
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            existingArea = i.next()
            # Areas ending below the row needs to be moved down or stretched
            if existingArea.row2 >= row:
                existingArea.row2 += 1
                if existingArea.row1 >= row:
                    existingArea.row1 += 1
        if self._cursorY >= row:
            self._cursorY += 1
        self.setRows(self._rows + 1)
        self._structuralChange = True
        self.requestRepaint()

    def removeRow(self, row):
        """Removes row and all components in the row. Components which span over
        several rows are removed if the selected row is the component's first
        row.
        <p>
        If the last row is removed then all remaining components will be removed
        and the grid will be reduced to one row. The cursor will be moved to the
        upper left cell of the grid.
        </p>

        @param row
                   The row number to remove
        """
        if row >= self._rows:
            raise self.IllegalArgumentException('Cannot delete row ' + row + ' from a gridlayout with height ' + self._rows)
        # Remove all components in row
        _0 = True
        col = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                col += 1
            if not (col < self.getColumns()):
                break
            self.removeComponent(col, row)
        # Shrink or remove areas in the selected row
        _1 = True
        i = self._areas
        while True:
            if _1 is True:
                _1 = False
            if not i.hasNext():
                break
            existingArea = i.next()
            if existingArea.row2 >= row:
                existingArea.row2 -= 1
                if existingArea.row1 > row:
                    existingArea.row1 -= 1
        if self._rows == 1:
            # Removing the last row means that the dimensions of the Grid
            # layout will be truncated to 1 empty row and the cursor is moved
            # to the first cell

            self._cursorX = 0
            self._cursorY = 0
        else:
            self.setRows(self._rows - 1)
            if self._cursorY > row:
                self._cursorY -= 1
        self._structuralChange = True
        self.requestRepaint()

    def setColumnExpandRatio(self, columnIndex, ratio):
        """Sets the expand ratio of given column. Expand ratio defines how excess
        space is distributed among columns. Excess space means the space not
        consumed by non relatively sized components.

        <p>
        By default excess space is distributed evenly.

        <p>
        Note, that width needs to be defined for this method to have any effect.

        @see #setWidth(float, int)

        @param columnIndex
        @param ratio
        """
        self._columnExpandRatio.put(columnIndex, ratio)
        self.requestRepaint()

    def getColumnExpandRatio(self, columnIndex):
        """Returns the expand ratio of given column

        @see #setColumnExpandRatio(int, float)

        @param columnIndex
        @return the expand ratio, 0.0f by default
        """
        r = self._columnExpandRatio[columnIndex]
        return 0 if r is None else r.floatValue()

    def setRowExpandRatio(self, rowIndex, ratio):
        """Sets the expand ratio of given row. Expand ratio defines how excess space
        is distributed among rows. Excess space means the space not consumed by
        non relatively sized components.

        <p>
        By default excess space is distributed evenly.

        <p>
        Note, that height needs to be defined for this method to have any effect.

        @see #setHeight(float, int)

        @param rowIndex
        @param ratio
        """
        self._rowExpandRatio.put(rowIndex, ratio)
        self.requestRepaint()

    def getRowExpandRatio(self, rowIndex):
        """Returns the expand ratio of given row.

        @see #setRowExpandRatio(int, float)

        @param rowIndex
        @return the expand ratio, 0.0f by default
        """
        r = self._rowExpandRatio[rowIndex]
        return 0 if r is None else r.floatValue()

    def getComponent(self, x, y):
        """Gets the Component at given index.

        @param x
                   x-index
        @param y
                   y-index
        @return Component in given cell or null if empty
        """
        _0 = True
        iterator = self._areas
        while True:
            if _0 is True:
                _0 = False
            if not iterator.hasNext():
                break
            area = iterator.next()
            if (
                area.getColumn1() <= x and x <= area.getColumn2() and area.getRow1() <= y and y <= area.getRow2()
            ):
                return area.getComponent()
        return None

    def getComponentArea(self, component):
        """Returns information about the area where given component is layed in the
        GridLayout.

        @param component
                   the component whose area information is requested.
        @return an Area object that contains information how component is layed
                in the grid
        """
        _0 = True
        iterator = self._areas
        while True:
            if _0 is True:
                _0 = False
            if not iterator.hasNext():
                break
            area = iterator.next()
            if area.getComponent() == component:
                return area
        return None

    def addListener(self, listener):
        self.addListener(self._CLICK_EVENT, self.LayoutClickEvent, listener, self.LayoutClickListener.clickMethod)

    def removeListener(self, listener):
        self.removeListener(self._CLICK_EVENT, self.LayoutClickEvent, listener)
