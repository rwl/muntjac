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
# from com.vaadin.data.util.filter.IsNull import (IsNull,)
# from junit.framework.Assert import (Assert,)


class IsNullFilterTest(AbstractFilterTest):

    def testIsNull(self):
        item1 = PropertysetItem()
        item1.addItemProperty('a', ObjectProperty(None, str))
        item1.addItemProperty('b', ObjectProperty('b', str))
        item2 = PropertysetItem()
        item2.addItemProperty('a', ObjectProperty('a', str))
        item2.addItemProperty('b', ObjectProperty(None, str))
        filter1 = IsNull('a')
        filter2 = IsNull('b')
        Assert.assertTrue(filter1.passesFilter(None, item1))
        Assert.assertFalse(filter1.passesFilter(None, item2))
        Assert.assertFalse(filter2.passesFilter(None, item1))
        Assert.assertTrue(filter2.passesFilter(None, item2))

    def testIsNullAppliesToProperty(self):
        filterA = IsNull('a')
        filterB = IsNull('b')
        Assert.assertTrue(filterA.appliesToProperty('a'))
        Assert.assertFalse(filterA.appliesToProperty('b'))
        Assert.assertFalse(filterB.appliesToProperty('a'))
        Assert.assertTrue(filterB.appliesToProperty('b'))

    def testIsNullEqualsHashCode(self):
        filter1 = IsNull('a')
        filter1b = IsNull('a')
        filter2 = IsNull('b')
        # equals()
        Assert.assertEquals(filter1, filter1b)
        Assert.assertFalse(filter1 == filter2)
        Assert.assertFalse(filter1 == And())
        # hashCode()
        Assert.assertEquals(filter1.hashCode(), filter1b.hashCode())
