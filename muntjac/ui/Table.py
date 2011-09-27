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

import logging

from muntjac.event.dd.DropTarget import DropTarget
from muntjac.terminal.KeyMapper import KeyMapper
from muntjac.event.Action import Action
from muntjac.ui.DefaultFieldFactory import DefaultFieldFactory
from muntjac.event.dd.DragSource import DragSource
from muntjac.terminal.gwt.client.MouseEventDetails import MouseEventDetails
from muntjac.ui.Component import Component, Event as ComponentEvent
from muntjac.event.DataBoundTransferable import DataBoundTransferable
from muntjac.data.Property import ValueChangeNotifier
from muntjac.ui.Field import Field
from muntjac.ui.FieldFactory import FieldFactory
from muntjac.ui.Form import Form
from muntjac.ui.ComponentContainer import ComponentContainer
from muntjac.event.MouseEvents import ClickEvent

from muntjac.data.Container import \
    Container, Ordered, Sortable, Indexed,\
    ItemSetChangeNotifier, PropertySetChangeNotifier

from muntjac.event.dd.acceptcriteria.ServerSideCriterion import \
    ServerSideCriterion

from muntjac.ui.AbstractSelect import \
    AbstractSelect, MultiSelectMode, AbstractSelectTargetDetails

from muntjac.event.ItemClickEvent import \
    ItemClickEvent, ItemClickNotifier, ItemClickSource

from muntjac.data.util.ContainerOrderedWrapper import \
    ContainerOrderedWrapper

from muntjac.data.util.IndexedContainer import \
    ItemSetChangeEvent, IndexedContainer

from muntjac.terminal.gwt.client.ui.VScrollTable import VScrollTable


class TableDragMode(object):
    """Modes that Table support as drag sourse."""

    # Table does not start drag and drop events. HTM5 style events started
    # by browser may still happen.
    NONE = 'NONE'

    # Table starts drag with a one row only.
    ROW = 'ROW'

    # Table drags selected rows, if drag starts on a selected rows. Else it
    # starts like in ROW mode. Note, that in Transferable there will still
    # be only the row on which the drag started, other dragged rows need to
    # be checked from the source Table.
    MULTIROW = 'MULTIROW'

    _values = [NONE, ROW, MULTIROW]

    @classmethod
    def values(cls):
        return cls._values[:]


class Table(AbstractSelect, Action, Container, Container, Ordered, Container,
            Sortable, ItemClickSource, ItemClickNotifier, DragSource, DropTarget):
    """<p>
    <code>Table</code> is used for representing data or components in a pageable
    and selectable table.
    </p>

    <p>
    Scalability of the Table is largely dictated by the container. A table does
    not have a limit for the number of items and is just as fast with hundreds of
    thousands of items as with just a few. The current GWT implementation with
    scrolling however limits the number of rows to around 500000, depending on
    the browser and the pixel height of rows.
    </p>

    <p>
    Components in a Table will not have their caption nor icon rendered.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """

