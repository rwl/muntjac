# -*- coding: utf-8 -*-
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
