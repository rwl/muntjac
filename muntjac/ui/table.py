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

"""Used for representing data or components in a pageable and selectable
table."""

import logging

from warnings import warn

from muntjac.ui.field import IField
from muntjac.ui.field_factory import IFieldFactory
from muntjac.ui.form import Form
from muntjac.ui.default_field_factory import DefaultFieldFactory
from muntjac.ui.component_container import IComponentContainer
from muntjac.ui.component import IComponent, Event as ComponentEvent

from muntjac.data.property import IValueChangeNotifier, IValueChangeListener
from muntjac.event.mouse_events import ClickEvent
from muntjac.event import action
from muntjac.event.data_bound_transferable import DataBoundTransferable
from muntjac.event.dd.drop_target import IDropTarget
from muntjac.event.dd.drag_source import IDragSource

from muntjac.terminal.key_mapper import KeyMapper
from muntjac.terminal.gwt.client.mouse_event_details import MouseEventDetails
from muntjac.terminal.gwt.client.ui.v_scroll_table import VScrollTable

from muntjac.data import container

from muntjac.event.dd.acceptcriteria.server_side_criterion import \
    ServerSideCriterion

from muntjac.ui.abstract_select import \
    AbstractSelect, MultiSelectMode, AbstractSelectTargetDetails

from muntjac.event.item_click_event import \
    ItemClickEvent, IItemClickNotifier, IItemClickSource, ITEM_CLICK_METHOD,\
    IItemClickListener

from muntjac.data.util.indexed_container import \
    ItemSetChangeEvent, IndexedContainer

from muntjac.util import clsname


logger = logging.getLogger(__name__)


