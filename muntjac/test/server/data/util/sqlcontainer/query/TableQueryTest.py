# -*- coding: utf-8 -*-
from com.vaadin.data.util.sqlcontainer.DataGenerator import (DataGenerator,)
from com.vaadin.data.util.sqlcontainer.AllTests import (AllTests,)
# from com.vaadin.data.util.sqlcontainer.OptimisticLockException import (OptimisticLockException,)
# from java.sql.PreparedStatement import (PreparedStatement,)
# from org.junit.After import (After,)
# from org.junit.Assert import (Assert,)
# from org.junit.Before import (Before,)
# from org.junit.Test import (Test,)
DB = AllTests.DB


class TableQueryTest(object):
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

    def construction_legalParameters_shouldSucceed(self):
        """TableQuery construction tests
             *********************************************************************
        """
        tQuery = TableQuery('people', self._connectionPool, DefaultSQLGenerator())
        Assert.assertArrayEquals(['ID'], list(tQuery.getPrimaryKeyColumns()))
        correctTableName = 'people'.equalsIgnoreCase(tQuery.getTableName())
        Assert.assertTrue(correctTableName)

    def construction_legalParameters_defaultGenerator_shouldSucceed(self):
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        Assert.assertArrayEquals(['ID'], list(tQuery.getPrimaryKeyColumns()))
        correctTableName = 'people'.equalsIgnoreCase(tQuery.getTableName())
        Assert.assertTrue(correctTableName)

    def construction_nonExistingTableName_shouldFail(self):
        TableQuery('skgwaguhsd', self._connectionPool, DefaultSQLGenerator())

    def construction_emptyTableName_shouldFail(self):
        TableQuery('', self._connectionPool, DefaultSQLGenerator())

    def construction_nullSqlGenerator_shouldFail(self):
        TableQuery('people', self._connectionPool, None)

    def construction_nullConnectionPool_shouldFail(self):
        TableQuery('people', None, DefaultSQLGenerator())

    def getCount_simpleQuery_returnsFour(self):
        """TableQuery row count tests
             *********************************************************************
        """
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        Assert.assertEquals(4, tQuery.getCount())

    def getCount_simpleQueryTwoMorePeopleAdded_returnsSix(self):
        # Add some people
        conn = self._connectionPool.reserveConnection()
        statement = conn.createStatement()
        if AllTests.db == DB.MSSQL:
            statement.executeUpdate('insert into people values(\'Bengt\', 30)')
            statement.executeUpdate('insert into people values(\'Ingvar\', 50)')
        else:
            statement.executeUpdate('insert into people values(default, \'Bengt\', 30)')
            statement.executeUpdate('insert into people values(default, \'Ingvar\', 50)')
        statement.close()
        conn.commit()
        self._connectionPool.releaseConnection(conn)
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        Assert.assertEquals(6, tQuery.getCount())

    def getCount_normalState_releasesConnection(self):
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        tQuery.getCount()
        tQuery.getCount()
        Assert.assertNotNull(self._connectionPool.reserveConnection())

    def getResults_simpleQuery_returnsFourRecords(self):
        """TableQuery get results tests
             *********************************************************************
        """
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        tQuery.beginTransaction()
        rs = tQuery.getResults(0, 0)
        Assert.assertTrue(rs.next())
        Assert.assertEquals(0 + self._offset, rs.getInt(1))
        Assert.assertEquals('Ville', rs.getString(2))
        Assert.assertTrue(rs.next())
        Assert.assertEquals(1 + self._offset, rs.getInt(1))
        Assert.assertEquals('Kalle', rs.getString(2))
        Assert.assertTrue(rs.next())
        Assert.assertEquals(2 + self._offset, rs.getInt(1))
        Assert.assertEquals('Pelle', rs.getString(2))
        Assert.assertTrue(rs.next())
        Assert.assertEquals(3 + self._offset, rs.getInt(1))
        Assert.assertEquals('Börje', rs.getString(2))
        Assert.assertFalse(rs.next())
        tQuery.commit()

    def getResults_noDelegate5000Rows_returns5000rows(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        tQuery.beginTransaction()
        rs = tQuery.getResults(0, 0)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 5000):
                break
            Assert.assertTrue(rs.next())
        Assert.assertFalse(rs.next())
        tQuery.commit()

    def beginTransaction_readOnly_shouldSucceed(self):
        """TableQuery transaction management tests
             *********************************************************************
        """
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        tQuery.beginTransaction()

    def beginTransaction_transactionAlreadyActive_shouldFail(self):
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        tQuery.beginTransaction()
        tQuery.beginTransaction()

    def commit_readOnly_shouldSucceed(self):
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        tQuery.beginTransaction()
        tQuery.commit()

    def rollback_readOnly_shouldSucceed(self):
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        tQuery.beginTransaction()
        tQuery.rollback()

    def commit_noActiveTransaction_shouldFail(self):
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        tQuery.commit()

    def rollback_noActiveTransaction_shouldFail(self):
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        tQuery.rollback()

    def containsRowWithKeys_existingKeys_returnsTrue(self):
        """TableQuery row query with given keys tests
             *********************************************************************
        """
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        Assert.assertTrue(tQuery.containsRowWithKey(1))

    def containsRowWithKeys_nonexistingKeys_returnsTrue(self):
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        Assert.assertFalse(tQuery.containsRowWithKey(1337))

    def containsRowWithKeys_invalidKeys_shouldFail(self):
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        b = True
        try:
            b = tQuery.containsRowWithKey('foo')
        except SQLException, se:
            return
        Assert.assertFalse(b)

    def containsRowWithKeys_nullKeys_shouldFailAndReleaseConnections(self):
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        # We should now be able to reserve two connections
        try:
            tQuery.containsRowWithKey([None])
        except SQLException, e:
            self._connectionPool.reserveConnection()
            self._connectionPool.reserveConnection()

    def setFilters_shouldReturnCorrectCount(self):
        """TableQuery filtering and ordering tests
             *********************************************************************
        """
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        filters = list()
        filters.add(Like('NAME', '%lle'))
        tQuery.setFilters(filters)
        Assert.assertEquals(3, tQuery.getCount())

    def setOrderByNameAscending_shouldReturnCorrectOrder(self):
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        orderBys = Arrays.asList(OrderBy('NAME', True))
        tQuery.setOrderBy(orderBys)
        tQuery.beginTransaction()
        rs = tQuery.getResults(0, 0)
        Assert.assertTrue(rs.next())
        Assert.assertEquals(3 + self._offset, rs.getInt(1))
        Assert.assertEquals('Börje', rs.getString(2))
        Assert.assertTrue(rs.next())
        Assert.assertEquals(1 + self._offset, rs.getInt(1))
        Assert.assertEquals('Kalle', rs.getString(2))
        Assert.assertTrue(rs.next())
        Assert.assertEquals(2 + self._offset, rs.getInt(1))
        Assert.assertEquals('Pelle', rs.getString(2))
        Assert.assertTrue(rs.next())
        Assert.assertEquals(0 + self._offset, rs.getInt(1))
        Assert.assertEquals('Ville', rs.getString(2))
        Assert.assertFalse(rs.next())
        tQuery.commit()

    def setOrderByNameDescending_shouldReturnCorrectOrder(self):
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        orderBys = Arrays.asList(OrderBy('NAME', False))
        tQuery.setOrderBy(orderBys)
        tQuery.beginTransaction()
        rs = tQuery.getResults(0, 0)
        Assert.assertTrue(rs.next())
        Assert.assertEquals(0 + self._offset, rs.getInt(1))
        Assert.assertEquals('Ville', rs.getString(2))
        Assert.assertTrue(rs.next())
        Assert.assertEquals(2 + self._offset, rs.getInt(1))
        Assert.assertEquals('Pelle', rs.getString(2))
        Assert.assertTrue(rs.next())
        Assert.assertEquals(1 + self._offset, rs.getInt(1))
        Assert.assertEquals('Kalle', rs.getString(2))
        Assert.assertTrue(rs.next())
        Assert.assertEquals(3 + self._offset, rs.getInt(1))
        Assert.assertEquals('Börje', rs.getString(2))
        Assert.assertFalse(rs.next())
        tQuery.commit()

    def setFilters_nullParameter_shouldSucceed(self):
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        tQuery.setFilters(None)

    def setOrderBy_nullParameter_shouldSucceed(self):
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        tQuery.setOrderBy(None)

    def removeRowThroughContainer_legalRowItem_shouldSucceed(self):
        """TableQuery row removal tests
             *********************************************************************
        """
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = SQLContainer(tQuery)
        container.setAutoCommit(False)
        Assert.assertTrue(container.removeItem(container.getItemIds().next()))
        Assert.assertEquals(4, tQuery.getCount())
        Assert.assertEquals(3, len(container))
        container.commit()
        Assert.assertEquals(3, tQuery.getCount())
        Assert.assertEquals(3, len(container))

    def removeRowThroughContainer_nonexistingRowId_shouldFail(self):
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = SQLContainer(tQuery)
        container.setAutoCommit(True)
        Assert.assertFalse(container.removeItem('foo'))

    def insertRowThroughContainer_shouldSucceed(self):
        """TableQuery row adding / modification tests
             *********************************************************************
        """
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        tQuery.setVersionColumn('ID')
        container = SQLContainer(tQuery)
        container.setAutoCommit(False)
        item = container.addItem()
        Assert.assertNotNull(item)
        Assert.assertEquals(4, tQuery.getCount())
        Assert.assertEquals(5, len(container))
        container.commit()
        Assert.assertEquals(5, tQuery.getCount())
        Assert.assertEquals(5, len(container))

    def modifyRowThroughContainer_shouldSucceed(self):
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        # In this test the primary key is used as a version column
        tQuery.setVersionColumn('ID')
        container = SQLContainer(tQuery)
        container.setAutoCommit(False)
        # Check that the container size is correct and there is no 'Viljami'
        Assert.assertEquals(4, len(container))
        filters = list()
        filters.add(Equal('NAME', 'Viljami'))
        tQuery.setFilters(filters)
        Assert.assertEquals(0, tQuery.getCount())
        tQuery.setFilters(None)
        # Fetch first item, modify and commit
        item = container.getItem(container.getItemIds().next())
        Assert.assertNotNull(item)
        ri = item
        Assert.assertNotNull(ri.getItemProperty('NAME'))
        ri.getItemProperty('NAME').setValue('Viljami')
        container.commit()
        # Check that the size is still correct and only 1 'Viljami' is found
        Assert.assertEquals(4, tQuery.getCount())
        Assert.assertEquals(4, len(container))
        tQuery.setFilters(filters)
        Assert.assertEquals(1, tQuery.getCount())

    def storeRow_noVersionColumn_shouldSucceed(self):
        tQuery = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = SQLContainer(tQuery)
        id = container.addItem()
        row = container.getItem(id)
        row.getItemProperty('NAME').setValue('R2D2')
        row.getItemProperty('AGE').setValue(123)
        tQuery.beginTransaction()
        tQuery.storeRow(row)
        tQuery.commit()
        conn = self._connectionPool.reserveConnection()
        stmt = conn.prepareStatement('SELECT * FROM PEOPLE WHERE \"NAME\" = ?')
        stmt.setString(1, 'R2D2')
        rs = stmt.executeQuery()
        Assert.assertTrue(rs.next())
        rs.close()
        stmt.close()
        self._connectionPool.releaseConnection(conn)

    def storeRow_versionSetAndEqualToDBValue_shouldSucceed(self):
        DataGenerator.addVersionedData(self._connectionPool)
        tQuery = TableQuery('versioned', self._connectionPool, AllTests.sqlGen)
        tQuery.setVersionColumn('VERSION')
        container = SQLContainer(tQuery)
        row = container.getItem(container.firstItemId())
        Assert.assertEquals('Junk', row.getItemProperty('TEXT').getValue())
        row.getItemProperty('TEXT').setValue('asdf')
        container.commit()
        conn = self._connectionPool.reserveConnection()
        stmt = conn.prepareStatement('SELECT * FROM VERSIONED WHERE \"TEXT\" = ?')
        stmt.setString(1, 'asdf')
        rs = stmt.executeQuery()
        Assert.assertTrue(rs.next())
        rs.close()
        stmt.close()
        conn.commit()
        self._connectionPool.releaseConnection(conn)

    def storeRow_versionSetAndLessThanDBValue_shouldThrowException(self):
        if AllTests.db == DB.HSQLDB:
            raise OptimisticLockException('HSQLDB doesn\'t support row versioning for optimistic locking - don\'t run this test.', None)
        DataGenerator.addVersionedData(self._connectionPool)
        tQuery = TableQuery('versioned', self._connectionPool, AllTests.sqlGen)
        tQuery.setVersionColumn('VERSION')
        container = SQLContainer(tQuery)
        row = container.getItem(container.firstItemId())
        Assert.assertEquals('Junk', row.getItemProperty('TEXT').getValue())
        row.getItemProperty('TEXT').setValue('asdf')
        # Update the version using another connection.
        conn = self._connectionPool.reserveConnection()
        stmt = conn.prepareStatement('UPDATE VERSIONED SET \"TEXT\" = ? WHERE \"ID\" = ?')
        stmt.setString(1, 'foo')
        stmt.setObject(2, row.getItemProperty('ID').getValue())
        stmt.executeUpdate()
        stmt.close()
        conn.commit()
        self._connectionPool.releaseConnection(conn)
        container.commit()

    def removeRow_versionSetAndEqualToDBValue_shouldSucceed(self):
        DataGenerator.addVersionedData(self._connectionPool)
        tQuery = TableQuery('versioned', self._connectionPool, AllTests.sqlGen)
        tQuery.setVersionColumn('VERSION')
        container = SQLContainer(tQuery)
        row = container.getItem(container.firstItemId())
        Assert.assertEquals('Junk', row.getItemProperty('TEXT').getValue())
        container.removeItem(container.firstItemId())
        container.commit()
        conn = self._connectionPool.reserveConnection()
        stmt = conn.prepareStatement('SELECT * FROM VERSIONED WHERE \"TEXT\" = ?')
        stmt.setString(1, 'Junk')
        rs = stmt.executeQuery()
        Assert.assertFalse(rs.next())
        rs.close()
        stmt.close()
        conn.commit()
        self._connectionPool.releaseConnection(conn)

    def removeRow_versionSetAndLessThanDBValue_shouldThrowException(self):
        if AllTests.db == AllTests.DB.HSQLDB:
            # HSQLDB doesn't support versioning, so this is to make the test
            # green.
            raise OptimisticLockException(None)
        DataGenerator.addVersionedData(self._connectionPool)
        tQuery = TableQuery('versioned', self._connectionPool, AllTests.sqlGen)
        tQuery.setVersionColumn('VERSION')
        container = SQLContainer(tQuery)
        row = container.getItem(container.firstItemId())
        Assert.assertEquals('Junk', row.getItemProperty('TEXT').getValue())
        # Update the version using another connection.
        conn = self._connectionPool.reserveConnection()
        stmt = conn.prepareStatement('UPDATE VERSIONED SET \"TEXT\" = ? WHERE \"ID\" = ?')
        stmt.setString(1, 'asdf')
        stmt.setObject(2, row.getItemProperty('ID').getValue())
        stmt.executeUpdate()
        stmt.close()
        conn.commit()
        self._connectionPool.releaseConnection(conn)
        container.removeItem(container.firstItemId())
        container.commit()

    def removeRow_throwsOptimisticLockException_shouldStillWork(self):
        if AllTests.db == AllTests.DB.HSQLDB:
            # HSQLDB doesn't support versioning, so this is to make the test
            # green.
            return
        DataGenerator.addVersionedData(self._connectionPool)
        tQuery = TableQuery('versioned', self._connectionPool, AllTests.sqlGen)
        tQuery.setVersionColumn('VERSION')
        container = SQLContainer(tQuery)
        row = container.getItem(container.firstItemId())
        Assert.assertEquals('Junk', row.getItemProperty('TEXT').getValue())
        # Update the version using another connection.
        conn = self._connectionPool.reserveConnection()
        stmt = conn.prepareStatement('UPDATE VERSIONED SET \"TEXT\" = ? WHERE \"ID\" = ?')
        stmt.setString(1, 'asdf')
        stmt.setObject(2, row.getItemProperty('ID').getValue())
        stmt.executeUpdate()
        stmt.close()
        conn.commit()
        self._connectionPool.releaseConnection(conn)
        itemToRemove = container.firstItemId()
        # This is expected, refresh and try again.
        try:
            container.removeItem(itemToRemove)
            container.commit()
        except OptimisticLockException, e:
            container.rollback()
            container.removeItem(itemToRemove)
            container.commit()
        id = container.addItem()
        item = container.getItem(id)
        item.getItemProperty('TEXT').setValue('foo')
        container.commit()
