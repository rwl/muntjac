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

from warnings import warn

from muntjac.test.server.data.util.NestedMethodPropertyTest import \
    NestedMethodPropertyTest

from muntjac.test.server.data.util.AbstractBeanContainerTest import \
    AbstractBeanContainerTest, ClassName, Person

from muntjac.data.util.bean_item_container import BeanItemContainer


class BeanItemContainerTest(AbstractBeanContainerTest):
    """Test basic functionality of BeanItemContainer.

    Most sorting related tests are in {@link BeanItemContainerSortTest}.
    """

    def getContainer(self):
        return BeanItemContainer(ClassName)


    def setUp(self):
        # basics from the common container test
        self._nameToBean = dict()
        self._nameToBean.clear()

        for i in range(len(self.sampleData)):
            className = ClassName(self.sampleData[i], i)
            self._nameToBean[self.sampleData[i]] = className


    def initializeContainer(self, container):
        beanItemContainer = container
        beanItemContainer.removeAllItems()
        it = self._nameToBean.values()
        while it.hasNext():
            beanItemContainer.addBean(it.next())


    def validateContainer(self, container, expectedFirstItemId,
                expectedLastItemId, itemIdInSet, itemIdNotInSet,
                checkGetItemNull, expectedSize):
        notInSet = self._nameToBean.get(itemIdNotInSet)
        if notInSet is None and itemIdNotInSet is not None:
            notInSet = ClassName(str(itemIdNotInSet), 9999)
        super(BeanItemContainerTest, self).validateContainer(container,
                self._nameToBean.get(expectedFirstItemId),
                self._nameToBean.get(expectedLastItemId),
                self._nameToBean.get(itemIdInSet),
                notInSet, checkGetItemNull, expectedSize)


    def isFilteredOutItemNull(self):
        return False


    def testBasicOperations(self):
        self.testBasicContainerOperations(self.getContainer())


    def testFiltering(self):
        self.testContainerFiltering(self.getContainer())


    def testSorting(self):
        self.testContainerSorting(self.getContainer())


    def testSortingAndFiltering(self):
        # duplicated from parent class and modified - adding items to
        # BeanItemContainer differs from other containers
        self.testContainerSortingAndFiltering(self.getContainer())


    def testContainerOrdered(self):
        container = BeanItemContainer(str)

        idd = 'test1'

        item = container.addBean(idd)
        self.assertNotEquals(item, None)

        self.assertEquals(idd, container.firstItemId())
        self.assertEquals(idd, container.lastItemId())

        # isFirstId
        self.assertTrue(container.isFirstId(idd))
        self.assertTrue(container.isFirstId(container.firstItemId()))

        # isLastId
        self.assertTrue(container.isLastId(idd))
        self.assertTrue(container.isLastId(container.lastItemId()))

        # Add a new item before the first
        # addItemAfter
        newFirstId = 'newFirst'
        item = container.addItemAfter(None, newFirstId)
        self.assertNotEquals(item, None)
        self.assertNotEquals(container.getItem(newFirstId), None)

        # isFirstId
        self.assertTrue(container.isFirstId(newFirstId))
        self.assertTrue(container.isFirstId(container.firstItemId()))

        # isLastId
        self.assertTrue(container.isLastId(idd))
        self.assertTrue(container.isLastId(container.lastItemId()))

        # nextItemId
        self.assertEquals(idd, container.nextItemId(newFirstId))
        self.assertEquals(container.nextItemId(idd), None)
        self.assertEquals(container.nextItemId('not-in-container'), None)

        # prevItemId
        self.assertEquals(newFirstId, container.prevItemId(idd))
        self.assertEquals(container.prevItemId(newFirstId), None)
        self.assertEquals(container.prevItemId('not-in-container'), None)

        # addItemAfter(Object)
        newSecondItemId = 'newSecond'
        item = container.addItemAfter(newFirstId, newSecondItemId)

        # order is now: newFirstId, newSecondItemId, idd
        self.assertNotEquals(item, None)
        self.assertNotEquals(container.getItem(newSecondItemId), None)
        self.assertEquals(idd, container.nextItemId(newSecondItemId))
        self.assertEquals(newFirstId, container.prevItemId(newSecondItemId))

        # addItemAfter(Object,Object)
        fourthId = 'idd of the fourth item'
        fourth = container.addItemAfter(newFirstId, fourthId)

        # order is now: newFirstId, fourthId, newSecondItemId, idd
        self.assertNotEquals(fourth, None)
        self.assertEquals(fourth, container.getItem(fourthId))
        self.assertEquals(newSecondItemId, container.nextItemId(fourthId))
        self.assertEquals(newFirstId, container.prevItemId(fourthId))

        # addItemAfter(Object,Object)
        fifthId = 'fifth'
        fifth = container.addItemAfter(None, fifthId)
        # order is now: fifthId, newFirstId, fourthId, newSecondItemId, idd
        self.assertNotEquals(fifth, None)
        self.assertEquals(fifth, container.getItem(fifthId))
        self.assertEquals(newFirstId, container.nextItemId(fifthId))
        self.assertEquals(container.prevItemId(fifthId), None)


    def testContainerIndexed(self):
        self.testContainerIndexed(self.getContainer(),
                self._nameToBean.get(self.sampleData[2]), 2, False,
                ClassName('org.vaadin.test.Test', 8888), True)


    # this only applies to the collection constructor with no type parameter
    def testCollectionConstructors(self):
        warn('deprecated', DeprecationWarning)

        classNames = list()
        classNames.append(ClassName('a.b.c.Def', 1))
        classNames.append(ClassName('a.b.c.Fed', 2))
        classNames.append(ClassName('b.c.d.Def', 3))

        # note that this constructor is problematic, users should use the
        # version that
        # takes the bean class as a parameter
        container = BeanItemContainer(classNames)

        self.assertEquals(3, len(container))
        self.assertEquals(classNames[0], container.firstItemId())
        self.assertEquals(classNames[1], container.getIdByIndex(1))
        self.assertEquals(classNames[2], container.lastItemId())

        container2 = BeanItemContainer(ClassName, classNames)

        self.assertEquals(3, len(container2))
        self.assertEquals(classNames[0], container2.firstItemId())
        self.assertEquals(classNames[1], container2.getIdByIndex(1))
        self.assertEquals(classNames[2], container2.lastItemId())


    def testEmptyCollectionConstructor(self):
        try:
            BeanItemContainer(None)
            self.fail(('Initializing BeanItemContainer from a null '
                    'collection should not work!'))
        except ValueError:
            pass  # success

        try:
            BeanItemContainer(list())
            self.fail(('Initializing BeanItemContainer from an empty '
                    'collection should not work!'))
        except ValueError:
            pass  # success


    def testItemSetChangeListeners(self):
        container = self.getContainer()
        counter = self.ItemSetChangeCounter()
        container.addListener(counter)

        cn1 = ClassName('com.example.Test', 1111)
        cn2 = ClassName('com.example.Test2', 2222)

        self.initializeContainer(container)
        counter.reset()
        container.addBean(cn1)
        counter.assertOnce()

        self.initializeContainer(container)
        counter.reset()
        container.addItem(cn1)
        counter.assertOnce()
        # no notification if already in container
        container.addItem(cn1)
        counter.assertNone()
        container.addItem(cn2)
        counter.assertOnce()

        self.initializeContainer(container)
        counter.reset()
        container.addItemAfter(None, cn1)
        counter.assertOnce()
        self.assertEquals('com.example.Test',
                container.getContainerProperty(container.firstItemId(),
                        self.FULLY_QUALIFIED_NAME).getValue())

        self.initializeContainer(container)
        counter.reset()
        container.addItemAfter(container.firstItemId(), cn1)
        counter.assertOnce()
        self.assertEquals('com.example.Test',
                container.getContainerProperty(container.getIdByIndex(1),
                        self.FULLY_QUALIFIED_NAME).getValue())

        self.initializeContainer(container)
        counter.reset()
        container.addItemAfter(container.lastItemId(), cn1)
        counter.assertOnce()
        self.assertEquals('com.example.Test',
                container.getContainerProperty(container.lastItemId(),
                        self.FULLY_QUALIFIED_NAME).getValue())

        self.initializeContainer(container)
        counter.reset()
        container.addItemAt(0, cn1)
        counter.assertOnce()
        self.assertEquals('com.example.Test',
                container.getContainerProperty(container.firstItemId(),
                        self.FULLY_QUALIFIED_NAME).getValue())

        self.initializeContainer(container)
        counter.reset()
        container.addItemAt(1, cn1)
        counter.assertOnce()
        self.assertEquals('com.example.Test',
                container.getContainerProperty(container.getIdByIndex(1),
                        self.FULLY_QUALIFIED_NAME).getValue())

        self.initializeContainer(container)
        counter.reset()
        container.addItemAt(len(container), cn1)
        counter.assertOnce()
        self.assertEquals('com.example.Test',
                container.getContainerProperty(container.lastItemId(),
                        self.FULLY_QUALIFIED_NAME).getValue())

        self.initializeContainer(container)
        counter.reset()
        container.removeItem(self._nameToBean[self.sampleData[0]])
        counter.assertOnce()

        self.initializeContainer(container)
        counter.reset()
        # no notification for removing a non-existing item
        container.removeItem(cn1)
        counter.assertNone()

        self.initializeContainer(container)
        counter.reset()
        container.removeAllItems()
        counter.assertOnce()
        # already empty
        container.removeAllItems()
        counter.assertNone()


    def testItemSetChangeListenersFiltering(self):
        container = self.getContainer()
        counter = self.ItemSetChangeCounter()
        container.addListener(counter)

        cn1 = ClassName('com.example.Test', 1111)
        cn2 = ClassName('com.example.Test2', 2222)
        other = ClassName('com.example.Other', 3333)

        # simply adding or removing container filters should cause event
        # (content changes)

        self.initializeContainer(container)
        counter.reset()
        container.addContainerFilter(self.SIMPLE_NAME, 'a', True, False)
        counter.assertOnce()
        container.removeContainerFilters(self.SIMPLE_NAME)
        counter.assertOnce()

        self.initializeContainer(container)
        counter.reset()
        container.addContainerFilter(self.SIMPLE_NAME, 'a', True, False)
        counter.assertOnce()
        container.removeAllContainerFilters()
        counter.assertOnce()

        # perform operations while filtering container

        self.initializeContainer(container)
        counter.reset()
        container.addContainerFilter(self.FULLY_QUALIFIED_NAME, 'Test',
                True, False)
        counter.assertOnce()

        # passes filter
        container.addBean(cn1)
        counter.assertOnce()

        # passes filter but already in the container
        container.addBean(cn1)
        counter.assertNone()

        self.initializeContainer(container)
        counter.reset()

        # passes filter
        container.addItem(cn1)
        counter.assertOnce()

        # already in the container
        container.addItem(cn1)
        counter.assertNone()
        container.addItem(cn2)
        counter.assertOnce()
        # does not pass filter
        container.addItem(other)
        counter.assertNone()

        self.initializeContainer(container)
        counter.reset()
        container.addItemAfter(None, cn1)
        counter.assertOnce()
        self.assertEquals('com.example.Test',
                container.getContainerProperty(container.firstItemId(),
                        self.FULLY_QUALIFIED_NAME).getValue())

        self.initializeContainer(container)
        counter.reset()
        container.addItemAfter(container.firstItemId(), cn1)
        counter.assertOnce()
        self.assertEquals('com.example.Test',
                container.getContainerProperty(container.getIdByIndex(1),
                        self.FULLY_QUALIFIED_NAME).getValue())

        self.initializeContainer(container)
        counter.reset()
        container.addItemAfter(container.lastItemId(), cn1)
        counter.assertOnce()
        self.assertEquals('com.example.Test',
                container.getContainerProperty(container.lastItemId(),
                        self.FULLY_QUALIFIED_NAME).getValue())

        self.initializeContainer(container)
        counter.reset()
        container.addItemAt(0, cn1)
        counter.assertOnce()
        self.assertEquals('com.example.Test',
                container.getContainerProperty(container.firstItemId(),
                        self.FULLY_QUALIFIED_NAME).getValue())

        self.initializeContainer(container)
        counter.reset()
        container.addItemAt(1, cn1)
        counter.assertOnce()
        self.assertEquals('com.example.Test',
                container.getContainerProperty(container.getIdByIndex(1),
                        self.FULLY_QUALIFIED_NAME).getValue())

        self.initializeContainer(container)
        counter.reset()
        container.addItemAt(len(container), cn1)
        counter.assertOnce()
        self.assertEquals('com.example.Test',
                container.getContainerProperty(container.lastItemId(),
                        self.FULLY_QUALIFIED_NAME).getValue())

        # does not pass filter
        # note: testAddRemoveWhileFiltering() checks position for these after
        # removing filter etc, here concentrating on listeners

        self.initializeContainer(container)
        counter.reset()
        container.addItemAfter(None, other)
        counter.assertNone()

        self.initializeContainer(container)
        counter.reset()
        container.addItemAfter(container.firstItemId(), other)
        counter.assertNone()

        self.initializeContainer(container)
        counter.reset()
        container.addItemAfter(container.lastItemId(), other)
        counter.assertNone()

        self.initializeContainer(container)
        counter.reset()
        container.addItemAt(0, other)
        counter.assertNone()

        self.initializeContainer(container)
        counter.reset()
        container.addItemAt(1, other)
        counter.assertNone()

        self.initializeContainer(container)
        counter.reset()
        container.addItemAt(len(container), other)
        counter.assertNone()

        # passes filter

        self.initializeContainer(container)
        counter.reset()
        container.addItem(cn1)
        counter.assertOnce()
        container.removeItem(cn1)
        counter.assertOnce()

        # does not pass filter

        self.initializeContainer(container)
        counter.reset()
        # not visible
        container.removeItem(self._nameToBean[self.sampleData[0]])
        counter.assertNone()

        container.removeAllItems()
        counter.assertOnce()
        # no visible items
        container.removeAllItems()
        counter.assertNone()


    def testAddRemoveWhileFiltering(self):
        container = BeanItemContainer(Person)

        john = Person('John')
        jane = Person('Jane')
        matthew = Person('Matthew')

        jack = Person('Jack')
        michael = Person('Michael')
        william = Person('William')
        julia = Person('Julia')
        george = Person('George')
        mark = Person('Mark')

        container.addBean(john)
        container.addBean(jane)
        container.addBean(matthew)

        self.assertEquals(3, len(container))
        # john, jane, matthew

        container.addContainerFilter('name', 'j', True, True)

        self.assertEquals(2, len(container))
        # john, jane, (matthew)

        # add a bean that passes the filter
        container.addBean(jack)
        self.assertEquals(3, len(container))
        self.assertEquals(jack, container.lastItemId())
        # john, jane, (matthew), jack

        # add beans that do not pass the filter
        container.addBean(michael)
        # john, jane, (matthew), jack, (michael)
        container.addItemAfter(None, william)
        # (william), john, jane, (matthew), jack, (michael)

        # add after an item that is shown
        container.addItemAfter(john, george)
        # (william), john, (george), jane, (matthew), jack, (michael)
        self.assertEquals(3, len(container))
        self.assertEquals(john, container.firstItemId())

        # add after an item that is not shown does nothing
        container.addItemAfter(william, julia)
        # (william), john, (george), jane, (matthew), jack, (michael)
        self.assertEquals(3, len(container))
        self.assertEquals(john, container.firstItemId())

        container.addItemAt(1, julia)
        # (william), john, julia, (george), jane, (matthew), jack, (michael)
        container.addItemAt(2, mark)
        # (william), john, julia, (mark), (george), jane, (matthew), jack,
        # (michael)

        container.removeItem(matthew)
        # (william), john, julia, (mark), (george), jane, jack, (michael)

        self.assertEquals(4, len(container))
        self.assertEquals(jack, container.lastItemId())

        container.removeContainerFilters('name')

        self.assertEquals(8, len(container))
        self.assertEquals(william, container.firstItemId())
        self.assertEquals(john, container.nextItemId(william))
        self.assertEquals(julia, container.nextItemId(john))
        self.assertEquals(mark, container.nextItemId(julia))
        self.assertEquals(george, container.nextItemId(mark))
        self.assertEquals(jane, container.nextItemId(george))
        self.assertEquals(jack, container.nextItemId(jane))
        self.assertEquals(michael, container.lastItemId())


    def testRefilterOnPropertyModification(self):
        container = BeanItemContainer(Person)

        john = Person('John')
        jane = Person('Jane')
        matthew = Person('Matthew')

        container.addBean(john)
        container.addBean(jane)
        container.addBean(matthew)

        self.assertEquals(3, len(container))
        # john, jane, matthew

        container.addContainerFilter('name', 'j', True, True)

        self.assertEquals(2, len(container))
        # john, jane, (matthew)

        # #6053 currently, modification of an item that is not visible does not
        # trigger refiltering - should it?
        # matthew.setName("Julia");
        # assertEquals(3, container.size());
        # john, jane, julia

        john.setName('Mark')
        self.assertEquals(2, len(container))

        # (mark), jane, julia
        container.removeAllContainerFilters()

        self.assertEquals(3, len(container))


    def testAddAll(self):
        container = BeanItemContainer(Person)

        john = Person('John')
        jane = Person('Jane')
        matthew = Person('Matthew')

        container.addBean(john)
        container.addBean(jane)
        container.addBean(matthew)

        self.assertEquals(3, len(container))
        # john, jane, matthew

        jack = Person('Jack')
        michael = Person('Michael')

        # addAll
        container.addAll(list(jack, michael))
        # john, jane, matthew, jack, michael

        self.assertEquals(5, len(container))
        self.assertEquals(jane, container.nextItemId(john))
        self.assertEquals(matthew, container.nextItemId(jane))
        self.assertEquals(jack, container.nextItemId(matthew))
        self.assertEquals(michael, container.nextItemId(jack))


    def testUnsupportedMethods(self):
        container = BeanItemContainer(Person)
        container.addBean(Person('John'))

        try:
            container.addItem()
            self.fail()
        except NotImplementedError:
            pass  # should get exception

        try:
            container.addItemAfter(Person('Jane'))
            self.fail()
        except NotImplementedError:
            pass  # should get exception

        try:
            container.addItemAt(0)
            self.fail()
        except NotImplementedError:
            pass  # should get exception

        try:
            container.addContainerProperty('lastName', str, '')
            self.fail()
        except NotImplementedError:
            pass  # should get exception

        self.assertEquals(1, len(container))


    def testRemoveContainerProperty(self):
        container = BeanItemContainer(Person)
        john = Person('John')
        container.addBean(john)

        self.assertEquals('John',
                container.getContainerProperty(john, 'name').getValue())
        self.assertTrue(container.removeContainerProperty('name'))
        self.assertEquals(container.getContainerProperty(john, 'name'), None)
        self.assertNotEquals(container.getItem(john), None)

        # property removed also from item
        self.assertEquals(container.getItem(john).getItemProperty('name'),
                None)


    def testAddNullBean(self):
        container = BeanItemContainer(Person)
        john = Person('John')
        container.addBean(john)

        self.assertEquals(container.addItem(None), None)
        self.assertEquals(container.addItemAfter(None, None), None)
        self.assertEquals(container.addItemAfter(john, None), None)
        self.assertEquals(container.addItemAt(0, None), None)

        self.assertEquals(1, len(container))


    def testBeanIdResolver(self):
        container = BeanItemContainer(Person)
        john = Person('John')
        self.assertEquals(john,
                container.getBeanIdResolver().getIdForBean(john))


    def testNullBeanClass(self):
        try:
            BeanItemContainer(None)
        except ValueError:
            pass  # should get exception


    def testAddNestedContainerProperty(self):
        container = BeanItemContainer(NestedMethodPropertyTest.Person)

        john = NestedMethodPropertyTest.Person('John',
                NestedMethodPropertyTest.Address('Ruukinkatu 2-4', 20540))
        container.addBean(john)

        self.assertTrue(container.addNestedContainerProperty('address.street'))
        self.assertEquals('Ruukinkatu 2-4',
                container.getContainerProperty(john,
                        'address.street').getValue())
