# Copyright (C) 2010 Abo Akademi University
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
#
# Note: This is a modified file from GAEContainer. For further information
#       please visit http://vaadin.com/directory#addon/gaecontainer.

from muntjac.data.util.gaecontainer.query.IncompatibleFilterException \
    import IncompatibleFilterException


class QueryRepresentation(object):
    """Internal representation of a query.

    Only used internally.

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    def __init__(self, kind):
        # *exception if already set filters does not work with new sort order
        self._properties = list()
        self._filters = dict()
        self._kind = kind
        self._query = None
        self._properties.add(QueryProperty('__key__', True))


    def sort(self, propertyId, ascending):
        self._properties.clear()

        for i in range(len(propertyId)):
            self._properties.add( QueryProperty(propertyId[i], ascending[i]) )

        self._properties.add(self.QueryProperty('__key__', True))


    def getQueryIdentifier(self):
        # could find some more compact way of uniquely represting queries
        queryIdentifier = self._kind
        for property in self._properties:
            queryIdentifier += str(property.propertyId)
            if property.direction == SortDirection.DESCENDING:
                queryIdentifier += 'DESC'

        for propertyId in self._filters:
            queryIdentifier += str(propertyId)
            for filter in self._filters[propertyId]:
                queryIdentifier += str(filter)

        return queryIdentifier


    def getFilterRepresentation(self):
        # does not care about sort orders
        filterIdentifier = self._kind

        for propertyId in self._filters:
            filterIdentifier += str(propertyId)
            for fltr in self._filters[propertyId]:
                filterIdentifier += str(fltr)

        return filterIdentifier


    def getKind(self):
        return self._kind


    def getQuery(self, order=None, inverted=False):
        if order is None:
            return self.doGetQuery(False)
        else:
            # get query with sort criteria applied only to property of order
            # or null if there is no criteria of order order
            sortCriteria = self._properties.get(order)
            if sortCriteria is None:
                return None
            else:
                self._query = Query(self._kind)
                self.addSortOrders(self._query, inverted,
                        self._properties.subList(order, len(self._properties)))
                return self._query


    def getQueryFromEnd(self):
        return self.doGetQuery(True)


    def sortQuantity(self):
        return len(self._properties)


    def doGetQuery(self, inverted):
        self._query = Query(self._kind)
        self.addSortOrders(self._query, inverted, self._properties)
        self.addFilters(self._query)
        return self._query


    def addSortOrders(self, q, inverted, properties):
        if inverted:
            for sortCriteria in properties:
                direction = sortCriteria.direction
                if direction == SortDirection.ASCENDING:
                    q.addSort(str(sortCriteria.propertyId),
                        SortDirection.DESCENDING)
                if direction == SortDirection.DESCENDING:
                    q.addSort(str(sortCriteria.propertyId),
                            SortDirection.ASCENDING)
        else:
            for sortCriteria in properties:
                if sortCriteria.direction is not None:
                    q.addSort(str(sortCriteria.propertyId),
                            sortCriteria.direction)


    def addFilters(self, q):
        for propertyId in self._filters:
            for fltr in self._filters[propertyId]:
                q.addFilter(str(propertyId), fltr.operator, fltr.value)


    def addFilter(self, propertyId, operator, value):
        # not checking if propertyId exists or if value is of correct type,
        # this should be checked in container

        self.validate(propertyId, operator)

        fltr = Filter(operator, value)
        if propertyId in self._filters:
            self._filters[propertyId].add(fltr)
        else:
            f = [fltr]
            self._filters[propertyId] = f


    def validate(self, propertyId, operator):
        if not (FilterOperator.EQUAL == operator):  # its a inequality operator

            # Inequality Filters Are Allowed On One Property Only
            for filterKey in self._filters:
                filterList = self._filters[filterKey]
                for fltr in filterList:
                    if (fltr.operator != FilterOperator.EQUAL
                            and filterKey != propertyId):
                        raise IncompatibleFilterException(
                                'Trying to add inequality filter to '
                                + propertyId + ' but ' + filterKey
                                + 'already has inequality filter. '
                                + 'Inequality filters are allowed on one '
                                + 'property only')

            # Properties in inequality filters must be sorted before
            # other sort orders
            firstSortId = self._properties.getFirst().propertyId
            if (firstSortId != propertyId) and (firstSortId != '__key__'):
                raise IncompatibleFilterException(
                        'Properties in inequality filters must be sorted '
                        'before other sort orders')


    def removeFilters(self, propertyId):
        self._filters.remove(propertyId)


    def hasFilters(self):
        return len(self._filters) != 0


class QueryProperty(object):

    def __init__(self, propertyId, ascending=None):
        self.propertyId = propertyId
        self._direction = None

        if ascending is not None:
            if ascending:
                self._direction = SortDirection.ASCENDING
            else:
                self._direction = SortDirection.DESCENDING


class Filter(object):

    def __init__(self, operator, value):
        self.operator = operator
        self.value = value
