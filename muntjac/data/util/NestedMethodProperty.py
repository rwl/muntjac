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

from muntjac.data.util.MethodProperty import MethodException, MethodProperty
from muntjac.data.util.AbstractProperty import AbstractProperty
from muntjac.data.Property import ReadOnlyException


class NestedMethodProperty(AbstractProperty):
    """Nested accessor based property for a bean.

    The property is specified in the dotted notation, e.g. "address.street", and
    can contain multiple levels of nesting.

    When accessing the property value, all intermediate getters must return
    non-null values.

    @see MethodProperty

    @since 6.6
    """

    # Special serialization to handle method references
    def writeObject(self, out):
        # Special serialization to handle method references
        out.defaultWriteObject()
        # getMethods and setMethod are reconstructed on read based on
        # propertyName


    def readObject(self, in_):
        in_.defaultReadObject()
        self.initialize(self._instance.getClass(), self._propertyName)


    def __init__(self, *args):
        """Constructs a nested method property for a given object instance. The
        property name is a dot separated string pointing to a nested property,
        e.g. "manager.address.street".

        @param instance
                   top-level bean to which the property applies
        @param propertyName
                   dot separated nested property name
        @throws IllegalArgumentException
                    if the property name is invalid
        ---
        For internal use to deduce property type etc. without a bean instance.
        Calling {@link #setValue(Object)} or {@link #getValue()} on properties
        constructed this way is not supported.

        @param instanceClass
                   class of the top-level bean
        @param propertyName
        """
        # needed for de-serialization
        self._propertyName = None

        # chain of getter methods
        self._getMethods = None

        # The setter method.
        self._setMethod = None

        # Bean instance used as a starting point for accessing the property value.
        self._instance = None
        self._type = None

        _0 = args
        _1 = len(args)
        if _1 == 2:
            if isinstance(_0[0], object):
                instance, propertyName = _0
                self._instance = instance
                self.initialize(instance.getClass(), propertyName)
            else:
                instanceClass, propertyName = _0
                self._instance = None
                self.initialize(instanceClass, propertyName)
        else:
            raise ValueError


    def initialize(self, beanClass, propertyName):
        """Initializes most of the internal fields based on the top-level bean
        instance and property name (dot-separated string).

        @param beanClass
                   class of the top-level bean to which the property applies
        @param propertyName
                   dot separated nested property name
        @throws IllegalArgumentException
                    if the property name is invalid
        """
        getMethods = list()
        lastSimplePropertyName = propertyName
        lastClass = beanClass
        # first top-level property, then go deeper in a loop
        propertyClass = beanClass
        simplePropertyNames = propertyName.split('\\.')
        if propertyName.endswith('.') or (0 == len(simplePropertyNames)):
            raise self.IllegalArgumentException('Invalid property name \'' + propertyName + '\'')
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(simplePropertyNames)):
                break
            simplePropertyName = simplePropertyNames[i].trim()
            if len(simplePropertyName) > 0:
                lastSimplePropertyName = simplePropertyName
                lastClass = propertyClass
                try:
                    getter = MethodProperty.initGetterMethod(simplePropertyName, propertyClass)
                    propertyClass = getter.getReturnType()
                    getMethods.add(getter)
                except Exception, e:  # NoSuchMethodException
                    raise self.IllegalArgumentException('Bean property \'' + simplePropertyName + '\' not found', e)
            else:
                raise self.IllegalArgumentException('Empty or invalid bean property identifier in \'' + propertyName + '\'')
        # In case the get method is found, resolve the type
        lastGetMethod = getMethods[len(getMethods) - 1]
        typ = lastGetMethod.getReturnType()
        # Finds the set method
        setMethod = None
        # Assure that the first letter is upper cased (it is a common
        # mistake to write firstName, not FirstName).
        try:
            if self.Character.isLowerCase(lastSimplePropertyName[0]):
                buf = lastSimplePropertyName.toCharArray()
                buf[0] = self.Character.toUpperCase(buf[0])
                lastSimplePropertyName = str(buf)
            setMethod = lastClass.getMethod('set' + lastSimplePropertyName, [typ])
        except Exception:  # NoSuchMethodException
            pass
        self._type = MethodProperty.convertPrimitiveType(typ)
        self._propertyName = propertyName
        self._getMethods = getMethods
        self._setMethod = setMethod


    def getType(self):
        return self._type


    def isReadOnly(self):
        return super(NestedMethodProperty, self).isReadOnly() or (None is self._setMethod)


    def getValue(self):
        """Gets the value stored in the Property. The value is resolved by calling
        the specified getter method with the argument specified at instantiation.

        @return the value of the Property
        """
        try:
            obj = self._instance
            for m in self._getMethods:
                obj = m.invoke(obj)
            return obj
        except Exception, e:
            raise MethodException(self, e)


    def setValue(self, newValue):
        """Sets the value of the property. This method supports setting from
        <code>String</code>s if either <code>String</code> is directly assignable
        to property type, or the type class contains a string constructor.

        @param newValue
                   the New value of the property.
        @throws <code>Property.ReadOnlyException</code> if the object is in
                read-only mode.
        @throws <code>Property.ConversionException</code> if
                <code>newValue</code> can't be converted into the Property's
                native type directly or through <code>String</code>.
        @see #invokeSetMethod(Object)
        """
        # Checks the mode
        if self.isReadOnly():
            raise ReadOnlyException()
        value = MethodProperty.convertValue(newValue, self._type)
        self.invokeSetMethod(value)
        self.fireValueChange()


    def invokeSetMethod(self, value):
        """Internal method to actually call the setter method of the wrapped
        property.

        @param value
        """
        try:
            obj = self._instance
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(self._getMethods) - 1):
                    break
                obj = self._getMethods[i].invoke(obj)
            self._setMethod.invoke(object, [value])
        except Exception, e:  # InvocationTargetException
            raise MethodException(self, e.getTargetException())
        except Exception, e:
            raise MethodException(self, e)


    def getGetMethods(self):
        """Returns an unmodifiable list of getter methods to call in sequence to get
        the property value.

        This API may change in future versions.

        @return unmodifiable list of getter methods corresponding to each segment
                of the property name
        """
        return list(self._getMethods)
