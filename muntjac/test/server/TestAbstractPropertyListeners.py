# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.data.Property.ReadOnlyStatusChangeEvent import (ReadOnlyStatusChangeEvent,)
# from com.vaadin.data.Property.ReadOnlyStatusChangeListener import (ReadOnlyStatusChangeListener,)
# from com.vaadin.data.util.AbstractProperty import (AbstractProperty,)
# from com.vaadin.data.util.ObjectProperty import (ObjectProperty,)


class TestAbstractPropertyListeners(AbstractListenerMethodsTest):

    def testValueChangeListenerAddGetRemove(self):
        self.testListenerAddGetRemove(AbstractProperty, ValueChangeEvent, ValueChangeListener, ObjectProperty(''))

    def testReadOnlyStatusChangeListenerAddGetRemove(self):
        self.testListenerAddGetRemove(AbstractProperty, ReadOnlyStatusChangeEvent, ReadOnlyStatusChangeListener, ObjectProperty(''))
