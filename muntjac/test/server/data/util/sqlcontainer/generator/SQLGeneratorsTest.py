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
# from com.vaadin.data.util.filter.Or import (Or,)
# from com.vaadin.data.util.sqlcontainer.RowItem import (RowItem,)
# from org.junit.After import (After,)
# from org.junit.Assert import (Assert,)
# from org.junit.Before import (Before,)
# from org.junit.Test import (Test,)


class SQLGeneratorsTest(object):
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

    def generateSelectQuery_basicQuery_shouldSucceed(self):
        sg = DefaultSQLGenerator()
        sh = sg.generateSelectQuery('TABLE', None, None, 0, 0, None)
        Assert.assertEquals(sh.getQueryString(), 'SELECT * FROM TABLE')

    def generateSelectQuery_pagingAndColumnsSet_shouldSucceed(self):
        sg = DefaultSQLGenerator()
        sh = sg.generateSelectQuery('TABLE', None, None, 4, 8, 'COL1, COL2, COL3')
        Assert.assertEquals(sh.getQueryString(), 'SELECT COL1, COL2, COL3 FROM TABLE LIMIT 8 OFFSET 4')

    def generateSelectQuery_filtersAndOrderingSet_shouldSucceed(self):
        """Note: Only tests one kind of filter and ordering."""
        sg = DefaultSQLGenerator()
        f = list()
        f.add(Like('name', '%lle'))
        ob = Arrays.asList(OrderBy('name', True))
        sh = sg.generateSelectQuery('TABLE', f, ob, 0, 0, None)
        Assert.assertEquals(sh.getQueryString(), 'SELECT * FROM TABLE WHERE \"name\" LIKE ? ORDER BY \"name\" ASC')

    def generateSelectQuery_filtersAndOrderingSet_exclusiveFilteringMode_shouldSucceed(self):
        sg = DefaultSQLGenerator()
        f = list()
        f.add(Or(Like('name', '%lle'), Like('name', 'vi%')))
        ob = Arrays.asList(OrderBy('name', True))
        sh = sg.generateSelectQuery('TABLE', f, ob, 0, 0, None)
        # TODO
        Assert.assertEquals(sh.getQueryString(), 'SELECT * FROM TABLE WHERE (\"name\" LIKE ? ' + 'OR \"name\" LIKE ?) ORDER BY \"name\" ASC')

    def generateDeleteQuery_basicQuery_shouldSucceed(self):
        # No need to run this for Oracle/MSSQL generators since the
        # DefaultSQLGenerator method would be called anyway.

        if (
            isinstance(AllTests.sqlGen, MSSQLGenerator) or isinstance(AllTests.sqlGen, OracleGenerator)
        ):
            return
        sg = AllTests.sqlGen
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = SQLContainer(query)
        sh = sg.generateDeleteQuery('people', query.getPrimaryKeyColumns(), None, container.getItem(container.getItemIds().next()))
        Assert.assertEquals('DELETE FROM people WHERE \"ID\" = ?', sh.getQueryString())

    def generateUpdateQuery_basicQuery_shouldSucceed(self):
        # No need to run this for Oracle/MSSQL generators since the
        # DefaultSQLGenerator method would be called anyway.

        if (
            isinstance(AllTests.sqlGen, MSSQLGenerator) or isinstance(AllTests.sqlGen, OracleGenerator)
        ):
            return
        sg = DefaultSQLGenerator()
        query = TableQuery('people', self._connectionPool)
        container = SQLContainer(query)
        ri = container.getItem(container.getItemIds().next())
        ri.getItemProperty('NAME').setValue('Viljami')
        sh = sg.generateUpdateQuery('people', ri)
        Assert.assertTrue(('UPDATE people SET \"NAME\" = ?, \"AGE\" = ? WHERE \"ID\" = ?' == sh.getQueryString()) or ('UPDATE people SET \"AGE\" = ?, \"NAME\" = ? WHERE \"ID\" = ?' == sh.getQueryString()))

    def generateInsertQuery_basicQuery_shouldSucceed(self):
        # No need to run this for Oracle/MSSQL generators since the
        # DefaultSQLGenerator method would be called anyway.

        if (
            isinstance(AllTests.sqlGen, MSSQLGenerator) or isinstance(AllTests.sqlGen, OracleGenerator)
        ):
            return
        sg = DefaultSQLGenerator()
        query = TableQuery('people', self._connectionPool)
        container = SQLContainer(query)
        ri = container.getItem(container.addItem())
        ri.getItemProperty('NAME').setValue('Viljami')
        sh = sg.generateInsertQuery('people', ri)
        Assert.assertTrue(('INSERT INTO people (\"NAME\", \"AGE\") VALUES (?, ?)' == sh.getQueryString()) or ('INSERT INTO people (\"AGE\", \"NAME\") VALUES (?, ?)' == sh.getQueryString()))

    def generateComplexSelectQuery_forOracle_shouldSucceed(self):
        sg = OracleGenerator()
        f = list()
        f.add(Like('name', '%lle'))
        ob = Arrays.asList(OrderBy('name', True))
        sh = sg.generateSelectQuery('TABLE', f, ob, 4, 8, 'NAME, ID')
        Assert.assertEquals('SELECT * FROM (SELECT x.*, ROWNUM AS \"rownum\" FROM' + ' (SELECT NAME, ID FROM TABLE WHERE \"name\" LIKE ?' + ' ORDER BY \"name\" ASC) x) WHERE \"rownum\" BETWEEN 5 AND 12', sh.getQueryString())

    def generateComplexSelectQuery_forMSSQL_shouldSucceed(self):
        sg = MSSQLGenerator()
        f = list()
        f.add(Like('name', '%lle'))
        ob = Arrays.asList(OrderBy('name', True))
        sh = sg.generateSelectQuery('TABLE', f, ob, 4, 8, 'NAME, ID')
        Assert.assertEquals(sh.getQueryString(), 'SELECT * FROM (SELECT row_number() OVER ' + '( ORDER BY \"name\" ASC) AS rownum, NAME, ID ' + 'FROM TABLE WHERE \"name\" LIKE ?) ' + 'AS a WHERE a.rownum BETWEEN 5 AND 12')

    def generateComplexSelectQuery_forOracle_exclusiveFilteringMode_shouldSucceed(self):
        sg = OracleGenerator()
        f = list()
        f.add(Or(Like('name', '%lle'), Like('name', 'vi%')))
        ob = Arrays.asList(OrderBy('name', True))
        sh = sg.generateSelectQuery('TABLE', f, ob, 4, 8, 'NAME, ID')
        Assert.assertEquals(sh.getQueryString(), 'SELECT * FROM (SELECT x.*, ROWNUM AS \"rownum\" FROM' + ' (SELECT NAME, ID FROM TABLE WHERE (\"name\" LIKE ?' + ' OR \"name\" LIKE ?) ' + 'ORDER BY \"name\" ASC) x) WHERE \"rownum\" BETWEEN 5 AND 12')

    def generateComplexSelectQuery_forMSSQL_exclusiveFilteringMode_shouldSucceed(self):
        sg = MSSQLGenerator()
        f = list()
        f.add(Or(Like('name', '%lle'), Like('name', 'vi%')))
        ob = Arrays.asList(OrderBy('name', True))
        sh = sg.generateSelectQuery('TABLE', f, ob, 4, 8, 'NAME, ID')
        Assert.assertEquals(sh.getQueryString(), 'SELECT * FROM (SELECT row_number() OVER ' + '( ORDER BY \"name\" ASC) AS rownum, NAME, ID ' + 'FROM TABLE WHERE (\"name\" LIKE ? ' + 'OR \"name\" LIKE ?)) ' + 'AS a WHERE a.rownum BETWEEN 5 AND 12')
