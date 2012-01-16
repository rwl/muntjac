# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@


class ITableFieldFactory(object):
    """Factory interface for creating new Field-instances based on Container
    (datasource), item id, property id and uiContext (the component responsible
    for displaying fields). Currently this interface is used by L{Table},
    but might later be used by some other components for L{Field}
    generation.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: @VERSION@
    @see: FormFieldFactory
    """

    def createField(self, container, itemId, propertyId, uiContext):
        """Creates a field based on the Container, item id, property id and
        the component responsible for displaying the field (most commonly
        L{Table}).

        @param container:
                   the Container where the property belongs to.
        @param itemId:
                   the item Id.
        @param propertyId:
                   the Id of the property.
        @param uiContext:
                   the component where the field is presented.
        @return: A field suitable for editing the specified data or null if the
                property should not be editable.
        """
        raise NotImplementedError