class Table(AbstractSelect, #container.IOrdered, action.IContainer,
            container.ISortable, IItemClickSource, IItemClickNotifier,
            IDragSource, IDropTarget):
    """C{Table} is used for representing data or components in a
    pageable and selectable table.

    Scalability of the Table is largely dictated by the container. A table
    does not have a limit for the number of items and is just as fast with
    hundreds of thousands of items as with just a few. The current GWT
    implementation with scrolling however limits the number of rows to
    around 500000, depending on the browser and the pixel height of rows.

    Components in a Table will not have their caption nor icon rendered.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    CLIENT_WIDGET = None #ClientWidget(VScrollTable, LoadStyle.EAGER)

    CELL_KEY = 0
    CELL_HEADER = 1
    CELL_ICON = 2
    CELL_ITEMID = 3
    CELL_GENERATED_ROW = 4
    CELL_FIRSTCOL = 5

    #: Left column alignment. <b>This is the default behaviour.</b>
    ALIGN_LEFT = 'b'

    #: Center column alignment.
    ALIGN_CENTER = 'c'

    #: Right column alignment.
    ALIGN_RIGHT = 'e'

    #: Column header mode: Column headers are hidden.
    COLUMN_HEADER_MODE_HIDDEN = -1

    #: Column header mode: Property ID:s are used as column headers.
    COLUMN_HEADER_MODE_ID = 0

    #: Column header mode: Column headers are explicitly specified with
    #  L{setColumnHeaders}.
    COLUMN_HEADER_MODE_EXPLICIT = 1

    #: Column header mode: Column headers are explicitly specified with
    #  L{setColumnHeaders}. If a header is not specified
    #  for a given property, its property id is used instead.
    #
    #  B{This is the default behavior.}
    COLUMN_HEADER_MODE_EXPLICIT_DEFAULTS_ID = 2

    #: Row caption mode: The row headers are hidden.
    #  B{This is the default mode.}
    ROW_HEADER_MODE_HIDDEN = -1

    #: Row caption mode: Items Id-objects toString is used as row caption.
    ROW_HEADER_MODE_ID = AbstractSelect.ITEM_CAPTION_MODE_ID

    #: Row caption mode: Item-objects toString is used as row caption.
    ROW_HEADER_MODE_ITEM = AbstractSelect.ITEM_CAPTION_MODE_ITEM

    #: Row caption mode: Index of the item is used as item caption. The
    #  index mode can only be used with the containers implementing
    #  container.IIndexed interface.
    ROW_HEADER_MODE_INDEX = AbstractSelect.ITEM_CAPTION_MODE_INDEX

    #: Row caption mode: Item captions are explicitly specified.
    ROW_HEADER_MODE_EXPLICIT = AbstractSelect.ITEM_CAPTION_MODE_EXPLICIT

    #: Row caption mode: Item captions are read from property specified
    #  with L{#setItemCaptionPropertyId(Object)}.
    ROW_HEADER_MODE_PROPERTY = AbstractSelect.ITEM_CAPTION_MODE_PROPERTY

    #: Row caption mode: Only icons are shown, the captions are hidden.
    ROW_HEADER_MODE_ICON_ONLY = AbstractSelect.ITEM_CAPTION_MODE_ICON_ONLY

    #: Row caption mode: Item captions are explicitly specified, but if
    #  the caption is missing, the item id objects C{toString()}
    #  is used instead.
    ROW_HEADER_MODE_EXPLICIT_DEFAULTS_ID = \
            AbstractSelect.ITEM_CAPTION_MODE_EXPLICIT_DEFAULTS_ID

    #: The default rate that table caches rows for smooth scrolling.
    _CACHE_RATE_DEFAULT = 2

    _ROW_HEADER_COLUMN_KEY = '0'

    _ROW_HEADER_FAKE_PROPERTY_ID = object()


    def __init__(self, caption=None, dataSource=None):
        """Creates a new table with caption and connect it to a IContainer.
        """
        #: True if column collapsing is allowed.
        self._columnCollapsingAllowed = False

        #: True if reordering of columns is allowed on the client side.
        self._columnReorderingAllowed = False

        #: Keymapper for column ids.
        self._columnIdMap = KeyMapper()

        #: Holds visible column propertyIds - in order.
        self._visibleColumns = list()

        #: Holds propertyIds of currently collapsed columns.
        self._collapsedColumns = set()

        #: Holds headers for visible columns (by propertyId).
        self._columnHeaders = dict()

        #: Holds footers for visible columns (by propertyId).
        self._columnFooters = dict()

        #: Holds icons for visible columns (by propertyId).
        self._columnIcons = dict()

        #: Holds alignments for visible columns (by propertyId).
        self._columnAlignments = dict()

        #: Holds column widths in pixels (Integer) or expand ratios
        #  (Float) for visible columns (by propertyId).
        self._columnWidths = dict()

        #: Holds column generators
        self._columnGenerators = dict()

        #: Holds value of property pageLength. 0 disables paging.
        self._pageLength = 15

        #: Id the first item on the current page.
        self._currentPageFirstItemId = None

        #: Index of the first item on the current page.
        self._currentPageFirstItemIndex = 0

        #: Holds value of property selectable.
        self._selectable = False

        #: Holds value of property columnHeaderMode.
        self._columnHeaderMode = self.COLUMN_HEADER_MODE_EXPLICIT_DEFAULTS_ID

        #: Should the Table footer be visible?
        self._columnFootersVisible = False

        #: True iff the row captions are hidden.
        self._rowCaptionsAreHidden = True

        #: Page contents buffer used in buffered mode.
        self._pageBuffer = None

        #: Set of properties listened - the list is kept to release
        #  the listeners later.
        self._listenedProperties = None

        #: Set of visible components - the is used for needsRepaint
        #  calculation.
        self._visibleComponents = None

        #: List of action handlers.
        self._actionHandlers = None

        #: Action mapper.
        self._actionMapper = None

        #: Table cell editor factory.
        self._fieldFactory = DefaultFieldFactory.get()

        #: Is table editable.
        self._editable = False

        #: Current sorting direction.
        self._sortAscending = True

        #: Currently table is sorted on this propertyId.
        self._sortContainerPropertyId = None

        #: Is table sorting disabled alltogether; even if some of
        #  the properties would be sortable.
        self._sortDisabled = False

        #: Number of rows explicitly requested by the client to be painted
        #  on next paint. This is -1 if no request by the client is made.
        #  Painting the component will automatically reset this to -1.
        self._reqRowsToPaint = -1

        #: Index of the first rows explicitly requested by the client to be
        #  painted. This is -1 if no request by the client is made. Painting
        #  the component will automatically reset this to -1.
        self._reqFirstRowToPaint = -1

        self._firstToBeRenderedInClient = -1

        self._lastToBeRenderedInClient = -1

        self._isContentRefreshesEnabled = True

        self._pageBufferFirstIndex = 0

        self._containerChangeToBeRendered = False

        #: Table cell specific style generator
        self._cellStyleGenerator = None

        #: Table cell specific tooltip generator
        self._itemDescriptionGenerator = None

        #: EXPERIMENTAL feature: will tell the client to re-calculate column
        #  widths if set to true. Currently no setter: extend to enable.
        self.alwaysRecalculateColumnWidths = False

        self._cacheRate = self._CACHE_RATE_DEFAULT

        self._dragMode = TableDragMode.NONE

        self._dropHandler = None

        self._multiSelectMode = MultiSelectMode.DEFAULT

        self._rowCacheInvalidated = False

        self._rowGenerator = None

        self._associatedProperties = dict()

        self._painted = False


        super(Table, self).__init__()

        self.setRowHeaderMode(self.ROW_HEADER_MODE_HIDDEN)

        if caption is not None:
            self.setCaption(caption)

        if dataSource is not None:
            self.setContainerDataSource(dataSource)


    def getVisibleColumns(self):
        """Gets the array of visible column id:s, including generated columns.

        The columns are show in the order of their appearance in this array.

        @return: an array of currently visible propertyIds and generated column
                 ids.
        """
        if self._visibleColumns is None:
            return None

        return list(self._visibleColumns)


    def setVisibleColumns(self, visibleColumns):
        """Sets the array of visible column property ids.

        The columns are show in the order of their appearance in this array.

        @param visibleColumns:
                   the array of shown property ids.
        """
        # Visible columns must exist
        if visibleColumns is None:
            raise ValueError, 'Can not set visible columns to null value'

        # TODO: add error check that no duplicate identifiers exist

        # Checks that the new visible columns contains no nulls and
        # properties exist
        properties = self.getContainerPropertyIds()
        for vc in visibleColumns:
            if vc is None:
                raise ValueError, 'Ids must be non-nulls'
            elif (vc not in properties) and (vc not in self._columnGenerators):
                raise ValueError('Ids must exist in the IContainer '
                        'or as a generated column , missing id: ' + str(vc))

        # If this is called before the constructor is finished, it might be
        # uninitialized
        newVC = list()
        for vc in visibleColumns:
            newVC.append(vc)

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
        self.refreshRowCache()


    def getColumnHeaders(self):
        """Gets the headers of the columns.

        The headers match the property id:s given my the set visible column
        headers. The table must be set in either L{COLUMN_HEADER_MODE_EXPLICIT}
        or L{COLUMN_HEADER_MODE_EXPLICIT_DEFAULTS_ID} mode to show the
        headers. In the defaults mode any nulls in the headers array are
        replaced with id.__str__.

        @return: the array of column headers.
        """
        if self._columnHeaders is None:
            return None

        headers = list()

        for col in self._visibleColumns:
            headers.append( self.getColumnHeader(col) )

        return headers


    def setColumnHeaders(self, columnHeaders):
        """Sets the headers of the columns.

        The headers match the property id:s given my the set visible column
        headers. The table must be set in either L{COLUMN_HEADER_MODE_EXPLICIT}
        or L{COLUMN_HEADER_MODE_EXPLICIT_DEFAULTS_ID} mode to show the
        headers. In the defaults mode any nulls in the headers array are
        replaced with id.toString() outputs when rendering.

        @param columnHeaders:
                   the Array of column headers that match the
                   L{getVisibleColumns} method.
        """
        if len(columnHeaders) != len(self._visibleColumns):
            raise ValueError,('The length of the headers array must '
                    'match the number of visible columns')

        self._columnHeaders.clear()

        i = 0
        it = iter(self._visibleColumns)
        while i < len(columnHeaders):
            try:
                self._columnHeaders[it.next()] = columnHeaders[i]
                i += 1
            except StopIteration:
                break

        self.requestRepaint()


    def getColumnIcons(self):
        """Gets the icons of the columns.

        The icons in headers match the property ids given my the set visible
        column headers. The table must be set in either
        L{COLUMN_HEADER_MODE_EXPLICIT} or
        L{COLUMN_HEADER_MODE_EXPLICIT_DEFAULTS_ID} mode to show the
        headers with icons.

        @return: the array of icons that match the L{getVisibleColumns}.
        """
        if self._columnIcons is None:
            return None

        icons = list()
        for col in self._visibleColumns:
            icons.append( self._columnIcons[col] )

        return icons


    def setColumnIcons(self, columnIcons):
        """Sets the icons of the columns.

        The icons in headers match the property id:s given my the set visible
        column headers. The table must be set in either
        L{COLUMN_HEADER_MODE_EXPLICIT} or
        L{COLUMN_HEADER_MODE_EXPLICIT_DEFAULTS_ID} mode to show the
        headers with icons.

        @param columnIcons: the array of icons that match the
                            L{getVisibleColumns}.
        """
        if len(columnIcons) != len(self._visibleColumns):
            raise ValueError('The length of the icons array must '
                    'match the number of visible columns')

        del self._columnIcons[:]

        # FIXME: realloc array

        for i, col in enumerate(self._visibleColumns):
            self._columnIcons[col] = columnIcons[i]

        # Assure visual refresh
        self.requestRepaint()


    def getColumnAlignments(self):
        """Gets the array of column alignments.

        The items in the array must match the properties identified by
        L{getVisibleColumns}. The possible values for the alignments
        include:

          - L{ALIGN_LEFT}: Left alignment
          - L{ALIGN_CENTER}: Centered
          - L{ALIGN_RIGHT}: Right alignment

        The alignments default to L{ALIGN_LEFT}: any null values are
        rendered as align lefts.

        @return: the column alignments array.
        """
        if self._columnAlignments is None:
            return None

        alignments = list()

        for col in self._visibleColumns:
            alignments.append( self.getColumnAlignment(col) )

        return alignments


    def setColumnAlignments(self, columnAlignments):
        """Sets the column alignments.

        The items in the array must match the properties identified by
        L{getVisibleColumns}. The possible values for the alignments
        include:

          - L{ALIGN_LEFT}: Left alignmen
          - L{ALIGN_CENTER}: Centered
          - L{ALIGN_RIGHT}: Right alignment

        The alignments default to L{ALIGN_LEFT}

        @param columnAlignments:
                   the column alignments array.
        """
        if len(columnAlignments) != len(self._visibleColumns):
            raise ValueError('The length of the alignments array '
                    'must match the number of visible columns')

        # Checks all alignments
        for i, a in enumerate(columnAlignments):
            if ((a is not None)
                    and (a is not self.ALIGN_LEFT)
                    and (a is not self.ALIGN_CENTER)
                    and (a is not self.ALIGN_RIGHT)):
                raise ValueError('Column ' + str(i) + ' aligment \''
                        + a + '\' is invalid')

        # Resets the alignments
        newCA = dict()

        i = 0
        it = iter(self._visibleColumns)
        while i < len(columnAlignments):
            try:
                newCA[ it.next() ] = columnAlignments[i]
                i += 1
            except StopIteration:
                break

        self._columnAlignments = newCA

        # Assures the visual refresh. No need to reset the page buffer before
        # as the content has not changed, only the alignments.
        self.refreshRenderedCells()


    def setColumnWidth(self, propertyId, width):
        """Sets columns width (in pixels). Theme may not necessary respect
        very small or very big values. Setting width to -1 (default) means
        that theme will make decision of width.

        Column can either have a fixed width or expand ratio. The latter one
        set is used. See @link L{setColumnExpandRatio}.

        @param propertyId:
                   colunmns property id
        @param width:
                   width to be reserved for colunmns content
        """
        if propertyId is None:
            # Since propertyId is null, this is the row header. Use the
            # magic id to store the width of the row header.
            propertyId = self._ROW_HEADER_FAKE_PROPERTY_ID

        if width < 0:
            if propertyId in self._columnWidths:
                del self._columnWidths[propertyId]
        else:
            self._columnWidths[propertyId] = int(width)

        self.requestRepaint()


    def setColumnExpandRatio(self, propertyId, expandRatio):
        """Sets the column expand ratio for given column.

        Expand ratios can be defined to customize the way how excess space is
        divided among columns. Table can have excess space if it has its width
        defined and there is horizontally more space than columns consume
        naturally. Excess space is the space that is not used by columns with
        explicit width (see L{setColumnWidth}) or with
        natural width (no width nor expand ratio).

        By default (without expand ratios) the excess space is divided
        proportionally to columns natural widths.

        Only expand ratios of visible columns are used in final calculations.

        Column can either have a fixed width or expand ratio. The latter one
        set is used.

        A column with expand ratio is considered to be minimum width by
        default (if no excess space exists). The minimum width is defined
        by terminal implementation.

        If terminal implementation supports re-sizable columns the column
        becomes fixed width column if users resizes the column.

        @param propertyId:
                   columns property id
        @param expandRatio:
                   the expandRatio used to divide excess space for this column
        """
        if expandRatio < 0:
            if propertyId in self._columnWidths:
                del self._columnWidths[propertyId]
        else:
            self._columnWidths[propertyId] = float(expandRatio)


    def getColumnExpandRatio(self, propertyId):
        width = self._columnWidths.get(propertyId)
        if (width is None) or (not isinstance(width, float)):
            return -1

        return float(width)


    def getColumnWidth(self, propertyId):
        """Gets the pixel width of column

        @return: width of column or -1 when value not set
        """
        if propertyId is None:
            # Since propertyId is null, this is the row header. Use the
            # magic id to retrieve the width of the row header.
            propertyId = self._ROW_HEADER_FAKE_PROPERTY_ID

        width = self._columnWidths.get(propertyId)
        if (width is None) or (not isinstance(width, int)):
            return -1

        return int(width)


    def getPageLength(self):
        """Gets the page length.

        Setting page length 0 disables paging.

        @return: the length of one page.
        """
        return self._pageLength


    def setPageLength(self, pageLength):
        """Sets the page length.

        Setting page length 0 disables paging. The page length defaults to 15.

        If Table has width set (L{setWidth} ) the client
        side may update the page length automatically the correct value.

        @param pageLength:
                   the length of one page.
        """
        if (pageLength >= 0) and (self._pageLength != pageLength):
            self._pageLength = pageLength
            # Assures the visual refresh
            self.refreshRowCache()


    def setCacheRate(self, cacheRate):
        """This method adjusts a possible caching mechanism of table
        implementation.

        Table component may fetch and render some rows outside visible area.
        With complex tables (for example containing layouts and components),
        the client side may become unresponsive. Setting the value lower, UI
        will become more responsive. With higher values scrolling in client
        will hit server less frequently.

        The amount of cached rows will be cacheRate multiplied with pageLength
        L{setPageLength} both below and above visible area.

        @param cacheRate:
                   a value over 0 (fastest rendering time). Higher value will
                   cache more rows on server (smoother scrolling). Default
                   value is 2.
        """
        if cacheRate < 0:
            raise ValueError, 'cacheRate cannot be less than zero'

        if self._cacheRate != cacheRate:
            self._cacheRate = cacheRate
            self.requestRepaint()


    def getCacheRate(self):
        """@see: L{setCacheRate}

        @return: the current cache rate value
        """
        return self._cacheRate


    def getCurrentPageFirstItemId(self):
        """Getter for property currentPageFirstItem.

        @return: the Value of property currentPageFirstItem.
        """
        # Priorise index over id if indexes are supported
        if isinstance(self.items, container.IIndexed):
            index = self.getCurrentPageFirstItemIndex()
            idd = None
            if (index >= 0) and (index < len(self)):
                idd = self.getIdByIndex(index)

            if (idd is not None) and (idd != self._currentPageFirstItemId):
                self._currentPageFirstItemId = idd

        # If there is no item id at all, use the first one
        if self._currentPageFirstItemId is None:
            self._currentPageFirstItemId = self.firstItemId()

        return self._currentPageFirstItemId


    def getIdByIndex(self, index):
        return self.items.getIdByIndex(index)


    def setCurrentPageFirstItemId(self, currentPageFirstItemId):
        """Setter for property currentPageFirstItemId.

        @param currentPageFirstItemId:
                   the new value of property currentPageFirstItemId.
        """
        # Gets the corresponding index
        index = -1
        if isinstance(self.items, container.IIndexed):
            index = self.indexOfId(currentPageFirstItemId)
        else:
            # If the table item container does not have index, we have to
            # calculates the index by hand
            idd = self.firstItemId()
            while (idd is not None) and (idd != currentPageFirstItemId):
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
        self.refreshRowCache()


    def indexOfId(self, itemId):
        return self.items.indexOfId(itemId)


    def getColumnIcon(self, propertyId):
        """Gets the icon Resource for the specified column.

        @param propertyId:
                   the propertyId identifying the column.
        @return: the icon for the specified column; null if the column has
                no icon set, or if the column is not visible.
        """
        return self._columnIcons.get(propertyId)


    def setColumnIcon(self, propertyId, icon):
        """Sets the icon Resource for the specified column.

        Throws ValueError if the specified column is not
        visible.

        @param propertyId:
                   the propertyId identifying the column.
        @param icon:
                   the icon Resource to set.
        """
        if icon is None:
            if propertyId in self._columnIcons:
                del self._columnIcons[propertyId]
        else:
            self._columnIcons[propertyId] = icon

        # Assures the visual refresh
        self.requestRepaint()


    def getColumnHeader(self, propertyId):
        """Gets the header for the specified column.

        @param propertyId:
                   the propertyId identifying the column.
        @return: the header for the specified column if it has one.
        """
        if self.getColumnHeaderMode() == self.COLUMN_HEADER_MODE_HIDDEN:
            return None

        header = self._columnHeaders.get(propertyId)
        if ((header is None
                and self.getColumnHeaderMode() ==
                        self.COLUMN_HEADER_MODE_EXPLICIT_DEFAULTS_ID)
                or (self.getColumnHeaderMode() == self.COLUMN_HEADER_MODE_ID)):
            header = str(propertyId)

        return header


    def setColumnHeader(self, propertyId, header):
        """Sets the column header for the specified column;

        @param propertyId:
                   the propertyId identifying the column.
        @param header:
                   the header to set.
        """
        if header is None:
            if propertyId in self._columnHeaders:
                del self._columnHeaders[propertyId]
        else:
            self._columnHeaders[propertyId] = header

        self.requestRepaint()


    def getColumnAlignment(self, propertyId):
        """Gets the specified column's alignment.

        @param propertyId:
                   the propertyID identifying the column.
        @return: the specified column's alignment if it as one; null otherwise.
        """
        a = self._columnAlignments.get(propertyId)
        return self.ALIGN_LEFT if a is None else a


    def setColumnAlignment(self, propertyId, alignment):
        """Sets the specified column's alignment.

        Throws IllegalArgumentException if the alignment is not one of
        the following: L{ALIGN_LEFT}, L{ALIGN_CENTER} or L{ALIGN_RIGHT}

        @param propertyId:
                   the propertyID identifying the column.
        @param alignment:
                   the desired alignment.
        """
        # Checks for valid alignments
        if (alignment is not None
                and (alignment is not self.ALIGN_LEFT)
                and (alignment is not self.ALIGN_CENTER)
                and (alignment is not self.ALIGN_RIGHT)):
            raise ValueError('Column alignment \'' + alignment
                    + '\' is not supported.')

        if (alignment is None) or (alignment == self.ALIGN_LEFT):
            if propertyId in self._columnAlignments:
                del self._columnAlignments[propertyId]
        else:
            self._columnAlignments[propertyId] = alignment

        # Assures the visual refresh. No need to reset the page buffer before
        # as the content has not changed, only the alignments.
        self.refreshRenderedCells()


    def isColumnCollapsed(self, propertyId):
        """Checks if the specified column is collapsed.

        @param propertyId:
                   the propertyID identifying the column.
        @return: true if the column is collapsed; false otherwise;
        """
        return ((self._collapsedColumns is not None)
                and (propertyId in self._collapsedColumns))


    def setColumnCollapsed(self, propertyId, collapsed):
        """Sets whether the specified column is collapsed or not.

        @param propertyId:
                   the propertyID identifying the column.
        @param collapsed:
                   the desired collapsedness.
        @raise ValueError:
                    if column collapsing is not allowed
        """
        if not self.isColumnCollapsingAllowed():
            raise ValueError, 'Column collapsing not allowed!'

        if collapsed:
            self._collapsedColumns.add(propertyId)
        else:
            if propertyId in self._collapsedColumns:
                self._collapsedColumns.remove(propertyId)

        # Assures the visual refresh
        self.refreshRowCache()


    def isColumnCollapsingAllowed(self):
        """Checks if column collapsing is allowed.

        @return: true if columns can be collapsed; false otherwise.
        """
        return self._columnCollapsingAllowed


    def setColumnCollapsingAllowed(self, collapsingAllowed):
        """Sets whether column collapsing is allowed or not.

        @param collapsingAllowed:
                   specifies whether column collapsing is allowed.
        """
        self._columnCollapsingAllowed = collapsingAllowed

        if not collapsingAllowed:
            self._collapsedColumns.clear()

        # Assures the visual refresh. No need to reset the page buffer before
        # as the content has not changed, only the alignments.
        self.refreshRenderedCells()


    def isColumnReorderingAllowed(self):
        """Checks if column reordering is allowed.

        @return: true if columns can be reordered; false otherwise.
        """
        return self._columnReorderingAllowed


    def setColumnReorderingAllowed(self, columnReorderingAllowed):
        """Sets whether column reordering is allowed or not.

        @param columnReorderingAllowed:
                   specifies whether column reordering is allowed.
        """
        if columnReorderingAllowed != self._columnReorderingAllowed:
            self._columnReorderingAllowed = columnReorderingAllowed
            self.requestRepaint()


    def setColumnOrder(self, columnOrder):
        # Arranges visible columns according to given columnOrder. Silently
        # ignores colimnId:s that are not visible columns, and keeps the
        # internal order of visible columns left out of the ordering
        # (trailing). Silently does nothing if columnReordering is not
        # allowed.
        if (columnOrder is None) or (not self.isColumnReorderingAllowed()):
            return

        newOrder = list()
        for order in columnOrder:
            if (order is not None) and (order in self._visibleColumns):
                self._visibleColumns.remove(order)
                newOrder.append(order)

        for columnId in self._visibleColumns:
            if columnId not in newOrder:
                newOrder.append(columnId)

        self._visibleColumns = newOrder

        # Assure visual refresh
        self.refreshRowCache()


    def getCurrentPageFirstItemIndex(self):
        """Getter for property currentPageFirstItem.

        @return: the Value of property currentPageFirstItem.
        """
        return self._currentPageFirstItemIndex


    def setCurrentPageFirstItemIndex(self, newIndex,
                needsPageBufferReset=True):
        """Setter for property currentPageFirstItem.

        @param newIndex:
                   the New value of property currentPageFirstItem.
        """
        if newIndex < 0:
            newIndex = 0

        # minimize IContainer.size() calls which may be expensive. For
        # example it may cause sql query.
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
        if isinstance(self.items, container.IIndexed):
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
            while ((self._currentPageFirstItemIndex < newIndex)
                    and (not self.isLastId(self._currentPageFirstItemId))):
                self._currentPageFirstItemIndex += 1
                self._currentPageFirstItemId = \
                        self.nextItemId(self._currentPageFirstItemId)

            # If we did hit the border
            if self.isLastId(self._currentPageFirstItemId):
                self._currentPageFirstItemIndex = size - 1

            # Go backwards in the middle of the list (respect borders)
            while ((self._currentPageFirstItemIndex > newIndex)
                    and (not self.isFirstId(self._currentPageFirstItemId))):
                self._currentPageFirstItemIndex -= 1
                self._currentPageFirstItemId = \
                        self.prevItemId(self._currentPageFirstItemId)

            # If we did hit the border
            if self.isFirstId(self._currentPageFirstItemId):
                self._currentPageFirstItemIndex = 0

            # Go forwards once more
            while ((self._currentPageFirstItemIndex < newIndex)
                    and (not self.isLastId(self._currentPageFirstItemId))):
                self._currentPageFirstItemIndex += 1
                self._currentPageFirstItemId = \
                        self.nextItemId(self._currentPageFirstItemId)

            # If for some reason we do hit border again, override
            # the user index request
            if self.isLastId(self._currentPageFirstItemId):
                newIndex = self._currentPageFirstItemIndex = size - 1

        if needsPageBufferReset:
            # Assures the visual refresh
            self.refreshRowCache()


    def isPageBufferingEnabled(self):
        """Getter for property pageBuffering.

        @deprecated: functionality is not needed in ajax rendering model

        @return: the value of property pageBuffering.
        """
        return True


    def setPageBufferingEnabled(self, pageBuffering):
        """Setter for property pageBuffering.

        @deprecated: functionality is not needed in ajax rendering model

        @param pageBuffering:
                   the new value of property pageBuffering.
        """
        warn('functionality is not needed in ajax rendering model',
             DeprecationWarning)


    def isSelectable(self):
        """Getter for property selectable.

        The table is not selectable by default.

        @return: the Value of property selectable.
        """
        return self._selectable


    def setSelectable(self, selectable):
        """Setter for property selectable.

        The table is not selectable by default.

        @param selectable:
                   the new value of property selectable.
        """
        if self._selectable != selectable:
            self._selectable = selectable
            self.requestRepaint()


    def getColumnHeaderMode(self):
        """Getter for property columnHeaderMode.

        @return: the value of property columnHeaderMode.
        """
        return self._columnHeaderMode


    def setColumnHeaderMode(self, columnHeaderMode):
        """Setter for property columnHeaderMode.

        @param columnHeaderMode:
                   the new value of property columnHeaderMode.
        """
        if (columnHeaderMode != self._columnHeaderMode
                and columnHeaderMode >= self.COLUMN_HEADER_MODE_HIDDEN
                and (columnHeaderMode <=
                        self.COLUMN_HEADER_MODE_EXPLICIT_DEFAULTS_ID)):
            self._columnHeaderMode = columnHeaderMode
            self.requestRepaint()


    def refreshRenderedCells(self):
        """Refreshes the rows in the internal cache. Only if
        L{resetPageBuffer} is called before this then all values are
        guaranteed to be recreated.
        """
        if self.getParent() is None:
            return

        if not self._isContentRefreshesEnabled:
            return

        # Collects the basic facts about the table page
        pagelen = self.getPageLength()
        firstIndex = self.getCurrentPageFirstItemIndex()
        rows = totalRows = self.size()
        if (rows > 0) and (firstIndex >= 0):
            rows -= firstIndex

        if (pagelen > 0) and (pagelen < rows):
            rows = pagelen

        # If "to be painted next" variables are set, use them
        if (self._lastToBeRenderedInClient -
                self._firstToBeRenderedInClient > 0):
            rows = (self._lastToBeRenderedInClient -
                        self._firstToBeRenderedInClient) + 1

        if self._firstToBeRenderedInClient >= 0:
            if self._firstToBeRenderedInClient < totalRows:
                firstIndex = self._firstToBeRenderedInClient
            else:
                firstIndex = totalRows - 1
        else:
            # initial load
            self._firstToBeRenderedInClient = firstIndex

        if totalRows > 0:
            if (rows + firstIndex) > totalRows:
                rows = totalRows - firstIndex
        else:
            rows = 0
        # Saves the results to internal buffer
        self._pageBuffer = self.getVisibleCellsNoCache(firstIndex, rows, True)
        if rows > 0:
            self._pageBufferFirstIndex = firstIndex
        self.setRowCacheInvalidated(True)
        self.requestRepaint()


    def requestRepaint(self):
        """Requests that the Table should be repainted as soon as possible.

        Note that a C{Table} does not necessarily repaint its contents when
        this method has been called. See L{refreshRowCache} for forcing an
        update of the contents.
        """
        # Overridden only for doc-string
        super(Table, self).requestRepaint()


    def removeRowsFromCacheAndFillBottom(self, firstIndex, rows):
        totalCachedRows = len(self._pageBuffer[self.CELL_ITEMID])
        totalRows = self.size()
        firstIndexInPageBuffer = firstIndex - self._pageBufferFirstIndex

        # firstIndexInPageBuffer is the first row to be removed. "rows" rows
        # after that should be removed. If the page buffer does not contain
        # that many rows, we only remove the rows that actually are in the page
        # buffer.
        if firstIndexInPageBuffer + rows > totalCachedRows:
            rows = totalCachedRows - firstIndexInPageBuffer

        # Unregister components that will no longer be in the page buffer to
        # make sure that no components leak.
        self.unregisterComponentsAndPropertiesInRows(firstIndex, rows)

        # The number of rows that should be in the cache after this operation
        # is done (pageBuffer currently contains the expanded items).
        newCachedRowCount = totalCachedRows
        if newCachedRowCount + self._pageBufferFirstIndex > totalRows:
            newCachedRowCount = totalRows - self._pageBufferFirstIndex

        # The index at which we should render the first row that does not come
        # from the previous page buffer.
        firstAppendedRowInPageBuffer = totalCachedRows - rows
        firstAppendedRow = \
                firstAppendedRowInPageBuffer + self._pageBufferFirstIndex

        # Calculate the maximum number of new rows that we can add to the page
        # buffer. Less than the rows we removed if the container does not
        # contain that many items afterwards.
        maxRowsToRender = totalRows - firstAppendedRow
        rowsToAdd = rows
        if rowsToAdd > maxRowsToRender:
            rowsToAdd = maxRowsToRender

        cells = None
        if rowsToAdd > 0:
            cells = self.getVisibleCellsNoCache(firstAppendedRow, rowsToAdd,
                    False)

        # Create the new cache buffer by copying the first rows from the old
        # buffer, moving the following rows upwards and appending more rows if
        # applicable.
        pbl = len(self._pageBuffer)
        newPageBuffer = [([None] * newCachedRowCount) for _ in range(pbl)]
        for i in range(pbl):
            for row in range(firstIndexInPageBuffer):
                # Copy the first rows
                newPageBuffer[i][row] = self._pageBuffer[i][row]

            for row in range(firstIndexInPageBuffer,
                    firstAppendedRowInPageBuffer):
                # Move the rows that were after the expanded rows
                newPageBuffer[i][row] = self._pageBuffer[i][row + rows]

            for row in range(firstAppendedRowInPageBuffer, newCachedRowCount):
                # Add the newly rendered rows. Only used if rowsToAdd > 0
                # (cells != null)
                newPageBuffer[i][row] = cells[i][row - firstAppendedRowInPageBuffer]

        self._pageBuffer = newPageBuffer


    def getVisibleCellsUpdateCacheRows(self, firstIndex, rows):
        cells = self.getVisibleCellsNoCache(firstIndex, rows, False)
        cacheIx = firstIndex - self._pageBufferFirstIndex
        # update the new rows in the cache.
        totalCachedRows = len(self._pageBuffer[self.CELL_ITEMID])
        end = min(cacheIx + rows, totalCachedRows)
        for ix in range(cacheIx, end):
            for i in range(len(self._pageBuffer)):
                self._pageBuffer[i][ix] = cells[i][ix - cacheIx]
        return cells


    def getVisibleCellsInsertIntoCache(self, firstIndex, rows):
        """@param firstIndex:
                   The position where new rows should be inserted
        @param rows:
                   The maximum number of rows that should be inserted at
                   position firstIndex. Less rows will be inserted if the
                   page buffer is too small.
        """
        logger.debug(
                'Insert %d rows at index %d to existing page buffer requested'
                % (rows, firstIndex))

        # Page buffer must not become larger than pageLength*cacheRate before
        # or after the current page
        minPageBufferIndex = (self.getCurrentPageFirstItemIndex()
                - (self.getPageLength() * self.getCacheRate()))
        if minPageBufferIndex < 0:
            minPageBufferIndex = 0

        maxPageBufferIndex = (self.getCurrentPageFirstItemIndex()
                + (self.getPageLength() * (1 + self.getCacheRate())))
        maxBufferSize = maxPageBufferIndex - minPageBufferIndex

        if self.getPageLength() == 0:
            # If pageLength == 0 then all rows should be rendered
            maxBufferSize = len(self._pageBuffer[0]) + rows

        # Number of rows that were previously cached. This is not necessarily
        # the same as pageLength if we do not have enough rows in the
        # container.
        currentlyCachedRowCount = len(self._pageBuffer[self.CELL_ITEMID])

        # firstIndexInPageBuffer is the offset in pageBuffer where the new rows
        # will be inserted (firstIndex is the index in the whole table).
        #
        # E.g. scrolled down to row 1000: firstIndex==1010,
        # pageBufferFirstIndex==1000 -> cacheIx==10
        firstIndexInPageBuffer = firstIndex - self._pageBufferFirstIndex

        # If rows > size available in page buffer
        if firstIndexInPageBuffer + rows > maxBufferSize:
            rows = maxBufferSize - firstIndexInPageBuffer

        # "rows" rows will be inserted at firstIndex. Find out how many old
        # rows fall outside the new buffer so we can unregister components in
        # the cache.

        # All rows until the insertion point remain, always.
        firstCacheRowToRemoveInPageBuffer = firstIndexInPageBuffer

        # IF there is space remaining in the buffer after the rows have been
        # inserted, we can keep more rows.

        numberOfOldRowsAfterInsertedRows = (maxBufferSize
                - firstIndexInPageBuffer - rows)
        if numberOfOldRowsAfterInsertedRows > 0:
            firstCacheRowToRemoveInPageBuffer += \
                    numberOfOldRowsAfterInsertedRows

        if firstCacheRowToRemoveInPageBuffer <= currentlyCachedRowCount:
            # Unregister all components that fall beyond the cache limits after
            # inserting the new rows.
            self.unregisterComponentsAndPropertiesInRows(
                    firstCacheRowToRemoveInPageBuffer
                            + self._pageBufferFirstIndex,
                    (currentlyCachedRowCount
                            - firstCacheRowToRemoveInPageBuffer)
                            + self._pageBufferFirstIndex)

        # Calculate the new cache size
        newCachedRowCount = currentlyCachedRowCount
        if (maxBufferSize == 0) or (currentlyCachedRowCount < maxBufferSize):
            newCachedRowCount = currentlyCachedRowCount + rows
            if maxBufferSize > 0 and newCachedRowCount > maxBufferSize:
                newCachedRowCount = maxBufferSize

        # Paint the new rows into a separate buffer
        cells = self.getVisibleCellsNoCache(firstIndex, rows, False)

        # Create the new cache buffer and fill it with the data from the old
        # buffer as well as the inserted rows.

        pbl = len(self._pageBuffer)
        newPageBuffer = [([None] * newCachedRowCount) for _ in range(pbl)]

        for i in range(pbl):
            for row in range(firstIndexInPageBuffer):
                # Copy the first rows
                newPageBuffer[i][row] = self._pageBuffer[i][row]

            for row in range(firstIndexInPageBuffer,
                    firstIndexInPageBuffer + rows):
                # Copy the newly created rows
                newPageBuffer[i][row] = cells[i][row - firstIndexInPageBuffer]

            for row in range(firstIndexInPageBuffer + rows, newCachedRowCount):
                # Move the old rows down below the newly inserted rows
                newPageBuffer[i][row] = self._pageBuffer[i][row - rows]

        self._pageBuffer = newPageBuffer

        logger.debug('Page Buffer now contains %d rows (%d - %d)' %
                (len(self._pageBuffer[self.CELL_ITEMID]),
                 self._pageBufferFirstIndex,
                 (self._pageBufferFirstIndex
                        + len(self._pageBuffer[self.CELL_ITEMID]) - 1)))

        return cells


    def getVisibleCellsNoCache(self, firstIndex, rows, replaceListeners):
        """Render rows with index "firstIndex" to "firstIndex+rows-1" to a new
        buffer.

        Reuses values from the current page buffer if the rows are found there.
        """
        logger.debug('Render visible cells for rows %d - %d' %
                (firstIndex, (firstIndex + rows - 1)))
        colids = self.getVisibleColumns()
        cols = len(colids)

        oldListenedProperties = self._listenedProperties
        oldVisibleComponents = self._visibleComponents

        if replaceListeners:
            # initialize the listener collections, this should only be done if
            # the entire cache is refreshed (through refreshRenderedCells)
            self._listenedProperties = set()
            self._visibleComponents = set()

        cells = [([None] * rows) for _ in range(cols + self.CELL_FIRSTCOL)]
        if rows == 0:
            self.unregisterPropertiesAndComponents(oldListenedProperties,
                    oldVisibleComponents)
            return cells

        # Gets the first item id
        if isinstance(self.items, container.IIndexed):
            idd = self.getIdByIndex(firstIndex)
        else:
            idd = self.firstItemId()
            for i in range(firstIndex):
                idd = self.nextItemId(idd)

        headmode = self.getRowHeaderMode()
        iscomponent = [None] * cols
        for i in range(cols):
            iscomponent[i] = ((colids[i] in self._columnGenerators)
                    or issubclass(self.getType(colids[i]), IComponent))

        if (self._pageBuffer is not None
                and len(self._pageBuffer[self.CELL_ITEMID]) > 0):
            firstIndexNotInCache = (self._pageBufferFirstIndex
                    + len(self._pageBuffer[self.CELL_ITEMID]))
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

            if self._rowGenerator is not None:
                generatedRow = self._rowGenerator.generateRow(self, idd)
            else:
                generatedRow =  None
            cells[self.CELL_GENERATED_ROW][i] = generatedRow

            for j in range(cols):
                if self.isColumnCollapsed(colids[j]):
                    continue
                p = None
                value = ''
                isGeneratedRow = generatedRow is not None
                isGeneratedColumn = colids[j] in self._columnGenerators
                isGenerated = isGeneratedRow or isGeneratedColumn

                if not isGenerated:
                    p = self.getContainerProperty(idd, colids[j])

                if isGeneratedRow:
                    if generatedRow.isSpanColumns() and j > 0:
                        value = None
                    elif (generatedRow.isSpanColumns() and j == 0
                            and isinstance(generatedRow.getValue(),IComponent)):
                        value = generatedRow.getValue()
                    elif len(generatedRow.getText()) > j:
                        value = generatedRow.getText()[j]
                else:
                    # check in current pageBuffer already has row
                    index = firstIndex + i
                    if (p is not None) or isGenerated:
                        indexInOldBuffer = index - self._pageBufferFirstIndex
                        if (index < firstIndexNotInCache
                                and index >= self._pageBufferFirstIndex
                                and self._pageBuffer[self.CELL_GENERATED_ROW][indexInOldBuffer] is None
                                and self._pageBuffer[self.CELL_ITEMID][indexInOldBuffer] == idd):
                            # we already have data in our cache,
                            # recycle it instead of fetching it via
                            # getValue/getPropertyValue
                            value = self._pageBuffer[self.CELL_FIRSTCOL + j][indexInOldBuffer]
                            if (not isGeneratedColumn and iscomponent[j]
                                    or (not isinstance(value, IComponent))):
                                self.listenProperty(p, oldListenedProperties)
                        elif isGeneratedColumn:
                            cg = self._columnGenerators[colids[j]]
                            value = cg.generateCell(self, idd, colids[j])
                            if (value is not None
                                    and not isinstance(value, IComponent)
                                    and not isinstance(value, basestring)):
                                # Avoid errors if a generator returns
                                # something other than a Component or a string
                                value = str(value)
                        elif iscomponent[j]:
                            value = p.getValue()
                            self.listenProperty(p, oldListenedProperties)
                        elif p is not None:
                            value = self.getPropertyValue(idd, colids[j], p)
                            # If returned value is Component (via
                            # fieldfactory or overridden getPropertyValue)
                            # we excpect it to listen property value
                            # changes. Otherwise if property emits value
                            # change events, table will start to listen
                            # them and refresh content when needed.
                            if not isinstance(value, IComponent):
                                self.listenProperty(p, oldListenedProperties)
                        else:
                            value = self.getPropertyValue(idd, colids[j], None)

                if isinstance(value, IComponent):
                    self.registerComponent(value)

                cells[self.CELL_FIRSTCOL + j][i] = value

            # Gets the next item id
            if isinstance(self.items, container.IIndexed):
                index = firstIndex + i + 1
                if index < self.size():
                    idd = self.getIdByIndex(index)
                else:
                    idd = None
            else:
                idd = self.nextItemId(idd)

            filledRows += 1
            i += 1

        # Assures that all the rows of the cell-buffer are valid
        if filledRows != len(cells[0]):
            temp = [[None] * filledRows] * len(cells)
            for i in range(len(cells)):
                for j in range(filledRows):
                    temp[i][j] = cells[i][j]
            cells = temp

        self.unregisterPropertiesAndComponents(oldListenedProperties,
                oldVisibleComponents)

        return cells


    def registerComponent(self, component):
        #logger.debug('Registered %s: %s' % (component.__class__.__name__,
        #        component.getCaption()))
        if component.getParent() is not self:
            component.setParent(self)
        self._visibleComponents.add(component)


    def listenProperty(self, p, oldListenedProperties):
        if isinstance(p, IValueChangeNotifier):
            if ((oldListenedProperties is None)
                    or (p not in oldListenedProperties)):
                p.addListener(self, IValueChangeListener)

            # register listened properties, so we can do proper cleanup to
            # free memory. Essential if table has loads of data and it is
            # used for a long time.
            self._listenedProperties.add(p)


    def unregisterComponentsAndPropertiesInRows(self, firstIx, count):
        """@param firstIx:
                  Index of the first row to process. Global index, not
                  relative to page buffer.
        @param count:
        """
        logger.debug("Unregistering components in rows %d - %d" %
                (firstIx, (firstIx + count - 1)))
        colids = self.getVisibleColumns()
        if (self._pageBuffer is not None
                and len(self._pageBuffer[self.CELL_ITEMID]) > 0):
            bufSize = len(self._pageBuffer[self.CELL_ITEMID])
            ix = firstIx - self._pageBufferFirstIndex
            ix = 0 if ix < 0 else ix
            if ix < bufSize:
                count = bufSize - ix if count > bufSize - ix else count
                for i in range(count):
                    for c in range(len(colids)):
                        col = self.CELL_FIRSTCOL + c
                        cellVal = self._pageBuffer[col][i + ix]
                        if (isinstance(cellVal, IComponent)
                                and cellVal in self._visibleComponents):
                            self._visibleComponents.remove(cellVal)
                            self.unregisterComponent(cellVal)
                        else:
                            r = self._pageBuffer[self.CELL_ITEMID][i + ix]
                            p = self.getContainerProperty(r, colids[c])
                            if (isinstance(p, IValueChangeNotifier)
                                    and p in self._listenedProperties):
                                self._listenedProperties.remove(p)
                                p.removeListener(self)


    def unregisterPropertiesAndComponents(self, oldListenedProperties,
                oldVisibleComponents):
        """Helper method to remove listeners and maintain correct component
        hierarchy. Detaches properties and components if those are no more
        rendered in client.

        @param oldListenedProperties:
                   set of properties that where listened in last render
        @param oldVisibleComponents:
                   set of components that where attached in last render
        """
        if oldVisibleComponents is not None:
            for c in oldVisibleComponents:
                if  c not in self._visibleComponents:
                    self.unregisterComponent(c)

        if oldListenedProperties is not None:
            for o in oldListenedProperties:
                if o not in self._listenedProperties:
                    o.removeListener(self, IValueChangeListener)


    def unregisterComponent(self, component):
        """This method cleans up a IComponent that has been generated when
        Table is in editable mode. The component needs to be detached from
        its parent and if it is a field, it needs to be detached from its
        property data source in order to allow garbage collection to take
        care of removing the unused component from memory.

        Override this method and C{getPropertyValue}
        with custom logic if you need to deal with buffered fields.

        @see: L{getPropertyValue}

        @param component:
                   a set of components that should be unregistered.
        """
        #logger.debug("Unregistered %s: %s" % (component.__class__.__name__,
        #        component.getCaption()))
        component.setParent(None)
        # Also remove property data sources to unregister listeners keeping
        # the fields in memory.
        if isinstance(component, IField):
            field = component
            associatedProperty = \
                    self._associatedProperties.pop(component, None)
            if (associatedProperty is not None
                    and field.getPropertyDataSource() == associatedProperty):
                # Remove the property data source only if it's the one we
                # added in getPropertyValue
                field.setPropertyDataSource(None)


    def refreshCurrentPage(self):
        """Refreshes the current page contents.

        @deprecated: should not need to be used
        """
        warn('should not need to be used', DeprecationWarning)


    def setRowHeaderMode(self, mode):
        """Sets the row header mode.

        The mode can be one of the following ones:

          - L{ROW_HEADER_MODE_HIDDEN}: The row captions are hidden.
          - L{ROW_HEADER_MODE_ID}: Items Id-objects C{__str__}
            is used as row caption.
          - L{ROW_HEADER_MODE_ITEM}: Item-objects C{__str__}
            is used as row caption.
          - L{ROW_HEADER_MODE_PROPERTY}: Property set with
            L{setItemCaptionPropertyId} is used as row header.
          - L{ROW_HEADER_MODE_EXPLICIT_DEFAULTS_ID}: Items Id-objects
            C{__str__} is used as row header. If caption is explicitly
            specified, it overrides the id-caption.
          - L{ROW_HEADER_MODE_EXPLICIT}: The row headers must be explicitly
            specified.
          - L{ROW_HEADER_MODE_INDEX}: The index of the item is used as row
            caption. The index mode can only be used with the containers
            implementing C{container.IIndexed} interface.

        The default value is L{ROW_HEADER_MODE_HIDDEN}

        @param mode:
                   the one of the modes listed above.
        """
        if self.ROW_HEADER_MODE_HIDDEN == mode:
            self._rowCaptionsAreHidden = True
        else:
            self._rowCaptionsAreHidden = False
            self.setItemCaptionMode(mode)

        # Assures the visual refresh. No need to reset the page buffer before
        # as the content has not changed, only the alignments.
        self.refreshRenderedCells()


    def getRowHeaderMode(self):
        """Gets the row header mode.

        @return: the row header mode.
        @see: L{setRowHeaderMode}
        """
        if self._rowCaptionsAreHidden:
            return self.ROW_HEADER_MODE_HIDDEN
        else:
            return self.getItemCaptionMode()


    def addItem(self, *args):
        """Adds the new row to table and fill the visible cells (except
        generated columns) with given values.

        @param args: tuple of the form
            - (cells, itemId)
              1. the Object array that is used for filling the visible
                 cells new row. The types must be settable to visible
                 column property types.
              2. the Id the new row. If null, a new id is automatically
                 assigned. If given, the table cant already have a item
                 with given id.
        @return: Returns item id for the new row. Returns null if operation
                 fails.
        """
        nargs = len(args)
        if nargs < 2:
            return super(Table, self).addItem(*args)
        elif nargs == 2:
            cells, itemId = args
            # remove generated columns from the list of columns being assigned
            availableCols = list()
            for idd in self._visibleColumns:
                if  idd not in self._columnGenerators:
                    availableCols.append(idd)

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
                item.getItemProperty( availableCols[i] ).setValue(cells[i])

            if not isinstance(self.items, container.IItemSetChangeNotifier):
                self.refreshRowCache()

            return itemId
        else:
            raise ValueError, 'too many arguments'


    def refreshRowCache(self):
        """Discards and recreates the internal row cache. Call this if you make
        changes that affect the rows but the information about the changes are
        not automatically propagated to the Table.

        Do not call this e.g. if you have updated the data model through a
        Property. These types of changes are automatically propagated to the
        Table.

        A typical case when this is needed is if you update a generator (e.g.
        CellStyleGenerator) and want to ensure that the rows are redrawn with
        new styles.

        I{Note that calling this method is not cheap so avoid calling it
        unnecessarily.}
        """
        self.resetPageBuffer()
        self.refreshRenderedCells()


    def setContainerDataSource(self, newDataSource):

        self.disableContentRefreshing()

        if newDataSource is None:
            newDataSource = IndexedContainer()

        # Assures that the data source is ordered by making unordered
        # containers ordered by wrapping them
        if isinstance(newDataSource, container.IOrdered):
            super(Table, self).setContainerDataSource(newDataSource)
        else:
            raise NotImplementedError
            #super(Table, self).setContainerDataSource(
            #    ContainerOrderedWrapper(newDataSource) )

        # Resets page position
        self._currentPageFirstItemId = None
        self._currentPageFirstItemIndex = 0

        # Resets column properties
        if self._collapsedColumns is not None:
            self._collapsedColumns.clear()

        # columnGenerators 'override' properties, don't add
        # the same id twice
        col = list()
        for idd in self.getContainerPropertyIds():
            if (self._columnGenerators is None
                    or idd not in self._columnGenerators):
                col.append(idd)

        # generators added last
        if (self._columnGenerators is not None
                and len(self._columnGenerators) > 0):
            col.extend(self._columnGenerators.keys())

        self.setVisibleColumns(col)

        # Assure visual refresh
        self.resetPageBuffer()

        self.enableContentRefreshing(True)


    def getItemIdsInRange(self, itemId, length):
        """Gets items ids from a range of key values
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

        @param variables:
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
            newValue = newValue.difference(renderedItemIds)

        # Then add (possibly some of them back) rows that are currently
        # selected on the client side (the ones that the client side is aware
        # of).
        for i in range(len(ka)):
            # key to id
            idd = self.itemIdMapper.get( ka[i] )
            if (not self.isNullSelectionAllowed()
                    and (idd is None)
                    or (idd == self.getNullSelectionItemId())):
                # skip empty selection if nullselection is not allowed
                self.requestRepaint()
            elif idd is not None and self.containsId(idd):
                newValue.add(idd)

        # Add range items aka shift clicked multiselection areas
        if ranges is not None:
            for rnge in ranges:
                if len(rnge) > 0:
                    split = rnge.split('-')
                    startItemId = self.itemIdMapper.get(split[0])
                    length = int(split[1])
                    ids = self.getItemIdsInRange(startItemId, length)
                    newValue.update(ids)

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

    # IComponent basics

    def changeVariables(self, source, variables):
        """Invoked when the value of a variable has changed.

        @see: L{Select.changeVariables}
        """
        clientNeedsContentRefresh = False

        self.handleClickEvent(variables)

        self.handleColumnResizeEvent(variables)

        self.handleColumnWidthUpdates(variables)

        self.disableContentRefreshing()

        if not self.isSelectable() and 'selected' in variables:
            # Not-selectable is a special case, AbstractSelect does not
            # support. TODO could be optimized.
            variables = dict(variables)
            del variables['selected']

        # The AbstractSelect cannot handle the multiselection properly,
        # instead we handle it ourself
        elif (self.isSelectable()
                and self.isMultiSelect()
                and 'selected' in variables
                and self._multiSelectMode == MultiSelectMode.DEFAULT):
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
                self._firstToBeRenderedInClient = \
                        variables.get('firstToBeRendered')
                self._lastToBeRenderedInClient = \
                        variables.get('lastToBeRendered')
            except Exception:
                # FIXME: Handle exception
                logger.info('Could not parse the first and/or last rows.')

            # respect suggested rows only if table is not otherwise
            # updated (row caches emptied by other event)
            if not self._containerChangeToBeRendered:
                value = variables.get('reqfirstrow')
                if value is not None:
                    self._reqFirstRowToPaint = int(value)
                value = variables.get('reqrows')
                if value is not None:
                    self._reqRowsToPaint = int(value)
                    # sanity check
                    if (self._reqFirstRowToPaint
                            + self._reqRowsToPaint > self.size()):
                        self._reqRowsToPaint = \
                                self.size() - self._reqFirstRowToPaint

            logger.debug("Client wants rows %d - %d" %
                    (self._reqFirstRowToPaint,
                    (self._reqFirstRowToPaint + self._reqRowsToPaint - 1)))
            clientNeedsContentRefresh = True

        if not self._sortDisabled:
            # Sorting
            doSort = False
            if 'sortcolumn' in variables:
                colId = variables.get('sortcolumn')
                if (colId is not None
                        and not ('' == colId)
                        and not ('null' == colId)):
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
                        idd = self._columnIdMap.get( str(ids[i]) )
                        self.setColumnCollapsed(idd, True)
                except Exception:
                    # FIXME: Handle exception
                    logger.info('Could not determine column collapsing state')

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
                    logger.info('Could not determine column reordering state')

                clientNeedsContentRefresh = True

        self.enableContentRefreshing(clientNeedsContentRefresh)

        # Actions
        if 'action' in variables:
            st = variables.get('action').split(',')  # FIXME: StringTokenizer
            if len(st) == 2:
                itemId = self.itemIdMapper.get(st[0].strip())
                action = self._actionMapper.get(st[1].strip())
                if (action is not None
                        and (itemId is None)
                        or self.containsId(itemId)
                        and self._actionHandlers is not None):
                    for ah in self._actionHandlers:
                        ah.handleAction(action, self, itemId)


    def handleClickEvent(self, variables):
        """Handles click event.
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
                event = ItemClickEvent(self, item, itemId, propertyId, evt)
                self.fireEvent(event)

        # Header click event
        elif 'headerClickEvent' in variables:
            details = MouseEventDetails.deSerialize(
                    variables.get('headerClickEvent'))
            cid = variables.get('headerClickCID')
            propertyId = None
            if cid is not None:
                propertyId = self._columnIdMap.get(str(cid))
            self.fireEvent( HeaderClickEvent(self, propertyId, details) )

        # Footer click event
        elif 'footerClickEvent' in variables:
            details = MouseEventDetails.deSerialize(
                    variables.get('footerClickEvent'))
            cid = variables.get('footerClickCID')
            propertyId = None
            if cid is not None:
                propertyId = self._columnIdMap.get(str(cid))
            self.fireEvent( FooterClickEvent(self, propertyId, details) )


    def handleColumnResizeEvent(self, variables):
        """Handles the column resize event sent by the client.
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

                self.fireColumnResizeEvent(propertyId, previousWidth,
                        currentWidth)


    def fireColumnResizeEvent(self, propertyId, previousWidth, currentWidth):
        # Update the sizes on the server side. If a column previously had a
        # expand ratio and the user resized the column then the expand ratio
        # will be turned into a static pixel size.
        self.setColumnWidth(propertyId, currentWidth)

        evt = ColumnResizeEvent(self, propertyId, previousWidth, currentWidth)
        self.fireEvent(evt)


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
        """Go to mode where content updates are not done. This is due we want
        to bypass expensive content for some reason (like when we know we may
        have other content changes on their way).

        @return: true if content refresh flag was enabled prior this call
        """
        wasDisabled = self._isContentRefreshesEnabled
        self._isContentRefreshesEnabled = False
        return wasDisabled


    def enableContentRefreshing(self, refreshContent):
        """Go to mode where content content refreshing has effect.

        @param refreshContent:
                   true if content refresh needs to be done
        """
        self._isContentRefreshesEnabled = True
        if refreshContent:
            self.refreshRenderedCells()
            # Ensure that client gets a response
            self.requestRepaint()


    def paintContent(self, target):
        # Body actions - Actions which has the target null and can be invoked
        # by right clicking on the table body.
        actionSet = self.findAndPaintBodyActions(target)

        cells = self.getVisibleCells()
        rows = self.findNumRowsToPaint(target, cells)

        total = self.size()
        if self.shouldHideNullSelectionItem():
            total -= 1
            rows -= 1

        # Table attributes
        self.paintTableAttributes(target, rows, total)

        self.paintVisibleColumnOrder(target)

        # Rows
        if (self.isPartialRowUpdate() and self._painted
                and not target.isFullRepaint()):
            self.paintPartialRowUpdate(target, actionSet)
            # Send the page buffer indexes to ensure that the client side stays
            # in sync. Otherwise we _might_ have the situation where the client
            # side discards too few or too many rows, causing out of sync
            # issues.
            #
            # This could probably be done for full repaints also to simplify
            # the client side.
            pageBufferLastIndex = (self._pageBufferFirstIndex
                    + self._pageBuffer[self.CELL_ITEMID].length) - 1
            target.addAttribute(VScrollTable.ATTRIBUTE_PAGEBUFFER_FIRST,
                    self._pageBufferFirstIndex)
            target.addAttribute(VScrollTable.ATTRIBUTE_PAGEBUFFER_LAST,
                    pageBufferLastIndex)
        elif target.isFullRepaint() or self.isRowCacheInvalidated():
            self.paintRows(target, cells, actionSet)
            self.setRowCacheInvalidated(False)

        self.paintSorting(target)

        self.resetVariablesAndPageBuffer(target)

        # Actions
        self.paintActions(target, actionSet)

        self.paintColumnOrder(target)

        # Available columns
        self.paintAvailableColumns(target)

        self.paintVisibleColumns(target)

        if self._dropHandler is not None:
            self._dropHandler.getAcceptCriterion().paint(target)

        self._painted = True


    def setRowCacheInvalidated(self, invalidated):
        self._rowCacheInvalidated = invalidated


    def isRowCacheInvalidated(self):
        return self._rowCacheInvalidated


    def paintPartialRowUpdate(self, target, actionSet):
        self.paintPartialRowUpdates(target, actionSet)
        self.paintPartialRowAdditions(target, actionSet)


    def paintPartialRowUpdates(self, target, actionSet):
        iscomponent = self.findCellsWithComponents()

        firstIx = self.getFirstUpdatedItemIndex()
        count = self.getUpdatedRowCount()

        target.startTag('urows')
        target.addAttribute('firsturowix', firstIx)
        target.addAttribute('numurows', count)

        # Partial row updates bypass the normal caching mechanism.
        cells = self.getVisibleCellsUpdateCacheRows(firstIx, count)
        for indexInRowbuffer in range(count):
            itemId = cells[self.CELL_ITEMID][indexInRowbuffer]

            if self.shouldHideNullSelectionItem():
                # Remove null selection item if null selection is not allowed
                continue

            self.paintRow(target, cells, self.isEditable(), actionSet,
                    iscomponent, indexInRowbuffer, itemId)

        target.endTag('urows')


    def paintPartialRowAdditions(self, target, actionSet):
        iscomponent = self.findCellsWithComponents()

        firstIx = self.getFirstAddedItemIndex()
        count = self.getAddedRowCount()

        target.startTag('prows')

        if not self.shouldHideAddedRows():
            logger.debug('Paint rows for add. Index: %d, count: %d.' %
                    (firstIx, count))

            # Partial row additions bypass the normal caching mechanism.
            cells = self.getVisibleCellsInsertIntoCache(firstIx, count)
            if len(cells[0]) < count:
                # delete the rows below, since they will fall beyond the cache
                # page.
                target.addAttribute('delbelow', True)
                count = len(cells[0])

            for indexInRowbuffer in range(count):
                itemId = cells[self.CELL_ITEMID][indexInRowbuffer]
                if self.shouldHideNullSelectionItem():
                    # Remove null selection item if null selection is not
                    # allowed
                    continue

                self.paintRow(target, cells, self.isEditable(), actionSet,
                        iscomponent, indexInRowbuffer, itemId)
        else:
            logger.debug('Paint rows for remove. Index: %d, count: %d.' %
                    (firstIx, count))
            self.removeRowsFromCacheAndFillBottom(firstIx, count)
            target.addAttribute('hide', True)

        target.addAttribute('firstprowix', firstIx)
        target.addAttribute('numprows', count)
        target.endTag('prows')


    def isPartialRowUpdate(self):
        """Subclass and override this to enable partial row updates and
        additions, which bypass the normal caching mechanism. This is useful
        for e.g. TreeTable.

        @return: true if this update is a partial row update, false if not.
                 For plain Table it is always false.
        """
        return False


    def getFirstAddedItemIndex(self):
        """Subclass and override this to enable partial row additions,
        bypassing the normal caching mechanism. This is useful for e.g.
        TreeTable, where expanding a node should only fetch and add the
        items inside of that node.

        @return: The index of the first added item. For plain Table it
                 is always 0.
        """
        return 0


    def getAddedRowCount(self):
        """Subclass and override this to enable partial row additions,
        bypassing the normal caching mechanism. This is useful for e.g.
        TreeTable, where expanding a node should only fetch and add the
        items inside of that node.

        @return: the number of rows to be added, starting at the index
                 returned by L{getFirstAddedItemIndex}. For plain Table
                 it is always 0.
        """
        return 0


    def shouldHideAddedRows(self):
        """Subclass and override this to enable removing of rows, bypassing
        the normal caching and lazy loading mechanism. This is useful for e.g.
        TreeTable, when you need to hide certain rows as a node is collapsed.

        This should return true if the rows pointed to by
        L{getFirstAddedItemIndex} and L{getAddedRowCount} should be hidden
        instead of added.

        @return: whether the rows to add (see L{getFirstAddedItemIndex}
                 and L{getAddedRowCount}) should be added or hidden. For
                 plain Table it is always false.
        """
        return False


    def getFirstUpdatedItemIndex(self):
        """Subclass and override this to enable partial row updates, bypassing
        the normal caching and lazy loading mechanism. This is useful for
        updating the state of certain rows, e.g. in the TreeTable the collapsed
        state of a single node is updated using this mechanism.

        @return: the index of the first item to be updated. For plain Table it
                 is always 0.
        """
        return 0


    def getUpdatedRowCount(self):
        """Subclass and override this to enable partial row updates, bypassing
        the normal caching and lazy loading mechanism. This is useful for
        updating the state of certain rows, e.g. in the TreeTable the collapsed
        state of a single node is updated using this mechanism.

        @return: the number of rows to update, starting at the index returned
                 by L{getFirstUpdatedItemIndex}. For plain table it is always
                 0.
        """
        return 0


    def paintTableAttributes(self, target, rows, total):
        self.paintTabIndex(target)
        self.paintDragMode(target)
        self.paintSelectMode(target)

        if self._cacheRate != self._CACHE_RATE_DEFAULT:
            target.addAttribute('cr', self._cacheRate)

        target.addAttribute('cols', len(self.getVisibleColumns()))
        target.addAttribute('rows', rows)

        if self._reqFirstRowToPaint >= 0:
            target.addAttribute('firstrow', self._reqFirstRowToPaint)
        else:
            target.addAttribute('firstrow', self._firstToBeRenderedInClient)

        target.addAttribute('totalrows', total)

        if self.getPageLength() != 0:
            target.addAttribute('pagelength', self.getPageLength())

        if self.areColumnHeadersEnabled():
            target.addAttribute('colheaders', True)

        if self.rowHeadersAreEnabled():
            target.addAttribute('rowheaders', True)

        target.addAttribute('colfooters', self._columnFootersVisible)

        # The cursors are only shown on pageable table
        if ((self.getCurrentPageFirstItemIndex() != 0)
                or (self.getPageLength() > 0)):
            target.addVariable(self, 'firstvisible',
                    self.getCurrentPageFirstItemIndex())


    def resetVariablesAndPageBuffer(self, target):
        """Resets and paints "to be painted next" variables. Also reset
        pageBuffer"""
        self._reqFirstRowToPaint = -1
        self._reqRowsToPaint = -1
        self._containerChangeToBeRendered = False
        target.addVariable(self, 'reqrows', self._reqRowsToPaint)
        target.addVariable(self, 'reqfirstrow', self._reqFirstRowToPaint)


    def areColumnHeadersEnabled(self):
        return self.getColumnHeaderMode() != self.COLUMN_HEADER_MODE_HIDDEN


    def paintVisibleColumns(self, target):
        target.startTag('visiblecolumns')
        if self.rowHeadersAreEnabled():
            target.startTag('column')
            target.addAttribute('cid', self._ROW_HEADER_COLUMN_KEY)
            self.paintColumnWidth(target, self._ROW_HEADER_FAKE_PROPERTY_ID)
            target.endTag('column')

        sortables = self.getSortableContainerPropertyIds()
        for colId in self._visibleColumns:
            if colId is not None:
                target.startTag('column')
                target.addAttribute('cid', self._columnIdMap.key(colId))

                head = self.getColumnHeader(colId)
                if head is not None:
                    target.addAttribute('caption', head)
                else:
                    target.addAttribute('caption', '')

                foot = self.getColumnFooter(colId)
                if foot is not None:
                    target.addAttribute('fcaption', foot)
                else:
                    target.addAttribute('fcaption', '')

                if self.isColumnCollapsed(colId):
                    target.addAttribute('collapsed', True)

                if self.areColumnHeadersEnabled():
                    if self.getColumnIcon(colId) is not None:
                        target.addAttribute('icon', self.getColumnIcon(colId))
                    if colId in sortables:
                        target.addAttribute('sortable', True)

                if not (self.ALIGN_LEFT == self.getColumnAlignment(colId)):
                    target.addAttribute('align', self.getColumnAlignment(colId))

                self.paintColumnWidth(target, colId)
                target.endTag('column')
        target.endTag('visiblecolumns')


    def paintAvailableColumns(self, target):
        if self._columnCollapsingAllowed:
            collapsedCols = set()
            for colId in self._visibleColumns:
                if self.isColumnCollapsed(colId):
                    collapsedCols.add(colId)

            collapsedKeys = [None] * len(collapsedCols)
            nextColumn = 0
            for colId in self._visibleColumns:
                if self.isColumnCollapsed(colId):
                    collapsedKeys[nextColumn] = self._columnIdMap.key(colId)
                    nextColumn += 1
            target.addVariable(self, 'collapsedcolumns', collapsedKeys)


    def paintActions(self, target, actionSet):
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


    def paintColumnOrder(self, target):
        if self._columnReorderingAllowed:
            colorder = [None] * len(self._visibleColumns)
            i = 0
            for colId in self._visibleColumns:
                colorder[i] = self._columnIdMap.key(colId)
                i += 1
            target.addVariable(self, 'columnorder', colorder)


    def paintSorting(self, target):
        # Sorting
        if isinstance(self.getContainerDataSource(), container.ISortable):
            target.addVariable(self, 'sortcolumn',
                    self._columnIdMap.key(self._sortContainerPropertyId))
            target.addVariable(self, 'sortascending', self._sortAscending)


    def paintRows(self, target, cells, actionSet):
        iscomponent = self.findCellsWithComponents()

        target.startTag('rows')
        # cells array contains all that are supposed to be visible on client,
        # but we'll start from the one requested by client
        start = 0
        if (self._reqFirstRowToPaint != -1
                and self._firstToBeRenderedInClient != -1):
            start = self._reqFirstRowToPaint - self._firstToBeRenderedInClient

        end = len(cells[0])
        if self._reqRowsToPaint != -1:
            end = start + self._reqRowsToPaint

        # sanity check
        if (self._lastToBeRenderedInClient != -1
                and self._lastToBeRenderedInClient < end):
            end = self._lastToBeRenderedInClient + 1

        if (start > len(cells[self.CELL_ITEMID])) or (start < 0):
            start = 0

        for indexInRowbuffer in range(start, end):
            itemId = cells[self.CELL_ITEMID][indexInRowbuffer]

            if self.shouldHideNullSelectionItem():
                # Remove null selection item if null selection is not allowed
                continue

            self.paintRow(target, cells, self.isEditable(), actionSet,
                    iscomponent, indexInRowbuffer, itemId)

        target.endTag('rows')


    def findCellsWithComponents(self):
        isComponent = [None] * len(self._visibleColumns)
        ix = 0
        for columnId in self._visibleColumns:
            if columnId in self._columnGenerators:
                isComponent[ix] = True
                ix += 1
            else:
                colType = self.getType(columnId)
                isComponent[ix] = (colType is not None
                        and issubclass(colType, IComponent))
                ix += 1
        return isComponent


    def paintVisibleColumnOrder(self, target):
        # Visible column order
        visibleColOrder = list()
        for columnId in self._visibleColumns:
            if not self.isColumnCollapsed(columnId):
                visibleColOrder.append(self._columnIdMap.key(columnId))
        target.addAttribute('vcolorder', list(visibleColOrder))


    def findAndPaintBodyActions(self, target):
        actionSet = set()
        if self._actionHandlers is not None:
            keys = list()
            for ah in self._actionHandlers:
                # Getting actions for the null item, which in this case means
                # the body item
                actions = ah.getActions(None, self)
                if actions is not None:
                    for action in actions:
                        actionSet.add(action)
                        keys.append(self._actionMapper.key(action))

            target.addAttribute('alb', list(keys))

        return actionSet


    def shouldHideNullSelectionItem(self):
        return (not self.isNullSelectionAllowed()
            and (self.getNullSelectionItemId() is not None)
            and self.containsId(self.getNullSelectionItemId()))


    def findNumRowsToPaint(self, target, cells):
        if self._reqRowsToPaint >= 0:
            rows = self._reqRowsToPaint
        else:
            rows = len(cells[0])
            if self.alwaysRecalculateColumnWidths:
                # TODO experimental feature for now: tell the client to
                # recalculate column widths.
                # We'll only do this for paints that do not originate from
                # table scroll/cache requests (i.e when reqRowsToPaint<0)
                target.addAttribute('recalcWidths', True)
        return rows


    def paintSelectMode(self, target):
        if self._multiSelectMode != MultiSelectMode.DEFAULT:
            target.addAttribute('multiselectmode',
                    MultiSelectMode.ordinal(self._multiSelectMode))
        if self.isSelectable():
            if self.isMultiSelect():
                target.addAttribute('selectmode', 'multi')
            else:
                target.addAttribute('selectmode', 'single')
        else:
            target.addAttribute('selectmode', 'none')

        if not self.isNullSelectionAllowed():
            target.addAttribute('nsa', False)

        # selection support
        # The select variable is only enabled if selectable
        if self.isSelectable():
            target.addVariable(self, 'selected', self.findSelectedKeys())


    def findSelectedKeys(self):
        selectedKeys = list()
        if self.isMultiSelect():
            sel = set(self.getValue())
            vids = self.getVisibleItemIds()
            for idd in vids:
                if idd in sel:
                    selectedKeys.append(self.itemIdMapper.key(idd))
        else:
            value = self.getValue()
            if value is None:
                value = self.getNullSelectionItemId()

            if value is not None:
                selectedKeys.append(self.itemIdMapper.key(value))

        return selectedKeys


    def paintDragMode(self, target):
        if self._dragMode != TableDragMode.NONE:
            target.addAttribute('dragmode',
                    TableDragMode.ordinal(self._dragMode))


    def paintTabIndex(self, target):
        # The tab ordering number
        if self.getTabIndex() > 0:
            target.addAttribute('tabindex', self.getTabIndex())


    def paintColumnWidth(self, target, columnId):
        if columnId in self._columnWidths:
            if self.getColumnWidth(columnId) > -1:
                target.addAttribute('width',
                        str(self.getColumnWidth(columnId)))
            else:
                target.addAttribute('er',
                        self.getColumnExpandRatio(columnId))


    def rowHeadersAreEnabled(self):
        return self.getRowHeaderMode() != self.ROW_HEADER_MODE_HIDDEN


    def paintRow(self, target, cells, iseditable, actionSet, iscomponent,
                indexInRowbuffer, itemId):
        target.startTag('tr')

        self.paintRowAttributes(target, cells, actionSet, indexInRowbuffer,
                itemId)

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
                if (cellStyle is not None) and (cellStyle != ''):
                    target.addAttribute(('style-'
                            + self._columnIdMap.key(columnId)), cellStyle)

            if ((iscomponent[currentColumn] or iseditable
                    or cells[self.CELL_GENERATED_ROW][indexInRowbuffer] != None)
                    and isinstance(cells[(self.CELL_FIRSTCOL
                            + currentColumn)][indexInRowbuffer], IComponent)):
                c = cells[self.CELL_FIRSTCOL + currentColumn][indexInRowbuffer]
                if c is None:
                    target.addText('')
                    self.paintCellTooltips(target, itemId, columnId)
                else:
                    c.paint(target)
            else:
                target.addText(cells[(self.CELL_FIRSTCOL
                        + currentColumn)][indexInRowbuffer])
                self.paintCellTooltips(target, itemId, columnId)

            currentColumn += 1

        target.endTag('tr')


    def paintCellTooltips(self, target, itemId, columnId):
        if self._itemDescriptionGenerator is not None:
            itemDescription = \
                self._itemDescriptionGenerator.generateDescription(self,
                        itemId, columnId)
            if itemDescription is not None and itemDescription != '':
                target.addAttribute('descr-' + self._columnIdMap.key(columnId),
                        itemDescription)


    def paintRowTooltips(self, target, itemId):
        if self._itemDescriptionGenerator is not None:
            rowDescription = \
                self._itemDescriptionGenerator.generateDescription(self,
                        itemId, None)
            if rowDescription is not None and rowDescription != '':
                target.addAttribute('rowdescr', rowDescription)


    def paintRowAttributes(self, *args):
        """A method where extended Table implementations may add their
        custom attributes for rows.
        """
        # tr attributes
        nargs = len(args)
        if nargs == 2:
            target, itemId = args
            pass
        elif nargs == 5:
            target, cells, actionSet, indexInRowbuffer, itemId = args

            self.paintRowIcon(target, cells, indexInRowbuffer)
            self.paintRowHeader(target, cells, indexInRowbuffer)
            self.paintGeneratedRowInfo(target, cells, indexInRowbuffer)

            target.addAttribute('key',
                    int( str(cells[self.CELL_KEY][indexInRowbuffer]) ))

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

            # For each row, if a cellStyleGenerator is specified, get the
            # specific style for the cell, using null as propertyId. If there
            # is any, add it to the target.
            if self._cellStyleGenerator is not None:
                rowStyle = self._cellStyleGenerator.getStyle(itemId, None)
                if (rowStyle is not None) and (rowStyle != ''):
                    target.addAttribute('rowstyle', rowStyle)

            self.paintRowTooltips(target, itemId)

            self.paintRowAttributes(target, itemId)
        else:
            raise ValueError, 'invalid number of arguments'


    def paintGeneratedRowInfo(self, target, cells, indexInRowBuffer):
        generatedRow = cells[self.CELL_GENERATED_ROW][indexInRowBuffer]
        if generatedRow is not None:
            target.addAttribute('gen_html',
                    generatedRow.isHtmlContentAllowed())
            target.addAttribute('gen_span',
                    generatedRow.isSpanColumns())
            target.addAttribute('gen_widget',
                    isinstance(generatedRow.getValue(), IComponent))


    def paintRowHeader(self, target, cells, indexInRowbuffer):
        if self.rowHeadersAreEnabled():
            if cells[self.CELL_HEADER][indexInRowbuffer] is not None:
                target.addAttribute('caption',
                        cells[self.CELL_HEADER][indexInRowbuffer])


    def paintRowIcon(self, target, cells, indexInRowbuffer):
        if (self.rowHeadersAreEnabled()
                and cells[self.CELL_ICON][indexInRowbuffer] is not None):
            target.addAttribute('icon',
                    cells[self.CELL_ICON][indexInRowbuffer])


    def getVisibleCells(self):
        """Gets the cached visible table contents.

        @return: the cached visible table contents.
        """
        if self._pageBuffer is None:
            self.refreshRenderedCells()
        return self._pageBuffer


    def getPropertyValue(self, rowId, colId, prop):
        """Gets the value of property.

        By default if the table is editable the fieldFactory is used to
        create editors for table cells. Otherwise formatPropertyValue is
        used to format the value representation.

        @param rowId:
                   the Id of the row (same as item Id).
        @param colId:
                   the Id of the column.
        @param prop:
                   the Property to be presented.
        @return: Object either formatted value or IComponent for field.
        @see: L{setTableFieldFactory}
        """
        if self.isEditable() and (self._fieldFactory is not None):
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
        """Formats table cell property values. By default the
        property.__str__ and return a empty string for null properties.

        @param rowId:
                   the Id of the row (same as item Id).
        @param colId:
                   the Id of the column.
        @param prop:
                   the Property to be formatted.
        @return: the string representation of property and its value.
        """
        if prop is None:
            return ''
        return str(prop)

    # Action container

    def addActionHandler(self, actionHandler):
        """Registers a new action handler for this container

        @see: L{action.container.addActionHandler}
        """
        if actionHandler is not None:

            if self._actionHandlers is None:
                self._actionHandlers = list()
                self._actionMapper = KeyMapper()

            if actionHandler not in self._actionHandlers:
                self._actionHandlers.append(actionHandler)
                # Assures the visual refresh. No need to reset the page buffer
                # before as the content has not changed, only the action
                # handlers.
                self.refreshRenderedCells()


    def removeActionHandler(self, actionHandler):
        """Removes a previously registered action handler for the contents
        of this container.

        @see: L{container.removeActionHandler}
        """
        if (self._actionHandlers is not None
                and actionHandler in self._actionHandlers):
            self._actionHandlers.remove(actionHandler)
            if len(self._actionHandlers) == 0:
                self._actionHandlers = None
                self._actionMapper = None
            # Assures the visual refresh. No need to reset the page buffer
            # before as the content has not changed, only the action
            # handlers.
            self.refreshRenderedCells()


    def removeAllActionHandlers(self):
        """Removes all action handlers"""
        self._actionHandlers = None
        self._actionMapper = None
        # Assures the visual refresh. No need to reset the page buffer
        # before as the content has not changed, only the action
        # handlers.
        self.refreshRenderedCells()


    # Property value change listening support

    def valueChange(self, event):
        """Notifies this listener that the Property's value has changed.

        Also listens changes in rendered items to refresh content area.

        @see: L{property.IValueChangeListener.valueChange}
        """
        if event.getProperty() == self:
            super(Table, self).valueChange(event)

        else:
            self.resetPageBuffer()
            self.refreshRenderedCells()
            self._containerChangeToBeRendered = True

        self.requestRepaint()


    def resetPageBuffer(self):
        """Clears the current page buffer. Call this before
        L{refreshRenderedCells} to ensure that all content is
        updated from the properties.
        """
        self._firstToBeRenderedInClient = -1
        self._lastToBeRenderedInClient = -1
        self._reqFirstRowToPaint = -1
        self._reqRowsToPaint = -1
        self._pageBuffer = None


    def attach(self):
        """Notifies the component that it is connected to an application.

        @see: L{IComponent.attach}
        """
        super(Table, self).attach()

        self.refreshRenderedCells()

        if self._visibleComponents is not None:
            for c in self._visibleComponents:
                c.attach()


    def detach(self):
        """Notifies the component that it is detached from the application

        @see: L{IComponent.detach}
        """
        super(Table, self).detach()

        if self._visibleComponents is not None:
            for c in self._visibleComponents:
                c.detach()


    def removeAllItems(self):
        """Removes all Items from the IContainer.

        @see: L{IContainer.removeAllItems}
        """
        self._currentPageFirstItemId = None
        self._currentPageFirstItemIndex = 0
        return super(Table, self).removeAllItems()


    def removeItem(self, itemId):
        """Removes the Item identified by C{ItemId} from the
        IContainer.

        @see: L{IContainer.removeItem}
        """
        nextItemId = self.nextItemId(itemId)
        ret = super(Table, self).removeItem(itemId)
        if (ret and itemId is not None
                and itemId == self._currentPageFirstItemId):
            self._currentPageFirstItemId = nextItemId

        if not isinstance(self.items, container.IItemSetChangeNotifier):
            self.refreshRowCache()

        return ret


    def removeContainerProperty(self, propertyId):
        """Removes a Property specified by the given Property ID from the
        IContainer.

        @see: L{IContainer.removeContainerProperty}
        """
        # If a visible property is removed, remove the corresponding column
        self._visibleColumns.remove(propertyId)
        if propertyId in self._columnAlignments:
            del self._columnAlignments[propertyId]
        if propertyId in self._columnIcons:
            del self._columnIcons[propertyId]
        if propertyId in self._columnHeaders:
            del self._columnHeaders[propertyId]
        if propertyId in self._columnFooters:
            del self._columnFooters[propertyId]
        return super(Table, self).removeContainerProperty(propertyId)


    def addContainerProperty(self, *args):
        """Adds a new property to the table and show it as a visible column.

        @param args: tuple of the form
            - (propertyId, type, defaultValue)
              1. the Id of the proprty.
              2. the class of the property.
              3. the default value given for all existing items.
            - (propertyId, type, defaultValue, columnHeader, columnIcon,
            columnAlignment)
              1. the Id of the proprty
              2. the class of the property
              3. the default value given for all existing items
              4. the Explicit header of the column. If explicit header is
                 not needed, this should be set null.
              5. the Icon of the column. If icon is not needed, this should
                 be set null.
              6. the Alignment of the column. Null implies align left.
        @raise NotImplementedError:
                    if the operation is not supported.
        @see: L{IContainer.addContainerProperty}
        """
        args = args
        nargs = len(args)
        if nargs == 3:
            propertyId, typ, defaultValue = args
            visibleColAdded = False
            if propertyId not in self._visibleColumns:
                self._visibleColumns.append(propertyId)
                visibleColAdded = True
            if not super(Table, self).addContainerProperty(propertyId,
                    typ, defaultValue):
                if visibleColAdded:
                    self._visibleColumns.remove(propertyId)
                return False
            if not isinstance(self.items, container.IPropertySetChangeNotifier):
                self.refreshRowCache()
            return True
        elif nargs == 6:
            (propertyId, typ, defaultValue, columnHeader, columnIcon,
                    columnAlignment) = args
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

        A generated column is a column that exists only in the Table, not as a
        property in the underlying IContainer. It shows up just as a regular
        column.

        A generated column will override a property with the same id, so that
        the generated column is shown instead of the column representing the
        property. Note that getContainerProperty() will still get the real
        property.

        Table will not listen to value change events from properties overridden
        by generated columns. If the content of your generated column depends
        on properties that are not directly visible in the table, attach value
        change listener to update the content on all depended properties.
        Otherwise your UI might not get updated as expected.

        Also note that getVisibleColumns() will return the generated columns,
        while getContainerPropertyIds() will not.

        @param idd:
                   the id of the column to be added
        @param generatedColumn:
                   the L{IColumnGenerator} to use for this column
        """
        if generatedColumn is None:
            raise ValueError, 'Can not add null as a GeneratedColumn'
        if idd in self._columnGenerators:
            raise ValueError, ('Can not add the same GeneratedColumn '
                    'twice, id:' + idd)
        else:
            self._columnGenerators[idd] = generatedColumn
            # add to visible column list unless already there (overriding
            # column from DS)
            if idd not in self._visibleColumns:
                self._visibleColumns.append(idd)

            self.refreshRowCache()


    def getColumnGenerator(self, columnId):
        """Returns the IColumnGenerator used to generate the given column.

        @param columnId:
                   The id of the generated column
        @return: The IColumnGenerator used for the given columnId or null.
        """
        return self._columnGenerators.get(columnId)


    def removeGeneratedColumn(self, columnId):
        """Removes a generated column previously added with addGeneratedColumn.

        @param columnId:
                   id of the generated column to remove
        @return: true if the column could be removed (existed in the Table)
        """
        if columnId in self._columnGenerators:
            del self._columnGenerators[columnId]
            # remove column from visibleColumns list unless it exists in
            # container (generator previously overrode this column)
            if columnId not in self.items.getContainerPropertyIds():
                self._visibleColumns.remove(columnId)
            self.refreshRowCache()
            return True
        else:
            return False


    def getVisibleItemIds(self):
        """Returns item identifiers of the items which are currently rendered
        on the client.

        Note, that some due to historical reasons the name of the method is bit
        misleading. Some items may be partly or totally out of the viewport of
        the table's scrollable area. Actully detecting rows which can be
        actually seen by the end user may be problematic due to the client
        server architecture. Using L{getCurrentPageFirstItemId}
        combined with L{getPageLength} may produce good enough
        estimates in some situations.

        @see: L{Select.getVisibleItemIds}
        """
        visible = list()
        cells = self.getVisibleCells()

        for i in range(len(cells[self.CELL_ITEMID])):
            visible.append(cells[self.CELL_ITEMID][i])

        return visible


    def containerItemSetChange(self, event):
        """IContainer datasource item set change. Table must flush its buffers
        on change.

        @see: L{container.ItemSetChangeListener.containerItemSetChange}
        """
        super(Table, self).containerItemSetChange(event)

        if isinstance(event, ItemSetChangeEvent):
            evt = event
            # if the event is not a global one and the added item is outside
            # the visible/buffered area, no need to do anything
            if (evt.getAddedItemIndex() != -1
                    and self._firstToBeRenderedInClient >= 0
                    and self._lastToBeRenderedInClient >= 0
                    and (self._firstToBeRenderedInClient
                            > evt.getAddedItemIndex())
                    or (self._lastToBeRenderedInClient
                            < evt.getAddedItemIndex())):
                return

        # ensure that page still has first item in page, ignore buffer refresh
        # (forced in this method)
        self.setCurrentPageFirstItemIndex(self.getCurrentPageFirstItemIndex(),
                False)

        self.refreshRowCache()


    def containerPropertySetChange(self, event):
        """IContainer datasource property set change. Table must flush its
        buffers on change.

        @see: L{container.PropertySetChangeListener.containerPropertySetChange}
        """
        self.disableContentRefreshing()
        super(Table, self).containerPropertySetChange(event)

        # sanitetize visibleColumns. note that we are not adding previously
        # non-existing properties as columns
        containerPropertyIds = \
                self.getContainerDataSource().getContainerPropertyIds()
        newVisibleColumns = list(self._visibleColumns)

        for idd in newVisibleColumns:
            if (idd not in containerPropertyIds
                    or (idd in self._columnGenerators)):
                newVisibleColumns.remove()
        self.setVisibleColumns(list(newVisibleColumns))

        # same for collapsed columns
        for idd in self._collapsedColumns:
            if (idd not in containerPropertyIds
                    or (idd in self._columnGenerators)):
                self._collapsedColumns.remove()

        self.resetPageBuffer()
        self.enableContentRefreshing(True)


    def setNewItemsAllowed(self, allowNewOptions):
        """Adding new items is not supported.

        @raise NotImplementedError:
                    if set to true.
        @see: L{Select.setNewItemsAllowed}
        """
        if allowNewOptions:
            raise NotImplementedError


    def nextItemId(self, itemId):
        """Gets the ID of the Item following the Item that corresponds to
        itemId.

        @see: L{IOrdered.nextItemId}
        """
        return self.items.nextItemId(itemId)


    def prevItemId(self, itemId):
        """Gets the ID of the Item preceding the Item that corresponds to
        the itemId.

        @see: L{IOrdered.prevItemId}
        """
        return self.items.prevItemId(itemId)


    def firstItemId(self):
        """Gets the ID of the first Item in the IContainer.

        @see: L{IOrdered.firstItemId}
        """
        return self.items.firstItemId()


    def lastItemId(self):
        """Gets the ID of the last Item in the IContainer.

        @see: L{IOrdered.lastItemId}
        """
        return self.items.lastItemId()


    def isFirstId(self, itemId):
        """Tests if the Item corresponding to the given Item ID is the first
        Item in the IContainer.

        @see: L{IOrdered.isFirstId}
        """
        return self.items.isFirstId(itemId)


    def isLastId(self, itemId):
        """Tests if the Item corresponding to the given Item ID is the last
        Item in the IContainer.

        @see: L{IOrdered.isLastId}
        """
        return self.items.isLastId(itemId)


    def addItemAfter(self, previousItemId, newItemId=None):
        """Adds new item after the given item.

        @see: L{IOrdered.addItemAfter}
        """
        if newItemId is None:
            item = self.items.addItemAfter(previousItemId)
        else:
            item = self.items.addItemAfter(previousItemId, newItemId)

        if not isinstance(self.items, container.IItemSetChangeNotifier):
            self.refreshRowCache()

        return item


    def setTableFieldFactory(self, fieldFactory):
        """Sets the TableFieldFactory that is used to create editor for
        table cells.

        The TableFieldFactory is only used if the Table is editable. By
        default the DefaultFieldFactory is used.

        @param fieldFactory:
                   the field factory to set.
        @see: L{isEditable}
        @see: L{DefaultFieldFactory}
        """
        self._fieldFactory = fieldFactory


    def getTableFieldFactory(self):
        """Gets the TableFieldFactory that is used to create editor for
        table cells.

        The IFieldFactory is only used if the Table is editable.

        @return: TableFieldFactory used to create the IField instances.
        @see: L{isEditable}
        """
        return self._fieldFactory


    def getFieldFactory(self):
        """Gets the IFieldFactory that is used to create editor for
        table cells.

        The IFieldFactory is only used if the Table is editable.

        @return: IFieldFactory used to create the IField instances.
        @see: L{isEditable}
        @deprecated: use L{getTableFieldFactory} instead
        """
        if isinstance(self._fieldFactory, IFieldFactory):
            return self._fieldFactory

        return None


    def setFieldFactory(self, fieldFactory):
        """Sets the IFieldFactory that is used to create editor for table
        cells.

        The IFieldFactory is only used if the Table is editable. By default
        the BaseFieldFactory is used.

        @param fieldFactory:
                   the field factory to set.
        @see: L{isEditable}
        @see: L{BaseFieldFactory}
        @deprecated: use L{setTableFieldFactory()} instead
        """
        warn('use setTableFieldFactory() instead', DeprecationWarning)

        self._fieldFactory = fieldFactory
        # Assure visual refresh
        self.refreshRowCache()


    def isEditable(self):
        """Is table editable.

        If table is editable a editor of type IField is created for each table
        cell. The assigned IFieldFactory is used to create the instances.

        To provide custom editors for table cells create a class implementing
        the IFieldFactory interface, and assign it to table, and set the
        editable property to true.

        @return: true if table is editable, false otherwise.
        @see: L{IField}
        @see: L{IFieldFactory}
        """
        return self._editable


    def setEditable(self, editable):
        """Sets the editable property.

        If table is editable a editor of type IField is created for each table
        cell. The assigned IFieldFactory is used to create the instances.

        To provide custom editors for table cells create a class implementins
        the IFieldFactory interface, and assign it to table, and set the
        editable property to true.

        @param editable:
                   true if table should be editable by user.
        @see: L{IField}
        @see: L{IFieldFactory}
        """
        self._editable = editable
        # Assure visual refresh
        self.refreshRowCache()


    def sort(self, *args):
        """Sorts the table.

        @raise NotImplementedError:
                    if the container data source does not implement
                    container.ISortable
        @see: L{ISortable.sort}
        """
        nargs = len(args)
        if nargs == 0:
            if self.getSortContainerPropertyId() is None:
                return
            self.sort([self._sortContainerPropertyId], [self._sortAscending])
        elif nargs == 2:
            propertyId, ascending = args
            c = self.getContainerDataSource()
            if isinstance(c, container.ISortable):
                pageIndex = self.getCurrentPageFirstItemIndex()
                c.sort(propertyId, ascending)
                self.setCurrentPageFirstItemIndex(pageIndex)
                self.refreshRowCache()
            elif c is not None:
                raise NotImplementedError, \
                        'Underlying Data does not allow sorting'
        else:
            raise ValueError, 'invalid number of arguments'


    def getSortableContainerPropertyIds(self):
        """Gets the container property IDs, which can be used to sort the item.

        @see: L{ISortable.getSortableContainerPropertyIds}
        """
        c = self.getContainerDataSource()
        if isinstance(c, container.ISortable) and not self.isSortDisabled():
            return c.getSortableContainerPropertyIds()
        else:
            return list()


    def getSortContainerPropertyId(self):
        """Gets the currently sorted column property ID.

        @return: the IContainer property id of the currently sorted column.
        """
        return self._sortContainerPropertyId


    def setSortContainerPropertyId(self, propertyId, doSort=True):
        """Sets the currently sorted column property id. With
        doSort flag actual sorting may be bypassed.

        @param propertyId:
                   the IContainer property id of the currently sorted column.
        @param doSort:
        """
        if ((self._sortContainerPropertyId is not None
            and not (self._sortContainerPropertyId == propertyId))
                or (self._sortContainerPropertyId is None
                    and propertyId is not None)):
            self._sortContainerPropertyId = propertyId
            if doSort:
                self.sort()
                # Assures the visual refresh. This should not be necessary as
                # sort() calls refreshRowCache.
                self.refreshRenderedCells()


    def isSortAscending(self):
        """Is the table currently sorted in ascending order.

        @return: C{True} if ascending, C{False} if descending.
        """
        return self._sortAscending


    def setSortAscending(self, ascending, doSort=True):
        """Sets the table in ascending order. With doSort flag actual
        sort can be bypassed.

        @param ascending:
                   C{True} if ascending, C{False} if descending.
        @param doSort:
        """
        if self._sortAscending != ascending:
            self._sortAscending = ascending
            if doSort:
                self.sort()

        # Assures the visual refresh. This should not be necessary as
        # sort() calls refreshRowCache
        self.refreshRenderedCells()


    def isSortDisabled(self):
        """Is sorting disabled altogether.

        True iff no sortable columns are given even in the case where
        data source would support this.

        @return: True iff sorting is disabled.
        """
        return self._sortDisabled


    def setSortDisabled(self, sortDisabled):
        """Disables the sorting altogether.

        To disable sorting altogether, set to true. In this case no
        sortable columns are given even in the case where datasource
        would support this.

        @param sortDisabled:
                   True iff sorting is disabled.
        """
        if self._sortDisabled != sortDisabled:
            self._sortDisabled = sortDisabled
            self.requestRepaint()


    def setLazyLoading(self, useLazyLoading):
        """Table does not support lazy options loading mode. Setting this
        true will throw NotImplementedError.

        @see: L{Select.setLazyLoading}
        """
        if useLazyLoading:
            raise NotImplementedError, \
                    'Lazy options loading is not supported by Table.'


    def setCellStyleGenerator(self, cellStyleGenerator):
        """Set cell style generator for Table.

        @param cellStyleGenerator:
                   New cell style generator or null to remove generator.
        """
        self._cellStyleGenerator = cellStyleGenerator
        # Assures the visual refresh. No need to reset the page buffer
        # before as the content has not changed, only the style generators
        self.refreshRenderedCells()


    def getCellStyleGenerator(self):
        """Get the current cell style generator."""
        return self._cellStyleGenerator


    def addListener(self, listener, iface=None):
        """Adds a header click/footer click/column resize/column reorder
        listener which handles the click events when the user clicks on a
        column header cell in the Table.

        The listener will receive events which contain information about which
        column was clicked and some details about the mouse event.

        @param listener:
                   The handler which should handle the events.
        """
        if (isinstance(listener, IColumnReorderListener) and
                (iface is None or issubclass(iface, IColumnReorderListener))):
            self.registerListener(
                    VScrollTable.COLUMN_REORDER_EVENT_ID,
                    ColumnReorderEvent, listener,
                    COLUMN_REORDER_METHOD)

        if (isinstance(listener, IColumnResizeListener) and
                (iface is None or issubclass(iface, IColumnResizeListener))):
            self.registerListener(
                    VScrollTable.COLUMN_RESIZE_EVENT_ID,
                    ColumnResizeEvent, listener,
                    COLUMN_RESIZE_METHOD)

        if (isinstance(listener, IFooterClickListener) and
                (iface is None or issubclass(iface, IFooterClickListener))):
            self.registerListener(
                    VScrollTable.FOOTER_CLICK_EVENT_ID,
                    FooterClickEvent, listener,
                    FOOTER_CLICK_METHOD)

        if (isinstance(listener, IHeaderClickListener) and
                (iface is None or issubclass(iface, IHeaderClickListener))):
            self.registerListener(
                    VScrollTable.HEADER_CLICK_EVENT_ID,
                    HeaderClickEvent, listener,
                    HEADER_CLICK_METHOD)

        if (isinstance(listener, IItemClickListener) and
                (iface is None or issubclass(iface, IItemClickListener))):
            self.registerListener(
                    VScrollTable.ITEM_CLICK_EVENT_ID,
                    ItemClickEvent, listener,
                    ITEM_CLICK_METHOD)

        super(Table, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, ColumnReorderEvent):
            self.registerCallback(ColumnReorderEvent, callback,
                    VScrollTable.COLUMN_REORDER_EVENT_ID, *args)

        elif issubclass(eventType, ColumnResizeEvent):
            self.registerCallback(ColumnResizeEvent, callback,
                    VScrollTable.COLUMN_RESIZE_EVENT_ID, *args)

        elif issubclass(eventType, FooterClickEvent):
            self.registerCallback(FooterClickEvent, callback,
                    VScrollTable.FOOTER_CLICK_EVENT_ID, *args)

        elif issubclass(eventType, HeaderClickEvent):
            self.registerCallback(HeaderClickEvent, callback,
                    VScrollTable.HEADER_CLICK_EVENT_ID, *args)

        elif issubclass(eventType, ItemClickEvent):
            self.registerCallback(ItemClickEvent, callback,
                    VScrollTable.ITEM_CLICK_EVENT_ID, *args)

        else:
            super(Table, self).addCallback(callback, eventType, *args)


    def removeListener(self, listener, iface=None):
        """Removes a listener from the Table.

        @param listener:
                   The listener to remove
        """
        if (isinstance(listener, IColumnReorderListener) and
                (iface is None or issubclass(iface, IColumnReorderListener))):
            self.withdrawListener(
                    VScrollTable.COLUMN_REORDER_EVENT_ID,
                    ColumnReorderEvent, listener)

        if (isinstance(listener, IColumnResizeListener) and
                (iface is None or issubclass(iface, IColumnResizeListener))):
            self.withdrawListener(
                    VScrollTable.COLUMN_RESIZE_EVENT_ID,
                    ColumnResizeEvent, listener)

        if (isinstance(listener, IFooterClickListener) and
                (iface is None or issubclass(iface, IFooterClickListener))):
            self.withdrawListener(
                    VScrollTable.FOOTER_CLICK_EVENT_ID,
                    FooterClickEvent, listener)

        if (isinstance(listener, IHeaderClickListener) and
                (iface is None or issubclass(iface, IHeaderClickListener))):
            self.withdrawListener(
                    VScrollTable.HEADER_CLICK_EVENT_ID,
                    HeaderClickEvent, listener)

        if (isinstance(listener, IItemClickListener) and
                (iface is None or issubclass(iface, IItemClickListener))):
            self.withdrawListener(
                    VScrollTable.ITEM_CLICK_EVENT_ID,
                    ItemClickEvent, listener)

        super(Table, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, ColumnReorderEvent):
            self.withdrawCallback(ColumnReorderEvent, callback,
                    VScrollTable.COLUMN_REORDER_EVENT_ID)

        elif issubclass(eventType, ColumnResizeEvent):
            self.withdrawCallback(ColumnResizeEvent, callback,
                    VScrollTable.COLUMN_RESIZE_EVENT_ID)

        elif issubclass(eventType, FooterClickEvent):
            self.withdrawCallback(FooterClickEvent, callback,
                    VScrollTable.FOOTER_CLICK_EVENT_ID)

        elif issubclass(eventType, HeaderClickEvent):
            self.withdrawCallback(HeaderClickEvent, callback,
                    VScrollTable.HEADER_CLICK_EVENT_ID)

        elif issubclass(eventType, ItemClickEvent):
            self.withdrawCallback(ItemClickEvent, callback,
                    VScrollTable.ITEM_CLICK_EVENT_ID)

        else:
            super(Table, self).removeCallback(callback, eventType)


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
                    # Form has children in layout, but is
                    # not IComponentContainer
                    c.requestRepaint()
                    c.getLayout().requestRepaintAll()
                elif isinstance(c, Table):
                    c.requestRepaintAll()
                elif isinstance(c, IComponentContainer):
                    c.requestRepaintAll()
                else:
                    c.requestRepaint()


    def setDragMode(self, newDragMode):
        """Sets the drag start mode of the Table. Drag start mode controls
        how Table behaves as a drag source.
        """
        self._dragMode = newDragMode
        self.requestRepaint()


    def getDragMode(self):
        """@return: the current start mode of the Table. Drag start mode
                    controls how Table behaves as a drag source.
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
        return AbstractSelectTargetDetails(clientVariables, self)


    def setMultiSelectMode(self, mode):
        """Sets the behavior of how the multi-select mode should behave when
        the table is both selectable and in multi-select mode.

        Note, that on some clients the mode may not be respected. E.g. on
        touch based devices CTRL/SHIFT base selection method is invalid, so
        touch based browsers always use the L{MultiSelectMode.SIMPLE}.

        @param mode:
                   The select mode of the table
        """
        self._multiSelectMode = mode
        self.requestRepaint()


    def getMultiSelectMode(self):
        """Returns the select mode in which multi-select is used.

        @return: The multi select mode
        """
        return self._multiSelectMode


    def getColumnFooter(self, propertyId):
        """Gets the footer caption beneath the rows

        @param propertyId:
                   The propertyId of the column *
        @return: The caption of the footer or NULL if not set
        """
        return self._columnFooters.get(propertyId)


    def setColumnFooter(self, propertyId, footer):
        """Sets the column footer caption. The column footer caption is the
        text displayed beneath the column if footers have been set visible.

        @param propertyId:
                   The properyId of the column
        @param footer:
                   The caption of the footer
        """
        if footer is None:
            if propertyId in self._columnFooters:
                del self._columnFooters[propertyId]
        else:
            self._columnFooters[propertyId] = footer

        self.requestRepaint()

    def setFooterVisible(self, visible):
        """Sets the footer visible in the bottom of the table.

        The footer can be used to add column related data like sums to the
        bottom of the Table using setColumnFooter.

        @param visible:
                   Should the footer be visible
        """
        if visible != self._columnFootersVisible:
            self._columnFootersVisible = visible
            self.requestRepaint()


    def setItemDescriptionGenerator(self, generator):
        """Set the item description generator which generates tooltips for
        cells and rows in the Table

        @param generator:
                   The generator to use or null to disable
        """
        if generator != self._itemDescriptionGenerator:
            self._itemDescriptionGenerator = generator
            # Assures the visual refresh. No need to reset the page buffer
            # before as the content has not changed, only the descriptions
            self.refreshRenderedCells()


    def getItemDescriptionGenerator(self):
        """Get the item description generator which generates tooltips for
        cells and rows in the Table.
        """
        return self._itemDescriptionGenerator


    def isFooterVisible(self):
        """Is the footer currently visible?

        @return: Returns true if visible else false
        """
        return self._columnFootersVisible


    def setRowGenerator(self, generator):
        """Assigns a row generator to the table. The row generator will be
        able to replace rows in the table when it is rendered.

        @param generator:
                   the new row generator
        """
        self._rowGenerator = generator
        self.refreshRowCache()


    def getRowGenerator(self):
        """@return the current row generator"""
        return self._rowGenerator


