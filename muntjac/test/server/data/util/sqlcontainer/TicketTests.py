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
# from com.vaadin.data.util.sqlcontainer.SQLContainer import (SQLContainer,)
# from com.vaadin.ui.Table import (Table,)
# from com.vaadin.ui.Window import (Window,)
# from org.easymock.EasyMock import (EasyMock,)
# from org.easymock.IAnswer import (IAnswer,)
# from org.junit.Assert import (Assert,)
# from org.junit.Before import (Before,)
# from org.junit.Test import (Test,)
DB = AllTests.DB


class TicketTests(object):
    _connectionPool = None

    def setUp(self):
        self._connectionPool = SimpleJDBCConnectionPool(AllTests.dbDriver, AllTests.dbURL, AllTests.dbUser, AllTests.dbPwd, 2, 2)
        DataGenerator.addPeopleToDatabase(self._connectionPool)

    def ticket5867_throwsIllegalState_transactionAlreadyActive(self):
        container = SQLContainer(FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool))
        table = Table()
        w = Window()
        w.addComponent(table)
        table.setContainerDataSource(container)

    def ticket6136_freeform_ageIs18(self):
        query = FreeformQuery('SELECT * FROM people', Arrays.asList('ID'), self._connectionPool)
        delegate = EasyMock.createMock(FreeformStatementDelegate)
        filters = list()
        delegate.setFilters(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(EasyMock.isA(list))
        EasyMock.expectLastCall().anyTimes()
        delegate.setOrderBy(None)
        EasyMock.expectLastCall().anyTimes()
        delegate.setFilters(EasyMock.isA(list))


        class _0_(IAnswer):

            def answer(self):
                orders = EasyMock.getCurrentArguments()[0]
                self.filters.clear()
                self.filters.addAll(orders)
                return None


        _0_ = _0_()
        EasyMock.expectLastCall().andAnswer(_0_)
        None.anyTimes()


        class _1_(IAnswer):

            def answer(self):
                args = EasyMock.getCurrentArguments()
                offset = args[0]
                limit = args[1]
                return FreeformQueryUtil.getQueryWithFilters(self.filters, offset, limit)


        _1_ = _1_()
        EasyMock.expect(delegate.getQueryStatement(EasyMock.anyInt(), EasyMock.anyInt())).andAnswer(_1_)
        None.anyTimes()


        class _2_(IAnswer):

            def answer(self):
                sh = StatementHelper()
                query = str('SELECT COUNT(*) FROM people')
                if not self.filters.isEmpty():
                    query.__add__(QueryBuilder.getWhereStringForFilters(self.filters, sh))
                sh.setQueryString(str(query))
                return sh


        _2_ = _2_()
        EasyMock.expect(delegate.getCountStatement()).andAnswer(_2_)
        None.anyTimes()
        EasyMock.replay(delegate)
        query.setDelegate(delegate)
        container = SQLContainer(query)
        # Ville, Kalle, Pelle, Börje
        Assert.assertEquals(4, len(container))
        Assert.assertEquals('Börje', container.getContainerProperty(container.lastItemId(), 'NAME').getValue())
        container.addContainerFilter(Equal('AGE', 18))
        # Pelle
        Assert.assertEquals(1, len(container))
        Assert.assertEquals('Pelle', container.getContainerProperty(container.firstItemId(), 'NAME').getValue())
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals(BigDecimal(18), container.getContainerProperty(container.firstItemId(), 'AGE').getValue())
        else:
            Assert.assertEquals(18, container.getContainerProperty(container.firstItemId(), 'AGE').getValue())
        EasyMock.verify(delegate)

    def ticket6136_table_ageIs18(self):
        query = TableQuery('people', self._connectionPool, AllTests.sqlGen)
        container = SQLContainer(query)
        # Ville, Kalle, Pelle, Börje
        Assert.assertEquals(4, len(container))
        container.addContainerFilter(Equal('AGE', 18))
        # Pelle
        Assert.assertEquals(1, len(container))
        Assert.assertEquals('Pelle', container.getContainerProperty(container.firstItemId(), 'NAME').getValue())
        if AllTests.db == DB.ORACLE:
            Assert.assertEquals(BigDecimal(18), container.getContainerProperty(container.firstItemId(), 'AGE').getValue())
        else:
            Assert.assertEquals(18, container.getContainerProperty(container.firstItemId(), 'AGE').getValue())

    def ticket7434_getItem_Modified_Changed_Unchanged(self):
        container = SQLContainer(TableQuery('people', self._connectionPool, AllTests.sqlGen))
        id = container.firstItemId()
        item = container.getItem(id)
        name = item.getItemProperty('NAME').getValue()
        # set a different name
        item.getItemProperty('NAME').setValue('otherName')
        Assert.assertEquals('otherName', item.getItemProperty('NAME').getValue())
        # access the item and reset the name to its old value
        item2 = container.getItem(id)
        item2.getItemProperty('NAME').setValue(name)
        Assert.assertEquals(name, item2.getItemProperty('NAME').getValue())
        item3 = container.getItem(id)
        name3 = item3.getItemProperty('NAME').getValue()
        Assert.assertEquals(name, name3)
