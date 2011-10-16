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

from muntjac.data.util.bean_item_container import BeanItemContainer
from muntjac.data.util.default_item_sorter import DefaultItemSorter


class Person(object):

    def __init__(self):
        self._name = None
        self._age = None

    def getAge(self):
        return self._age

    def setAge(self, age):
        self._age = age

    def setName(self, name):
        self._name = name

    def getName(self):
        return self._name


class Parent(Person):

    def __init__(self):
        self._children = set()

    def setChildren(self, children):
        self._children = children

    def getChildren(self):
        return self._children


class BeanItemContainerSortTest(TestCase):

    def __init__(self):
        self._names = ['Antti', 'Ville', 'Sirkka', 'Jaakko', 'Pekka', 'John']
        self._ages = [10, 20, 50, 12, 64, 67]
        self._sortedByAge = [self._names[0], self._names[3], self._names[1],
                             self._names[2], self._names[4], self._names[5]]

    def getContainer(self):
        bc = BeanItemContainer(Person)
        for i in range(len(self._names)):
            p = Person()
            p.setName(self._names[i])
            p.setAge(self._ages[i])
            bc.addBean(p)
        return bc


    def getParentContainer(self):
        bc = BeanItemContainer(Parent)
        for i in range(len(self._names)):
            p = Parent()
            p.setName(self._names[i])
            p.setAge(self._ages[i])
            bc.addBean(p)
        return bc


    def testSort(self, b=True):
        container = self.getContainer()
        container.sort(['name'], [b])
        asList = list(self._names)
        asList.sort()  # FIXME: sort
        if not b:
            asList[::-1]  # reverse
        i = 0
        for string in asList:
            idByIndex = container.getIdByIndex(i)
            i += 1
            self.assertTrue(container.containsId(idByIndex))
            self.assertEquals(string, idByIndex.getName())


    def testReverseSort(self):
        self.testSort(False)


    def primitiveSorting(self):
        container = self.getContainer()
        container.sort(['age'], [True])

        i = 0
        for string in self._sortedByAge:
            idByIndex = container.getIdByIndex(i)
            i += 1
            self.assertTrue(container.containsId(idByIndex))
            self.assertEquals(string, idByIndex.getName())


    def customSorting(self):
        container = self.getContainer()

        # custom sorter using the reverse order
        class ReverseSorter(DefaultItemSorter):

            def compare(self, o1, o2):
                return -super(ReverseSorter, self).compare(o1, o2)

        container.setItemSorter(ReverseSorter())

        container.sort(['age'], [True])

        i = len(container) - 1
        for string in self._sortedByAge:
            idByIndex = container.getIdByIndex(i)
            i -= 1
            self.assertTrue(container.containsId(idByIndex))
            self.assertEquals(string, idByIndex.getName())


    def testGetSortableProperties(self):
        container = self.getContainer()

        sortablePropertyIds = container.getSortableContainerPropertyIds()
        self.assertEquals(2, len(sortablePropertyIds))
        self.assertTrue('name' in sortablePropertyIds)
        self.assertTrue('age' in sortablePropertyIds)


    def testGetNonSortableProperties(self):
        container = self.getParentContainer()

        self.assertEquals(3, len(container.getContainerPropertyIds()))

        sortablePropertyIds = container.getSortableContainerPropertyIds()
        self.assertEquals(2, len(sortablePropertyIds))
        self.assertTrue('name' in sortablePropertyIds)
        self.assertTrue('age' in sortablePropertyIds)
