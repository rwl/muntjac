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


class Container(object):
    """<p>
    A specialized set of identified Items. Basically the Container is a set of
    {@link Item}s, but it imposes certain constraints on its contents. These
    constraints state the following:
    </p>

    <ul>
    <li>All Items in the Container must have the same number of Properties.
    <li>All Items in the Container must have the same Property ID's (see
    {@link Item#getItemPropertyIds()}).
    <li>All Properties in the Items corresponding to the same Property ID must
    have the same data type.
    <li>All Items within a container are uniquely identified by their non-null
    IDs.
    </ul>

    <p>
    The Container can be visualized as a representation of a relational database
    table. Each Item in the Container represents a row in the table, and all
    cells in a column (identified by a Property ID) have the same data type. Note
    that as with the cells in a database table, no Property in a Container may be
    empty, though they may contain <code>null</code> values.
    </p>

    <p>
    Note that though uniquely identified, the Items in a Container are not
    necessarily {@link Container.Ordered ordered} or {@link Container.Indexed
    indexed}.
    </p>

    <p>
    Containers can derive Item ID's from the item properties or use other,
    container specific or user specified identifiers.
    </p>

    <p>
    If a container is {@link Filterable filtered} or {@link Sortable sorted},
    most of the the methods of the container interface and its subinterfaces
    (container size, {@link #containsId(Object)}, iteration and indices etc.)
    relate to the filtered and sorted view, not to the full container contents.
    See individual method javadoc for exceptions to this (adding and removing
    items).
    </p>

    <p>
    <img src=doc-files/Container_full.gif>
    </p>

    <p>
    The Container interface is split to several subinterfaces so that a class can
    implement only the ones it needs.
    </p>

    @author IT Mill Ltd
    @version
    @VERSION@
    @since 3.0
    """

    def getItem(self, itemId):
        """Gets the {@link Item} with the given Item ID from the Container. If the
        Container does not contain the requested Item, <code>null</code> is
        returned.

        Containers should not return Items that are filtered out.

        @param itemId
                   ID of the {@link Item} to retrieve
        @return the {@link Item} with the given ID or <code>null</code> if the
                Item is not found in the Container
        """
        pass

    def getContainerPropertyIds(self):
        """Gets the ID's of all Properties stored in the Container. The ID's cannot
        be modified through the returned collection.

        @return unmodifiable collection of Property IDs
        """
        pass

    def getItemIds(self):
        """Gets the ID's of all visible (after filtering and sorting) Items stored
        in the Container. The ID's cannot be modified through the returned
        collection.

        If the container is {@link Ordered}, the collection returned by this
        method should follow that order. If the container is {@link Sortable},
        the items should be in the sorted order.

        Calling this method for large lazy containers can be an expensive
        operation and should be avoided when practical.

        @return unmodifiable collection of Item IDs
        """
        pass

    def getContainerProperty(self, itemId, propertyId):
        """Gets the Property identified by the given itemId and propertyId from the
        Container. If the Container does not contain the item or it is filtered
        out, or the Container does not have the Property, <code>null</code> is
        returned.

        @param itemId
                   ID of the visible Item which contains the Property
        @param propertyId
                   ID of the Property to retrieve
        @return Property with the given ID or <code>null</code>
        """
        pass

    def getType(self, propertyId):
        """Gets the data type of all Properties identified by the given Property ID.

        @param propertyId
                   ID identifying the Properties
        @return data type of the Properties
        """
        pass

    def size(self):
        """Gets the number of visible Items in the Container.

        Filtering can hide items so that they will not be visible through the
        container API.

        @return number of Items in the Container
        """
        pass

    def containsId(self, itemId):
        """Tests if the Container contains the specified Item.

        Filtering can hide items so that they will not be visible through the
        container API, and this method should respect visibility of items (i.e.
        only indicate visible items as being in the container) if feasible for
        the container.

        @param itemId
                   ID the of Item to be tested
        @return boolean indicating if the Container holds the specified Item
        """
        pass

    def addItem(self, *args):
        """Creates a new Item with the given ID in the Container.

        <p>
        The new Item is returned, and it is ready to have its Properties
        modified. Returns <code>null</code> if the operation fails or the
        Container already contains a Item with the given ID.
        </p>

        <p>
        This functionality is optional.
        </p>

        @param itemId
                   ID of the Item to be created
        @return Created new Item, or <code>null</code> in case of a failure
        @throws UnsupportedOperationException
                    if adding an item with an explicit item ID is not supported
                    by the container
        ---
        Creates a new Item into the Container, and assign it an automatic ID.

        <p>
        The new ID is returned, or <code>null</code> if the operation fails.
        After a successful call you can use the {@link #getItem(Object ItemId)
        <code>getItem</code>}method to fetch the Item.
        </p>

        <p>
        This functionality is optional.
        </p>

        @return ID of the newly created Item, or <code>null</code> in case of a
                failure
        @throws UnsupportedOperationException
                    if adding an item without an explicit item ID is not
                    supported by the container
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            pass # astStmt: [Stmt([]), None]
        elif _1 == 1:
            itemId, = _0
        else:
            raise ARGERROR(0, 1)

    def removeItem(self, itemId):
        """Removes the Item identified by <code>ItemId</code> from the Container.

        <p>
        Containers that support filtering should also allow removing an item that
        is currently filtered out.
        </p>

        <p>
        This functionality is optional.
        </p>

        @param itemId
                   ID of the Item to remove
        @return <code>true</code> if the operation succeeded, <code>false</code>
                if not
        @throws UnsupportedOperationException
                    if the container does not support removing individual items
        """
        pass

    def addContainerProperty(self, propertyId, type, defaultValue):
        """Adds a new Property to all Items in the Container. The Property ID, data
        type and default value of the new Property are given as parameters.

        This functionality is optional.

        @param propertyId
                   ID of the Property
        @param type
                   Data type of the new Property
        @param defaultValue
                   The value all created Properties are initialized to
        @return <code>true</code> if the operation succeeded, <code>false</code>
                if not
        @throws UnsupportedOperationException
                    if the container does not support explicitly adding container
                    properties
        """
        pass

    def removeContainerProperty(self, propertyId):
        """Removes a Property specified by the given Property ID from the Container.
        Note that the Property will be removed from all Items in the Container.

        This functionality is optional.

        @param propertyId
                   ID of the Property to remove
        @return <code>true</code> if the operation succeeded, <code>false</code>
                if not
        @throws UnsupportedOperationException
                    if the container does not support removing container
                    properties
        """
        pass

    def removeAllItems(self):
        """Removes all Items from the Container.

        <p>
        Note that Property ID and type information is preserved. This
        functionality is optional.
        </p>

        @return <code>true</code> if the operation succeeded, <code>false</code>
                if not
        @throws UnsupportedOperationException
                    if the container does not support removing all items
        """
        pass

class Ordered(Container):
    """Interface for Container classes whose {@link Item}s can be traversed in
    order.

    <p>
    If the container is filtered or sorted, the traversal applies to the
    filtered and sorted view.
    </p>
    <p>
    The <code>addItemAfter()</code> methods should apply filters to the added
    item after inserting it, possibly hiding it immediately. If the container
    is being sorted, they may add items at the correct sorted position
    instead of the given position. See also {@link Filterable} and
    {@link Sortable} for more information.
    </p>
    """

    def nextItemId(self, itemId):
        """Gets the ID of the Item following the Item that corresponds to
        <code>itemId</code>. If the given Item is the last or not found in
        the Container, <code>null</code> is returned.

        @param itemId
                   ID of a visible Item in the Container
        @return ID of the next visible Item or <code>null</code>
        """
        pass

    def prevItemId(self, itemId):
        """Gets the ID of the Item preceding the Item that corresponds to
        <code>itemId</code>. If the given Item is the first or not found in
        the Container, <code>null</code> is returned.

        @param itemId
                   ID of a visible Item in the Container
        @return ID of the previous visible Item or <code>null</code>
        """
        pass

    def firstItemId(self):
        """Gets the ID of the first Item in the Container.

        @return ID of the first visible Item in the Container
        """
        pass

    def lastItemId(self):
        """Gets the ID of the last Item in the Container..

        @return ID of the last visible Item in the Container
        """
        pass

    def isFirstId(self, itemId):
        """Tests if the Item corresponding to the given Item ID is the first
        Item in the Container.

        @param itemId
                   ID of an Item in the Container
        @return <code>true</code> if the Item is first visible item in the
                Container, <code>false</code> if not
        """
        pass

    def isLastId(self, itemId):
        """Tests if the Item corresponding to the given Item ID is the last Item
        in the Container.

        @return <code>true</code> if the Item is last visible item in the
                Container, <code>false</code> if not
        """
        pass

    def addItemAfter(self, *args):
        """Adds a new item after the given item.
        <p>
        Adding an item after null item adds the item as first item of the
        ordered container.
        </p>

        @see Ordered Ordered: adding items in filtered or sorted containers

        @param previousItemId
                   Id of the visible item in ordered container after which to
                   insert the new item.
        @return item id the the created new item or null if the operation
                fails.
        @throws UnsupportedOperationException
                    if the operation is not supported by the container
        ---
        Adds a new item after the given item.
        <p>
        Adding an item after null item adds the item as first item of the
        ordered container.
        </p>

        @see Ordered Ordered: adding items in filtered or sorted containers

        @param previousItemId
                   Id of the visible item in ordered container after which to
                   insert the new item.
        @param newItemId
                   Id of the new item to be added.
        @return new item or null if the operation fails.
        @throws UnsupportedOperationException
                    if the operation is not supported by the container
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            previousItemId, = _0
        elif _1 == 2:
            previousItemId, newItemId = _0
        else:
            raise ARGERROR(1, 2)

