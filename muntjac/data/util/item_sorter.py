# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""An item comparator which is compatible with the ISortable interface."""


class IItemSorter(object):  # FIXME: Comparator, Cloneable, Serializable
    """An item comparator which is compatible with the L{ISortable} interface.
    The C{IItemSorter} interface can be used in C{Sortable} implementations
    to provide a custom sorting method.
    """

    def setSortProperties(self, container, propertyId, ascending):
        """Sets the parameters for an upcoming sort operation. The parameters
        determine what container to sort and how the C{IItemSorter} sorts the
        container.

        @param container:
                   The container that will be sorted. The container must
                   contain the propertyIds given in the C{propertyId}
                   parameter.
        @param propertyId:
                   The property ids used for sorting. The property ids must
                   exist in the container and should only be used if they are
                   also sortable, i.e include in the collection returned by
                   C{container.getSortableContainerPropertyIds()}. See
                   L{ISortable.sort} for more information.
        @param ascending:
                   Sorting order flags for each property id. See
                   L{ISortable.sort} for more information.
        """
        raise NotImplementedError


    def compare(self, itemId1, itemId2):
        """Compares its two arguments for order. Returns a negative integer,
        zero, or a positive integer as the first argument is less than, equal
        to, or greater than the second.

        The parameters for the C{IItemSorter} C{compare()} method must always
        be item ids which exist in the container set using L{setSortProperties}.

        @see: L{IComparator.compare}
        """
        raise NotImplementedError
