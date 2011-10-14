# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.data.Property.ReadOnlyStatusChangeEvent import (ReadOnlyStatusChangeEvent,)
# from com.vaadin.data.Property.ReadOnlyStatusChangeListener import (ReadOnlyStatusChangeListener,)
# from com.vaadin.data.Property.ValueChangeEvent import (ValueChangeEvent,)
# from com.vaadin.data.Property.ValueChangeListener import (ValueChangeListener,)


class TestAbstractFieldListeners(AbstractListenerMethodsTest):

    def testReadOnlyStatusChangeListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Button, ReadOnlyStatusChangeEvent, ReadOnlyStatusChangeListener)

    def testValueChangeListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Button, ValueChangeEvent, ValueChangeListener)
