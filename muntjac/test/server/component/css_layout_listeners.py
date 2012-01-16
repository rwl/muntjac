# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.css_layout import CssLayout

from muntjac.event.layout_events import LayoutClickEvent, ILayoutClickListener


class CssLayoutListeners(AbstractListenerMethodsTest):

    def testLayoutClickListenerAddGetRemove(self):
        self._testListenerAddGetRemove(CssLayout, LayoutClickEvent,
                ILayoutClickListener)
