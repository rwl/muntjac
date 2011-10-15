# Copyright (C) 2010 IT Mill Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from muntjac.test.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
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
