# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.embedded import Embedded
from muntjac.event.mouse_events import ClickEvent, IClickListener


class EmbeddedListeners(AbstractListenerMethodsTest):

    def testClickListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Embedded, ClickEvent, IClickListener)
