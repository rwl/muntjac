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

import logging

from muntjac.data.util.AbstractProperty import AbstractProperty
from muntjac.data.Property import ReadOnlyException, ConversionException
from muntjac.util.SerializerHelper import SerializerHelper


class MethodProperty(AbstractProperty):
    """<p>
    Proxy class for creating Properties from pairs of getter and setter methods
    of a Bean property. An instance of this class can be thought as having been
    attached to a field of an object. Accessing the object through the Property
    interface directly manipulates the underlying field.
    </p>

    <p>
    It's assumed that the return value returned by the getter method is
    assignable to the type of the property, and the setter method parameter is
    assignable to that value.
    </p>

    <p>
    A valid getter method must always be available, but instance of this class
    can be constructed with a <code>null</code> setter method in which case the
    resulting MethodProperty is read-only.
    </p>

    <p>
    MethodProperty implements Property.ValueChangeNotifier, but does not
    automatically know whether or not the getter method will actually return a
    new value - value change listeners are always notified when setValue is
    called, without verifying what the getter returns.
    </p>

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """

    _logger = logging.getLogger(MethodProperty.getName())

    # Special serialization to handle method references
    def writeObject(self, out):
        out.defaultWriteObject()
        SerializerHelper.writeClass(out, self._type)
        out.writeObject(self._instance)
        out.writeObject(self._setArgs)
        out.writeObject(self._getArgs)
        if self._setMethod is not None:
            out.writeObject(self._setMethod.getName())
            SerializerHelper.writeClassArray(out, self._setMethod.getParameterTypes())
        else:
            out.writeObject(None)
            out.writeObject(None)
        if self._getMethod is not None:
            out.writeObject(self._getMethod.getName())
            SerializerHelper.writeClassArray(out, self._getMethod.getParameterTypes())
        else:
            out.writeObject(None)
            out.writeObject(None)


    # Special serialization to handle method references
    def readObject(self, in_):
        in_.defaultReadObject()
        try:
            class1 = SerializerHelper.readClass(in_)
            self._type = class1
            self._instance = in_.readObject()
            self._setArgs = in_.readObject()
            self._getArgs = in_.readObject()
            name = in_.readObject()
            paramTypes = SerializerHelper.readClassArray(in_)
            if name is not None:
                self._setMethod = self._instance.getClass().getMethod(name, paramTypes)
            else:
                self._setMethod = None
            name = in_.readObject()
            paramTypes = SerializerHelper.readClassArray(in_)
            if name is not None:
                self._getMethod = self._instance.getClass().getMethod(name, paramTypes)
            else:
                self._getMethod = None
        except Exception:  # SecurityException, NoSuchMethodException
            self._logger.critical('Internal deserialization error')


    def __init__(self, *args):
        """<p>
        Creates a new instance of <code>MethodProperty</code> from a named bean
        property. This constructor takes an object and the name of a bean
        property and initializes itself with the accessor methods for the
        property.
        </p>
        <p>
        The getter method of a <code>MethodProperty</code> instantiated with this
        constructor will be called with no arguments, and the setter method with
        only the new value as the sole argument.
        </p>

        <p>
        If the setter method is unavailable, the resulting
        <code>MethodProperty</code> will be read-only, otherwise it will be
        read-write.
        </p>

        <p>
        Method names are constructed from the bean property by adding
        get/is/are/set prefix and capitalising the first character in the name of
        the given bean property.
        </p>

        @param instance
                   the object that includes the property.
        @param beanPropertyName
                   the name of the property to bind to.
        ---
        <p>
        Creates a new instance of <code>MethodProperty</code> from named getter
        and setter methods. The getter method of a <code>MethodProperty</code>
        instantiated with this constructor will be called with no arguments, and
        the setter method with only the new value as the sole argument.
        </p>

        <p>
        If the setter method is <code>null</code>, the resulting
        <code>MethodProperty</code> will be read-only, otherwise it will be
        read-write.
        </p>

        @param type
                   the type of the property.
        @param instance
                   the object that includes the property.
        @param getMethodName
                   the name of the getter method.
        @param setMethodName
                   the name of the setter method.
        ---
        <p>
        Creates a new instance of <code>MethodProperty</code> with the getter and
        setter methods. The getter method of a <code>MethodProperty</code>
        instantiated with this constructor will be called with no arguments, and
        the setter method with only the new value as the sole argument.
        </p>

        <p>
        If the setter method is <code>null</code>, the resulting
        <code>MethodProperty</code> will be read-only, otherwise it will be
        read-write.
        </p>

        @param type
                   the type of the property.
        @param instance
                   the object that includes the property.
        @param getMethod
                   the getter method.
        @param setMethod
                   the setter method.
        ---
        <p>
        Creates a new instance of <code>MethodProperty</code> from named getter
        and setter methods and argument lists. The getter method of a
        <code>MethodProperty</code> instantiated with this constructor will be
        called with the getArgs as arguments. The setArgs will be used as the
        arguments for the setter method, though the argument indexed by the
        setArgumentIndex will be replaced with the argument passed to the
        {@link #setValue(Object newValue)} method.
        </p>

        <p>
        For example, if the <code>setArgs</code> contains <code>A</code>,
        <code>B</code> and <code>C</code>, and <code>setArgumentIndex =
        1</code>, the call <code>methodProperty.setValue(X)</code> would result
        in the setter method to be called with the parameter set of
        <code>{A, X, C}</code>
        </p>

        @param type
                   the type of the property.
        @param instance
                   the object that includes the property.
        @param getMethodName
                   the name of the getter method.
        @param setMethodName
                   the name of the setter method.
        @param getArgs
                   the fixed argument list to be passed to the getter method.
        @param setArgs
                   the fixed argument list to be passed to the setter method.
        @param setArgumentIndex
                   the index of the argument in <code>setArgs</code> to be
                   replaced with <code>newValue</code> when
                   {@link #setValue(Object newValue)} is called.
        ---
        <p>
        Creates a new instance of <code>MethodProperty</code> from the getter and
        setter methods, and argument lists.
        </p>
        <p>
        This constructor behaves exactly like
        {@link #MethodProperty(Class type, Object instance, String getMethodName, String setMethodName, Object [] getArgs, Object [] setArgs, int setArgumentIndex)}
        except that instead of names of the getter and setter methods this
        constructor is given the actual methods themselves.
        </p>

        @param type
                   the type of the property.
        @param instance
                   the object that includes the property.
        @param getMethod
                   the getter method.
        @param setMethod
                   the setter method.
        @param getArgs
                   the fixed argument list to be passed to the getter method.
        @param setArgs
                   the fixed argument list to be passed to the setter method.
        @param setArgumentIndex
                   the index of the argument in <code>setArgs</code> to be
                   replaced with <code>newValue</code> when
                   {@link #setValue(Object newValue)} is called.
        """
        # The object that includes the property the MethodProperty is bound to.
        self._instance = None

        # Argument arrays for the getter and setter methods.
        self._setArgs = None
        self._getArgs = None

        # The getter and setter methods.
        self._setMethod = None
        self._getMethod = None

        # Index of the new value in the argument list for the setter method. If the
        # setter method requires several parameters, this index tells which one is
        # the actual value to change.
        self._setArgumentIndex = None

        # Type of the property.
        self._type = None

        _0 = args
        _1 = len(args)
        if _1 == 2:
            instance, beanPropertyName = _0
            beanClass = instance.getClass()
            # Assure that the first letter is upper cased (it is a common
            # mistake to write firstName, not FirstName).
            if self.Character.isLowerCase(beanPropertyName[0]):
                buf = beanPropertyName.toCharArray()
                buf[0] = self.Character.toUpperCase(buf[0])
                beanPropertyName = str(buf)
            # Find the get method
            self._getMethod = None
            # In case the get method is found, resolve the type
            try:
                self._getMethod = self.initGetterMethod(beanPropertyName, beanClass)
            except Exception:  # NoSuchMethodException
                raise self.MethodException(self, 'Bean property ' + beanPropertyName + ' can not be found')
            returnType = self._getMethod.getReturnType()
            # Finds the set method
            self._setMethod = None
            # Gets the return type from get method
            try:
                self._setMethod = beanClass.getMethod('set' + beanPropertyName, [returnType])
            except Exception:  # NoSuchMethodException
                pass
            if returnType.isPrimitive():
                self._type = self.convertPrimitiveType(returnType)
                if self._type.isPrimitive():
                    raise self.MethodException(self, 'Bean property ' + beanPropertyName + ' getter return type must not be void')
            else:
                self._type = returnType
            self.setArguments([], [None], 0)
            self._instance = instance
        elif _1 == 4:
            if isinstance(_0[2], None):  # Method
                typ, instance, getMethod, setMethod = _0
                self.__init__(typ, instance, getMethod, setMethod, [], [None], 0)
            else:
                typ, instance, getMethodName, setMethodName = _0
                self.__init__(typ, instance, getMethodName, setMethodName, [], [None], 0)
        elif _1 == 7:
            if isinstance(_0[2], None):  # Method
                typ, instance, getMethod, setMethod, getArgs, setArgs, setArgumentIndex = _0
                if getMethod is None:
                    raise self.MethodException(self, 'Property GET-method cannot not be null: ' + typ)
                if setMethod is not None:
                    if setArgs is None:
                        raise self.IndexOutOfBoundsException('The setArgs can not be null')
                    if (setArgumentIndex < 0) or (setArgumentIndex >= len(setArgs)):
                        raise self.IndexOutOfBoundsException('The setArgumentIndex must be >= 0 and < setArgs.length')
                # Gets the return type from get method
                typ = self.convertPrimitiveType(typ)
                self._getMethod = getMethod
                self._setMethod = setMethod
                self.setArguments(getArgs, setArgs, setArgumentIndex)
                self._instance = instance
                self._type = typ
            else:
                typ, instance, getMethodName, setMethodName, getArgs, setArgs, setArgumentIndex = _0
                if setMethodName is not None and setArgs is None:
                    raise self.IndexOutOfBoundsException('The setArgs can not be null')
                if (
                    setMethodName is not None and (setArgumentIndex < 0) or (setArgumentIndex >= len(setArgs))
                ):
                    raise self.IndexOutOfBoundsException('The setArgumentIndex must be >= 0 and < setArgs.length')
                # Set type
                self._type = typ
                # Find set and get -methods
                m = instance.getClass().getMethods()
                # Finds get method
                found = False
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(m)):
                        break
                    # Tests the name of the get Method
                    if not (m[i].getName() == getMethodName):
                        # name does not match, try next method
                        continue
                    # Tests return type
                    if not (typ == m[i].getReturnType()):
                        continue
                    # Tests the parameter types
                    c = m[i].getParameterTypes()
                    if len(c) != len(getArgs):
                        # not the right amount of parameters, try next method
                        continue
                    j = 0
                    while j < len(c):
                        if getArgs[j] is not None and not c[j].isAssignableFrom(getArgs[j].getClass()):
                            # parameter type does not match, try next method
                            break
                        j += 1
                    if j == len(c):
                        # all paramteters matched
                        if found == True:
                            raise self.MethodException(self, 'Could not uniquely identify ' + getMethodName + '-method')
                        else:
                            found = True
                            self._getMethod = m[i]
                if found != True:
                    raise self.MethodException(self, 'Could not find ' + getMethodName + '-method')
                # Finds set method
                if setMethodName is not None:
                    # Finds setMethod
                    found = False
                    _1 = True
                    i = 0
                    while True:
                        if _1 is True:
                            _1 = False
                        else:
                            i += 1
                        if not (i < len(m)):
                            break
                        # Checks name
                        if not (m[i].getName() == setMethodName):
                            # name does not match, try next method
                            continue
                        # Checks parameter compatibility
                        c = m[i].getParameterTypes()
                        if len(c) != len(setArgs):
                            # not the right amount of parameters, try next method
                            continue
                        j = 0
                        while j < len(c):
                            if setArgs[j] is not None and not c[j].isAssignableFrom(setArgs[j].getClass()):
                                # parameter type does not match, try next method
                                break
                            elif j == setArgumentIndex and not (c[j] == type):
                                # Property type is not the same as setArg type
                                break
                            j += 1
                        if j == len(c):
                            # all parameters match
                            if found == True:
                                raise self.MethodException(self, 'Could not identify unique ' + setMethodName + '-method')
                            else:
                                found = True
                                self._setMethod = m[i]
                    if found != True:
                        raise self.MethodException(self, 'Could not identify ' + setMethodName + '-method')
                # Gets the return type from get method
                self._type = self.convertPrimitiveType(type)
                self.setArguments(getArgs, setArgs, setArgumentIndex)
                self._instance = instance
        else:
            raise ValueError

    @classmethod
    def initGetterMethod(cls, propertyName, beanClass):
        """Find a getter method for a property (getXyz(), isXyz() or areXyz()).

        @param propertyName
                   name of the property
        @param beanClass
                   class in which to look for the getter methods
        @return Method
        @throws NoSuchMethodException
                    if no getter found
        """
        propertyName = propertyName[:1].toUpperCase() + (propertyName[1:])
        getMethod = None
        try:
            getMethod = beanClass.getMethod('get' + propertyName, [])
        except Exception:  # NoSuchMethodException
            try:
                getMethod = beanClass.getMethod('is' + propertyName, [])
            except Exception:  # NoSuchMethodException
                getMethod = beanClass.getMethod('are' + propertyName, [])
        return getMethod

    @classmethod
    def convertPrimitiveType(cls, typ):
        # Gets the return typ from get method
        if typ.isPrimitive():
            if typ == bool:
                typ = bool
            elif typ == int:
                typ = int
            elif typ == float:
                typ = float
            elif typ == float:
                typ = float
            elif typ == str:  # Byte
                typ = int
            elif typ == str:  # Character
                typ = str
            elif typ == int:  # Short
                typ = int
            elif typ == long: # Long
                typ = long
        return typ


    def getType(self):
        """Returns the type of the Property. The methods <code>getValue</code> and
        <code>setValue</code> must be compatible with this type: one must be able
        to safely cast the value returned from <code>getValue</code> to the given
        type and pass any variable assignable to this type as an argument to
        <code>setValue</code>.

        @return type of the Property
        """
        return self._type


    def isReadOnly(self):
        """Tests if the object is in read-only mode. In read-only mode calls to
        <code>setValue</code> will throw <code>ReadOnlyException</code> and will
        not modify the value of the Property.

        @return <code>true</code> if the object is in read-only mode,
                <code>false</code> if it's not
        """
        return super(MethodProperty, self).isReadOnly() or (self._setMethod is None)


    def getValue(self):
        """Gets the value stored in the Property. The value is resolved by calling
        the specified getter method with the argument specified at instantiation.

        @return the value of the Property
        """
        try:
            return self._getMethod.invoke(self._instance, self._getArgs)
        except Exception, e:
            raise self.MethodException(self, e)


    def setArguments(self, getArgs, setArgs, setArgumentIndex):
        """<p>
        Sets the setter method and getter method argument lists.
        </p>

        @param getArgs
                   the fixed argument list to be passed to the getter method.
        @param setArgs
                   the fixed argument list to be passed to the setter method.
        @param setArgumentIndex
                   the index of the argument in <code>setArgs</code> to be
                   replaced with <code>newValue</code> when
                   {@link #setValue(Object newValue)} is called.
        """
        self._getArgs = [None] * len(getArgs)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(getArgs)):
                break
            self._getArgs[i] = getArgs[i]
        self._setArgs = [None] * len(setArgs)
        _1 = True
        i = 0
        while True:
            if _1 is True:
                _1 = False
            else:
                i += 1
            if not (i < len(setArgs)):
                break
            self._setArgs[i] = setArgs[i]
        self._setArgumentIndex = setArgumentIndex


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
        value = self.convertValue(newValue, self._type)
        self.invokeSetMethod(value)
        self.fireValueChange()


    @classmethod
    def convertValue(cls, value, typ):
        """Convert a value to the given type, using a constructor of the type that
        takes a single String parameter (toString() for the value) if necessary.

        @param value
                   to convert
        @param type
                   type into which the value should be converted
        @return converted value
        """
        if (None is value) or typ.isAssignableFrom(value.getClass()):
            return value
        # convert using a string constructor
        # Gets the string constructor
        try:
            constr = typ.getConstructor([str])
            # Create a new object from the string
            return constr([str(value)])
        except Exception, e:
            raise ConversionException(e)


    def invokeSetMethod(self, value):
        """Internal method to actually call the setter method of the wrapped
        property.

        @param value
        """
        # Construct a temporary argument array only if needed
        try:
            if len(self._setArgs) == 1:
                self._setMethod.invoke(self._instance, [value])
            else:
                # Sets the value to argument array
                args = [None] * len(self._setArgs)
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(self._setArgs)):
                        break
                    args[i] = value if i == self._setArgumentIndex else self._setArgs[i]
                self._setMethod.invoke(self._instance, args)
        except Exception, e:  # InvocationTargetException
            targetException = e.getTargetException()
            raise self.MethodException(self, targetException)
        except Exception, e:
            raise self.MethodException(self, e)


    def fireValueChange(self):
        """Sends a value change event to all registered listeners.

        Public for backwards compatibility, visibility may be reduced in future
        versions.
        """
        super(MethodProperty, self).fireValueChange()


class MethodException(RuntimeError):
    """<code>Exception</code> object that signals that there were problems
    calling or finding the specified getter or setter methods of the
    property.

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, *args):
        """Constructs a new <code>MethodException</code> with the specified
        detail message.

        @param property
                   the property.
        @param msg
                   the detail message.
        ---
        Constructs a new <code>MethodException</code> from another exception.

        @param property
                   the property.
        @param cause
                   the cause of the exception.
        """
        # The method property from which the exception originates from
        self._property = None
        # Cause of the method exception
        self._cause = None

        _0 = args
        _1 = len(args)
        if _1 == 2:
            if isinstance(_0[1], Exception):
                prop, cause = _0
                self._property = prop
                self._cause = cause
            else:
                prop, msg = _0
                super(MethodException, self)(msg)
                self._property = prop
        else:
            raise ValueError


    def getCause(self):
        """@see java.lang.Throwable#getCause()"""
        return self._cause


    def getMethodProperty(self):
        """Gets the method property this exception originates from.

        @return MethodProperty or null if not a valid MethodProperty
        """
        return self._property if isinstance(self._property, MethodProperty) else None


    def getProperty(self):
        """Gets the method property this exception originates from.

        @return Property from which the exception originates
        """
        return self._property
