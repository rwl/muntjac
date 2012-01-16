# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.horizontal_layout import HorizontalLayout
from muntjac.ui.vertical_layout import VerticalLayout

from muntjac.ui.component_container import \
    ComponentDetachEvent, IComponentDetachListener, \
    ComponentAttachEvent, IComponentAttachListener


class TestAbstractComponentContainerListeners(AbstractListenerMethodsTest):

    def testComponentDetachListenerAddGetRemove(self):
        self._testListenerAddGetRemove(HorizontalLayout,
                ComponentDetachEvent, IComponentDetachListener)


    def testComponentAttachListenerAddGetRemove(self):
        self._testListenerAddGetRemove(VerticalLayout,
                ComponentAttachEvent, IComponentAttachListener)
