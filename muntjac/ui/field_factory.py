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

from muntjac.ui.table_field_factory import ITableFieldFactory
from muntjac.ui.form_field_factory import IFormFieldFactory


class IFieldFactory(IFormFieldFactory, ITableFieldFactory):
    """Factory for creating new Field-instances based on type, datasource
    and/or context.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.0
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
