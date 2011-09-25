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

import logging

from muntjac.data.util.MethodProperty import MethodProperty
from muntjac.data.util.VaadinPropertyDescriptor import VaadinPropertyDescriptor
from muntjac.util.SerializerHelper import SerializerHelper


class MethodPropertyDescriptor(VaadinPropertyDescriptor):
    """Property descriptor that is able to create simple {@link MethodProperty}
    instances for a bean, using given accessors.

    @param <BT>
               bean type

    @since 6.6
    """
    _logger = logging.getLogger(MethodPropertyDescriptor.getName())


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
        except Exception:  # SecurityException, NoSuchMethodException
            self._logger.critical('Internal deserialization error')


    def getName(self):
        return self._name


    def getPropertyType(self):
        return self._propertyType


    def createProperty(self, bean):
        return MethodProperty(self._propertyType, bean, self._readMethod, self._writeMethod)
