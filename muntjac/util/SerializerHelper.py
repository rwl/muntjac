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


class SerializerHelper(object):
    """Helper class for performing serialization. Most of the methods are here are
    workarounds for problems in Google App Engine. Used internally by Vaadin and
    should not be used by application developers. Subject to change at any time.

    @since 6.0
    """

    @classmethod
    def writeClass(cls, out, cls):
        """Serializes the class reference so {@link #readClass(ObjectInputStream)}
        can deserialize it. Supports null class references.

        @param out
                   The {@link ObjectOutputStream} to serialize to.
        @param cls
                   A class or null.
        @throws IOException
                    Rethrows any IOExceptions from the ObjectOutputStream
        """
        if cls is None:
            out.writeObject(None)  # FIXME ObjectOutputStream
        else:
            out.writeObject(cls.getName())


    @classmethod
    def writeClassArray(cls, out, classes):
        """Serializes the class references so
        {@link #readClassArray(ObjectInputStream)} can deserialize it. Supports
        null class arrays.

        @param out
                   The {@link ObjectOutputStream} to serialize to.
        @param classes
                   An array containing class references or null.
        @throws IOException
                    Rethrows any IOExceptions from the ObjectOutputStream
        """
        if classes is None:
            out.writeObject(None)  # FIXME ObjectOutputStream
        else:
            classNames = [None] * len(classes)
            for i in range(len(classes)):
                classNames[i] = classes[i].getName()

            out.writeObject(classNames)


    @classmethod
    def readClassArray(cls, in_):
        """Deserializes a class references serialized by
        {@link #writeClassArray(ObjectOutputStream, Class[])}. Supports null
        class arrays.

        @param in
                   {@link ObjectInputStream} to read from.
        @return Class array with the class references or null.
        @throws ClassNotFoundException
                    If one of the classes could not be resolved.
        @throws IOException
                    Rethrows IOExceptions from the ObjectInputStream
        """
        classNames = in_.readObject()  # FIXME ObjectInputStream
        if classNames is None:
            return None
        classes = [None] * len(classNames)
        for i in range(len(classNames)):
            classes[i] = cls.resolveClass(classNames[i])

        return classes

    # List of primitive classes. Google App Engine has problems
    # serializing/deserializing these (#3064).
    _primitiveClasses = [int, long, float, bool]


    @classmethod
    def resolveClass(cls, className):
        """Resolves the class given by {@code className}.

        @param className
                   The fully qualified class name.
        @return A {@code Class} reference.
        @throws ClassNotFoundException
                    If the class could not be resolved.
        """
        for c in cls._primitiveClasses:
            if className == c.getName():
                return c

        return (lambda x: getattr(__import__(x.rsplit('.', 1)[0], fromlist=x.rsplit('.', 1)[0]), x.split('.')[-1]))(className)


    @classmethod
    def readClass(cls, in_):
        """Deserializes a class reference serialized by
        {@link #writeClass(ObjectOutputStream, Class)}. Supports null class
        references.

        @param in
                   {@code ObjectInputStream} to read from.
        @return Class reference to the resolved class
        @throws ClassNotFoundException
                    If the class could not be resolved.
        @throws IOException
                    Rethrows IOExceptions from the ObjectInputStream
        """
        className = in_.readObject()
        if className is None:
            return None
        else:
            return cls.resolveClass(className)