class TableDragMode(object):
    """Modes that Table support as drag sourse."""

    #: Table does not start drag and drop events. HTM5 style events started
    #  by browser may still happen.
    NONE = 'NONE'

    #: Table starts drag with a one row only.
    ROW = 'ROW'

    #: Table drags selected rows, if drag starts on a selected rows. Else it
    #  starts like in ROW mode. Note, that in Transferable there will still
    #  be only the row on which the drag started, other dragged rows need to
    #  be checked from the source Table.
    MULTIROW = 'MULTIROW'

    _values = [NONE, ROW, MULTIROW]

    @classmethod
    def values(cls):
        return cls._values[:]

    @classmethod
    def ordinal(cls, val):
        return cls._values.index(val)


class IColumnGenerator(object):
    """Used to create "generated columns"; columns that exist only in the
    Table, not in the underlying IContainer. Implement this interface and pass
    it to Table.addGeneratedColumn along with an id for the column to be
    generated.
    """

    def generateCell(self, source, itemId, columnId):
        """Called by Table when a cell in a generated column needs to be
        generated.

        @param source:
                   the source Table
        @param itemId:
                   the itemId (aka rowId) for the of the cell to be generated
        @param columnId:
                   the id for the generated column (as specified in
                   addGeneratedColumn)
        @return: A L{IComponent} that should be rendered in the cell or a
                 string that should be displayed in the cell. Other return
                 values are not supported.
        """
        raise NotImplementedError


