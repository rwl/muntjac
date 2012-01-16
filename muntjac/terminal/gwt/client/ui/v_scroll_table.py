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


class VScrollTable(object):

    ITEM_CLICK_EVENT_ID = 'itemClick'
    HEADER_CLICK_EVENT_ID = 'handleHeaderClick'
    FOOTER_CLICK_EVENT_ID = 'handleFooterClick'
    COLUMN_RESIZE_EVENT_ID = 'columnResize'
    COLUMN_REORDER_EVENT_ID = 'columnReorder'

    ATTRIBUTE_PAGEBUFFER_FIRST = "pb-ft"
    ATTRIBUTE_PAGEBUFFER_LAST = "pb-l"
