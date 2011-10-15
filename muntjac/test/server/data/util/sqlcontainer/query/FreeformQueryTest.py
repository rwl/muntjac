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
from com.vaadin.data.util.sqlcontainer.AllTests import (AllTests,)
# from org.easymock.EasyMock import (EasyMock,)
# from org.junit.After import (After,)
# from org.junit.Assert import (Assert,)
# from org.junit.Before import (Before,)
# from org.junit.Test import (Test,)
DB = AllTests.DB


class FreeformQueryTest(object):
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
        ffQuery = FreeformQuery('SELECT * FROM foo', Arrays.asList('ID'), self._connectionPool)
        Assert.assertArrayEquals(['ID'], list(ffQuery.getPrimaryKeyColumns()))
        Assert.assertEquals('SELECT * FROM foo', ffQuery.getQueryString())

    def construction_emptyQueryString_shouldFail(self):
        FreeformQuery('', Arrays.asList('ID'), self._connectionPool)

    def construction_nullPrimaryKeys_shouldSucceed(self):
        FreeformQuery('SELECT * FROM foo', None, self._connectionPool)

    def construction_nullPrimaryKeys2_shouldSucceed(self):
        FreeformQuery('SELECT * FROM foo', self._connectionPool)

    def construction_emptyPrimaryKeys_shouldSucceed(self):
        FreeformQuery('SELECT * FROM foo', self._connectionPool)

    def construction_emptyStringsInPrimaryKeys_shouldFail(self):
        FreeformQuery('SELECT * FROM foo', Arrays.asList(''), self._connectionPool)

    def construction_nullConnectionPool_shouldFail(self):
        FreeformQuery('SELECT * FROM foo', Arrays.asList('ID'), None)

    def getCount_simpleQuery_returnsFour(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        Assert.assertEquals(4, query.getCount())

    def getCount_illegalQuery_shouldThrowSQLException(self):
        query = FreeformQuery('SELECT * FROM asdf', Arrays.asList('ID'), self._connectionPool)
        query.getResults(0, 50)

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
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        Assert.assertEquals(6, query.getCount())

    def getCount_moreComplexQuery_returnsThree(self):
        query = FreeformQuery('SELECT * FROM people WHERE \"NAME\" LIKE \'%lle\'', self._connectionPool, ['ID'])
        Assert.assertEquals(3, query.getCount())

    def getCount_normalState_releasesConnection(self):
        query = FreeformQuery('SELECT * FROM people WHERE \"NAME\" LIKE \'%lle\'', self._connectionPool, 'ID')
        query.getCount()
        query.getCount()
        Assert.assertNotNull(self._connectionPool.reserveConnection())

    def getCount_delegateRegistered_shouldUseDelegate(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        EasyMock.expect(delegate.getCountQuery()).andReturn('SELECT COUNT(*) FROM people WHERE \"NAME\" LIKE \'%lle\'')
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        Assert.assertEquals(3, query.getCount())
        EasyMock.verify(delegate)

    def getCount_delegateRegisteredZeroRows_returnsZero(self):
        DataGenerator.createGarbage(self._connectionPool)
        query = FreeformQuery('SELECT * FROM GARBAGE', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        EasyMock.expect(delegate.getCountQuery()).andReturn('SELECT COUNT(*) FROM GARBAGE')
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        Assert.assertEquals(0, query.getCount())
        EasyMock.verify(delegate)

    def getResults_simpleQuery_returnsFourRecords(self):
        query = FreeformQuery('SELECT \"ID\",\"NAME\" FROM people', Arrays.asList('ID'), self._connectionPool)
        query.beginTransaction()
        rs = query.getResults(0, 0)
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
        query.commit()

    def getResults_moreComplexQuery_returnsThreeRecords(self):
        query = FreeformQuery('SELECT * FROM people WHERE \"NAME\" LIKE \'%lle\'', Arrays.asList('ID'), self._connectionPool)
        query.beginTransaction()
        rs = query.getResults(0, 0)
        Assert.assertTrue(rs.next())
        Assert.assertEquals(0 + self._offset, rs.getInt(1))
        Assert.assertEquals('Ville', rs.getString(2))
        Assert.assertTrue(rs.next())
        Assert.assertEquals(1 + self._offset, rs.getInt(1))
        Assert.assertEquals('Kalle', rs.getString(2))
        Assert.assertTrue(rs.next())
        Assert.assertEquals(2 + self._offset, rs.getInt(1))
        Assert.assertEquals('Pelle', rs.getString(2))
        Assert.assertFalse(rs.next())
        query.commit()

    def getResults_noDelegate5000Rows_returns5000rows(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        query.beginTransaction()
        rs = query.getResults(0, 0)
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
        query.commit()

    def setFilters_noDelegate_shouldFail(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        filters = list()
        filters.add(Like('name', '%lle'))
        query.setFilters(filters)

    def setOrderBy_noDelegate_shouldFail(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        query.setOrderBy(Arrays.asList(OrderBy('name', True)))

    def storeRow_noDelegateNoTransactionActive_shouldFail(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        query.storeRow(RowItem(SQLContainer(query), RowId([1]), None))

    def storeRow_noDelegate_shouldFail(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        container = EasyMock.createNiceMock(SQLContainer)
        EasyMock.replay(container)
        query.beginTransaction()
        query.storeRow(RowItem(container, RowId([1]), None))
        query.commit()
        EasyMock.verify(container)

    def removeRow_noDelegate_shouldFail(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        container = EasyMock.createNiceMock(SQLContainer)
        EasyMock.replay(container)
        query.beginTransaction()
        query.removeRow(RowItem(container, RowId([1]), None))
        query.commit()
        EasyMock.verify(container)

    def beginTransaction_readOnly_shouldSucceed(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        query.beginTransaction()

    def commit_readOnly_shouldSucceed(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        query.beginTransaction()
        query.commit()

    def rollback_readOnly_shouldSucceed(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        query.beginTransaction()
        query.rollback()

    def commit_noActiveTransaction_shouldFail(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        query.commit()

    def rollback_noActiveTransaction_shouldFail(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        query.rollback()

    def containsRowWithKeys_simpleQueryWithExistingKeys_returnsTrue(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        Assert.assertTrue(query.containsRowWithKey(1))

    def containsRowWithKeys_simpleQueryWithNonexistingKeys_returnsTrue(self):
        # (expected = SQLException.class)
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        Assert.assertFalse(query.containsRowWithKey(1337))

    def containsRowWithKeys_simpleQueryWithInvalidKeys_shouldFail(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        Assert.assertFalse(query.containsRowWithKey(38796))

    def containsRowWithKeys_queryContainingWhereClauseAndExistingKeys_returnsTrue(self):
        query = FreeformQuery('SELECT * FROM people WHERE \"NAME\" LIKE \'%lle\'', Arrays.asList('ID'), self._connectionPool)
        Assert.assertTrue(query.containsRowWithKey(1))

    def containsRowWithKeys_queryContainingLowercaseWhereClauseAndExistingKeys_returnsTrue(self):
        query = FreeformQuery('select * from people where \"NAME\" like \'%lle\'', Arrays.asList('ID'), self._connectionPool)
        Assert.assertTrue(query.containsRowWithKey(1))

    def containsRowWithKeys_nullKeys_shouldFailAndReleaseConnections(self):
        # -------- Tests with a delegate ---------
        query = FreeformQuery('select * from people where \"NAME\" like \'%lle\'', Arrays.asList('ID'), self._connectionPool)
        # We should now be able to reserve two connections
        try:
            query.containsRowWithKey([None])
        except SQLException, e:
            self._connectionPool.reserveConnection()
            self._connectionPool.reserveConnection()

    def setDelegate_noExistingDelegate_shouldRegisterNewDelegate(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        query.setDelegate(delegate)
        Assert.assertEquals(delegate, query.getDelegate())

    def getResults_hasDelegate_shouldCallDelegate(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        if AllTests.db == DB.MSSQL:
            EasyMock.expect(delegate.getQueryString(0, 2)).andReturn('SELECT * FROM (SELECT row_number()' + 'OVER (ORDER BY id ASC) AS rownum, * FROM people)' + ' AS a WHERE a.rownum BETWEEN 0 AND 2')
        elif AllTests.db == DB.ORACLE:
            EasyMock.expect(delegate.getQueryString(0, 2)).andReturn('SELECT * FROM (SELECT  x.*, ROWNUM AS r FROM' + ' (SELECT * FROM people) x) WHERE r BETWEEN 1 AND 2')
        else:
            EasyMock.expect(delegate.getQueryString(0, 2)).andReturn('SELECT * FROM people LIMIT 2 OFFSET 0')
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        query.beginTransaction()
        query.getResults(0, 2)
        EasyMock.verify(delegate)
        query.commit()

    def getResults_delegateImplementsGetQueryString_shouldHonorOffsetAndPagelength(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        if AllTests.db == DB.MSSQL:
            EasyMock.expect(delegate.getQueryString(0, 2)).andReturn('SELECT * FROM (SELECT row_number()' + 'OVER (ORDER BY id ASC) AS rownum, * FROM people)' + ' AS a WHERE a.rownum BETWEEN 0 AND 2')
        elif AllTests.db == DB.ORACLE:
            EasyMock.expect(delegate.getQueryString(0, 2)).andReturn('SELECT * FROM (SELECT  x.*, ROWNUM AS r FROM' + ' (SELECT * FROM people) x) WHERE r BETWEEN 1 AND 2')
        else:
            EasyMock.expect(delegate.getQueryString(0, 2)).andReturn('SELECT * FROM people LIMIT 2 OFFSET 0')
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        query.beginTransaction()
        rs = query.getResults(0, 2)
        rsoffset = 0
        if AllTests.db == DB.MSSQL:
            rsoffset += 1
        Assert.assertTrue(rs.next())
        Assert.assertEquals(0 + self._offset, rs.getInt(1 + rsoffset))
        Assert.assertEquals('Ville', rs.getString(2 + rsoffset))
        Assert.assertTrue(rs.next())
        Assert.assertEquals(1 + self._offset, rs.getInt(1 + rsoffset))
        Assert.assertEquals('Kalle', rs.getString(2 + rsoffset))
        Assert.assertFalse(rs.next())
        EasyMock.verify(delegate)
        query.commit()

    def getResults_delegateRegistered5000Rows_returns100rows(self):
        DataGenerator.addFiveThousandPeople(self._connectionPool)
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        if AllTests.db == DB.MSSQL:
            EasyMock.expect(delegate.getQueryString(200, 100)).andReturn('SELECT * FROM (SELECT row_number()' + 'OVER (ORDER BY id ASC) AS rownum, * FROM people)' + ' AS a WHERE a.rownum BETWEEN 201 AND 300')
        elif AllTests.db == DB.ORACLE:
            EasyMock.expect(delegate.getQueryString(200, 100)).andReturn('SELECT * FROM (SELECT  x.*, ROWNUM AS r FROM' + ' (SELECT * FROM people ORDER BY ID ASC) x) WHERE r BETWEEN 201 AND 300')
        else:
            EasyMock.expect(delegate.getQueryString(200, 100)).andReturn('SELECT * FROM people LIMIT 100 OFFSET 200')
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        query.beginTransaction()
        rs = query.getResults(200, 100)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 100):
                break
            Assert.assertTrue(rs.next())
            Assert.assertEquals(200 + i + self._offset, rs.getInt('ID'))
        Assert.assertFalse(rs.next())
        query.commit()

    def setFilters_delegateImplementsSetFilters_shouldPassFiltersToDelegate(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        filters = list()
        filters.add(Like('name', '%lle'))
        delegate.setFilters(filters)
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        query.setFilters(filters)
        EasyMock.verify(delegate)

    def setFilters_delegateDoesNotImplementSetFilters_shouldFail(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        filters = list()
        filters.add(Like('name', '%lle'))
        delegate.setFilters(filters)
        EasyMock.expectLastCall().andThrow(self.UnsupportedOperationException())
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        query.setFilters(filters)
        EasyMock.verify(delegate)

    def setOrderBy_delegateImplementsSetOrderBy_shouldPassArgumentsToDelegate(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        orderBys = Arrays.asList(OrderBy('name', False))
        delegate.setOrderBy(orderBys)
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        query.setOrderBy(orderBys)
        EasyMock.verify(delegate)

    def setOrderBy_delegateDoesNotImplementSetOrderBy_shouldFail(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        orderBys = Arrays.asList(OrderBy('name', False))
        delegate.setOrderBy(orderBys)
        EasyMock.expectLastCall().andThrow(self.UnsupportedOperationException())
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        query.setOrderBy(orderBys)
        EasyMock.verify(delegate)

    def setFilters_noDelegateAndNullParameter_shouldSucceed(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        query.setFilters(None)

    def setOrderBy_noDelegateAndNullParameter_shouldSucceed(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        query.setOrderBy(None)

    def storeRow_delegateImplementsStoreRow_shouldPassToDelegate(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        EasyMock.expect(delegate.storeRow(EasyMock.isA(Connection), EasyMock.isA(RowItem))).andReturn(1)
        container = EasyMock.createNiceMock(SQLContainer)
        EasyMock.replay(delegate, container)
        query.setDelegate(delegate)
        query.beginTransaction()
        row = RowItem(container, RowId([1]), None)
        query.storeRow(row)
        query.commit()
        EasyMock.verify(delegate, container)

    def storeRow_delegateDoesNotImplementStoreRow_shouldFail(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        EasyMock.expect(delegate.storeRow(EasyMock.isA(Connection), EasyMock.isA(RowItem))).andThrow(self.UnsupportedOperationException())
        container = EasyMock.createNiceMock(SQLContainer)
        EasyMock.replay(delegate, container)
        query.setDelegate(delegate)
        query.beginTransaction()
        row = RowItem(container, RowId([1]), None)
        query.storeRow(row)
        query.commit()
        EasyMock.verify(delegate, container)

    def removeRow_delegateImplementsRemoveRow_shouldPassToDelegate(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        EasyMock.expect(delegate.removeRow(EasyMock.isA(Connection), EasyMock.isA(RowItem))).andReturn(True)
        container = EasyMock.createNiceMock(SQLContainer)
        EasyMock.replay(delegate, container)
        query.setDelegate(delegate)
        query.beginTransaction()
        row = RowItem(container, RowId([1]), None)
        query.removeRow(row)
        query.commit()
        EasyMock.verify(delegate, container)

    def removeRow_delegateDoesNotImplementRemoveRow_shouldFail(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        EasyMock.expect(delegate.removeRow(EasyMock.isA(Connection), EasyMock.isA(RowItem))).andThrow(self.UnsupportedOperationException())
        container = EasyMock.createNiceMock(SQLContainer)
        EasyMock.replay(delegate, container)
        query.setDelegate(delegate)
        query.beginTransaction()
        row = RowItem(container, RowId([1]), None)
        query.removeRow(row)
        query.commit()
        EasyMock.verify(delegate, container)

    def beginTransaction_delegateRegistered_shouldSucceed(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        query.beginTransaction()

    def beginTransaction_transactionAlreadyActive_shouldFail(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        query.beginTransaction()
        query.beginTransaction()

    def commit_delegateRegisteredNoActiveTransaction_shouldFail(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        query.commit()

    def commit_delegateRegisteredActiveTransaction_shouldSucceed(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        query.beginTransaction()
        query.commit()

    def commit_delegateRegisteredActiveTransactionDoubleCommit_shouldFail(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        query.beginTransaction()
        query.commit()
        query.commit()

    def rollback_delegateRegisteredNoActiveTransaction_shouldFail(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        query.rollback()

    def rollback_delegateRegisteredActiveTransaction_shouldSucceed(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        query.beginTransaction()
        query.rollback()

    def rollback_delegateRegisteredActiveTransactionDoubleRollback_shouldFail(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        query.beginTransaction()
        query.rollback()
        query.rollback()

    def rollback_delegateRegisteredCommittedTransaction_shouldFail(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        query.beginTransaction()
        query.commit()
        query.rollback()

    def commit_delegateRegisteredRollbackedTransaction_shouldFail(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        query.beginTransaction()
        query.rollback()
        query.commit()

    def containsRowWithKeys_delegateRegistered_shouldCallGetContainsRowQueryString(self):
        query = FreeformQuery('SELECT * FROM people WHERE name LIKE \'%lle\'', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        EasyMock.expect(delegate.getContainsRowQueryString(1)).andReturn('')
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        query.containsRowWithKey(1)
        EasyMock.verify(delegate)

    def containsRowWithKeys_delegateRegistered_shouldUseResultFromGetContainsRowQueryString(self):
        query = FreeformQuery('SELECT * FROM people WHERE \"NAME\" LIKE \'%lle\'', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        # In order to test that this is the query that is actually used, we use
        # a non-existing id in place of the existing one.
        EasyMock.expect(delegate.getContainsRowQueryString(1)).andReturn('SELECT * FROM people WHERE \"NAME\" LIKE \'%lle\' AND \"ID\" = 1337')
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        # The id (key) used should be 1337 as above, for the call with key = 1
        Assert.assertFalse(query.containsRowWithKey(1))
        EasyMock.verify(delegate)

    def containsRowWithKeys_delegateRegisteredGetContainsRowQueryStringNotImplemented_shouldBuildQueryString(self):
        query = FreeformQuery('SELECT * FROM people WHERE \"NAME\" LIKE \'%lle\'', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformQueryDelegate)
        EasyMock.expect(delegate.getContainsRowQueryString(1)).andThrow(self.UnsupportedOperationException())
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        Assert.assertTrue(query.containsRowWithKey(1))
        EasyMock.verify(delegate)