class ICellStyleGenerator(object):
    """Allow to define specific style on cells (and rows) contents. Implements
    this interface and pass it to Table.setCellStyleGenerator. Row styles are
    generated when porpertyId is null. The CSS class name that will be added
    to the cell content is C{v-table-cell-content-[style name]}, and
    the row style will be C{v-table-row-[style name]}.
    """

    def getStyle(self, itemId, propertyId):
        """Called by Table when a cell (and row) is painted.

        @param itemId:
                   The itemId of the painted cell
        @param propertyId:
                   The propertyId of the cell, null when getting row style
        @return: The style name to add to this cell or row. (the CSS class
                 name will be v-table-cell-content-[style name], or
                 v-table-row-[style name] for rows)
        """
        raise NotImplementedError


class TableTransferable(DataBoundTransferable):
    """Concrete implementation of L{DataBoundTransferable} for data
    transferred from a table.

    @see: L{DataBoundTransferable}.
    """

    def __init__(self, rawVariables, table):
        super(TableTransferable, self).__init__(table, rawVariables)
        obj = rawVariables.get('itemId')
        if obj is not None:
            self.setData('itemId', table.itemIdMapper.get(object))

        obj = rawVariables.get('propertyId')
        if obj is not None:
            self.setData('propertyId', table._columnIdMap.get(object))


    def getItemId(self):
        return self.getData('itemId')


    def getPropertyId(self):
        return self.getData('propertyId')


    def getSourceComponent(self):
        return super(TableTransferable, self).getSourceComponent()


