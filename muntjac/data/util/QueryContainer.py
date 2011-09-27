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

from muntjac.data.Item import Item
from muntjac.data.util.ObjectProperty import ObjectProperty
from muntjac.data.Container import Container, Indexed, Ordered


class QueryContainer(Container, Container, Ordered, Container, Indexed):
    """<p>
    The <code>QueryContainer</code> is the specialized form of Container which is
    Ordered and Indexed. This is used to represent the contents of relational
    database tables accessed through the JDBC Connection in the Vaadin Table.
    This creates Items based on the queryStatement provided to the container.
    </p>

    <p>
    The <code>QueryContainer</code> can be visualized as a representation of a
    relational database table.Each Item in the container represents the row
    fetched by the query.All cells in a column have same data type and the data
    type information is retrieved from the metadata of the resultset.
    </p>

    <p>
    Note : If data in the tables gets modified, Container will not get reflected
    with the updates, we have to explicity invoke QueryContainer.refresh method.
    {@link com.vaadin.data.util.QueryContainer#refresh() refresh()}
    </p>

    @see com.vaadin.data.Container

    @author IT Mill Ltd.
    @version
    @since 4.0

    @deprecated will be removed in the future, use the SQLContainer add-on
    """

    # default ResultSet type
#    DEFAULT_RESULTSET_TYPE = ResultSet.TYPE_SCROLL_INSENSITIVE

    # default ResultSet concurrency
