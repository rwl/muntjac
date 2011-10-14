# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.data.Container.ItemSetChangeEvent import (ItemSetChangeEvent,)
# from com.vaadin.data.Container.ItemSetChangeListener import (ItemSetChangeListener,)
# from com.vaadin.data.Container.PropertySetChangeEvent import (PropertySetChangeEvent,)
# from com.vaadin.data.Container.PropertySetChangeListener import (PropertySetChangeListener,)
# from com.vaadin.ui.ComboBox import (ComboBox,)


class TestAbstractSelectListeners(AbstractListenerMethodsTest):

    def testItemSetChangeListenerAddGetRemove(self):
        self.testListenerAddGetRemove(ComboBox, ItemSetChangeEvent, ItemSetChangeListener)

    def testPropertySetChangeListenerAddGetRemove(self):
        self.testListenerAddGetRemove(ComboBox, PropertySetChangeEvent, PropertySetChangeListener)
