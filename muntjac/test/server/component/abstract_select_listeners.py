# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.combo_box import ComboBox

from muntjac.data.container import \
    IItemSetChangeEvent, IItemSetChangeListener, \
    IPropertySetChangeEvent, IPropertySetChangeListener


class TestAbstractSelectListeners(AbstractListenerMethodsTest):

    def testItemSetChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(ComboBox, IItemSetChangeEvent,
                IItemSetChangeListener)


    def testPropertySetChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(ComboBox, IPropertySetChangeEvent,
                IPropertySetChangeListener)
