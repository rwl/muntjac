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

from muntjac.test.server.data.util.filter.AbstractFilterTest import \
    AbstractFilterTest

# from com.vaadin.data.util.BeanItem import (BeanItem,)
# from com.vaadin.data.util.filter.And import (And,)
# from com.vaadin.data.util.filter.Not import (Not,)
# from junit.framework.Assert import (Assert,)


class NotFilterTest(AbstractFilterTest):

    def setUp(self):
        AbstractFilterTest.setUp(self)

        self.item1 = BeanItem(1)
        self.item2 = BeanItem(2)


    def testNot(self):
        origFilter = self.SameItemFilter(self.item1)
        filter = Not(origFilter)
        self.assertTrue(origFilter.passesFilter(None, self.item1))
        self.assertFalse(origFilter.passesFilter(None, self.item2))
        self.assertFalse(filter.passesFilter(None, self.item1))
        self.assertTrue(filter.passesFilter(None, self.item2))


    def testANotAppliesToProperty(self):
        filterA = Not(self.SameItemFilter(self.item1, 'a'))
        filterB = Not(self.SameItemFilter(self.item1, 'b'))
        self.assertTrue(filterA.appliesToProperty('a'))
        self.assertFalse(filterA.appliesToProperty('b'))
        self.assertFalse(filterB.appliesToProperty('a'))
        self.assertTrue(filterB.appliesToProperty('b'))


    def testNotEqualsHashCode(self):
        origFilter = self.SameItemFilter(self.item1)
        filter1 = Not(origFilter)
        filter1b = Not(self.SameItemFilter(self.item1))
        filter2 = Not(self.SameItemFilter(self.item2))
        # equals()
        self.assertEquals(filter1, filter1b)
        self.assertFalse(filter1 == filter2)
        self.assertFalse(filter1 == origFilter)
        self.assertFalse(filter1 == And())
        # hashCode()
        self.assertEquals(filter1.hashCode(), filter1b.hashCode())
