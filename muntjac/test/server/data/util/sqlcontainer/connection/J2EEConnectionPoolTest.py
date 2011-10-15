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

from com.vaadin.data.util.sqlcontainer.connection.MockInitialContextFactory import (MockInitialContextFactory,)
# from javax.naming.Context import (Context,)
# from javax.naming.NamingException import (NamingException,)
# from javax.sql.DataSource import (DataSource,)
# from junit.framework.Assert import (Assert,)
# from org.easymock.EasyMock import (EasyMock,)
# from org.junit.Test import (Test,)


class J2EEConnectionPoolTest(object):

    def reserveConnection_dataSourceSpecified_shouldReturnValidConnection(self):
        connection = EasyMock.createMock(Connection)
        connection.setAutoCommit(False)
        EasyMock.expectLastCall()
        ds = EasyMock.createMock(DataSource)
        ds.getConnection()
        EasyMock.expectLastCall().andReturn(connection)
        EasyMock.replay(connection, ds)
        pool = self.J2EEConnectionPool(ds)
        c = pool.reserveConnection()
        Assert.assertEquals(connection, c)
        EasyMock.verify(connection, ds)

    def releaseConnection_shouldCloseConnection(self):
        connection = EasyMock.createMock(Connection)
        connection.setAutoCommit(False)
        EasyMock.expectLastCall()
        connection.close()
        EasyMock.expectLastCall()
        ds = EasyMock.createMock(DataSource)
        ds.getConnection()
        EasyMock.expectLastCall().andReturn(connection)
        EasyMock.replay(connection, ds)
        pool = self.J2EEConnectionPool(ds)
        c = pool.reserveConnection()
        Assert.assertEquals(connection, c)
        pool.releaseConnection(c)
        EasyMock.verify(connection, ds)

    def reserveConnection_dataSourceLookedUp_shouldReturnValidConnection(self):
        connection = EasyMock.createMock(Connection)
        connection.setAutoCommit(False)
        EasyMock.expectLastCall()
        connection.close()
        EasyMock.expectLastCall()
        ds = EasyMock.createMock(DataSource)
        ds.getConnection()
        EasyMock.expectLastCall().andReturn(connection)
        System.setProperty('java.naming.factory.initial', 'com.vaadin.data.util.sqlcontainer.connection.MockInitialContextFactory')
        context = EasyMock.createMock(Context)
        context.lookup('testDataSource')
        EasyMock.expectLastCall().andReturn(ds)
        MockInitialContextFactory.setMockContext(context)
        EasyMock.replay(context, connection, ds)
        pool = self.J2EEConnectionPool('testDataSource')
        c = pool.reserveConnection()
        Assert.assertEquals(connection, c)
        pool.releaseConnection(c)
        EasyMock.verify(context, connection, ds)

    def reserveConnection_nonExistantDataSourceLookedUp_shouldFail(self):
        System.setProperty('java.naming.factory.initial', 'com.vaadin.addon.sqlcontainer.connection.MockInitialContextFactory')
        context = EasyMock.createMock(Context)
        context.lookup('foo')
        EasyMock.expectLastCall().andThrow(NamingException('fail'))
        MockInitialContextFactory.setMockContext(context)
        EasyMock.replay(context)
        pool = self.J2EEConnectionPool('foo')
        pool.reserveConnection()
        EasyMock.verify(context)

    def releaseConnection_null_shouldSucceed(self):
        ds = EasyMock.createMock(DataSource)
        EasyMock.replay(ds)
        pool = self.J2EEConnectionPool(ds)
        pool.releaseConnection(None)
        EasyMock.verify(ds)
