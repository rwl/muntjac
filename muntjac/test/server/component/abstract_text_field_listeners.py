# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.text_field import TextField

from muntjac.event.field_events import \
    TextChangeEvent, ITextChangeListener, FocusEvent, IFocusListener, \
    BlurEvent, IBlurListener


class TestAbstractTextFieldListeners(AbstractListenerMethodsTest):

    def testTextChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(TextField, TextChangeEvent,
                ITextChangeListener)


    def testFocusListenerAddGetRemove(self):
        self._testListenerAddGetRemove(TextField, FocusEvent, IFocusListener)


    def testBlurListenerAddGetRemove(self):
        self._testListenerAddGetRemove(TextField, BlurEvent, IBlurListener)
