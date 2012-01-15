# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@


class IFormFieldFactory(object):
    """Factory interface for creating new Field-instances based on
    L{Item}, property id and uiContext (the component responsible for
    displaying fields). Currently this interface is used by L{Form}, but
    might later be used by some other components for L{Field} generation.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: @VERSION@
    @see: L{TableFieldFactory}
    """

    def createField(self, item, propertyId, uiContext):
        """Creates a field based on the item, property id and the component
        (most commonly L{Form}) where the Field will be presented.

        @param item:
                   the item where the property belongs to.
        @param propertyId:
                   the Id of the property.
        @param uiContext:
                   the component where the field is presented, most commonly
                   this is L{Form}. uiContext will not necessary be the
                   parent component of the field, but the one that is
                   responsible for creating it.
        @return: Field the field suitable for editing the specified data.
        """
        raise NotImplementedError
