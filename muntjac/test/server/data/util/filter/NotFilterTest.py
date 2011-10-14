# -*- coding: utf-8 -*-
from com.vaadin.data.util.filter.AbstractFilterTest import (AbstractFilterTest,)
# from com.vaadin.data.util.BeanItem import (BeanItem,)
# from com.vaadin.data.util.filter.And import (And,)
# from com.vaadin.data.util.filter.Not import (Not,)
# from junit.framework.Assert import (Assert,)


class NotFilterTest(AbstractFilterTest):
    item1 = BeanItem(1)
    item2 = BeanItem(2)

    def testNot(self):
        origFilter = self.SameItemFilter(self.item1)
        filter = Not(origFilter)
        Assert.assertTrue(origFilter.passesFilter(None, self.item1))
        Assert.assertFalse(origFilter.passesFilter(None, self.item2))
        Assert.assertFalse(filter.passesFilter(None, self.item1))
        Assert.assertTrue(filter.passesFilter(None, self.item2))

    def testANotAppliesToProperty(self):
        filterA = Not(self.SameItemFilter(self.item1, 'a'))
        filterB = Not(self.SameItemFilter(self.item1, 'b'))
        Assert.assertTrue(filterA.appliesToProperty('a'))
        Assert.assertFalse(filterA.appliesToProperty('b'))
        Assert.assertFalse(filterB.appliesToProperty('a'))
        Assert.assertTrue(filterB.appliesToProperty('b'))

    def testNotEqualsHashCode(self):
        origFilter = self.SameItemFilter(self.item1)
        filter1 = Not(origFilter)
        filter1b = Not(self.SameItemFilter(self.item1))
        filter2 = Not(self.SameItemFilter(self.item2))
        # equals()
        Assert.assertEquals(filter1, filter1b)
        Assert.assertFalse(filter1 == filter2)
        Assert.assertFalse(filter1 == origFilter)
        Assert.assertFalse(filter1 == And())
        # hashCode()
        Assert.assertEquals(filter1.hashCode(), filter1b.hashCode())
