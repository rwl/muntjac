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

from muntjac.data.util.AbstractProperty import AbstractProperty
from muntjac.data.Property import ReadOnlyException, ConversionException


class ObjectProperty(AbstractProperty):
    """A simple data object containing one typed value. This class is a
    straightforward implementation of the the {@link com.vaadin.data.Property}
    interface.

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, *args):
        """Creates a new instance of ObjectProperty with the given value. The type
        of the property is automatically initialized to be the type of the given
        value.

        @param value
                   the Initial value of the Property.
        ---
        Creates a new instance of ObjectProperty with the given value and type.

        Any value of type Object is accepted because, if the type class contains
        a string constructor, the toString of the value is used to create the new
        value. See {@link #setValue(Object)}.

        @param value
                   the Initial value of the Property.
        @param type
                   the type of the value. The value must be assignable to given
                   type.
        ---
        Creates a new instance of ObjectProperty with the given value, type and
        read-only mode status.

        Any value of type Object is accepted, see
        {@link #ObjectProperty(Object, Class)}.

        @param value
                   the Initial value of the property.
        @param type
                   the type of the value. <code>value</code> must be assignable
                   to this type.
        @param readOnly
                   Sets the read-only mode.
        """
        # The value contained by the Property.
        self._value = None

        # Data type of the Property's value.
        self._type = None

        # the cast is safe, because an object of type T has class Class<T>
        _0 = args
        _1 = len(args)
        if _1 == 1:
            value, = _0
            self.__init__(value, value.getClass())
        elif _1 == 2:
            value, typ = _0
            self._type = typ
            self.setValue(value)
        elif _1 == 3:
            value, typ, readOnly = _0
            self.__init__(value, typ)
            self.setReadOnly(readOnly)
        else:
            raise ValueError


    def getType(self):
        """Returns the type of the ObjectProperty. The methods <code>getValue</code>
        and <code>setValue</code> must be compatible with this type: one must be
        able to safely cast the value returned from <code>getValue</code> to the
        given type and pass any variable assignable to this type as an argument
        to <code>setValue</code>.

        @return type of the Property
        """
        return self._type


    def getValue(self):
        """Gets the value stored in the Property.

        @return the value stored in the Property
        """
        return self._value


    def setValue(self, newValue):
        """Sets the value of the property. This method supports setting from
        <code>String</code> if either <code>String</code> is directly assignable
        to property type, or the type class contains a string constructor.

        @param newValue
                   the New value of the property.
        @throws <code>Property.ReadOnlyException</code> if the object is in
                read-only mode
        @throws <code>Property.ConversionException</code> if the newValue can't
                be converted into the Property's native type directly or through
                <code>String</code>
        """
        # Checks the mode
        if self.isReadOnly():
            raise ReadOnlyException()
        # Tries to assign the compatible value directly
        if (newValue is None) or self._type.isAssignableFrom(newValue.getClass()):
            value = newValue
            self._value = value
        else:
            # Gets the string constructor
            try:
                constr = self.getType().getConstructor([str])
                # Creates new object from the string
                value = constr([str(newValue)])
            except Exception, e:
                raise ConversionException(e)
        self.fireValueChange()
