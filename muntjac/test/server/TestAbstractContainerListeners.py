# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)


class TestAbstractContainerListeners(AbstractListenerMethodsTest):

    def testItemSetChangeListenerAddGetRemove(self):
        self.testListenerAddGetRemove(IndexedContainer, ItemSetChangeEvent, ItemSetChangeListener)

    def testPropertySetChangeListenerAddGetRemove(self):
        self.testListenerAddGetRemove(IndexedContainer, PropertySetChangeEvent, PropertySetChangeListener)