#    CLIENT_WIDGET = VScrollTable
#    LOAD_STYLE = LoadStyle.EAGER

    _logger = logging.getLogger(__class__.__name__)

    CELL_KEY = 0

    CELL_HEADER = 1

    CELL_ICON = 2

    CELL_ITEMID = 3

    CELL_FIRSTCOL = 4

    # Left column alignment. <b>This is the default behaviour. </b>
    ALIGN_LEFT = 'b'

    # Center column alignment.
    ALIGN_CENTER = 'c'

    # Right column alignment.
    ALIGN_RIGHT = 'e'

    # Column header mode: Column headers are hidden.
    COLUMN_HEADER_MODE_HIDDEN = -1

    # Column header mode: Property ID:s are used as column headers.
    COLUMN_HEADER_MODE_ID = 0

    # Column header mode: Column headers are explicitly specified with
    # {@link #setColumnHeaders(String[])}.
    COLUMN_HEADER_MODE_EXPLICIT = 1

    # Column header mode: Column headers are explicitly specified with
    # {@link #setColumnHeaders(String[])}. If a header is not specified for a
    # given property, its property id is used instead.
    # <p>
    # <b>This is the default behavior. </b>
    COLUMN_HEADER_MODE_EXPLICIT_DEFAULTS_ID = 2

    # Row caption mode: The row headers are hidden. <b>This is the default
    # mode. </b>
    ROW_HEADER_MODE_HIDDEN = -1

    # Row caption mode: Items Id-objects toString is used as row caption.
    ROW_HEADER_MODE_ID = AbstractSelect.ITEM_CAPTION_MODE_ID

    # Row caption mode: Item-objects toString is used as row caption.
    ROW_HEADER_MODE_ITEM = AbstractSelect.ITEM_CAPTION_MODE_ITEM

    # Row caption mode: Index of the item is used as item caption. The index
    # mode can only be used with the containers implementing Container.Indexed
    # interface.
    ROW_HEADER_MODE_INDEX = AbstractSelect.ITEM_CAPTION_MODE_INDEX

    # Row caption mode: Item captions are explicitly specified.
    ROW_HEADER_MODE_EXPLICIT = AbstractSelect.ITEM_CAPTION_MODE_EXPLICIT

    # Row caption mode: Item captions are read from property specified with
    # {@link #setItemCaptionPropertyId(Object)}.
    ROW_HEADER_MODE_PROPERTY = AbstractSelect.ITEM_CAPTION_MODE_PROPERTY

    # Row caption mode: Only icons are shown, the captions are hidden.
    ROW_HEADER_MODE_ICON_ONLY = AbstractSelect.ITEM_CAPTION_MODE_ICON_ONLY

    # Row caption mode: Item captions are explicitly specified, but if the
    # caption is missing, the item id objects <code>toString()</code> is used
    # instead.
    ROW_HEADER_MODE_EXPLICIT_DEFAULTS_ID = AbstractSelect.ITEM_CAPTION_MODE_EXPLICIT_DEFAULTS_ID

    # The default rate that table caches rows for smooth scrolling.
    _CACHE_RATE_DEFAULT = 2

    _ROW_HEADER_COLUMN_KEY = '0'

    _ROW_HEADER_FAKE_PROPERTY_ID = object()


    def __init__(self, caption=None, dataSource=None):
        """Creates a new empty table.
        ---
        Creates a new empty table with caption.

        @param caption
        ---
        Creates a new table with caption and connect it to a Container.

        @param caption
        @param dataSource
        """
        # True if column collapsing is allowed.
        self._columnCollapsingAllowed = False

        # True if reordering of columns is allowed on the client side.
        self._columnReorderingAllowed = False

        # Keymapper for column ids.
        self._columnIdMap = KeyMapper()

        # Holds visible column propertyIds - in order.
        self._visibleColumns = list()

        # Holds propertyIds of currently collapsed columns.
        self._collapsedColumns = set()

        # Holds headers for visible columns (by propertyId).
        self._columnHeaders = dict()

        # Holds footers for visible columns (by propertyId).
        self._columnFooters = dict()

        # Holds icons for visible columns (by propertyId).
        self._columnIcons = dict()

        # Holds alignments for visible columns (by propertyId).
        self._columnAlignments = dict()

        # Holds column widths in pixels (Integer) or expand ratios (Float) for
        # visible columns (by propertyId).
        self._columnWidths = dict()

        # Holds column generators
        self._columnGenerators = dict()

        # Holds value of property pageLength. 0 disables paging.
        self._pageLength = 15

        # Id the first item on the current page.
        self._currentPageFirstItemId = None

        # Index of the first item on the current page.
        self._currentPageFirstItemIndex = 0

        # Holds value of property selectable.
        self._selectable = False

        # Holds value of property columnHeaderMode.
        self._columnHeaderMode = self.COLUMN_HEADER_MODE_EXPLICIT_DEFAULTS_ID

        # Should the Table footer be visible?
        self._columnFootersVisible = False

        # True iff the row captions are hidden.
        self._rowCaptionsAreHidden = True

        # Page contents buffer used in buffered mode.
        self._pageBuffer = None

        # Set of properties listened - the list is kept to release the listeners
        # later.
        self._listenedProperties = None

        # Set of visible components - the is used for needsRepaint calculation.
        self._visibleComponents = None

        # List of action handlers.
        self._actionHandlers = None

        # Action mapper.
        self._actionMapper = None

        # Table cell editor factory.
        self._fieldFactory = DefaultFieldFactory.get()

        # Is table editable.
        self._editable = False

        # Current sorting direction.
        self._sortAscending = True

        # Currently table is sorted on this propertyId.
        self._sortContainerPropertyId = None

        # Is table sorting disabled alltogether; even if some of the properties
        # would be sortable.
        self._sortDisabled = False

        # Number of rows explicitly requested by the client to be painted on next
        # paint. This is -1 if no request by the client is made. Painting the
        # component will automatically reset this to -1.
        self._reqRowsToPaint = -1

        # Index of the first rows explicitly requested by the client to be painted.
        # This is -1 if no request by the client is made. Painting the component
        # will automatically reset this to -1.
        self._reqFirstRowToPaint = -1
        self._firstToBeRenderedInClient = -1
        self._lastToBeRenderedInClient = -1
        self._isContentRefreshesEnabled = True
        self._pageBufferFirstIndex = None
        self._containerChangeToBeRendered = False

        # Table cell specific style generator
        self._cellStyleGenerator = None

        # EXPERIMENTAL feature: will tell the client to re-calculate column widths
        # if set to true. Currently no setter: extend to enable.
        self.alwaysRecalculateColumnWidths = False
        self._cacheRate = self._CACHE_RATE_DEFAULT
        self._dragMode = TableDragMode.NONE
        self._dropHandler = None
        self._multiSelectMode = MultiSelectMode.DEFAULT
        self._associatedProperties = dict()

        self.setRowHeaderMode(self.ROW_HEADER_MODE_HIDDEN)

        if caption is not None:
            self.setCaption(caption)

        if dataSource is not None:
            self.setContainerDataSource(dataSource)

    # Table functionality

    def getVisibleColumns(self):
        """Gets the array of visible column id:s, including generated columns.

        <p>
        The columns are show in the order of their appearance in this array.
        </p>

        @return an array of currently visible propertyIds and generated column
                ids.
        """
        if self._visibleColumns is None:
            return None

        return list(self._visibleColumns)


    def setVisibleColumns(self, visibleColumns):
        """Sets the array of visible column property id:s.

        <p>
        The columns are show in the order of their appearance in this array.
        </p>

        @param visibleColumns
                   the Array of shown property id:s.
        """
        # Visible columns must exist
        if visibleColumns is None:
            raise ValueError, 'Can not set visible columns to null value'

        # TODO add error check that no duplicate identifiers exist

        # Checks that the new visible columns contains no nulls and properties
        # exist
        properties = self.getContainerPropertyIds()
        for i in range(len(properties)):
            if visibleColumns[i] is None:
                raise ValueError, 'Ids must be non-nulls'
            elif visibleColumns[i] not in properties \
                    and not (visibleColumns[i] in self._columnGenerators):
                raise ValueError, 'Ids must exist in the Container or as a generated column , missing id: ' \
                    + visibleColumns[i]

        # If this is called before the constructor is finished, it might be
        # uninitialized
        newVC = list()
        for i in range(len(visibleColumns)):
            newVC.append( visibleColumns[i] )

        # Removes alignments, icons and headers from hidden columns
        if self._visibleColumns is not None:
            disabledHere = self.disableContentRefreshing()
            try:
                for col in visibleColumns:
                    if col not in newVC:
                        self.setColumnHeader(col, None)
                        self.setColumnAlignment(col, None)
                        self.setColumnIcon(col, None)
            finally:
                if disabledHere:
                    self.enableContentRefreshing(False)

        self._visibleColumns = newVC

        # Assures visual refresh
        self.resetPageBuffer()
        self.refreshRenderedCells()


    def getColumnHeaders(self):
        """Gets the headers of the columns.

        <p>
        The headers match the property id:s given my the set visible column
        headers. The table must be set in either
        {@link #COLUMN_HEADER_MODE_EXPLICIT} or
        {@link #COLUMN_HEADER_MODE_EXPLICIT_DEFAULTS_ID} mode to show the
        headers. In the defaults mode any nulls in the headers array are replaced
        with id.toString().
        </p>

        @return the Array of column headers.
        """
        if self._columnHeaders is None:
            return None

        headers = [None] * len(self._visibleColumns)

        for i, col in enumerate(self._visibleColumns):
            headers[i] = self.getColumnHeader(col)

        return headers


    def setColumnHeaders(self, columnHeaders):
        """Sets the headers of the columns.

        <p>
        The headers match the property id:s given my the set visible column
        headers. The table must be set in either
        {@link #COLUMN_HEADER_MODE_EXPLICIT} or
        {@link #COLUMN_HEADER_MODE_EXPLICIT_DEFAULTS_ID} mode to show the
        headers. In the defaults mode any nulls in the headers array are replaced
        with id.toString() outputs when rendering.
        </p>

        @param columnHeaders
                   the Array of column headers that match the
                   {@link #getVisibleColumns()} method.
        """
        if len(columnHeaders) != len(self._visibleColumns):
            raise ValueError, 'The length of the headers array must match the number of visible columns'

        del self._columnHeaders[:]

        i = 0
        it = iter(self._visibleColumns)
        while i < len(columnHeaders):
            try:
                self._columnHeaders.put(it.next(), columnHeaders[i])
                i += 1
            except StopIteration:
                break

        # Assures the visual refresh
        # FIXME: Is this really needed? Header captions should not affect
        # content so requestRepaint() should be sufficient.
        self.resetPageBuffer()
        self.refreshRenderedCells()


    def getColumnIcons(self):
        """Gets the icons of the columns.

        <p>
        The icons in headers match the property id:s given my the set visible
        column headers. The table must be set in either
        {@link #COLUMN_HEADER_MODE_EXPLICIT} or
        {@link #COLUMN_HEADER_MODE_EXPLICIT_DEFAULTS_ID} mode to show the headers
        with icons.
        </p>

        @return the Array of icons that match the {@link #getVisibleColumns()}.
        """
        if self._columnIcons is None:
            return None

        icons = [None] * len(self._visibleColumns)
        for i, col in enumerate(self._visibleColumns):
            icons[i] = self._columnIcons[col]
        return icons


    def setColumnIcons(self, columnIcons):
        """Sets the icons of the columns.

        <p>
        The icons in headers match the property id:s given my the set visible
        column headers. The table must be set in either
        {@link #COLUMN_HEADER_MODE_EXPLICIT} or
        {@link #COLUMN_HEADER_MODE_EXPLICIT_DEFAULTS_ID} mode to show the headers
        with icons.
        </p>

        @param columnIcons
                   the Array of icons that match the {@link #getVisibleColumns()}
                   .
        """
        if len(columnIcons) != len(self._visibleColumns):
            raise ValueError, 'The length of the icons array must match the number of visible columns'

        del self._columnIcons[:]

        for i, col in enumerate(self._visibleColumns):
            self._columnIcons[col] = columnIcons[i]

        # Assure visual refresh
        self.resetPageBuffer()
        self.refreshRenderedCells()


    def getColumnAlignments(self):
        """Gets the array of column alignments.

        <p>
        The items in the array must match the properties identified by
        {@link #getVisibleColumns()}. The possible values for the alignments
        include:
        <ul>
        <li>{@link #ALIGN_LEFT}: Left alignment</li>
        <li>{@link #ALIGN_CENTER}: Centered</li>
        <li>{@link #ALIGN_RIGHT}: Right alignment</li>
        </ul>
        The alignments default to {@link #ALIGN_LEFT}: any null values are
        rendered as align lefts.
        </p>

        @return the Column alignments array.
        """
        if self._columnAlignments is None:
            return None

        alignments = [None] * len(self._visibleColumns)

        for i, col in enumerate(self._visibleColumns):
            alignments[i] = self.getColumnAlignment(col)

        return alignments


    def setColumnAlignments(self, columnAlignments):
        """Sets the column alignments.

        <p>
        The items in the array must match the properties identified by
        {@link #getVisibleColumns()}. The possible values for the alignments
        include:
        <ul>
        <li>{@link #ALIGN_LEFT}: Left alignment</li>
        <li>{@link #ALIGN_CENTER}: Centered</li>
        <li>{@link #ALIGN_RIGHT}: Right alignment</li>
        </ul>
        The alignments default to {@link #ALIGN_LEFT}
        </p>

        @param columnAlignments
                   the Column alignments array.
        """
        if len(columnAlignments) != len(self._visibleColumns):
            raise ValueError, 'The length of the alignments array must match the number of visible columns'

        # Checks all alignments
        for i in range(len(columnAlignments)):
            a = columnAlignments[i]
            if a is not None \
                    and not (a == self.ALIGN_LEFT) \
                    and not (a == self.ALIGN_CENTER) \
                    and not (a == self.ALIGN_RIGHT):
                raise ValueError, 'Column ' + i + ' aligment \'' + a + '\' is invalid'

        # Resets the alignments
        newCA = dict()
        i = 0
        it = iter(self._visibleColumns)
        while i < len(columnAlignments):
            try:
                newCA[it.next()] = columnAlignments[i]
                i += 1
            except StopIteration:
                break

        self._columnAlignments = newCA

        # Assures the visual refresh
        self.resetPageBuffer()
        self.refreshRenderedCells()


    def setColumnWidth(self, propertyId, width):
        """Sets columns width (in pixels). Theme may not necessary respect very
        small or very big values. Setting width to -1 (default) means that theme
        will make decision of width.

        <p>
        Column can either have a fixed width or expand ratio. The latter one set
        is used. See @link {@link #setColumnExpandRatio(Object, float)}.

        @param propertyId
                   colunmns property id
        @param width
                   width to be reserved for colunmns content
        @since 4.0.3
        """
        if propertyId is None:
            # Since propertyId is null, this is the row header. Use the magic
            # id to store the width of the row header.
            propertyId = self._ROW_HEADER_FAKE_PROPERTY_ID

        if width < 0:
            self._columnWidths.remove(propertyId)
        else:
            self._columnWidths[propertyId] = int(width)


    def setColumnExpandRatio(self, propertyId, expandRatio):
        """Sets the column expand ratio for given column.
        <p>
        Expand ratios can be defined to customize the way how excess space is
        divided among columns. Table can have excess space if it has its width
        defined and there is horizontally more space than columns consume
        naturally. Excess space is the space that is not used by columns with
        explicit width (see {@link #setColumnWidth(Object, int)}) or with natural
        width (no width nor expand ratio).

        <p>
        By default (without expand ratios) the excess space is divided
        proportionally to columns natural widths.

        <p>
        Only expand ratios of visible columns are used in final calculations.

        <p>
        Column can either have a fixed width or expand ratio. The latter one set
        is used.

        <p>
        A column with expand ratio is considered to be minimum width by default
        (if no excess space exists). The minimum width is defined by terminal
        implementation.

        <p>
        If terminal implementation supports re-sizable columns the column becomes
        fixed width column if users resizes the column.

        @param propertyId
                   columns property id
        @param expandRatio
                   the expandRatio used to divide excess space for this column
        """
        if expandRatio < 0:
            self._columnWidths.remove(propertyId)
        else:
            self._columnWidths[propertyId] = float(expandRatio)


    def getColumnExpandRatio(self, propertyId):
        width = self._columnWidths.get(propertyId)
        if (width is None) or (not isinstance(width, float)):
            return -1

        return float(width)


    def getColumnWidth(self, propertyId):
        """Gets the pixel width of column

        @param propertyId
        @return width of column or -1 when value not set
        """
        if propertyId is None:
            # Since propertyId is null, this is the row header. Use the magic
            # id to retrieve the width of the row header.
            propertyId = self._ROW_HEADER_FAKE_PROPERTY_ID

        width = self._columnWidths.get(propertyId)
        if (width is None) or (not isinstance(width, int)):
            return -1

        return int(width)


    def getPageLength(self):
        """Gets the page length.

        <p>
        Setting page length 0 disables paging.
        </p>

        @return the Length of one page.
        """
        return self._pageLength


    def setPageLength(self, pageLength):
        """Sets the page length.

        <p>
        Setting page length 0 disables paging. The page length defaults to 15.
        </p>

        <p>
        If Table has width set ({@link #setWidth(float, int)} ) the client side
        may update the page length automatically the correct value.
        </p>

        @param pageLength
                   the length of one page.
        """
        if pageLength >= 0 and self._pageLength != pageLength:
            self._pageLength = pageLength
            # Assures the visual refresh
            self.resetPageBuffer()
            self.refreshRenderedCells()


    def setCacheRate(self, cacheRate):
        """This method adjusts a possible caching mechanism of table implementation.

        <p>
        Table component may fetch and render some rows outside visible area. With
        complex tables (for example containing layouts and components), the
        client side may become unresponsive. Setting the value lower, UI will
        become more responsive. With higher values scrolling in client will hit
        server less frequently.

        <p>
        The amount of cached rows will be cacheRate multiplied with pageLength (
        {@link #setPageLength(int)} both below and above visible area..

        @param cacheRate
                   a value over 0 (fastest rendering time). Higher value will
                   cache more rows on server (smoother scrolling). Default value
                   is 2.
        """
        if cacheRate < 0:
            raise ValueError, 'cacheRate cannot be less than zero'

        if self._cacheRate != cacheRate:
            self._cacheRate = cacheRate
            self.requestRepaint()


    def getCacheRate(self):
        """@see #setCacheRate(double)

        @return the current cache rate value
        """
        return self._cacheRate


    def getCurrentPageFirstItemId(self):
        """Getter for property currentPageFirstItem.

        @return the Value of property currentPageFirstItem.
        """
        # Priorise index over id if indexes are supported
        if isinstance(self.items, Indexed):
            index = self.getCurrentPageFirstItemIndex()
            idd = None
            if index >= 0 and index < len(self):
                idd = self.getIdByIndex(index)

            if idd is not None and not (idd == self._currentPageFirstItemId):
                self._currentPageFirstItemId = idd

        # If there is no item id at all, use the first one
        if self._currentPageFirstItemId is None:
            self._currentPageFirstItemId = self.firstItemId()

        return self._currentPageFirstItemId


    def getIdByIndex(self, index):
        return self.items.getIdByIndex(index)


    def setCurrentPageFirstItemId(self, currentPageFirstItemId):
        """Setter for property currentPageFirstItemId.

        @param currentPageFirstItemId
                   the New value of property currentPageFirstItemId.
        """
        # Gets the corresponding index
        index = -1
        if isinstance(self.items, Indexed):
            index = self.indexOfId(currentPageFirstItemId)
        else:
            # If the table item container does not have index, we have to
            # calculates the index by hand
            idd = self.firstItemId()
            while idd is not None and not (idd == currentPageFirstItemId):
                index += 1
                idd = self.nextItemId(idd)
            if idd is None:
                index = -1

        # If the search for item index was successful
        if index >= 0:
            # The table is not capable of displaying an item in the container
            # as the first if there are not enough items following the selected
            # item so the whole table (pagelength) is filled.
            maxIndex = len(self) - self._pageLength
            if maxIndex < 0:
                maxIndex = 0

            if index > maxIndex:
                self.setCurrentPageFirstItemIndex(maxIndex)
                return

            self._currentPageFirstItemId = currentPageFirstItemId
            self._currentPageFirstItemIndex = index

        # Assures the visual refresh
        self.resetPageBuffer()
        self.refreshRenderedCells()


    def indexOfId(self, itemId):
        return self.items.indexOfId(itemId)


    def getColumnIcon(self, propertyId):
        """Gets the icon Resource for the specified column.

        @param propertyId
                   the propertyId indentifying the column.
        @return the icon for the specified column; null if the column has no icon
                set, or if the column is not visible.
        """
        return self._columnIcons.get(propertyId)


    def setColumnIcon(self, propertyId, icon):
        """Sets the icon Resource for the specified column.
        <p>
        Throws IllegalArgumentException if the specified column is not visible.
        </p>

        @param propertyId
                   the propertyId identifying the column.
        @param icon
                   the icon Resource to set.
        """
        if icon is None:
            del self._columnIcons[propertyId]
        else:
            self._columnIcons[propertyId] = icon

        # Assures the visual refresh
        self.resetPageBuffer()
        self.refreshRenderedCells()


    def getColumnHeader(self, propertyId):
        """Gets the header for the specified column.

        @param propertyId
                   the propertyId identifying the column.
        @return the header for the specified column if it has one.
        """
        if self.getColumnHeaderMode() == self.COLUMN_HEADER_MODE_HIDDEN:
            return None

        header = self._columnHeaders.get(propertyId)
        if (header is None and self.getColumnHeaderMode() == self.COLUMN_HEADER_MODE_EXPLICIT_DEFAULTS_ID) \
                or (self.getColumnHeaderMode() == self.COLUMN_HEADER_MODE_ID):
            header = str(propertyId)

        return header


    def setColumnHeader(self, propertyId, header):
        """Sets the column header for the specified column;

        @param propertyId
                   the propertyId identifying the column.
        @param header
                   the header to set.
        """
        if header is None:
            del self._columnHeaders[propertyId]
        else:
            self._columnHeaders.put(propertyId, header)

        # Assures the visual refresh
        # FIXME: Is this really needed? Header captions should not affect
        # content so requestRepaint() should be sufficient.
        self.refreshRenderedCells()


    def getColumnAlignment(self, propertyId):
        """Gets the specified column's alignment.

        @param propertyId
                   the propertyID identifying the column.
        @return the specified column's alignment if it as one; null otherwise.
        """
        a = self._columnAlignments.get(propertyId)
        return self.ALIGN_LEFT if a is None else a


    def setColumnAlignment(self, propertyId, alignment):
        """Sets the specified column's alignment.

        <p>
        Throws IllegalArgumentException if the alignment is not one of the
        following: {@link #ALIGN_LEFT}, {@link #ALIGN_CENTER} or
        {@link #ALIGN_RIGHT}
        </p>

        @param propertyId
                   the propertyID identifying the column.
        @param alignment
                   the desired alignment.
        """
        # Checks for valid alignments
        if alignment is not None \
                and not (alignment == self.ALIGN_LEFT) \
                and not (alignment == self.ALIGN_CENTER) \
                and not (alignment == self.ALIGN_RIGHT):
            raise ValueError, 'Column alignment \'' + alignment + '\' is not supported.'

        if alignment is None or alignment == self.ALIGN_LEFT:
            self._columnAlignments.remove(propertyId)
            return

        self._columnAlignments[propertyId] = alignment

        # Assures the visual refresh
        self.refreshRenderedCells()


    def isColumnCollapsed(self, propertyId):
        """Checks if the specified column is collapsed.

        @param propertyId
                   the propertyID identifying the column.
        @return true if the column is collapsed; false otherwise;
        """
        return self._collapsedColumns is not None and propertyId in self._collapsedColumns


    def setColumnCollapsed(self, propertyId, collapsed):
        """Sets whether the specified column is collapsed or not.


        @param propertyId
                   the propertyID identifying the column.
        @param collapsed
                   the desired collapsedness.
        @throws IllegalStateException
                    if column collapsing is not allowed
        """
        if not self.isColumnCollapsingAllowed():
            raise ValueError, 'Column collapsing not allowed!'

        if collapsed:
            self._collapsedColumns.add(propertyId)
        else:
            self._collapsedColumns.remove(propertyId)

        # Assures the visual refresh
        self.resetPageBuffer()
        self.refreshRenderedCells()


    def isColumnCollapsingAllowed(self):
        """Checks if column collapsing is allowed.

        @return true if columns can be collapsed; false otherwise.
        """
        return self._columnCollapsingAllowed


    def setColumnCollapsingAllowed(self, collapsingAllowed):
        """Sets whether column collapsing is allowed or not.

        @param collapsingAllowed
                   specifies whether column collapsing is allowed.
        """
        self._columnCollapsingAllowed = collapsingAllowed

        if not collapsingAllowed:
            self._collapsedColumns.clear()

        # Assures the visual refresh
        self.refreshRenderedCells()


    def isColumnReorderingAllowed(self):
        """Checks if column reordering is allowed.

        @return true if columns can be reordered; false otherwise.
        """
        return self._columnReorderingAllowed


    def setColumnReorderingAllowed(self, reorderingAllowed):
        """Sets whether column reordering is allowed or not.

        @param reorderingAllowed
                   specifies whether column reordering is allowed.
        """
        self._columnReorderingAllowed = reorderingAllowed

        # Assures the visual refresh
        self.refreshRenderedCells()


    def setColumnOrder(self, columnOrder):
        # Arranges visible columns according to given columnOrder. Silently ignores
        # colimnId:s that are not visible columns, and keeps the internal order of
        # visible columns left out of the ordering (trailing). Silently does
        # nothing if columnReordering is not allowed.
        if (columnOrder is None) or (not self.isColumnReorderingAllowed()):
            return

        newOrder = list()
        for i in range(len(columnOrder)):
            if columnOrder[i] is not None and columnOrder[i] in self._visibleColumns:
                self._visibleColumns.remove(columnOrder[i])
                newOrder.append(columnOrder[i])

        for columnId in self._visibleColumns:
            if columnId not in newOrder:
                newOrder.append(columnId)

        self._visibleColumns = newOrder

        # Assure visual refresh
        self.resetPageBuffer()
        self.refreshRenderedCells()


    def getCurrentPageFirstItemIndex(self):
        """Getter for property currentPageFirstItem.

        @return the Value of property currentPageFirstItem.
        """
        return self._currentPageFirstItemIndex


    def setCurrentPageFirstItemIndex(self, newIndex, needsPageBufferReset=True):
        """None
        ---
        Setter for property currentPageFirstItem.

        @param newIndex
                   the New value of property currentPageFirstItem.
        """
        if newIndex < 0:
            newIndex = 0

        # minimize Container.size() calls which may be expensive. For example
        # it may cause sql query.
        size = self.size()

        # The table is not capable of displaying an item in the container as
        # the first if there are not enough items following the selected item
        # so the whole table (pagelength) is filled.
        maxIndex = size - self._pageLength
        if maxIndex < 0:
            maxIndex = 0

        # Ensures that the new value is valid
        if newIndex > maxIndex:
            newIndex = maxIndex

        # Refresh first item id
        if isinstance(self.items, Indexed):
            try:
                self._currentPageFirstItemId = self.getIdByIndex(newIndex)
            except IndexError:
                self._currentPageFirstItemId = None

            self._currentPageFirstItemIndex = newIndex
        else:
            # For containers not supporting indexes, we must iterate the
            # container forwards / backwards
            # next available item forward or backward

            self._currentPageFirstItemId = self.firstItemId()

            # Go forwards in the middle of the list (respect borders)
            while self._currentPageFirstItemIndex < newIndex \
                    and not self.isLastId(self._currentPageFirstItemId):
                self._currentPageFirstItemIndex += 1
                self._currentPageFirstItemId = self.nextItemId(self._currentPageFirstItemId)

            # If we did hit the border
            if self.isLastId(self._currentPageFirstItemId):
                self._currentPageFirstItemIndex = size - 1

            # Go backwards in the middle of the list (respect borders)
            while self._currentPageFirstItemIndex > newIndex \
                    and not self.isFirstId(self._currentPageFirstItemId):
                self._currentPageFirstItemIndex -= 1
                self._currentPageFirstItemId = self.prevItemId(self._currentPageFirstItemId)

            # If we did hit the border
            if self.isFirstId(self._currentPageFirstItemId):
                self._currentPageFirstItemIndex = 0

            # Go forwards once more
            while self._currentPageFirstItemIndex < newIndex \
                    and not self.isLastId(self._currentPageFirstItemId):
                self._currentPageFirstItemIndex += 1
                self._currentPageFirstItemId = self.nextItemId(self._currentPageFirstItemId)

            # If for some reason we do hit border again, override
            # the user index request
            if self.isLastId(self._currentPageFirstItemId):
                newIndex = self._currentPageFirstItemIndex = size - 1

        if needsPageBufferReset:
            # Assures the visual refresh
            self.resetPageBuffer()
            self.refreshRenderedCells()


    def isPageBufferingEnabled(self):
        """Getter for property pageBuffering.

        @deprecated functionality is not needed in ajax rendering model

        @return the Value of property pageBuffering.
        """
        return True


    def setPageBufferingEnabled(self, pageBuffering):
        """Setter for property pageBuffering.

        @deprecated functionality is not needed in ajax rendering model

        @param pageBuffering
                   the New value of property pageBuffering.
        """
        raise DeprecationWarning, 'functionality is not needed in ajax rendering model'


    def isSelectable(self):
        """Getter for property selectable.

        <p>
        The table is not selectable by default.
        </p>

        @return the Value of property selectable.
        """
        return self._selectable


    def setSelectable(self, selectable):
        """Setter for property selectable.

        <p>
        The table is not selectable by default.
        </p>

        @param selectable
                   the New value of property selectable.
        """
        if self._selectable != selectable:
            self._selectable = selectable
            self.requestRepaint()


    def getColumnHeaderMode(self):
        """Getter for property columnHeaderMode.

        @return the Value of property columnHeaderMode.
        """
        return self._columnHeaderMode


    def setColumnHeaderMode(self, columnHeaderMode):
        """Setter for property columnHeaderMode.

        @param columnHeaderMode
                   the New value of property columnHeaderMode.
        """
        if columnHeaderMode >= self.COLUMN_HEADER_MODE_HIDDEN \
                and columnHeaderMode <= self.COLUMN_HEADER_MODE_EXPLICIT_DEFAULTS_ID:
            self._columnHeaderMode = columnHeaderMode

        # Assures the visual refresh
        self.refreshRenderedCells()


    def refreshRenderedCells(self):
        """Refreshes rendered rows"""
        if self.getParent() is None:
            return

        if self._isContentRefreshesEnabled:

            oldListenedProperties = self._listenedProperties
            oldVisibleComponents = self._visibleComponents

            # initialize the listener collections
            self._listenedProperties = set()
            self._visibleComponents = set()

            # Collects the basic facts about the table page
            colids = self.getVisibleColumns()
            cols = len(colids)
            pagelen = self.getPageLength()
            firstIndex = self.getCurrentPageFirstItemIndex()
            rows = totalRows = self.size()
            if rows > 0 and firstIndex >= 0:
                rows -= firstIndex

            if pagelen > 0 and pagelen < rows:
                rows = pagelen

            # If "to be painted next" variables are set, use them
            if self._lastToBeRenderedInClient - self._firstToBeRenderedInClient > 0:
                rows = (self._lastToBeRenderedInClient - self._firstToBeRenderedInClient) + 1

            if self._firstToBeRenderedInClient >= 0:
                if self._firstToBeRenderedInClient < totalRows:
                    firstIndex = self._firstToBeRenderedInClient
                else:
                    firstIndex = totalRows - 1
            else:
                # initial load
                self._firstToBeRenderedInClient = firstIndex

            if totalRows > 0:
                if rows + firstIndex > totalRows:
                    rows = totalRows - firstIndex
            else:
                rows = 0

            cells = [[None] * cols + self.CELL_FIRSTCOL] * rows
            if rows == 0:
                self._pageBuffer = cells
                self.unregisterPropertiesAndComponents(oldListenedProperties,
                                                       oldVisibleComponents)

                # We need to repaint so possible header or footer changes are
                # sent to the server
                self.requestRepaint()
                return

            # Gets the first item id
            if isinstance(self.items, Indexed):
                idd = self.getIdByIndex(firstIndex)
            else:
                idd = self.firstItemId()
                for i in range(firstIndex):
                    idd = self.nextItemId(idd)

            headmode = self.getRowHeaderMode()
            iscomponent = [None] * cols
            for i in range(cols):
                iscomponent[i] = (colids[i] in self._columnGenerators) \
                        or issubclass(self.getType(colids[i]), Component)

            if self._pageBuffer is not None \
                    and self._pageBuffer[self.CELL_ITEMID].length > 0:  # FIXME: check indexing
                firstIndexNotInCache = self._pageBufferFirstIndex \
                        + self._pageBuffer[self.CELL_ITEMID].length  # FIXME: check indexing
            else:
                firstIndexNotInCache = -1

            # Creates the page contents
            filledRows = 0
            i = 0
            while i < rows and idd is not None:
                cells[self.CELL_ITEMID][i] = idd
                cells[self.CELL_KEY][i] = self.itemIdMapper.key(idd)
                if headmode != self.ROW_HEADER_MODE_HIDDEN:
                    if headmode == self.ROW_HEADER_MODE_INDEX:
                        cells[self.CELL_HEADER][i] = str(i + firstIndex + 1)
                    else:
                        cells[self.CELL_HEADER][i] = self.getItemCaption(idd)

                    cells[self.CELL_ICON][i] = self.getItemIcon(idd)

                if cols > 0:
                    for j in cols:
                        if self.isColumnCollapsed(colids[j]):
                            continue

                        p = None
                        value = ''
                        isGenerated = colids[j] in self._columnGenerators

                        if not isGenerated:
                            p = self.getContainerProperty(idd, colids[j])

                        # check in current pageBuffer already has row
                        index = firstIndex + i
                        if (p is not None) or isGenerated:
                            if index < firstIndexNotInCache \
                                    and index >= self._pageBufferFirstIndex:
                                # we have data already in our cache,
                                # recycle it instead of fetching it via
                                # getValue/getPropertyValue
                                indexInOldBuffer = index - self._pageBufferFirstIndex
                                value = self._pageBuffer[self.CELL_FIRSTCOL + j][indexInOldBuffer]
                                if (not isGenerated and iscomponent[j]) \
                                        or (not isinstance(value, Component)):
                                    self.listenProperty(p, oldListenedProperties)

                            elif isGenerated:
                                cg = self._columnGenerators[colids[j]]
                                value = cg.generateCell(self, idd, colids[j])

                            elif iscomponent[j]:
                                value = p.getValue()
                                self.listenProperty(p, oldListenedProperties)

                            elif p is not None:
                                value = self.getPropertyValue(idd, colids[j], p)
                                # If returned value is Component (via
                                # fieldfactory or overridden
                                # getPropertyValue) we excpect it to listen
                                # property value changes. Otherwise if
                                # property emits value change events, table
                                # will start to listen them and refresh
                                # content when needed.
                                if not isinstance(value, Component):
                                    self.listenProperty(p, oldListenedProperties)

                            else:
                                value = self.getPropertyValue(idd, colids[j], None)

                        if isinstance(value, Component):
                            if (oldVisibleComponents is None) \
                                    or (not (value in oldVisibleComponents)):
                                value.setParent(self)

                            self._visibleComponents.add(value)

                        cells[self.CELL_FIRSTCOL + j][i] = value

                # Gets the next item idd
                if isinstance(self.items, Indexed):
                    index = firstIndex + i + 1
                    if index < totalRows:
                        idd = self.getIdByIndex(index)
                    else:
                        idd = None
                else:
                    idd = self.nextItemId(idd)

                filledRows += 1

            # Assures that all the rows of the cell-buffer are valid
            if filledRows != cells[0].length:
                temp = [[None] * len(cells)] * filledRows
                for i in range(len(cells)):
                    for j in range(filledRows):
                        temp[i][j] = cells[i][j]

                cells = temp

            self._pageBufferFirstIndex = firstIndex

            # Saves the results to internal buffer
            self._pageBuffer = cells

            self.unregisterPropertiesAndComponents(oldListenedProperties,
                                                   oldVisibleComponents)

            self.requestRepaint()


    def listenProperty(self, p, oldListenedProperties):
        if isinstance(p, ValueChangeNotifier):
            if (oldListenedProperties is None) or (not (p in oldListenedProperties)):
                p.addListener(self)

            # register listened properties, so we can do proper cleanup to free
            # memory. Essential if table has loads of data and it is used for a
            # long time.
            self._listenedProperties.add(p)


    def unregisterPropertiesAndComponents(self, oldListenedProperties,
                                          oldVisibleComponents):
        """Helper method to remove listeners and maintain correct component
        hierarchy. Detaches properties and components if those are no more
        rendered in client.

        @param oldListenedProperties
                   set of properties that where listened in last render
        @param oldVisibleComponents
                   set of components that where attached in last render
        """
        if oldVisibleComponents is not None:
            for c in oldVisibleComponents:
                if not (c in self._visibleComponents):
                    self.unregisterComponent(c)

        if oldListenedProperties is not None:
            for o in oldListenedProperties:
                if not (o in self._listenedProperties):
                    o.removeListener(self)


    def unregisterComponent(self, component):
        """This method cleans up a Component that has been generated when Table is
        in editable mode. The component needs to be detached from its parent and
        if it is a field, it needs to be detached from its property data source
        in order to allow garbage collection to take care of removing the unused
        component from memory.

        Override this method and getPropertyValue(Object, Object, Property) with
        custom logic if you need to deal with buffered fields.

        @see #getPropertyValue(Object, Object, Property)

        @param oldVisibleComponents
                   a set of components that should be unregistered.
        """
        component.setParent(None)
        # Also remove property data sources to unregister listeners keeping the
        # fields in memory.
        if isinstance(component, Field):
            field = component
            associatedProperty = self._associatedProperties.pop(component, None)
            if associatedProperty is not None \
                    and field.getPropertyDataSource() == associatedProperty:
                # Remove the property data source only if it's the one we
                # added in getPropertyValue
                field.setPropertyDataSource(None)


    def refreshCurrentPage(self):
        """Refreshes the current page contents.

        @deprecated should not need to be used
        """
        raise DeprecationWarning, 'should not need to be used'


    def setRowHeaderMode(self, mode):
        """Sets the row header mode.
        <p>
        The mode can be one of the following ones:
        <ul>
        <li>{@link #ROW_HEADER_MODE_HIDDEN}: The row captions are hidden.</li>
        <li>{@link #ROW_HEADER_MODE_ID}: Items Id-objects <code>toString()</code>
        is used as row caption.
        <li>{@link #ROW_HEADER_MODE_ITEM}: Item-objects <code>toString()</code>
        is used as row caption.
        <li>{@link #ROW_HEADER_MODE_PROPERTY}: Property set with
        {@link #setItemCaptionPropertyId(Object)} is used as row header.
        <li>{@link #ROW_HEADER_MODE_EXPLICIT_DEFAULTS_ID}: Items Id-objects
        <code>toString()</code> is used as row header. If caption is explicitly
        specified, it overrides the id-caption.
        <li>{@link #ROW_HEADER_MODE_EXPLICIT}: The row headers must be explicitly
        specified.</li>
        <li>{@link #ROW_HEADER_MODE_INDEX}: The index of the item is used as row
        caption. The index mode can only be used with the containers implementing
        <code>Container.Indexed</code> interface.</li>
        </ul>
        The default value is {@link #ROW_HEADER_MODE_HIDDEN}
        </p>

        @param mode
                   the One of the modes listed above.
        """
        if self.ROW_HEADER_MODE_HIDDEN == mode:
            self._rowCaptionsAreHidden = True
        else:
            self._rowCaptionsAreHidden = False
            self.setItemCaptionMode(mode)

        # Assure visual refresh
        self.refreshRenderedCells()


    def getRowHeaderMode(self):
        """Gets the row header mode.

        @return the Row header mode.
        @see #setRowHeaderMode(int)
        """
        return self.ROW_HEADER_MODE_HIDDEN if self._rowCaptionsAreHidden else self.getItemCaptionMode()


    def addItem(self, cells, itemId):
        """Adds the new row to table and fill the visible cells (except generated
        columns) with given values.

        @param cells
                   the Object array that is used for filling the visible cells
                   new row. The types must be settable to visible column property
                   types.
        @param itemId
                   the Id the new row. If null, a new id is automatically
                   assigned. If given, the table cant already have a item with
                   given id.
        @return Returns item id for the new row. Returns null if operation fails.
        """
        # remove generated columns from the list of columns being assigned
        availableCols = list()
        for idd in self._visibleColumns:
            if not (idd in self._columnGenerators):
                availableCols.add(idd)

        # Checks that a correct number of cells are given
        if len(cells) != len(availableCols):
            return None

        # Creates new item
        if itemId is None:
            itemId = self.items.addItem()
            if itemId is None:
                return None
            item = self.items.getItem(itemId)
        else:
            item = self.items.addItem(itemId)

        if item is None:
            return None

        # Fills the item properties
        for i in range(len(availableCols)):
            item.getItemProperty(availableCols[i]).setValue(cells[i])

        if not isinstance(self.items, ItemSetChangeNotifier):
            self.resetPageBuffer()
            self.refreshRenderedCells()

        return itemId

        # Overriding select behavior

    def setValue(self, newValue):
        # external selection change, need to truncate pageBuffer
        self.resetPageBuffer()
        self.refreshRenderedCells()
        super(Table, self).setValue(newValue)


    def setContainerDataSource(self, newDataSource):

        self.disableContentRefreshing()

        if newDataSource is None:
            newDataSource = IndexedContainer()

        # Assures that the data source is ordered by making unordered
        # containers ordered by wrapping them
        if isinstance(newDataSource, Ordered):
            super(Table, self).setContainerDataSource(newDataSource)
        else:
            super(Table, self).setContainerDataSource( ContainerOrderedWrapper(newDataSource) )

        # Resets page position
        self._currentPageFirstItemId = None
        self._currentPageFirstItemIndex = 0

        # Resets column properties
        if self._collapsedColumns is not None:
            self._collapsedColumns.clear()

        # columnGenerators 'override' properties, don't add the same id twice
        col = list()
        for idd in self.getContainerPropertyIds():
            if (self._columnGenerators is None) or (not (idd in self._columnGenerators)):
                col.add(idd)

        # generators added last
        if self._columnGenerators is not None and len(self._columnGenerators) > 0:
            col.extend(self._columnGenerators.keys())

        self.setVisibleColumns(col)

        # Assure visual refresh
        self.resetPageBuffer()

        self.enableContentRefreshing(True)


    def getItemIdsInRange(self, itemId, length):
        """Gets items ids from a range of key values

        @param startRowKey
                   The start key
        @param endRowKey
                   The end key
        @return
        """
        ids = set()
        for _ in range(length):
            # should not be null unless client-server
            # are out of sync
            assert itemId is not None
            ids.add(itemId)
            itemId = self.nextItemId(itemId)
        return ids


    def handleSelectedItems(self, variables):
        """Handles selection if selection is a multiselection

        @param variables
                   The variables
        """
        ka = variables.get('selected')
        ranges = variables.get('selectedRanges')

        renderedItemIds = self.getCurrentlyRenderedItemIds()

        newValue = set(self.getValue())

        if 'clearSelections' in variables:
            # the client side has instructed to swipe all previous selections
            newValue.clear()
        else:
            # first clear all selections that are currently rendered rows (the
            # ones that the client side counterpart is aware of)
            newValue.removeAll(renderedItemIds)

        # Then add (possibly some of them back) rows that are currently
        # selected on the client side (the ones that the client side is aware
        # of).
        for i in range(len(ka)):
            # key to id
            idd = self.itemIdMapper.get( ka[i] )
            if not self.isNullSelectionAllowed() \
                    and (idd is None) \
                    or (idd == self.getNullSelectionItemId()):
                # skip empty selection if nullselection is not allowed
                self.requestRepaint()
            elif idd is not None and self.containsId(idd):
                newValue.add(idd)

        # Add range items aka shift clicked multiselection areas
        if ranges is not None:
            for rnge in ranges:
                split = rnge.split('-')
                startItemId = self.itemIdMapper.get(split[0])
                length = int( split[1] )
                newValue.update( self.getItemIdsInRange(startItemId, length) )

        if not self.isNullSelectionAllowed() and len(newValue) == 0:
            # empty selection not allowed, keep old value
            self.requestRepaint()
            return

        self.setValue(newValue, True)


    def getCurrentlyRenderedItemIds(self):
        ids = set()
        if self._pageBuffer is not None:
            for i in range(len( self._pageBuffer[self.CELL_ITEMID] )):
                ids.add( self._pageBuffer[self.CELL_ITEMID][i] )
        return ids


    # Component basics


    def changeVariables(self, source, variables):
        """Invoked when the value of a variable has changed.

        @see com.vaadin.ui.Select#changeVariables(java.lang.Object,
             java.util.Map)
        """
        clientNeedsContentRefresh = False

        self.handleClickEvent(variables)

        self.handleColumnResizeEvent(variables)

        self.handleColumnWidthUpdates(variables)

        self.disableContentRefreshing()

        if not self.isSelectable() and 'selected' in variables:
            # Not-selectable is a special case, AbstractSelect does not support
            # TODO could be optimized.
            variables = dict(variables)
            del variables['selected']

        # The AbstractSelect cannot handle the multiselection properly, instead
        # we handle it ourself
        elif self.isSelectable() \
                and self.isMultiSelect() \
                and 'selected' in variables \
                and self._multiSelectMode == self.MultiSelectMode.DEFAULT:
            self.handleSelectedItems(variables)
            variables = dict(variables)
            del variables['selected']

        super(Table, self).changeVariables(source, variables)

        # Client might update the pagelength if Table height is fixed
        if 'pagelength' in variables:
            # Sets pageLength directly to avoid repaint that setter causes
            self._pageLength = variables.get('pagelength')

        # Page start index
        if 'firstvisible' in variables:
            value = variables.get('firstvisible')
            if value is not None:
                self.setCurrentPageFirstItemIndex(int(value), False)

        # Sets requested firstrow and rows for the next paint
        if 'reqfirstrow' in variables or 'reqrows' in variables:

            try:
                self._firstToBeRenderedInClient = int(variables.get('firstToBeRendered'))
                self._lastToBeRenderedInClient = int(variables.get('lastToBeRendered'))
            except Exception:
                # FIXME: Handle exception
                self._logger.info('Could not parse the first and/or last rows.')

            # respect suggested rows only if table is not otherwise updated
            # (row caches emptied by other event)
            if not self._containerChangeToBeRendered:
                value = variables.get('reqfirstrow')
                if value is not None:
                    self._reqFirstRowToPaint = int(value)
                value = variables.get('reqrows')
                if value is not None:
                    self._reqRowsToPaint = int(value)
                    # sanity check
                    if self._reqFirstRowToPaint + self._reqRowsToPaint > self.size():
                        self._reqRowsToPaint = self.size() - self._reqFirstRowToPaint

            clientNeedsContentRefresh = True

        if not self._sortDisabled:
            # Sorting
            doSort = False
            if 'sortcolumn' in variables:
                colId = variables.get('sortcolumn')
                if colId is not None \
                        and not ('' == colId) \
                        and not ('null' == colId):
                    idd = self._columnIdMap.get(colId)
                    self.setSortContainerPropertyId(idd, False)
                    doSort = True

            if 'sortascending' in variables:
                state = bool(variables.get('sortascending'))
                if state != self._sortAscending:
                    self.setSortAscending(state, False)
                    doSort = True

            if doSort:
                self.sort()
                self.resetPageBuffer()

        # Dynamic column hide/show and order
        # Update visible columns
        if self.isColumnCollapsingAllowed():
            if 'collapsedcolumns' in variables:
                try:
                    ids = variables.get('collapsedcolumns')
                    for col in self._visibleColumns:
                        self.setColumnCollapsed(col, False)

                    for i in range(len(ids)):
                        self.setColumnCollapsed(self._columnIdMap.get( str(ids[i]) ), True)
                except Exception:
                    # FIXME: Handle exception
                    self._logger.info('Could not determine column collapsing state')

                clientNeedsContentRefresh = True

        if self.isColumnReorderingAllowed():
            if 'columnorder' in variables:
                try:
                    ids = variables['columnorder']
                    # need a real Object[], ids can be a String[]
                    idsTemp = [None] * len(ids)
                    for i in range(len(ids)):
                        idsTemp[i] = self._columnIdMap.get( str(ids[i]) )

                    self.setColumnOrder(idsTemp)
                    if self.hasListeners( ColumnReorderEvent ):
                        self.fireEvent( ColumnReorderEvent(self) )
                except Exception:
                    # FIXME: Handle exception
                    self._logger.info('Could not determine column reordering state')

                clientNeedsContentRefresh = True

        self.enableContentRefreshing(clientNeedsContentRefresh)

        # Actions
        if 'action' in variables:
            st = variables.get('action').split(',')  # FIXME: implement StringTokenizer
            if len(st) == 2:
                itemId = self.itemIdMapper.get(st[0].strip())
                action = self._actionMapper.get(st[1].strip())
                if action is not None \
                        and (itemId is None) \
                        or self.containsId(itemId) \
                        and self._actionHandlers is not None:
                    for ah in self._actionHandlers:
                        ah.handleAction(action, self, itemId)


    def handleClickEvent(self, variables):
        """Handles click event

        @param variables
        """
        # Item click event
        if 'clickEvent' in variables:
            key = variables.get('clickedKey')
            itemId = self.itemIdMapper.get(key)
            propertyId = None
            colkey = variables.get('clickedColKey')
            # click is not necessary on a property
            if colkey is not None:
                propertyId = self._columnIdMap.get(colkey)

            evt = MouseEventDetails.deSerialize(variables.get('clickEvent'))
            item = self.getItem(itemId)
            if item is not None:
                self.fireEvent( ItemClickEvent(self, item, itemId, propertyId, evt) )

        # Header click event
        elif 'headerClickEvent' in variables:
            details = MouseEventDetails.deSerialize(variables.get('headerClickEvent'))
            cid = variables.get('headerClickCID')
            propertyId = None
            if cid is not None:
                propertyId = self._columnIdMap.get(str(cid))
            self.fireEvent( HeaderClickEvent(self, propertyId, details) )

        # Footer click event
        elif 'footerClickEvent' in variables:
            details = MouseEventDetails.deSerialize(variables.get('footerClickEvent'))
            cid = variables.get('footerClickCID')
            propertyId = None
            if cid is not None:
                propertyId = self._columnIdMap.get(str(cid))
            self.fireEvent( FooterClickEvent(self, propertyId, details) )


    def handleColumnResizeEvent(self, variables):
        """Handles the column resize event sent by the client.

        @param variables
        """
        if 'columnResizeEventColumn' in variables:
            cid = variables.get('columnResizeEventColumn')
            propertyId = None
            if cid is not None:
                propertyId = self._columnIdMap.get( str(cid) )

                prev = variables.get('columnResizeEventPrev')
                previousWidth = -1
                if prev is not None:
                    previousWidth = int( str(prev) )

                curr = variables.get('columnResizeEventCurr')
                currentWidth = -1
                if curr is not None:
                    currentWidth = int( str(curr) )

                self.fireColumnResizeEvent(propertyId,
                                           previousWidth,
                                           currentWidth)


    def fireColumnResizeEvent(self, propertyId, previousWidth, currentWidth):
        # Update the sizes on the server side. If a column previously had a
        # expand ratio and the user resized the column then the expand ratio
        # will be turned into a static pixel size.
        self.setColumnWidth(propertyId, currentWidth)

        self.fireEvent( ColumnResizeEvent(self,
                                          propertyId,
                                          previousWidth,
                                          currentWidth) )


    def handleColumnWidthUpdates(self, variables):
        if 'columnWidthUpdates' in variables:
            events = variables.get('columnWidthUpdates')
            for string in events:
                eventDetails = string.split(':')
                propertyId = self._columnIdMap.get( eventDetails[0] )
                if propertyId is None:
                    propertyId = self._ROW_HEADER_FAKE_PROPERTY_ID

                width = int( eventDetails[1] )
                self.setColumnWidth(propertyId, width)


    def disableContentRefreshing(self):
        """Go to mode where content updates are not done. This is due we want to
        bypass expensive content for some reason (like when we know we may have
        other content changes on their way).

        @return true if content refresh flag was enabled prior this call
        """
        wasDisabled = self._isContentRefreshesEnabled
        self._isContentRefreshesEnabled = False
        return wasDisabled


    def enableContentRefreshing(self, refreshContent):
        """Go to mode where content content refreshing has effect.

        @param refreshContent
                   true if content refresh needs to be done
        """
        self._isContentRefreshesEnabled = True
        if refreshContent:
            self.refreshRenderedCells()
            # Ensure that client gets a response
            self.requestRepaint()


    def paintContent(self, target):

        # The tab ordering number
        if self.getTabIndex() > 0:
            target.addAttribute('tabindex', self.getTabIndex())

        if self._dragMode != self.TableDragMode.NONE:
            target.addAttribute('dragmode', TableDragMode.values().index(self._dragMode))  # ordinal()

        if self._multiSelectMode != self.MultiSelectMode.DEFAULT:
            target.addAttribute('multiselectmode', MultiSelectMode.values().index(self._multiSelectMode))  # ordinal()

        # Initialize temps
        colids = self.getVisibleColumns()
        cols = len(colids)
        first = self.getCurrentPageFirstItemIndex()
        total = self.size()
        pagelen = self.getPageLength()
        colHeadMode = self.getColumnHeaderMode()
        colheads = colHeadMode != self.COLUMN_HEADER_MODE_HIDDEN
        cells = self.getVisibleCells()
        iseditable = self.isEditable()

        if self._reqRowsToPaint >= 0:
            rows = self._reqRowsToPaint
        else:
            rows = cells[0].length  # FIXME: check indexing

            if self.alwaysRecalculateColumnWidths:
                # TODO experimental feature for now: tell the client to
                # recalculate column widths.
                # We'll only do this for paints that do not originate from
                # table scroll/cache requests (i.e when reqRowsToPaint<0)
                target.addAttribute('recalcWidths', True)

        if not self.isNullSelectionAllowed() \
                and self.getNullSelectionItemId() is not None \
                and self.containsId(self.getNullSelectionItemId()):
            total -= 1
            rows -= 1

        # selection support
        selectedKeys = list()
        if self.isMultiSelect():
            sel = set( self.getValue() )
            vids = self.getVisibleItemIds()
            for idd in vids:
                if idd in sel:
                    selectedKeys.append( self.itemIdMapper.key(idd) )

        else:
            value = self.getValue()
            if value is None:
                value = self.getNullSelectionItemId()
            if value is not None:
                selectedKeys.append( self.itemIdMapper.key(value) )

        # Table attributes
        if self.isSelectable():
            target.addAttribute('selectmode', 'multi' if self.isMultiSelect() else 'single')
        else:
            target.addAttribute('selectmode', 'none')

        if self._cacheRate != self._CACHE_RATE_DEFAULT:
            target.addAttribute('cr', self._cacheRate)

        target.addAttribute('cols', cols)
        target.addAttribute('rows', rows)

        if not self.isNullSelectionAllowed():
            target.addAttribute('nsa', False)

        target.addAttribute('firstrow', self._reqFirstRowToPaint if self._reqFirstRowToPaint >= 0 else self._firstToBeRenderedInClient)
        target.addAttribute('totalrows', total)

        if pagelen != 0:
            target.addAttribute('pagelength', pagelen)

        if colheads:
            target.addAttribute('colheaders', True)

        if self.rowHeadersAreEnabled():
            target.addAttribute('rowheaders', True)

        target.addAttribute('colfooters', self._columnFootersVisible)

        # Body actions - Actions which has the target null and can be invoked
        # by right clicking on the table body.
        actionSet = set()
        if self._actionHandlers is not None:
            keys = list()
            for ah in self._actionHandlers:
                # Getting actions for the null item, which in this case means
                # the body item
                aa = ah.getActions(None, self)
                if aa is not None:
                    for ai in range(len(aa)):
                        key = self._actionMapper.key(aa[ai])
                        actionSet.add( aa[ai] )
                        keys.append(key)

            target.addAttribute('alb', keys)

        # Visible column order
        sortables = self.getSortableContainerPropertyIds()
        visibleColOrder = list()
        for columnId in self._visibleColumns:
            if not self.isColumnCollapsed(columnId):
                visibleColOrder.append( self._columnIdMap.key(columnId) )

        target.addAttribute('vcolorder', list(visibleColOrder))

        # Rows
        selectable = self.isSelectable()
        iscomponent = [None] * len(self._visibleColumns)
        iscomponentIndex = 0
        it = iter( self._visibleColumns )
        while iscomponentIndex < len(iscomponent):
            try:
                columnId = it.next()
                if columnId in self._columnGenerators:
                    iscomponent[iscomponentIndex] = True
                else:
                    colType = self.getType(columnId)
                    iscomponent[iscomponentIndex] = colType is not None and issubclass(colType, Component)
                iscomponentIndex += 1
            except StopIteration:
                break
        target.startTag('rows')

        # cells array contains all that are supposed to be visible on client,
        # but we'll start from the one requested by client
        start = 0
        if self._reqFirstRowToPaint != -1 and self._firstToBeRenderedInClient != -1:
            start = self._reqFirstRowToPaint - self._firstToBeRenderedInClient

        end = len(cells[0])  # FIXME: check indexing
        if self._reqRowsToPaint != -1:
            end = start + self._reqRowsToPaint

        # sanity check
        if self._lastToBeRenderedInClient != -1 \
                and self._lastToBeRenderedInClient < end:
            end = self._lastToBeRenderedInClient + 1

        if start > len(cells[self.CELL_ITEMID]) or start < 0:
            start = 0

        for indexInRowbuffer in range(start, end):
            itemId = cells[self.CELL_ITEMID][indexInRowbuffer]
            if not self.isNullSelectionAllowed() \
                    and self.getNullSelectionItemId() is not None \
                    and itemId == self.getNullSelectionItemId():
                # Remove null selection item if null selection is not allowed
                continue

            self.paintRow(target, cells, iseditable, actionSet,
                          iscomponent, indexInRowbuffer, itemId)
        target.endTag('rows')

        # The select variable is only enabled if selectable
        if selectable:
            target.addVariable(self, 'selected', selectedKeys)

        # The cursors are only shown on pageable table
        if (first != 0) or (self.getPageLength() > 0):
            target.addVariable(self, 'firstvisible', first)

        # Sorting
        if isinstance(self.getContainerDataSource(), Sortable):
            target.addVariable(self, 'sortcolumn',
                    self._columnIdMap.key(self._sortContainerPropertyId))
            target.addVariable(self, 'sortascending', self._sortAscending)

        # Resets and paints "to be painted next" variables. Also reset
        # pageBuffer
        self._reqFirstRowToPaint = -1
        self._reqRowsToPaint = -1
        self._containerChangeToBeRendered = False
        target.addVariable(self, 'reqrows', self._reqRowsToPaint)
        target.addVariable(self, 'reqfirstrow', self._reqFirstRowToPaint)

        # Actions
        if len(actionSet) > 0:
            target.addVariable(self, 'action', '')
            target.startTag('actions')
            for a in actionSet:
                target.startTag('action')

                if a.getCaption() is not None:
                    target.addAttribute('caption', a.getCaption())

                if a.getIcon() is not None:
                    target.addAttribute('icon', a.getIcon())

                target.addAttribute('key', self._actionMapper.key(a))
                target.endTag('action')

            target.endTag('actions')

        if self._columnReorderingAllowed:
            colorder = [None] * len(self._visibleColumns)
            i = 0
            it = iter(self._visibleColumns)
            while i < len(colorder):
                try:
                    colorder[i] = self._columnIdMap.key(it.next())
                    i += 1
                except StopIteration:
                    break
            target.addVariable(self, 'columnorder', colorder)

        # Available columns
        if self._columnCollapsingAllowed:
            ccs = set()
            for o in self._visibleColumns:
                if self.isColumnCollapsed(o):
                    ccs.add(o)
            collapsedkeys = [None] * len(ccs)
            nextColumn = 0
            it = iter( self._visibleColumns )
            while nextColumn < len(collapsedkeys):
                columnId = it.next()
                if self.isColumnCollapsed(columnId):
                    collapsedkeys[nextColumn] = self._columnIdMap.key(columnId)
                    nextColumn += 1
            target.addVariable(self, 'collapsedcolumns', collapsedkeys)

        target.startTag('visiblecolumns')
        if self.rowHeadersAreEnabled():
            target.startTag('column')
            target.addAttribute('cid', self._ROW_HEADER_COLUMN_KEY)
            self.paintColumnWidth(target, self._ROW_HEADER_FAKE_PROPERTY_ID)
            target.endTag('column')

        i = 0
        for columnId in self._visibleColumns:
            if columnId is not None:
                target.startTag('column')
                target.addAttribute('cid', self._columnIdMap.key(columnId))
                head = self.getColumnHeader(columnId)
                target.addAttribute('caption', head if head is not None else '')
                foot = self.getColumnFooter(columnId)
                target.addAttribute('fcaption', foot if foot is not None else '')
                if self.isColumnCollapsed(columnId):
                    target.addAttribute('collapsed', True)

                if colheads:
                    if self.getColumnIcon(columnId) is not None:
                        target.addAttribute('icon', self.getColumnIcon(columnId))

                    if sortables.contains(columnId):
                        target.addAttribute('sortable', True)

                if not (self.ALIGN_LEFT == self.getColumnAlignment(columnId)):
                    target.addAttribute('align', self.getColumnAlignment(columnId))

                self.paintColumnWidth(target, columnId)
                target.endTag('column')

        target.endTag('visiblecolumns')

        if self._dropHandler is not None:
            self._dropHandler.getAcceptCriterion().paint(target)


    def paintColumnWidth(self, target, columnId):
        if columnId in self._columnWidths:
            if self.getColumnWidth(columnId) > -1:
                target.addAttribute('width', str(self.getColumnWidth(columnId)))
            else:
                target.addAttribute('er', self.getColumnExpandRatio(columnId))


    def rowHeadersAreEnabled(self):
        return self.getRowHeaderMode() != self.ROW_HEADER_MODE_HIDDEN


    def paintRow(self, target, cells, iseditable, actionSet, iscomponent,
                 indexInRowbuffer, itemId):
        target.startTag('tr')

        self.paintRowAttributes(target, cells, actionSet,
                                indexInRowbuffer, itemId)

        # cells
        currentColumn = 0
        for columnId in self._visibleColumns:
            if (columnId is None) or self.isColumnCollapsed(columnId):
                continue

            # For each cell, if a cellStyleGenerator is specified, get the
            # specific style for the cell. If there is any, add it to the
            # target.
            if self._cellStyleGenerator is not None:
                cellStyle = self._cellStyleGenerator.getStyle(itemId, columnId)
                if cellStyle is not None and not (cellStyle == ''):
                    target.addAttribute('style-' + self._columnIdMap.key(columnId),
                                        cellStyle)

            if iscomponent[currentColumn] \
                    or iseditable \
                    and isinstance(Component, cells[self.CELL_FIRSTCOL + currentColumn][indexInRowbuffer]):
                c = cells[self.CELL_FIRSTCOL + currentColumn][indexInRowbuffer]
                if c is None:
                    target.addText('')
                else:
                    c.paint(target)
            else:
                target.addText(cells[self.CELL_FIRSTCOL + currentColumn][indexInRowbuffer])

        target.endTag('tr')


    def paintRowAttributes(self, *args):
        """None
        ---
        A method where extended Table implementations may add their custom
        attributes for rows.

        @param target
        @param itemId
        """
        # tr attributes
        nargs = len(args)
        if nargs == 2:
            target, itemId = args
        elif nargs == 5:
            target, cells, actionSet, indexInRowbuffer, itemId = args

            self.paintRowIcon(target, cells, indexInRowbuffer)
            self.paintRowHeader(target, cells, indexInRowbuffer)

            target.addAttribute('key', int(str(cells[self.CELL_KEY][indexInRowbuffer])))

            if self.isSelected(itemId):
                target.addAttribute('selected', True)

            # Actions
            if self._actionHandlers is not None:
                keys = list()
                for ah in self._actionHandlers:
                    aa = ah.getActions(itemId, self)
                    if aa is not None:
                        for ai in range(len(aa)):
                            key = self._actionMapper.key(aa[ai])
                            actionSet.add(aa[ai])
                            keys.append(key)
                target.addAttribute('al', keys)

            # For each row, if a cellStyleGenerator is specified, get the specific
            # style for the cell, using null as propertyId. If there is any, add it
            # to the target.
            if self._cellStyleGenerator is not None:
                rowStyle = self._cellStyleGenerator.getStyle(itemId, None)
                if rowStyle is not None and not (rowStyle == ''):
                    target.addAttribute('rowstyle', rowStyle)

            self.paintRowAttributes(target, itemId)
        else:
            raise ValueError, 'invalid number of arguments'


    def paintRowHeader(self, target, cells, indexInRowbuffer):
        if self.rowHeadersAreEnabled():
            if cells[self.CELL_HEADER][indexInRowbuffer] is not None:
                target.addAttribute('caption', cells[self.CELL_HEADER][indexInRowbuffer])


    def paintRowIcon(self, target, cells, indexInRowbuffer):
        if self.rowHeadersAreEnabled() \
                and cells[self.CELL_ICON][indexInRowbuffer] is not None:
            target.addAttribute('icon', cells[self.CELL_ICON][indexInRowbuffer])


    def getVisibleCells(self):
        """Gets the cached visible table contents.

        @return the cached visible table contents.
        """
        if self._pageBuffer is None:
            self.refreshRenderedCells()
        return self._pageBuffer


    def getPropertyValue(self, rowId, colId, prop):
        """Gets the value of property.

        By default if the table is editable the fieldFactory is used to create
        editors for table cells. Otherwise formatPropertyValue is used to format
        the value representation.

        @param rowId
                   the Id of the row (same as item Id).
        @param colId
                   the Id of the column.
        @param property
                   the Property to be presented.
        @return Object Either formatted value or Component for field.
        @see #setTableFieldFactory(TableFieldFactory)
        """
        if self.isEditable() and self._fieldFactory is not None:
            f = self._fieldFactory.createField(self.getContainerDataSource(),
                                               rowId, colId, self)
            if f is not None:
                # Remember that we have made this association so we can remove
                # it when the component is removed
                self._associatedProperties[f] = prop
                f.setPropertyDataSource(prop)
                return f

        return self.formatPropertyValue(rowId, colId, prop)


    def formatPropertyValue(self, rowId, colId, prop):
        """Formats table cell property values. By default the property.toString()
        and return a empty string for null properties.

        @param rowId
                   the Id of the row (same as item Id).
        @param colId
                   the Id of the column.
        @param property
                   the Property to be formatted.
        @return the String representation of property and its value.
        @since 3.1
        """
        # Action container
        if prop is None:
            return ''
        return str(prop)


    def addActionHandler(self, actionHandler):
        """Registers a new action handler for this container

        @see com.vaadin.event.Action.Container#addActionHandler(Action.Handler)
        """
        if actionHandler is not None:

            if self._actionHandlers is None:
                self._actionHandlers = list()
                self._actionMapper = KeyMapper()

            if actionHandler not in self._actionHandlers:
                self._actionHandlers.append(actionHandler)
                self.requestRepaint()


    def removeActionHandler(self, actionHandler):
        """Removes a previously registered action handler for the contents of this
        container.

        @see com.vaadin.event.Action.Container#removeActionHandler(Action.Handler)
        """
        if self._actionHandlers is not None \
                and actionHandler in self._actionHandlers:
            self._actionHandlers.remove(actionHandler)
            if len(self._actionHandlers) == 0:
                self._actionHandlers = None
                self._actionMapper = None
            self.requestRepaint()


    def removeAllActionHandlers(self):
        """Removes all action handlers"""
        self._actionHandlers = None
        self._actionMapper = None
        self.requestRepaint()


    # Property value change listening support


    def valueChange(self, event):
        """Notifies this listener that the Property's value has changed.

        Also listens changes in rendered items to refresh content area.

        @see com.vaadin.data.Property.ValueChangeListener#valueChange(Property.ValueChangeEvent)
        """
        if event.getProperty() == self:
            super(Table, self).valueChange(event)

        else:
            self.resetPageBuffer()
            self.refreshRenderedCells()
            self._containerChangeToBeRendered = True

        self.requestRepaint()


    def resetPageBuffer(self):
        self._firstToBeRenderedInClient = -1
        self._lastToBeRenderedInClient = -1
        self._reqFirstRowToPaint = -1
        self._reqRowsToPaint = -1
        self._pageBuffer = None


    def attach(self):
        """Notifies the component that it is connected to an application.

        @see com.vaadin.ui.Component#attach()
        """
        super(Table, self).attach()

        self.refreshRenderedCells()

        if self._visibleComponents is not None:
            for c in self._visibleComponents:
                c.attach()


    def detach(self):
        """Notifies the component that it is detached from the application

        @see com.vaadin.ui.Component#detach()
        """
        super(Table, self).detach()

        if self._visibleComponents is not None:
            for c in self._visibleComponents:
                c.detach()


    def removeAllItems(self):
        """Removes all Items from the Container.

        @see com.vaadin.data.Container#removeAllItems()
        """
        self._currentPageFirstItemId = None
        self._currentPageFirstItemIndex = 0
        return super(Table, self).removeAllItems()


    def removeItem(self, itemId):
        """Removes the Item identified by <code>ItemId</code> from the Container.

        @see com.vaadin.data.Container#removeItem(Object)
        """
        nextItemId = self.nextItemId(itemId)
        ret = super(Table, self).removeItem(itemId)
        if ret and itemId is not None \
                and itemId == self._currentPageFirstItemId:
            self._currentPageFirstItemId = nextItemId

        if not isinstance(self.items, ItemSetChangeNotifier):
            self.resetPageBuffer()
            self.refreshRenderedCells()

        return ret


    def removeContainerProperty(self, propertyId):
        """Removes a Property specified by the given Property ID from the Container.

        @see com.vaadin.data.Container#removeContainerProperty(Object)
        """

        # If a visible property is removed, remove the corresponding column
        self._visibleColumns.remove(propertyId)
        del self._columnAlignments[propertyId]
        del self._columnIcons[propertyId]
        del self._columnHeaders[propertyId]
        del self._columnFooters[propertyId]
        return super(Table, self).removeContainerProperty(propertyId)


    def addContainerProperty(self, *args):
        """Adds a new property to the table and show it as a visible column.

        @param propertyId
                   the Id of the proprty.
        @param type
                   the class of the property.
        @param defaultValue
                   the default value given for all existing items.
        @see com.vaadin.data.Container#addContainerProperty(Object, Class,
             Object)
        ---
        Adds a new property to the table and show it as a visible column.

        @param propertyId
                   the Id of the proprty
        @param type
                   the class of the property
        @param defaultValue
                   the default value given for all existing items
        @param columnHeader
                   the Explicit header of the column. If explicit header is not
                   needed, this should be set null.
        @param columnIcon
                   the Icon of the column. If icon is not needed, this should be
                   set null.
        @param columnAlignment
                   the Alignment of the column. Null implies align left.
        @throws UnsupportedOperationException
                    if the operation is not supported.
        @see com.vaadin.data.Container#addContainerProperty(Object, Class,
             Object)
        """
        args = args
        nargs = len(args)
        if nargs == 3:
            propertyId, typ, defaultValue = args
            visibleColAdded = False
            if not self._visibleColumns.contains(propertyId):
                self._visibleColumns.add(propertyId)
                visibleColAdded = True
            if not super(Table, self).addContainerProperty(propertyId, typ, defaultValue):
                if visibleColAdded:
                    self._visibleColumns.remove(propertyId)
                return False
            if not isinstance(self.items, PropertySetChangeNotifier):
                self.resetPageBuffer()
                self.refreshRenderedCells()
            return True
        elif nargs == 6:
            propertyId, typ, defaultValue, columnHeader, columnIcon, columnAlignment = args
            if not self.addContainerProperty(propertyId, typ, defaultValue):
                return False
            self.setColumnAlignment(propertyId, columnAlignment)
            self.setColumnHeader(propertyId, columnHeader)
            self.setColumnIcon(propertyId, columnIcon)
            return True
        else:
            raise ValueError, 'invalid number of arguments'


    def addGeneratedColumn(self, idd, generatedColumn):
        """Adds a generated column to the Table.
        <p>
        A generated column is a column that exists only in the Table, not as a
        property in the underlying Container. It shows up just as a regular
        column.
        </p>
        <p>
        A generated column will override a property with the same id, so that the
        generated column is shown instead of the column representing the
        property. Note that getContainerProperty() will still get the real
        property.
        </p>
        <p>
        Table will not listen to value change events from properties overridden
        by generated columns. If the content of your generated column depends on
        properties that are not directly visible in the table, attach value
        change listener to update the content on all depended properties.
        Otherwise your UI might not get updated as expected.
        </p>
        <p>
        Also note that getVisibleColumns() will return the generated columns,
        while getContainerPropertyIds() will not.
        </p>

        @param id
                   the id of the column to be added
        @param generatedColumn
                   the {@link ColumnGenerator} to use for this column
        """
        if generatedColumn is None:
            raise ValueError, 'Can not add null as a GeneratedColumn'
        if idd in self._columnGenerators:
            raise ValueError, 'Can not add the same GeneratedColumn twice, id:' + idd
        else:
            self._columnGenerators[idd] = generatedColumn
            # add to visible column list unless already there (overriding
            # column from DS)
            if idd not in self._visibleColumns:
                self._visibleColumns.append(idd)

            self.resetPageBuffer()
            self.refreshRenderedCells()


    def getColumnGenerator(self, columnId):
        """Returns the ColumnGenerator used to generate the given column.

        @param columnId
                   The id of the generated column
        @return The ColumnGenerator used for the given columnId or null.
        """
        return self._columnGenerators.get(columnId)


    def removeGeneratedColumn(self, columnId):
        """Removes a generated column previously added with addGeneratedColumn.

        @param columnId
                   id of the generated column to remove
        @return true if the column could be removed (existed in the Table)
        """
        if columnId in self._columnGenerators:
            del self._columnGenerators[columnId]
            # remove column from visibleColumns list unless it exists in
            # container (generator previously overrode this column)
            if columnId not in self.items.getContainerPropertyIds():
                self._visibleColumns.remove(columnId)
            self.resetPageBuffer()
            self.refreshRenderedCells()
            return True
        else:
            return False


    def getVisibleItemIds(self):
        """Returns item identifiers of the items which are currently rendered on the
        client.
        <p>
        Note, that some due to historical reasons the name of the method is bit
        misleading. Some items may be partly or totally out of the viewport of
        the table's scrollable area. Actully detecting rows which can be actually
        seen by the end user may be problematic due to the client server
        architecture. Using {@link #getCurrentPageFirstItemId()} combined with
        {@link #getPageLength()} may produce good enough estimates in some
        situations.

        @see com.vaadin.ui.Select#getVisibleItemIds()
        """
        visible = list()
        cells = self.getVisibleCells()

        for i in range(len(cells[self.CELL_ITEMID])):
            visible.append(cells[self.CELL_ITEMID][i])

        return visible


    def containerItemSetChange(self, event):
        """Container datasource item set change. Table must flush its buffers on
        change.

        @see com.vaadin.data.Container.ItemSetChangeListener#containerItemSetChange(com.vaadin.data.Container.ItemSetChangeEvent)
        """
        super(Table, self).containerItemSetChange(event)

        if isinstance(event, ItemSetChangeEvent):
            evt = event
            # if the event is not a global one and the added item is outside
            # the visible/buffered area, no need to do anything
            if evt.getAddedItemIndex() != -1 \
                    and self._firstToBeRenderedInClient >= 0 \
                    and self._lastToBeRenderedInClient >= 0 \
                    and (self._firstToBeRenderedInClient > evt.getAddedItemIndex()) \
                    or (self._lastToBeRenderedInClient < evt.getAddedItemIndex()):
                return

        # ensure that page still has first item in page, ignore buffer refresh
        # (forced in this method)
        self.setCurrentPageFirstItemIndex(self.getCurrentPageFirstItemIndex(), False)

        self.resetPageBuffer()
        self.refreshRenderedCells()


    def containerPropertySetChange(self, event):
        """Container datasource property set change. Table must flush its buffers on
        change.

        @see com.vaadin.data.Container.PropertySetChangeListener#containerPropertySetChange(com.vaadin.data.Container.PropertySetChangeEvent)
        """
        self.disableContentRefreshing()
        super(Table, self).containerPropertySetChange(event)

        # sanitetize visibleColumns. note that we are not adding previously
        # non-existing properties as columns
        containerPropertyIds = self.getContainerDataSource().getContainerPropertyIds()
        newVisibleColumns = list(self._visibleColumns)

        for idd in newVisibleColumns:
            if idd not in containerPropertyIds or (idd in self._columnGenerators):
                newVisibleColumns.remove()
        self.setVisibleColumns(list(newVisibleColumns))

        # same for collapsed columns
        for idd in self._collapsedColumns:
            if idd not in containerPropertyIds or (id in self._columnGenerators):
                self._collapsedColumns.remove()

        self.resetPageBuffer()
        self.enableContentRefreshing(True)


    def setNewItemsAllowed(self, allowNewOptions):
        """Adding new items is not supported.

        @throws UnsupportedOperationException
                    if set to true.
        @see com.vaadin.ui.Select#setNewItemsAllowed(boolean)
        """
        if allowNewOptions:
            raise NotImplementedError


    def nextItemId(self, itemId):
        """Gets the ID of the Item following the Item that corresponds to itemId.

        @see com.vaadin.data.Container.Ordered#nextItemId(java.lang.Object)
        """
        return self.items.nextItemId(itemId)


    def prevItemId(self, itemId):
        """Gets the ID of the Item preceding the Item that corresponds to the
        itemId.

        @see com.vaadin.data.Container.Ordered#prevItemId(java.lang.Object)
        """
        return self.items.prevItemId(itemId)


    def firstItemId(self):
        """Gets the ID of the first Item in the Container.

        @see com.vaadin.data.Container.Ordered#firstItemId()
        """
        return self.items.firstItemId()


    def lastItemId(self):
        """Gets the ID of the last Item in the Container.

        @see com.vaadin.data.Container.Ordered#lastItemId()
        """
        return self.items.lastItemId()


    def isFirstId(self, itemId):
        """Tests if the Item corresponding to the given Item ID is the first Item in
        the Container.

        @see com.vaadin.data.Container.Ordered#isFirstId(java.lang.Object)
        """
        return self.items.isFirstId(itemId)


    def isLastId(self, itemId):
        """Tests if the Item corresponding to the given Item ID is the last Item in
        the Container.

        @see com.vaadin.data.Container.Ordered#isLastId(java.lang.Object)
        """
        return self.items.isLastId(itemId)


    def addItemAfter(self, previousItemId, newItemId=None):
        """Adds new item after the given item.

        @see com.vaadin.data.Container.Ordered#addItemAfter(java.lang.Object)
        ---
        Adds new item after the given item.

        @see com.vaadin.data.Container.Ordered#addItemAfter(java.lang.Object,
             java.lang.Object)
        """
        if newItemId is None:
            item = self.items.addItemAfter(previousItemId)
        else:
            item = self.items.addItemAfter(previousItemId, newItemId)

        if not isinstance(self.items, ItemSetChangeNotifier):
            self.resetPageBuffer()
            self.refreshRenderedCells()

        return item


    def setTableFieldFactory(self, fieldFactory):
        """Sets the TableFieldFactory that is used to create editor for table cells.

        The TableFieldFactory is only used if the Table is editable. By default
        the DefaultFieldFactory is used.

        @param fieldFactory
                   the field factory to set.
        @see #isEditable
        @see DefaultFieldFactory
        """
        self._fieldFactory = fieldFactory


    def getTableFieldFactory(self):
        """Gets the TableFieldFactory that is used to create editor for table cells.

        The FieldFactory is only used if the Table is editable.

        @return TableFieldFactory used to create the Field instances.
        @see #isEditable
        """
        return self._fieldFactory


    def getFieldFactory(self):
        """Gets the FieldFactory that is used to create editor for table cells.

        The FieldFactory is only used if the Table is editable.

        @return FieldFactory used to create the Field instances.
        @see #isEditable
        @deprecated use {@link #getTableFieldFactory()} instead
        """
        if isinstance(self._fieldFactory, FieldFactory):
            return self._fieldFactory

        return None


    def setFieldFactory(self, fieldFactory):
        """Sets the FieldFactory that is used to create editor for table cells.

        The FieldFactory is only used if the Table is editable. By default the
        BaseFieldFactory is used.

        @param fieldFactory
                   the field factory to set.
        @see #isEditable
        @see BaseFieldFactory
        @deprecated use {@link #setTableFieldFactory(TableFieldFactory)} instead
        """
        self._fieldFactory = fieldFactory
        # Assure visual refresh
        self.resetPageBuffer()
        self.refreshRenderedCells()


    def isEditable(self):
        """Is table editable.

        If table is editable a editor of type Field is created for each table
        cell. The assigned FieldFactory is used to create the instances.

        To provide custom editors for table cells create a class implementins the
        FieldFactory interface, and assign it to table, and set the editable
        property to true.

        @return true if table is editable, false oterwise.
        @see Field
        @see FieldFactory
        """
        return self._editable


    def setEditable(self, editable):
        """Sets the editable property.

        If table is editable a editor of type Field is created for each table
        cell. The assigned FieldFactory is used to create the instances.

        To provide custom editors for table cells create a class implementins the
        FieldFactory interface, and assign it to table, and set the editable
        property to true.

        @param editable
                   true if table should be editable by user.
        @see Field
        @see FieldFactory
        """
        self._editable = editable
        # Assure visual refresh
        self.resetPageBuffer()
        self.refreshRenderedCells()


    def sort(self, *args):
        """Sorts the table.

        @throws UnsupportedOperationException
                    if the container data source does not implement
                    Container.Sortable
        @see com.vaadin.data.Container.Sortable#sort(java.lang.Object[],
             boolean[])
        ---
        Sorts the table by currently selected sorting column.

        @throws UnsupportedOperationException
                    if the container data source does not implement
                    Container.Sortable
        """
        nargs = len(args)
        if nargs == 0:
            if self.getSortContainerPropertyId() is None:
                return
            self.sort([self._sortContainerPropertyId], [self._sortAscending])
        elif nargs == 2:
            propertyId, ascending = args
            c = self.getContainerDataSource()
            if isinstance(c, Sortable):
                pageIndex = self.getCurrentPageFirstItemIndex()
                c.sort(propertyId, ascending)
                self.setCurrentPageFirstItemIndex(pageIndex)
                self.resetPageBuffer()
                self.refreshRenderedCells()
            elif c is not None:
                raise NotImplementedError, 'Underlying Data does not allow sorting'
        else:
            raise ValueError, 'invalid number of arguments'


    def getSortableContainerPropertyIds(self):
        """Gets the container property IDs, which can be used to sort the item.

        @see com.vaadin.data.Container.Sortable#getSortableContainerPropertyIds()
        """
        c = self.getContainerDataSource()
        if isinstance(c, Sortable) and not self.isSortDisabled():
            return c.getSortableContainerPropertyIds()
        else:
            return list()


    def getSortContainerPropertyId(self):
        """Gets the currently sorted column property ID.

        @return the Container property id of the currently sorted column.
        """
        return self._sortContainerPropertyId


    def setSortContainerPropertyId(self, propertyId, doSort=True):
        """Sets the currently sorted column property id.

        @param propertyId
                   the Container property id of the currently sorted column.
        ---
        Internal method to set currently sorted column property id. With doSort
        flag actual sorting may be bypassed.

        @param propertyId
        @param doSort
        """
        if (self._sortContainerPropertyId is not None \
            and not (self._sortContainerPropertyId == propertyId)) \
                or (self._sortContainerPropertyId is None \
                    and propertyId is not None):
            self._sortContainerPropertyId = propertyId
            if doSort:
                self.sort()
                # Assures the visual refresh
                self.refreshRenderedCells()


    def isSortAscending(self):
        """Is the table currently sorted in ascending order.

        @return <code>true</code> if ascending, <code>false</code> if descending.
        """
        return self._sortAscending


    def setSortAscending(self, ascending, doSort=True):
        """Sets the table in ascending order.

        @param ascending
                   <code>true</code> if ascending, <code>false</code> if
                   descending.
        ---
        Internal method to set sort ascending. With doSort flag actual sort can
        be bypassed.

        @param ascending
        @param doSort
        """
        if self._sortAscending != ascending:
            self._sortAscending = ascending
            if doSort:
                self.sort()
        # Assures the visual refresh
        self.refreshRenderedCells()


    def isSortDisabled(self):
        """Is sorting disabled altogether.

        True iff no sortable columns are given even in the case where data source
        would support this.

        @return True iff sorting is disabled.
        """
        return self._sortDisabled


    def setSortDisabled(self, sortDisabled):
        """Disables the sorting altogether.

        To disable sorting altogether, set to true. In this case no sortable
        columns are given even in the case where datasource would support this.

        @param sortDisabled
                   True iff sorting is disabled.
        """
        if self._sortDisabled != sortDisabled:
            self._sortDisabled = sortDisabled
            self.refreshRenderedCells()


    def setLazyLoading(self, useLazyLoading):
        """Table does not support lazy options loading mode. Setting this true will
        throw UnsupportedOperationException.

        @see com.vaadin.ui.Select#setLazyLoading(boolean)
        """
        if useLazyLoading:
            raise NotImplementedError, 'Lazy options loading is not supported by Table.'


    def setCellStyleGenerator(self, cellStyleGenerator):
        """Set cell style generator for Table.

        @param cellStyleGenerator
                   New cell style generator or null to remove generator.
        """
        self._cellStyleGenerator = cellStyleGenerator
        self.requestRepaint()


    def getCellStyleGenerator(self):
        """Get the current cell style generator."""
        return self._cellStyleGenerator


    def addListener(self, listener):
        """None
        ---
        Adds a header click listener which handles the click events when the user
        clicks on a column header cell in the Table.
        <p>
        The listener will receive events which contain information about which
        column was clicked and some details about the mouse event.
        </p>

        @param listener
                   The handler which should handle the header click events.
        ---
        Adds a footer click listener which handles the click events when the user
        clicks on a column footer cell in the Table.
        <p>
        The listener will receive events which contain information about which
        column was clicked and some details about the mouse event.
        </p>

        @param listener
                   The handler which should handle the footer click events.
        ---
        Adds a column resize listener to the Table. A column resize listener is
        called when a user resizes a columns width.

        @param listener
                   The listener to attach to the Table
        ---
        Adds a column reorder listener to the Table. A column reorder listener is
        called when a user reorders columns.

        @param listener
                   The listener to attach to the Table
        """
        if isinstance(listener, ColumnReorderListener):
            self.addListener(VScrollTable.COLUMN_REORDER_EVENT_ID, self.ColumnReorderEvent, listener, self.ColumnReorderEvent.METHOD)
        elif isinstance(listener, ColumnResizeListener):
            self.addListener(VScrollTable.COLUMN_RESIZE_EVENT_ID, self.ColumnResizeEvent, listener, self.ColumnResizeEvent.COLUMN_RESIZE_METHOD)
        elif isinstance(listener, FooterClickListener):
            self.addListener(VScrollTable.FOOTER_CLICK_EVENT_ID, self.FooterClickEvent, listener, self.FooterClickEvent.FOOTER_CLICK_METHOD)
        elif isinstance(listener, HeaderClickListener):
            self.addListener(VScrollTable.HEADER_CLICK_EVENT_ID, self.HeaderClickEvent, listener, self.HeaderClickEvent.HEADER_CLICK_METHOD)
        else:
            self.addListener(VScrollTable.ITEM_CLICK_EVENT_ID, ItemClickEvent, listener, ItemClickEvent.ITEM_CLICK_METHOD)


    def removeListener(self, listener):
        """None
        ---
        Removes a header click listener

        @param listener
                   The listener to remove.
        ---
        Removes a footer click listener

        @param listener
                   The listener to remove.
        ---
        Removes a column resize listener from the Table.

        @param listener
                   The listener to remove
        ---
        Removes a column reorder listener from the Table.

        @param listener
                   The listener to remove
        """

        if isinstance(listener, ColumnReorderListener):
            self.removeListener(VScrollTable.COLUMN_REORDER_EVENT_ID, self.ColumnReorderEvent, listener)
        elif isinstance(listener, ColumnResizeListener):
            self.removeListener(VScrollTable.COLUMN_RESIZE_EVENT_ID, self.ColumnResizeEvent, listener)
        elif isinstance(listener, FooterClickListener):
            self.removeListener(VScrollTable.FOOTER_CLICK_EVENT_ID, self.FooterClickEvent, listener)
        elif isinstance(listener, HeaderClickListener):
            self.removeListener(VScrollTable.HEADER_CLICK_EVENT_ID, self.HeaderClickEvent, listener)
        else:
            self.removeListener(VScrollTable.ITEM_CLICK_EVENT_ID, ItemClickEvent, listener)


    def setEnabled(self, enabled):
        # Virtually identical to AbstractCompoenentContainer.setEnabled();
        super(Table, self).setEnabled(enabled)
        if self.getParent() is not None and not self.getParent().isEnabled():
            # some ancestor still disabled, don't update children
            return
        else:
            self.requestRepaintAll()


    def requestRepaintAll(self):
        self.requestRepaint()
        if self._visibleComponents is not None:
            for c in self._visibleComponents:
                if isinstance(c, Form):
                    # Form has children in layout, but is not
                    # ComponentContainer
                    c.requestRepaint()
                    c.getLayout().requestRepaintAll()
                elif isinstance(c, Table):
                    c.requestRepaintAll()
                elif isinstance(c, ComponentContainer):
                    c.requestRepaintAll()
                else:
                    c.requestRepaint()


    def setDragMode(self, newDragMode):
        """Sets the drag start mode of the Table. Drag start mode controls how Table
        behaves as a drag source.

        @param newDragMode
        """
        self._dragMode = newDragMode
        self.requestRepaint()


    def getDragMode(self):
        """@return the current start mode of the Table. Drag start mode controls how
                Table behaves as a drag source.
        """
        return self._dragMode


    def getTransferable(self, rawVariables):
        transferable = TableTransferable(rawVariables, self)
        return transferable


    def getDropHandler(self):
        return self._dropHandler


    def setDropHandler(self, dropHandler):
        self._dropHandler = dropHandler


    def translateDropTargetDetails(self, clientVariables):
        return AbstractSelectTargetDetails(clientVariables, self)  # FIXME: _AbstractSelect_self


    def setMultiSelectMode(self, mode):
        """Sets the behavior of how the multi-select mode should behave when the
        table is both selectable and in multi-select mode.
        <p>
        Note, that on some clients the mode may not be respected. E.g. on touch
        based devices CTRL/SHIFT base selection method is invalid, so touch based
        browsers always use the {@link MultiSelectMode#SIMPLE}.

        @param mode
                   The select mode of the table
        """
        self._multiSelectMode = mode
        self.requestRepaint()


    def getMultiSelectMode(self):
        """Returns the select mode in which multi-select is used.

        @return The multi select mode
        """
        return self._multiSelectMode


    def getColumnFooter(self, propertyId):
        """Gets the footer caption beneath the rows

        @param propertyId
                   The propertyId of the column *
        @return The caption of the footer or NULL if not set
        """
        return self._columnFooters.get(propertyId)


    def setColumnFooter(self, propertyId, footer):
        """Sets the column footer caption. The column footer caption is the text
        displayed beneath the column if footers have been set visible.

        @param propertyId
                   The properyId of the column

        @param footer
                   The caption of the footer
        """
        if footer is None:
            del self._columnFooters[propertyId]
        else:
            self._columnFooters[propertyId] = footer

        self.requestRepaint()

    def setFooterVisible(self, visible):
        """Sets the footer visible in the bottom of the table.
        <p>
        The footer can be used to add column related data like sums to the bottom
        of the Table using setColumnFooter(Object propertyId, String footer).
        </p>

        @param visible
                   Should the footer be visible
        """
        self._columnFootersVisible = visible
        # Assures the visual refresh
        self.refreshRenderedCells()


    def isFooterVisible(self):
        """Is the footer currently visible?

        @return Returns true if visible else false
        """
        return self._columnFootersVisible


