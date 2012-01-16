# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

from unittest import TestCase
from muntjac.data.util.indexed_container import IndexedContainer
from muntjac.data.util.hierarchical_container import HierarchicalContainer


class TestContainerSorting(TestCase):

    _ITEM_DATA_MINUS2_NULL = 'Data -2 null'
    _ITEM_DATA_MINUS2 = 'Data -2'
    _ITEM_DATA_MINUS1 = 'Data -1'
    _ITEM_DATA_MINUS1_NULL = 'Data -1 null'
    _ITEM_ANOTHER_NULL = 'Another null'
    _ITEM_STRING_2 = 'String 2'
    _ITEM_STRING_NULL2 = 'String null'
    _ITEM_STRING_1 = 'String 1'

    _PROPERTY_INTEGER_NULL2 = 'integer-null'
    _PROPERTY_INTEGER_NOT_NULL = 'integer-not-null'
    _PROPERTY_STRING_NULL = 'string-null'
    _PROPERTY_STRING_ID = 'string-not-null'


    def setUp(self):
        super(TestContainerSorting, self).setUp()


    def testEmptyFilteredIndexedContainer(self):
        ic = IndexedContainer()
        self.addProperties(ic)
        self.populate(ic)
        ic.addContainerFilter(self._PROPERTY_STRING_ID, 'aasdfasdfasdf',
                True, False)
        ic.sort([self._PROPERTY_STRING_ID], [True])


    def testFilteredIndexedContainer(self):
        ic = IndexedContainer()
        self.addProperties(ic)
        self.populate(ic)
        ic.addContainerFilter(self._PROPERTY_STRING_ID, 'a', True, False)
        ic.sort([self._PROPERTY_STRING_ID], [True])
        self.verifyOrder(ic, [self._ITEM_ANOTHER_NULL, self._ITEM_DATA_MINUS1,
                self._ITEM_DATA_MINUS1_NULL, self._ITEM_DATA_MINUS2,
                self._ITEM_DATA_MINUS2_NULL])


    def testIndexedContainer(self):
        ic = IndexedContainer()

        self.addProperties(ic)
        self.populate(ic)

        ic.sort([self._PROPERTY_STRING_ID], [True])
        self.verifyOrder(ic, [self._ITEM_ANOTHER_NULL, self._ITEM_DATA_MINUS1,
                self._ITEM_DATA_MINUS1_NULL, self._ITEM_DATA_MINUS2,
                self._ITEM_DATA_MINUS2_NULL, self._ITEM_STRING_1,
                self._ITEM_STRING_2, self._ITEM_STRING_NULL2])

        ic.sort([self._PROPERTY_INTEGER_NOT_NULL, self._PROPERTY_INTEGER_NULL2,
                self._PROPERTY_STRING_ID], [True, False, True])
        self.verifyOrder(ic, [self._ITEM_DATA_MINUS2,
                self._ITEM_DATA_MINUS2_NULL, self._ITEM_DATA_MINUS1,
                self._ITEM_DATA_MINUS1_NULL, self._ITEM_ANOTHER_NULL,
                self._ITEM_STRING_NULL2, self._ITEM_STRING_1,
                self._ITEM_STRING_2])

        ic.sort([self._PROPERTY_INTEGER_NOT_NULL, self._PROPERTY_INTEGER_NULL2,
                 self._PROPERTY_STRING_ID], [True, True, True])
        self.verifyOrder(ic, [self._ITEM_DATA_MINUS2_NULL,
                self._ITEM_DATA_MINUS2, self._ITEM_DATA_MINUS1_NULL,
                self._ITEM_DATA_MINUS1, self._ITEM_ANOTHER_NULL,
                self._ITEM_STRING_NULL2, self._ITEM_STRING_1,
                self._ITEM_STRING_2])


    def testHierarchicalContainer(self):
        hc = HierarchicalContainer()
        self.populateContainer(hc)
        hc.sort(['name'], [True])
        self.verifyOrder(hc, ['Audi', 'C++', 'Call of Duty', 'Cars',
                'English', 'Fallout', 'Finnish', 'Ford', 'Games', 'Java',
                'Might and Magic', 'Natural languages', 'PHP',
                'Programming languages', 'Python', 'Red Alert', 'Swedish',
                'Toyota', 'Volvo'])
        self.assertArrays(list(hc.rootItemIds()), [self._nameToId['Cars'],
                self._nameToId['Games'], self._nameToId['Natural languages'],
                self._nameToId['Programming languages']])
        self.assertArrays(list(hc.getChildren(self._nameToId['Games'])),
                [self._nameToId['Call of Duty'], self._nameToId['Fallout'],
                 self._nameToId['Might and Magic'],
                 self._nameToId['Red Alert']])


    @classmethod
    def populateContainer(cls, container):
        container.addContainerProperty('name', str, None)
        cls.addItem(container, 'Games', None)
        cls.addItem(container, 'Call of Duty', 'Games')
        cls.addItem(container, 'Might and Magic', 'Games')
        cls.addItem(container, 'Fallout', 'Games')
        cls.addItem(container, 'Red Alert', 'Games')
        cls.addItem(container, 'Cars', None)
        cls.addItem(container, 'Toyota', 'Cars')
        cls.addItem(container, 'Volvo', 'Cars')
        cls.addItem(container, 'Audi', 'Cars')
        cls.addItem(container, 'Ford', 'Cars')
        cls.addItem(container, 'Natural languages', None)
        cls.addItem(container, 'Swedish', 'Natural languages')
        cls.addItem(container, 'English', 'Natural languages')
        cls.addItem(container, 'Finnish', 'Natural languages')
        cls.addItem(container, 'Programming languages', None)
        cls.addItem(container, 'C++', 'Programming languages')
        cls.addItem(container, 'PHP', 'Programming languages')
        cls.addItem(container, 'Java', 'Programming languages')
        cls.addItem(container, 'Python', 'Programming languages')

    _index = 0
    _nameToId = dict()
    _idToName = dict()

    @classmethod
    def addItem(cls, *args):
        nargs = len(args)
        if nargs == 3:
            container, string, parent = args
            cls._nameToId[string] = cls._index
            cls._idToName[cls._index] = string
            item = container.addItem(cls._index)
            item.getItemProperty('name').setValue(string)
            if parent is not None and isinstance(container, HierarchicalContainer):
                container.setParent(cls._index, cls._nameToId[parent])
            cls._index += 1
        elif nargs == 5:
            ic, idd, string_null, integer, integer_null = args
            i = ic.addItem(idd)
            i.getItemProperty(cls._PROPERTY_STRING_ID).setValue(idd)
            i.getItemProperty(cls._PROPERTY_STRING_NULL).setValue(string_null)
            i.getItemProperty(cls._PROPERTY_INTEGER_NOT_NULL).setValue(integer)
            i.getItemProperty(cls._PROPERTY_INTEGER_NULL2).setValue(integer_null)
            return i
        else:
            raise ValueError


    def verifyOrder(self, ic, idOrder):
        size = len(ic)
        actual = [None] * size
        for index, o in enumerate(ic.getItemIds()):
            if (o.__class__ == int) and (idOrder[index].__class__ == str):
                o = self._idToName[o]
            actual[index] = o
        self.assertArrays(actual, idOrder)


    def assertArrays(self, actualObjects, expectedObjects):
        self.assertEquals(len(expectedObjects), len(actualObjects),
            'Actual contains a different number of values than was expected')

        for i in range(len(actualObjects)):
            actual = actualObjects[i]
            expected = expectedObjects[i]
            self.assertEquals(expected, actual, 'Item[%d] does not match' % i)


    def populate(self, ic):
        self.addItem(ic, self._ITEM_STRING_1, self._ITEM_STRING_1, 1, 1)
        self.addItem(ic, self._ITEM_STRING_NULL2, None, 0, None)
        self.addItem(ic, self._ITEM_STRING_2, self._ITEM_STRING_2, 2, 2)
        self.addItem(ic, self._ITEM_ANOTHER_NULL, None, 0, None)
        self.addItem(ic, self._ITEM_DATA_MINUS1, self._ITEM_DATA_MINUS1, -1, -1)
        self.addItem(ic, self._ITEM_DATA_MINUS1_NULL, None, -1, None)
        self.addItem(ic, self._ITEM_DATA_MINUS2, self._ITEM_DATA_MINUS2, -2, -2)
        self.addItem(ic, self._ITEM_DATA_MINUS2_NULL, None, -2, None)


    def addProperties(self, ic):
        ic.addContainerProperty('id', str, None)
        ic.addContainerProperty(self._PROPERTY_STRING_ID, str, '')
        ic.addContainerProperty(self._PROPERTY_STRING_NULL, str, None)
        ic.addContainerProperty(self._PROPERTY_INTEGER_NULL2, int, None)
        ic.addContainerProperty(self._PROPERTY_INTEGER_NOT_NULL, int, 0)
        ic.addContainerProperty('comparable-null', int, 0)


class MyObject(object):

    def __init__(self):
        _data = None

    def __eq__(self, o):
        if o is None:
            return 1
        if o.data is None:
            return 0 if self._data is None else 1
        elif self._data is None:
            return -1
        else:
            return self._data == o.data
