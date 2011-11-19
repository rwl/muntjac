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


class ITableFieldFactory(object):
    """Factory interface for creating new Field-instances based on Container
    (datasource), item id, property id and uiContext (the component responsible
    for displaying fields). Currently this interface is used by L{Table},
    but might later be used by some other components for L{Field}
    generation.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.0
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
