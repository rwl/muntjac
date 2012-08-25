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

"""Provides a default implementation of an IItemSorter."""

from muntjac.data.util.item_sorter import IItemSorter


class DefaultItemSorter(IItemSorter):
    """Provides a default implementation of an IItemSorter. The
    C{DefaultItemSorter} adheres to the L{ISortable.sort} rules and sorts
    the container according to the properties given using L{setSortProperties}.

    A Comparator is used for comparing the individual C{Property}
    values. The comparator can be set using the constructor. If no comparator
    is provided a default comparator is used.
    """

    def __init__(self, propertyValueComparator=None):
        """Constructs a DefaultItemSorter which uses the C{Comparator}
        indicated by the C{propertyValueComparator} parameter for
        comparing C{Property} values. Uses the default C{Comparator}
        for comparing C{Property} values if propertyValueComparator is None.

        @param propertyValueComparator:
                   The comparator to use when comparing individual
                   C{Property} values
        """
        self._sortPropertyIds = None
        self._sortDirections = None
        self._container = None
        self._propertyValueComparator = None

        if propertyValueComparator is None:
            DefaultItemSorter.__init__(self, DefaultPropertyValueComparator())
        else:
            self._propertyValueComparator = propertyValueComparator


    def __call__(self, o1, o2):
        return self.compare(o1, o2)


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

        for i in range(len(self._sortPropertyIds)):
            result = self.compareProperty(self._sortPropertyIds[i],
                    self._sortDirections[i], item1, item2)

            # If order can be decided
            if result != 0:
                return result

        return 0


    def compareProperty(self, propertyId, sortDirection, item1, item2):
        """Compares the property indicated by C{propertyId} in the items
        indicated by C{item1} and C{item2} for order. Returns a negative
        integer, zero, or a positive integer as the property value in
        the first item is less than, equal to, or greater than the property
        value in the second item. If the C{sortDirection} is false the
        returned value is negated.

        The comparator set for this C{DefaultItemSorter} is used for
        comparing the two property values.

        @param propertyId:
                   The property id for the property that is used for comparison.
        @param sortDirection:
                   The direction of the sort. A false value negates the result.
        @param item1:
                   The first item to compare.
        @param item2:
                   The second item to compare.
        @return: a negative, zero, or positive integer if the property value in
                the first item is less than, equal to, or greater than the
                property value in the second item. Negated if
                C{sortDirection} is false.
        """
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

        for i in range(len(propertyId)):
            if propertyId[i] in sortable:
                ids.append(propertyId[i])
                order = bool(ascending[i]) if i < len(ascending) else True
                orders.append(order)

        self._sortPropertyIds = list(ids)
        self._sortDirections = [None] * len(orders)

        for i in range(len(self._sortDirections)):
            self._sortDirections[i] = bool( orders[i] )


class DefaultPropertyValueComparator(object):
    """Provides a default comparator used for comparing L{Property} values.
    The C{DefaultPropertyValueComparator} assumes all objects it compares
    can be cast to Comparable.
    """

    def __call__(self, o1, o2):
        return self.compare(o1, o1)


    def compare(self, o1, o2):
        r = 0
        # Normal non-null comparison
        if o1 is not None and o2 is not None:
            # Assume the objects to be comparable
            r = cmp(o1, o2)
        elif o1 == o2:
            # Objects are equal if both are null
            r = 0
        elif o1 is None:
            # null is less than non-null
            r = -1
        else:
            # non-null is greater than null
            r = 1
        return r
