# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

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
