# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.data.Container.PropertySetChangeEvent import (PropertySetChangeEvent,)
# from com.vaadin.data.Container.PropertySetChangeListener import (PropertySetChangeListener,)
# from com.vaadin.data.Property.ValueChangeEvent import (ValueChangeEvent,)
# from com.vaadin.data.Property.ValueChangeListener import (ValueChangeListener,)
# from com.vaadin.data.util.IndexedContainer import (IndexedContainer,)


class IndexedContainerListeners(AbstractListenerMethodsTest):

    def testValueChangeListenerAddGetRemove(self):
        self.testListenerAddGetRemove(IndexedContainer, ValueChangeEvent, ValueChangeListener)

    def testPropertySetChangeListenerAddGetRemove(self):
        self.testListenerAddGetRemove(IndexedContainer, PropertySetChangeEvent, PropertySetChangeListener)