class ColumnGenerator(object):
    """Used to create "generated columns"; columns that exist only in the Table,
    not in the underlying Container. Implement this interface and pass it to
    Table.addGeneratedColumn along with an id for the column to be generated.
    """

    def generateCell(self, source, itemId, columnId):
        """Called by Table when a cell in a generated column needs to be
        generated.

        @param source
                   the source Table
        @param itemId
                   the itemId (aka rowId) for the of the cell to be generated
        @param columnId
                   the id for the generated column (as specified in
                   addGeneratedColumn)
        @return
        """
        pass


class CellStyleGenerator(object):
    """Allow to define specific style on cells (and rows) contents. Implements
    this interface and pass it to Table.setCellStyleGenerator. Row styles are
    generated when porpertyId is null. The CSS class name that will be added
    to the cell content is <tt>v-table-cell-content-[style name]</tt>, and
    the row style will be <tt>v-table-row-[style name]</tt>.
    """

    def getStyle(self, itemId, propertyId):
        """Called by Table when a cell (and row) is painted.

        @param itemId
                   The itemId of the painted cell
        @param propertyId
                   The propertyId of the cell, null when getting row style
        @return The style name to add to this cell or row. (the CSS class
                name will be v-table-cell-content-[style name], or
                v-table-row-[style name] for rows)
        """
        pass


