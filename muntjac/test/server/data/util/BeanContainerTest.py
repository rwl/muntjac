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

from muntjac.test.server.data.util.NestedMethodPropertyTest import \
    NestedMethodPropertyTest

from muntjac.test.server.data.util.AbstractBeanContainerTest import \
    AbstractBeanContainerTest, ClassName, Person

from muntjac.data.util.abstract_bean_container import BeanIdResolver
from muntjac.data.util.bean_container import BeanContainer


class PersonNameResolver(BeanIdResolver):

    def getIdForBean(self, bean):
        return bean.getName() if bean is not None else None


class NullResolver(BeanIdResolver):

    def getIdForBean(self, bean):
        return None


class BeanContainerTest(AbstractBeanContainerTest):

    def getContainer(self):
        return BeanContainer(ClassName)


    def setUp(self):
        self._nameToBean = {}
        self._nameToBean.clear()

        for i in range(len(self.sampleData)):
            className = ClassName(self.sampleData[i], i)
            self._nameToBean[self.sampleData[i]] = className


    def initializeContainer(self, container):
        beanItemContainer = container
        beanItemContainer.removeAllItems()
        for k, v in self._nameToBean.iteritems:
            beanItemContainer.addItem(k, v)


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
        # BeanContainer differs from other containers
        self.testContainerSortingAndFiltering(self.getContainer())


    def testContainerOrdered(self):
        # TODO test IIndexed interface operation - testContainerIndexed()?
        container = BeanContainer(str)

        idd = 'test1'

        item = container.addItem(idd, 'value')
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
        item = container.addItemAfter(None, newFirstId, 'newFirstValue')
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

        # addItemAfter(IDTYPE, IDTYPE, BT)
        newSecondItemId = 'newSecond'
        item = container.addItemAfter(newFirstId, newSecondItemId,
                'newSecondValue')
        # order is now: newFirstId, newSecondItemId, idd
        self.assertNotEquals(item, None)
        self.assertNotEquals(container.getItem(newSecondItemId), None)
        self.assertEquals(idd, container.nextItemId(newSecondItemId))
        self.assertEquals(newFirstId, container.prevItemId(newSecondItemId))

        # addItemAfter(IDTYPE, IDTYPE, BT)
        fourthId = 'idd of the fourth item'
        fourth = container.addItemAfter(newFirstId, fourthId, 'fourthValue')
        # order is now: newFirstId, fourthId, newSecondItemId, idd
        self.assertNotEquals(fourth, None)
        self.assertEquals(fourth, container.getItem(fourthId))
        self.assertEquals(newSecondItemId, container.nextItemId(fourthId))
        self.assertEquals(newFirstId, container.prevItemId(fourthId))

        # addItemAfter(IDTYPE, IDTYPE, BT)
        fifthId = 'fifth'
        fifth = container.addItemAfter(None, fifthId, 'fifthValue')
        # order is now: fifthId, newFirstId, fourthId, newSecondItemId, idd
        self.assertNotEquals(fifth, None)
        self.assertEquals(fifth, container.getItem(fifthId))
        self.assertEquals(newFirstId, container.nextItemId(fifthId))
        self.assertEquals(container.prevItemId(fifthId), None)


    def testAddItemAt(self):
        container = BeanContainer(str)

        container.addItem('id1', 'value1')
        # id1
        container.addItemAt(0, 'id2', 'value2')
        # id2, id1
        container.addItemAt(1, 'id3', 'value3')
        # id2, id3, id1
        container.addItemAt(len(container), 'id4', 'value4')
        # id2, id3, id1, id4

        self.assertEquals(container.addItemAt(-1, 'id5', 'value5'), None)
        self.assertEquals(container.addItemAt(len(container) + 1, 'id6',
                'value6'), None)

        self.assertEquals(4, len(container))
        self.assertEquals('id2', container.getIdByIndex(0))
        self.assertEquals('id3', container.getIdByIndex(1))
        self.assertEquals('id1', container.getIdByIndex(2))
        self.assertEquals('id4', container.getIdByIndex(3))


    def testUnsupportedMethods(self):
        container = BeanContainer(Person)
        container.addItem('John', Person('John'))

        try:
            container.addItem()
            self.fail()
        except NotImplementedError:
            pass  # should get exception

        try:
            container.addItem(None)
            self.fail()
        except NotImplementedError:
            pass  # should get exception

        try:
            container.addItemAfter(None, None)
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
            container.addItemAt(0, Person('Jane'))
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
        container = BeanContainer(Person)
        container.setBeanIdResolver(self.PersonNameResolver())
        container.addBean(Person('John'))

        self.assertEquals('John',
                container.getContainerProperty('John', 'name').getValue())
        self.assertTrue(container.removeContainerProperty('name'))
        self.assertEquals(container.getContainerProperty('John', 'name'),
                None)

        self.assertNotEquals(container.getItem('John'), None)
        # property removed also from item
        self.assertEquals(container.getItem('John').getItemProperty('name'),
                None)


    def testAddNullBeans(self):
        container = BeanContainer(Person)

        self.assertEquals(container.addItem('id1', None), None)
        self.assertEquals(container.addItemAfter(None, 'id2', None), None)
        self.assertEquals(container.addItemAt(0, 'id3', None), None)

        self.assertEquals(0, len(container))


    def testAddNullId(self):
        container = BeanContainer(Person)

        john = Person('John')

        self.assertEquals(container.addItem(None, john), None)
        self.assertEquals(container.addItemAfter(None, None, john), None)
        self.assertEquals(container.addItemAt(0, None, john), None)

        self.assertEquals(0, len(container))


    def testEmptyContainer(self):
        container = BeanContainer(Person)

        self.assertEquals(container.firstItemId(), None)
        self.assertEquals(container.lastItemId(), None)
        self.assertEquals(0, len(container))

        # could test more about empty container


    def testAddBeanWithoutResolver(self):
        container = BeanContainer(Person)

        try:
            container.addBean(Person('John'))
            self.fail()
        except self.IllegalStateException:
            pass  # should get exception

        try:
            container.addBeanAfter(None, Person('Jane'))
            self.fail()
        except self.IllegalStateException:
            pass  # should get exception

        try:
            container.addBeanAt(0, Person('Jack'))
            self.fail()
        except self.IllegalStateException:
            pass  # should get exception

        try:
            container.addAll( [Person('Jack')] )
            self.fail()
        except self.IllegalStateException:
            pass  # should get exception

        self.assertEquals(0, len(container))


    def testAddBeanWithNullResolver(self):
        container = BeanContainer(Person)

        # resolver that returns null as item id
        container.setBeanIdResolver(self.NullResolver())

        try:
            container.addBean(Person('John'))
            self.fail()
        except ValueError:
            pass  # should get exception

        try:
            container.addBeanAfter(None, Person('Jane'))
            self.fail()
        except ValueError:
            pass  # should get exception

        try:
            container.addBeanAt(0, Person('Jack'))
            self.fail()
        except ValueError:
            pass  # should get exception

        self.assertEquals(0, len(container))


    def testAddBeanWithResolver(self):
        container = BeanContainer(Person)
        container.setBeanIdResolver(self.PersonNameResolver())

        self.assertNotEquals(container.addBean(Person('John')), None)
        self.assertNotEquals(container.addBeanAfter(None, Person('Jane')), None)
        self.assertNotEquals(container.addBeanAt(0, Person('Jack')), None)

        container.addAll( [Person('Jill'), Person('Joe')] )

        self.assertTrue(container.containsId('John'))
        self.assertTrue(container.containsId('Jane'))
        self.assertTrue(container.containsId('Jack'))
        self.assertTrue(container.containsId('Jill'))
        self.assertTrue(container.containsId('Joe'))
        self.assertEquals(3, container.indexOfId('Jill'))
        self.assertEquals(4, container.indexOfId('Joe'))
        self.assertEquals(5, len(container))


    def testAddNullBeansWithResolver(self):
        container = BeanContainer(Person)
        container.setBeanIdResolver(PersonNameResolver())

        self.assertEquals(container.addBean(None), None)
        self.assertEquals(container.addBeanAfter(None, None), None)
        self.assertEquals(container.addBeanAt(0, None), None)

        self.assertEquals(0, len(container))


    def testAddBeanWithPropertyResolver(self):
        container = BeanContainer(Person)
        container.setBeanIdProperty('name')

        self.assertNotEquals(container.addBean(Person('John')), None)
        self.assertNotEquals(container.addBeanAfter(None, Person('Jane')), None)
        self.assertNotEquals(container.addBeanAt(0, Person('Jack')), None)

        container.addAll( [Person('Jill'), Person('Joe')] )

        self.assertTrue(container.containsId('John'))
        self.assertTrue(container.containsId('Jane'))
        self.assertTrue(container.containsId('Jack'))
        self.assertTrue(container.containsId('Jill'))
        self.assertTrue(container.containsId('Joe'))
        self.assertEquals(3, container.indexOfId('Jill'))
        self.assertEquals(4, container.indexOfId('Joe'))
        self.assertEquals(5, len(container))


    def testAddNestedContainerProperty(self):
        container = BeanContainer(NestedMethodPropertyTest.Person)
        container.setBeanIdProperty('name')

        container.addBean(NestedMethodPropertyTest.Person('John',
                NestedMethodPropertyTest.Address('Ruukinkatu 2-4', 20540)))

        self.assertTrue(container.addNestedContainerProperty('address.street'))
        self.assertEquals('Ruukinkatu 2-4',
                container.getContainerProperty('John',
                        'address.street').getValue())
