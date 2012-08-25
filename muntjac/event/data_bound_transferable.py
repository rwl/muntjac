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