class TableTransferable(DataBoundTransferable):
    """Concrete implementation of {@link DataBoundTransferable} for data
    transferred from a table.

    @see {@link DataBoundTransferable}.

    @since 6.3
    """

    def __init__(self, rawVariables, _Table_this):
        super(TableTransferable, self)(_Table_this, rawVariables)
        obj = rawVariables.get('itemId')
        if obj is not None:
            self.setData('itemId', self.itemIdMapper.get(object))

        obj = rawVariables.get('propertyId')
        if obj is not None:
            self.setData('propertyId', self.columnIdMap.get(object))


    def getItemId(self):
        return self.getData('itemId')


    def getPropertyId(self):
        return self.getData('propertyId')


    def getSourceComponent(self):
        return super(TableTransferable, self).getSourceComponent()


class TableDropCriterion(ServerSideCriterion):
    """Lazy loading accept criterion for Table. Accepted target rows are loaded
    from server once per drag and drop operation. Developer must override one
    method that decides on which rows the currently dragged data can be
    dropped.

    <p>
    Initially pretty much no data is sent to client. On first required
    criterion check (per drag request) the client side data structure is
    initialized from server and no subsequent requests requests are needed
    during that drag and drop operation.
    """

    def __init__(self):
        self._table = None
        self._allowedItemIds = None


    def getIdentifier(self):
        return TableDropCriterion.getCanonicalName()  # FIXME: getCanonicalName


    def accept(self, dragEvent):
        dropTargetData = dragEvent.getTargetDetails()
        self._table = dragEvent.getTargetDetails().getTarget()
        visibleItemIds = list(self._table.getPageLength())
        len(visibleItemIds)
        idd = self._table.getCurrentPageFirstItemId()
        i = 0
        while i < self._table.getPageLength() and idd is not None:
            visibleItemIds.append(idd)
            idd = self._table.nextItemId(idd)
            i += 1
        self._allowedItemIds = self.getAllowedItemIds(dragEvent, self._table, visibleItemIds)
        return dropTargetData.getItemIdOver() in self._allowedItemIds


    def paintResponse(self, target):
        # send allowed nodes to client so subsequent requests can be
        # avoided
        arry = list(self._allowedItemIds)
        for i in range(len(arry)):
            key = self._table.itemIdMapper.key( arry[i] )
            arry[i] = key

        target.addAttribute('allowedIds', arry)


    def getAllowedItemIds(self, dragEvent, table, visibleItemIds):
        """@param dragEvent
        @param table
                   the table for which the allowed item identifiers are
                   defined
        @param visibleItemIds
                   the list of currently rendered item identifiers, accepted
                   item id's need to be detected only for these visible items
        @return the set of identifiers for items on which the dragEvent will
                be accepted
        """
        pass


