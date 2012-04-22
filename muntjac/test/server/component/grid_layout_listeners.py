# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.grid_layout import GridLayout
from muntjac.event.layout_events import LayoutClickEvent, ILayoutClickListener


class GridLayoutListeners(AbstractListenerMethodsTest):

    def testLayoutClickListenerAddGetRemove(self):
        self._testListenerAddGetRemove(GridLayout, LayoutClickEvent,
                ILayoutClickListener)
