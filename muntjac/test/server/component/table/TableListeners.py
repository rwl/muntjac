# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.event.ItemClickEvent import (ItemClickEvent,)
# from com.vaadin.event.ItemClickEvent.ItemClickListener import (ItemClickListener,)
# from com.vaadin.ui.Table.ColumnReorderEvent import (ColumnReorderEvent,)
# from com.vaadin.ui.Table.ColumnReorderListener import (ColumnReorderListener,)
# from com.vaadin.ui.Table.ColumnResizeEvent import (ColumnResizeEvent,)
# from com.vaadin.ui.Table.ColumnResizeListener import (ColumnResizeListener,)
# from com.vaadin.ui.Table.FooterClickEvent import (FooterClickEvent,)
# from com.vaadin.ui.Table.FooterClickListener import (FooterClickListener,)
# from com.vaadin.ui.Table.HeaderClickEvent import (HeaderClickEvent,)
# from com.vaadin.ui.Table.HeaderClickListener import (HeaderClickListener,)


class TableListeners(AbstractListenerMethodsTest):

    def testColumnResizeListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Table, ColumnResizeEvent, ColumnResizeListener)

    def testItemClickListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Table, ItemClickEvent, ItemClickListener)

    def testFooterClickListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Table, FooterClickEvent, FooterClickListener)

    def testHeaderClickListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Table, HeaderClickEvent, HeaderClickListener)

    def testColumnReorderListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Table, ColumnReorderEvent, ColumnReorderListener)
