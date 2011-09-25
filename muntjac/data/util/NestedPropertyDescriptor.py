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

from muntjac.data.util.NestedMethodProperty import NestedMethodProperty
from muntjac.data.util.VaadinPropertyDescriptor import VaadinPropertyDescriptor


class NestedPropertyDescriptor(VaadinPropertyDescriptor):
    """Property descriptor that is able to create nested property instances for a
    bean.

    The property is specified in the dotted notation, e.g. "address.street", and
    can contain multiple levels of nesting.

    @param <BT>
               bean type

    @since 6.6
    """

    def __init__(self, name, beanType):
        """Creates a property descriptor that can create MethodProperty instances to
        access the underlying bean property.

        @param name
                   of the property in a dotted path format, e.g. "address.street"
        @param beanType
                   type (class) of the top-level bean
        @throws IllegalArgumentException
                    if the property name is invalid
        """
        self._name = name
        prop = NestedMethodProperty(beanType, name)
        self._propertyType = prop.getType()


    def getName(self):
        return self._name


    def getPropertyType(self):
        return self._propertyType


    def createProperty(self, bean):
        return NestedMethodProperty(bean, self._name)
