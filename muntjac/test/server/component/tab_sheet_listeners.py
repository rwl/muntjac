# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.tab_sheet import \
    TabSheet, SelectedTabChangeEvent, ISelectedTabChangeListener


class TabSheetListeners(AbstractListenerMethodsTest):

    def testSelectedTabChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(TabSheet, SelectedTabChangeEvent,
                ISelectedTabChangeListener)
