# -*- coding: utf-8 -*-
from com.vaadin.data.util.MethodProperty import (MethodProperty,)
from com.vaadin.data.util.VaadinPropertyDescriptor import (VaadinPropertyDescriptor,)
from com.vaadin.util.SerializerHelper import (SerializerHelper,)
# from java.io.IOException import (IOException,)
# from java.lang.reflect.Method import (Method,)


class MethodPropertyDescriptor(VaadinPropertyDescriptor):
    """Property descriptor that is able to create simple {@link MethodProperty}
    instances for a bean, using given accessors.

    @param <BT>
               bean type

    @since 6.6
    """
    _logger = Logger.getLogger(MethodPropertyDescriptor.getName())
    _name = None
    _propertyType = None
    _readMethod = None
    _writeMethod = None

    def __init__(self, name, propertyType, readMethod, writeMethod):
        """Creates a property descriptor that can create MethodProperty instances to
        access the underlying bean property.

        @param name
                   of the property
        @param propertyType
                   type (class) of the property
        @param readMethod
                   getter {@link Method} for the property
        @param writeMethod
                   setter {@link Method} for the property or null if read-only
                   property
        """
        # Special serialization to handle method references
        self._name = name
        self._propertyType = propertyType
        self._readMethod = readMethod
        self._writeMethod = writeMethod

    def writeObject(self, out):
        # Special serialization to handle method references
        out.defaultWriteObject()
        SerializerHelper.writeClass(out, self._propertyType)
        if self._writeMethod is not None:
            out.writeObject(self._writeMethod.getName())
            SerializerHelper.writeClass(out, self._writeMethod.getDeclaringClass())
            SerializerHelper.writeClassArray(out, self._writeMethod.getParameterTypes())
        else:
            out.writeObject(None)
            out.writeObject(None)
            out.writeObject(None)
        if self._readMethod is not None:
            out.writeObject(self._readMethod.getName())
            SerializerHelper.writeClass(out, self._readMethod.getDeclaringClass())
            SerializerHelper.writeClassArray(out, self._readMethod.getParameterTypes())
        else:
            out.writeObject(None)
            out.writeObject(None)
            out.writeObject(None)

    def readObject(self, in_):
        in_.defaultReadObject()
        try:
            class1 = SerializerHelper.readClass(in_)
            self._propertyType = class1
            name = in_.readObject()
            writeMethodClass = SerializerHelper.readClass(in_)
            paramTypes = SerializerHelper.readClassArray(in_)
            if name is not None:
                self._writeMethod = writeMethodClass.getMethod(name, paramTypes)
            else:
                self._writeMethod = None
            name = in_.readObject()
            readMethodClass = SerializerHelper.readClass(in_)
            paramTypes = SerializerHelper.readClassArray(in_)
            if name is not None:
                self._readMethod = readMethodClass.getMethod(name, paramTypes)
            else:
                self._readMethod = None
        except SecurityException, e:
            self._logger.log(Level.SEVERE, 'Internal deserialization error', e)
        except NoSuchMethodException, e:
            self._logger.log(Level.SEVERE, 'Internal deserialization error', e)

    def getName(self):
        return self._name

    def getPropertyType(self):
        return self._propertyType

    def createProperty(self, bean):
        return MethodProperty(self._propertyType, bean, self._readMethod, self._writeMethod)
