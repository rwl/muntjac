# -*- coding: utf-8 -*-
from com.vaadin.data.util.sqlcontainer.DataGenerator import (DataGenerator,)
from com.vaadin.data.util.sqlcontainer.AllTests import (AllTests,)
# from com.vaadin.data.util.sqlcontainer.query.TableQuery import (TableQuery,)
# from org.easymock.EasyMock import (EasyMock,)
# from org.junit.After import (After,)
# from org.junit.Assert import (Assert,)
# from org.junit.Before import (Before,)
# from org.junit.Test import (Test,)
DB = AllTests.DB


class SQLContainerTableQueryTest(object):
    _offset = AllTests.offset
    _createGarbage = AllTests.createGarbage
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

    def constructor_withTableQuery_shouldSucceed(self):
        self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))

    def containsId_withTableQueryAndExistingId_returnsTrue(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        Assert.assertTrue(container.containsId(self.RowId([1 + self._offset])))

    def containsId_withTableQueryAndNonexistingId_returnsFalse(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        Assert.assertFalse(container.containsId(self.RowId([1337 + self._offset])))

    def getContainerProperty_tableExistingItemIdAndPropertyId_returnsProperty(self):
        t = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = self.SQLContainer(t)
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals('Ville', container.getContainerProperty(self.RowId([BigDecimal(0 + self._offset)]), 'NAME').getValue())
        else:
            Assert.assertEquals('Ville', container.getContainerProperty(self.RowId([0 + self._offset]), 'NAME').getValue())

    def getContainerProperty_tableExistingItemIdAndNonexistingPropertyId_returnsNull(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        Assert.assertNull(container.getContainerProperty(self.RowId([1 + self._offset]), 'asdf'))

    def getContainerProperty_tableNonexistingItemId_returnsNull(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        Assert.assertNull(container.getContainerProperty(self.RowId([1337 + self._offset]), 'NAME'))

    def getContainerPropertyIds_table_returnsIDAndNAME(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        propertyIds = container.getContainerPropertyIds()
        Assert.assertEquals(3, len(propertyIds))
        Assert.assertArrayEquals(['ID', 'NAME', 'AGE'], list(propertyIds))

    def getItem_tableExistingItemId_returnsItem(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        if AllTests.db == DB.ORACLE:
            item = container.getItem(self.RowId([BigDecimal(0 + self._offset)]))
        else:
            item = container.getItem(self.RowId([0 + self._offset]))
        Assert.assertNotNull(item)
        Assert.assertEquals('Ville', item.getItemProperty('NAME').getValue())

    def getItem_commitedModifiedAndRefreshed(self):
        OLD_VALUE = 'SomeValue'
        # $NON-NLS-1$
        NEW_VALUE = 'OtherValue'
        # $NON-NLS-1$
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        itemID = container.addItem()
        item = container.getItem(itemID)
        item.getItemProperty('NAME').setValue(OLD_VALUE)
        # $NON-NLS-1$
        container.commit()
        itemID = container.getIdByIndex(len(container) - 1)
        item = container.getItem(itemID)
        Assert.assertEquals(OLD_VALUE, item.getItemProperty('NAME').getValue())
        item.getItemProperty('NAME').setValue(NEW_VALUE)
        # $NON-NLS-1$
        # refresh the container which free's the caches
        # and the modified cache keeps untouched which is a really powerful
        # feature
        container.refresh()
        # access the item again will use the item from the modified cache.
        item = container.getItem(itemID)
        Assert.assertEquals(NEW_VALUE, item.getItemProperty('NAME').getValue())

    def getItem_table5000RowsWithParameter1337_returnsItemWithId1337(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = self.SQLContainer(query)
        if AllTests.db == DB.ORACLE:
            item = container.getItem(self.RowId([BigDecimal(1337 + self._offset)]))
            Assert.assertNotNull(item)
            Assert.assertEquals(BigDecimal(1337 + self._offset), item.getItemProperty('ID').getValue())
        else:
            item = container.getItem(self.RowId([1337 + self._offset]))
            Assert.assertNotNull(item)
            Assert.assertEquals(1337 + self._offset, item.getItemProperty('ID').getValue())
        Assert.assertEquals('Person 1337', item.getItemProperty('NAME').getValue())

    def getItemIds_table_returnsItemIdsWithKeys0through3(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
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

    def getType_tableNAMEPropertyId_returnsString(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        Assert.assertEquals(str, container.getType('NAME'))

    def getType_tableIDPropertyId_returnsInteger(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals(BigDecimal, container.getType('ID'))
        else:
            Assert.assertEquals(int, container.getType('ID'))

    def getType_tableNonexistingPropertyId_returnsNull(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        Assert.assertNull(container.getType('asdf'))

    def size_table_returnsFour(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        Assert.assertEquals(4, len(container))

    def size_tableOneAddedItem_returnsFive(self):
        conn = self._connectionPool.reserveConnection()
        statement = conn.createStatement()
        if AllTests.db == DB.MSSQL:
            statement.executeUpdate('insert into people values(\'Bengt\', 30)')
        else:
            statement.executeUpdate('insert into people values(default, \'Bengt\', 30)')
        statement.close()
        conn.commit()
        self._connectionPool.releaseConnection(conn)
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        Assert.assertEquals(5, len(container))

    def indexOfId_tableWithParameterThree_returnsThree(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals(3, container.indexOfId(self.RowId([BigDecimal(3 + self._offset)])))
        else:
            Assert.assertEquals(3, container.indexOfId(self.RowId([3 + self._offset])))

    def indexOfId_table5000RowsWithParameter1337_returns1337(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        q = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = self.SQLContainer(q)
        if AllTests.db == DB.ORACLE:
            container.getItem(self.RowId([BigDecimal(1337 + self._offset)]))
            Assert.assertEquals(1337, container.indexOfId(self.RowId([BigDecimal(1337 + self._offset)])))
        else:
            container.getItem(self.RowId([1337 + self._offset]))
            Assert.assertEquals(1337, container.indexOfId(self.RowId([1337 + self._offset])))

    def getIdByIndex_table5000rowsIndex1337_returnsRowId1337(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        itemId = container.getIdByIndex(1337)
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals(str(self.RowId([1337 + self._offset])), str(itemId))
        else:
            Assert.assertEquals(self.RowId([1337 + self._offset]), itemId)

    def getIdByIndex_tableWithPaging5000rowsIndex1337_returnsRowId1337(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = self.SQLContainer(query)
        itemId = container.getIdByIndex(1337)
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals(str(self.RowId([1337 + self._offset])), str(itemId))
        else:
            Assert.assertEquals(self.RowId([1337 + self._offset]), itemId)

    def nextItemId_tableCurrentItem1337_returnsItem1338(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        itemId = container.getIdByIndex(1337)
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals(str(self.RowId([1338 + self._offset])), str(container.nextItemId(itemId)))
        else:
            Assert.assertEquals(self.RowId([1338 + self._offset]), container.nextItemId(itemId))

    def prevItemId_tableCurrentItem1337_returns1336(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        itemId = container.getIdByIndex(1337)
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals(str(self.RowId([1336 + self._offset])), str(container.prevItemId(itemId)))
        else:
            Assert.assertEquals(self.RowId([1336 + self._offset]), container.prevItemId(itemId))

    def firstItemId_table_returnsItemId0(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals(str(self.RowId([0 + self._offset])), str(container.firstItemId()))
        else:
            Assert.assertEquals(self.RowId([0 + self._offset]), container.firstItemId())

    def lastItemId_table5000Rows_returnsItemId4999(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals(str(self.RowId([4999 + self._offset])), str(container.lastItemId()))
        else:
            Assert.assertEquals(self.RowId([4999 + self._offset]), container.lastItemId())

    def isFirstId_tableActualFirstId_returnsTrue(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        if AllTests.db == DB.ORACLE:
            Assert.assertTrue(container.isFirstId(self.RowId([BigDecimal(0 + self._offset)])))
        else:
            Assert.assertTrue(container.isFirstId(self.RowId([0 + self._offset])))

    def isFirstId_tableSecondId_returnsFalse(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        if AllTests.db == DB.ORACLE:
            Assert.assertFalse(container.isFirstId(self.RowId([BigDecimal(1 + self._offset)])))
        else:
            Assert.assertFalse(container.isFirstId(self.RowId([1 + self._offset])))

    def isLastId_tableSecondId_returnsFalse(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        if AllTests.db == DB.ORACLE:
            Assert.assertFalse(container.isLastId(self.RowId([BigDecimal(1 + self._offset)])))
        else:
            Assert.assertFalse(container.isLastId(self.RowId([1 + self._offset])))

    def isLastId_tableLastId_returnsTrue(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        if AllTests.db == DB.ORACLE:
            Assert.assertTrue(container.isLastId(self.RowId([BigDecimal(3 + self._offset)])))
        else:
            Assert.assertTrue(container.isLastId(self.RowId([3 + self._offset])))

    def isLastId_table5000RowsLastId_returnsTrue(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        if AllTests.db == DB.ORACLE:
            Assert.assertTrue(container.isLastId(self.RowId([BigDecimal(4999 + self._offset)])))
        else:
            Assert.assertTrue(container.isLastId(self.RowId([4999 + self._offset])))

    def allIdsFound_table5000RowsLastId_shouldSucceed(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 5000):
                break
            Assert.assertTrue(container.containsId(container.getIdByIndex(i)))

    def allIdsFound_table5000RowsLastId_autoCommit_shouldSucceed(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        container.setAutoCommit(True)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 5000):
                break
            Assert.assertTrue(container.containsId(container.getIdByIndex(i)))

    def refresh_table_sizeShouldUpdate(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        Assert.assertEquals(4, len(container))
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        container.refresh()
        Assert.assertEquals(5000, len(container))

    def refresh_tableWithoutCallingRefresh_sizeShouldNotUpdate(self):
        # Yeah, this is a weird one. We're testing that the size doesn't update
        # after adding lots of items unless we call refresh inbetween. This to
        # make sure that the refresh method actually refreshes stuff and isn't
        # a NOP.
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        Assert.assertEquals(4, len(container))
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        Assert.assertEquals(4, len(container))

    def setAutoCommit_table_shouldSucceed(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        container.setAutoCommit(True)
        Assert.assertTrue(container.isAutoCommit())
        container.setAutoCommit(False)
        Assert.assertFalse(container.isAutoCommit())

    def getPageLength_table_returnsDefault100(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        Assert.assertEquals(100, container.getPageLength())

    def setPageLength_table_shouldSucceed(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        container.setPageLength(20)
        Assert.assertEquals(20, container.getPageLength())
        container.setPageLength(200)
        Assert.assertEquals(200, container.getPageLength())

    def addContainerProperty_normal_isUnsupported(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        container.addContainerProperty('asdf', str, '')

    def removeContainerProperty_normal_isUnsupported(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        container.removeContainerProperty('asdf')

    def addItemObject_normal_isUnsupported(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        container.addItem('asdf')

    def addItemAfterObjectObject_normal_isUnsupported(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        container.addItemAfter('asdf', 'foo')

    def addItemAtIntObject_normal_isUnsupported(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        container.addItemAt(2, 'asdf')

    def addItemAtInt_normal_isUnsupported(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        container.addItemAt(2)

    def addItemAfterObject_normal_isUnsupported(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        container.addItemAfter('asdf')

    def addItem_tableAddOneNewItem_returnsItemId(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        itemId = container.addItem()
        Assert.assertNotNull(itemId)

    def addItem_tableAddOneNewItem_autoCommit_returnsFinalItemId(self):
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = self.SQLContainer(query)
        container.setAutoCommit(True)
        itemId = container.addItem()
        Assert.assertNotNull(itemId)
        Assert.assertTrue(isinstance(itemId, self.RowId))
        Assert.assertFalse(isinstance(itemId, self.TemporaryRowId))

    def addItem_tableAddOneNewItem_autoCommit_sizeIsIncreased(self):
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = self.SQLContainer(query)
        container.setAutoCommit(True)
        originalSize = len(container)
        container.addItem()
        Assert.assertEquals(originalSize + 1, len(container))

    def addItem_tableAddOneNewItem_shouldChangeSize(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        size = len(container)
        container.addItem()
        Assert.assertEquals(size + 1, len(container))

    def addItem_tableAddTwoNewItems_shouldChangeSize(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        size = len(container)
        id1 = container.addItem()
        id2 = container.addItem()
        Assert.assertEquals(size + 2, len(container))
        Assert.assertNotSame(id1, id2)
        Assert.assertFalse(id1 == id2)

    def nextItemId_tableNewlyAddedItem_returnsNewlyAdded(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        lastId = container.lastItemId()
        id = container.addItem()
        Assert.assertEquals(id, container.nextItemId(lastId))

    def lastItemId_tableNewlyAddedItem_returnsNewlyAdded(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        lastId = container.lastItemId()
        id = container.addItem()
        Assert.assertEquals(id, container.lastItemId())
        Assert.assertNotSame(lastId, container.lastItemId())

    def indexOfId_tableNewlyAddedItem_returnsFour(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id = container.addItem()
        Assert.assertEquals(4, container.indexOfId(id))

    def getItem_tableNewlyAddedItem_returnsNewlyAdded(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id = container.addItem()
        Assert.assertNotNull(container.getItem(id))

    def getItemIds_tableNewlyAddedItem_containsNewlyAdded(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id = container.addItem()
        Assert.assertTrue(container.getItemIds().contains(id))

    def getContainerProperty_tableNewlyAddedItem_returnsPropertyOfNewlyAddedItem(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id = container.addItem()
        item = container.getItem(id)
        item.getItemProperty('NAME').setValue('asdf')
        Assert.assertEquals('asdf', container.getContainerProperty(id, 'NAME').getValue())

    def containsId_tableNewlyAddedItem_returnsTrue(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id = container.addItem()
        Assert.assertTrue(container.containsId(id))

    def prevItemId_tableTwoNewlyAddedItems_returnsFirstAddedItem(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id1 = container.addItem()
        id2 = container.addItem()
        Assert.assertEquals(id1, container.prevItemId(id2))

    def firstItemId_tableEmptyResultSet_returnsFirstAddedItem(self):
        DataGenerator.createGarbage(self._connectionPool)
        container = self.SQLContainer(TableQuery('garbage', self._connectionPool, AllTests.sqlGen))
        id = container.addItem()
        Assert.assertSame(id, container.firstItemId())

    def isFirstId_tableEmptyResultSet_returnsFirstAddedItem(self):
        DataGenerator.createGarbage(self._connectionPool)
        container = self.SQLContainer(TableQuery('garbage', self._connectionPool, AllTests.sqlGen))
        id = container.addItem()
        Assert.assertTrue(container.isFirstId(id))

    def isLastId_tableOneItemAdded_returnsTrueForAddedItem(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id = container.addItem()
        Assert.assertTrue(container.isLastId(id))

    def isLastId_tableTwoItemsAdded_returnsTrueForLastAddedItem(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        container.addItem()
        id2 = container.addItem()
        Assert.assertTrue(container.isLastId(id2))

    def getIdByIndex_tableOneItemAddedLastIndexInContainer_returnsAddedItem(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id = container.addItem()
        Assert.assertEquals(id, container.getIdByIndex(len(container) - 1))

    def removeItem_tableNoAddedItems_removesItemFromContainer(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        size = len(container)
        id = container.firstItemId()
        Assert.assertTrue(container.removeItem(id))
        Assert.assertNotSame(id, container.firstItemId())
        Assert.assertEquals(size - 1, len(container))

    def containsId_tableRemovedItem_returnsFalse(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id = container.firstItemId()
        Assert.assertTrue(container.removeItem(id))
        Assert.assertFalse(container.containsId(id))

    def removeItem_tableOneAddedItem_removesTheAddedItem(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id = container.addItem()
        size = len(container)
        Assert.assertTrue(container.removeItem(id))
        Assert.assertFalse(container.containsId(id))
        Assert.assertEquals(size - 1, len(container))

    def getItem_tableItemRemoved_returnsNull(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id = container.firstItemId()
        Assert.assertTrue(container.removeItem(id))
        Assert.assertNull(container.getItem(id))

    def getItem_tableAddedItemRemoved_returnsNull(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id = container.addItem()
        Assert.assertNotNull(container.getItem(id))
        Assert.assertTrue(container.removeItem(id))
        Assert.assertNull(container.getItem(id))

    def getItemIds_tableItemRemoved_shouldNotContainRemovedItem(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id = container.firstItemId()
        Assert.assertTrue(container.getItemIds().contains(id))
        Assert.assertTrue(container.removeItem(id))
        Assert.assertFalse(container.getItemIds().contains(id))

    def getItemIds_tableAddedItemRemoved_shouldNotContainRemovedItem(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id = container.addItem()
        Assert.assertTrue(container.getItemIds().contains(id))
        Assert.assertTrue(container.removeItem(id))
        Assert.assertFalse(container.getItemIds().contains(id))

    def containsId_tableItemRemoved_returnsFalse(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id = container.firstItemId()
        Assert.assertTrue(container.containsId(id))
        Assert.assertTrue(container.removeItem(id))
        Assert.assertFalse(container.containsId(id))

    def containsId_tableAddedItemRemoved_returnsFalse(self):
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = self.SQLContainer(query)
        id = container.addItem()
        Assert.assertTrue(container.containsId(id))
        Assert.assertTrue(container.removeItem(id))
        Assert.assertFalse(container.containsId(id))

    def nextItemId_tableItemRemoved_skipsRemovedItem(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        first = container.getIdByIndex(0)
        second = container.getIdByIndex(1)
        third = container.getIdByIndex(2)
        Assert.assertTrue(container.removeItem(second))
        Assert.assertEquals(third, container.nextItemId(first))

    def nextItemId_tableAddedItemRemoved_skipsRemovedItem(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        first = container.lastItemId()
        second = container.addItem()
        third = container.addItem()
        Assert.assertTrue(container.removeItem(second))
        Assert.assertEquals(third, container.nextItemId(first))

    def prevItemId_tableItemRemoved_skipsRemovedItem(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        first = container.getIdByIndex(0)
        second = container.getIdByIndex(1)
        third = container.getIdByIndex(2)
        Assert.assertTrue(container.removeItem(second))
        Assert.assertEquals(first, container.prevItemId(third))

    def prevItemId_tableAddedItemRemoved_skipsRemovedItem(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        first = container.lastItemId()
        second = container.addItem()
        third = container.addItem()
        Assert.assertTrue(container.removeItem(second))
        Assert.assertEquals(first, container.prevItemId(third))

    def firstItemId_tableFirstItemRemoved_resultChanges(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        first = container.firstItemId()
        Assert.assertTrue(container.removeItem(first))
        Assert.assertNotSame(first, container.firstItemId())

    def firstItemId_tableNewlyAddedFirstItemRemoved_resultChanges(self):
        DataGenerator.createGarbage(self._connectionPool)
        container = self.SQLContainer(TableQuery('garbage', self._connectionPool, AllTests.sqlGen))
        first = container.addItem()
        second = container.addItem()
        Assert.assertSame(first, container.firstItemId())
        Assert.assertTrue(container.removeItem(first))
        Assert.assertSame(second, container.firstItemId())

    def lastItemId_tableLastItemRemoved_resultChanges(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        last = container.lastItemId()
        Assert.assertTrue(container.removeItem(last))
        Assert.assertNotSame(last, container.lastItemId())

    def lastItemId_tableAddedLastItemRemoved_resultChanges(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        last = container.addItem()
        Assert.assertSame(last, container.lastItemId())
        Assert.assertTrue(container.removeItem(last))
        Assert.assertNotSame(last, container.lastItemId())

    def isFirstId_tableFirstItemRemoved_returnsFalse(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        first = container.firstItemId()
        Assert.assertTrue(container.removeItem(first))
        Assert.assertFalse(container.isFirstId(first))

    def isFirstId_tableAddedFirstItemRemoved_returnsFalse(self):
        DataGenerator.createGarbage(self._connectionPool)
        container = self.SQLContainer(TableQuery('garbage', self._connectionPool, AllTests.sqlGen))
        first = container.addItem()
        container.addItem()
        Assert.assertSame(first, container.firstItemId())
        Assert.assertTrue(container.removeItem(first))
        Assert.assertFalse(container.isFirstId(first))

    def isLastId_tableLastItemRemoved_returnsFalse(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        last = container.lastItemId()
        Assert.assertTrue(container.removeItem(last))
        Assert.assertFalse(container.isLastId(last))

    def isLastId_tableAddedLastItemRemoved_returnsFalse(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        last = container.addItem()
        Assert.assertSame(last, container.lastItemId())
        Assert.assertTrue(container.removeItem(last))
        Assert.assertFalse(container.isLastId(last))

    def indexOfId_tableItemRemoved_returnsNegOne(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id = container.getIdByIndex(2)
        Assert.assertTrue(container.removeItem(id))
        Assert.assertEquals(-1, container.indexOfId(id))

    def indexOfId_tableAddedItemRemoved_returnsNegOne(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id = container.addItem()
        Assert.assertTrue(container.indexOfId(id) != -1)
        Assert.assertTrue(container.removeItem(id))
        Assert.assertEquals(-1, container.indexOfId(id))

    def getIdByIndex_tableItemRemoved_resultChanges(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id = container.getIdByIndex(2)
        Assert.assertTrue(container.removeItem(id))
        Assert.assertNotSame(id, container.getIdByIndex(2))

    def getIdByIndex_tableAddedItemRemoved_resultChanges(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id = container.addItem()
        container.addItem()
        index = container.indexOfId(id)
        Assert.assertTrue(container.removeItem(id))
        Assert.assertNotSame(id, container.getIdByIndex(index))

    def removeAllItems_table_shouldSucceed(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        Assert.assertTrue(container.removeAllItems())
        Assert.assertEquals(0, len(container))

    def removeAllItems_tableAddedItems_shouldSucceed(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        container.addItem()
        container.addItem()
        Assert.assertTrue(container.removeAllItems())
        Assert.assertEquals(0, len(container))

    def commit_tableAddedItem_shouldBeWrittenToDB(self):
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = self.SQLContainer(query)
        id = container.addItem()
        container.getContainerProperty(id, 'NAME').setValue('New Name')
        Assert.assertTrue(isinstance(id, self.TemporaryRowId))
        Assert.assertSame(id, container.lastItemId())
        container.commit()
        Assert.assertFalse(isinstance(container.lastItemId(), self.TemporaryRowId))
        Assert.assertEquals('New Name', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())

    def commit_tableTwoAddedItems_shouldBeWrittenToDB(self):
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = self.SQLContainer(query)
        id = container.addItem()
        id2 = container.addItem()
        container.getContainerProperty(id, 'NAME').setValue('Herbert')
        container.getContainerProperty(id2, 'NAME').setValue('Larry')
        Assert.assertTrue(isinstance(id2, self.TemporaryRowId))
        Assert.assertSame(id2, container.lastItemId())
        container.commit()
        nextToLast = container.getIdByIndex(len(container) - 2)
        Assert.assertFalse(isinstance(nextToLast, self.TemporaryRowId))
        Assert.assertEquals('Herbert', container.getContainerProperty(nextToLast, 'NAME').getValue())
        Assert.assertFalse(isinstance(container.lastItemId(), self.TemporaryRowId))
        Assert.assertEquals('Larry', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())

    def commit_tableRemovedItem_shouldBeRemovedFromDB(self):
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = self.SQLContainer(query)
        last = container.lastItemId()
        container.removeItem(last)
        container.commit()
        Assert.assertFalse(last == container.lastItemId())

    def commit_tableLastItemUpdated_shouldUpdateRowInDB(self):
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = self.SQLContainer(query)
        last = container.lastItemId()
        container.getContainerProperty(last, 'NAME').setValue('Donald')
        container.commit()
        Assert.assertEquals('Donald', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())

    def rollback_tableItemAdded_discardsAddedItem(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        size = len(container)
        id = container.addItem()
        container.getContainerProperty(id, 'NAME').setValue('foo')
        Assert.assertEquals(size + 1, len(container))
        container.rollback()
        Assert.assertEquals(size, len(container))
        Assert.assertFalse('foo' == container.getContainerProperty(container.lastItemId(), 'NAME').getValue())

    def rollback_tableItemRemoved_restoresRemovedItem(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        size = len(container)
        last = container.lastItemId()
        container.removeItem(last)
        Assert.assertEquals(size - 1, len(container))
        container.rollback()
        Assert.assertEquals(size, len(container))
        Assert.assertEquals(last, container.lastItemId())

    def rollback_tableItemChanged_discardsChanges(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        last = container.lastItemId()
        container.getContainerProperty(last, 'NAME').setValue('foo')
        container.rollback()
        Assert.assertFalse('foo' == container.getContainerProperty(container.lastItemId(), 'NAME').getValue())

    def itemChangeNotification_table_isModifiedReturnsTrue(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        Assert.assertFalse(container.isModified())
        last = container.getItem(container.lastItemId())
        container.itemChangeNotification(last)
        Assert.assertTrue(container.isModified())

    def itemSetChangeListeners_table_shouldFire(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        listener = EasyMock.createMock(ItemSetChangeListener)
        listener.containerItemSetChange(EasyMock.isA(ItemSetChangeEvent))
        EasyMock.replay(listener)
        container.addListener(listener)
        container.addItem()
        EasyMock.verify(listener)

    def itemSetChangeListeners_tableItemRemoved_shouldFire(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        listener = EasyMock.createMock(ItemSetChangeListener)
        listener.containerItemSetChange(EasyMock.isA(ItemSetChangeEvent))
        EasyMock.expectLastCall().anyTimes()
        EasyMock.replay(listener)
        container.addListener(listener)
        container.removeItem(container.lastItemId())
        EasyMock.verify(listener)

    def removeListener_table_shouldNotFire(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        listener = EasyMock.createMock(ItemSetChangeListener)
        EasyMock.replay(listener)
        container.addListener(listener)
        container.removeListener(listener)
        container.addItem()
        EasyMock.verify(listener)

    def isModified_tableRemovedItem_returnsTrue(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        Assert.assertFalse(container.isModified())
        container.removeItem(container.lastItemId())
        Assert.assertTrue(container.isModified())

    def isModified_tableAddedItem_returnsTrue(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        Assert.assertFalse(container.isModified())
        container.addItem()
        Assert.assertTrue(container.isModified())

    def isModified_tableChangedItem_returnsTrue(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        Assert.assertFalse(container.isModified())
        container.getContainerProperty(container.lastItemId(), 'NAME').setValue('foo')
        Assert.assertTrue(container.isModified())

    def getSortableContainerPropertyIds_table_returnsAllPropertyIds(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        sortableIds = container.getSortableContainerPropertyIds()
        Assert.assertTrue(sortableIds.contains('ID'))
        Assert.assertTrue(sortableIds.contains('NAME'))
        Assert.assertTrue(sortableIds.contains('AGE'))
        Assert.assertEquals(3, len(sortableIds))
        if (AllTests.db == DB.MSSQL) or (AllTests.db == DB.ORACLE):
            Assert.assertFalse(sortableIds.contains('rownum'))

    def addOrderBy_table_shouldReorderResults(self):
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = self.SQLContainer(query)
        # Ville, Kalle, Pelle, Börje
        Assert.assertEquals('Ville', container.getContainerProperty(container.firstItemId(), 'NAME').getValue())
        Assert.assertEquals('Börje', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        container.addOrderBy(OrderBy('NAME', True))
        # Börje, Kalle, Pelle, Ville
        Assert.assertEquals('Börje', container.getContainerProperty(container.firstItemId(), 'NAME').getValue())
        Assert.assertEquals('Ville', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())

    def addOrderBy_tableIllegalColumn_shouldFail(self):
        container = self.SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        container.addOrderBy(OrderBy('asdf', True))

    def sort_table_sortsByName(self):
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = self.SQLContainer(query)
        # Ville, Kalle, Pelle, Börje
        Assert.assertEquals('Ville', container.getContainerProperty(container.firstItemId(), 'NAME').getValue())
        Assert.assertEquals('Börje', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        container.sort(['NAME'], [True])
        # Börje, Kalle, Pelle, Ville
        Assert.assertEquals('Börje', container.getContainerProperty(container.firstItemId(), 'NAME').getValue())
        Assert.assertEquals('Ville', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())

    def addFilter_table_filtersResults(self):
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = self.SQLContainer(query)
        # Ville, Kalle, Pelle, Börje
        Assert.assertEquals(4, len(container))
        Assert.assertEquals('Börje', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        container.addContainerFilter(Like('NAME', '%lle'))
        # Ville, Kalle, Pelle
        Assert.assertEquals(3, len(container))
        Assert.assertEquals('Pelle', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())

    def addContainerFilter_filtersResults(self):
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = self.SQLContainer(query)
        # Ville, Kalle, Pelle, Börje
        Assert.assertEquals(4, len(container))
        container.addContainerFilter('NAME', 'Vi', False, False)
        # Ville
        Assert.assertEquals(1, len(container))
        Assert.assertEquals('Ville', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())

    def addContainerFilter_ignoreCase_filtersResults(self):
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = self.SQLContainer(query)
        # Ville, Kalle, Pelle, Börje
        Assert.assertEquals(4, len(container))
        container.addContainerFilter('NAME', 'vi', True, False)
        # Ville
        Assert.assertEquals(1, len(container))
        Assert.assertEquals('Ville', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())

    def removeAllContainerFilters_table_noFiltering(self):
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
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

    def removeContainerFilters_table_noFiltering(self):
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = self.SQLContainer(query)
        # Ville, Kalle, Pelle, Börje
        Assert.assertEquals(4, len(container))
        container.addContainerFilter('NAME', 'Vi', False, False)
        # Ville
        Assert.assertEquals(1, len(container))
        Assert.assertEquals('Ville', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        container.removeContainerFilters('NAME')
        Assert.assertEquals(4, len(container))
        Assert.assertEquals('Börje', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())

    def addFilter_tableBufferedItems_alsoFiltersBufferedItems(self):
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
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

    def sort_tableBufferedItems_sortsBufferedItemsLastInOrderAdded(self):
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
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
