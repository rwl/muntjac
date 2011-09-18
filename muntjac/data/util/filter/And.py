# -*- coding: utf-8 -*-
from com.vaadin.data.util.filter.AbstractJunctionFilter import (AbstractJunctionFilter,)
# from com.vaadin.data.Container.Filter import (Filter,)


class And(AbstractJunctionFilter):
    """A compound {@link Filter} that accepts an item if all of its filters accept
    the item.

    If no filters are given, the filter should accept all items.

    This filter also directly supports in-memory filtering when all sub-filters
    do so.

    @see Or

    @since 6.6
    """

    def __init__(self, *filters):
        """@param filters
                   filters of which the And filter will be composed
        """
        super(And, self)(filters)

    def passesFilter(self, itemId, item):
        for filter in self.getFilters():
            if not filter.passesFilter(itemId, item):
                return False
        return True
