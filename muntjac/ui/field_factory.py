# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.ui.table_field_factory import ITableFieldFactory
from muntjac.ui.form_field_factory import IFormFieldFactory


class IFieldFactory(IFormFieldFactory, ITableFieldFactory):
    """Factory for creating new Field-instances based on type, datasource
    and/or context.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: @VERSION@
    @deprecated: IFieldFactory was split into two lighter interfaces.
                 Use IFormFieldFactory or ITableFieldFactory or both instead.
    """

    def createField(self, *args):
        """Creates a field based on type of data.

        @param args: tuple of the form
            - (type, uiContext)
              1. the type of data presented in field.
              2. the component where the field is presented.
            - (property, uiContext)
              1. the property datasource.
              2. the component where the field is presented.
        @return: Field the field suitable for editing the specified data.
        """
        raise NotImplementedError
