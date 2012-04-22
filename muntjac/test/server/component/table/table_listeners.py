# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.table import \
    (Table, ColumnResizeEvent, IColumnResizeListener, FooterClickEvent,
     IFooterClickListener, HeaderClickEvent, IHeaderClickListener,
     ColumnReorderEvent, IColumnReorderListener)

from muntjac.event.item_click_event import ItemClickEvent, IItemClickListener



class TableListeners(AbstractListenerMethodsTest):

    def testColumnResizeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Table, ColumnResizeEvent,
                IColumnResizeListener)


    def testItemClickListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Table, ItemClickEvent,
                IItemClickListener)


    def testFooterClickListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Table, FooterClickEvent,
                IFooterClickListener)


    def testHeaderClickListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Table, HeaderClickEvent,
                IHeaderClickListener)


    def testColumnReorderListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Table, ColumnReorderEvent,
                IColumnReorderListener)
