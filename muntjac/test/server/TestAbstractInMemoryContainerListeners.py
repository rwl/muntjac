# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.data.Container.ItemSetChangeEvent import (ItemSetChangeEvent,)
# from com.vaadin.data.Container.ItemSetChangeListener import (ItemSetChangeListener,)


class TestAbstractInMemoryContainerListeners(AbstractListenerMethodsTest):

    def testItemSetChangeListenerAddGetRemove(self):
        self.testListenerAddGetRemove(IndexedContainer, ItemSetChangeEvent, ItemSetChangeListener)
