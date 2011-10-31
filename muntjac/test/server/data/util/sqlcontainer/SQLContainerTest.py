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

from com.vaadin.data.util.sqlcontainer.DataGenerator import (DataGenerator,)
from com.vaadin.data.util.sqlcontainer.FreeformQueryUtil import (FreeformQueryUtil,)
from com.vaadin.data.util.sqlcontainer.AllTests import (AllTests,)
# from com.vaadin.data.Container.Filter import (Filter,)
# from com.vaadin.data.Container.ItemSetChangeEvent import (ItemSetChangeEvent,)
# from com.vaadin.data.Container.ItemSetChangeListener import (ItemSetChangeListener,)
# from com.vaadin.data.Item import (Item,)
# from com.vaadin.data.util.filter.Compare.Equal import (Equal,)
# from com.vaadin.data.util.filter.Like import (Like,)
# from com.vaadin.data.util.sqlcontainer.connection.JDBCConnectionPool import (JDBCConnectionPool,)
# from com.vaadin.data.util.sqlcontainer.connection.SimpleJDBCConnectionPool import (SimpleJDBCConnectionPool,)
# from com.vaadin.data.util.sqlcontainer.query.FreeformQuery import (FreeformQuery,)
# from com.vaadin.data.util.sqlcontainer.query.FreeformQueryDelegate import (FreeformQueryDelegate,)
# from com.vaadin.data.util.sqlcontainer.query.FreeformStatementDelegate import (FreeformStatementDelegate,)
# from com.vaadin.data.util.sqlcontainer.query.OrderBy import (OrderBy,)
# from com.vaadin.data.util.sqlcontainer.query.generator.MSSQLGenerator import (MSSQLGenerator,)
# from com.vaadin.data.util.sqlcontainer.query.generator.OracleGenerator import (OracleGenerator,)
# from com.vaadin.data.util.sqlcontainer.query.generator.SQLGenerator import (SQLGenerator,)
# from com.vaadin.data.util.sqlcontainer.query.generator.StatementHelper import (StatementHelper,)
# from com.vaadin.data.util.sqlcontainer.query.generator.filter.QueryBuilder import (QueryBuilder,)
# from java.math.BigDecimal import (BigDecimal,)
# from java.sql.Connection import (Connection,)
# from java.sql.SQLException import (SQLException,)
# from java.sql.Statement import (Statement,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Collection import (Collection,)
# from java.util.List import (List,)
# from java.util.logging.Handler import (Handler,)
# from java.util.logging.LogRecord import (LogRecord,)
# from java.util.logging.Logger import (Logger,)
# from org.easymock.EasyMock import (EasyMock,)
# from org.easymock.IAnswer import (IAnswer,)
# from org.junit.After import (After,)
# from org.junit.Assert import (Assert,)
# from org.junit.Before import (Before,)
# from org.junit.Test import (Test,)
DB = AllTests.DB