class TableDropCriterion(ServerSideCriterion):
    """Lazy loading accept criterion for Table. Accepted target rows are
    loaded from server once per drag and drop operation. Developer must
    override one method that decides on which rows the currently dragged
    data can be dropped.

    Initially pretty much no data is sent to client. On first required
    criterion check (per drag request) the client side data structure is
    initialized from server and no subsequent requests requests are needed
    during that drag and drop operation.
    """

    def __init__(self):
        super(TableDropCriterion, self).__init__()

        self._table = None
        self._allowedItemIds = None


    def getIdentifier(self):
        return clsname(TableDropCriterion)


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
        self._allowedItemIds = self.getAllowedItemIds(dragEvent,
                self._table, visibleItemIds)
        return dropTargetData.getItemIdOver() in self._allowedItemIds


    def paintResponse(self, target):
        # send allowed nodes to client so subsequent requests
        # can be avoided
        arry = list(self._allowedItemIds)
        for i in range(len(arry)):
            key = self._table.itemIdMapper.key( arry[i] )
            arry[i] = key

        target.addAttribute('allowedIds', arry)


    def getAllowedItemIds(self, dragEvent, table, visibleItemIds):
        """@param dragEvent:
        @param table:
                   the table for which the allowed item identifiers are
                   defined
        @param visibleItemIds:
                   the list of currently rendered item identifiers, accepted
                   item id's need to be detected only for these visible items
        @return: the set of identifiers for items on which the dragEvent will
                 be accepted
        """
        pass


