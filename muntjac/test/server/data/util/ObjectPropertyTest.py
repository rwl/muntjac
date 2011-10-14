# -*- coding: utf-8 -*-
# from junit.framework.TestCase import (TestCase,)
# from org.junit.Assert import (Assert,)


class ObjectPropertyTest(TestCase):

    class TestSuperClass(object):
        _name = None

        def __init__(self, name):
            self._name = name

        def getName(self):
            return self._name

        def toString(self):
            return self.getName()

    class TestSubClass(TestSuperClass):

        def __init__(self, name):
            super(TestSubClass, self)('Subclass: ' + name)

    _super1 = TestSuperClass('super1')
    _sub1 = TestSubClass('sub1')

    def testSimple(self):
        prop1 = ObjectProperty(self._super1, self.TestSuperClass)
        Assert.assertEquals('super1', prop1.getValue().getName())
        prop1 = ObjectProperty(self._super1)
        Assert.assertEquals('super1', prop1.getValue().getName())
        prop2 = ObjectProperty(self._sub1, self.TestSubClass)
        Assert.assertEquals('Subclass: sub1', prop2.getValue().getName())
        prop2 = ObjectProperty(self._sub1)
        Assert.assertEquals('Subclass: sub1', prop2.getValue().getName())

    def testSetValueObjectSuper(self):
        prop = ObjectProperty(self._super1, self.TestSuperClass)
        Assert.assertEquals('super1', prop.getValue().getName())
        prop.setValue(self.TestSuperClass('super2'))
        Assert.assertEquals('super1', self._super1.getName())
        Assert.assertEquals('super2', prop.getValue().getName())

    def testSetValueObjectSub(self):
        prop = ObjectProperty(self._sub1, self.TestSubClass)
        Assert.assertEquals('Subclass: sub1', prop.getValue().getName())
        prop.setValue(self.TestSubClass('sub2'))
        Assert.assertEquals('Subclass: sub1', self._sub1.getName())
        Assert.assertEquals('Subclass: sub2', prop.getValue().getName())

    def testSetValueStringSuper(self):
        prop = ObjectProperty(self._super1, self.TestSuperClass)
        Assert.assertEquals('super1', prop.getValue().getName())
        prop.setValue('super2')
        Assert.assertEquals('super1', self._super1.getName())
        Assert.assertEquals('super2', prop.getValue().getName())

    def testSetValueStringSub(self):
        prop = ObjectProperty(self._sub1, self.TestSubClass)
        Assert.assertEquals('Subclass: sub1', prop.getValue().getName())
        prop.setValue('sub2')
        Assert.assertEquals('Subclass: sub1', self._sub1.getName())
        Assert.assertEquals('Subclass: sub2', prop.getValue().getName())

    def testMixedGenerics(self):
        prop = ObjectProperty(self._sub1)
        Assert.assertEquals('Subclass: sub1', prop.getValue().getName())
        Assert.assertEquals(prop.getType(), self.TestSubClass)
        # create correct subclass based on the runtime type of the instance
        # given to ObjectProperty constructor, which is a subclass of the type
        # parameter
        prop.setValue('sub2')
        Assert.assertEquals('Subclass: sub2', prop.getValue().getName())