class SQLContainerTest(object):
    _offset = AllTests.offset
    _connectionPool = None

    def setUp(self):
        try:
            self._connectionPool = SimpleJDBCConnectionPool(AllTests.dbDriver, AllTests.dbURL, AllTests.dbUser, AllTests.dbPwd, 2, 2)
        except SQLException, e:
            e.printStackTrace()
            Assert.fail(e.getMessage())
        DataGenerator.addPeopleToDatabase(self._connectionPool)

    def tearDown(self):
        if self._connectionPool is not None:
            self._connectionPool.destroy()

    def constructor_withFreeformQuery_shouldSucceed(self):
        self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))

    def constructor_withIllegalFreeformQuery_shouldFail(self):
        c = self.SQLContainer(FreeformQuery('SELECT * FROM asdf', self._connectionPool, 'ID'))
        c.getItem(c.firstItemId())

    def containsId_withFreeformQueryAndExistingId_returnsTrue(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        Assert.assertTrue(container.containsId(self.RowId([1])))

    def containsId_withFreeformQueryAndNonexistingId_returnsFalse(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        Assert.assertFalse(container.containsId(self.RowId([1337])))

    def getContainerProperty_freeformExistingItemIdAndPropertyId_returnsProperty(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals('Ville', container.getContainerProperty(self.RowId([BigDecimal(0 + self._offset)]), 'NAME').getValue())
        else:
            Assert.assertEquals('Ville', container.getContainerProperty(self.RowId([0 + self._offset]), 'NAME').getValue())

    def getContainerProperty_freeformExistingItemIdAndNonexistingPropertyId_returnsNull(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        Assert.assertNull(container.getContainerProperty(self.RowId([1 + self._offset]), 'asdf'))

    def getContainerProperty_freeformNonexistingItemId_returnsNull(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        Assert.assertNull(container.getContainerProperty(self.RowId([1337 + self._offset]), 'NAME'))

    def getContainerPropertyIds_freeform_returnsIDAndNAME(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        propertyIds = container.getContainerPropertyIds()
        Assert.assertEquals(3, len(propertyIds))
        Assert.assertArrayEquals(['ID', 'NAME', 'AGE'], list(propertyIds))

    def getItem_freeformExistingItemId_returnsItem(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        if AllTests.db == DB.ORACLE:
            item = container.getItem(self.RowId([BigDecimal(0 + self._offset)]))
        else:
            item = container.getItem(self.RowId([0 + self._offset]))
        Assert.assertNotNull(item)
        Assert.assertEquals('Ville', item.getItemProperty('NAME').getValue())

    def getItem_freeform5000RowsWithParameter1337_returnsItemWithId1337(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        if AllTests.db == DB.ORACLE:
            item = container.getItem(self.RowId([BigDecimal(1337 + self._offset)]))
            Assert.assertNotNull(item)
            Assert.assertEquals(BigDecimal(1337 + self._offset), item.getItemProperty('ID').getValue())
        else:
            item = container.getItem(self.RowId([1337 + self._offset]))
            Assert.assertNotNull(item)
            Assert.assertEquals(1337 + self._offset, item.getItemProperty('ID').getValue())
        Assert.assertEquals('Person 1337', item.getItemProperty('NAME').getValue())

    def getItemIds_freeform_returnsItemIdsWithKeys0through3(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        itemIds = container.getItemIds()
        Assert.assertEquals(4, len(itemIds))
        zero = self.RowId([0 + self._offset])
        one = self.RowId([1 + self._offset])
        two = self.RowId([2 + self._offset])
        three = self.RowId([3 + self._offset])
        if AllTests.db == DB.ORACLE:
            correct = ['1', '2', '3', '4']
            oracle = list()
            for o in itemIds:
                oracle.add(str(o))
            Assert.assertArrayEquals(correct, list(oracle))
        else:
            Assert.assertArrayEquals([zero, one, two, three], list(itemIds))

    def getType_freeformNAMEPropertyId_returnsString(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        Assert.assertEquals(str, container.getType('NAME'))

    def getType_freeformIDPropertyId_returnsInteger(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals(BigDecimal, container.getType('ID'))
        else:
            Assert.assertEquals(int, container.getType('ID'))

    def getType_freeformNonexistingPropertyId_returnsNull(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        Assert.assertNull(container.getType('asdf'))

    def size_freeform_returnsFour(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        Assert.assertEquals(4, len(container))

    def size_freeformOneAddedItem_returnsFive(self):
        conn = self._connectionPool.reserveConnection()
        statement = conn.createStatement()
        if AllTests.db == DB.MSSQL:
            statement.executeUpdate('insert into people values(\'Bengt\', \'42\')')
        else:
            statement.executeUpdate('insert into people values(default, \'Bengt\', \'42\')')
        statement.close()
        conn.commit()
        self._connectionPool.releaseConnection(conn)
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        Assert.assertEquals(5, len(container))

    def indexOfId_freeformWithParameterThree_returnsThree(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals(3, container.indexOfId(self.RowId([BigDecimal(3 + self._offset)])))
        else:
            Assert.assertEquals(3, container.indexOfId(self.RowId([3 + self._offset])))

    def indexOfId_freeform5000RowsWithParameter1337_returns1337(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people ORDER BY \"ID\" ASC', self._connectionPool, 'ID'))
        if AllTests.db == DB.ORACLE:
            container.getItem(self.RowId([BigDecimal(1337 + self._offset)]))
            Assert.assertEquals(1337, container.indexOfId(self.RowId([BigDecimal(1337 + self._offset)])))
        else:
            container.getItem(self.RowId([1337 + self._offset]))
            Assert.assertEquals(1337, container.indexOfId(self.RowId([1337 + self._offset])))

    def getIdByIndex_freeform5000rowsIndex1337_returnsRowId1337(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people ORDER BY \"ID\" ASC', self._connectionPool, 'ID'))
        itemId = container.getIdByIndex(1337)
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals(self.RowId([BigDecimal(1337 + self._offset)]), itemId)
        else:
            Assert.assertEquals(self.RowId([1337 + self._offset]), itemId)

    def getIdByIndex_freeformWithPaging5000rowsIndex1337_returnsRowId1337(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        query = FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID')
        delegate = EasyMock.createMock(FreeformQueryDelegate)


        class _0_(IAnswer):

            def answer(self):
                args = EasyMock.getCurrentArguments()
                offset = args[0]
                limit = args[1]
                if AllTests.db == DB.MSSQL:
                    start = offset + 1
                    end = offset + limit + 1
                    q = 'SELECT * FROM (SELECT row_number() OVER' + ' ( ORDER BY \"ID\" ASC) AS rownum, * FROM people)' + ' AS a WHERE a.rownum BETWEEN ' + start + ' AND ' + end
                    return q
                elif AllTests.db == DB.ORACLE:
                    start = offset + 1
                    end = offset + limit + 1
                    q = 'SELECT * FROM (SELECT x.*, ROWNUM AS r FROM' + ' (SELECT * FROM people ORDER BY \"ID\" ASC) x) ' + ' WHERE r BETWEEN ' + start + ' AND ' + end
                    return q
                else:
                    return 'SELECT * FROM people LIMIT ' + limit + ' OFFSET ' + offset


        _0_ = _0_()
        EasyMock.expect(delegate.getQueryString(EasyMock.anyInt(), EasyMock.anyInt())).andAnswer(_0_)
        None.anyTimes()
        delegate.setFilters(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setFilters(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        EasyMock.expect(delegate.getCountQuery()).andThrow(self.NotImplementedError()).anyTimes()
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        container = self.SQLContainer(query)
        itemId = container.getIdByIndex(1337)
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals(str(self.RowId([1337 + self._offset])), str(itemId))
        else:
            Assert.assertEquals(self.RowId([1337 + self._offset]), itemId)

    def nextItemId_freeformCurrentItem1337_returnsItem1338(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people ORDER BY \"ID\" ASC', self._connectionPool, 'ID'))
        itemId = container.getIdByIndex(1337)
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals(str(self.RowId([1338 + self._offset])), str(container.nextItemId(itemId)))
        else:
            Assert.assertEquals(self.RowId([1338 + self._offset]), container.nextItemId(itemId))

    def prevItemId_freeformCurrentItem1337_returns1336(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people ORDER BY \"ID\" ASC', self._connectionPool, 'ID'))
        itemId = container.getIdByIndex(1337)
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals(str(self.RowId([1336 + self._offset])), str(container.prevItemId(itemId)))
        else:
            Assert.assertEquals(self.RowId([1336 + self._offset]), container.prevItemId(itemId))

    def firstItemId_freeform_returnsItemId0(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals(str(self.RowId([0 + self._offset])), str(container.firstItemId()))
        else:
            Assert.assertEquals(self.RowId([0 + self._offset]), container.firstItemId())

    def lastItemId_freeform5000Rows_returnsItemId4999(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people ORDER BY \"ID\" ASC', self._connectionPool, 'ID'))
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals(str(self.RowId([4999 + self._offset])), str(container.lastItemId()))
        else:
            Assert.assertEquals(self.RowId([4999 + self._offset]), container.lastItemId())

    def isFirstId_freeformActualFirstId_returnsTrue(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        if AllTests.db == DB.ORACLE:
            Assert.assertTrue(container.isFirstId(self.RowId([BigDecimal(0 + self._offset)])))
        else:
            Assert.assertTrue(container.isFirstId(self.RowId([0 + self._offset])))

    def isFirstId_freeformSecondId_returnsFalse(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        if AllTests.db == DB.ORACLE:
            Assert.assertFalse(container.isFirstId(self.RowId([BigDecimal(1 + self._offset)])))
        else:
            Assert.assertFalse(container.isFirstId(self.RowId([1 + self._offset])))

    def isLastId_freeformSecondId_returnsFalse(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        if AllTests.db == DB.ORACLE:
            Assert.assertFalse(container.isLastId(self.RowId([BigDecimal(1 + self._offset)])))
        else:
            Assert.assertFalse(container.isLastId(self.RowId([1 + self._offset])))

    def isLastId_freeformLastId_returnsTrue(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        if AllTests.db == DB.ORACLE:
            Assert.assertTrue(container.isLastId(self.RowId([BigDecimal(3 + self._offset)])))
        else:
            Assert.assertTrue(container.isLastId(self.RowId([3 + self._offset])))

    def isLastId_freeform5000RowsLastId_returnsTrue(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people ORDER BY \"ID\" ASC', self._connectionPool, 'ID'))
        if AllTests.db == DB.ORACLE:
            Assert.assertTrue(container.isLastId(self.RowId([BigDecimal(4999 + self._offset)])))
        else:
            Assert.assertTrue(container.isLastId(self.RowId([4999 + self._offset])))

    def refresh_freeform_sizeShouldUpdate(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        Assert.assertEquals(4, len(container))
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        container.refresh()
        Assert.assertEquals(5000, len(container))

    def refresh_freeformWithoutCallingRefresh_sizeShouldNotUpdate(self):
        # Yeah, this is a weird one. We're testing that the size doesn't update
        # after adding lots of items unless we call refresh inbetween. This to
        # make sure that the refresh method actually refreshes stuff and isn't
        # a NOP.
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        Assert.assertEquals(4, len(container))
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        Assert.assertEquals(4, len(container))

    def setAutoCommit_freeform_shouldSucceed(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        container.setAutoCommit(True)
        Assert.assertTrue(container.isAutoCommit())
        container.setAutoCommit(False)
        Assert.assertFalse(container.isAutoCommit())

    def getPageLength_freeform_returnsDefault100(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        Assert.assertEquals(100, container.getPageLength())

    def setPageLength_freeform_shouldSucceed(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        container.setPageLength(20)
        Assert.assertEquals(20, container.getPageLength())
        container.setPageLength(200)
        Assert.assertEquals(200, container.getPageLength())

    def addContainerProperty_normal_isUnsupported(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        container.addContainerProperty('asdf', str, '')

    def removeContainerProperty_normal_isUnsupported(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        container.removeContainerProperty('asdf')

    def addItemObject_normal_isUnsupported(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        container.addItem('asdf')

    def addItemAfterObjectObject_normal_isUnsupported(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        container.addItemAfter('asdf', 'foo')

    def addItemAtIntObject_normal_isUnsupported(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        container.addItemAt(2, 'asdf')

    def addItemAtInt_normal_isUnsupported(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        container.addItemAt(2)

    def addItemAfterObject_normal_isUnsupported(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        container.addItemAfter('asdf')

    def addItem_freeformAddOneNewItem_returnsItemId(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        itemId = container.addItem()
        Assert.assertNotNull(itemId)

    def addItem_freeformAddOneNewItem_shouldChangeSize(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        size = len(container)
        container.addItem()
        Assert.assertEquals(size + 1, len(container))

    def addItem_freeformAddTwoNewItems_shouldChangeSize(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        size = len(container)
        id1 = container.addItem()
        id2 = container.addItem()
        Assert.assertEquals(size + 2, len(container))
        Assert.assertNotSame(id1, id2)
        Assert.assertFalse(id1 == id2)

    def nextItemId_freeformNewlyAddedItem_returnsNewlyAdded(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        lastId = container.lastItemId()
        id = container.addItem()
        Assert.assertEquals(id, container.nextItemId(lastId))

    def lastItemId_freeformNewlyAddedItem_returnsNewlyAdded(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        lastId = container.lastItemId()
        id = container.addItem()
        Assert.assertEquals(id, container.lastItemId())
        Assert.assertNotSame(lastId, container.lastItemId())

    def indexOfId_freeformNewlyAddedItem_returnsFour(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id = container.addItem()
        Assert.assertEquals(4, container.indexOfId(id))

    def getItem_freeformNewlyAddedItem_returnsNewlyAdded(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id = container.addItem()
        Assert.assertNotNull(container.getItem(id))

    def getItem_freeformNewlyAddedItemAndFiltered_returnsNull(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        container.addContainerFilter(Equal('NAME', 'asdf'))
        id = container.addItem()
        Assert.assertNull(container.getItem(id))

    def getItemUnfiltered_freeformNewlyAddedItemAndFiltered_returnsNewlyAdded(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        container.addContainerFilter(Equal('NAME', 'asdf'))
        id = container.addItem()
        Assert.assertNotNull(container.getItemUnfiltered(id))

    def getItemIds_freeformNewlyAddedItem_containsNewlyAdded(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id = container.addItem()
        Assert.assertTrue(container.getItemIds().contains(id))

    def getContainerProperty_freeformNewlyAddedItem_returnsPropertyOfNewlyAddedItem(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id = container.addItem()
        item = container.getItem(id)
        item.getItemProperty('NAME').setValue('asdf')
        Assert.assertEquals('asdf', container.getContainerProperty(id, 'NAME').getValue())

    def containsId_freeformNewlyAddedItem_returnsTrue(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id = container.addItem()
        Assert.assertTrue(container.containsId(id))

    def prevItemId_freeformTwoNewlyAddedItems_returnsFirstAddedItem(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id1 = container.addItem()
        id2 = container.addItem()
        Assert.assertEquals(id1, container.prevItemId(id2))

    def firstItemId_freeformEmptyResultSet_returnsFirstAddedItem(self):
        DataGenerator.createGarbage(self._connectionPool)
        container = self.SQLContainer(FreeformQuery('SELECT * FROM GARBAGE', self._connectionPool, 'ID'))
        id = container.addItem()
        Assert.assertSame(id, container.firstItemId())

    def isFirstId_freeformEmptyResultSet_returnsFirstAddedItem(self):
        DataGenerator.createGarbage(self._connectionPool)
        container = self.SQLContainer(FreeformQuery('SELECT * FROM GARBAGE', self._connectionPool, 'ID'))
        id = container.addItem()
        Assert.assertTrue(container.isFirstId(id))

    def isLastId_freeformOneItemAdded_returnsTrueForAddedItem(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id = container.addItem()
        Assert.assertTrue(container.isLastId(id))

    def isLastId_freeformTwoItemsAdded_returnsTrueForLastAddedItem(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        container.addItem()
        id2 = container.addItem()
        Assert.assertTrue(container.isLastId(id2))

    def getIdByIndex_freeformOneItemAddedLastIndexInContainer_returnsAddedItem(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id = container.addItem()
        Assert.assertEquals(id, container.getIdByIndex(len(container) - 1))

    def removeItem_freeformNoAddedItems_removesItemFromContainer(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        size = len(container)
        id = container.firstItemId()
        Assert.assertTrue(container.removeItem(id))
        Assert.assertNotSame(id, container.firstItemId())
        Assert.assertEquals(size - 1, len(container))

    def containsId_freeformRemovedItem_returnsFalse(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id = container.firstItemId()
        Assert.assertTrue(container.removeItem(id))
        Assert.assertFalse(container.containsId(id))

    def containsId_unknownObject(self):

        class ensureNoLogging(Handler):

            def publish(self, record):
                Assert.fail('No messages should be logged')

            def flush(self):
                pass

            def close(self):
                pass

        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        logger = Logger.getLogger(self.SQLContainer.getName())
        logger.addHandler(ensureNoLogging)
        try:
            Assert.assertFalse(container.containsId(self.Object()))
        finally:
            logger.removeHandler(ensureNoLogging)

    def removeItem_freeformOneAddedItem_removesTheAddedItem(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id = container.addItem()
        size = len(container)
        Assert.assertTrue(container.removeItem(id))
        Assert.assertFalse(container.containsId(id))
        Assert.assertEquals(size - 1, len(container))

    def getItem_freeformItemRemoved_returnsNull(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id = container.firstItemId()
        Assert.assertTrue(container.removeItem(id))
        Assert.assertNull(container.getItem(id))

    def getItem_freeformAddedItemRemoved_returnsNull(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id = container.addItem()
        Assert.assertNotNull(container.getItem(id))
        Assert.assertTrue(container.removeItem(id))
        Assert.assertNull(container.getItem(id))

    def getItemIds_freeformItemRemoved_shouldNotContainRemovedItem(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id = container.firstItemId()
        Assert.assertTrue(container.getItemIds().contains(id))
        Assert.assertTrue(container.removeItem(id))
        Assert.assertFalse(container.getItemIds().contains(id))

    def getItemIds_freeformAddedItemRemoved_shouldNotContainRemovedItem(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id = container.addItem()
        Assert.assertTrue(container.getItemIds().contains(id))
        Assert.assertTrue(container.removeItem(id))
        Assert.assertFalse(container.getItemIds().contains(id))

    def containsId_freeformItemRemoved_returnsFalse(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id = container.firstItemId()
        Assert.assertTrue(container.containsId(id))
        Assert.assertTrue(container.removeItem(id))
        Assert.assertFalse(container.containsId(id))

    def containsId_freeformAddedItemRemoved_returnsFalse(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id = container.addItem()
        Assert.assertTrue(container.containsId(id))
        Assert.assertTrue(container.removeItem(id))
        Assert.assertFalse(container.containsId(id))

    def nextItemId_freeformItemRemoved_skipsRemovedItem(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        first = container.getIdByIndex(0)
        second = container.getIdByIndex(1)
        third = container.getIdByIndex(2)
        Assert.assertTrue(container.removeItem(second))
        Assert.assertEquals(third, container.nextItemId(first))

    def nextItemId_freeformAddedItemRemoved_skipsRemovedItem(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        first = container.lastItemId()
        second = container.addItem()
        third = container.addItem()
        Assert.assertTrue(container.removeItem(second))
        Assert.assertEquals(third, container.nextItemId(first))

    def prevItemId_freeformItemRemoved_skipsRemovedItem(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        first = container.getIdByIndex(0)
        second = container.getIdByIndex(1)
        third = container.getIdByIndex(2)
        Assert.assertTrue(container.removeItem(second))
        Assert.assertEquals(first, container.prevItemId(third))

    def prevItemId_freeformAddedItemRemoved_skipsRemovedItem(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        first = container.lastItemId()
        second = container.addItem()
        third = container.addItem()
        Assert.assertTrue(container.removeItem(second))
        Assert.assertEquals(first, container.prevItemId(third))

    def firstItemId_freeformFirstItemRemoved_resultChanges(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        first = container.firstItemId()
        Assert.assertTrue(container.removeItem(first))
        Assert.assertNotSame(first, container.firstItemId())

    def firstItemId_freeformNewlyAddedFirstItemRemoved_resultChanges(self):
        DataGenerator.createGarbage(self._connectionPool)
        container = self.SQLContainer(FreeformQuery('SELECT * FROM GARBAGE', self._connectionPool, 'ID'))
        first = container.addItem()
        second = container.addItem()
        Assert.assertSame(first, container.firstItemId())
        Assert.assertTrue(container.removeItem(first))
        Assert.assertSame(second, container.firstItemId())

    def lastItemId_freeformLastItemRemoved_resultChanges(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        last = container.lastItemId()
        Assert.assertTrue(container.removeItem(last))
        Assert.assertNotSame(last, container.lastItemId())

    def lastItemId_freeformAddedLastItemRemoved_resultChanges(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        last = container.addItem()
        Assert.assertSame(last, container.lastItemId())
        Assert.assertTrue(container.removeItem(last))
        Assert.assertNotSame(last, container.lastItemId())

    def isFirstId_freeformFirstItemRemoved_returnsFalse(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        first = container.firstItemId()
        Assert.assertTrue(container.removeItem(first))
        Assert.assertFalse(container.isFirstId(first))

    def isFirstId_freeformAddedFirstItemRemoved_returnsFalse(self):
        DataGenerator.createGarbage(self._connectionPool)
        container = self.SQLContainer(FreeformQuery('SELECT * FROM GARBAGE', self._connectionPool, 'ID'))
        first = container.addItem()
        container.addItem()
        Assert.assertSame(first, container.firstItemId())
        Assert.assertTrue(container.removeItem(first))
        Assert.assertFalse(container.isFirstId(first))

    def isLastId_freeformLastItemRemoved_returnsFalse(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        last = container.lastItemId()
        Assert.assertTrue(container.removeItem(last))
        Assert.assertFalse(container.isLastId(last))

    def isLastId_freeformAddedLastItemRemoved_returnsFalse(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        last = container.addItem()
        Assert.assertSame(last, container.lastItemId())
        Assert.assertTrue(container.removeItem(last))
        Assert.assertFalse(container.isLastId(last))

    def indexOfId_freeformItemRemoved_returnsNegOne(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id = container.getIdByIndex(2)
        Assert.assertTrue(container.removeItem(id))
        Assert.assertEquals(-1, container.indexOfId(id))

    def indexOfId_freeformAddedItemRemoved_returnsNegOne(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id = container.addItem()
        Assert.assertTrue(container.indexOfId(id) != -1)
        Assert.assertTrue(container.removeItem(id))
        Assert.assertEquals(-1, container.indexOfId(id))

    def getIdByIndex_freeformItemRemoved_resultChanges(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id = container.getIdByIndex(2)
        Assert.assertTrue(container.removeItem(id))
        Assert.assertNotSame(id, container.getIdByIndex(2))

    def getIdByIndex_freeformAddedItemRemoved_resultChanges(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        id = container.addItem()
        container.addItem()
        index = container.indexOfId(id)
        Assert.assertTrue(container.removeItem(id))
        Assert.assertNotSame(id, container.getIdByIndex(index))

    def removeAllItems_freeform_shouldSucceed(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        Assert.assertTrue(container.removeAllItems())
        Assert.assertEquals(0, len(container))

    def removeAllItems_freeformAddedItems_shouldSucceed(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        container.addItem()
        container.addItem()
        Assert.assertTrue(container.removeAllItems())
        Assert.assertEquals(0, len(container))

    def commit_freeformAddedItem_shouldBeWrittenToDB(self):
        delegate = EasyMock.createMock(FreeformQueryDelegate)


        class _2_(IAnswer):

            def answer(self):
                conn = EasyMock.getCurrentArguments()[0]
                item = EasyMock.getCurrentArguments()[1]
                statement = conn.createStatement()
                if AllTests.db == DB.MSSQL:
                    statement.executeUpdate('insert into people values(\'' + item.getItemProperty('NAME').getValue() + '\', \'' + item.getItemProperty('AGE').getValue() + '\')')
                else:
                    statement.executeUpdate('insert into people values(default, \'' + item.getItemProperty('NAME').getValue() + '\', \'' + item.getItemProperty('AGE').getValue() + '\')')
                statement.close()
                conn.commit()
                SQLContainerTest_this._connectionPool.releaseConnection(conn)
                return 1


        _2_ = _2_()
        EasyMock.expect(delegate.storeRow(EasyMock.isA(Connection), EasyMock.isA(self.RowItem))).andAnswer(_2_)
        None.anyTimes()


        class _3_(IAnswer):

            def answer(self):
                args = EasyMock.getCurrentArguments()
                offset = args[0]
                limit = args[1]
                if AllTests.db == DB.MSSQL:
                    start = offset + 1
                    end = offset + limit + 1
                    q = 'SELECT * FROM (SELECT row_number() OVER' + ' ( ORDER BY \"ID\" ASC) AS rownum, * FROM people)' + ' AS a WHERE a.rownum BETWEEN ' + start + ' AND ' + end
                    return q
                elif AllTests.db == DB.ORACLE:
                    start = offset + 1
                    end = offset + limit + 1
                    q = 'SELECT * FROM (SELECT x.*, ROWNUM AS r FROM' + ' (SELECT * FROM people ORDER BY \"ID\" ASC) x) ' + ' WHERE r BETWEEN ' + start + ' AND ' + end
                    return q
                else:
                    return 'SELECT * FROM people LIMIT ' + limit + ' OFFSET ' + offset


        _3_ = _3_()
        EasyMock.expect(delegate.getQueryString(EasyMock.anyInt(), EasyMock.anyInt())).andAnswer(_3_)
        None.anyTimes()
        delegate.setFilters(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setFilters(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        EasyMock.expect(delegate.getCountQuery()).andThrow(self.NotImplementedError()).anyTimes()
        query = FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID')
        query.setDelegate(delegate)
        EasyMock.replay(delegate)
        container = self.SQLContainer(query)
        id = container.addItem()
        container.getContainerProperty(id, 'NAME').setValue('New Name')
        container.getContainerProperty(id, 'AGE').setValue(30)
        Assert.assertTrue(isinstance(id, self.TemporaryRowId))
        Assert.assertSame(id, container.lastItemId())
        container.commit()
        Assert.assertFalse(isinstance(container.lastItemId(), self.TemporaryRowId))
        Assert.assertEquals('New Name', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        EasyMock.verify(delegate)

    def commit_freeformTwoAddedItems_shouldBeWrittenToDB(self):
        delegate = EasyMock.createMock(FreeformQueryDelegate)


        class _4_(IAnswer):

            def answer(self):
                conn = EasyMock.getCurrentArguments()[0]
                item = EasyMock.getCurrentArguments()[1]
                statement = conn.createStatement()
                if AllTests.db == DB.MSSQL:
                    statement.executeUpdate('insert into people values(\'' + item.getItemProperty('NAME').getValue() + '\', \'' + item.getItemProperty('AGE').getValue() + '\')')
                else:
                    statement.executeUpdate('insert into people values(default, \'' + item.getItemProperty('NAME').getValue() + '\', \'' + item.getItemProperty('AGE').getValue() + '\')')
                statement.close()
                conn.commit()
                SQLContainerTest_this._connectionPool.releaseConnection(conn)
                return 1


        _4_ = _4_()
        EasyMock.expect(delegate.storeRow(EasyMock.isA(Connection), EasyMock.isA(self.RowItem))).andAnswer(_4_)
        None.anyTimes()


        class _5_(IAnswer):

            def answer(self):
                args = EasyMock.getCurrentArguments()
                offset = args[0]
                limit = args[1]
                if AllTests.db == DB.MSSQL:
                    start = offset + 1
                    end = offset + limit + 1
                    q = 'SELECT * FROM (SELECT row_number() OVER' + ' ( ORDER BY \"ID\" ASC) AS rownum, * FROM people)' + ' AS a WHERE a.rownum BETWEEN ' + start + ' AND ' + end
                    return q
                elif AllTests.db == DB.ORACLE:
                    start = offset + 1
                    end = offset + limit + 1
                    q = 'SELECT * FROM (SELECT x.*, ROWNUM AS r FROM' + ' (SELECT * FROM people ORDER BY \"ID\" ASC) x) ' + ' WHERE r BETWEEN ' + start + ' AND ' + end
                    return q
                else:
                    return 'SELECT * FROM people LIMIT ' + limit + ' OFFSET ' + offset


        _5_ = _5_()
        EasyMock.expect(delegate.getQueryString(EasyMock.anyInt(), EasyMock.anyInt())).andAnswer(_5_)
        None.anyTimes()
        delegate.setFilters(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setFilters(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        EasyMock.expect(delegate.getCountQuery()).andThrow(self.NotImplementedError()).anyTimes()
        query = FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID')
        query.setDelegate(delegate)
        EasyMock.replay(delegate)
        container = self.SQLContainer(query)
        id = container.addItem()
        id2 = container.addItem()
        container.getContainerProperty(id, 'NAME').setValue('Herbert')
        container.getContainerProperty(id, 'AGE').setValue(30)
        container.getContainerProperty(id2, 'NAME').setValue('Larry')
        container.getContainerProperty(id2, 'AGE').setValue(50)
        Assert.assertTrue(isinstance(id2, self.TemporaryRowId))
        Assert.assertSame(id2, container.lastItemId())
        container.commit()
        nextToLast = container.getIdByIndex(len(container) - 2)
        Assert.assertFalse(isinstance(nextToLast, self.TemporaryRowId))
        Assert.assertEquals('Herbert', container.getContainerProperty(nextToLast, 'NAME').getValue())
        Assert.assertFalse(isinstance(container.lastItemId(), self.TemporaryRowId))
        Assert.assertEquals('Larry', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        EasyMock.verify(delegate)

    def commit_freeformRemovedItem_shouldBeRemovedFromDB(self):
        delegate = EasyMock.createMock(FreeformQueryDelegate)


        class _6_(IAnswer):

            def answer(self):
                conn = EasyMock.getCurrentArguments()[0]
                item = EasyMock.getCurrentArguments()[1]
                statement = conn.createStatement()
                statement.executeUpdate('DELETE FROM people WHERE \"ID\"=' + item.getItemProperty('ID'))
                statement.close()
                return True


        _6_ = _6_()
        EasyMock.expect(delegate.removeRow(EasyMock.isA(Connection), EasyMock.isA(self.RowItem))).andAnswer(_6_)
        None.anyTimes()


        class _7_(IAnswer):

            def answer(self):
                args = EasyMock.getCurrentArguments()
                offset = args[0]
                limit = args[1]
                if AllTests.db == DB.MSSQL:
                    start = offset + 1
                    end = offset + limit + 1
                    q = 'SELECT * FROM (SELECT row_number() OVER' + ' ( ORDER BY \"ID\" ASC) AS rownum, * FROM people)' + ' AS a WHERE a.rownum BETWEEN ' + start + ' AND ' + end
                    return q
                elif AllTests.db == DB.ORACLE:
                    start = offset + 1
                    end = offset + limit + 1
                    q = 'SELECT * FROM (SELECT x.*, ROWNUM AS r FROM' + ' (SELECT * FROM people ORDER BY \"ID\" ASC) x) ' + ' WHERE r BETWEEN ' + start + ' AND ' + end
                    return q
                else:
                    return 'SELECT * FROM people LIMIT ' + limit + ' OFFSET ' + offset


        _7_ = _7_()
        EasyMock.expect(delegate.getQueryString(EasyMock.anyInt(), EasyMock.anyInt())).andAnswer(_7_)
        None.anyTimes()
        delegate.setFilters(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setFilters(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        EasyMock.expect(delegate.getCountQuery()).andThrow(self.NotImplementedError()).anyTimes()
        query = FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID')
        query.setDelegate(delegate)
        EasyMock.replay(delegate)
        container = self.SQLContainer(query)
        last = container.lastItemId()
        container.removeItem(last)
        container.commit()
        Assert.assertFalse(last == container.lastItemId())
        EasyMock.verify(delegate)

    def commit_freeformLastItemUpdated_shouldUpdateRowInDB(self):
        delegate = EasyMock.createMock(FreeformQueryDelegate)


        class _8_(IAnswer):

            def answer(self):
                conn = EasyMock.getCurrentArguments()[0]
                item = EasyMock.getCurrentArguments()[1]
                statement = conn.createStatement()
                statement.executeUpdate('UPDATE people SET \"NAME\"=\'' + item.getItemProperty('NAME').getValue() + '\' WHERE \"ID\"=' + item.getItemProperty('ID').getValue())
                statement.close()
                conn.commit()
                SQLContainerTest_this._connectionPool.releaseConnection(conn)
                return 1


        _8_ = _8_()
        EasyMock.expect(delegate.storeRow(EasyMock.isA(Connection), EasyMock.isA(self.RowItem))).andAnswer(_8_)
        None.anyTimes()


        class _9_(IAnswer):

            def answer(self):
                args = EasyMock.getCurrentArguments()
                offset = args[0]
                limit = args[1]
                if AllTests.db == DB.MSSQL:
                    start = offset + 1
                    end = offset + limit + 1
                    q = 'SELECT * FROM (SELECT row_number() OVER' + ' ( ORDER BY \"ID\" ASC) AS rownum, * FROM people)' + ' AS a WHERE a.rownum BETWEEN ' + start + ' AND ' + end
                    return q
                elif AllTests.db == DB.ORACLE:
                    start = offset + 1
                    end = offset + limit + 1
                    q = 'SELECT * FROM (SELECT x.*, ROWNUM AS r FROM' + ' (SELECT * FROM people ORDER BY \"ID\" ASC) x) ' + ' WHERE r BETWEEN ' + start + ' AND ' + end
                    return q
                else:
                    return 'SELECT * FROM people LIMIT ' + limit + ' OFFSET ' + offset


        _9_ = _9_()
        EasyMock.expect(delegate.getQueryString(EasyMock.anyInt(), EasyMock.anyInt())).andAnswer(_9_)
        None.anyTimes()
        delegate.setFilters(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setFilters(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        EasyMock.expect(delegate.getCountQuery()).andThrow(self.NotImplementedError()).anyTimes()
        query = FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID')
        query.setDelegate(delegate)
        EasyMock.replay(delegate)
        container = self.SQLContainer(query)
        last = container.lastItemId()
        container.getContainerProperty(last, 'NAME').setValue('Donald')
        container.commit()
        Assert.assertEquals('Donald', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        EasyMock.verify(delegate)

    def rollback_freeformItemAdded_discardsAddedItem(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        size = len(container)
        id = container.addItem()
        container.getContainerProperty(id, 'NAME').setValue('foo')
        Assert.assertEquals(size + 1, len(container))
        container.rollback()
        Assert.assertEquals(size, len(container))
        Assert.assertFalse('foo' == container.getContainerProperty(container.lastItemId(), 'NAME').getValue())

    def rollback_freeformItemRemoved_restoresRemovedItem(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        size = len(container)
        last = container.lastItemId()
        container.removeItem(last)
        Assert.assertEquals(size - 1, len(container))
        container.rollback()
        Assert.assertEquals(size, len(container))
        Assert.assertEquals(last, container.lastItemId())

    def rollback_freeformItemChanged_discardsChanges(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        last = container.lastItemId()
        container.getContainerProperty(last, 'NAME').setValue('foo')
        container.rollback()
        Assert.assertFalse('foo' == container.getContainerProperty(container.lastItemId(), 'NAME').getValue())

    def itemChangeNotification_freeform_isModifiedReturnsTrue(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        Assert.assertFalse(container.isModified())
        last = container.getItem(container.lastItemId())
        container.itemChangeNotification(last)
        Assert.assertTrue(container.isModified())

    def itemSetChangeListeners_freeform_shouldFire(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        listener = EasyMock.createMock(ItemSetChangeListener)
        listener.containerItemSetChange(EasyMock.isA(ItemSetChangeEvent))
        EasyMock.replay(listener)
        container.addListener(listener)
        container.addItem()
        EasyMock.verify(listener)

    def itemSetChangeListeners_freeformItemRemoved_shouldFire(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        listener = EasyMock.createMock(ItemSetChangeListener)
        listener.containerItemSetChange(EasyMock.isA(ItemSetChangeEvent))
        EasyMock.expectLastCall().anyTimes()
        EasyMock.replay(listener)
        container.addListener(listener)
        container.removeItem(container.lastItemId())
        EasyMock.verify(listener)

    def removeListener_freeform_shouldNotFire(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        listener = EasyMock.createMock(ItemSetChangeListener)
        EasyMock.replay(listener)
        container.addListener(listener)
        container.removeListener(listener)
        container.addItem()
        EasyMock.verify(listener)

    def isModified_freeformRemovedItem_returnsTrue(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        Assert.assertFalse(container.isModified())
        container.removeItem(container.lastItemId())
        Assert.assertTrue(container.isModified())

    def isModified_freeformAddedItem_returnsTrue(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        Assert.assertFalse(container.isModified())
        container.addItem()
        Assert.assertTrue(container.isModified())

    def isModified_freeformChangedItem_returnsTrue(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        Assert.assertFalse(container.isModified())
        container.getContainerProperty(container.lastItemId(), 'NAME').setValue('foo')
        Assert.assertTrue(container.isModified())

    def getSortableContainerPropertyIds_freeform_returnsAllPropertyIds(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        sortableIds = container.getSortableContainerPropertyIds()
        Assert.assertTrue(sortableIds.contains('ID'))
        Assert.assertTrue(sortableIds.contains('NAME'))
        Assert.assertTrue(sortableIds.contains('AGE'))
        Assert.assertEquals(3, len(sortableIds))

    def addOrderBy_freeform_shouldReorderResults(self):
        query = FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID')
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        orderBys = list()
        delegate.setFilters(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setFilters(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(EasyMock.isA(list))


        class _10_(IAnswer):

            def answer(self):
                orders = EasyMock.getCurrentArguments()[0]
                self.orderBys.clear()
                self.orderBys.addAll(orders)
                return None


        _10_ = _10_()
        EasyMock.expectLastCall().andAnswer(_10_)
        None.anyTimes()


        class _11_(IAnswer):

            def answer(self):
                args = EasyMock.getCurrentArguments()
                offset = args[0]
                limit = args[1]
                if AllTests.db == DB.MSSQL:
                    gen = MSSQLGenerator()
                    if (self.orderBys is None) or self.orderBys.isEmpty():
                        ob = list()
                        ob.add(OrderBy('ID', True))
                        return gen.generateSelectQuery('people', None, ob, offset, limit, None).getQueryString()
                    else:
                        return gen.generateSelectQuery('people', None, self.orderBys, offset, limit, None).getQueryString()
                elif AllTests.db == DB.ORACLE:
                    gen = OracleGenerator()
                    if (self.orderBys is None) or self.orderBys.isEmpty():
                        ob = list()
                        ob.add(OrderBy('ID', True))
                        return gen.generateSelectQuery('people', None, ob, offset, limit, None).getQueryString()
                    else:
                        return gen.generateSelectQuery('people', None, self.orderBys, offset, limit, None).getQueryString()
                else:
                    query = str('SELECT * FROM people')
                    if not self.orderBys.isEmpty():
                        query.__add__(' ORDER BY ')
                        for orderBy in self.orderBys:
                            query.__add__('\"' + orderBy.getColumn() + '\"')
                            if orderBy.isAscending():
                                query.__add__(' ASC')
                            else:
                                query.__add__(' DESC')
                    query.__add__(' LIMIT ').append(limit).append(' OFFSET ').append(offset)
                    return str(query)


        _11_ = _11_()
        EasyMock.expect(delegate.getQueryString(EasyMock.anyInt(), EasyMock.anyInt())).andAnswer(_11_)
        None.anyTimes()
        EasyMock.expect(delegate.getCountQuery()).andThrow(self.NotImplementedError()).anyTimes()
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        container = self.SQLContainer(query)
        # Ville, Kalle, Pelle, Börje
        Assert.assertEquals('Ville', container.getContainerProperty(container.firstItemId(), 'NAME').getValue())
        Assert.assertEquals('Börje', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        container.addOrderBy(OrderBy('NAME', True))
        # Börje, Kalle, Pelle, Ville
        Assert.assertEquals('Börje', container.getContainerProperty(container.firstItemId(), 'NAME').getValue())
        Assert.assertEquals('Ville', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        EasyMock.verify(delegate)

    def addOrderBy_freeformIllegalColumn_shouldFail(self):
        container = self.SQLContainer(FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID'))
        container.addOrderBy(OrderBy('asdf', True))

    def sort_freeform_sortsByName(self):
        query = FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID')
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        orderBys = list()
        delegate.setFilters(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setFilters(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(EasyMock.isA(list))


        class _12_(IAnswer):

            def answer(self):
                orders = EasyMock.getCurrentArguments()[0]
                self.orderBys.clear()
                self.orderBys.addAll(orders)
                return None


        _12_ = _12_()
        EasyMock.expectLastCall().andAnswer(_12_)
        None.anyTimes()


        class _13_(IAnswer):

            def answer(self):
                args = EasyMock.getCurrentArguments()
                offset = args[0]
                limit = args[1]
                if AllTests.db == DB.MSSQL:
                    gen = MSSQLGenerator()
                    if (self.orderBys is None) or self.orderBys.isEmpty():
                        ob = list()
                        ob.add(OrderBy('ID', True))
                        return gen.generateSelectQuery('people', None, ob, offset, limit, None).getQueryString()
                    else:
                        return gen.generateSelectQuery('people', None, self.orderBys, offset, limit, None).getQueryString()
                elif AllTests.db == DB.ORACLE:
                    gen = OracleGenerator()
                    if (self.orderBys is None) or self.orderBys.isEmpty():
                        ob = list()
                        ob.add(OrderBy('ID', True))
                        return gen.generateSelectQuery('people', None, ob, offset, limit, None).getQueryString()
                    else:
                        return gen.generateSelectQuery('people', None, self.orderBys, offset, limit, None).getQueryString()
                else:
                    query = str('SELECT * FROM people')
                    if not self.orderBys.isEmpty():
                        query.__add__(' ORDER BY ')
                        for orderBy in self.orderBys:
                            query.__add__('\"' + orderBy.getColumn() + '\"')
                            if orderBy.isAscending():
                                query.__add__(' ASC')
                            else:
                                query.__add__(' DESC')
                    query.__add__(' LIMIT ').append(limit).append(' OFFSET ').append(offset)
                    return str(query)


        _13_ = _13_()
        EasyMock.expect(delegate.getQueryString(EasyMock.anyInt(), EasyMock.anyInt())).andAnswer(_13_)
        None.anyTimes()
        EasyMock.expect(delegate.getCountQuery()).andThrow(self.NotImplementedError()).anyTimes()
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        container = self.SQLContainer(query)
        # Ville, Kalle, Pelle, Börje
        Assert.assertEquals('Ville', container.getContainerProperty(container.firstItemId(), 'NAME').getValue())
        Assert.assertEquals('Börje', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        container.sort(['NAME'], [True])
        # Börje, Kalle, Pelle, Ville
        Assert.assertEquals('Börje', container.getContainerProperty(container.firstItemId(), 'NAME').getValue())
        Assert.assertEquals('Ville', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        EasyMock.verify(delegate)

    def addFilter_freeform_filtersResults(self):
        query = FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID')
        delegate = EasyMock.createMock(FreeformStatementDelegate)
        filters = list()
        delegate.setFilters(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setFilters(EasyMock.isA(list))


        class _14_(IAnswer):

            def answer(self):
                orders = EasyMock.getCurrentArguments()[0]
                self.filters.clear()
                self.filters.addAll(orders)
                return None


        _14_ = _14_()
        EasyMock.expectLastCall().andAnswer(_14_)
        None.anyTimes()


        class _15_(IAnswer):

            def answer(self):
                args = EasyMock.getCurrentArguments()
                offset = args[0]
                limit = args[1]
                return FreeformQueryUtil.getQueryWithFilters(self.filters, offset, limit)


        _15_ = _15_()
        EasyMock.expect(delegate.getQueryStatement(EasyMock.anyInt(), EasyMock.anyInt())).andAnswer(_15_)
        None.anyTimes()


        class _16_(IAnswer):

            def answer(self):
                sh = StatementHelper()
                query = str('SELECT COUNT(*) FROM people')
                if not self.filters.isEmpty():
                    query.__add__(QueryBuilder.getWhereStringForFilters(self.filters, sh))
                sh.setQueryString(str(query))
                return sh


        _16_ = _16_()
        EasyMock.expect(delegate.getCountStatement()).andAnswer(_16_)
        None.anyTimes()
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        container = self.SQLContainer(query)
        # Ville, Kalle, Pelle, Börje
        Assert.assertEquals(4, len(container))
        Assert.assertEquals('Börje', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        container.addContainerFilter(Like('NAME', '%lle'))
        # Ville, Kalle, Pelle
        Assert.assertEquals(3, len(container))
        Assert.assertEquals('Pelle', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        EasyMock.verify(delegate)

    def addContainerFilter_filtersResults(self):
        query = FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID')
        delegate = EasyMock.createMock(FreeformStatementDelegate)
        filters = list()
        delegate.setFilters(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        delegate.setFilters(EasyMock.isA(list))


        class _17_(IAnswer):

            def answer(self):
                orders = EasyMock.getCurrentArguments()[0]
                self.filters.clear()
                self.filters.addAll(orders)
                return None


        _17_ = _17_()
        EasyMock.expectLastCall().andAnswer(_17_)
        None.anyTimes()


        class _18_(IAnswer):

            def answer(self):
                args = EasyMock.getCurrentArguments()
                offset = args[0]
                limit = args[1]
                return FreeformQueryUtil.getQueryWithFilters(self.filters, offset, limit)


        _18_ = _18_()
        EasyMock.expect(delegate.getQueryStatement(EasyMock.anyInt(), EasyMock.anyInt())).andAnswer(_18_)
        None.anyTimes()


        class _19_(IAnswer):

            def answer(self):
                sh = StatementHelper()
                query = str('SELECT COUNT(*) FROM people')
                if not self.filters.isEmpty():
                    query.__add__(QueryBuilder.getWhereStringForFilters(self.filters, sh))
                sh.setQueryString(str(query))
                return sh


        _19_ = _19_()
        EasyMock.expect(delegate.getCountStatement()).andAnswer(_19_)
        None.anyTimes()
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        container = self.SQLContainer(query)
        # Ville, Kalle, Pelle, Börje
        Assert.assertEquals(4, len(container))
        container.addContainerFilter('NAME', 'Vi', False, False)
        # Ville
        Assert.assertEquals(1, len(container))
        Assert.assertEquals('Ville', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        EasyMock.verify(delegate)

    def addContainerFilter_ignoreCase_filtersResults(self):
        query = FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID')
        delegate = EasyMock.createMock(FreeformStatementDelegate)
        filters = list()
        delegate.setFilters(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setFilters(EasyMock.isA(list))


        class _20_(IAnswer):

            def answer(self):
                orders = EasyMock.getCurrentArguments()[0]
                self.filters.clear()
                self.filters.addAll(orders)
                return None


        _20_ = _20_()
        EasyMock.expectLastCall().andAnswer(_20_)
        None.anyTimes()


        class _21_(IAnswer):

            def answer(self):
                args = EasyMock.getCurrentArguments()
                offset = args[0]
                limit = args[1]
                return FreeformQueryUtil.getQueryWithFilters(self.filters, offset, limit)


        _21_ = _21_()
        EasyMock.expect(delegate.getQueryStatement(EasyMock.anyInt(), EasyMock.anyInt())).andAnswer(_21_)
        None.anyTimes()


        class _22_(IAnswer):

            def answer(self):
                sh = StatementHelper()
                query = str('SELECT COUNT(*) FROM people')
                if not self.filters.isEmpty():
                    query.__add__(QueryBuilder.getWhereStringForFilters(self.filters, sh))
                sh.setQueryString(str(query))
                return sh


        _22_ = _22_()
        EasyMock.expect(delegate.getCountStatement()).andAnswer(_22_)
        None.anyTimes()
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        container = self.SQLContainer(query)
        # Ville, Kalle, Pelle, Börje
        Assert.assertEquals(4, len(container))
        # FIXME LIKE %asdf% doesn't match a string that begins with asdf
        container.addContainerFilter('NAME', 'vi', True, True)
        # Ville
        Assert.assertEquals(1, len(container))
        Assert.assertEquals('Ville', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        EasyMock.verify(delegate)

    def removeAllContainerFilters_freeform_noFiltering(self):
        query = FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID')
        delegate = EasyMock.createMock(FreeformStatementDelegate)
        filters = list()
        delegate.setFilters(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setFilters(EasyMock.isA(list))


        class _23_(IAnswer):

            def answer(self):
                orders = EasyMock.getCurrentArguments()[0]
                self.filters.clear()
                self.filters.addAll(orders)
                return None


        _23_ = _23_()
        EasyMock.expectLastCall().andAnswer(_23_)
        None.anyTimes()


        class _24_(IAnswer):

            def answer(self):
                args = EasyMock.getCurrentArguments()
                offset = args[0]
                limit = args[1]
                return FreeformQueryUtil.getQueryWithFilters(self.filters, offset, limit)


        _24_ = _24_()
        EasyMock.expect(delegate.getQueryStatement(EasyMock.anyInt(), EasyMock.anyInt())).andAnswer(_24_)
        None.anyTimes()


        class _25_(IAnswer):

            def answer(self):
                sh = StatementHelper()
                query = str('SELECT COUNT(*) FROM people')
                if not self.filters.isEmpty():
                    query.__add__(QueryBuilder.getWhereStringForFilters(self.filters, sh))
                sh.setQueryString(str(query))
                return sh


        _25_ = _25_()
        EasyMock.expect(delegate.getCountStatement()).andAnswer(_25_)
        None.anyTimes()
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        container = self.SQLContainer(query)
        # Ville, Kalle, Pelle, Börje
        Assert.assertEquals(4, len(container))
        container.addContainerFilter('NAME', 'Vi', False, False)
        # Ville
        Assert.assertEquals(1, len(container))
        Assert.assertEquals('Ville', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        container.removeAllContainerFilters()
        Assert.assertEquals(4, len(container))
        Assert.assertEquals('Börje', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        EasyMock.verify(delegate)

    def removeContainerFilters_freeform_noFiltering(self):
        query = FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID')
        delegate = EasyMock.createMock(FreeformStatementDelegate)
        filters = list()
        delegate.setFilters(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setFilters(EasyMock.isA(list))


        class _26_(IAnswer):

            def answer(self):
                orders = EasyMock.getCurrentArguments()[0]
                self.filters.clear()
                self.filters.addAll(orders)
                return None


        _26_ = _26_()
        EasyMock.expectLastCall().andAnswer(_26_)
        None.anyTimes()


        class _27_(IAnswer):

            def answer(self):
                args = EasyMock.getCurrentArguments()
                offset = args[0]
                limit = args[1]
                return FreeformQueryUtil.getQueryWithFilters(self.filters, offset, limit)


        _27_ = _27_()
        EasyMock.expect(delegate.getQueryStatement(EasyMock.anyInt(), EasyMock.anyInt())).andAnswer(_27_)
        None.anyTimes()


        class _28_(IAnswer):

            def answer(self):
                sh = StatementHelper()
                query = str('SELECT COUNT(*) FROM people')
                if not self.filters.isEmpty():
                    query.__add__(QueryBuilder.getWhereStringForFilters(self.filters, sh))
                sh.setQueryString(str(query))
                return sh


        _28_ = _28_()
        EasyMock.expect(delegate.getCountStatement()).andAnswer(_28_)
        None.anyTimes()
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        container = self.SQLContainer(query)
        # Ville, Kalle, Pelle, Börje
        Assert.assertEquals(4, len(container))
        container.addContainerFilter('NAME', 'Vi', False, True)
        # Ville
        Assert.assertEquals(1, len(container))
        Assert.assertEquals('Ville', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        container.removeContainerFilters('NAME')
        Assert.assertEquals(4, len(container))
        Assert.assertEquals('Börje', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        EasyMock.verify(delegate)

    def addFilter_freeformBufferedItems_alsoFiltersBufferedItems(self):
        query = FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID')
        delegate = EasyMock.createMock(FreeformStatementDelegate)
        filters = list()
        delegate.setFilters(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setFilters(EasyMock.isA(list))


        class _29_(IAnswer):

            def answer(self):
                orders = EasyMock.getCurrentArguments()[0]
                self.filters.clear()
                self.filters.addAll(orders)
                return None


        _29_ = _29_()
        EasyMock.expectLastCall().andAnswer(_29_)
        None.anyTimes()


        class _30_(IAnswer):

            def answer(self):
                args = EasyMock.getCurrentArguments()
                offset = args[0]
                limit = args[1]
                return FreeformQueryUtil.getQueryWithFilters(self.filters, offset, limit)


        _30_ = _30_()
        EasyMock.expect(delegate.getQueryStatement(EasyMock.anyInt(), EasyMock.anyInt())).andAnswer(_30_)
        None.anyTimes()


        class _31_(IAnswer):

            def answer(self):
                sh = StatementHelper()
                query = str('SELECT COUNT(*) FROM people')
                if not self.filters.isEmpty():
                    query.__add__(QueryBuilder.getWhereStringForFilters(self.filters, sh))
                sh.setQueryString(str(query))
                return sh


        _31_ = _31_()
        EasyMock.expect(delegate.getCountStatement()).andAnswer(_31_)
        None.anyTimes()
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        container = self.SQLContainer(query)
        # Ville, Kalle, Pelle, Börje
        Assert.assertEquals(4, len(container))
        Assert.assertEquals('Börje', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        id1 = container.addItem()
        container.getContainerProperty(id1, 'NAME').setValue('Palle')
        id2 = container.addItem()
        container.getContainerProperty(id2, 'NAME').setValue('Bengt')
        container.addContainerFilter(Like('NAME', '%lle'))
        # Ville, Kalle, Pelle, Palle
        Assert.assertEquals(4, len(container))
        Assert.assertEquals('Ville', container.getContainerProperty(container.getIdByIndex(0), 'NAME').getValue())
        Assert.assertEquals('Kalle', container.getContainerProperty(container.getIdByIndex(1), 'NAME').getValue())
        Assert.assertEquals('Pelle', container.getContainerProperty(container.getIdByIndex(2), 'NAME').getValue())
        Assert.assertEquals('Palle', container.getContainerProperty(container.getIdByIndex(3), 'NAME').getValue())
        Assert.assertNull(container.getIdByIndex(4))
        Assert.assertNull(container.nextItemId(container.getIdByIndex(3)))
        Assert.assertFalse(container.containsId(id2))
        Assert.assertFalse(container.getItemIds().contains(id2))
        Assert.assertNull(container.getItem(id2))
        Assert.assertEquals(-1, container.indexOfId(id2))
        Assert.assertNotSame(id2, container.lastItemId())
        Assert.assertSame(id1, container.lastItemId())
        EasyMock.verify(delegate)

    def sort_freeformBufferedItems_sortsBufferedItemsLastInOrderAdded(self):
        query = FreeformQuery('SELECT * FROM people', self._connectionPool, 'ID')
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        orderBys = list()
        delegate.setFilters(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setFilters(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(EasyMock.isA(list))


        class _32_(IAnswer):

            def answer(self):
                orders = EasyMock.getCurrentArguments()[0]
                self.orderBys.clear()
                self.orderBys.addAll(orders)
                return None


        _32_ = _32_()
        EasyMock.expectLastCall().andAnswer(_32_)
        None.anyTimes()


        class _33_(IAnswer):

            def answer(self):
                args = EasyMock.getCurrentArguments()
                offset = args[0]
                limit = args[1]
                if AllTests.db == DB.MSSQL:
                    gen = MSSQLGenerator()
                    if (self.orderBys is None) or self.orderBys.isEmpty():
                        ob = list()
                        ob.add(OrderBy('ID', True))
                        return gen.generateSelectQuery('people', None, ob, offset, limit, None).getQueryString()
                    else:
                        return gen.generateSelectQuery('people', None, self.orderBys, offset, limit, None).getQueryString()
                elif AllTests.db == DB.ORACLE:
                    gen = OracleGenerator()
                    if (self.orderBys is None) or self.orderBys.isEmpty():
                        ob = list()
                        ob.add(OrderBy('ID', True))
                        return gen.generateSelectQuery('people', None, ob, offset, limit, None).getQueryString()
                    else:
                        return gen.generateSelectQuery('people', None, self.orderBys, offset, limit, None).getQueryString()
                else:
                    query = str('SELECT * FROM people')
                    if not self.orderBys.isEmpty():
                        query.__add__(' ORDER BY ')
                        for orderBy in self.orderBys:
                            query.__add__('\"' + orderBy.getColumn() + '\"')
                            if orderBy.isAscending():
                                query.__add__(' ASC')
                            else:
                                query.__add__(' DESC')
                    query.__add__(' LIMIT ').append(limit).append(' OFFSET ').append(offset)
                    return str(query)


        _33_ = _33_()
        EasyMock.expect(delegate.getQueryString(EasyMock.anyInt(), EasyMock.anyInt())).andAnswer(_33_)
        None.anyTimes()
        EasyMock.expect(delegate.getCountQuery()).andThrow(self.NotImplementedError()).anyTimes()
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        container = self.SQLContainer(query)
        # Ville, Kalle, Pelle, Börje
        Assert.assertEquals('Ville', container.getContainerProperty(container.firstItemId(), 'NAME').getValue())
        Assert.assertEquals('Börje', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        id1 = container.addItem()
        container.getContainerProperty(id1, 'NAME').setValue('Wilbert')
        id2 = container.addItem()
        container.getContainerProperty(id2, 'NAME').setValue('Albert')
        container.sort(['NAME'], [True])
        # Börje, Kalle, Pelle, Ville, Wilbert, Albert
        Assert.assertEquals('Börje', container.getContainerProperty(container.firstItemId(), 'NAME').getValue())
        Assert.assertEquals('Wilbert', container.getContainerProperty(container.getIdByIndex(len(container) - 2), 'NAME').getValue())
        Assert.assertEquals('Albert', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        EasyMock.verify(delegate)
