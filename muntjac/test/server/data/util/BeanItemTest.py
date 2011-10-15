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

# from com.vaadin.data.util.BeanItem import (BeanItem,)
# from com.vaadin.data.util.MethodProperty import (MethodProperty,)
# from com.vaadin.data.util.MethodPropertyDescriptor import (MethodPropertyDescriptor,)
# from com.vaadin.data.util.VaadinPropertyDescriptor import (VaadinPropertyDescriptor,)
# from java.lang.reflect.Constructor import (Constructor,)
# from java.lang.reflect.InvocationTargetException import (InvocationTargetException,)
# from java.lang.reflect.Method import (Method,)
# from junit.framework.Assert import (Assert,)
# from junit.framework.TestCase import (TestCase,)


class BeanItemTest(TestCase):
    """Test BeanItem specific features.

    Only public API is tested, not the methods with package visibility.

    See also {@link PropertySetItemTest}, which tests the base class.
    """

    class MySuperClass(object):
        _superPrivate = 1
        _superPrivate2 = 2
        superProtected = 3.0
        _superProtected2 = 4.0
        superPublic = True
        _superPublic2 = True

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
        _name = None
        value = 123

        def __init__(self, name):
            self._name = name

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

    def testGetProperties(self):
        item = BeanItem(self.MySuperClass())
        itemPropertyIds = item.getItemPropertyIds()
        Assert.assertEquals(3, len(itemPropertyIds))
        Assert.assertTrue(itemPropertyIds.contains('superPrivate'))
        Assert.assertTrue(itemPropertyIds.contains('superProtected'))
        Assert.assertTrue(itemPropertyIds.contains('superPublic'))

    def testGetSuperClassProperties(self):
        item = BeanItem(self.MyClass('bean1'))
        itemPropertyIds = item.getItemPropertyIds()
        Assert.assertEquals(6, len(itemPropertyIds))
        Assert.assertTrue(itemPropertyIds.contains('superPrivate'))
        Assert.assertTrue(itemPropertyIds.contains('superProtected'))
        Assert.assertTrue(itemPropertyIds.contains('superPublic'))
        Assert.assertTrue(itemPropertyIds.contains('name'))
        Assert.assertTrue(itemPropertyIds.contains('noField'))
        Assert.assertTrue(itemPropertyIds.contains('name2'))

    def testOverridingProperties(self):
        item = BeanItem(self.MyClass2('bean2'))
        itemPropertyIds = item.getItemPropertyIds()
        Assert.assertEquals(6, len(itemPropertyIds))
        Assert.assertTrue(self.MyClass2 == item.getBean().getClass())
        # check that name2 accessed via MyClass2, not MyClass
        Assert.assertFalse(item.getItemProperty('name2').isReadOnly())

    def testGetInterfaceProperties(self):
        method = BeanItem.getDeclaredMethod('getPropertyDescriptors', self.Class)
        method.setAccessible(True)
        propertyDescriptors = method.invoke(None, self.MySuperInterface)
        Assert.assertEquals(2, len(propertyDescriptors))
        Assert.assertTrue('super1' in propertyDescriptors)
        Assert.assertTrue('override' in propertyDescriptors)
        property = propertyDescriptors.get('override').createProperty(self.getClass())
        Assert.assertTrue(property.isReadOnly())

    def testGetSuperInterfaceProperties(self):
        method = BeanItem.getDeclaredMethod('getPropertyDescriptors', self.Class)
        method.setAccessible(True)
        propertyDescriptors = method.invoke(None, self.MySubInterface)
        Assert.assertEquals(4, len(propertyDescriptors))
        Assert.assertTrue('sub' in propertyDescriptors)
        Assert.assertTrue('super1' in propertyDescriptors)
        Assert.assertTrue('super2' in propertyDescriptors)
        Assert.assertTrue('override' in propertyDescriptors)
        property = propertyDescriptors.get('override').createProperty(self.getClass())
        Assert.assertFalse(property.isReadOnly())

    def testPropertyExplicitOrder(self):
        ids = list()
        ids.add('name')
        ids.add('superPublic')
        ids.add('name2')
        ids.add('noField')
        item = BeanItem(self.MyClass('bean1'), ids)
        it = item.getItemPropertyIds()
        Assert.assertEquals('name', it.next())
        Assert.assertEquals('superPublic', it.next())
        Assert.assertEquals('name2', it.next())
        Assert.assertEquals('noField', it.next())
        Assert.assertFalse(it.hasNext())

    def testPropertyExplicitOrder2(self):
        item = BeanItem(self.MyClass('bean1'), ['name', 'superPublic', 'name2', 'noField'])
        it = item.getItemPropertyIds()
        Assert.assertEquals('name', it.next())
        Assert.assertEquals('superPublic', it.next())
        Assert.assertEquals('name2', it.next())
        Assert.assertEquals('noField', it.next())
        Assert.assertFalse(it.hasNext())

    def testPropertyBadPropertyName(self):
        ids = list()
        ids.add('name3')
        ids.add('name')
        # currently silently ignores non-existent properties
        item = BeanItem(self.MyClass('bean1'), ids)
        it = item.getItemPropertyIds()
        Assert.assertEquals('name', it.next())
        Assert.assertFalse(it.hasNext())

    def testRemoveProperty(self):
        item = BeanItem(self.MyClass('bean1'))
        itemPropertyIds = item.getItemPropertyIds()
        Assert.assertEquals(6, len(itemPropertyIds))
        item.removeItemProperty('name2')
        Assert.assertEquals(5, len(itemPropertyIds))
        Assert.assertFalse(itemPropertyIds.contains('name2'))

    def testRemoveSuperProperty(self):
        item = BeanItem(self.MyClass('bean1'))
        itemPropertyIds = item.getItemPropertyIds()
        Assert.assertEquals(6, len(itemPropertyIds))
        item.removeItemProperty('superPrivate')
        Assert.assertEquals(5, len(itemPropertyIds))
        Assert.assertFalse(itemPropertyIds.contains('superPrivate'))

    def testPropertyTypes(self):
        item = BeanItem(self.MyClass('bean1'))
        Assert.assertTrue(int == item.getItemProperty('superPrivate').getType())
        Assert.assertTrue(float == item.getItemProperty('superProtected').getType())
        Assert.assertTrue(bool == item.getItemProperty('superPublic').getType())
        Assert.assertTrue(str == item.getItemProperty('name').getType())

    def testPropertyReadOnly(self):
        item = BeanItem(self.MyClass('bean1'))
        Assert.assertFalse(item.getItemProperty('name').isReadOnly())
        Assert.assertTrue(item.getItemProperty('name2').isReadOnly())

    def testCustomProperties(self):
        propertyDescriptors = LinkedHashMap()
        propertyDescriptors.put('myname', MethodPropertyDescriptor('myname', self.MyClass, self.MyClass.getDeclaredMethod('getName'), self.MyClass.getDeclaredMethod('setName', str)))
        instance = self.MyClass('bean1')
        constructor = BeanItem.getDeclaredConstructor(self.Object, dict)
        constructor.setAccessible(True)
        item = constructor(instance, propertyDescriptors)
        Assert.assertEquals(1, len(item.getItemPropertyIds()))
        Assert.assertEquals('bean1', item.getItemProperty('myname').getValue())

    def testAddRemoveProperty(self):
        pd = MethodPropertyDescriptor('myname', self.MyClass, self.MyClass.getDeclaredMethod('getName'), self.MyClass.getDeclaredMethod('setName', str))
        item = BeanItem(self.MyClass('bean1'))
        Assert.assertEquals(6, len(item.getItemPropertyIds()))
        Assert.assertEquals(None, item.getItemProperty('myname'))
        item.addItemProperty('myname', pd.createProperty(item.getBean()))
        Assert.assertEquals(7, len(item.getItemPropertyIds()))
        Assert.assertEquals('bean1', item.getItemProperty('myname').getValue())
        item.removeItemProperty('myname')
        Assert.assertEquals(6, len(item.getItemPropertyIds()))
        Assert.assertEquals(None, item.getItemProperty('myname'))
