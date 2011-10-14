# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.data.util.BeanItemContainer import (BeanItemContainer,)


class TestAbstractBeanContainerListeners(AbstractListenerMethodsTest):

    def testPropertySetChangeListenerAddGetRemove(self):
        self.testListenerAddGetRemove(BeanItemContainer, PropertySetChangeEvent, PropertySetChangeListener, BeanItemContainer(PropertySetChangeListener))