#    DEFAULT_RESULTSET_CONCURRENCY = ResultSet.CONCUR_READ_ONLY

    def __init__(self, *args):
        """Constructs new <code>QueryContainer</code> with the specified
        <code>queryStatement</code>.

        @param queryStatement
                   Database query
        @param connection
                   Connection object
        @param resultSetType
        @param resultSetConcurrency
        @throws SQLException
                    when database operation fails
        ---
        Constructs new <code>QueryContainer</code> with the specified
        queryStatement using the default resultset type and default resultset
        concurrency.

        @param queryStatement
                   Database query
        @param connection
                   Connection object
        @see QueryContainer#DEFAULT_RESULTSET_TYPE
        @see QueryContainer#DEFAULT_RESULTSET_CONCURRENCY
        @throws SQLException
                    when database operation fails
        """
        self._resultSetType = self.DEFAULT_RESULTSET_TYPE
        self._resultSetConcurrency = self.DEFAULT_RESULTSET_CONCURRENCY
        self._queryStatement = None
        self._connection = None
        self._result = None
        self._propertyIds = None
        self._propertyTypes = dict()
        self._size = -1
        self._statement = None

        _0 = args
        _1 = len(args)
        if _1 == 2:
            queryStatement, connection = _0
            self.__init__(queryStatement, connection, self.DEFAULT_RESULTSET_TYPE, self.DEFAULT_RESULTSET_CONCURRENCY)
        elif _1 == 4:
            queryStatement, connection, resultSetType, resultSetConcurrency = _0
            self._queryStatement = queryStatement
            self._connection = connection
            self._resultSetType = resultSetType
            self._resultSetConcurrency = resultSetConcurrency
            self.init()
        else:
            raise ValueError

    def init(self):
        """Fills the Container with the items and properties. Invoked by the
        constructor.

        @throws SQLException
                    when parameter initialization fails.
        @see QueryContainer#QueryContainer(String, Connection, int, int).
        """
        self.refresh()
        metadata = self._result.getMetaData()
        count = metadata.getColumnCount()
        l = list(count)
        _0 = True
        i = 1
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i <= count):
                break
            columnName = metadata.getColumnName(i)
            l.add(columnName)
            p = self.getContainerProperty(int(1), columnName)
            self._propertyTypes.put(columnName, self.Object if p is None else p.getType())
        self._propertyIds = list(l)


    def refresh(self):
        """<p>
        Restores items in the container. This method will update the latest data
        to the container.
        </p>
        Note: This method should be used to update the container with the latest
        items.

        @throws SQLException
                    when database operation fails
        """
        self.close()
        self._statement = self._connection.createStatement(self._resultSetType, self._resultSetConcurrency)
        self._result = self._statement.executeQuery(self._queryStatement)
        self._result.last()
        self._size = self._result.getRow()


    def close(self):
        """Releases and nullifies the <code>statement</code>.

        @throws SQLException
                    when database operation fails
        """
        if self._statement is not None:
            self._statement.close()
        self._statement = None


    def getItem(self, idd):
        """Gets the Item with the given Item ID from the Container.

        @param id
                   ID of the Item to retrieve
        @return Item Id.
        """
        return self.Row(idd)


    def getContainerPropertyIds(self):
        """Gets the collection of propertyId from the Container.

        @return Collection of Property ID.
        """
        return self._propertyIds


    def getItemIds(self):
        """Gets an collection of all the item IDs in the container.

        @return collection of Item IDs
        """
        c = list(self._size)
        _0 = True
        i = 1
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i <= self._size):
                break
            c.add(int(i))
        return c

    def getContainerProperty(self, itemId, propertyId):
        """Gets the property identified by the given itemId and propertyId from the
        container. If the container does not contain the property
        <code>null</code> is returned.

        @param itemId
                   ID of the Item which contains the Property
        @param propertyId
                   ID of the Property to retrieve

        @return Property with the given ID if exists; <code>null</code>
                otherwise.
        """
        if not (isinstance(itemId, int) and isinstance(propertyId, str)):
            return None
        # Handle also null values from the database
        try:
            self._result.absolute(itemId.intValue())
            value = self._result.getObject(propertyId)
        except Exception:
            return None
        return ObjectProperty(value if value is not None else str(''))

    def getType(self, idd):
        """Gets the data type of all properties identified by the given type ID.

        @param id
                   ID identifying the Properties

        @return data type of the Properties
        """
        return self._propertyTypes[idd]


    def size(self):
        """Gets the number of items in the container.

        @return the number of items in the container.
        """
        return self._size

    def containsId(self, idd):
        """Tests if the list contains the specified Item.

        @param id
                   ID the of Item to be tested.
        @return <code>true</code> if given id is in the container;
                <code>false</code> otherwise.
        """
        if not isinstance(id, int):
            return False
        i = id.intValue()
        if i < 1:
            return False
        if i > self._size:
            return False
        return True

    def addItem(self, *args):
        """Creates new Item with the given ID into the Container.

        @param itemId
                   ID of the Item to be created.

        @return Created new Item, or <code>null</code> if it fails.

        @throws UnsupportedOperationException
                    if the addItem method is not supported.
        ---
        Creates a new Item into the Container, and assign it an ID.

        @return ID of the newly created Item, or <code>null</code> if it fails.
        @throws UnsupportedOperationException
                    if the addItem method is not supported.
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            raise NotImplementedError
        elif _1 == 1:
            raise NotImplementedError
        else:
            raise ValueError


    def removeItem(self, itemId):
        """Removes the Item identified by ItemId from the Container.

        @param itemId
                   ID of the Item to remove.
        @return <code>true</code> if the operation succeeded; <code>false</code>
                otherwise.
        @throws UnsupportedOperationException
                    if the removeItem method is not supported.
        """
        raise NotImplementedError

    def addContainerProperty(self, propertyId, typ, defaultValue):
        """Adds new Property to all Items in the Container.

        @param propertyId
                   ID of the Property
        @param type
                   Data type of the new Property
        @param defaultValue
                   The value all created Properties are initialized to.
        @return <code>true</code> if the operation succeeded; <code>false</code>
                otherwise.
        @throws UnsupportedOperationException
                    if the addContainerProperty method is not supported.
        """
        raise NotImplementedError


    def removeContainerProperty(self, propertyId):
        """Removes a Property specified by the given Property ID from the Container.

        @param propertyId
                   ID of the Property to remove
        @return <code>true</code> if the operation succeeded; <code>false</code>
                otherwise.
        @throws UnsupportedOperationException
                    if the removeContainerProperty method is not supported.
        """
        raise NotImplementedError


    def removeAllItems(self):
        """Removes all Items from the Container.

        @return <code>true</code> if the operation succeeded; <code>false</code>
                otherwise.
        @throws UnsupportedOperationException
                    if the removeAllItems method is not supported.
        """
        raise NotImplementedError


    def addItemAfter(self, *args):
        """Adds new item after the given item.

        @param previousItemId
                   Id of the previous item in ordered container.
        @param newItemId
                   Id of the new item to be added.
        @return Returns new item or <code>null</code> if the operation fails.
        @throws UnsupportedOperationException
                    if the addItemAfter method is not supported.
        ---
        Adds new item after the given item.

        @param previousItemId
                   Id of the previous item in ordered container.
        @return Returns item id created new item or <code>null</code> if the
                operation fails.
        @throws UnsupportedOperationException
                    if the addItemAfter method is not supported.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            raise NotImplementedError
        elif _1 == 2:
            raise NotImplementedError
        else:
            raise ValueError


    def firstItemId(self):
        """Returns id of first item in the Container.

        @return ID of the first Item in the list.
        """
        if self._size < 1:
            return None
        return int(1)


    def isFirstId(self, idd):
        """Returns <code>true</code> if given id is first id at first index.

        @param id
                   ID of an Item in the Container.
        """
        return self._size > 0 and isinstance(id, int) and id.intValue() == 1

    def isLastId(self, idd):
        """Returns <code>true</code> if given id is last id at last index.

        @param id
                   ID of an Item in the Container
        """
        return self._size > 0 and isinstance(id, int) and id.intValue() == self._size


    def lastItemId(self):
        """Returns id of last item in the Container.

        @return ID of the last Item.
        """
        if self._size < 1:
            return None
        return int(self._size)


    def nextItemId(self, idd):
        """Returns id of next item in container at next index.

        @param id
                   ID of an Item in the Container.
        @return ID of the next Item or null.
        """
        if (self._size < 1) or (not isinstance(id, int)):
            return None
        i = id.intValue()
        if i >= self._size:
            return None
        return int(i + 1)


    def prevItemId(self, idd):
        """Returns id of previous item in container at previous index.

        @param id
                   ID of an Item in the Container.
        @return ID of the previous Item or null.
        """
        if (self._size < 1) or (not isinstance(id, int)):
            return None
        i = id.intValue()
        if i <= 1:
            return None
        return int(i - 1)


    def finalize(self):
        """Closes the statement.

        @see #close()
        """
        try:
            self.close()
        except Exception:  # SQLException
            pass

    def addItemAt(self, *args):
        """Adds the given item at the position of given index.

        @param index
                   Index to add the new item.
        @param newItemId
                   Id of the new item to be added.
        @return new item or <code>null</code> if the operation fails.
        @throws UnsupportedOperationException
                    if the addItemAt is not supported.
        ---
        Adds item at the position of provided index in the container.

        @param index
                   Index to add the new item.
        @return item id created new item or <code>null</code> if the operation
                fails.

        @throws UnsupportedOperationException
                    if the addItemAt is not supported.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            raise NotImplementedError
        elif _1 == 2:
            raise NotImplementedError
        else:
            raise ValueError


    def getIdByIndex(self, index):
        """Gets the Index id in the container.

        @param index
                   Index Id.
        @return ID in the given index.
        """
        if ((self._size < 1) or (index < 0)) or (index >= self._size):
            return None
        return int(index + 1)

    def indexOfId(self, idd):
        """Gets the index of the Item corresponding to id in the container.

        @param id
                   ID of an Item in the Container
        @return index of the Item, or -1 if the Container does not include the
                Item
        """
        if (self._size < 1) or (not isinstance(id, int)):
            return -1
        i = id.intValue()
        if (i >= self._size) or (i < 1):
            return -1
        return i - 1


class Row(Item):
    """The <code>Row</code> class implements methods of Item.

    @author IT Mill Ltd.
    @version
    @since 4.0
    """
    _id = None

    def __init__(self, rowId):
        self._id = rowId

    def addItemProperty(self, idd, prop):
        """Adds the item property.

        @param id
                   ID of the new Property.
        @param property
                   Property to be added and associated with ID.
        @return <code>true</code> if the operation succeeded;
                <code>false</code> otherwise.
        @throws UnsupportedOperationException
                    if the addItemProperty method is not supported.
        """
        raise NotImplementedError

    def getItemProperty(self, propertyId):
        """Gets the property corresponding to the given property ID stored in
        the Item.

        @param propertyId
                   identifier of the Property to get
        @return the Property with the given ID or <code>null</code>
        """
        return self.getContainerProperty(self._id, propertyId)

    def getItemPropertyIds(self):
        """Gets the collection of property IDs stored in the Item.

        @return unmodifiable collection containing IDs of the Properties
                stored the Item.
        """
        return self.propertyIds

    def removeItemProperty(self, idd):
        """Removes given item property.

        @param id
                   ID of the Property to be removed.
        @return <code>true</code> if the item property is removed;
                <code>false</code> otherwise.
        @throws UnsupportedOperationException
                    if the removeItemProperty is not supported.
        """
        raise NotImplementedError
