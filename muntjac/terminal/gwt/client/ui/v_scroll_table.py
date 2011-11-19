# Copyright (C) 2011 Vaadin Ltd.
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


class VScrollTable(object):

    ITEM_CLICK_EVENT_ID = 'itemClick'
    HEADER_CLICK_EVENT_ID = 'handleHeaderClick'
    FOOTER_CLICK_EVENT_ID = 'handleFooterClick'
    COLUMN_RESIZE_EVENT_ID = 'columnResize'
    COLUMN_REORDER_EVENT_ID = 'columnReorder'

    ATTRIBUTE_PAGEBUFFER_FIRST = "pb-ft"
    ATTRIBUTE_PAGEBUFFER_LAST = "pb-l"
