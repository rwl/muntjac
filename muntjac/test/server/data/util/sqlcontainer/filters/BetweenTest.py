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

# from com.vaadin.data.Property import (Property,)
# from com.vaadin.data.util.filter.Between import (Between,)
# from junit.framework.Assert import (Assert,)
# from org.easymock.EasyMock import (EasyMock,)
# from org.junit.Test import (Test,)


class BetweenTest(object):

    def itemWithPropertyValue(self, propertyId, value):
        property = EasyMock.createMock(Property)
        property.getValue()
        EasyMock.expectLastCall().andReturn(value).anyTimes()
        EasyMock.replay(property)
        item = EasyMock.createMock(Item)
        item.getItemProperty(propertyId)
        EasyMock.expectLastCall().andReturn(property).anyTimes()
        EasyMock.replay(item)
        return item

    def passesFilter_valueIsInRange_shouldBeTrue(self):
        item = self.itemWithPropertyValue('foo', 15)
        between = Between('foo', 1, 30)
        Assert.assertTrue(between.passesFilter('foo', item))

    def passesFilter_valueIsOutOfRange_shouldBeFalse(self):
        item = self.itemWithPropertyValue('foo', 15)
        between = Between('foo', 0, 2)
        Assert.assertFalse(between.passesFilter('foo', item))

    def passesFilter_valueNotComparable_shouldBeFalse(self):
        item = self.itemWithPropertyValue('foo', self.Object())
        between = Between('foo', 0, 2)
        Assert.assertFalse(between.passesFilter('foo', item))

    def appliesToProperty_differentProperties_shoudlBeFalse(self):
        between = Between('foo', 0, 2)
        Assert.assertFalse(between.appliesToProperty('bar'))

    def appliesToProperty_sameProperties_shouldBeTrue(self):
        between = Between('foo', 0, 2)
        Assert.assertTrue(between.appliesToProperty('foo'))

    def hashCode_equalInstances_shouldBeEqual(self):
        b1 = Between('foo', 0, 2)
        b2 = Between('foo', 0, 2)
        Assert.assertEquals(b1.hashCode(), b2.hashCode())

    def equals_differentObjects_shouldBeFalse(self):
        b1 = Between('foo', 0, 2)
        obj = self.Object()
        Assert.assertFalse(b1 == obj)

    def equals_sameInstance_shouldBeTrue(self):
        b1 = Between('foo', 0, 2)
        b2 = b1
        Assert.assertTrue(b1 == b2)

    def equals_equalInstances_shouldBeTrue(self):
        b1 = Between('foo', 0, 2)
        b2 = Between('foo', 0, 2)
        Assert.assertTrue(b1 == b2)

    def equals_equalInstances2_shouldBeTrue(self):
        b1 = Between(None, None, None)
        b2 = Between(None, None, None)
        Assert.assertTrue(b1 == b2)

    def equals_secondValueDiffers_shouldBeFalse(self):
        b1 = Between('foo', 0, 1)
        b2 = Between('foo', 0, 2)
        Assert.assertFalse(b1 == b2)

    def equals_firstAndSecondValueDiffers_shouldBeFalse(self):
        b1 = Between('foo', 0, None)
        b2 = Between('foo', 1, 2)
        Assert.assertFalse(b1 == b2)

    def equals_propertyAndFirstAndSecondValueDiffers_shouldBeFalse(self):
        b1 = Between('foo', None, 1)
        b2 = Between('bar', 1, 2)
        Assert.assertFalse(b1 == b2)

    def equals_propertiesDiffer_shouldBeFalse(self):
        b1 = Between(None, 0, 1)
        b2 = Between('bar', 0, 1)
        Assert.assertFalse(b1 == b2)
