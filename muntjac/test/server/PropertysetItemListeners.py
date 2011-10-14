# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.data.Item.PropertySetChangeEvent import (PropertySetChangeEvent,)
# from com.vaadin.data.Item.PropertySetChangeListener import (PropertySetChangeListener,)
# from com.vaadin.data.util.PropertysetItem import (PropertysetItem,)


class PropertysetItemListeners(AbstractListenerMethodsTest):

    def testPropertySetChangeListenerAddGetRemove(self):
        self.testListenerAddGetRemove(PropertysetItem, PropertySetChangeEvent, PropertySetChangeListener)
