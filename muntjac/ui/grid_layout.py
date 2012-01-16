# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

"""Defines a container that consists of components with certain coordinates
on a grid."""

from warnings import warn

try:
    from cStringIO import StringIO
except ImportError, e:
    from StringIO import StringIO

from muntjac.ui.alignment import Alignment
from muntjac.ui.abstract_layout import AbstractLayout
from muntjac.ui.layout import IAlignmentHandler, ISpacingHandler
from muntjac.ui.alignment_utils import AlignmentUtils
from muntjac.terminal.gwt.client.event_id import EventId

from muntjac.event.layout_events import \
    ILayoutClickNotifier, LayoutClickEvent, ILayoutClickListener

from muntjac.util import fullname


class GridLayout(AbstractLayout, IAlignmentHandler, ISpacingHandler,
            ILayoutClickNotifier):
    """A container that consists of components with certain coordinates (cell
    position) on a grid. It also maintains cursor for adding component in
    left to right, top to bottom order.

    Each component in a C{GridLayout} uses a certain L{area<grid_layout.Area>}
    (column1,row1,column2,row2) from the grid. One should not add components
    that would overlap with the existing components because in such case an
    L{OverlapsException} is thrown. Adding component with cursor automatically
    extends the grid by increasing the grid height.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    CLIENT_WIDGET = None #ClientWidget(VGridLayout, LoadStyle.EAGER)

    _CLICK_EVENT = EventId.LAYOUT_CLICK
    _ALIGNMENT_DEFAULT = Alignment.TOP_LEFT

    def __init__(self, columns=1, rows=1):
        """Constructor for grid of given size (number of cells). Note that
        grid's final size depends on the items that are added into the grid.
        Grid grows if you add components outside the grid's area.

        @param columns:
                   Number of columns in the grid.
        @param rows:
                   Number of rows in the grid.
        """
        super(GridLayout, self).__init__()

        #: Initial grid columns.
        self._cols = 0

        #: Initial grid rows.
        self._rows = 0

        #: Cursor X position: this is where the next component with
        #  unspecified x,y is inserted
        self._cursorX = 0

        #: Cursor Y position: this is where the next component with
        #  unspecified x,y is inserted
        self._cursorY = 0

        #: Contains all items that are placed on the grid. These are
        #  components with grid area definition.
        self._areas = list()

        #: Mapping from components to their respective areas.
        self._components = list()

        #: Mapping from components to alignments (horizontal + vertical).
        self._componentToAlignment = dict()

        #: Is spacing between contained components enabled. Defaults to
        #  false.
        self._spacing = False

        #: Has there been rows inserted or deleted in the middle of the
        #  layout since the last paint operation.
        self._structuralChange = False

        self._columnExpandRatio = dict()
        self._rowExpandRatio = dict()

        self.setColumns(columns)
        self.setRows(rows)


    def addComponent(self, *args):
        """Adds a component with a specified area to the grid. The area the
        new component should take is defined by specifying the upper left
        corner (column1, row1) and the lower right corner (column2, row2) of
        the area.

        If the new component overlaps with any of the existing components
        already present in the grid the operation will fail and an
        L{OverlapsException} is thrown.

        Alternatively, adds the component into this container to cells
        column1,row1 (NortWest corner of the area.) End coordinates (SouthEast
        corner of the area) are the same as column1,row1. Component width and
        height is 1.

        Finally, adds the component into this container to the cursor position.
        If the cursor position is already occupied, the cursor is moved
        forwards to find free position. If the cursor goes out from the bottom
        of the grid, the grid is automatically extended.

        @param args: tuple of the form
            - (c, column1, row1, column2, row2)
              1. the component to be added.
              2. the column of the upper left corner of the area
                 C{c} is supposed to occupy.
              3. the row of the upper left corner of the area
                 C{c} is supposed to occupy.
              4. the column of the lower right corner of the area
                 C{c} is supposed to occupy.
              5. the row of the lower right corner of the area
                 C{c} is supposed to occupy.
            - (c, column, row)
              1. the component to be added.
              2. the column index.
              3. the row index.
            - (c)
              1. the component to be added.
        @raise OverlapsException:
                    if the new component overlaps with any of the components
                    already in the grid.
        @raise OutOfBoundsException:
                    if the cell is outside the grid area.
        """
        nargs = len(args)
        if nargs == 1:
            component, = args
            # Finds first available place from the grid
            done = False
            while not done:
                try:
                    area = Area(component, self._cursorX, self._cursorY,
                            self._cursorX, self._cursorY)
                    self.checkExistingOverlaps(area)
                    done = True
                except OverlapsException, e:
                    self.space()

            # Extends the grid if needed
            if self._cursorX >= self._cols:
                self._cols = self._cursorX + 1
            else:
                self._cols = self._cols

            if self._cursorY >= self._rows:
                self._rows = self._cursorY + 1
            else:
                self._rows = self._rows

            self.addComponent(component, self._cursorX, self._cursorY)
        elif nargs == 3:
            c, column, row = args
            self.addComponent(c, column, row, column, row)
        elif nargs == 5:
            component, column1, row1, column2, row2 = args

            if component is None:
                raise ValueError, 'Component must not be null'

            # Checks that the component does not already exist in the container
            if component in self._components:
                raise ValueError, 'Component is already in the container'

            # Creates the area
            area = Area(component, column1, row1, column2, row2)

            # Checks the validity of the coordinates
            if column2 < column1 or row2 < row1:
                raise ValueError, 'Illegal coordinates for the component'

            if (column1 < 0 or row1 < 0 or column2 >= self._cols
                    or row2 >= self._rows):
                raise OutOfBoundsException(area)

            # Checks that newItem does not overlap with existing items
            self.checkExistingOverlaps(area)

            # Inserts the component to right place at the list
            # Respect top-down, left-right ordering
            # component.setParent(this);
            index = 0
            done = False
            while not done and (index < len(self._areas)):
                existingArea = self._areas[index]
                if ((existingArea._row1 >= row1
                        and existingArea._column1 > column1)
                                or (existingArea._row1 > row1)):
                    self._areas.insert(index, area)
                    self._components.insert(index, component)
                    done = True
                index += 1

            if not done:
                self._areas.append(area)
                self._components.append(component)

            # Attempt to add to super
            try:
                super(GridLayout, self).addComponent(component)
            except ValueError, e:
                self._areas.remove(area)
                self._components.remove(component)
                raise e

            # update cursor position, if it's within this area; use first
            # position outside this area, even if it's occupied
            if (self._cursorX >= column1 and self._cursorX <= column2
                    and self._cursorY >= row1 and self._cursorY <= row2):
                # cursor within area
                self._cursorX = column2 + 1  # one right of area
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
            raise ValueError, 'invalid number of arguments'


    def checkExistingOverlaps(self, area):
        """Tests if the given area overlaps with any of the items already
        on the grid.

        @param area:
                   the Area to be checked for overlapping.
        @raise OverlapsException:
                    if C{area} overlaps with any existing area.
        """
        for existingArea in self._areas:
            if existingArea.overlaps(area):
                # Component not added, overlaps with existing component
                raise OverlapsException(existingArea)


    def newLine(self):
        """Force the next component to be added to the beginning of the next
        line. By calling this function user can ensure that no more components
        are added to the right of the previous component.

        @see: L{space}
        """
        self._cursorX = 0
        self._cursorY += 1


    def space(self):
        """Moves the cursor forwards by one. If the cursor goes out of the
        right grid border, move it to next line.

        @see: L{newLine}
        """
        self._cursorX += 1
        if self._cursorX >= self._cols:
            self._cursorX = 0
            self._cursorY += 1


    def removeComponent(self, *args):
        """Removes the given component from this container or removes the
        component specified with it's cell index.

        @param args: tuple of the form
            - (c)
              1. the component to be removed.
            - (column, row)
              1. the component's column.
              2. the component's row.
        """
        # Check that the component is contained in the container
        nargs = len(args)
        if nargs == 1:
            component, = args
            if component is None or component not in self._components:
                return
            area = None
            for a in self._areas:
                if a.getComponent() == component:
                    area = a

            self._components.remove(component)
            if area is not None:
                self._areas.remove(area)

            if component in self._componentToAlignment:
                del self._componentToAlignment[component]

            super(GridLayout, self).removeComponent(component)

            self.requestRepaint()
        elif nargs == 2:
            column, row = args
            # Finds the area
            for area in self._areas:
                if area.getColumn1() == column and area.getRow1() == row:
                    self.removeComponent(area.getComponent())
                    return
        else:
            raise ValueError, 'too many arguments'


    def getComponentIterator(self):
        """Gets an iterator to the component container contents. Using the
        Iterator it's possible to step through the contents of the container.

        @return: the iterator of the components inside the container.
        """
        return iter(self._components)


    def getComponentCount(self):
        """Gets the number of contained components. Consistent with the
        iterator returned by L{getComponentIterator}.

        @return: the number of contained components
        """
        return len(self._components)


    def paintContent(self, target):
        """Paints the contents of this component.

        @param target: the Paint Event.
        @raise PaintException: if the paint operation failed.
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
        areaiterator = iter(self._areas)

        # Current item to be processed (fetch first item)
        try:
            area = areaiterator.next()
        except StopIteration:
            area = None

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
            # no columns has been expanded, all cols have same
            # expand rate
            equalSize = 1 / float(self._cols)
            myRatio = int( round(equalSize * 1000) )
            for i in range(self._cols):
                columnExpandRatioArray[i] = myRatio

            realColExpandRatioSum = myRatio * self._cols
        else:
            for i in range(self._cols):
                myRatio = int( round((self.getColumnExpandRatio(i) / colSum)
                        * 1000) )
                columnExpandRatioArray[i] = myRatio
                realColExpandRatioSum += myRatio

        equallyDividedRows = False
        realRowExpandRatioSum = 0
        rowSum = self.getExpandRatioSum(self._rowExpandRatio)
        if rowSum == 0:
            # no rows have been expanded
            equallyDividedRows = True
            equalSize = 1 / float(self._rows)
            myRatio = int( round(equalSize * 1000) )
            for i in range(self._rows):
                rowExpandRatioArray[i] = myRatio
            realRowExpandRatioSum = myRatio * self._rows

        index = 0
        # Iterates every applicable row
        for cury in range(self._rows):
            target.startTag('gr')

            if not equallyDividedRows:
                myRatio = int( round((self.getRowExpandRatio(cury) / rowSum)
                        * 1000) )
                rowExpandRatioArray[cury] = myRatio
                realRowExpandRatioSum += myRatio

            # Iterates every applicable column
            for curx in range(self._cols):

                # Checks if current item is located at curx,cury
                if (area is not None and (area._row1 == cury)
                        and (area._column1 == curx)):

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
                    cols = (area._column2 - area._column1) + 1
                    rows = (area._row2 - area._row1) + 1
                    target.startTag('gc')

                    target.addAttribute('x', curx)
                    target.addAttribute('y', cury)

                    if cols > 1:
                        target.addAttribute('w', cols)

                    if rows > 1:
                        target.addAttribute('h', rows)

                    area.getComponent().paint(target)

                    ca = self.getComponentAlignment( area.getComponent() )
                    alignmentsArray[index] = str(ca.getBitMask())
                    index += 1

                    target.endTag('gc')

                    # Fetch next item
                    try:
                        area = areaiterator.next()
                    except StopIteration:
                        area = None

                    # Updates the cellUsed if rowspan needed
                    if rows > 1:
                        spannedx = curx
                        for _ in range(1, self._cols + 1):
                            cellUsed[int(spannedx)] = int((cury + rows) - 1)
                            spannedx += 1

                    # Skips the current item's spanned columns
                    if cols > 1:
                        curx += cols - 1
                else:
                    # Checks against cellUsed, render space or ignore cell
                    if int(curx) in cellUsed:

                        # Current column contains already an item,
                        # check if rowspan affects at current x,y position
                        rowspanDepth = int( cellUsed.get(int(curx)) )

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

                            # Removes the cellUsed key as it has become
                            # obsolete
                            del cellUsed[int(curx)]
                    else:
                        # empty cell is needed
                        emptyCells += 1

            # Last column handled of current row

            # Checks if empty cell needs to be rendered
            if emptyCells > 0:
                target.startTag('gc')
                target.addAttribute('x', self._cols - emptyCells)
                target.addAttribute('y', cury)
                if emptyCells > 1:
                    target.addAttribute('w', emptyCells)

                target.endTag('gc')

                emptyCells = 0

            target.endTag('gr')

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
        summ = 0.0
        for v in ratioMap.values():
            summ += v
        return summ


    def getComponentAlignment(self, childComponent):
        alignment = self._componentToAlignment.get(childComponent)
        if alignment is None:
            return self._ALIGNMENT_DEFAULT
        else:
            return alignment



    def setColumns(self, columns):
        """Sets the number of columns in the grid. The column count can
        not be reduced if there are any areas that would be outside of the
        shrunk grid.

        @param columns: the new number of columns in the grid.
        """
        # The the param
        if columns < 1:
            raise ValueError, ('The number of columns and rows in the '
                    'grid must be at least 1')

        # In case of no change
        if self._cols == columns:
            return

        # Checks for overlaps
        if self._cols > columns:
            for area in self._areas:
                if area.column2 >= columns:
                    raise OutOfBoundsException(area)

        self._cols = columns

        self.requestRepaint()


    def getColumns(self):
        """Get the number of columns in the grid.

        @return: the number of columns in the grid.
        """
        return self._cols


    def setRows(self, rows):
        """Sets the number of rows in the grid. The number of rows can
        not be reduced if there are any areas that would be outside of
        the shrunk grid.

        @param rows: the new number of rows in the grid.
        """
        # The the param
        if rows < 1:
            raise ValueError, ('The number of columns and rows in the '
                    'grid must be at least 1')

        # In case of no change
        if self._rows == rows:
            return

        # Checks for overlaps
        if self._rows > rows:
            for area in self._areas:
                if area.row2 >= rows:
                    raise OutOfBoundsException(area)

        self._rows = rows

        self.requestRepaint()


    def getRows(self):
        """Get the number of rows in the grid.

        @return: the number of rows in the grid.
        """
        return self._rows


    def getCursorX(self):
        """Gets the current cursor x-position. The cursor position points
        the position for the next component that is added without specifying
        its coordinates (grid cell). When the cursor position is occupied,
        the next component will be added to first free position after the
        cursor.

        @return: the grid column the Cursor is on.
        """
        return self._cursorX


    def setCursorX(self, cursorX):
        """Sets the current cursor x-position. This is usually handled
        automatically by GridLayout.
        """
        self._cursorX = cursorX


    def getCursorY(self):
        """Gets the current cursor y-position. The cursor position points
        the position for the next component that is added without specifying
        its coordinates (grid cell). When the cursor position is occupied,
        the next component will be added to first free position after the
        cursor.

        @return: the grid row the Cursor is on.
        """
        return self._cursorY


    def setCursorY(self, cursorY):
        """Sets the current cursor y-position. This is usually handled
        automatically by GridLayout.
        """
        self._cursorY = cursorY


    def replaceComponent(self, oldComponent, newComponent):
        # Gets the locations
        oldLocation = None
        newLocation = None

        for location in self._areas:
            component = location.getComponent()
            if component == oldComponent:
                oldLocation = location

            if component == newComponent:
                newLocation = location

        if oldLocation is None:
            self.addComponent(newComponent)
        elif newLocation is None:
            self.removeComponent(oldComponent)
            self.addComponent(newComponent,
                    oldLocation.getColumn1(), oldLocation.getRow1(),
                    oldLocation.getColumn2(), oldLocation.getRow2())
        else:
            oldLocation.setComponent(newComponent)
            newLocation.setComponent(oldComponent)
            self.requestRepaint()


    def removeAllComponents(self):
        # Removes all components from this container.
        super(GridLayout, self).removeAllComponents()
        self._componentToAlignment = dict()
        self._cursorX = 0
        self._cursorY = 0


    def setComponentAlignment(self, *args):
        """Sets the component alignment using a short hand string notation.

        @deprecated: Replaced by L{setComponentAlignment}
        @param args: tuple of the form
            - (component, alignment)
              1. A child component in this layout
              2. A short hand notation described in L{AlignmentUtils}
            - (childComponent, horizontalAlignment, verticalAlignment)
        """
        warn('replaced by setComponentAlignment', DeprecationWarning)

        nargs = len(args)
        if nargs == 2:
            if isinstance(args[1], Alignment):
                childComponent, alignment = args
                self._componentToAlignment[childComponent] = alignment
                self.requestRepaint()
            else:
                component, alignment = args
                AlignmentUtils.setComponentAlignment(self, component,
                        alignment)
        elif nargs == 3:
            childComponent, horizontalAlignment, verticalAlignment = args
            self._componentToAlignment[childComponent] = \
                    Alignment(horizontalAlignment + verticalAlignment)
            self.requestRepaint()
        else:
            raise ValueError, 'invalid number of arguments'


    def setSpacing(self, enabled):
        self._spacing = enabled
        self.requestRepaint()


    def isSpacingEnabled(self):
        return self._spacing


    def isSpacing(self):
        return self._spacing


    def insertRow(self, row):
        """Inserts an empty row at the chosen position in the grid.

        @param row: Number of the row the new row will be inserted before
        """
        if row > self._rows:
            raise ValueError, ('Cannot insert row at '
                    + row + ' in a gridlayout with height ' + self._rows)

        for existingArea in self._areas:
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
        """Removes row and all components in the row. Components which span
        over several rows are removed if the selected row is the component's
        first row.

        If the last row is removed then all remaining components will be
        removed and the grid will be reduced to one row. The cursor will be
        moved to the upper left cell of the grid.

        @param row: The row number to remove
        """
        if row >= self._rows:
            raise ValueError, ('Cannot delete row '
                    + row + ' from a gridlayout with height ' + self._rows)

        # Remove all components in row
        for col in range(self.getColumns()):
            self.removeComponent(col, row)

        # Shrink or remove areas in the selected row
        for existingArea in self._areas:
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
        """Sets the expand ratio of given column. Expand ratio defines how
        excess space is distributed among columns. Excess space means the
        space not consumed by non relatively sized components.

        By default excess space is distributed evenly.

        Note, that width needs to be defined for this method to have any
        effect.

        @see: L{setWidth}
        """
        self._columnExpandRatio[columnIndex] = ratio
        self.requestRepaint()


    def getColumnExpandRatio(self, columnIndex):
        """Returns the expand ratio of given column

        @see: L{setColumnExpandRatio}
        @return: the expand ratio, 0.0 by default
        """
        r = self._columnExpandRatio.get(columnIndex)
        return 0 if r is None else float(r)


    def setRowExpandRatio(self, rowIndex, ratio):
        """Sets the expand ratio of given row. Expand ratio defines how
        excess space is distributed among rows. Excess space means the
        space not consumed by non relatively sized components.

        By default excess space is distributed evenly.

        Note, that height needs to be defined for this method to have
        any effect.

        @see: L{setHeight}
        """
        self._rowExpandRatio[rowIndex] = ratio
        self.requestRepaint()


    def getRowExpandRatio(self, rowIndex):
        """Returns the expand ratio of given row.

        @see: L{setRowExpandRatio}
        @return: the expand ratio, 0.0 by default
        """
        r = self._rowExpandRatio.get(rowIndex)
        return 0 if r is None else float(r)


    def getComponent(self, x, y):
        """Gets the Component at given index.

        @param x:
                   x-index
        @param y:
                   y-index
        @return: Component in given cell or null if empty
        """
        for area in self._areas:
            if (area.getColumn1() <= x and x <= area.getColumn2()
                    and area.getRow1() <= y and y <= area.getRow2()):
                return area.getComponent()

        return None


    def getComponentArea(self, component):
        """Returns information about the area where given component is layed
        in the GridLayout.

        @param component:
                   the component whose area information is requested.
        @return: an Area object that contains information how component is
                layed in the grid
        """
        for area in self._areas:
            if area.getComponent() == component:
                return area
        return None


    def addListener(self, listener, iface=None):
        if (isinstance(listener, ILayoutClickListener) and
                (iface is None or issubclass(iface, ILayoutClickListener))):
            self.registerListener(self._CLICK_EVENT, LayoutClickEvent,
                    listener, ILayoutClickListener.clickMethod)

        super(GridLayout, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, LayoutClickEvent):
            self.registerCallback(LayoutClickEvent, callback,
                    self._CLICK_EVENT, *args)
        else:
            super(GridLayout, self).addCallback(callback, eventType, *args)


    def removeListener(self, listener, iface=None):
        if (isinstance(listener, ILayoutClickListener) and
                (iface is None or issubclass(iface, ILayoutClickListener))):
            self.withdrawListener(self._CLICK_EVENT, LayoutClickEvent,
                    listener)

        super(GridLayout, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, LayoutClickEvent):
            self.withdrawCallback(LayoutClickEvent, callback,
                    self._CLICK_EVENT)

        else:
            super(GridLayout, self).removeCallback(callback, eventType)


