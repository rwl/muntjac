# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.panel import Panel
from muntjac.event.mouse_events import ClickEvent, IClickListener


class PanelListeners(AbstractListenerMethodsTest):

    def testClickListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Panel, ClickEvent, IClickListener)