class IHeaderClickListener(object):
    """Interface for the listener for column header mouse click events. The
    headerClick method is called when the user presses a header column cell.
    """

    def headerClick(self, event):
        """Called when a user clicks a header column cell

        @param event:
                   The event which contains information about the column and
                   the mouse click event
        """
        raise NotImplementedError


HEADER_CLICK_METHOD = getattr(IHeaderClickListener, 'headerClick')


class HeaderClickEvent(ClickEvent):
    """Click event fired when clicking on the Table headers. The event
    includes a reference the the Table the event originated from, the property
    id of the column which header was pressed and details about the mouse
    event itself.
    """

    def __init__(self, source, propertyId, details):
        super(HeaderClickEvent, self).__init__(source, details)
        self._columnPropertyId = propertyId


    def getPropertyId(self):
        """Gets the property id of the column which header was pressed

        @return: The column propety id
        """
        return self._columnPropertyId


class IFooterClickListener(object):
    """Interface for the listener for column footer mouse click events. The
    footerClick method is called when the user presses a footer column cell.
    """

    def footerClick(self, event):
        """Called when a user clicks a footer column cell

        @param event:
                   The event which contains information about the column and
                   the mouse click event
        """
        raise NotImplementedError


FOOTER_CLICK_METHOD = getattr(IFooterClickListener, 'footerClick')


