# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.vertical_layout import VerticalLayout
from muntjac.event.layout_events import LayoutClickEvent, ILayoutClickListener


class TestAbstractOrderedLayoutListeners(AbstractListenerMethodsTest):

    def testLayoutClickListenerAddGetRemove(self):
        self._testListenerAddGetRemove(VerticalLayout, LayoutClickEvent,
                ILayoutClickListener)
