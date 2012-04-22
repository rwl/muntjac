# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.select import Select

from muntjac.event.field_events import \
    FocusEvent, IFocusListener, BlurEvent, IBlurListener


class SelectListeners(AbstractListenerMethodsTest):

    def testFocusListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Select, FocusEvent, IFocusListener)


    def testBlurListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Select, BlurEvent, IBlurListener)