class HeaderClickListener(object):
    """Interface for the listener for column header mouse click events. The
    headerClick method is called when the user presses a header column cell.
    """

    def headerClick(self, event):
        """Called when a user clicks a header column cell

        @param event
                   The event which contains information about the column and
                   the mouse click event
        """
        pass


class HeaderClickEvent(ClickEvent):
    """Click event fired when clicking on the Table headers. The event includes
    a reference the the Table the event originated from, the property id of
    the column which header was pressed and details about the mouse event
    itself.
    """
    HEADER_CLICK_METHOD = getattr(HeaderClickListener, 'headerClick')

    def __init__(self, source, propertyId, details):
        super(HeaderClickEvent, self)(source, details)
        self._columnPropertyId = propertyId

    def getPropertyId(self):
        """Gets the property id of the column which header was pressed

        @return The column propety id
        """
        return self._columnPropertyId


class FooterClickListener(object):
    """Interface for the listener for column footer mouse click events. The
    footerClick method is called when the user presses a footer column cell.
    """

    def footerClick(self, event):
        """Called when a user clicks a footer column cell

        @param event
                   The event which contains information about the column and
                   the mouse click event
        """
        pass


class FooterClickEvent(ClickEvent):
    """Click event fired when clicking on the Table footers. The event includes
    a reference the the Table the event originated from, the property id of
    the column which header was pressed and details about the mouse event
    itself.
    """

    FOOTER_CLICK_METHOD = getattr(FooterClickListener, 'footerClick')

    def __init__(self, source, propertyId, details):
        """Constructor

        @param source
                   The source of the component
        @param propertyId
                   The propertyId of the column
        @param details
                   The mouse details of the click
        """
        super(FooterClickEvent, self)(source, details)
        self._columnPropertyId = propertyId

    def getPropertyId(self):
        """Gets the property id of the column which header was pressed

        @return The column propety id
        """
        return self._columnPropertyId


