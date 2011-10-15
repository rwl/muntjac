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

# from com.vaadin.data.util.NestedMethodProperty import (NestedMethodProperty,)
# from java.io.ByteArrayInputStream import (ByteArrayInputStream,)
# from java.io.ByteArrayOutputStream import (ByteArrayOutputStream,)
# from java.io.IOException import (IOException,)
# from java.io.ObjectInputStream import (ObjectInputStream,)
# from java.io.ObjectOutputStream import (ObjectOutputStream,)
# from java.io.Serializable import (Serializable,)
# from junit.framework.Assert import (Assert,)
# from junit.framework.TestCase import (TestCase,)


class NestedMethodPropertyTest(TestCase):

    class Address(Serializable):
        _street = None
        _postalCodePrimitive = None
        _postalCodeObject = None

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

    class Person(Serializable):
        _name = None
        _address = None

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

    class Team(Serializable):
        _name = None
        _manager = None

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

    _oldMill = None
    _joonas = None
    _vaadin = None

    def setUp(self):
        self._oldMill = self.Address('Ruukinkatu 2-4', 20540)
        self._joonas = self.Person('Joonas', self._oldMill)
        self._vaadin = self.Team('Vaadin', self._joonas)

    def tearDown(self):
        self._vaadin = None
        self._joonas = None
        self._oldMill = None

    def testSingleLevelNestedSimpleProperty(self):
        nameProperty = NestedMethodProperty(self._vaadin, 'name')
        Assert.assertEquals(str, nameProperty.getType())
        Assert.assertEquals('Vaadin', nameProperty.getValue())

    def testSingleLevelNestedObjectProperty(self):
        managerProperty = NestedMethodProperty(self._vaadin, 'manager')
        Assert.assertEquals(self.Person, managerProperty.getType())
        Assert.assertEquals(self._joonas, managerProperty.getValue())

    def testMultiLevelNestedProperty(self):
        managerNameProperty = NestedMethodProperty(self._vaadin, 'manager.name')
        addressProperty = NestedMethodProperty(self._vaadin, 'manager.address')
        streetProperty = NestedMethodProperty(self._vaadin, 'manager.address.street')
        postalCodePrimitiveProperty = NestedMethodProperty(self._vaadin, 'manager.address.postalCodePrimitive')
        postalCodeObjectProperty = NestedMethodProperty(self._vaadin, 'manager.address.postalCodeObject')
        booleanProperty = NestedMethodProperty(self._vaadin, 'manager.address.boolean')
        Assert.assertEquals(str, managerNameProperty.getType())
        Assert.assertEquals('Joonas', managerNameProperty.getValue())
        Assert.assertEquals(self.Address, addressProperty.getType())
        Assert.assertEquals(self._oldMill, addressProperty.getValue())
        Assert.assertEquals(str, streetProperty.getType())
        Assert.assertEquals('Ruukinkatu 2-4', streetProperty.getValue())
        Assert.assertEquals(int, postalCodePrimitiveProperty.getType())
        Assert.assertEquals(20540, postalCodePrimitiveProperty.getValue())
        Assert.assertEquals(int, postalCodeObjectProperty.getType())
        Assert.assertEquals(20540, postalCodeObjectProperty.getValue())
        Assert.assertEquals(bool, booleanProperty.getType())
        Assert.assertEquals(True, booleanProperty.getValue())

    def testEmptyPropertyName(self):
        # should get exception
        try:
            NestedMethodProperty(self._vaadin, '')
            self.fail()
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]
        # should get exception
        try:
            NestedMethodProperty(self._vaadin, ' ')
            self.fail()
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]

    def testInvalidPropertyName(self):
        # should get exception
        try:
            NestedMethodProperty(self._vaadin, '.')
            self.fail()
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]
        # should get exception
        try:
            NestedMethodProperty(self._vaadin, '.manager')
            self.fail()
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]
        # should get exception
        try:
            NestedMethodProperty(self._vaadin, 'manager.')
            self.fail()
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]
        # should get exception
        try:
            NestedMethodProperty(self._vaadin, 'manager..name')
            self.fail()
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]

    def testInvalidNestedPropertyName(self):
        # should get exception
        try:
            NestedMethodProperty(self._vaadin, 'member')
            self.fail()
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]
        # should get exception
        try:
            NestedMethodProperty(self._vaadin, 'manager.pet')
            self.fail()
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]
        # should get exception
        try:
            NestedMethodProperty(self._vaadin, 'manager.address.city')
            self.fail()
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]

    def testNullNestedProperty(self):
        managerNameProperty = NestedMethodProperty(self._vaadin, 'manager.name')
        streetProperty = NestedMethodProperty(self._vaadin, 'manager.address.street')
        self._joonas.setAddress(None)
        # should get exception
        try:
            streetProperty.getValue()
            self.fail()
        except Exception, e:
            pass # astStmt: [Stmt([]), None]
        self._vaadin.setManager(None)
        # should get exception
        try:
            managerNameProperty.getValue()
            self.fail()
        except Exception, e:
            pass # astStmt: [Stmt([]), None]
        # should get exception
        try:
            streetProperty.getValue()
            self.fail()
        except Exception, e:
            pass # astStmt: [Stmt([]), None]
        self._vaadin.setManager(self._joonas)
        Assert.assertEquals('Joonas', managerNameProperty.getValue())

    def testMultiLevelNestedPropertySetValue(self):
        managerNameProperty = NestedMethodProperty(self._vaadin, 'manager.name')
        addressProperty = NestedMethodProperty(self._vaadin, 'manager.address')
        streetProperty = NestedMethodProperty(self._vaadin, 'manager.address.street')
        postalCodePrimitiveProperty = NestedMethodProperty(self._vaadin, 'manager.address.postalCodePrimitive')
        postalCodeObjectProperty = NestedMethodProperty(self._vaadin, 'manager.address.postalCodeObject')
        managerNameProperty.setValue('Joonas L')
        Assert.assertEquals('Joonas L', self._joonas.getName())
        streetProperty.setValue('Ruukinkatu')
        Assert.assertEquals('Ruukinkatu', self._oldMill.getStreet())
        postalCodePrimitiveProperty.setValue(0)
        postalCodeObjectProperty.setValue(1)
        Assert.assertEquals(0, self._oldMill.getPostalCodePrimitive())
        Assert.assertEquals(Integer.valueOf.valueOf(1), self._oldMill.getPostalCodeObject())
        postalCodeObjectProperty.setValue(None)
        Assert.assertNull(self._oldMill.getPostalCodeObject())
        address2 = self.Address('Other street', 12345)
        addressProperty.setValue(address2)
        Assert.assertEquals('Other street', streetProperty.getValue())

    def testSerialization(self):
        streetProperty = NestedMethodProperty(self._vaadin, 'manager.address.street')
        baos = ByteArrayOutputStream()
        ObjectOutputStream(baos).writeObject(streetProperty)
        property2 = ObjectInputStream(ByteArrayInputStream(baos.toByteArray())).readObject()
        Assert.assertEquals('Ruukinkatu 2-4', property2.getValue())

    def testIsReadOnly(self):
        streetProperty = NestedMethodProperty(self._vaadin, 'manager.address.street')
        booleanProperty = NestedMethodProperty(self._vaadin, 'manager.address.boolean')
        Assert.assertFalse(streetProperty.isReadOnly())
        Assert.assertTrue(booleanProperty.isReadOnly())
