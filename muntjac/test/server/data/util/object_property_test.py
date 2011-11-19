# Copyright (C) 2011 Vaadin Ltd.
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


class ObjectPropertyTest(TestCase):

    def setUp(self):
        TestCase.setUp(self)

        self._super1 = TestSuperClass('super1')
        self._sub1 = TestSubClass('sub1')


    def testSimple(self):
        prop1 = ObjectProperty(self._super1, TestSuperClass)
        self.assertEquals('super1', prop1.getValue().getName())
        prop1 = ObjectProperty(self._super1)
        self.assertEquals('super1', prop1.getValue().getName())
        prop2 = ObjectProperty(self._sub1, TestSubClass)
        self.assertEquals('Subclass: sub1', prop2.getValue().getName())
        prop2 = ObjectProperty(self._sub1)
        self.assertEquals('Subclass: sub1', prop2.getValue().getName())


    def testSetValueObjectSuper(self):
        prop = ObjectProperty(self._super1, TestSuperClass)
        self.assertEquals('super1', prop.getValue().getName())
        prop.setValue(TestSuperClass('super2'))
        self.assertEquals('super1', self._super1.getName())
        self.assertEquals('super2', prop.getValue().getName())


    def testSetValueObjectSub(self):
        prop = ObjectProperty(self._sub1, TestSubClass)
        self.assertEquals('Subclass: sub1', prop.getValue().getName())
        prop.setValue(TestSubClass('sub2'))
        self.assertEquals('Subclass: sub1', self._sub1.getName())
        self.assertEquals('Subclass: sub2', prop.getValue().getName())


    def testSetValueStringSuper(self):
        prop = ObjectProperty(self._super1, TestSuperClass)
        self.assertEquals('super1', prop.getValue().getName())
        prop.setValue('super2')
        self.assertEquals('super1', self._super1.getName())
        self.assertEquals('super2', prop.getValue().getName())


    def testSetValueStringSub(self):
        prop = ObjectProperty(self._sub1, TestSubClass)
        self.assertEquals('Subclass: sub1', prop.getValue().getName())
        prop.setValue('sub2')
        self.assertEquals('Subclass: sub1', self._sub1.getName())
        self.assertEquals('Subclass: sub2', prop.getValue().getName())


    def testMixedGenerics(self):
        prop = ObjectProperty(self._sub1)
        self.assertEquals('Subclass: sub1', prop.getValue().getName())
        self.assertEquals(prop.getType(), TestSubClass)
        # create correct subclass based on the runtime type of the instance
        # given to ObjectProperty constructor, which is a subclass of the type
        # parameter
        prop.setValue('sub2')
        self.assertEquals('Subclass: sub2', prop.getValue().getName())


class TestSuperClass(object):

    def __init__(self, name):
        self._name = name

    def getName(self):
        return self._name

    def __str__(self):
        return self.getName()


class TestSubClass(TestSuperClass):

    def __init__(self, name):
        super(TestSubClass, self).__init__('Subclass: ' + name)