class Sortable(Ordered):
    """Interface for Container classes whose {@link Item}s can be sorted.
    <p>
    When an {@link Ordered} or {@link Indexed} container is sorted, all
    relevant operations of these interfaces should only use the filtered and
    sorted contents and the filtered indices to the container. Indices or
    item identifiers in the public API refer to the visible view unless
    otherwise stated. However, the <code>addItem*()</code> methods may add
    items that will be filtered out after addition or moved to another
    position based on sorting.
    </p>
    <p>
    How sorting is performed when a {@link Hierarchical} container implements
    {@link Sortable} is implementation specific and should be documented in
    the implementing class. However, the recommended approach is sorting the
    roots and the sets of children of each item separately.
    </p>
    <p>
    Depending on the container type, sorting a container may permanently
    change the internal order of items in the container.
    </p>
    """

    def sort(self, propertyId, ascending):
        """Sort method.

        Sorts the container items.

        Sorting a container can irreversibly change the order of its items or
        only change the order temporarily, depending on the container.

        @param propertyId
                   Array of container property IDs, whose values are used to
                   sort the items in container as primary, secondary, ...
                   sorting criterion. All of the item IDs must be in the
                   collection returned by
                   {@link #getSortableContainerPropertyIds()}
        @param ascending
                   Array of sorting order flags corresponding to each
                   property ID used in sorting. If this array is shorter than
                   propertyId array, ascending order is assumed for items
                   where the order is not specified. Use <code>true</code> to
                   sort in ascending order, <code>false</code> to use
                   descending order.
        """
        pass

    def getSortableContainerPropertyIds(self):
        """Gets the container property IDs which can be used to sort the items.

        @return the IDs of the properties that can be used for sorting the
                container
        """
        pass

