# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.event.FieldEvents.BlurEvent import (BlurEvent,)
# from com.vaadin.event.FieldEvents.BlurListener import (BlurListener,)
# from com.vaadin.event.FieldEvents.FocusEvent import (FocusEvent,)
# from com.vaadin.event.FieldEvents.FocusListener import (FocusListener,)
# from com.vaadin.event.FieldEvents.TextChangeEvent import (TextChangeEvent,)
# from com.vaadin.event.FieldEvents.TextChangeListener import (TextChangeListener,)
# from com.vaadin.ui.TextField import (TextField,)


class TestAbstractTextFieldListeners(AbstractListenerMethodsTest):

    def testTextChangeListenerAddGetRemove(self):
        self.testListenerAddGetRemove(TextField, TextChangeEvent, TextChangeListener)

    def testFocusListenerAddGetRemove(self):
        self.testListenerAddGetRemove(TextField, FocusEvent, FocusListener)

    def testBlurListenerAddGetRemove(self):
        self.testListenerAddGetRemove(TextField, BlurEvent, BlurListener)
