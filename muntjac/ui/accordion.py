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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

"""Defines a component similar to a TabSheet, but with a vertical orientation.
"""

from muntjac.ui.tab_sheet import TabSheet


class Accordion(TabSheet):
    """An accordion is a component similar to a L{TabSheet}, but
    with a vertical orientation and the selected component presented
    between tabs.

    Closable tabs are not supported by the accordion.

    The L{Accordion} can be styled with the .v-accordion, .v-accordion-item,
    .v-accordion-item-first and .v-accordion-item-caption styles.

    @see: L{TabSheet}
    """

    CLIENT_WIDGET = None #ClientWidget(VAccordion)
