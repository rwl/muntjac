# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.label import Label, ValueChangeEvent
from muntjac.data.property import IValueChangeListener


class LabelListeners(AbstractListenerMethodsTest):

    def testValueChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Label, ValueChangeEvent,
                IValueChangeListener)
