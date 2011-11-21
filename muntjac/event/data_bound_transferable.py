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

"""Parent class for Transferable implementations that have a Muntjac
container as a data source."""

from muntjac.event.transferable_impl import TransferableImpl
from muntjac.data.container import IViewer


class DataBoundTransferable(TransferableImpl):
    """Parent class for L{Transferable} implementations that have a Muntjac
    container as a data source. The transfer is associated with an item
    (identified by its Id) and optionally also a property identifier (e.g. a
    table column identifier when transferring a single table cell).

    The component must implement the interface L{IViewer}.

    In most cases, receivers of data transfers should depend on this class
    instead of its concrete subclasses.
    """

    def __init__(self, sourceComponent, rawVariables):
        super(DataBoundTransferable, self).__init__(sourceComponent,
                rawVariables)


    def getItemId(self):
        """Returns the identifier of the item being transferred.

        @return: item identifier
        """
        pass


    def getPropertyId(self):
        """Returns the optional property identifier that the transfer concerns.

        This can be e.g. the table column from which a drag operation
        originated.

        @return: property identifier
        """
        pass


    def getSourceContainer(self):
        """Returns the container data source from which the transfer occurs.

        L{IViewer.getContainerDataSource} is used to obtain the underlying
        container of the source component.

        @return: Container
        """
        sourceComponent = self.getSourceComponent()
        if isinstance(sourceComponent, IViewer):
            return sourceComponent.getContainerDataSource()
        else:
            # this should not happen
            return None