class ColumnResizeListener(object):
    """Interface for listening to column resize events."""

    def columnResize(self, event):
        """This method is triggered when the column has been resized

        @param event
                   The event which contains the column property id, the
                   previous width of the column and the current width of the
                   column
        """
        pass


class ColumnResizeEvent(ComponentEvent):
    """This event is fired when a column is resized. The event contains the
    columns property id which was fired, the previous width of the column and
    the width of the column after the resize.
    """

    COLUMN_RESIZE_METHOD = getattr(ColumnResizeListener, 'columnResize')

    def __init__(self, source, propertyId, previous, current):
        """Constructor

        @param source
                   The source of the event
        @param propertyId
                   The columns property id
        @param previous
                   The width in pixels of the column before the resize event
        @param current
                   The width in pixels of the column after the resize event
        """
        super(ColumnResizeEvent, self)(source)
        self._previousWidth = previous
        self._currentWidth = current
        self._columnPropertyId = propertyId

    def getPropertyId(self):
        """Get the column property id of the column that was resized.

        @return The column property id
        """
        return self._columnPropertyId

    def getPreviousWidth(self):
        """Get the width in pixels of the column before the resize event

        @return Width in pixels
        """
        return self._previousWidth

    def getCurrentWidth(self):
        """Get the width in pixels of the column after the resize event

        @return Width in pixels
        """
        return self._currentWidth


class ColumnReorderListener(object):
    """Interface for listening to column reorder events."""

    def columnReorder(self, event):
        """This method is triggered when the column has been reordered

        @param event
        """
        pass


class ColumnReorderEvent(ComponentEvent):
    """This event is fired when a columns are reordered by the end user user."""

    METHOD = getattr(ColumnReorderListener, 'columnReorder')

    def __init__(self, source):
        """Constructor

        @param source
                   The source of the event
        """
        super(ColumnReorderEvent, self)(source)
