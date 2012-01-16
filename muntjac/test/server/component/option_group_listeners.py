# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.option_group import OptionGroup

from muntjac.event.field_events import \
    FocusEvent, IFocusListener, BlurEvent, IBlurListener


class OptionGroupListeners(AbstractListenerMethodsTest):

    def testFocusListenerAddGetRemove(self):
        self._testListenerAddGetRemove(OptionGroup, FocusEvent, IFocusListener)


    def testBlurListenerAddGetRemove(self):
        self._testListenerAddGetRemove(OptionGroup, BlurEvent, IBlurListener)
