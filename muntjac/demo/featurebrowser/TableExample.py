# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.demo.featurebrowser.GeneratedColumnExample import (GeneratedColumnExample,)
# from com.vaadin.data.Item import (Item,)
# from com.vaadin.data.Property import (Property,)
# from com.vaadin.event.Action import (Action,)
# from com.vaadin.ui.Button import (Button,)
# from com.vaadin.ui.Button.ClickEvent import (ClickEvent,)
# from com.vaadin.ui.CheckBox import (CheckBox,)
# from com.vaadin.ui.HorizontalLayout import (HorizontalLayout,)
# from com.vaadin.ui.Table import (Table,)
# from com.vaadin.ui.themes.BaseTheme import (BaseTheme,)
# from java.util.Iterator import (Iterator,)
# from java.util.Random import (Random,)
# from java.util.Set import (Set,)


class TableExample(CustomComponent, Action.Handler, Button.ClickListener):
    """Table example.

    @author IT Mill Ltd.
    """
    # Actions
    _ACTION_SAVE = Action('Save')
    _ACTION_DELETE = Action('Delete')
    _ACTION_HIRE = Action('Hire')
    # Action sets
    _ACTIONS_NOHIRE = [_ACTION_SAVE, _ACTION_DELETE]
    _ACTIONS_HIRE = [_ACTION_HIRE, _ACTION_SAVE, _ACTION_DELETE]
    # Properties
    _PROPERTY_SPECIES = 'Species'
    _PROPERTY_TYPE = 'Type'
    _PROPERTY_KIND = 'Kind'
    _PROPERTY_HIRED = 'Hired'
    # "global" components
    _source = None
    _saved = None
    _saveSelected = None
    _hireSelected = None
    _deleteSelected = None
    _deselect = None

    def __init__(self):
        # set up the properties (columns)
        margin = VerticalLayout()
        margin.setMargin(True)
        root = TabSheet()
        self.setCompositionRoot(margin)
        margin.addComponent(root)
        # main layout
        main = VerticalLayout()
        main.setCaption('Basic Table')
        main.setMargin(True)
        root.addTab(main)
        # "source" table with bells & whistlesenabled
        self._source = Table('All creatures')
        self._source.setPageLength(7)
        self._source.setWidth('550px')
        self._source.setColumnCollapsingAllowed(True)
        self._source.setColumnReorderingAllowed(True)
        self._source.setSelectable(True)
        self._source.setMultiSelect(True)
        self._source.setRowHeaderMode(Table.ROW_HEADER_MODE_ID)
        self.fillTable(self._source)
        self._source.addActionHandler(self)
        main.addComponent(self._source)
        # x-selected button row
        horiz = HorizontalLayout()
        horiz.setMargin(False, False, True, False)
        main.addComponent(horiz)
        self._saveSelected = Button('Save selected')
        self._saveSelected.setStyleName(BaseTheme.BUTTON_LINK)
        self._saveSelected.addListener(self)
        horiz.addComponent(self._saveSelected)
        self._hireSelected = Button('Hire selected')
        self._hireSelected.setStyleName(BaseTheme.BUTTON_LINK)
        self._hireSelected.addListener(self)
        horiz.addComponent(self._hireSelected)
        self._deleteSelected = Button('Delete selected')
        self._deleteSelected.setStyleName(BaseTheme.BUTTON_LINK)
        self._deleteSelected.addListener(self)
        horiz.addComponent(self._deleteSelected)
        self._deselect = Button('Deselect all')
        self._deselect.setStyleName(BaseTheme.BUTTON_LINK)
        self._deselect.addListener(self)
        horiz.addComponent(self._deselect)
        editmode = CheckBox('Editmode ')

        class _0_(CheckBox.ClickListener):

            def buttonClick(self, event):
                TableExample_this._source.setEditable(event.getButton().getValue().booleanValue())

        _0_ = _0_()
        editmode.addListener(_0_)
        editmode.setImmediate(True)
        horiz.addComponent(editmode)
        # "saved" table, minimalistic
        self._saved = Table('Saved creatures')
        self._saved.setPageLength(5)
        self._saved.setWidth('550px')
        self._saved.setSelectable(False)
        self._saved.setColumnHeaderMode(Table.COLUMN_HEADER_MODE_HIDDEN)
        self._saved.setRowHeaderMode(Table.ROW_HEADER_MODE_ID)
        self.initProperties(self._saved)
        self._saved.addActionHandler(self)
        main.addComponent(self._saved)
        b = CheckBox('Modify saved creatures')

        class _1_(CheckBox.ClickListener):

            def buttonClick(self, event):
                TableExample_this._saved.setEditable(event.getButton().getValue().booleanValue())

        _1_ = _1_()
        b.addListener(_1_)
        b.setImmediate(True)
        main.addComponent(b)
        gencols = GeneratedColumnExample()
        gencols.setCaption('Generated Columns')
        root.addComponent(gencols)

    def initProperties(self, table):
        # fill the table with some random data
        table.addContainerProperty(self._PROPERTY_SPECIES, str, '')
        table.addContainerProperty(self._PROPERTY_TYPE, str, '')
        table.addContainerProperty(self._PROPERTY_KIND, str, '')
        table.addContainerProperty(self._PROPERTY_HIRED, bool, Boolean.FALSE.FALSE)

    def fillTable(self, table):
        # Called for each item (row), returns valid actions for that item
        self.initProperties(table)
        sp = ['Fox', 'Dog', 'Cat', 'Moose', 'Penguin', 'Cow']
        ty = ['Quick', 'Lazy', 'Sleepy', 'Fidgety', 'Crazy', 'Kewl']
        ki = ['Jumping', 'Walking', 'Sleeping', 'Skipping', 'Dancing']
        r = Random(5)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 100):
                break
            s = sp[r.nextDouble() * len(sp)]
            t = ty[r.nextDouble() * len(ty)]
            k = ki[r.nextDouble() * len(ki)]
            table.addItem([s, t, k, Boolean.FALSE.FALSE], int(i))

    def getActions(self, target, sender):
        # called when an action is invoked on an item (row)
        if sender == self._source:
            item = self._source.getItem(target)
            # save, delete, and hire if not already hired
            if (
                item is not None and item.getItemProperty(self._PROPERTY_HIRED).getValue() == Boolean.FALSE.FALSE
            ):
                return self._ACTIONS_HIRE
            else:
                return self._ACTIONS_NOHIRE
        else:
            # "saved" table only has one action
            return [self._ACTION_DELETE]

    def handleAction(self, action, sender, target):
        if sender == self._source:
            item = self._source.getItem(target)
            if action == self._ACTION_HIRE:
                # set HIRED property to true
                item.getItemProperty(self._PROPERTY_HIRED).setValue(Boolean.TRUE.TRUE)
                if self._saved.containsId(target):
                    item = self._saved.getItem(target)
                    item.getItemProperty(self._PROPERTY_HIRED).setValue(Boolean.TRUE.TRUE)
                self.getWindow().showNotification('Hired', '' + item)
            elif action == self._ACTION_SAVE:
                if self._saved.containsId(target):
                    # let's not save twice
                    self.getWindow().showNotification('Already saved', '' + item)
                    return
                # "manual" copy of the item properties we want
                added = self._saved.addItem(target)
                p = added.getItemProperty(self._PROPERTY_SPECIES)
                p.setValue(item.getItemProperty(self._PROPERTY_SPECIES).getValue())
                p = added.getItemProperty(self._PROPERTY_TYPE)
                p.setValue(item.getItemProperty(self._PROPERTY_TYPE).getValue())
                p = added.getItemProperty(self._PROPERTY_KIND)
                p.setValue(item.getItemProperty(self._PROPERTY_KIND).getValue())
                p = added.getItemProperty(self._PROPERTY_HIRED)
                p.setValue(item.getItemProperty(self._PROPERTY_HIRED).getValue())
                self.getWindow().showNotification('Saved', '' + item)
            else:
                # ACTION_DELETE
                self.getWindow().showNotification('Deleted ', '' + item)
                self._source.removeItem(target)
        elif action == self._ACTION_DELETE:
            item = self._saved.getItem(target)
            self.getWindow().showNotification('Deleted', '' + item)
            self._saved.removeItem(target)
        # sender==saved

    def buttonClick(self, event):
        b = event.getButton()
        if b == self._deselect:
            self._source.setValue(None)
        elif b == self._saveSelected:
            # loop each selected and copy to "saved" table
            selected = self._source.getValue()
            s = 0
            _0 = True
            it = selected
            while True:
                if _0 is True:
                    _0 = False
                if not it.hasNext():
                    break
                id = it.next()
                if not self._saved.containsId(id):
                    item = self._source.getItem(id)
                    added = self._saved.addItem(id)
                    # "manual" copy of the properties we want
                    p = added.getItemProperty(self._PROPERTY_SPECIES)
                    p.setValue(item.getItemProperty(self._PROPERTY_SPECIES).getValue())
                    p = added.getItemProperty(self._PROPERTY_TYPE)
                    p.setValue(item.getItemProperty(self._PROPERTY_TYPE).getValue())
                    p = added.getItemProperty(self._PROPERTY_KIND)
                    p.setValue(item.getItemProperty(self._PROPERTY_KIND).getValue())
                    p = added.getItemProperty(self._PROPERTY_HIRED)
                    p.setValue(item.getItemProperty(self._PROPERTY_HIRED).getValue())
                    s += 1
            self.getWindow().showNotification('Saved ' + s)
        elif b == self._hireSelected:
            # loop each selected and set property HIRED to true
            s = 0
            selected = self._source.getValue()
            _1 = True
            it = selected
            while True:
                if _1 is True:
                    _1 = False
                if not it.hasNext():
                    break
                id = it.next()
                item = self._source.getItem(id)
                p = item.getItemProperty(self._PROPERTY_HIRED)
                if p.getValue() == Boolean.FALSE.FALSE:
                    p.setValue(Boolean.TRUE.TRUE)
                    s += 1
                if self._saved.containsId(id):
                    # also update "saved" table
                    item = self._saved.getItem(id)
                    item.getItemProperty(self._PROPERTY_HIRED).setValue(Boolean.TRUE.TRUE)
            self.getWindow().showNotification('Hired ' + s)
        else:
            # loop trough selected and delete
            s = 0
            selected = self._source.getValue()
            _2 = True
            it = selected
            while True:
                if _2 is True:
                    _2 = False
                if not it.hasNext():
                    break
                id = it.next()
                if self._source.containsId(id):
                    s += 1
                    self._source.removeItem(id)
            self.getWindow().showNotification('Deleted ' + s)
