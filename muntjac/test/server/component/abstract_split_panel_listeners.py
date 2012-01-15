# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.horizontal_split_panel import HorizontalSplitPanel

from muntjac.ui.abstract_split_panel import \
    SplitterClickEvent, ISplitterClickListener


class TestAbstractSplitPanelListeners(AbstractListenerMethodsTest):

    def testSplitterClickListenerAddGetRemove(self):
        self._testListenerAddGetRemove(HorizontalSplitPanel,
                SplitterClickEvent, ISplitterClickListener)