class Area(object):
    """This class defines an area on a grid. An Area is defined by the cells
    of its upper left corner (column1,row1) and lower right corner
    (column2, row2).

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, component, column1, row1, column2, row2):
        """Construct a new area on a grid.

        @param component:
                   the component connected to the area.
        @param column1:
                   The column of the upper left corner cell of the area
                   C{c} is supposed to occupy.
        @param row1:
                   The row of the upper left corner cell of the area
                   C{c} is supposed to occupy.
        @param column2:
                   The column of the lower right corner cell of the area
                   C{c} is supposed to occupy.
        @param row2:
                   The row of the lower right corner cell of the area
                   C{c} is supposed to occupy.
        @raise OverlapsException:
                    if the new component overlaps with any of the components
                    already in the grid
        """
        # The column of the upper left corner cell of the area.
        self._column1 = column1

        # The row of the upper left corner cell of the area.
        self._row1 = row1

        # The column of the lower right corner cell of the area.
        self._column2 = column2

        # The row of the lower right corner cell of the area.
        self._row2 = row2

        # Component painted on the area.
        self._component = component


    def overlaps(self, other):
        """Tests if the given Area overlaps with an another Area.

        @param other:
                   the Another Area that's to be tested for overlap with this
                   area.
        @return: C{True} if C{other} overlaps with this
                area, C{False} if it doesn't.
        """
        return (self._column1 <= other.getColumn2()
                and self._row1 <= other.getRow2()
                and self._column2 >= other.getColumn1()
                and self._row2 >= other.getRow1())


    def getComponent(self):
        """Gets the component connected to the area.

        @return: the Component.
        """
        return self._component


    def setComponent(self, newComponent):
        """Sets the component connected to the area.

        This function only sets the value in the datastructure and does not
        send any events or set parents.

        @param newComponent:
                   the new connected overriding the existing one.
        """
        self._component = newComponent


    def getX1(self):
        """@deprecated: Use getColumn1() instead.

        @see: L{GridLayout.getColumn1}
        """
        warn('Use getColumn1() instead.', DeprecationWarning)
        return self.getColumn1()


    def getColumn1(self):
        """Gets the column of the top-left corner cell.

        @return: the column of the top-left corner cell.
        """
        return self._column1


    def getX2(self):
        """@deprecated: Use getColumn2() instead.

        @see: L{GridLayout.getColumn2}
        """
        warn('Use getColumn2() instead.', DeprecationWarning)
        return self.getColumn2()


    def getColumn2(self):
        """Gets the column of the bottom-right corner cell.

        @return: the column of the bottom-right corner cell.
        """
        return self._column2


    def getY1(self):
        """@deprecated: Use getRow1() instead.

        @see: L{GridLayout.getRow1}
        """
        warn('Use getRow1() instead.', DeprecationWarning)
        return self.getRow1()


    def getRow1(self):
        """Gets the row of the top-left corner cell.

        @return: the row of the top-left corner cell.
        """
        return self._row1


    def getY2(self):
        """@deprecated: Use getRow2() instead.

        @see: L{GridLayout.getRow2}
        """
        warn('Use getRow2() instead.', DeprecationWarning)
        return self.getRow2()


    def getRow2(self):
        """Gets the row of the bottom-right corner cell.

        @return: the row of the bottom-right corner cell.
        """
        return self._row2


class OverlapsException(RuntimeError):
    """Gridlayout does not support laying components on top of each other.
    An C{OverlapsException} is thrown when a component already
    exists (even partly) at the same space on a grid with the new component.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, existingArea):
        """Constructs an C{OverlapsException}.
        """
        self._existingArea = existingArea


    def getMessage(self):
        sb = StringIO()
        component = self._existingArea.getComponent()
        sb.write(component)
        sb.write('( type = ')
        sb.write(fullname(component))
        if component.getCaption() is not None:
            sb.write(', caption = \"')
            sb.write(component.getCaption())
            sb.write('\"')
        sb.write(')')
        sb.write(' is already added to ')
        sb.write(self._existingArea.column1)
        sb.write(',')
        sb.write(self._existingArea.column1)
        sb.write(',')
        sb.write(self._existingArea.row1)
        sb.write(',')
        sb.write(self._existingArea.row2)
        sb.write('(column1, column2, row1, row2).')
        result = sb.getvalue()
        sb.close()
        return result


    def getArea(self):
        """Gets the area .

        @return: the existing area.
        """
        return self._existingArea


class OutOfBoundsException(RuntimeError):
    """An C{Exception} object which is thrown when an area
    exceeds the bounds of the grid.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, areaOutOfBounds):
        """Constructs an C{OoutOfBoundsException} with the
        specified detail message.
        """
        self._areaOutOfBounds = areaOutOfBounds


    def getArea(self):
        """Gets the area that is out of bounds.

        @return: the area out of Bound.
        """
        return self._areaOutOfBounds
