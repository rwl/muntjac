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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

"""A simple data object containing one typed value."""

from muntjac.data.util.abstract_property import AbstractProperty
from muntjac.data.property import ReadOnlyException, ConversionException


class ObjectProperty(AbstractProperty):
    """A simple data object containing one typed value. This class is a
    straightforward implementation of the the L{IProperty} interface.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.3
    """

    def __init__(self, value, typ=None, readOnly=None):
        """Creates a new instance of ObjectProperty with the given value,
        type and read-only mode status.

        Any value of type Object is accepted, see L{ObjectProperty}.

        @param value:
                   the Initial value of the property.
        @param typ:
                   the type of the value. C{value} must be assignable
                   to this type.
        @param readOnly:
                   Sets the read-only mode.
        """
        super(ObjectProperty, self).__init__()

        #: The value contained by the Property.
        self._value = None

        #: Data type of the Property's value.
        self._type = None

        if typ is None and readOnly is None:
            ObjectProperty.__init__(self, value, value.__class__)
        elif readOnly is None:
            self._type = typ
            self.setValue(value)
        else:
            ObjectProperty.__init__(self, value, typ)
            self.setReadOnly(readOnly)


    def getType(self):
        """Returns the type of the ObjectProperty. The methods C{getValue}
        and C{setValue} must be compatible with this type: one must be
        able to safely cast the value returned from C{getValue} to the
        given type and pass any variable assignable to this type as an
        argument to C{setValue}.

        @return: type of the Property
        """
        return self._type


    def getValue(self):
        """Gets the value stored in the Property.

        @return: the value stored in the Property
        """
        return self._value


    def setValue(self, newValue):
        """Sets the value of the property. This method supports setting from
        C{str} if either C{str} is directly assignable to property type, or
        the type class contains a string constructor.

        @param newValue:
                   the New value of the property.
        @raise ReadOnlyException:
                   if the object is in read-only mode
        @raise ConversionException:
                   if the newValue can't be converted into the Property's
                   native type directly or through C{str}
        """
        # Checks the mode
        if self.isReadOnly():
            raise ReadOnlyException()

        # Tries to assign the compatible value directly
        if newValue is None or issubclass(newValue.__class__, self._type):
            self._value = newValue
        else:
            # Gets the string constructor
            try:
                #constr = self.getType().getConstructor([str])
                constr = self.getType()  # FIXME: getConstructor
                # Creates new object from the string
                self._value = constr(str(newValue))  # FIXME: *args
            except Exception, e:
                raise ConversionException(e)

        self.fireValueChange()
