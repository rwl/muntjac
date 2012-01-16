# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.absolute_layout import AbsoluteLayout
from muntjac.event.layout_events import LayoutClickEvent, ILayoutClickListener


class AbsoluteLayoutListeners(AbstractListenerMethodsTest):

    def testLayoutClickListenerAddGetRemove(self):
        self._testListenerAddGetRemove(AbsoluteLayout,
                LayoutClickEvent, ILayoutClickListener)
