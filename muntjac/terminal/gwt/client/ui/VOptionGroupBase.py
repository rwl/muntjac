# Copyright (C) 2011 Vaadin Ltd
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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.ui.Field import (Field,)
from com.vaadin.terminal.gwt.client.Focusable import (Focusable,)
from com.vaadin.terminal.gwt.client.ui.VNativeButton import (VNativeButton,)
from com.vaadin.terminal.gwt.client.ui.VTextField import (VTextField,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
# from com.google.gwt.event.dom.client.ChangeHandler import (ChangeHandler,)
# from com.google.gwt.user.client.ui.Panel import (Panel,)
# from java.util.Set import (Set,)


class VOptionGroupBase(Composite, Paintable, Field, ClickHandler, ChangeHandler, KeyPressHandler, Focusable):
    CLASSNAME_OPTION = 'v-select-option'
    client = None
    id = None
    selectedKeys = None
    _immediate = None
    _multiselect = None
    _disabled = None
    _readonly = None
    _cols = 0
    _rows = 0
    _nullSelectionAllowed = True
    _nullSelectionItemAvailable = False
    # Widget holding the different options (e.g. ListBox or Panel for radio
    # buttons) (optional, fallbacks to container Panel)

    optionsContainer = None
    # Panel containing the component
    _container = None
    _newItemField = None
    _newItemButton = None

    def __init__(self, *args):
        # Call this if you wish to specify your own container for the option
        # elements (e.g. SELECT)

        _0 = args
        _1 = len(args)
        if _1 == 1:
            classname, = _0
            self._container = self.FlowPanel()
            self.initWidget(self._container)
            self.optionsContainer = self._container
            self._container.setStyleName(classname)
            self._immediate = False
            self._multiselect = False
        elif _1 == 2:
            w, classname = _0
            self.__init__(classname)
            self.optionsContainer = w
            self._container.add(self.optionsContainer)
        else:
            raise ARGERROR(1, 2)

    def isImmediate(self):
        return self._immediate

    def isMultiselect(self):
        return self._multiselect

    def isDisabled(self):
        return self._disabled

    def isReadonly(self):
        return self._readonly

    def isNullSelectionAllowed(self):
        return self._nullSelectionAllowed

    def isNullSelectionItemAvailable(self):
        return self._nullSelectionItemAvailable

    def getColumns(self):
        """@return "cols" specified in uidl, 0 if not specified"""
        return self._cols

    def getRows(self):
        """@return "rows" specified in uidl, 0 if not specified"""
        return self._rows

    def updateFromUIDL(self, uidl, client):
        self.client = client
        self.id = uidl.getId()
        if client.updateComponent(self, uidl, True):
            return
        self.selectedKeys = uidl.getStringArrayVariableAsSet('selected')
        self._readonly = uidl.getBooleanAttribute('readonly')
        self._disabled = uidl.getBooleanAttribute('disabled')
        self._multiselect = 'multi' == uidl.getStringAttribute('selectmode')
        self._immediate = uidl.getBooleanAttribute('immediate')
        self._nullSelectionAllowed = uidl.getBooleanAttribute('nullselect')
        self._nullSelectionItemAvailable = uidl.getBooleanAttribute('nullselectitem')
        if uidl.hasAttribute('cols'):
            self._cols = uidl.getIntAttribute('cols')
        if uidl.hasAttribute('rows'):
            self._rows = uidl.getIntAttribute('rows')
        ops = uidl.getChildUIDL(0)
        if self.getColumns() > 0:
            self._container.setWidth(self.getColumns() + 'em')
            if self._container != self.optionsContainer:
                self.optionsContainer.setWidth('100%')
        self.buildOptions(ops)
        if uidl.getBooleanAttribute('allownewitem'):
            if self._newItemField is None:
                self._newItemButton = VNativeButton()
                self._newItemButton.setText('+')
                self._newItemButton.addClickHandler(self)
                self._newItemField = VTextField()
                self._newItemField.addKeyPressHandler(self)
            self._newItemField.setEnabled(not self._disabled and not self._readonly)
            self._newItemButton.setEnabled(not self._disabled and not self._readonly)
            if (
                (self._newItemField is None) or (self._newItemField.getParent() != self._container)
            ):
                self._container.add(self._newItemField)
                self._container.add(self._newItemButton)
                w = self._container.getOffsetWidth() - self._newItemButton.getOffsetWidth()
                self._newItemField.setWidth(self.Math.max(w, 0) + 'px')
        elif self._newItemField is not None:
            self._container.remove(self._newItemField)
            self._container.remove(self._newItemButton)
        self.setTabIndex(uidl.getIntAttribute('tabindex') if uidl.hasAttribute('tabindex') else 0)

    def setTabIndex(self, tabIndex):
        pass

    def onClick(self, event):
        if (
            event.getSource() == self._newItemButton and not (self._newItemField.getText() == '')
        ):
            self.client.updateVariable(self.id, 'newitem', self._newItemField.getText(), True)
            self._newItemField.setText('')

    def onChange(self, event):
        if self._multiselect:
            self.client.updateVariable(self.id, 'selected', self.getSelectedItems(), self._immediate)
        else:
            self.client.updateVariable(self.id, 'selected', ['' + self.getSelectedItem()], self._immediate)

    def onKeyPress(self, event):
        if (
            event.getSource() == self._newItemField and event.getCharCode() == self.KeyCodes.KEY_ENTER
        ):
            self._newItemButton.click()

    def buildOptions(self, uidl):
        pass

    def getSelectedItems(self):
        pass

    def getSelectedItem(self):
        sel = self.getSelectedItems()
        if len(sel) > 0:
            return sel[0]
        else:
            return None
