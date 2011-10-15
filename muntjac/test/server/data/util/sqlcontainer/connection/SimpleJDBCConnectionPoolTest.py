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

from com.vaadin.data.util.sqlcontainer.AllTests import (AllTests,)
# from junit.framework.Assert import (Assert,)
# from org.easymock.EasyMock import (EasyMock,)
# from org.junit.Before import (Before,)
# from org.junit.Test import (Test,)


class SimpleJDBCConnectionPoolTest(object):
    _connectionPool = None

    def setUp(self):
        self._connectionPool = SimpleJDBCConnectionPool(AllTests.dbDriver, AllTests.dbURL, AllTests.dbUser, AllTests.dbPwd, 2, 2)

    def reserveConnection_reserveNewConnection_returnsConnection(self):
        conn = self._connectionPool.reserveConnection()
        Assert.assertNotNull(conn)

    def releaseConnection_releaseUnused_shouldNotThrowException(self):
        conn = self._connectionPool.reserveConnection()
        self._connectionPool.releaseConnection(conn)
        Assert.assertFalse(conn.isClosed())

    def reserveConnection_noConnectionsLeft_shouldFail(self):
        try:
            self._connectionPool.reserveConnection()
            self._connectionPool.reserveConnection()
        except SQLException, e:
            e.printStackTrace()
            Assert.fail('Exception before all connections used! ' + e.getMessage())
        self._connectionPool.reserveConnection()
        Assert.fail('Reserving connection didn\'t fail even though no connections are available!')

    def reserveConnection_oneConnectionLeft_returnsConnection(self):
        try:
            self._connectionPool.reserveConnection()
        except SQLException, e:
            e.printStackTrace()
            Assert.fail('Exception before all connections used! ' + e.getMessage())
        conn = self._connectionPool.reserveConnection()
        Assert.assertNotNull(conn)

    def reserveConnection_oneConnectionJustReleased_returnsConnection(self):
        conn2 = None
        try:
            self._connectionPool.reserveConnection()
            conn2 = self._connectionPool.reserveConnection()
        except SQLException, e:
            e.printStackTrace()
            Assert.fail('Exception before all connections used! ' + e.getMessage())
        self._connectionPool.releaseConnection(conn2)
        self._connectionPool.reserveConnection()

    def construct_allParametersNull_shouldFail(self):
        cp = SimpleJDBCConnectionPool(None, None, None, None)

    def construct_onlyDriverNameGiven_shouldFail(self):
        cp = SimpleJDBCConnectionPool(AllTests.dbDriver, None, None, None)

    def construct_onlyDriverNameAndUrlGiven_shouldFail(self):
        cp = SimpleJDBCConnectionPool(AllTests.dbDriver, AllTests.dbURL, None, None)

    def construct_onlyDriverNameAndUrlAndUserGiven_shouldFail(self):
        cp = SimpleJDBCConnectionPool(AllTests.dbDriver, AllTests.dbURL, AllTests.dbUser, None)

    def construct_nonExistingDriver_shouldFail(self):
        cp = SimpleJDBCConnectionPool('foo', AllTests.dbURL, AllTests.dbUser, AllTests.dbPwd)

    def reserveConnection_newConnectionOpened_shouldSucceed(self):
        self._connectionPool = SimpleJDBCConnectionPool(AllTests.dbDriver, AllTests.dbURL, AllTests.dbUser, AllTests.dbPwd, 0, 2)
        c = self._connectionPool.reserveConnection()
        Assert.assertNotNull(c)

    def releaseConnection_nullConnection_shouldDoNothing(self):
        self._connectionPool.releaseConnection(None)

    def releaseConnection_failingRollback_shouldCallClose(self):
        c = EasyMock.createMock(Connection)
        c.getAutoCommit()
        EasyMock.expectLastCall().andReturn(False)
        c.rollback()
        EasyMock.expectLastCall().andThrow(SQLException('Rollback failed'))
        c.close()
        EasyMock.expectLastCall().atLeastOnce()
        EasyMock.replay(c)
        # make sure the connection pool is initialized
        self._connectionPool.reserveConnection()
        self._connectionPool.releaseConnection(c)
        EasyMock.verify(c)

    def destroy_shouldCloseAllConnections(self):
        c1 = self._connectionPool.reserveConnection()
        c2 = self._connectionPool.reserveConnection()
        self._connectionPool.destroy()
        Assert.assertTrue(c1.isClosed())
        Assert.assertTrue(c2.isClosed())

    def destroy_shouldCloseAllConnections2(self):
        c1 = self._connectionPool.reserveConnection()
        c2 = self._connectionPool.reserveConnection()
        self._connectionPool.releaseConnection(c1)
        self._connectionPool.releaseConnection(c2)
        self._connectionPool.destroy()
        Assert.assertTrue(c1.isClosed())
        Assert.assertTrue(c2.isClosed())
