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

# from java.util.SortedSet import (SortedSet,)
# from java.util.TreeSet import (TreeSet,)
# from junit.framework.Assert import (Assert,)
# from junit.framework.TestCase import (TestCase,)


class PerformanceTestIndexedContainer(TestCase):
    _REPEATS = 10
    _ITEMS = 50000
    _ADD_ITEM_FAIL_THRESHOLD = 200
    # TODO should improve performance of these methods
    _ADD_ITEM_AT_FAIL_THRESHOLD = 5000
    _ADD_ITEM_AFTER_FAIL_THRESHOLD = 5000
    _ADD_ITEM_AFTER_LAST_FAIL_THRESHOLD = 5000
    _ADD_ITEMS_CONSTRUCTOR_FAIL_THRESHOLD = 200

    def testAddItemPerformance(self):
        times = list()
        _0 = True
        j = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                j += 1
            if not (j < self._REPEATS):
                break
            c = IndexedContainer()
            start = 1000 * time.time()
            _1 = True
            i = 0
            while True:
                if _1 is True:
                    _1 = False
                else:
                    i += 1
                if not (i < self._ITEMS):
                    break
                c.addItem()
            times.add(1000 * time.time() - start)
        self.checkMedian(self._ITEMS, times, 'IndexedContainer.addItem()', self._ADD_ITEM_FAIL_THRESHOLD)

    def testAddItemAtPerformance(self):
        times = list()
        _0 = True
        j = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                j += 1
            if not (j < self._REPEATS):
                break
            c = IndexedContainer()
            start = 1000 * time.time()
            _1 = True
            i = 0
            while True:
                if _1 is True:
                    _1 = False
                else:
                    i += 1
                if not (i < self._ITEMS):
                    break
                c.addItemAt(0)
            times.add(1000 * time.time() - start)
        self.checkMedian(self._ITEMS, times, 'IndexedContainer.addItemAt()', self._ADD_ITEM_AT_FAIL_THRESHOLD)

    def testAddItemAfterPerformance(self):
        initialId = 'Item0'
        times = list()
        _0 = True
        j = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                j += 1
            if not (j < self._REPEATS):
                break
            c = IndexedContainer()
            c.addItem(initialId)
            start = 1000 * time.time()
            _1 = True
            i = 0
            while True:
                if _1 is True:
                    _1 = False
                else:
                    i += 1
                if not (i < self._ITEMS):
                    break
                c.addItemAfter(initialId)
            times.add(1000 * time.time() - start)
        self.checkMedian(self._ITEMS, times, 'IndexedContainer.addItemAfter()', self._ADD_ITEM_AFTER_FAIL_THRESHOLD)

    def testAddItemAfterLastPerformance(self):
        # TODO running with less items because slow otherwise
        times = list()
        _0 = True
        j = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                j += 1
            if not (j < self._REPEATS):
                break
            c = IndexedContainer()
            c.addItem()
            start = 1000 * time.time()
            _1 = True
            i = 0
            while True:
                if _1 is True:
                    _1 = False
                else:
                    i += 1
                if not (i < self._ITEMS / 3):
                    break
                c.addItemAfter(c.lastItemId())
            times.add(1000 * time.time() - start)
        self.checkMedian(self._ITEMS / 3, times, 'IndexedContainer.addItemAfter(lastId)', self._ADD_ITEM_AFTER_LAST_FAIL_THRESHOLD)

    def testAddItemsConstructorPerformance(self):
        items = list(50000)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < self._ITEMS):
                break
            items.add(self.Object())
        times = TreeSet()
        _1 = True
        j = 0
        while True:
            if _1 is True:
                _1 = False
            else:
                j += 1
            if not (j < self._REPEATS):
                break
            start = 1000 * time.time()
            IndexedContainer(items)
            times.add(1000 * time.time() - start)
        self.checkMedian(self._ITEMS, times, 'IndexedContainer(Collection)', self._ADD_ITEMS_CONSTRUCTOR_FAIL_THRESHOLD)

    def checkMedian(self, items, times, methodName, threshold):
        median = self.median(times)
        print methodName + ' timings (ms) for ' + items + ' items: ' + times
        Assert.assertTrue(methodName + ' too slow, median time ' + median + 'ms for ' + items + ' items', median <= threshold)

    def median(self, times):
        list = list(times)
        Collections.sort(list)
        # not exact median in some cases, but good enough
        return list[len(list) / 2]
