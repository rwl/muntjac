# -*- coding: utf-8 -*-
from com.vaadin.data.util.filter.AbstractJunctionFilter import (AbstractJunctionFilter,)


class Or(AbstractJunctionFilter):
    """A compound {@link Filter} that accepts an item if any of its filters accept
    the item.

    If no filters are given, the filter should reject all items.

    This filter also directly supports in-memory filtering when all sub-filters
    do so.

    @see And

    @since 6.6
    """

    def __init__(self, *filters):
        """@param filters
                   filters of which the Or filter will be composed
        """
        super(Or, self)(filters)

    def passesFilter(self, itemId, item):
        for filter in self.getFilters():
            if filter.passesFilter(itemId, item):
                return True
        return False

    def appliesToProperty(self, propertyId):
        """Returns true if a change in the named property may affect the filtering
        result. If some of the sub-filters are not in-memory filters, true is
        returned.

        By default, all sub-filters are iterated to check if any of them applies.
        If there are no sub-filters, true is returned as an empty Or rejects all
        items.
        """
        if self.getFilters().isEmpty():
            # empty Or filters out everything
            return True
        else:
            return super(Or, self).appliesToProperty(propertyId)
