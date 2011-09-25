# Copyright (C) 2011 Vaadin Ltd
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


class VaadinPropertyDescriptor(object):
    """Property descriptor that can create a property instance for a bean.

    Used by {@link BeanItem} and {@link AbstractBeanContainer} to keep track of
    the set of properties of items.

    @param <BT>
               bean type

    @since 6.6
    """

    def getName(self):
        """Returns the name of the property.

        @return
        """
        pass

    def getPropertyType(self):
        """Returns the type of the property.

        @return Class<?>
        """
        pass

    def createProperty(self, bean):
        """Creates a new {@link Property} instance for this property for a bean.

        @param bean
        @return
        """
        pass