class FooterClickEvent(ClickEvent):
    """Click event fired when clicking on the Table footers. The event
    includes a reference the the Table the event originated from, the property
    id of the column which header was pressed and details about the mouse
    event itself.
    """

    def __init__(self, source, propertyId, details):
        """Constructor.

        @param source:
                   The source of the component
        @param propertyId:
                   The propertyId of the column
        @param details:
                   The mouse details of the click
        """
        super(FooterClickEvent, self).__init__(source, details)
        self._columnPropertyId = propertyId


    def getPropertyId(self):
        """Gets the property id of the column which header was pressed

        @return: The column propety id
        """
        return self._columnPropertyId


class IColumnResizeListener(object):
    """Interface for listening to column resize events."""

    def columnResize(self, event):
        """This method is triggered when the column has been resized

        @param event:
                   The event which contains the column property id, the
                   previous width of the column and the current width of
                   the column
        """
        raise NotImplementedError


COLUMN_RESIZE_METHOD = getattr(IColumnResizeListener, 'columnResize')


class ColumnResizeEvent(ComponentEvent):
    """This event is fired when a column is resized. The event contains the
    columns property id which was fired, the previous width of the column and
    the width of the column after the resize.
    """

    def __init__(self, source, propertyId, previous, current):
        """Constructor

        @param source:
                   The source of the event
        @param propertyId:
                   The columns property id
        @param previous:
                   The width in pixels of the column before the resize event
        @param current:
                   The width in pixels of the column after the resize event
        """
        super(ColumnResizeEvent, self).__init__(source)
        self._previousWidth = previous
        self._currentWidth = current
        self._columnPropertyId = propertyId


    def getPropertyId(self):
        """Get the column property id of the column that was resized.

        @return: The column property id
        """
        return self._columnPropertyId


    def getPreviousWidth(self):
        """Get the width in pixels of the column before the resize event

        @return: Width in pixels
        """
        return self._previousWidth


    def getCurrentWidth(self):
        """Get the width in pixels of the column after the resize event

        @return: Width in pixels
        """
        return self._currentWidth


