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

from muntjac.data.util.bean_item import BeanItem

from muntjac.data.util.method_property_descriptor import \
    MethodPropertyDescriptor


class BeanItemTest(TestCase):
    """Test BeanItem specific features.

    Only public API is tested, not the methods with package visibility.

    See also L{PropertySetItemTest}, which tests the base class.
    """

    def testGetProperties(self):
        item = BeanItem(MySuperClass())
        itemPropertyIds = item.getItemPropertyIds()
        self.assertEquals(3, len(itemPropertyIds))
        self.assertTrue('superPrivate' in itemPropertyIds)
        self.assertTrue('superProtected' in itemPropertyIds)
        self.assertTrue('superPublic' in itemPropertyIds)


    def testGetSuperClassProperties(self):
        item = BeanItem(self.MyClass('bean1'))
        itemPropertyIds = item.getItemPropertyIds()
        self.assertEquals(6, len(itemPropertyIds))
        self.assertTrue('superPrivate' in itemPropertyIds)
        self.assertTrue('superProtected' in itemPropertyIds)
        self.assertTrue('superPublic' in itemPropertyIds)
        self.assertTrue('name' in itemPropertyIds)
        self.assertTrue('noField' in itemPropertyIds)
        self.assertTrue('name2' in itemPropertyIds)


    def testOverridingProperties(self):
        item = BeanItem(MyClass2('bean2'))

        itemPropertyIds = item.getItemPropertyIds()
        self.assertEquals(6, len(itemPropertyIds))

        self.assertTrue(MyClass2 == item.getBean().__class__)

        # check that name2 accessed via MyClass2, not MyClass
        self.assertFalse(item.getItemProperty('name2').isReadOnly())


    def testGetInterfaceProperties(self):
        method = getattr(BeanItem, 'getPropertyDescriptors')
        method.setAccessible(True)
        propertyDescriptors = method(None, MySuperInterface)

        self.assertEquals(2, len(propertyDescriptors))
        self.assertTrue('super1' in propertyDescriptors)
        self.assertTrue('override' in propertyDescriptors)

        prop = propertyDescriptors.get('override').createProperty(
                self.__class__)
        self.assertTrue(prop.isReadOnly())


    def testGetSuperInterfaceProperties(self):
        method = getattr(BeanItem, 'getPropertyDescriptors')
        method.setAccessible(True)
        propertyDescriptors = method(None, MySubInterface)

        self.assertEquals(4, len(propertyDescriptors))
        self.assertTrue('sub' in propertyDescriptors)
        self.assertTrue('super1' in propertyDescriptors)
        self.assertTrue('super2' in propertyDescriptors)
        self.assertTrue('override' in propertyDescriptors)

        prop = propertyDescriptors.get('override').createProperty(
                self.__class__)
        self.assertFalse(prop.isReadOnly())


    def testPropertyExplicitOrder(self):
        ids = list()
        ids.append('name')
        ids.append('superPublic')
        ids.append('name2')
        ids.append('noField')

        item = BeanItem(MyClass('bean1'), ids)

        it = iter(item.getItemPropertyIds())
        self.assertEquals('name', it.next())
        self.assertEquals('superPublic', it.next())
        self.assertEquals('name2', it.next())
        self.assertEquals('noField', it.next())
        self.assertFalse(it.hasNext())


    def testPropertyExplicitOrder2(self):
        item = BeanItem(MyClass('bean1'),
                ['name', 'superPublic', 'name2', 'noField'])

        it = iter(item.getItemPropertyIds())
        self.assertEquals('name', it.next())
        self.assertEquals('superPublic', it.next())
        self.assertEquals('name2', it.next())
        self.assertEquals('noField', it.next())
        self.assertFalse(it.hasNext())


    def testPropertyBadPropertyName(self):
        ids = list()
        ids.append('name3')
        ids.append('name')

        # currently silently ignores non-existent properties
        item = BeanItem(MyClass('bean1'), ids)

        it = iter(item.getItemPropertyIds())
        self.assertEquals('name', it.next())
        self.assertFalse(it.hasNext())


    def testRemoveProperty(self):
        item = BeanItem(MyClass('bean1'))

        itemPropertyIds = item.getItemPropertyIds()
        self.assertEquals(6, len(itemPropertyIds))

        item.removeItemProperty('name2')
        self.assertEquals(5, len(itemPropertyIds))
        self.assertFalse(itemPropertyIds.contains('name2'))


    def testRemoveSuperProperty(self):
        item = BeanItem(MyClass('bean1'))

        itemPropertyIds = item.getItemPropertyIds()
        self.assertEquals(6, len(itemPropertyIds))

        item.removeItemProperty('superPrivate')
        self.assertEquals(5, len(itemPropertyIds))
        self.assertFalse(itemPropertyIds.contains('superPrivate'))


    def testPropertyTypes(self):
        item = BeanItem(MyClass('bean1'))

        self.assertTrue(int == item.getItemProperty('superPrivate').getType())
        self.assertTrue(float == item.getItemProperty('superProtected').getType())
        self.assertTrue(bool == item.getItemProperty('superPublic').getType())
        self.assertTrue(str == item.getItemProperty('name').getType())


    def testPropertyReadOnly(self):
        item = BeanItem(MyClass('bean1'))
        self.assertFalse(item.getItemProperty('name').isReadOnly())
        self.assertTrue(item.getItemProperty('name2').isReadOnly())


    def testCustomProperties(self):
        propertyDescriptors = dict()
        mpd = MethodPropertyDescriptor('myname', MyClass,
                getattr(MyClass, 'getName'), getattr(MyClass, 'setName'))
        propertyDescriptors['myname'] = mpd
        instance = MyClass('bean1')
        constructor = getattr(BeanItem, '__init__')
        constructor.setAccessible(True)
        item = constructor(instance, propertyDescriptors)

        self.assertEquals(1, len(item.getItemPropertyIds()))
        self.assertEquals('bean1', item.getItemProperty('myname').getValue())


    def testAddRemoveProperty(self):
        pd = MethodPropertyDescriptor('myname', MyClass,
                getattr(MyClass, 'getName'),
                getattr(MyClass, 'setName'))
        item = BeanItem(self.MyClass('bean1'))
        self.assertEquals(6, len(item.getItemPropertyIds()))
        self.assertEquals(None, item.getItemProperty('myname'))

        item.addItemProperty('myname', pd.createProperty(item.getBean()))
        self.assertEquals(7, len(item.getItemPropertyIds()))
        self.assertEquals('bean1', item.getItemProperty('myname').getValue())
        item.removeItemProperty('myname')
        self.assertEquals(6, len(item.getItemPropertyIds()))
        self.assertEquals(None, item.getItemProperty('myname'))


