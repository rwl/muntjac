# -*- coding: utf-8 -*-


class Not(Filter):
    """Negating filter that accepts the items rejected by another filter.

    This filter directly supports in-memory filtering when the negated filter
    does so.

    @since 6.6
    """
    _filter = None

    def __init__(self, filter):
        """Constructs a filter that negates a filter.

        @param filter
                   {@link Filter} to negate, not-null
        """
        self._filter = filter

    def getFilter(self):
        """Returns the negated filter.

        @return Filter
        """
        return self._filter

    def passesFilter(self, itemId, item):
        return not self._filter.passesFilter(itemId, item)

    def appliesToProperty(self, propertyId):
        """Returns true if a change in the named property may affect the filtering
        result. Return value is the same as {@link #appliesToProperty(Object)}
        for the negated filter.

        @return boolean
        """
        return self._filter.appliesToProperty(propertyId)

    def equals(self, obj):
        if (obj is None) or (not (self.getClass() == obj.getClass())):
            return False
        return self._filter == obj.getFilter()

    def hashCode(self):
        return self._filter.hashCode()
