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

# from com.vaadin.data.util.filter.And import (And,)
# from com.vaadin.data.util.filter.Compare.Greater import (Greater,)
# from com.vaadin.data.util.filter.Compare.GreaterOrEqual import (GreaterOrEqual,)
# from com.vaadin.data.util.filter.Compare.Less import (Less,)
# from com.vaadin.data.util.filter.Compare.LessOrEqual import (LessOrEqual,)
# from com.vaadin.data.util.filter.IsNull import (IsNull,)
# from com.vaadin.data.util.filter.Not import (Not,)
# from com.vaadin.data.util.filter.SimpleStringFilter import (SimpleStringFilter,)
# from com.vaadin.data.util.sqlcontainer.query.generator.filter.StringDecorator import (StringDecorator,)
# from junit.framework.Assert import (Assert,)
# from org.easymock.EasyMock import (EasyMock,)
# from org.junit.Test import (Test,)


class QueryBuilderTest(object):

    def mockedStatementHelper(self, *values):
        # escape bad characters and wildcards
        sh = EasyMock.createMock(StatementHelper)
        for val in values:
            sh.addParameterValue(val)
            EasyMock.expectLastCall()
        EasyMock.replay(sh)
        return sh

    def getWhereStringForFilter_equals(self):
        sh = self.mockedStatementHelper('Fido')
        f = Equal('NAME', 'Fido')
        Assert.assertEquals('\"NAME\" = ?', QueryBuilder.getWhereStringForFilter(f, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilter_greater(self):
        sh = self.mockedStatementHelper(18)
        f = Greater('AGE', 18)
        Assert.assertEquals('\"AGE\" > ?', QueryBuilder.getWhereStringForFilter(f, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilter_less(self):
        sh = self.mockedStatementHelper(65)
        f = Less('AGE', 65)
        Assert.assertEquals('\"AGE\" < ?', QueryBuilder.getWhereStringForFilter(f, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilter_greaterOrEqual(self):
        sh = self.mockedStatementHelper(18)
        f = GreaterOrEqual('AGE', 18)
        Assert.assertEquals('\"AGE\" >= ?', QueryBuilder.getWhereStringForFilter(f, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilter_lessOrEqual(self):
        sh = self.mockedStatementHelper(65)
        f = LessOrEqual('AGE', 65)
        Assert.assertEquals('\"AGE\" <= ?', QueryBuilder.getWhereStringForFilter(f, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilter_simpleStringFilter(self):
        sh = self.mockedStatementHelper('Vi%')
        f = SimpleStringFilter('NAME', 'Vi', False, True)
        Assert.assertEquals('\"NAME\" LIKE ?', QueryBuilder.getWhereStringForFilter(f, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilter_simpleStringFilterMatchAnywhere(self):
        sh = self.mockedStatementHelper('%Vi%')
        f = SimpleStringFilter('NAME', 'Vi', False, False)
        Assert.assertEquals('\"NAME\" LIKE ?', QueryBuilder.getWhereStringForFilter(f, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilter_simpleStringFilterMatchAnywhereIgnoreCase(self):
        sh = self.mockedStatementHelper('%VI%')
        f = SimpleStringFilter('NAME', 'Vi', True, False)
        Assert.assertEquals('UPPER(\"NAME\") LIKE ?', QueryBuilder.getWhereStringForFilter(f, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilter_startsWith(self):
        sh = self.mockedStatementHelper('Vi%')
        f = Like('NAME', 'Vi%')
        Assert.assertEquals('\"NAME\" LIKE ?', QueryBuilder.getWhereStringForFilter(f, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilter_startsWithNumber(self):
        sh = self.mockedStatementHelper('1%')
        f = Like('AGE', '1%')
        Assert.assertEquals('\"AGE\" LIKE ?', QueryBuilder.getWhereStringForFilter(f, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilter_endsWith(self):
        sh = self.mockedStatementHelper('%lle')
        f = Like('NAME', '%lle')
        Assert.assertEquals('\"NAME\" LIKE ?', QueryBuilder.getWhereStringForFilter(f, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilter_contains(self):
        sh = self.mockedStatementHelper('%ill%')
        f = Like('NAME', '%ill%')
        Assert.assertEquals('\"NAME\" LIKE ?', QueryBuilder.getWhereStringForFilter(f, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilter_between(self):
        sh = self.mockedStatementHelper(18, 65)
        f = Between('AGE', 18, 65)
        Assert.assertEquals('\"AGE\" BETWEEN ? AND ?', QueryBuilder.getWhereStringForFilter(f, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilter_caseInsensitive_equals(self):
        sh = self.mockedStatementHelper('FIDO')
        f = Like('NAME', 'Fido')
        f.setCaseSensitive(False)
        Assert.assertEquals('UPPER(\"NAME\") LIKE ?', QueryBuilder.getWhereStringForFilter(f, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilter_caseInsensitive_startsWith(self):
        sh = self.mockedStatementHelper('VI%')
        f = Like('NAME', 'Vi%')
        f.setCaseSensitive(False)
        Assert.assertEquals('UPPER(\"NAME\") LIKE ?', QueryBuilder.getWhereStringForFilter(f, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilter_caseInsensitive_endsWith(self):
        sh = self.mockedStatementHelper('%LLE')
        f = Like('NAME', '%lle')
        f.setCaseSensitive(False)
        Assert.assertEquals('UPPER(\"NAME\") LIKE ?', QueryBuilder.getWhereStringForFilter(f, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilter_caseInsensitive_contains(self):
        sh = self.mockedStatementHelper('%ILL%')
        f = Like('NAME', '%ill%')
        f.setCaseSensitive(False)
        Assert.assertEquals('UPPER(\"NAME\") LIKE ?', QueryBuilder.getWhereStringForFilter(f, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilters_listOfFilters(self):
        sh = self.mockedStatementHelper('%lle', 18)
        filters = list()
        filters.add(Like('NAME', '%lle'))
        filters.add(Greater('AGE', 18))
        Assert.assertEquals(' WHERE \"NAME\" LIKE ? AND \"AGE\" > ?', QueryBuilder.getWhereStringForFilters(filters, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilters_oneAndFilter(self):
        sh = self.mockedStatementHelper('%lle', 18)
        filters = list()
        filters.add(And(Like('NAME', '%lle'), Greater('AGE', 18)))
        Assert.assertEquals(' WHERE (\"NAME\" LIKE ? AND \"AGE\" > ?)', QueryBuilder.getWhereStringForFilters(filters, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilters_oneOrFilter(self):
        sh = self.mockedStatementHelper('%lle', 18)
        filters = list()
        filters.add(Or(Like('NAME', '%lle'), Greater('AGE', 18)))
        Assert.assertEquals(' WHERE (\"NAME\" LIKE ? OR \"AGE\" > ?)', QueryBuilder.getWhereStringForFilters(filters, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilters_complexCompoundFilters(self):
        sh = self.mockedStatementHelper('%lle', 18, 65, 'Pelle')
        filters = list()
        filters.add(Or(And(Like('NAME', '%lle'), Or(Less('AGE', 18), Greater('AGE', 65))), Equal('NAME', 'Pelle')))
        Assert.assertEquals(' WHERE ((\"NAME\" LIKE ? AND (\"AGE\" < ? OR \"AGE\" > ?)) OR \"NAME\" = ?)', QueryBuilder.getWhereStringForFilters(filters, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilters_complexCompoundFiltersAndSingleFilter(self):
        sh = self.mockedStatementHelper('%lle', 18, 65, 'Pelle', 'Virtanen')
        filters = list()
        filters.add(Or(And(Like('NAME', '%lle'), Or(Less('AGE', 18), Greater('AGE', 65))), Equal('NAME', 'Pelle')))
        filters.add(Equal('LASTNAME', 'Virtanen'))
        Assert.assertEquals(' WHERE ((\"NAME\" LIKE ? AND (\"AGE\" < ? OR \"AGE\" > ?)) OR \"NAME\" = ?) AND \"LASTNAME\" = ?', QueryBuilder.getWhereStringForFilters(filters, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilters_emptyList_shouldReturnEmptyString(self):
        filters = list()
        Assert.assertEquals('', QueryBuilder.getWhereStringForFilters(filters, StatementHelper()))

    def getWhereStringForFilters_NotFilter(self):
        sh = self.mockedStatementHelper(18)
        filters = list()
        filters.add(Not(Equal('AGE', 18)))
        Assert.assertEquals(' WHERE NOT \"AGE\" = ?', QueryBuilder.getWhereStringForFilters(filters, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilters_complexNegatedFilter(self):
        sh = self.mockedStatementHelper(65, 18)
        filters = list()
        filters.add(Not(Or(Equal('AGE', 65), Equal('AGE', 18))))
        Assert.assertEquals(' WHERE NOT (\"AGE\" = ? OR \"AGE\" = ?)', QueryBuilder.getWhereStringForFilters(filters, sh))
        EasyMock.verify(sh)

    def getWhereStringForFilters_isNull(self):
        filters = list()
        filters.add(IsNull('NAME'))
        Assert.assertEquals(' WHERE \"NAME\" IS NULL', QueryBuilder.getWhereStringForFilters(filters, StatementHelper()))

    def getWhereStringForFilters_isNotNull(self):
        filters = list()
        filters.add(Not(IsNull('NAME')))
        Assert.assertEquals(' WHERE \"NAME\" IS NOT NULL', QueryBuilder.getWhereStringForFilters(filters, StatementHelper()))

    def getWhereStringForFilters_customStringDecorator(self):
        QueryBuilder.setStringDecorator(StringDecorator('[', ']'))
        filters = list()
        filters.add(Not(IsNull('NAME')))
        Assert.assertEquals(' WHERE [NAME] IS NOT NULL', QueryBuilder.getWhereStringForFilters(filters, StatementHelper()))
        # Reset the default string decorator
        QueryBuilder.setStringDecorator(StringDecorator('\"', '\"'))