class MySuperClass(object):

    def __init__(self):
        self._superPrivate = 1
        self._superPrivate2 = 2
        self.superProtected = 3.0
        self._superProtected2 = 4.0
        self.superPublic = True
        self._superPublic2 = True

    def getSuperPrivate(self):
        return self._superPrivate

    def setSuperPrivate(self, superPrivate):
        self._superPrivate = superPrivate

    def getSuperProtected(self):
        return self.superProtected

    def setSuperProtected(self, superProtected):
        self.superProtected = superProtected

    def isSuperPublic(self):
        return self.superPublic

    def setSuperPublic(self, superPublic):
        self.superPublic = superPublic


class MyClass(MySuperClass):

    def __init__(self, name):
        self._name = name
        self.value = 123

    def setName(self, name):
        self._name = name

    def getName(self):
        return self._name

    def setNoField(self, name):
        pass

    def getNoField(self):
        return 'no field backing this setter'

    def getName2(self):
        return self._name


class MyClass2(MyClass):

    def __init__(self, name):
        super(MyClass2, self)(name)

    def setName(self, name):
        super(MyClass2, self).setName(name + '2')

    def getName(self):
        return super(MyClass2, self).getName() + '2'

    def getName2(self):
        return super(MyClass2, self).getName()

    def setName2(self, name):
        super(MyClass2, self).setName(name)


class MySuperInterface(object):

    def getSuper1(self):
        pass

    def setSuper1(self, i):
        pass

    def getOverride(self):
        pass


class MySuperInterface2(object):

    def getSuper2(self):
        pass


class MySubInterface(MySuperInterface, MySuperInterface2):

    def getSub(self):
        pass

    def setSub(self, i):
        pass

    def getOverride(self):
        pass

    def setOverride(self, i):
        pass
