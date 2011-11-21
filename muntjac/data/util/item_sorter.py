# Copyright (C) 2011 Vaadin Ltd.
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
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

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
