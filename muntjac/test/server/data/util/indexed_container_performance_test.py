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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

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
