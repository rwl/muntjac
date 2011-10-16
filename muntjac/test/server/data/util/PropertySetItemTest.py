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

from unittest import TestCase

from muntjac.data.util.object_property import ObjectProperty
from muntjac.data.item import IPropertySetChangeListener

from muntjac.data.util.propertyset_item import PropertysetItem


class PropertySetItemTest(TestCase):

    _ID1 = 'id1'
    _ID2 = 'id2'
    _ID3 = 'id3'

    _VALUE1 = 'value1'
    _VALUE2 = 'value2'
    _VALUE3 = 'value3'

    def setUp(self):
        self._prop1 = ObjectProperty(self._VALUE1, str)
        self._prop2 = ObjectProperty(self._VALUE2, str)
        self._prop3 = ObjectProperty(self._VALUE3, str)

        self._propertySetListenerMock = \
                EasyMock.createStrictMock(IPropertySetChangeListener)

        self._propertySetListenerMock2 = \
                EasyMock.createMock(IPropertySetChangeListener)


    def tearDown(self):
        self._prop1 = None
        self._prop2 = None
        self._prop3 = None
        self._propertySetListenerMock = None
        self._propertySetListenerMock2 = None


    def createPropertySetItem(self):
        return PropertysetItem()


    def testEmptyItem(self):
        item = self.createPropertySetItem()
        self.assertIsNotNone(item.getItemPropertyIds())
        self.assertEquals(0, len(item.getItemPropertyIds()))


    def testGetProperty(self):
        item = self.createPropertySetItem()

        self.assertIsNone(item.getItemProperty(self._ID1))

        item.addItemProperty(self._ID1, self._prop1)

        self.assertEquals(self._prop1, item.getItemProperty(self._ID1))
        self.assertIsNone(item.getItemProperty(self._ID2))


    def testAddSingleProperty(self):
        item = self.createPropertySetItem()

        item.addItemProperty(self._ID1, self._prop1)
        self.assertEquals(1, len(item.getItemPropertyIds()))
        firstValue = item.getItemPropertyIds().next()
        self.assertEquals(self._ID1, firstValue)
        self.assertEquals(self._prop1, item.getItemProperty(self._ID1))


    def testAddMultipleProperties(self):
        item = self.createPropertySetItem()

        item.addItemProperty(self._ID1, self._prop1)
        self.assertEquals(1, len(item.getItemPropertyIds()))
        self.assertEquals(self._prop1, item.getItemProperty(self._ID1))

        item.addItemProperty(self._ID2, self._prop2)
        self.assertEquals(2, len(item.getItemPropertyIds()))
        self.assertEquals(self._prop1, item.getItemProperty(self._ID1))
        self.assertEquals(self._prop2, item.getItemProperty(self._ID2))

        item.addItemProperty(self._ID3, self._prop3)
        self.assertEquals(3, len(item.getItemPropertyIds()))


    def testAddedPropertyOrder(self):
        item = self.createPropertySetItem()

        item.addItemProperty(self._ID1, self._prop1)
        item.addItemProperty(self._ID2, self._prop2)
        item.addItemProperty(self._ID3, self._prop3)

        it = item.getItemPropertyIds()
        self.assertEquals(self._ID1, it.next())
        self.assertEquals(self._ID2, it.next())
        self.assertEquals(self._ID3, it.next())


    def testAddPropertyTwice(self):
        item = self.createPropertySetItem()
        self.assertTrue(item.addItemProperty(self._ID1, self._prop1))
        self.assertFalse(item.addItemProperty(self._ID1, self._prop1))

        self.assertEquals(1, len(item.getItemPropertyIds()))
        self.assertEquals(self._prop1, item.getItemProperty(self._ID1))


    def testCannotChangeProperty(self):
        item = self.createPropertySetItem()
        self.assertTrue(item.addItemProperty(self._ID1, self._prop1))

        self.assertEquals(self._prop1, item.getItemProperty(self._ID1))

        self.assertFalse(item.addItemProperty(self._ID1, self._prop2))

        self.assertEquals(1, len(item.getItemPropertyIds()))
        self.assertEquals(self._prop1, item.getItemProperty(self._ID1))


    def testRemoveProperty(self):
        item = self.createPropertySetItem()
        item.addItemProperty(self._ID1, self._prop1)
        item.removeItemProperty(self._ID1)

        self.assertEquals(0, len(item.getItemPropertyIds()))
        self.assertIsNone(item.getItemProperty(self._ID1))


    def testRemovePropertyOrder(self):
        item = self.createPropertySetItem()
        item.addItemProperty(self._ID1, self._prop1)
        item.addItemProperty(self._ID2, self._prop2)
        item.addItemProperty(self._ID3, self._prop3)

        item.removeItemProperty(self._ID2)

        it = item.getItemPropertyIds()
        self.assertEquals(self._ID1, it.next())
        self.assertEquals(self._ID3, it.next())


    def testRemoveNonExistentListener(self):
        item = self.createPropertySetItem()
        item.removeListener(self._propertySetListenerMock)


    def testRemoveListenerTwice(self):
        item = self.createPropertySetItem()
        item.addListener(self._propertySetListenerMock)
        item.removeListener(self._propertySetListenerMock)
        item.removeListener(self._propertySetListenerMock)


    def testAddPropertyNotification(self):
        # exactly one notification each time
        item = self.createPropertySetItem()

        # Expectations and start test
        self._propertySetListenerMock.itemPropertySetChange(EasyMock.isA(PropertySetChangeEvent))
        EasyMock.replay(self._propertySetListenerMock)

        # Add listener and add a property -> should end up in listener once
        item.addListener(self._propertySetListenerMock)
        item.addItemProperty(self._ID1, self._prop1)

        # Ensure listener was called once
        EasyMock.verify(self._propertySetListenerMock)

        # Remove the listener -> should not end up in listener when adding a
        # property
        item.removeListener(self._propertySetListenerMock)
        item.addItemProperty(self._ID2, self._prop2)

        # Ensure listener still has been called only once
        EasyMock.verify(self._propertySetListenerMock)


    def testRemovePropertyNotification(self):
        # exactly one notification each time
        item = self.createPropertySetItem()
        item.addItemProperty(self._ID1, self._prop1)
        item.addItemProperty(self._ID2, self._prop2)

        # Expectations and start test
        self._propertySetListenerMock.itemPropertySetChange(EasyMock.isA(PropertySetChangeEvent))
        EasyMock.replay(self._propertySetListenerMock)

        # Add listener and add a property -> should end up in listener once
        item.addListener(self._propertySetListenerMock)
        item.removeItemProperty(self._ID1)

        # Ensure listener was called once
        EasyMock.verify(self._propertySetListenerMock)

        # Remove the listener -> should not end up in listener
        item.removeListener(self._propertySetListenerMock)
        item.removeItemProperty(self._ID2)

        # Ensure listener still has been called only once
        EasyMock.verify(self._propertySetListenerMock)


    def testItemEqualsNull(self):
        item = self.createPropertySetItem()
        self.assertFalse(item is None)


    def testEmptyItemEquals(self):
        item1 = self.createPropertySetItem()
        item2 = self.createPropertySetItem()
        self.assertTrue(item1 == item2)


    def testItemEqualsSingleProperty(self):
        item1 = self.createPropertySetItem()
        item2 = self.createPropertySetItem()
        item2.addItemProperty(self._ID1, self._prop1)
        item3 = self.createPropertySetItem()
        item3.addItemProperty(self._ID1, self._prop1)
        item4 = self.createPropertySetItem()
        item4.addItemProperty(self._ID1, self._prop2)
        item5 = self.createPropertySetItem()
        item5.addItemProperty(self._ID2, self._prop2)

        self.assertFalse(item1 == item2)
        self.assertFalse(item1 == item3)
        self.assertFalse(item1 == item4)
        self.assertFalse(item1 == item5)

        self.assertTrue(item2 == item3)
        self.assertFalse(item2 == item4)
        self.assertFalse(item2 == item5)

        self.assertFalse(item3 == item4)
        self.assertFalse(item3 == item5)

        self.assertFalse(item4 == item5)

        self.assertFalse(item2 == item1)


    def testItemEqualsMultipleProperties(self):
        item1 = self.createPropertySetItem()
        item1.addItemProperty(self._ID1, self._prop1)

        item2 = self.createPropertySetItem()
        item2.addItemProperty(self._ID1, self._prop1)
        item2.addItemProperty(self._ID2, self._prop2)

        item3 = self.createPropertySetItem()
        item3.addItemProperty(self._ID1, self._prop1)
        item3.addItemProperty(self._ID2, self._prop2)

        self.assertFalse(item1 == item2)

        self.assertTrue(item2 == item3)


    def testItemEqualsPropertyOrder(self):
        item1 = self.createPropertySetItem()
        item1.addItemProperty(self._ID1, self._prop1)
        item1.addItemProperty(self._ID2, self._prop2)

        item2 = self.createPropertySetItem()
        item2.addItemProperty(self._ID2, self._prop2)
        item2.addItemProperty(self._ID1, self._prop1)

        self.assertFalse(item1 == item2)


    def testEqualsSingleListener(self):
        item1 = self.createPropertySetItem()
        item2 = self.createPropertySetItem()

        item1.addListener(self._propertySetListenerMock)

        self.assertFalse(item1 == item2)
        self.assertFalse(item2 == item1)

        item2.addListener(self._propertySetListenerMock)

        self.assertTrue(item1 == item2)
        self.assertTrue(item2 == item1)


    def testEqualsMultipleListeners(self):
        item1 = self.createPropertySetItem()
        item2 = self.createPropertySetItem()

        item1.addListener(self._propertySetListenerMock)
        item1.addListener(self._propertySetListenerMock2)

        item2.addListener(self._propertySetListenerMock)

        self.assertFalse(item1 == item2)
        self.assertFalse(item2 == item1)

        item2.addListener(self._propertySetListenerMock2)

        self.assertTrue(item1 == item2)
        self.assertTrue(item2 == item1)


    def testEqualsAddRemoveListener(self):
        item1 = self.createPropertySetItem()
        item2 = self.createPropertySetItem()

        item1.addListener(self._propertySetListenerMock)
        item1.removeListener(self._propertySetListenerMock)

        self.assertTrue(item1 == item2)
        self.assertTrue(item2 == item1)


    def testItemHashCodeEmpty(self):
        item1 = self.createPropertySetItem()
        item2 = self.createPropertySetItem()

        self.assertEquals(item1.hashCode(), item2.hashCode())


    def testItemHashCodeAddProperties(self):
        item1 = self.createPropertySetItem()
        item2 = self.createPropertySetItem()

        self.assertEquals(item1.hashCode(), item2.hashCode())

        item1.addItemProperty(self._ID1, self._prop1)
        item1.addItemProperty(self._ID2, self._prop2)
        # hashCodes can be equal even if items are different

        item2.addItemProperty(self._ID1, self._prop1)
        item2.addItemProperty(self._ID2, self._prop2)
        # but here hashCodes must be equal
        self.assertEquals(item1.hashCode(), item2.hashCode())


    def testItemHashCodeAddListeners(self):
        item1 = self.createPropertySetItem()
        item2 = self.createPropertySetItem()

        self.assertEquals(item1.hashCode(), item2.hashCode())

        item1.addListener(self._propertySetListenerMock)
        # hashCodes can be equal even if items are different

        item2.addListener(self._propertySetListenerMock)
        # but here hashCodes must be equal
        self.assertEquals(item1.hashCode(), item2.hashCode())


    def testItemHashCodeAddRemoveProperty(self):
        item1 = self.createPropertySetItem()
        item2 = self.createPropertySetItem()

        item1.addItemProperty(self._ID1, self._prop1)
        item1.removeItemProperty(self._ID1)

        self.assertEquals(item1.hashCode(), item2.hashCode())


    def testItemHashCodeAddRemoveListener(self):
        item1 = self.createPropertySetItem()
        item2 = self.createPropertySetItem()

        item1.addListener(self._propertySetListenerMock)
        item1.removeListener(self._propertySetListenerMock)

        self.assertEquals(item1.hashCode(), item2.hashCode())


    def testToString(self):
        # toString() behavior is specified in the class javadoc
        item = self.createPropertySetItem()

        self.assertEquals('', str(item))

        item.addItemProperty(self._ID1, self._prop1)

        self.assertEquals(str(self._prop1), str(item))

        item.addItemProperty(self._ID2, self._prop2)

        self.assertEquals(str(self._prop1) + ' ' + str(self._prop2), str(item))
