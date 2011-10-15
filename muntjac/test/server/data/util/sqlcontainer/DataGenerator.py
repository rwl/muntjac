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
# from java.sql.ResultSet import (ResultSet,)
# from org.junit.Assert import (Assert,)
# from org.junit.Test import (Test,)
DB = AllTests.DB


class DataGenerator(object):

    def testDummy(self):
        # Added dummy test so JUnit will not complain about "No runnable methods".
        pass

    @classmethod
    def addPeopleToDatabase(cls, connectionPool):
        conn = connectionPool.reserveConnection()
        statement = conn.createStatement()
        # Will fail if table doesn't exist, which is OK.
        try:
            statement.execute('drop table PEOPLE')
            if AllTests.db == DB.ORACLE:
                statement.execute('drop sequence people_seq')
        except SQLException, e:
            conn.rollback()
        statement.execute(AllTests.peopleFirst)
        if AllTests.peopleSecond is not None:
            statement.execute(AllTests.peopleSecond)
        if AllTests.db == DB.ORACLE:
            statement.execute(AllTests.peopleThird)
        if AllTests.db == DB.MSSQL:
            statement.executeUpdate('insert into people values(\'Ville\', \'23\')')
            statement.executeUpdate('insert into people values(\'Kalle\', \'7\')')
            statement.executeUpdate('insert into people values(\'Pelle\', \'18\')')
            statement.executeUpdate('insert into people values(\'Börje\', \'64\')')
        else:
            statement.executeUpdate('insert into people values(default, \'Ville\', \'23\')')
            statement.executeUpdate('insert into people values(default, \'Kalle\', \'7\')')
            statement.executeUpdate('insert into people values(default, \'Pelle\', \'18\')')
            statement.executeUpdate('insert into people values(default, \'Börje\', \'64\')')
        statement.close()
        statement = conn.createStatement()
        rs = statement.executeQuery('select * from PEOPLE')
        Assert.assertTrue(rs.next())
        statement.close()
        conn.commit()
        connectionPool.releaseConnection(conn)

    @classmethod
    def addFiveThousandPeople(cls, connectionPool):
        conn = connectionPool.reserveConnection()
        statement = conn.createStatement()
        _0 = True
        i = 4
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 5000):
                break
            if AllTests.db == DB.MSSQL:
                statement.executeUpdate('insert into people values(\'Person ' + i + '\', \'' + (i % 99) + '\')')
            else:
                statement.executeUpdate('insert into people values(default, \'Person ' + i + '\', \'' + (i % 99) + '\')')
        statement.close()
        conn.commit()
        connectionPool.releaseConnection(conn)

    @classmethod
    def addVersionedData(cls, connectionPool):
        conn = connectionPool.reserveConnection()
        statement = conn.createStatement()
        # Will fail if table doesn't exist, which is OK.
        try:
            statement.execute('DROP TABLE VERSIONED')
            if AllTests.db == DB.ORACLE:
                statement.execute('drop sequence versioned_seq')
                statement.execute('drop sequence versioned_version')
        except SQLException, e:
            conn.rollback()
        for stmtString in AllTests.versionStatements:
            statement.execute(stmtString)
        if AllTests.db == DB.MSSQL:
            statement.executeUpdate('insert into VERSIONED values(\'Junk\', default)')
        else:
            statement.executeUpdate('insert into VERSIONED values(default, \'Junk\', default)')
        statement.close()
        statement = conn.createStatement()
        rs = statement.executeQuery('select * from VERSIONED')
        Assert.assertTrue(rs.next())
        statement.close()
        conn.commit()
        connectionPool.releaseConnection(conn)

    @classmethod
    def createGarbage(cls, connectionPool):
        conn = connectionPool.reserveConnection()
        statement = conn.createStatement()
        # Will fail if table doesn't exist, which is OK.
        try:
            statement.execute('drop table GARBAGE')
            if AllTests.db == DB.ORACLE:
                statement.execute('drop sequence garbage_seq')
        except SQLException, e:
            conn.rollback()
        statement.execute(AllTests.createGarbage)
        if AllTests.db == DB.ORACLE:
            statement.execute(AllTests.createGarbageSecond)
            statement.execute(AllTests.createGarbageThird)
        conn.commit()
        connectionPool.releaseConnection(conn)