class IColumnReorderListener(object):
    """Interface for listening to column reorder events."""

    def columnReorder(self, event):
        """This method is triggered when the column has been reordered
        """
        raise NotImplementedError


COLUMN_REORDER_METHOD = getattr(IColumnReorderListener, 'columnReorder')


class ColumnReorderEvent(ComponentEvent):
    """This event is fired when a columns are reordered by the end user user."""


    def __init__(self, source):
        """Constructor

        @param source:
                   The source of the event
        """
        super(ColumnReorderEvent, self).__init__(source)


class IRowGenerator(object):
    """Row generators can be used to replace certain items in a table with a
    generated string. The generator is called each time the table is
    rendered, which means that new strings can be generated each time.

    Row generators can be used for e.g. summary rows or grouping of items.
    """

    def generateRow(self, table, itemId):
        """Called for every row that is painted in the Table. Returning a
        GeneratedRow object will cause the row to be painted based on the
        contents of the GeneratedRow. A generated row is by default styled
        similarly to a header or footer row.

        The GeneratedRow data object contains the text that should be
        rendered in the row. The itemId in the container thus works only as a
        placeholder.

        If GeneratedRow.setSpanColumns(true) is used, there will be one
        String spanning all columns (use setText("Spanning text")). Otherwise
        you can define one String per visible column.

        If GeneratedRow.setRenderAsHtml(true) is used, the strings can
        contain HTML markup, otherwise all strings will be rendered as text
        (the default).

        A "v-table-generated-row" CSS class is added to all generated rows.
        For custom styling of a generated row you can combine a RowGenerator
        with a CellStyleGenerator.

        @param table:
                   The Table that is being painted
        @param itemId:
                   The itemId for the row
        @return: A GeneratedRow describing how the row should be painted or
                 null to paint the row with the contents from the container
        """
        raise NotImplementedError


class GeneratedRow(object):

    def __init__(self, *text):
        """Creates a new generated row. If only one string is passed in,
        columns are automatically spanned.

        @param text
        """
        self._htmlContentAllowed = False
        self._spanColumns = False
        self._text = None

        self.setHtmlContentAllowed(False)
        self.setSpanColumns((text is None) or (len(text) == 1))
        self.setText(text)


    def setText(self, *text):
        """Pass one string if spanColumns is used, one string for each visible
        column otherwise
        """
        if (text is None) or (len(text) == 1 and text[0] is None):
            text = ['']
        self._text = text


    def getText(self):
        return self._text


    def getValue(self):
        return self.getText()


    def isHtmlContentAllowed(self):
        return self._htmlContentAllowed


    def setHtmlContentAllowed(self, htmlContentAllowed):
        """If set to true, all strings passed to L{setText} will be rendered
        as HTML.

        @param htmlContentAllowed
        """
        self._htmlContentAllowed = htmlContentAllowed


    def isSpanColumns(self):
        return self._spanColumns


    def setSpanColumns(self, spanColumns):
        """If set to true, only one string will be rendered, spanning the
        entire row.
        """
        self._spanColumns = spanColumns