class Indexed(Ordered):
    """Interface for Container classes whose {@link Item}s can be accessed by
    their position in the container.
    <p>
    If the container is filtered or sorted, all indices refer to the filtered
    and sorted view. However, the <code>addItemAt()</code> methods may add
    items that will be filtered out after addition or moved to another
    position based on sorting.
    </p>
    """

    def indexOfId(self, itemId):
        """Gets the index of the Item corresponding to the itemId. The following
        is <code>true</code> for the returned index: 0 <= index < size(), or
        index = -1 if there is no visible item with that id in the container.

        @param itemId
                   ID of an Item in the Container
        @return index of the Item, or -1 if (the filtered and sorted view of)
                the Container does not include the Item
        """
        pass

    def getIdByIndex(self, index):
        """Gets the ID of an Item by an index number.

        @param index
                   Index of the requested id in (the filtered and sorted view
                   of) the Container
        @return ID of the Item in the given index
        """
        pass

    def addItemAt(self, *args):
        """Adds a new item at given index (in the filtered view).
        <p>
        The indices of the item currently in the given position and all the
        following items are incremented.
        </p>
        <p>
        This method should apply filters to the added item after inserting
        it, possibly hiding it immediately. If the container is being sorted,
        the item may be added at the correct sorted position instead of the
        given position. See {@link Indexed}, {@link Ordered},
        {@link Filterable} and {@link Sortable} for more information.
        </p>

        @param index
                   Index (in the filtered and sorted view) to add the new
                   item.
        @return item id of the created item or null if the operation fails.
        @throws UnsupportedOperationException
                    if the operation is not supported by the container
        ---
        Adds a new item at given index (in the filtered view).
        <p>
        The indexes of the item currently in the given position and all the
        following items are incremented.
        </p>
        <p>
        This method should apply filters to the added item after inserting
        it, possibly hiding it immediately. If the container is being sorted,
        the item may be added at the correct sorted position instead of the
        given position. See {@link Indexed}, {@link Filterable} and
        {@link Sortable} for more information.
        </p>

        @param index
                   Index (in the filtered and sorted view) at which to add
                   the new item.
        @param newItemId
                   Id of the new item to be added.
        @return new {@link Item} or null if the operation fails.
        @throws UnsupportedOperationException
                    if the operation is not supported by the container
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            index, = _0
        elif _1 == 2:
            index, newItemId = _0
        else:
            raise ARGERROR(1, 2)

class Hierarchical(Container):
    """<p>
    Interface for <code>Container</code> classes whose Items can be arranged
    hierarchically. This means that the Items in the container belong in a
    tree-like structure, with the following quirks:
    </p>

    <ul>
    <li>The Item structure may have more than one root elements
    <li>The Items in the hierarchy can be declared explicitly to be able or
    unable to have children.
    </ul>
    """

    def getChildren(self, itemId):
        """Gets the IDs of all Items that are children of the specified Item.
        The returned collection is unmodifiable.

        @param itemId
                   ID of the Item whose children the caller is interested in
        @return An unmodifiable {@link java.util.Collection collection}
                containing the IDs of all other Items that are children in
                the container hierarchy
        """
        pass

    def getParent(self, itemId):
        """Gets the ID of the parent Item of the specified Item.

        @param itemId
                   ID of the Item whose parent the caller wishes to find out.
        @return the ID of the parent Item. Will be <code>null</code> if the
                specified Item is a root element.
        """
        pass

    def rootItemIds(self):
        """Gets the IDs of all Items in the container that don't have a parent.
        Such items are called <code>root</code> Items. The returned
        collection is unmodifiable.

        @return An unmodifiable {@link java.util.Collection collection}
                containing IDs of all root elements of the container
        """
        pass

    def setParent(self, itemId, newParentId):
        """<p>
        Sets the parent of an Item. The new parent item must exist and be
        able to have children. (
        <code>{@link #areChildrenAllowed(Object)} == true</code> ). It is
        also possible to detach a node from the hierarchy (and thus make it
        root) by setting the parent <code>null</code>.
        </p>

        <p>
        This operation is optional.
        </p>

        @param itemId
                   ID of the item to be set as the child of the Item
                   identified with <code>newParentId</code>
        @param newParentId
                   ID of the Item that's to be the new parent of the Item
                   identified with <code>itemId</code>
        @return <code>true</code> if the operation succeeded,
                <code>false</code> if not
        """
        pass

    def areChildrenAllowed(self, itemId):
        """Tests if the Item with given ID can have children.

        @param itemId
                   ID of the Item in the container whose child capability is
                   to be tested
        @return <code>true</code> if the specified Item exists in the
                Container and it can have children, <code>false</code> if
                it's not found from the container or it can't have children.
        """
        pass

    def setChildrenAllowed(self, itemId, areChildrenAllowed):
        """<p>
        Sets the given Item's capability to have children. If the Item
        identified with <code>itemId</code> already has children and
        <code>{@link #areChildrenAllowed(Object)}</code> is false this method
        fails and <code>false</code> is returned.
        </p>
        <p>
        The children must be first explicitly removed with
        {@link #setParent(Object itemId, Object newParentId)}or
        {@link com.vaadin.data.Container#removeItem(Object itemId)}.
        </p>

        <p>
        This operation is optional. If it is not implemented, the method
        always returns <code>false</code>.
        </p>

        @param itemId
                   ID of the Item in the container whose child capability is
                   to be set
        @param areChildrenAllowed
                   boolean value specifying if the Item can have children or
                   not
        @return <code>true</code> if the operation succeeded,
                <code>false</code> if not
        """
        pass

    def isRoot(self, itemId):
        """Tests if the Item specified with <code>itemId</code> is a root Item.
        The hierarchical container can have more than one root and must have
        at least one unless it is empty. The {@link #getParent(Object itemId)}
        method always returns <code>null</code> for root Items.

        @param itemId
                   ID of the Item whose root status is to be tested
        @return <code>true</code> if the specified Item is a root,
                <code>false</code> if not
        """
        pass

    def hasChildren(self, itemId):
        """<p>
        Tests if the Item specified with <code>itemId</code> has child Items
        or if it is a leaf. The {@link #getChildren(Object itemId)} method
        always returns <code>null</code> for leaf Items.
        </p>

        <p>
        Note that being a leaf does not imply whether or not an Item is
        allowed to have children.
        </p>
        .

        @param itemId
                   ID of the Item to be tested
        @return <code>true</code> if the specified Item has children,
                <code>false</code> if not (is a leaf)
        """
        pass

    def removeItem(self, itemId):
        """<p>
        Removes the Item identified by <code>ItemId</code> from the
        Container.
        </p>

        <p>
        Note that this does not remove any children the item might have.
        </p>

        @param itemId
                   ID of the Item to remove
        @return <code>true</code> if the operation succeeded,
                <code>false</code> if not
        """
        pass

class SimpleFilterable(Container, Serializable):
    """Interface that is implemented by containers which allow reducing their
    visible contents based on a set of filters. This interface has been
    renamed from {@link Filterable}, and implementing the new
    {@link Filterable} instead of or in addition to {@link SimpleFilterable}
    is recommended. This interface might be removed in future Vaadin
    versions.
    <p>
    When a set of filters are set, only items that match all the filters are
    included in the visible contents of the container. Still new items that
    do not match filters can be added to the container. Multiple filters can
    be added and the container remembers the state of the filters. When
    multiple filters are added, all filters must match for an item to be
    visible in the container.
    </p>
    <p>
    When an {@link Ordered} or {@link Indexed} container is filtered, all
    operations of these interfaces should only use the filtered contents and
    the filtered indices to the container.
    </p>
    <p>
    How filtering is performed when a {@link Hierarchical} container
    implements {@link SimpleFilterable} is implementation specific and should
    be documented in the implementing class.
    </p>
    <p>
    Adding items (if supported) to a filtered {@link Ordered} or
    {@link Indexed} container should insert them immediately after the
    indicated visible item. The unfiltered position of items added at index
    0, at index {@link com.vaadin.data.Container#size()} or at an undefined
    position is up to the implementation.
    </p>
    <p>
    The functionality of SimpleFilterable can be implemented using the
    {@link Filterable} API and {@link SimpleStringFilter}.
    </p>

    @since 5.0 (renamed from Filterable to SimpleFilterable in 6.6)
    """

    def addContainerFilter(self, propertyId, filterString, ignoreCase, onlyMatchPrefix):
        """Add a filter for given property.

        The API {@link Filterable#addContainerFilter(Filter)} is recommended
        instead of this method. A {@link SimpleStringFilter} can be used with
        the new API to implement the old string filtering functionality.

        The filter accepts items for which toString() of the value of the
        given property contains or starts with given filterString. Other
        items are not visible in the container when filtered.

        If a container has multiple filters, only items accepted by all
        filters are visible.

        @param propertyId
                   Property for which the filter is applied to.
        @param filterString
                   String that must match the value of the property
        @param ignoreCase
                   Determine if the casing can be ignored when comparing
                   strings.
        @param onlyMatchPrefix
                   Only match prefixes; no other matches are included.
        """
        pass

    def removeAllContainerFilters(self):
        """Remove all filters from all properties."""
        pass

    def removeContainerFilters(self, propertyId):
        """Remove all filters from the given property.

        @param propertyId
                   for which to remove filters
        """
        pass

class Filter(Serializable):
    """Filter interface for container filtering.

    If a filter does not support in-memory filtering,
    {@link #passesFilter(Item)} should throw
    {@link UnsupportedOperationException}.

    Lazy containers must be able to map filters to their internal
    representation (e.g. SQL or JPA 2.0 Criteria).

    An {@link UnsupportedFilterException} can be thrown by the container if a
    particular filter is not supported by the container.

    An {@link Filter} should implement {@link #equals(Object)} and
    {@link #hashCode()} correctly to avoid duplicate filter registrations
    etc.

    @see Filterable

    @since 6.6
    """

    def passesFilter(self, itemId, item):
        """Check if an item passes the filter (in-memory filtering).

        @param itemId
                   identifier of the item being filtered; may be null when
                   the item is being added to the container
        @param item
                   the item being filtered
        @return true if the item is accepted by this filter
        @throws UnsupportedOperationException
                    if the filter cannot be used for in-memory filtering
        """
        pass

    def appliesToProperty(self, propertyId):
        """Check if a change in the value of a property can affect the filtering
        result. May always return true, at the cost of performance.

        If the filter cannot determine whether it may depend on the property
        or not, should return true.

        @param propertyId
        @return true if the filtering result may/does change based on changes
                to the property identified by propertyId
        """
        pass

class Filterable(Container, Serializable):
    """Interface that is implemented by containers which allow reducing their
    visible contents based on a set of filters.
    <p>
    When a set of filters are set, only items that match all the filters are
    included in the visible contents of the container. Still new items that
    do not match filters can be added to the container. Multiple filters can
    be added and the container remembers the state of the filters. When
    multiple filters are added, all filters must match for an item to be
    visible in the container.
    </p>
    <p>
    When an {@link Ordered} or {@link Indexed} container is filtered, all
    operations of these interfaces should only use the filtered and sorted
    contents and the filtered indices to the container. Indices or item
    identifiers in the public API refer to the visible view unless otherwise
    stated. However, the <code>addItem*()</code> methods may add items that
    will be filtered out after addition or moved to another position based on
    sorting.
    </p>
    <p>
    How filtering is performed when a {@link Hierarchical} container
    implements {@link Filterable} is implementation specific and should be
    documented in the implementing class.
    </p>
    <p>
    Adding items (if supported) to a filtered {@link Ordered} or
    {@link Indexed} container should insert them immediately after the
    indicated visible item. However, the unfiltered position of items added
    at index 0, at index {@link com.vaadin.data.Container#size()} or at an
    undefined position is up to the implementation.
    </p>

    <p>
    This API replaces the old Filterable interface, renamed to
    {@link SimpleFilterable} in Vaadin 6.6.
    </p>

    @since 6.6
    """

    def addContainerFilter(self, filter):
        """Adds a filter for the container.

        If a container has multiple filters, only items accepted by all
        filters are visible.

        @throws UnsupportedFilterException
                    if the filter is not supported by the container
        """
        pass

    def removeContainerFilter(self, filter):
        """Removes a filter from the container.

        This requires that the equals() method considers the filters as
        equivalent (same instance or properly implemented equals() method).
        """
        pass

    def removeAllContainerFilters(self):
        """Remove all active filters from the container."""
        pass

class Viewer(Serializable):
    """Interface implemented by viewer classes capable of using a Container as a
    data source.
    """

    def setContainerDataSource(self, newDataSource):
        """Sets the Container that serves as the data source of the viewer.

        @param newDataSource
                   The new data source Item
        """
        pass

    def getContainerDataSource(self):
        """Gets the Container serving as the data source of the viewer.

        @return data source Container
        """
        pass

class Editor(Container.Viewer, Serializable):
    """<p>
    Interface implemented by the editor classes supporting editing the
    Container. Implementing this interface means that the Container serving
    as the data source of the editor can be modified through it.
    </p>
    <p>
    Note that not implementing the <code>Container.Editor</code> interface
    does not restrict the class from editing the Container contents
    internally.
    </p>
    """
    # Contents change event
    pass

class ItemSetChangeEvent(Serializable):
    """An <code>Event</code> object specifying the Container whose Item set has
    changed (items added, removed or reordered).

    A simple property value change is not an item set change.
    """

    def getContainer(self):
        """Gets the Property where the event occurred.

        @return source of the event
        """
        pass

class ItemSetChangeListener(Serializable):
    """Container Item set change listener interface.

    An item set change refers to addition, removal or reordering of items in
    the container. A simple property value change is not an item set change.
    """

    def containerItemSetChange(self, event):
        """Lets the listener know a Containers visible (filtered and/or sorted,
        if applicable) Item set has changed.

        @param event
                   change event text
        """
        pass

class ItemSetChangeNotifier(Serializable):
    """The interface for adding and removing <code>ItemSetChangeEvent</code>
    listeners. By implementing this interface a class explicitly announces
    that it will generate a <code>ItemSetChangeEvent</code> when its contents
    are modified.

    An item set change refers to addition, removal or reordering of items in
    the container. A simple property value change is not an item set change.

    <p>
    Note: The general Java convention is not to explicitly declare that a
    class generates events, but to directly define the
    <code>addListener</code> and <code>removeListener</code> methods. That
    way the caller of these methods has no real way of finding out if the
    class really will send the events, or if it just defines the methods to
    be able to implement an interface.
    </p>
    """
    # Property set change event

    def addListener(self, listener):
        """Adds an Item set change listener for the object.

        @param listener
                   listener to be added
        """
        pass

    def removeListener(self, listener):
        """Removes the Item set change listener from the object.

        @param listener
                   listener to be removed
        """
        pass

class PropertySetChangeEvent(Serializable):
    """An <code>Event</code> object specifying the Container whose Property set
    has changed.

    A property set change means the addition, removal or other structural
    changes to the properties of a container. Changes concerning the set of
    items in the container and their property values are not property set
    changes.
    """

    def getContainer(self):
        """Retrieves the Container whose contents have been modified.

        @return Source Container of the event.
        """
        pass

class PropertySetChangeListener(Serializable):
    """The listener interface for receiving <code>PropertySetChangeEvent</code>
    objects.

    A property set change means the addition, removal or other structural
    change of the properties (supported property IDs) of a container. Changes
    concerning the set of items in the container and their property values
    are not property set changes.
    """

    def containerPropertySetChange(self, event):
        """Notifies this listener that the set of property IDs supported by the
        Container has changed.

        @param event
                   Change event.
        """
        pass

class PropertySetChangeNotifier(Serializable):
    """<p>
    The interface for adding and removing <code>PropertySetChangeEvent</code>
    listeners. By implementing this interface a class explicitly announces
    that it will generate a <code>PropertySetChangeEvent</code> when the set
    of property IDs supported by the container is modified.
    </p>

    <p>
    A property set change means the addition, removal or other structural
    changes to the properties of a container. Changes concerning the set of
    items in the container and their property values are not property set
    changes.
    </p>

    <p>
    Note that the general Java convention is not to explicitly declare that a
    class generates events, but to directly define the
    <code>addListener</code> and <code>removeListener</code> methods. That
    way the caller of these methods has no real way of finding out if the
    class really will send the events, or if it just defines the methods to
    be able to implement an interface.
    </p>
    """

    def addListener(self, listener):
        """Registers a new Property set change listener for this Container.

        @param listener
                   The new Listener to be registered
        """
        pass

    def removeListener(self, listener):
        """Removes a previously registered Property set change listener.

        @param listener
                   Listener to be removed
        """
        pass
