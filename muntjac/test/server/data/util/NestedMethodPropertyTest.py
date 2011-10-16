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

import pickle

from unittest import TestCase

from muntjac.data.util.nested_method_property import NestedMethodProperty


class NestedMethodPropertyTest(TestCase):

    def setUp(self):
        self._oldMill = Address('Ruukinkatu 2-4', 20540)
        self._joonas = Person('Joonas', self._oldMill)
        self._vaadin = Team('Vaadin', self._joonas)


    def tearDown(self):
        self._vaadin = None
        self._joonas = None
        self._oldMill = None


    def testSingleLevelNestedSimpleProperty(self):
        nameProperty = NestedMethodProperty(self._vaadin, 'name')
        self.assertEquals(str, nameProperty.getType())
        self.assertEquals('Vaadin', nameProperty.getValue())


    def testSingleLevelNestedObjectProperty(self):
        managerProperty = NestedMethodProperty(self._vaadin, 'manager')
        self.assertEquals(Person, managerProperty.getType())
        self.assertEquals(self._joonas, managerProperty.getValue())


    def testMultiLevelNestedProperty(self):
        managerNameProperty = NestedMethodProperty(self._vaadin,
                'manager.name')
        addressProperty = NestedMethodProperty(self._vaadin,
                'manager.address')
        streetProperty = NestedMethodProperty(self._vaadin,
                'manager.address.street')
        postalCodePrimitiveProperty = NestedMethodProperty(self._vaadin,
                'manager.address.postalCodePrimitive')
        postalCodeObjectProperty = NestedMethodProperty(self._vaadin,
                'manager.address.postalCodeObject')
        booleanProperty = NestedMethodProperty(self._vaadin,
                'manager.address.boolean')

        self.assertEquals(str, managerNameProperty.getType())
        self.assertEquals('Joonas', managerNameProperty.getValue())

        self.assertEquals(Address, addressProperty.getType())
        self.assertEquals(self._oldMill, addressProperty.getValue())

        self.assertEquals(str, streetProperty.getType())
        self.assertEquals('Ruukinkatu 2-4', streetProperty.getValue())

        self.assertEquals(int, postalCodePrimitiveProperty.getType())
        self.assertEquals(20540, postalCodePrimitiveProperty.getValue())

        self.assertEquals(int, postalCodeObjectProperty.getType())
        self.assertEquals(20540, postalCodeObjectProperty.getValue())

        self.assertEquals(bool, booleanProperty.getType())
        self.assertEquals(True, booleanProperty.getValue())


    def testEmptyPropertyName(self):
        try:
            NestedMethodProperty(self._vaadin, '')
            self.fail()
        except ValueError:
            pass  # should get exception

        try:
            NestedMethodProperty(self._vaadin, ' ')
            self.fail()
        except ValueError:
            pass  # should get exception


    def testInvalidPropertyName(self):
        try:
            NestedMethodProperty(self._vaadin, '.')
            self.fail()
        except ValueError:
            pass  # should get exception

        try:
            NestedMethodProperty(self._vaadin, '.manager')
            self.fail()
        except ValueError:
            pass  # should get exception

        try:
            NestedMethodProperty(self._vaadin, 'manager.')
            self.fail()
        except ValueError:
            pass  # should get exception

        try:
            NestedMethodProperty(self._vaadin, 'manager..name')
            self.fail()
        except ValueError:
            pass  # should get exception


    def testInvalidNestedPropertyName(self):
        try:
            NestedMethodProperty(self._vaadin, 'member')
            self.fail()
        except ValueError:
            pass  # should get exception

        try:
            NestedMethodProperty(self._vaadin, 'manager.pet')
            self.fail()
        except ValueError:
            pass  # should get exception

        try:
            NestedMethodProperty(self._vaadin, 'manager.address.city')
            self.fail()
        except ValueError:
            pass  # should get exception


    def testNullNestedProperty(self):
        managerNameProperty = NestedMethodProperty(self._vaadin,
                'manager.name')
        streetProperty = NestedMethodProperty(self._vaadin,
                'manager.address.street')

        self._joonas.setAddress(None)
        try:
            streetProperty.getValue()
            self.fail()
        except Exception:
            pass  # should get exception

        self._vaadin.setManager(None)
        try:
            managerNameProperty.getValue()
            self.fail()
        except Exception:
            pass  # should get exception

        try:
            streetProperty.getValue()
            self.fail()
        except Exception:
            pass  # should get exception

        self._vaadin.setManager(self._joonas)
        self.assertEquals('Joonas', managerNameProperty.getValue())


    def testMultiLevelNestedPropertySetValue(self):
        managerNameProperty = NestedMethodProperty(self._vaadin,
                'manager.name')
        addressProperty = NestedMethodProperty(self._vaadin,
                'manager.address')
        streetProperty = NestedMethodProperty(self._vaadin,
                'manager.address.street')
        postalCodePrimitiveProperty = NestedMethodProperty(self._vaadin,
                'manager.address.postalCodePrimitive')
        postalCodeObjectProperty = NestedMethodProperty(self._vaadin,
                'manager.address.postalCodeObject')

        managerNameProperty.setValue('Joonas L')
        self.assertEquals('Joonas L', self._joonas.getName())
        streetProperty.setValue('Ruukinkatu')
        self.assertEquals('Ruukinkatu', self._oldMill.getStreet())
        postalCodePrimitiveProperty.setValue(0)
        postalCodeObjectProperty.setValue(1)
        self.assertEquals(0, self._oldMill.getPostalCodePrimitive())
        self.assertEquals(int(1), self._oldMill.getPostalCodeObject())

        postalCodeObjectProperty.setValue(None)
        self.assertNull(self._oldMill.getPostalCodeObject())

        address2 = self.Address('Other street', 12345)
        addressProperty.setValue(address2)
        self.assertEquals('Other street', streetProperty.getValue())


    def testSerialization(self):
        streetProperty = NestedMethodProperty(self._vaadin,
                'manager.address.street')
        baos = pickle.dumps(streetProperty)
        property2 = pickle.loads(baos)
        self.assertEquals('Ruukinkatu 2-4', property2.getValue())


    def testIsReadOnly(self):
        streetProperty = NestedMethodProperty(self._vaadin,
                'manager.address.street')
        booleanProperty = NestedMethodProperty(self._vaadin,
                'manager.address.boolean')
        self.assertFalse(streetProperty.isReadOnly())
        self.assertTrue(booleanProperty.isReadOnly())


class Address(object):

    def __init__(self, street, postalCode):
        self._street = street
        self._postalCodePrimitive = postalCode
        self._postalCodeObject = postalCode

    def setStreet(self, street):
        self._street = street

    def getStreet(self):
        return self._street

    def setPostalCodePrimitive(self, postalCodePrimitive):
        self._postalCodePrimitive = postalCodePrimitive

    def getPostalCodePrimitive(self):
        return self._postalCodePrimitive

    def setPostalCodeObject(self, postalCodeObject):
        self._postalCodeObject = postalCodeObject

    def getPostalCodeObject(self):
        # read-only boolean property
        return self._postalCodeObject

    def isBoolean(self):
        return True


class Person(object):

    def __init__(self, name, address):
        self._name = name
        self._address = address

    def setName(self, name):
        self._name = name

    def getName(self):
        return self._name

    def setAddress(self, address):
        self._address = address

    def getAddress(self):
        return self._address


class Team(object):

    def __init__(self, name, manager):
        self._name = name
        self._manager = manager

    def setName(self, name):
        self._name = name

    def getName(self):
        return self._name

    def setManager(self, manager):
        self._manager = manager

    def getManager(self):
        return self._manager
