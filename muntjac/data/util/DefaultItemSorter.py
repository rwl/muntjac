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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.data.util.ItemSorter import (ItemSorter,)
# from com.vaadin.data.Container.Sortable import (Sortable,)
# from java.io.Serializable import (Serializable,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Comparator import (Comparator,)
# from java.util.List import (List,)


class DefaultItemSorter(ItemSorter):
    """Provides a default implementation of an ItemSorter. The
    <code>DefaultItemSorter</code> adheres to the
    {@link Sortable#sort(Object[], boolean[])} rules and sorts the container
    according to the properties given using
    {@link #setSortProperties(Sortable, Object[], boolean[])}.
    <p>
    A Comparator is used for comparing the individual <code>Property</code>
    values. The comparator can be set using the constructor. If no comparator is
    provided a default comparator is used.
    """
    _sortPropertyIds = None
    _sortDirections = None
    _container = None
    _propertyValueComparator = None

    def __init__(self, *args):
        """Constructs a DefaultItemSorter using the default <code>Comparator</code>
        for comparing <code>Property</code>values.
        ---
        Constructs a DefaultItemSorter which uses the <code>Comparator</code>
        indicated by the <code>propertyValueComparator</code> parameter for
        comparing <code>Property</code>values.

        @param propertyValueComparator
                   The comparator to use when comparing individual
                   <code>Property</code> values
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.__init__(self.DefaultPropertyValueComparator())
        elif _1 == 1:
            propertyValueComparator, = _0
            self._propertyValueComparator = propertyValueComparator
        else:
            raise ARGERROR(0, 1)

    # (non-Javadoc)
    # 
    # @see com.vaadin.data.util.ItemSorter#compare(java.lang.Object,
    # java.lang.Object)

    def compare(self, o1, o2):
        item1 = self._container.getItem(o1)
        item2 = self._container.getItem(o2)
        # Items can be null if the container is filtered. Null is considered
        # "less" than not-null.

        if item1 is None:
            if item2 is None:
                return 0
            else:
                return 1
        elif item2 is None:
            return -1
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(self._sortPropertyIds)):
                break
            result = self.compareProperty(self._sortPropertyIds[i], self._sortDirections[i], item1, item2)
            # If order can be decided
            if result != 0:
                return result
        return 0

    def compareProperty(self, propertyId, sortDirection, item1, item2):
        """Compares the property indicated by <code>propertyId</code> in the items
        indicated by <code>item1</code> and <code>item2</code> for order. Returns
        a negative integer, zero, or a positive integer as the property value in
        the first item is less than, equal to, or greater than the property value
        in the second item. If the <code>sortDirection</code> is false the
        returned value is negated.
        <p>
        The comparator set for this <code>DefaultItemSorter</code> is used for
        comparing the two property values.

        @param propertyId
                   The property id for the property that is used for comparison.
        @param sortDirection
                   The direction of the sort. A false value negates the result.
        @param item1
                   The first item to compare.
        @param item2
                   The second item to compare.
        @return a negative, zero, or positive integer if the property value in
                the first item is less than, equal to, or greater than the
                property value in the second item. Negated if
                {@code sortDirection} is false.
        """
        # Get the properties to compare
        # (non-Javadoc)
        # 
        # @see
        # com.vaadin.data.util.ItemSorter#setSortProperties(com.vaadin.data.Container
        # .Sortable, java.lang.Object[], boolean[])

        property1 = item1.getItemProperty(propertyId)
        property2 = item2.getItemProperty(propertyId)
        # Get the values to compare
        value1 = None if property1 is None else property1.getValue()
        value2 = None if property2 is None else property2.getValue()
        # Result of the comparison
        r = 0
        if sortDirection:
            r = self._propertyValueComparator.compare(value1, value2)
        else:
            r = self._propertyValueComparator.compare(value2, value1)
        return r

    def setSortProperties(self, container, propertyId, ascending):
        self._container = container
        # Removes any non-sortable property ids
        ids = list()
        orders = list()
        sortable = container.getSortableContainerPropertyIds()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(propertyId)):
                break
            if sortable.contains(propertyId[i]):
                ids.add(propertyId[i])
                orders.add(Boolean.valueOf.valueOf(ascending[i] if i < len(ascending) else True))
        self._sortPropertyIds = list(ids)
        self._sortDirections = [None] * len(orders)
        _1 = True
        i = 0
        while True:
            if _1 is True:
                _1 = False
            else:
                i += 1
            if not (i < len(self._sortDirections)):
                break
            self._sortDirections[i] = orders[i].booleanValue()

    class DefaultPropertyValueComparator(Comparator, Serializable):
        """Provides a default comparator used for comparing {@link Property} values.
        The <code>DefaultPropertyValueComparator</code> assumes all objects it
        compares can be cast to Comparable.
        """

        def compare(self, o1, o2):
            r = 0
            # Normal non-null comparison
            if o1 is not None and o2 is not None:
                # Assume the objects can be cast to Comparable, throw
                # ClassCastException otherwise.
                r = o1.compareTo(o2)
            elif o1 == o2:
                # Objects are equal if both are null
                r = 0
            elif o1 is None:
                r = -1
                # null is less than non-null
            else:
                r = 1
                # non-null is greater than null
            return r
