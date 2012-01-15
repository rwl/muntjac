# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.button import Button

from muntjac.data.property import \
    IReadOnlyStatusChangeEvent, IReadOnlyStatusChangeListener, \
    ValueChangeEvent, IValueChangeListener


class TestAbstractFieldListeners(AbstractListenerMethodsTest):

    def testReadOnlyStatusChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Button, IReadOnlyStatusChangeEvent,
                IReadOnlyStatusChangeListener)

    def testValueChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Button, ValueChangeEvent,
                IValueChangeListener)
