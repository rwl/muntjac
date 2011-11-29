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

from com.vaadin.terminal.gwt.client.VTooltip import (VTooltip,)
from com.vaadin.terminal.gwt.client.ui.VOptionGroupBase import (VOptionGroupBase,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Iterator import (Iterator,)


class VListSelect(VOptionGroupBase):
    CLASSNAME = 'v-select'
    _VISIBLE_COUNT = 10
    select = None
    _lastSelectedIndex = -1

    def __init__(self):
        super(VListSelect, self)(self.TooltipListBox(True), self.CLASSNAME)
        self.select = self.optionsContainer
        self.select.setSelect(self)
        self.select.addChangeHandler(self)
        self.select.addClickHandler(self)
        self.select.setStyleName(self.CLASSNAME + '-select')
        self.select.setVisibleItemCount(self._VISIBLE_COUNT)

    def buildOptions(self, uidl):
        self.select.setClient(self.client)
        self.select.setMultipleSelect(self.isMultiselect())
        self.select.setEnabled(not self.isDisabled() and not self.isReadonly())
        self.select.clear()
        if (
            not self.isMultiselect() and self.isNullSelectionAllowed() and not self.isNullSelectionItemAvailable()
        ):
            # can't unselect last item in singleselect mode
            self.select.addItem('', None)
        _0 = True
        i = uidl.getChildIterator()
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            optionUidl = i.next()
            self.select.addItem(optionUidl.getStringAttribute('caption'), optionUidl.getStringAttribute('key'))
            if optionUidl.hasAttribute('selected'):
                itemIndex = self.select.getItemCount() - 1
                self.select.setItemSelected(itemIndex, True)
                self._lastSelectedIndex = itemIndex
        if self.getRows() > 0:
            self.select.setVisibleItemCount(self.getRows())

    def getSelectedItems(self):
        selectedItemKeys = list()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < self.select.getItemCount()):
                break
            if self.select.isItemSelected(i):
                selectedItemKeys.add(self.select.getValue(i))
        return list([None] * len(selectedItemKeys))

    def onChange(self, event):
        si = self.select.getSelectedIndex()
        if si == -1 and not self.isNullSelectionAllowed():
            self.select.setSelectedIndex(self._lastSelectedIndex)
        else:
            self._lastSelectedIndex = si
            if self.isMultiselect():
                self.client.updateVariable(self.id, 'selected', self.getSelectedItems(), self.isImmediate())
            else:
                self.client.updateVariable(self.id, 'selected', ['' + self.getSelectedItem()], self.isImmediate())

    def setHeight(self, height):
        self.select.setHeight(height)
        super(VListSelect, self).setHeight(height)

    def setWidth(self, width):
        self.select.setWidth(width)
        super(VListSelect, self).setWidth(width)

    def setTabIndex(self, tabIndex):
        self.optionsContainer.setTabIndex(tabIndex)

    def focus(self):
        self.select.setFocus(True)


class TooltipListBox(ListBox):
    """Extended ListBox to listen tooltip events and forward them to generic
    handler.
    """
    _client = None
    _pntbl = None

    def __init__(self, isMultiselect):
        super(TooltipListBox, self)(isMultiselect)
        self.sinkEvents(VTooltip.TOOLTIP_EVENTS)

    def setClient(self, client):
        self._client = client

    def setSelect(self, s):
        self._pntbl = s

    def onBrowserEvent(self, event):
        super(TooltipListBox, self).onBrowserEvent(event)
        if self._client is not None:
            self._client.handleTooltipEvent(event, self._pntbl)
