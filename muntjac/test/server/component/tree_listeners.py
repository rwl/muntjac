# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.tree import \
    Tree, ExpandEvent, IExpandListener, CollapseEvent, ICollapseListener

from muntjac.event.item_click_event import ItemClickEvent, IItemClickListener


class TreeListeners(AbstractListenerMethodsTest):

    def testExpandListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Tree, ExpandEvent, IExpandListener)


    def testItemClickListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Tree, ItemClickEvent, IItemClickListener)


    def testCollapseListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Tree, CollapseEvent, ICollapseListener)
