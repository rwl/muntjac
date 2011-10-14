# -*- coding: utf-8 -*-
from __pyjamas__ import (ARGERROR, POSTDEC, POSTINC,)
# from com.vaadin.data.util.BeanItemContainer import (BeanItemContainer,)
# from com.vaadin.data.util.DefaultItemSorter import (DefaultItemSorter,)
# from java.util.Arrays import (Arrays,)
# from java.util.Collections import (Collections,)
# from java.util.HashSet import (HashSet,)
# from java.util.Set import (Set,)
# from junit.framework.Assert import (Assert,)
# from org.junit.Test import (Test,)


class BeanItemContainerSortTest(object):

    class Person(object):
        _name = None

        def getAge(self):
            return self._age

        def setAge(self, age):
            self._age = age

        _age = None

        def setName(self, name):
            self._name = name

        def getName(self):
            return self._name

    class Parent(Person):
        _children = set()

        def setChildren(self, children):
            self._children = children

        def getChildren(self):
            return self._children

    _names = ['Antti', 'Ville', 'Sirkka', 'Jaakko', 'Pekka', 'John']
    _ages = [10, 20, 50, 12, 64, 67]
    _sortedByAge = [_names[0], _names[3], _names[1], _names[2], _names[4], _names[5]]

    def getContainer(self):
        bc = BeanItemContainer(self.Person)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(self._names)):
                break
            p = self.Person()
            p.setName(self._names[i])
            p.setAge(self._ages[i])
            bc.addBean(p)
        return bc

    def getParentContainer(self):
        bc = BeanItemContainer(self.Parent)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(self._names)):
                break
            p = self.Parent()
            p.setName(self._names[i])
            p.setAge(self._ages[i])
            bc.addBean(p)
        return bc

    def testSort(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.testSort(True)
        elif _1 == 1:
            b, = _0
            container = self.getContainer()
            container.sort(['name'], [b])
            asList = Arrays.asList(self._names)
            Collections.sort(asList)
            if not b:
                Collections.reverse(asList)
            i = 0
            for string in asList:
                idByIndex = container.getIdByIndex(POSTINC(globals(), locals(), 'i'))
                Assert.assertTrue(container.containsId(idByIndex))
                Assert.assertEquals(string, idByIndex.getName())
        else:
            raise ARGERROR(0, 1)

    def testReverseSort(self):
        self.testSort(False)

    def primitiveSorting(self):
        container = self.getContainer()
        container.sort(['age'], [True])
        i = 0
        for string in self._sortedByAge:
            idByIndex = container.getIdByIndex(POSTINC(globals(), locals(), 'i'))
            Assert.assertTrue(container.containsId(idByIndex))
            Assert.assertEquals(string, idByIndex.getName())

    def customSorting(self):
        container = self.getContainer()
        # custom sorter using the reverse order

        class _0_(DefaultItemSorter):

            def compare(self, o1, o2):
                return -super(_0_, self).compare(o1, o2)

        _0_ = _0_()
        container.setItemSorter(_0_)
        container.sort(['age'], [True])
        i = len(container) - 1
        for string in self._sortedByAge:
            idByIndex = container.getIdByIndex(POSTDEC(globals(), locals(), 'i'))
            Assert.assertTrue(container.containsId(idByIndex))
            Assert.assertEquals(string, idByIndex.getName())

    def testGetSortableProperties(self):
        container = self.getContainer()
        sortablePropertyIds = container.getSortableContainerPropertyIds()
        Assert.assertEquals(2, len(sortablePropertyIds))
        Assert.assertTrue(sortablePropertyIds.contains('name'))
        Assert.assertTrue(sortablePropertyIds.contains('age'))

    def testGetNonSortableProperties(self):
        container = self.getParentContainer()
        Assert.assertEquals(3, len(container.getContainerPropertyIds()))
        sortablePropertyIds = container.getSortableContainerPropertyIds()
        Assert.assertEquals(2, len(sortablePropertyIds))
        Assert.assertTrue(sortablePropertyIds.contains('name'))
        Assert.assertTrue(sortablePropertyIds.contains('age'))
