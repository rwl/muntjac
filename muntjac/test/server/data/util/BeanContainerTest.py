# -*- coding: utf-8 -*-
from com.vaadin.data.util.NestedMethodPropertyTest import (NestedMethodPropertyTest,)
from com.vaadin.data.util.AbstractBeanContainerTest import (AbstractBeanContainerTest,)
# from com.vaadin.data.util.AbstractBeanContainer.BeanIdResolver import (BeanIdResolver,)
# from com.vaadin.data.util.BeanContainer import (BeanContainer,)
# from java.util.LinkedHashMap import (LinkedHashMap,)
# from java.util.Map import (Map,)
# from java.util.Map.Entry import (Entry,)
# from junit.framework.Assert import (Assert,)
ClassName = AbstractBeanContainerTest.ClassName
Person = AbstractBeanContainerTest.Person


class BeanContainerTest(AbstractBeanContainerTest):

    class PersonNameResolver(BeanIdResolver):

        def getIdForBean(self, bean):
            return bean.getName() if bean is not None else None

    class NullResolver(BeanIdResolver):

        def getIdForBean(self, bean):
            return None

    _nameToBean = LinkedHashMap()

    def getContainer(self):
        return BeanContainer(ClassName)

    def setUp(self):
        self._nameToBean.clear()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < self.sampleData.length):
                break
            className = ClassName(self.sampleData[i], i)
            self._nameToBean.put(self.sampleData[i], className)

    def initializeContainer(self, container):
        beanItemContainer = container
        beanItemContainer.removeAllItems()
        for entry in self._nameToBean.entrySet():
            beanItemContainer.addItem(entry.getKey(), entry.getValue())

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
        # TODO test Container.Indexed interface operation - testContainerIndexed()?
        container = BeanContainer(str)
        id = 'test1'
        item = container.addItem(id, 'value')
        self.assertNotNull(item)
        self.assertEquals(id, container.firstItemId())
        self.assertEquals(id, container.lastItemId())
        # isFirstId
        self.assertTrue(container.isFirstId(id))
        self.assertTrue(container.isFirstId(container.firstItemId()))
        # isLastId
        self.assertTrue(container.isLastId(id))
        self.assertTrue(container.isLastId(container.lastItemId()))
        # Add a new item before the first
        # addItemAfter
        newFirstId = 'newFirst'
        item = container.addItemAfter(None, newFirstId, 'newFirstValue')
        self.assertNotNull(item)
        self.assertNotNull(container.getItem(newFirstId))
        # isFirstId
        self.assertTrue(container.isFirstId(newFirstId))
        self.assertTrue(container.isFirstId(container.firstItemId()))
        # isLastId
        self.assertTrue(container.isLastId(id))
        self.assertTrue(container.isLastId(container.lastItemId()))
        # nextItemId
        self.assertEquals(id, container.nextItemId(newFirstId))
        self.assertNull(container.nextItemId(id))
        self.assertNull(container.nextItemId('not-in-container'))
        # prevItemId
        self.assertEquals(newFirstId, container.prevItemId(id))
        self.assertNull(container.prevItemId(newFirstId))
        self.assertNull(container.prevItemId('not-in-container'))
        # addItemAfter(IDTYPE, IDTYPE, BT)
        newSecondItemId = 'newSecond'
        item = container.addItemAfter(newFirstId, newSecondItemId, 'newSecondValue')
        # order is now: newFirstId, newSecondItemId, id
        self.assertNotNull(item)
        self.assertNotNull(container.getItem(newSecondItemId))
        self.assertEquals(id, container.nextItemId(newSecondItemId))
        self.assertEquals(newFirstId, container.prevItemId(newSecondItemId))
        # addItemAfter(IDTYPE, IDTYPE, BT)
        fourthId = 'id of the fourth item'
        fourth = container.addItemAfter(newFirstId, fourthId, 'fourthValue')
        # order is now: newFirstId, fourthId, newSecondItemId, id
        self.assertNotNull(fourth)
        self.assertEquals(fourth, container.getItem(fourthId))
        self.assertEquals(newSecondItemId, container.nextItemId(fourthId))
        self.assertEquals(newFirstId, container.prevItemId(fourthId))
        # addItemAfter(IDTYPE, IDTYPE, BT)
        fifthId = 'fifth'
        fifth = container.addItemAfter(None, fifthId, 'fifthValue')
        # order is now: fifthId, newFirstId, fourthId, newSecondItemId, id
        self.assertNotNull(fifth)
        self.assertEquals(fifth, container.getItem(fifthId))
        self.assertEquals(newFirstId, container.nextItemId(fifthId))
        self.assertNull(container.prevItemId(fifthId))

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
        self.assertNull(container.addItemAt(-1, 'id5', 'value5'))
        self.assertNull(container.addItemAt(len(container) + 1, 'id6', 'value6'))
        self.assertEquals(4, len(container))
        self.assertEquals('id2', container.getIdByIndex(0))
        self.assertEquals('id3', container.getIdByIndex(1))
        self.assertEquals('id1', container.getIdByIndex(2))
        self.assertEquals('id4', container.getIdByIndex(3))

    def testUnsupportedMethods(self):
        container = BeanContainer(Person)
        container.addItem('John', Person('John'))
        # should get exception
        try:
            container.addItem()
            Assert.fail()
        except self.UnsupportedOperationException, e:
            pass # astStmt: [Stmt([]), None]
        # should get exception
        try:
            container.addItem(None)
            Assert.fail()
        except self.UnsupportedOperationException, e:
            pass # astStmt: [Stmt([]), None]
        # should get exception
        try:
            container.addItemAfter(None, None)
            Assert.fail()
        except self.UnsupportedOperationException, e:
            pass # astStmt: [Stmt([]), None]
        # should get exception
        try:
            container.addItemAfter(Person('Jane'))
            Assert.fail()
        except self.UnsupportedOperationException, e:
            pass # astStmt: [Stmt([]), None]
        # should get exception
        try:
            container.addItemAt(0)
            Assert.fail()
        except self.UnsupportedOperationException, e:
            pass # astStmt: [Stmt([]), None]
        # should get exception
        try:
            container.addItemAt(0, Person('Jane'))
            Assert.fail()
        except self.UnsupportedOperationException, e:
            pass # astStmt: [Stmt([]), None]
        # should get exception
        try:
            container.addContainerProperty('lastName', str, '')
            Assert.fail()
        except self.UnsupportedOperationException, e:
            pass # astStmt: [Stmt([]), None]
        self.assertEquals(1, len(container))

    def testRemoveContainerProperty(self):
        container = BeanContainer(Person)
        container.setBeanIdResolver(self.PersonNameResolver())
        container.addBean(Person('John'))
        Assert.assertEquals('John', container.getContainerProperty('John', 'name').getValue())
        Assert.assertTrue(container.removeContainerProperty('name'))
        Assert.assertNull(container.getContainerProperty('John', 'name'))
        Assert.assertNotNull(container.getItem('John'))
        # property removed also from item
        Assert.assertNull(container.getItem('John').getItemProperty('name'))

    def testAddNullBeans(self):
        container = BeanContainer(Person)
        self.assertNull(container.addItem('id1', None))
        self.assertNull(container.addItemAfter(None, 'id2', None))
        self.assertNull(container.addItemAt(0, 'id3', None))
        self.assertEquals(0, len(container))

    def testAddNullId(self):
        container = BeanContainer(Person)
        john = Person('John')
        self.assertNull(container.addItem(None, john))
        self.assertNull(container.addItemAfter(None, None, john))
        self.assertNull(container.addItemAt(0, None, john))
        self.assertEquals(0, len(container))

    def testEmptyContainer(self):
        container = BeanContainer(Person)
        self.assertNull(container.firstItemId())
        self.assertNull(container.lastItemId())
        self.assertEquals(0, len(container))
        # could test more about empty container

    def testAddBeanWithoutResolver(self):
        container = BeanContainer(Person)
        # should get exception
        try:
            container.addBean(Person('John'))
            Assert.fail()
        except self.IllegalStateException, e:
            pass # astStmt: [Stmt([]), None]
        # should get exception
        try:
            container.addBeanAfter(None, Person('Jane'))
            Assert.fail()
        except self.IllegalStateException, e:
            pass # astStmt: [Stmt([]), None]
        # should get exception
        try:
            container.addBeanAt(0, Person('Jack'))
            Assert.fail()
        except self.IllegalStateException, e:
            pass # astStmt: [Stmt([]), None]
        # should get exception
        try:
            container.addAll(Arrays.asList([Person('Jack')]))
            Assert.fail()
        except self.IllegalStateException, e:
            pass # astStmt: [Stmt([]), None]
        self.assertEquals(0, len(container))

    def testAddBeanWithNullResolver(self):
        container = BeanContainer(Person)
        # resolver that returns null as item id
        container.setBeanIdResolver(self.NullResolver())
        # should get exception
        try:
            container.addBean(Person('John'))
            Assert.fail()
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]
        # should get exception
        try:
            container.addBeanAfter(None, Person('Jane'))
            Assert.fail()
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]
        # should get exception
        try:
            container.addBeanAt(0, Person('Jack'))
            Assert.fail()
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]
        self.assertEquals(0, len(container))

    def testAddBeanWithResolver(self):
        container = BeanContainer(Person)
        container.setBeanIdResolver(self.PersonNameResolver())
        self.assertNotNull(container.addBean(Person('John')))
        self.assertNotNull(container.addBeanAfter(None, Person('Jane')))
        self.assertNotNull(container.addBeanAt(0, Person('Jack')))
        container.addAll(Arrays.asList([Person('Jill'), Person('Joe')]))
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
        container.setBeanIdResolver(self.PersonNameResolver())
        self.assertNull(container.addBean(None))
        self.assertNull(container.addBeanAfter(None, None))
        self.assertNull(container.addBeanAt(0, None))
        self.assertEquals(0, len(container))

    def testAddBeanWithPropertyResolver(self):
        container = BeanContainer(Person)
        container.setBeanIdProperty('name')
        self.assertNotNull(container.addBean(Person('John')))
        self.assertNotNull(container.addBeanAfter(None, Person('Jane')))
        self.assertNotNull(container.addBeanAt(0, Person('Jack')))
        container.addAll(Arrays.asList([Person('Jill'), Person('Joe')]))
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
        container.addBean(NestedMethodPropertyTest.Person('John', NestedMethodPropertyTest.Address('Ruukinkatu 2-4', 20540)))
        self.assertTrue(container.addNestedContainerProperty('address.street'))
        self.assertEquals('Ruukinkatu 2-4', container.getContainerProperty('John', 'address.street').getValue())
