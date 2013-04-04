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

from muntjac.test.server.data.util.abstract_container_test \
    import ItemSetChangeCounter

from muntjac.test.server.data.util.abstract_in_memory_container_test \
    import AbstractInMemoryContainerTest

from muntjac.data.util.indexed_container import IndexedContainer


class TestIndexedContainer(AbstractInMemoryContainerTest):

    def testBasicOperations(self):
        c = IndexedContainer()
        self._testBasicContainerOperations(c)


    def testFiltering(self):
        c = IndexedContainer()
        self._testContainerFiltering(c)


    def testSorting(self):
        c = IndexedContainer()
        self._testContainerSorting(c)


    def testSortingAndFiltering(self):
        c = IndexedContainer()
        self._testContainerSortingAndFiltering(c)


    def testContainerOrdered(self):
        c = IndexedContainer()
        self._testContainerOrdered(c)


    def testContainerIndexed(self):
        c = IndexedContainer()
        self._testContainerIndexed(c, self.sampleData[2], 2, True,
                'newItemId', True)


    def testItemSetChangeListeners(self):
        container = IndexedContainer()
        counter = ItemSetChangeCounter()
        container.addListener(counter)

        id1 = 'id1'
        id2 = 'id2'
        id3 = 'id3'

        self.initializeContainer(container)
        counter.reset()
        container.addItem()
        counter.assertOnce()
        container.addItem(id1)
        counter.assertOnce()

        self.initializeContainer(container)
        counter.reset()
        container.addItemAt(0)
        counter.assertOnce()
        container.addItemAt(0, id1)
        counter.assertOnce()
        container.addItemAt(0, id2)
        counter.assertOnce()
        container.addItemAt(len(container), id3)
        counter.assertOnce()
        # no notification if already in container
        container.addItemAt(0, id1)
        counter.assertNone()

        self.initializeContainer(container)
        counter.reset()
        container.addItemAfter(None)
        counter.assertOnce()
        container.addItemAfter(None, id1)
        counter.assertOnce()
        container.addItemAfter(id1)
        counter.assertOnce()
        container.addItemAfter(id1, id2)
        counter.assertOnce()
        container.addItemAfter(container.firstItemId())
        counter.assertOnce()
        container.addItemAfter(container.lastItemId())
        counter.assertOnce()
        container.addItemAfter(container.lastItemId(), id3)
        counter.assertOnce()
        # no notification if already in container
        container.addItemAfter(0, id1)
        counter.assertNone()

        self.initializeContainer(container)
        counter.reset()
        container.removeItem(self.sampleData[0])
        counter.assertOnce()

        self.initializeContainer(container)
        counter.reset()
        # no notification for removing a non-existing item
        container.removeItem(id1)
        counter.assertNone()

        self.initializeContainer(container)
        counter.reset()
        container.removeAllItems()
        counter.assertOnce()
        # already empty
        container.removeAllItems()
        counter.assertNone()


    def testAddRemoveContainerFilter(self):
        container = IndexedContainer()
        counter = ItemSetChangeCounter()
        container.addListener(counter)

        # simply adding or removing container filters should cause events
        # (content changes)

        self.initializeContainer(container)
        counter.reset()
        container.addContainerFilter(self.SIMPLE_NAME, 'a', True, False)
        counter.assertOnce()
        container.removeContainerFilters(self.SIMPLE_NAME)
        counter.assertOnce()
        container.addContainerFilter(self.SIMPLE_NAME, 'a', True, False)
        counter.assertOnce()
        container.removeAllContainerFilters()
        counter.assertOnce()


    # TODO other tests should check positions after removing filter etc,
    # here concentrating on listeners
    def testItemSetChangeListenersFiltering(self):
        container = IndexedContainer()
        counter = ItemSetChangeCounter()
        container.addListener(counter)

        counter.reset()
        container.addContainerFilter(self.FULLY_QUALIFIED_NAME, 'Test', True, False)
        # no real change, so no notification required
        counter.assertNone()

        id1 = 'com.example.Test1'
        id2 = 'com.example.Test2'
        id3 = 'com.example.Other'

        # perform operations while filtering container

        self.initializeContainer(container)
        counter.reset()
        # passes filter
        item = container.addItem(id1)
        # no event if filtered out
        counter.assertNone()
        item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(id1)
        counter.assertOnce()
        # passes filter but already in the container
        item = container.addItem(id1)
        counter.assertNone()

        self.initializeContainer(container)
        counter.reset()
        # passes filter after change
        item = container.addItemAt(0, id1)
        counter.assertNone()
        item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(id1)
        counter.assertOnce()
        item = container.addItemAt(len(container), id2)
        counter.assertNone()
        item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(id2)
        counter.assertOnce()
        # passes filter but already in the container
        item = container.addItemAt(0, id1)
        counter.assertNone()
        item = container.addItemAt(len(container), id2)
        counter.assertNone()

        self.initializeContainer(container)
        counter.reset()
        # passes filter
        item = container.addItemAfter(None, id1)
        counter.assertNone()
        item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(id1)
        counter.assertOnce()
        item = container.addItemAfter(container.lastItemId(), id2)
        counter.assertNone()
        item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(id2)
        counter.assertOnce()
        # passes filter but already in the container
        item = container.addItemAfter(None, id1)
        counter.assertNone()
        item = container.addItemAfter(container.lastItemId(), id2)
        counter.assertNone()

        # does not pass filter

        # TODO implement rest

        self.initializeContainer(container)
        counter.reset()
        item = container.addItemAfter(None, id3)
        counter.assertNone()
        item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(id3)
        counter.assertNone()

        self.initializeContainer(container)
        counter.reset()
        item = container.addItemAfter(container.firstItemId(), id3)
        counter.assertNone()
        item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(id3)
        counter.assertNone()

        self.initializeContainer(container)
        counter.reset()
        item = container.addItemAfter(container.lastItemId(), id3)
        counter.assertNone()
        item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(id3)
        counter.assertNone()

        self.initializeContainer(container)
        counter.reset()
        item = container.addItemAt(0, id3)
        counter.assertNone()
        item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(id3)
        counter.assertNone()

        self.initializeContainer(container)
        counter.reset()
        item = container.addItemAt(1, id3)
        counter.assertNone()
        item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(id3)
        counter.assertNone()

        self.initializeContainer(container)
        counter.reset()
        item = container.addItemAt(len(container), id3)
        counter.assertNone()
        item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(id3)
        counter.assertNone()

        # passes filter

        self.initializeContainer(container)
        counter.reset()
        item = container.addItem(id1)
        counter.assertNone()
        item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(id1)
        counter.assertOnce()
        container.removeItem(id1)
        counter.assertOnce()
        # already removed
        container.removeItem(id1)
        counter.assertNone()

        item = container.addItem(id3)
        counter.assertNone()
        item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(id3)
        counter.assertNone()
        # not visible
        container.removeItem(id3)
        counter.assertNone()

        # remove all

        self.initializeContainer(container)
        item = container.addItem(id1)
        item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(id1)
        counter.reset()
        container.removeAllItems()
        counter.assertOnce()
        # no visible items
        container.removeAllItems()
        counter.assertNone()
