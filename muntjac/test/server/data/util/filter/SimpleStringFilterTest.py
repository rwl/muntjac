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

from com.vaadin.data.util.filter.AbstractFilterTest import (AbstractFilterTest,)
# from com.vaadin.data.util.filter.SimpleStringFilter import (SimpleStringFilter,)
# from junit.framework.Assert import (Assert,)


class SimpleStringFilterTest(AbstractFilterTest):

    @classmethod
    def createTestItem(cls):
        return cls.TestItem('abcde', 'TeSt')

    def getTestItem(self):
        return self.createTestItem()

    def f(self, propertyId, filterString, ignoreCase, onlyMatchPrefix):
        return SimpleStringFilter(propertyId, filterString, ignoreCase, onlyMatchPrefix)

    def passes(self, propertyId, filterString, ignoreCase, onlyMatchPrefix):
        return self.f(propertyId, filterString, ignoreCase, onlyMatchPrefix).passesFilter(None, self.getTestItem())

    def testStartsWithCaseSensitive(self):
        Assert.assertTrue(self.passes(self.PROPERTY1, 'ab', False, True))
        Assert.assertTrue(self.passes(self.PROPERTY1, '', False, True))
        Assert.assertFalse(self.passes(self.PROPERTY2, 'ab', False, True))
        Assert.assertFalse(self.passes(self.PROPERTY1, 'AB', False, True))

    def testStartsWithCaseInsensitive(self):
        Assert.assertTrue(self.passes(self.PROPERTY1, 'AB', True, True))
        Assert.assertTrue(self.passes(self.PROPERTY2, 'te', True, True))
        Assert.assertFalse(self.passes(self.PROPERTY2, 'AB', True, True))

    def testContainsCaseSensitive(self):
        Assert.assertTrue(self.passes(self.PROPERTY1, 'ab', False, False))
        Assert.assertTrue(self.passes(self.PROPERTY1, 'abcde', False, False))
        Assert.assertTrue(self.passes(self.PROPERTY1, 'cd', False, False))
        Assert.assertTrue(self.passes(self.PROPERTY1, 'e', False, False))
        Assert.assertTrue(self.passes(self.PROPERTY1, '', False, False))
        Assert.assertFalse(self.passes(self.PROPERTY2, 'ab', False, False))
        Assert.assertFalse(self.passes(self.PROPERTY1, 'es', False, False))

    def testContainsCaseInsensitive(self):
        Assert.assertTrue(self.passes(self.PROPERTY1, 'AB', True, False))
        Assert.assertTrue(self.passes(self.PROPERTY1, 'aBcDe', True, False))
        Assert.assertTrue(self.passes(self.PROPERTY1, 'CD', True, False))
        Assert.assertTrue(self.passes(self.PROPERTY1, '', True, False))
        Assert.assertTrue(self.passes(self.PROPERTY2, 'es', True, False))
        Assert.assertFalse(self.passes(self.PROPERTY2, 'ab', True, False))

    def testAppliesToProperty(self):
        filter = self.f(self.PROPERTY1, 'ab', False, True)
        Assert.assertTrue(filter.appliesToProperty(self.PROPERTY1))
        Assert.assertFalse(filter.appliesToProperty(self.PROPERTY2))
        Assert.assertFalse(filter.appliesToProperty('other'))

    def testEqualsHashCode(self):
        filter = self.f(self.PROPERTY1, 'ab', False, True)
        f1 = self.f(self.PROPERTY2, 'ab', False, True)
        f1b = self.f(self.PROPERTY2, 'ab', False, True)
        f2 = self.f(self.PROPERTY1, 'cd', False, True)
        f2b = self.f(self.PROPERTY1, 'cd', False, True)
        f3 = self.f(self.PROPERTY1, 'ab', True, True)
        f3b = self.f(self.PROPERTY1, 'ab', True, True)
        f4 = self.f(self.PROPERTY1, 'ab', False, False)
        f4b = self.f(self.PROPERTY1, 'ab', False, False)
        # equal but not same instance
        Assert.assertEquals(f1, f1b)
        Assert.assertEquals(f2, f2b)
        Assert.assertEquals(f3, f3b)
        Assert.assertEquals(f4, f4b)
        # more than one property differ
        Assert.assertFalse(f1 == f2)
        Assert.assertFalse(f1 == f3)
        Assert.assertFalse(f1 == f4)
        Assert.assertFalse(f2 == f1)
        Assert.assertFalse(f2 == f3)
        Assert.assertFalse(f2 == f4)
        Assert.assertFalse(f3 == f1)
        Assert.assertFalse(f3 == f2)
        Assert.assertFalse(f3 == f4)
        Assert.assertFalse(f4 == f1)
        Assert.assertFalse(f4 == f2)
        Assert.assertFalse(f4 == f3)
        # only one property differs
        Assert.assertFalse(filter == f1)
        Assert.assertFalse(filter == f2)
        Assert.assertFalse(filter == f3)
        Assert.assertFalse(filter == f4)
        Assert.assertFalse(f1 is None)
        Assert.assertFalse(f1 == self.Object())
        Assert.assertEquals(f1.hashCode(), f1b.hashCode())
        Assert.assertEquals(f2.hashCode(), f2b.hashCode())
        Assert.assertEquals(f3.hashCode(), f3b.hashCode())
        Assert.assertEquals(f4.hashCode(), f4b.hashCode())

    def testNonExistentProperty(self):
        Assert.assertFalse(self.passes('other1', 'ab', False, True))

    def testNullValueForProperty(self):
        item = self.createTestItem()
        item.addItemProperty('other1', self.NullProperty())
        Assert.assertFalse(self.f('other1', 'ab', False, True).passesFilter(None, item))
