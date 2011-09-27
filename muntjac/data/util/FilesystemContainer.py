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

from datetime import datetime

from muntjac.data.Item import Item
from muntjac.service.FileTypeResolver import FileTypeResolver
from muntjac.terminal.Resource import Resource
from muntjac.data.util.MethodProperty import MethodProperty
from muntjac.data.Container import Container, Hierarchical


class FileItem(Item):
    """A Item wrapper for files in a filesystem.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # The wrapped file.
    _file = None

    def __init__(self, lf, container):  # FIXME: inner class
        """Constructs a FileItem from a existing file."""
        self._file = lf
        self._container = container


    def getItemProperty(self, idd):
        # Gets the specified property of this file. Don't add a JavaDoc comment
        # here, we use the default documentation from implemented interface.
        return self.getContainerProperty(self._file, idd)


    def getItemPropertyIds(self):
        # Gets the IDs of all properties available for this item Don't add a
        # JavaDoc comment here, we use the default documentation from
        # implemented interface.
        return self.getContainerPropertyIds()


    def hashCode(self):
        """Calculates a integer hash-code for the Property that's unique inside
        the Item containing the Property. Two different Properties inside the
        same Item contained in the same list always have different
        hash-codes, though Properties in different Items may have identical
        hash-codes.

        @return A locally unique hash-code as integer
        """
        return self._file.hashCode() ^ self._container.hashCode()


    def equals(self, obj):
        """Tests if the given object is the same as the this object. Two
        Properties got from an Item with the same ID are equal.

        @param obj
                   an object to compare with this object.
        @return <code>true</code> if the given object is the same as this
                object, <code>false</code> if not
        """
        if (obj is None) or (not isinstance(obj, FileItem)):
            return False
        fi = obj
        return fi.getHost() == self.getHost() and fi.file == self._file


    def getHost(self):
        """Gets the host of this file."""
        return self._container


    def lastModified(self):
        """Gets the last modified date of this file.

        @return Date
        """
        return datetime(self._file.lastModified())


    def getName(self):
        """Gets the name of this file.

        @return file name of this file.
        """
        return self._file.getName()


    def getIcon(self):
        """Gets the icon of this file.

        @return the icon of this file.
        """
        return FileTypeResolver.getIcon(self._file)


    def getSize(self):
        """Gets the size of this file.

        @return size
        """
        if self._file.isDirectory():
            return 0

        return len(self._file)


    def toString(self):
        """@see java.lang.Object#toString()"""
        if '' == self._file.getName():
            return self._file.getAbsolutePath()

        return self._file.getName()


    def addItemProperty(self, idd, prop):
        """Filesystem container does not support adding new properties.

        @see com.vaadin.data.Item#addItemProperty(Object, Property)
        """
        raise NotImplementedError, 'Filesystem container ' \
                + 'does not support adding new properties'


    def removeItemProperty(self, idd):
        """Filesystem container does not support removing properties.

        @see com.vaadin.data.Item#removeItemProperty(Object)
        """
        raise NotImplementedError, 'Filesystem container does not support property removal'


