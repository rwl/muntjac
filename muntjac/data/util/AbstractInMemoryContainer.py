# Copyright (C) 2010 IT Mill Ltd.
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

from muntjac.data.util.DefaultItemSorter import DefaultItemSorter
from muntjac.data.Container import Container, Indexed, ItemSetChangeNotifier,\
    Sortable
from muntjac.data.util.AbstractContainer import AbstractContainer
from muntjac.data.util.ListSet import ListSet


class AbstractInMemoryContainer(AbstractContainer, ItemSetChangeNotifier,
                                Container, Indexed):
    """Abstract {@link Container} class that handles common functionality for
    in-memory containers. Concrete in-memory container classes can either inherit
    this class, inherit {@link AbstractContainer}, or implement the
    {@link Container} interface directly.

    Adding and removing items (if desired) must be implemented in subclasses by
    overriding the appropriate add*Item() and remove*Item() and removeAllItems()
    methods, calling the corresponding
    {@link #internalAddItemAfter(Object, Object, Item)},
    {@link #internalAddItemAt(int, Object, Item)},
    {@link #internalAddItemAtEnd(Object, Item, boolean)},
    {@link #internalRemoveItem(Object)} and {@link #internalRemoveAllItems()}
    methods.

    By default, adding and removing container properties is not supported, and
    subclasses need to implement {@link #getContainerPropertyIds()}. Optionally,
    subclasses can override {@link #addContainerProperty(Object, Class, Object)}
    and {@link #removeContainerProperty(Object)} to implement them.

    Features:
    <ul>
    <li> {@link Container.Ordered}
    <li> {@link Container.Indexed}
    <li> {@link Filterable} and {@link SimpleFilterable} (internal implementation,
    does not implement the interface directly)
    <li> {@link Sortable} (internal implementation, does not implement the
    interface directly)
    </ul>

    To implement {@link Sortable}, subclasses need to implement
    {@link #getSortablePropertyIds()} and call the superclass method
    {@link #sortContainer(Object[], boolean[])} in the method
    <code>sort(Object[], boolean[])</code>.

    To implement {@link Filterable}, subclasses need to implement the methods
    {@link Filterable#addContainerFilter(com.vaadin.data.Container.Filter)}
    (calling {@link #addFilter(Filter)}),
    {@link Filterable#removeAllContainerFilters()} (calling
    {@link #removeAllFilters()}) and
    {@link Filterable#removeContainerFilter(com.vaadin.data.Container.Filter)}
    (calling {@link #removeFilter(com.vaadin.data.Container.Filter)}).

    To implement {@link SimpleFilterable}, subclasses also need to implement the
    methods
    {@link SimpleFilterable#addContainerFilter(Object, String, boolean, boolean)}
    and {@link SimpleFilterable#removeContainerFilters(Object)} calling
    {@link #addFilter(com.vaadin.data.Container.Filter)} and
    {@link #removeFilters(Object)} respectively.

    @param <ITEMIDTYPE>
               the class of item identifiers in the container, use Object if can
               be any class
    @param <PROPERTYIDCLASS>
               the class of property identifiers for the items in the container,
               use Object if can be any class
    @param <ITEMCLASS>
               the (base) class of the Item instances in the container, use
               {@link Item} if unknown

    @since 6.6
    """

    def __init__(self):
        """Constructor for an abstract in-memory container."""

        # An ordered {@link List} of all item identifiers in the container,
        # including those that have been filtered out.
        #
        # Must not be null.
        self._allItemIds = None

        # An ordered {@link List} of item identifiers in the container after
        # filtering, excluding those that have been filtered out.
        #
        # This is what the external API of the {@link Container} interface and its
        # subinterfaces shows (e.g. {@link #size()}, {@link #nextItemId(Object)}).
        #
        # If null, the full item id list is used instead.
        self._filteredItemIds = None

        # Filters that are applied to the container to limit the items visible in
        # it
        self._filters = set()

        # The item sorter which is used for sorting the container.
        self._itemSorter = DefaultItemSorter()

        # Container interface methods with more specific return class
        # default implementation, can be overridden
        self.setAllItemIds( ListSet() )


    def getItem(self, itemId):
        if self.containsId(itemId):
            return self.getUnfilteredItem(itemId)
        else:
            return None


    def getUnfilteredItem(self, itemId):
        """Get an item even if filtered out.

        For internal use only.

        @param itemId
        @return
        """
        pass


    # cannot override getContainerPropertyIds() and getItemIds(): if subclass
    # uses Object as ITEMIDCLASS or PROPERTYIDCLASS, Collection<Object> cannot
    # be cast to Collection<MyInterface>
    # public abstract Collection<PROPERTYIDCLASS> getContainerPropertyIds();
    # public abstract Collection<ITEMIDCLASS> getItemIds();
    # Container interface method implementations


    def size(self):
        return len(self.getVisibleItemIds())


    def containsId(self, itemId):
        # only look at visible items after filtering
        if itemId is None:
            return False
        else:
            return itemId in self.getVisibleItemIds()


    def getItemIds(self):
        return list(self.getVisibleItemIds())


    def nextItemId(self, itemId):
        index = self.indexOfId(itemId)
        if index >= 0 and index < len(self) - 1:
            return self.getIdByIndex(index + 1)
        else:
            # out of bounds
            return None


    def prevItemId(self, itemId):
        index = self.indexOfId(itemId)
        if index > 0:
            return self.getIdByIndex(index - 1)
        else:
            # out of bounds
            return None


    def firstItemId(self):
        if len(self) > 0:
            return self.getIdByIndex(0)
        else:
            return None


    def lastItemId(self):
        if len(self) > 0:
            return self.getIdByIndex(len(self) - 1)
        else:
            return None


    def isFirstId(self, itemId):
        if itemId is None:
            return False

        return itemId == self.firstItemId()


    def isLastId(self, itemId):
        if itemId is None:
            return False

        return itemId == self.lastItemId()


    def getIdByIndex(self, index):
        return self.getVisibleItemIds().get(index)


    def indexOfId(self, itemId):
        return self.getVisibleItemIds().index(itemId)


    def addItemAt(self, index, newItemId=None):
        raise NotImplementedError, 'Adding items not supported. Override the relevant addItem*() methods if required as specified in AbstractInMemoryContainer javadoc.'


    def addItemAfter(self, previousItemId, newItemId=None):
        raise NotImplementedError, 'Adding items not supported. Override the relevant addItem*() methods if required as specified in AbstractInMemoryContainer javadoc.'


    def addItem(self, itemId=None):
        raise NotImplementedError, 'Adding items not supported. Override the relevant addItem*() methods if required as specified in AbstractInMemoryContainer javadoc.'


    def removeItem(self, itemId):
        raise NotImplementedError, 'Removing items not supported. Override the removeItem() method if required as specified in AbstractInMemoryContainer javadoc.'


    def removeAllItems(self):
        raise NotImplementedError, 'Removing items not supported. Override the removeAllItems() method if required as specified in AbstractInMemoryContainer javadoc.'


    def addContainerProperty(self, propertyId, typ, defaultValue):
        raise NotImplementedError, 'Adding container properties not supported. Override the addContainerProperty() method if required.'


    def removeContainerProperty(self, propertyId):
        raise NotImplementedError, 'Removing container properties not supported. Override the addContainerProperty() method if required.'


    def addListener(self, listener):
        super(AbstractInMemoryContainer, self).addListener(listener)


    def removeListener(self, listener):
        super(AbstractInMemoryContainer, self).removeListener(listener)


    def filterAll(self):
        """Filter the view to recreate the visible item list from the unfiltered
        items, and send a notification if the set of visible items changed in any
        way.
        """
        if self.doFilterContainer(not self.getFilters().isEmpty()):
            self.fireItemSetChange()


    def doFilterContainer(self, hasFilters):
        """Filters the data in the container and updates internal data structures.
        This method should reset any internal data structures and then repopulate
        them so {@link #getItemIds()} and other methods only return the filtered
        items.

        @param hasFilters
                   true if filters has been set for the container, false
                   otherwise
        @return true if the item set has changed as a result of the filtering
        """
        if not hasFilters:
            changed = len(self.getAllItemIds()) != len(self.getVisibleItemIds())
            self.setFilteredItemIds(None)
            return changed

        # Reset filtered list
        originalFilteredItemIds = self.getFilteredItemIds()
        wasUnfiltered = False
        if originalFilteredItemIds is None:
            originalFilteredItemIds = list()
            wasUnfiltered = True

        self.setFilteredItemIds(ListSet())

        # Filter
        equal = True
        origIt = iter(originalFilteredItemIds)
        for idd in self.getAllItemIds():
            if self.passesFilters(idd):
                # filtered list comes from the full list, can use ==
                try:
                    equal = equal and origIt.next() == idd  # FIXME: hasNext
                except StopIteration:
                    equal = False

                self.getFilteredItemIds().append(idd)

        try:
            origIt.next()
            result = True
        except StopIteration:
            result = (wasUnfiltered and len(self.getAllItemIds() > 0)) or (not equal)  # FIXME: hasNext

        return result


    def passesFilters(self, itemId):
        """Checks if the given itemId passes the filters set for the container. The
        caller should make sure the itemId exists in the container. For
        non-existing itemIds the behavior is undefined.

        @param itemId
                   An itemId that exists in the container.
        @return true if the itemId passes all filters or no filters are set,
                false otherwise.
        """
        item = self.getUnfilteredItem(itemId)
        if len(self.getFilters()) == 0:
            return True

        for f in self.getFilters():
            if not f.passesFilter(itemId, item):
                return False

        return True


    def addFilter(self, fltr):
        """Adds a container filter and re-filter the view.

        The filter must implement Filter and its sub-filters (if any) must also
        be in-memory filterable.

        This can be used to implement
        {@link Filterable#addContainerFilter(com.vaadin.data.Container.Filter)}
        and optionally also
        {@link SimpleFilterable#addContainerFilter(Object, String, boolean, boolean)}
        (with {@link SimpleStringFilter}).

        Note that in some cases, incompatible filters cannot be detected when
        added and an {@link UnsupportedFilterException} may occur when performing
        filtering.

        @throws UnsupportedFilterException
                    if the filter is detected as not supported by the container
        """
        self.getFilters().add(fltr)
        self.filterAll()


    def removeFilter(self, fltr):
        """Remove a specific container filter and re-filter the view (if necessary).

        This can be used to implement
        {@link Filterable#removeContainerFilter(com.vaadin.data.Container.Filter)}
        .
        """
        for f in self.getFilters():
            if f == fltr:
                self.getFilters().remove()
                self.filterAll()
                return


    def removeAllFilters(self):
        """Remove all container filters for all properties and re-filter the view.

        This can be used to implement
        {@link Filterable#removeAllContainerFilters()}.
        """
        if len(self.getFilters()) == 0:
            return

        self.getFilters().clear()
        self.filterAll()


    def isPropertyFiltered(self, propertyId):
        """Checks if there is a filter that applies to a given property.

        @param propertyId
        @return true if there is an active filter for the property
        """
        if len(self.getFilters()) == 0 or (propertyId is None):
            return False

        for f in self.getFilters():
            if f.appliesToProperty(propertyId):
                return True

        return False


    def removeFilters(self, propertyId):
        """Remove all container filters for a given property identifier and
        re-filter the view. This also removes filters applying to multiple
        properties including the one identified by propertyId.

        This can be used to implement
        {@link Filterable#removeContainerFilters(Object)}.

        @param propertyId
        @return Collection<Filter> removed filters
        """
        if len(self.getFilters()) == 0 or (propertyId is None):
            return list()

        removedFilters = list()
        for f in self.getFilters():
            if f.appliesToProperty(propertyId):
                removedFilters.append(f)
                self.getFilters().remove()

        if len(removedFilters) > 0:
            self.filterAll()
            return removedFilters

        return list()


    def getItemSorter(self):
        """Returns the ItemSorter used for comparing items in a sort. See
        {@link #setItemSorter(ItemSorter)} for more information.

        @return The ItemSorter used for comparing two items in a sort.
        """
        return self._itemSorter


    def setItemSorter(self, itemSorter):
        """Sets the ItemSorter used for comparing items in a sort. The
        {@link ItemSorter#compare(Object, Object)} method is called with item ids
        to perform the sorting. A default ItemSorter is used if this is not
        explicitly set.

        @param itemSorter
                   The ItemSorter used for comparing two items in a sort (not
                   null).
        """
        self._itemSorter = itemSorter


    def sortContainer(self, propertyId, ascending):
        """Sort base implementation to be used to implement {@link Sortable}.

        Subclasses should call this from a public
        {@link #sort(Object[], boolean[])} method when implementing Sortable.

        @see com.vaadin.data.Container.Sortable#sort(java.lang.Object[],
             boolean[])
        """
        if not isinstance(self, Sortable):
            raise NotImplementedError, 'Cannot sort a Container that does not implement Sortable'

        # Set up the item sorter for the sort operation
        self.getItemSorter().setSortProperties(self, propertyId, ascending)

        # Perform the actual sort
        self.doSort()

        # Post sort updates
        if self.isFiltered():
            self.filterAll()
        else:
            self.fireItemSetChange()


    def doSort(self):
        """Perform the sorting of the data structures in the container. This is
        invoked when the <code>itemSorter</code> has been prepared for the sort
        operation. Typically this method calls
        <code>Collections.sort(aCollection, getItemSorter())</code> on all arrays
        (containing item ids) that need to be sorted.
        """
        sorted(self.getAllItemIds(), key=self.getItemSorter())  # FIXME: sort


    def getSortablePropertyIds(self):
        """Returns the sortable property identifiers for the container. Can be used
        to implement {@link Sortable#getSortableContainerPropertyIds()}.
        """
        sortables = list()

        for propertyId in self.getContainerPropertyIds():
            propertyType = self.getType(propertyId)
            if hasattr(propertyType, '__eq__') or isinstance(propertyType, (int, float, bool)):  # FIXME: Comparable isPrimitive
                sortables.append(propertyId)

        return sortables


    def internalRemoveAllItems(self):
        """Removes all items from the internal data structures of this class. This
        can be used to implement {@link #removeAllItems()} in subclasses.

        No notification is sent, the caller has to fire a suitable item set
        change notification.
        """
        # Removes all Items
        self.getAllItemIds().clear()
        if self.isFiltered():
            self.getFilteredItemIds().clear()


    def internalRemoveItem(self, itemId):
        """Removes a single item from the internal data structures of this class.
        This can be used to implement {@link #removeItem(Object)} in subclasses.

        No notification is sent, the caller has to fire a suitable item set
        change notification.

        @param itemId
                   the identifier of the item to remove
        @return true if an item was successfully removed, false if failed to
                remove or no such item
        """
        if itemId is None:
            return False

        result = self.getAllItemIds().remove(itemId)
        if result and self.isFiltered():
            self.getFilteredItemIds().remove(itemId)

        return result


    def internalAddAt(self, position, itemId, item):
        """Adds the bean to all internal data structures at the given position.
        Fails if an item with itemId is already in the container. Returns a the
        item if it was added successfully, null otherwise.

        <p>
        Caller should initiate filtering after calling this method.
        </p>

        For internal use only - subclasses should use
        {@link #internalAddItemAtEnd(Object, Item, boolean)},
        {@link #internalAddItemAt(int, Object, Item, boolean)} and
        {@link #internalAddItemAfter(Object, Object, Item, boolean)} instead.

        @param position
                   The position at which the item should be inserted in the
                   unfiltered collection of items
        @param itemId
                   The item identifier for the item to insert
        @param item
                   The item to insert

        @return ITEMCLASS if the item was added successfully, null otherwise
        """
        if position < 0 or position > len(self.getAllItemIds()) \
                or itemId is None or item is None:
            return None

        # Make sure that the item has not been added previously
        if itemId in self.getAllItemIds():
            return None

        # "filteredList" will be updated in filterAll() which should be invoked
        # by the caller after calling this method.
        self.getAllItemIds().add(position, itemId)
        self.registerNewItem(position, itemId, item)

        return item


    def internalAddItemAtEnd(self, newItemId, item, fltr):
        """Add an item at the end of the container, and perform filtering if
        necessary. An event is fired if the filtered view changes.

        @param newItemId
        @param item
                   new item to add
        @param filter
                   true to perform filtering and send event after adding the
                   item, false to skip these operations for batch inserts - if
                   false, caller needs to make sure these operations are
                   performed at the end of the batch
        @return item added or null if no item was added
        """
        newItem = self.internalAddAt(len(self.getAllItemIds()), newItemId, item)

        if newItem is not None and fltr:
            # TODO filter only this item, use fireItemAdded()
            self.filterAll()
            if not self.isFiltered():
                # TODO hack: does not detect change in filterAll() in this case
                self.fireItemAdded(self.indexOfId(newItemId), newItemId, item)

        return newItem


    def internalAddItemAfter(self, previousItemId, newItemId, item, fltr):
        """Add an item after a given (visible) item, and perform filtering. An event
        is fired if the filtered view changes.

        The new item is added at the beginning if previousItemId is null.

        @param previousItemId
                   item id of a visible item after which to add the new item, or
                   null to add at the beginning
        @param newItemId
        @param item
                   new item to add
        @param filter
                   true to perform filtering and send event after adding the
                   item, false to skip these operations for batch inserts - if
                   false, caller needs to make sure these operations are
                   performed at the end of the batch
        @return item added or null if no item was added
        """
        # only add if the previous item is visible
        newItem = None
        if previousItemId is None:
            newItem = self.internalAddAt(0, newItemId, item)
        elif self.containsId(previousItemId):
            newItem = self.internalAddAt(self.getAllItemIds().index(previousItemId) + 1,
                                         newItemId, item)

        if newItem is not None and fltr:
            # TODO filter only this item, use fireItemAdded()
            self.filterAll()
            if not self.isFiltered():
                # TODO hack: does not detect change in filterAll() in this case
                self.fireItemAdded(self.indexOfId(newItemId), newItemId, item)

        return newItem


    def internalAddItemAt(self, index, newItemId, item, fltr):
        """Add an item at a given (visible after filtering) item index, and perform
        filtering. An event is fired if the filtered view changes.

        @param index
                   position where to add the item (visible/view index)
        @param newItemId
        @param item
                   new item to add
        @param filter
                   true to perform filtering and send event after adding the
                   item, false to skip these operations for batch inserts - if
                   false, caller needs to make sure these operations are
                   performed at the end of the batch
        @return item added or null if no item was added
        """
        if (index < 0) or (index > len(self)):
            return None
        elif index == 0:
            # add before any item, visible or not
            return self.internalAddItemAfter(None, newItemId, item, fltr)
        else:
            # if index==size(), adds immediately after last visible item
            return self.internalAddItemAfter(self.getIdByIndex(index - 1),
                                             newItemId, item, fltr)


    def registerNewItem(self, position, itemId, item):
        """Registers a new item as having been added to the container. This can
        involve storing the item or any relevant information about it in internal
        container-specific collections if necessary, as well as registering
        listeners etc.

        The full identifier list in {@link AbstractInMemoryContainer} has already
        been updated to reflect the new item when this method is called.

        @param position
        @param itemId
        @param item
        """
        pass


    def fireItemAdded(self, position, itemId, item):
        """Notify item set change listeners that an item has been added to the
        container.

        Unless subclasses specify otherwise, the default notification indicates a
        full refresh.

        @param postion
                   position of the added item in the view (if visible)
        @param itemId
                   id of the added item
        @param item
                   the added item
        """
        self.fireItemSetChange()


    def fireItemRemoved(self, position, itemId):
        """Notify item set change listeners that an item has been removed from the
        container.

        Unless subclasses specify otherwise, the default notification indicates a
        full refresh.

        @param postion
                   position of the removed item in the view prior to removal (if
                   was visible)
        @param itemId
                   id of the removed item, of type {@link Object} to satisfy
                   {@link Container#removeItem(Object)} API
        """
        self.fireItemSetChange()


    def getVisibleItemIds(self):
        """Returns the internal list of visible item identifiers after filtering.

        For internal use only.
        """
        if self.isFiltered():
            return self.getFilteredItemIds()
        else:
            return self.getAllItemIds()


    def isFiltered(self):
        """Returns true is the container has active filters.

        @return true if the container is currently filtered
        """
        return self._filteredItemIds is not None


    def setFilteredItemIds(self, filteredItemIds):
        """Internal helper method to set the internal list of filtered item
        identifiers. Should not be used outside this class except for
        implementing clone(), may disappear from future versions.

        @param filteredItemIds
        """
        self._filteredItemIds = filteredItemIds


    def getFilteredItemIds(self):
        """Internal helper method to get the internal list of filtered item
        identifiers. Should not be used outside this class except for
        implementing clone(), may disappear from future versions - use
        {@link #getVisibleItemIds()} in other contexts.

        @return List<ITEMIDTYPE>
        """
        return self._filteredItemIds


    def setAllItemIds(self, allItemIds):
        """Internal helper method to set the internal list of all item identifiers.
        Should not be used outside this class except for implementing clone(),
        may disappear from future versions.

        @param allItemIds
        """
        self._allItemIds = allItemIds


    def getAllItemIds(self):
        """Internal helper method to get the internal list of all item identifiers.
        Avoid using this method outside this class, may disappear in future
        versions.

        @return List<ITEMIDTYPE>
        """
        return self._allItemIds


    def setFilters(self, filters):
        """Set the internal collection of filters without performing filtering.

        This method is mostly for internal use, use
        {@link #addFilter(com.vaadin.data.Container.Filter)} and
        <code>remove*Filter*</code> (which also re-filter the container) instead
        when possible.

        @param filters
        """
        self._filters = filters


    def getFilters(self):
        """Returns the internal collection of filters. The returned collection
        should not be modified by callers outside this class.

        @return Set<Filter>
        """
        return self._filters
