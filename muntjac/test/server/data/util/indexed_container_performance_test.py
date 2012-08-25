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

import time

from unittest import TestCase
from muntjac.data.util.indexed_container import IndexedContainer


class PerformanceTestIndexedContainer(TestCase):

    _REPEATS = 10
    _ITEMS = 1000
    _ADD_ITEM_FAIL_THRESHOLD = 200
    # TODO should improve performance of these methods
    _ADD_ITEM_AT_FAIL_THRESHOLD = 5000
    _ADD_ITEM_AFTER_FAIL_THRESHOLD = 5000
    _ADD_ITEM_AFTER_LAST_FAIL_THRESHOLD = 5000
    _ADD_ITEMS_CONSTRUCTOR_FAIL_THRESHOLD = 200


    def testAddItemPerformance(self):
        times = list()
        for _ in range(self._REPEATS):
            c = IndexedContainer()
            start = 1000 * time.time()
            for _ in range(self._ITEMS):
                c.addItem()
            times.append((1000 * time.time()) - start)
        self.checkMedian(self._ITEMS, times, 'IndexedContainer.addItem()',
                self._ADD_ITEM_FAIL_THRESHOLD)


    def testAddItemAtPerformance(self):
        times = list()
        for _ in range(self._REPEATS):
            c = IndexedContainer()
            start = 1000 * time.time()
            for _ in range(self._ITEMS):
                c.addItemAt(0)
            times.append((1000 * time.time()) - start)
        self.checkMedian(self._ITEMS, times, 'IndexedContainer.addItemAt()',
                self._ADD_ITEM_AT_FAIL_THRESHOLD)


    def testAddItemAfterPerformance(self):
        initialId = 'Item0'
        times = list()
        for _ in range(self._REPEATS):
            c = IndexedContainer()
            c.addItem(initialId)
            start = 1000 * time.time()
            for _ in range(self._ITEMS):
                c.addItemAfter(initialId)
            times.append((1000 * time.time()) - start)
        self.checkMedian(self._ITEMS, times, 'IndexedContainer.addItemAfter()',
                self._ADD_ITEM_AFTER_FAIL_THRESHOLD)


    def testAddItemAfterLastPerformance(self):
        # TODO running with less items because slow otherwise
        times = list()
        for _ in range(self._REPEATS):
            c = IndexedContainer()
            c.addItem()
            start = 1000 * time.time()
            for _ in range(self._ITEMS):
                c.addItemAfter(c.lastItemId())
            times.append((1000 * time.time()) - start)
        self.checkMedian(self._ITEMS / 3, times,
                'IndexedContainer.addItemAfter(lastId)',
                self._ADD_ITEM_AFTER_LAST_FAIL_THRESHOLD)


    def testAddItemsConstructorPerformance(self):
        items = list()
        for _ in range(self._ITEMS):
            items.append(object())

        times = set()
        for _ in range(self._REPEATS):
            start = 1000 * time.time()
            IndexedContainer(items)
            times.add((1000 * time.time()) - start)
        self.checkMedian(self._ITEMS, times, 'IndexedContainer(Collection)',
                self._ADD_ITEMS_CONSTRUCTOR_FAIL_THRESHOLD)


    def checkMedian(self, items, times, methodName, threshold):
        median = self.median(times)
        print '%s timings (ms) for %d items: %s' % (methodName, items, times)
        self.assertTrue(median <= threshold,
            '%s too slow, median time %.2fms for %s items' %
            (methodName, median, items))


    def median(self, times):
        lst = list(times)
        lst.sort()
        # not exact median in some cases, but good enough
        return lst[len(lst) / 2]