class FilesystemContainer(Container, Hierarchical):
    """A hierarchical container wrapper for a filesystem.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # String identifier of a file's "name" property.
    PROPERTY_NAME = 'Name'

    # String identifier of a file's "size" property.
    PROPERTY_SIZE = 'Size'

    # String identifier of a file's "icon" property.
    PROPERTY_ICON = 'Icon'

    # String identifier of a file's "last modified" property.
    PROPERTY_LASTMODIFIED = 'Last Modified'

    # List of the string identifiers for the available properties.
    FILE_PROPERTIES = list()

    _FILEITEM_LASTMODIFIED = None

    _FILEITEM_NAME = None

    _FILEITEM_ICON = None

    _FILEITEM_SIZE = None

    FILE_PROPERTIES.append(PROPERTY_NAME)
    FILE_PROPERTIES.append(PROPERTY_ICON)
    FILE_PROPERTIES.append(PROPERTY_SIZE)
    FILE_PROPERTIES.append(PROPERTY_LASTMODIFIED)
    FILE_PROPERTIES = list(FILE_PROPERTIES)

    try:
        _FILEITEM_LASTMODIFIED = getattr(FileItem, 'lastModified')
        _FILEITEM_NAME = getattr(FileItem, 'getName')
        _FILEITEM_ICON = getattr(FileItem, 'getIcon')
        _FILEITEM_SIZE = getattr(FileItem, 'getSize')
    except AttributeError, e:
        raise RuntimeError, 'Internal error finding methods in FilesystemContainer'


    def __init__(self, *args):
        """Constructs a new <code>FileSystemContainer</code> with the specified file
        as the root of the filesystem. The files are included recursively.

        @param root
                   the root file for the new file-system container. Null values
                   are ignored.
        ---
        Constructs a new <code>FileSystemContainer</code> with the specified file
        as the root of the filesystem. The files are included recursively.

        @param root
                   the root file for the new file-system container.
        @param recursive
                   should the container recursively contain subdirectories.
        ---
        Constructs a new <code>FileSystemContainer</code> with the specified file
        as the root of the filesystem.

        @param root
                   the root file for the new file-system container.
        @param extension
                   the Filename extension (w/o separator) to limit the files in
                   container.
        @param recursive
                   should the container recursively contain subdirectories.
        ---
        Constructs a new <code>FileSystemContainer</code> with the specified root
        and recursivity status.

        @param root
                   the root file for the new file-system container.
        @param filter
                   the Filename filter to limit the files in container.
        @param recursive
                   should the container recursively contain subdirectories.
        """
        self._roots = []
        self._filter = None
        self._recursive = True

        args = args
        nargs = len(args)
        if nargs == 1:
            root, = args
            if root is not None:
                self._roots = [root]
        elif nargs == 2:
            root, recursive = args
            self.__init__(root)
            self.setRecursive(recursive)
        elif nargs == 3:
            if isinstance(args[1], None):  ## FIXME: FilenameFilter
                root, fltr, recursive = args
                self.__init__(root)
                self.setFilter(fltr)
                self.setRecursive(recursive)
            else:
                root, extension, recursive = args
                self.__init__(root)
                self.setFilter(extension)
                self.setRecursive(recursive)
        else:
            raise ValueError, 'invalid number of arguments'


    def addRoot(self, root):
        """Adds new root file directory. Adds a file to be included as root file
        directory in the <code>FilesystemContainer</code>.

        @param root
                   the File to be added as root directory. Null values are
                   ignored.
        """
        if root is not None:
            newRoots = [None] * (len(self._roots) + 1)
            for i in range(len(self._roots)):
                newRoots[i] = self._roots[i]

            newRoots[len(self._roots)] = root
            self._roots = newRoots


    def areChildrenAllowed(self, itemId):
        """Tests if the specified Item in the container may have children. Since a
        <code>FileSystemContainer</code> contains files and directories, this
        method returns <code>true</code> for directory Items only.

        @param itemId
                   the id of the item.
        @return <code>true</code> if the specified Item is a directory,
                <code>false</code> otherwise.
        """
        return isinstance(itemId, file) and itemId.canRead() and itemId.isDirectory()  # FIXME: File


    def getChildren(self, itemId):
        # Gets the ID's of all Items who are children of the specified Item. Don't
        # add a JavaDoc comment here, we use the default documentation from
        # implemented interface.
        if not isinstance(itemId, file):
            return list()

        if self._filter is not None:
            f = itemId.listFiles(self._filter)
        else:
            f = itemId.listFiles()

        if f is None:
            return list()

        l = list(f)
        sorted(l)
        return list(l)


    def getParent(self, itemId):
        # Gets the parent item of the specified Item. Don't add a JavaDoc comment
        # here, we use the default documentation from implemented interface.
        if not isinstance(itemId, file):
            return None
        return itemId.getParentFile()


    def hasChildren(self, itemId):
        # Tests if the specified Item has any children. Don't add a JavaDoc comment
        # here, we use the default documentation from implemented interface.
        if not isinstance(itemId, file):
            return False
        if self._filter is not None:
            l = itemId.list(self._filter)
        else:
            l = itemId.list()
        return l is not None and len(l) > 0


    def isRoot(self, itemId):
        # Tests if the specified Item is the root of the filesystem. Don't add a
        # JavaDoc comment here, we use the default documentation from implemented
        # interface.
        if not isinstance(itemId, file):
            return False

        for i in range(len(self._roots)):
            if self._roots[i] == itemId:
                return True

        return False


    def rootItemIds(self):
        # Gets the ID's of all root Items in the container. Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        # in single root case we use children
        if len(self._roots) == 1:
            if self._filter is not None:
                f = self._roots[0].listFiles(self._filter)
            else:
                f = self._roots[0].listFiles()
        else:
            f = self._roots

        if f is None:
            return list()

        l = list(f)
        sorted(l)

        return list(l)


    def setChildrenAllowed(self, itemId, areChildrenAllowed):
        """Returns <code>false</code> when conversion from files to directories is
        not supported.

        @param itemId
                   the ID of the item.
        @param areChildrenAllowed
                   the boolean value specifying if the Item can have children or
                   not.
        @return <code>true</code> if the operaton is successful otherwise
                <code>false</code>.
        @throws UnsupportedOperationException
                    if the setChildrenAllowed is not supported.
        """
        raise NotImplementedError, 'Conversion file to/from directory is not supported'


    def setParent(self, itemId, newParentId):
        """Returns <code>false</code> when moving files around in the filesystem is
        not supported.

        @param itemId
                   the ID of the item.
        @param newParentId
                   the ID of the Item that's to be the new parent of the Item
                   identified with itemId.
        @return <code>true</code> if the operation is successful otherwise
                <code>false</code>.
        @throws UnsupportedOperationException
                    if the setParent is not supported.
        """

        raise NotImplementedError, 'File moving is not supported'


    def containsId(self, itemId):
        # Tests if the filesystem contains the specified Item. Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.
        if not isinstance(itemId, file):
            return False
        val = False

        # Try to match all roots
        for i in range(len(self._roots)):
            try:
                val |= itemId.getCanonicalPath().startswith(self._roots[i].getCanonicalPath())
            except IOError:
                # Exception ignored
                pass

        if val and self._filter is not None:
            val &= self._filter.accept(itemId.getParentFile(), itemId.getName())

        return val


    def getItem(self, itemId):
        # Gets the specified Item from the filesystem. Don't add a JavaDoc comment
        # here, we use the default documentation from implemented interface.
        if not isinstance(itemId, file):
            return None

        return FileItem(itemId)


    def addItemIds(self, col, f):
        """Internal recursive method to add the files under the specified directory
        to the collection.

        @param col
                   the collection where the found items are added
        @param f
                   the root file where to start adding files
        """
        # Gets the IDs of Items in the filesystem. Don't add a JavaDoc comment
        # here, we use the default documentation from implemented interface.

        if self._filter is not None:
            l = f.listFiles(self._filter)
        else:
            l = f.listFiles()

        ll = list(l)
        sorted(ll)

        for lf in ll:
            col.add(lf)
            if lf.isDirectory():
                self.addItemIds(col, lf)


    def getItemIds(self):
        if self._recursive:
            col = list()
            for i in range(len(self._roots)):
                self.addItemIds(col, self._roots[i])

            return list(col)
        else:
            if len(self._roots) == 1:
                if self._filter is not None:
                    f = self._roots[0].listFiles(self._filter)
                else:
                    f = self._roots[0].listFiles()
            else:
                f = self._roots

            if f is None:
                return list()

            l = list(f)
            sorted(l)

            return list(l)


    def getContainerProperty(self, itemId, propertyId):
        """Gets the specified property of the specified file Item. The available
        file properties are "Name", "Size" and "Last Modified". If propertyId is
        not one of those, <code>null</code> is returned.

        @param itemId
                   the ID of the file whose property is requested.
        @param propertyId
                   the property's ID.
        @return the requested property's value, or <code>null</code>
        """
        if not isinstance(itemId, file):
            return None

        if propertyId == self.PROPERTY_NAME:
            return MethodProperty(self.getType(propertyId), FileItem(itemId), self._FILEITEM_NAME, None)

        if propertyId == self.PROPERTY_ICON:
            return MethodProperty(self.getType(propertyId), FileItem(itemId), self._FILEITEM_ICON, None)

        if propertyId == self.PROPERTY_SIZE:
            return MethodProperty(self.getType(propertyId), FileItem(itemId), self._FILEITEM_SIZE, None)

        if propertyId == self.PROPERTY_LASTMODIFIED:
            return MethodProperty(self.getType(propertyId), FileItem(itemId), self._FILEITEM_LASTMODIFIED, None)

        return None


    def getContainerPropertyIds(self):
        """Gets the collection of available file properties.

        @return Unmodifiable collection containing all available file properties.
        """
        return self.FILE_PROPERTIES


    def getType(self, propertyId):
        """Gets the specified property's data type. "Name" is a <code>String</code>,
        "Size" is a <code>Long</code>, "Last Modified" is a <code>Date</code>. If
        propertyId is not one of those, <code>null</code> is returned.

        @param propertyId
                   the ID of the property whose type is requested.
        @return data type of the requested property, or <code>null</code>
        """
        if propertyId == self.PROPERTY_NAME:
            return str

        if propertyId == self.PROPERTY_ICON:
            return Resource

        if propertyId == self.PROPERTY_SIZE:
            return long

        if propertyId == self.PROPERTY_LASTMODIFIED:
            return datetime

        return None


    def getFileCounts(self, f):
        """Internal method to recursively calculate the number of files under a root
        directory.

        @param f
                   the root to start counting from.
        """
        if self._filter is not None:
            l = f.listFiles(self._filter)
        else:
            l = f.listFiles()

        if l is None:
            return 0

        ret = len(l)
        for i in range(len(l)):
            if l[i].isDirectory():
                ret += self.getFileCounts(l[i])

        return ret


    def size(self):
        """Gets the number of Items in the container. In effect, this is the
        combined amount of files and directories.

        @return Number of Items in the container.
        """
        if self._recursive:
            counts = 0
            for i in range(len(self._roots)):
                counts += self.getFileCounts(self._roots[i])

            return counts
        else:
            if len(self._roots) == 1:
                if self._filter is not None:
                    f = self._roots[0].listFiles(self._filter)
                else:
                    f = self._roots[0].listFiles()
            else:
                f = self._roots

            if f is None:
                return 0

            return len(f)


    def getFilter(self):
        """Returns the file filter used to limit the files in this container.

        @return Used filter instance or null if no filter is assigned.
        """
        return self._filter


    def setFilter(self, filter_or_extension):
        """Sets the file filter used to limit the files in this container.

        @param filter
                   The filter to set. <code>null</code> disables filtering.
        ---
        Sets the file filter used to limit the files in this container.

        @param extension
                   the Filename extension (w/o separator) to limit the files in
                   container.
        """
        if isinstance(filter_or_extension, None):  # FilenameFilter
            self._filter = filter_or_extension
        else:
            self._filter = self.FileExtensionFilter(filter_or_extension)


    def isRecursive(self):
        """Is this container recursive filesystem.

        @return <code>true</code> if container is recursive, <code>false</code>
                otherwise.
        """
        return self._recursive


    def setRecursive(self, recursive):
        """Sets the container recursive property. Set this to false to limit the
        files directly under the root file.
        <p>
        Note : This is meaningful only if the root really is a directory.
        </p>

        @param recursive
                   the New value for recursive property.
        """
        self._recursive = recursive


    def addContainerProperty(self, propertyId, typ, defaultValue):
        # (non-Javadoc)
        #
        # @see com.vaadin.data.Container#addItem()

        raise NotImplementedError, 'File system container does not support this operation'


    def addItem(self, itemId=None):
        raise NotImplementedError, 'File system container does not support this operation'


    def removeAllItems(self):
        raise NotImplementedError, 'File system container does not support this operation'


    def removeItem(self, itemId):
        raise NotImplementedError, 'File system container does not support this operation'


    def removeContainerProperty(self, propertyId):
        raise NotImplementedError, 'File system container does not support this operation'


class FileExtensionFilter(object):  # FIXME: FilenameFilter
    """Generic file extension filter for displaying only files having certain
    extension.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """

    def __init__(self, fileExtension):
        """Constructs a new FileExtensionFilter using given extension.

        @param fileExtension
                   the File extension without the separator (dot).
        """
        self._filter = '.' + fileExtension


    def accept(self, directory, name):
        """Allows only files with the extension and directories.

        @see java.io.FilenameFilter#accept(File, String)
        """
        if name.endswith(self._filter):
            return True

        return file(directory, name).isDirectory()
