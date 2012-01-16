# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

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
