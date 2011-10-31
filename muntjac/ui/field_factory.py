# Copyright (C) 2010 IT Mill Ltd.
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

    @author: IT Mill Ltd.
    @author: Richard Lincoln
    @version @VERSION@
    @since 3.1
    @deprecated IFieldFactory was split into two lighter interfaces in 6.0
                Use IFormFieldFactory or ITableFieldFactory or both instead.
    """

    def createField(self, *args):
        """Creates a field based on type of data.

        @param type
                   the type of data presented in field.
        @param uiContext
                   the component where the field is presented.
        @return: Field the field suitable for editing the specified data.
        ---
        Creates a field based on the property datasource.

        @param property
                   the property datasource.
        @param uiContext
                   the component where the field is presented.
        @return: Field the field suitable for editing the specified data.
        """
        raise NotImplementedError
