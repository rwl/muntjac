# -*- coding: utf-8 -*-
from muntjac.demo.sampler.ExampleUtil import (ExampleUtil,)
# from com.vaadin.event.ItemClickEvent import (ItemClickEvent,)
# from com.vaadin.event.ItemClickEvent.ItemClickListener import (ItemClickListener,)
# from com.vaadin.ui.Link import (Link,)
# from java.util.HashMap import (HashMap,)


class TableStylingExample(VerticalLayout):
    _table = Table()
    _markedRows = dict()
    _markedCells = dict()
    ACTION_RED = Action('red')
    ACTION_BLUE = Action('blue')
    ACTION_GREEN = Action('green')
    ACTION_NONE = Action('none')
    ACTIONS = [ACTION_RED, ACTION_GREEN, ACTION_BLUE, ACTION_NONE]

    def __init__(self):
        self.setSpacing(True)
        self.addComponent(self._table)
        # set a style name, so we can style rows and cells
        self._table.setStyleName('contacts')
        # size
        self._table.setWidth('100%')
        self._table.setPageLength(7)
        # connect data source
        self._table.setContainerDataSource(ExampleUtil.getPersonContainer())
        # Generate the email-link from firstname & lastname

        class _0_(Table.ColumnGenerator):

            def generateCell(self, source, itemId, columnId):
                item = TableStylingExample_this._table.getItem(itemId)
                fn = item.getItemProperty(ExampleUtil.PERSON_PROPERTY_FIRSTNAME).getValue()
                ln = item.getItemProperty(ExampleUtil.PERSON_PROPERTY_LASTNAME).getValue()
                email = fn.toLowerCase() + '.' + ln.toLowerCase() + '@example.com'
                # the Link -component:
                emailLink = Link(email, ExternalResource('mailto:' + email))
                return emailLink

        _0_ = _0_()
        self._table.addGeneratedColumn('Email', _0_)
        # turn on column reordering and collapsing
        self._table.setColumnReorderingAllowed(True)
        self._table.setColumnCollapsingAllowed(True)
        # Actions (a.k.a context menu)

        class _1_(Action.Handler):

            def getActions(self, target, sender):
                return TableStylingExample_this.ACTIONS

            def handleAction(self, action, sender, target):
                TableStylingExample_this._markedRows.remove(target)
                if not (TableStylingExample_this.ACTION_NONE == action):
                    # we're using the cations caption as stylename as well:
                    TableStylingExample_this._markedRows.put(target, action.getCaption())
                # this causes the CellStyleGenerator to return new styles,
                # but table can't automatically know, we must tell it:
                TableStylingExample_this._table.requestRepaint()

        _1_ = _1_()
        self._table.addActionHandler(_1_)
        # style generator

        class _2_(CellStyleGenerator):

            def getStyle(self, itemId, propertyId):
                if propertyId is None:
                    # no propertyId, styling row
                    return TableStylingExample_this._markedRows[itemId]
                elif propertyId == 'Email':
                    # style the generated email column
                    return 'email'
                else:
                    cells = TableStylingExample_this._markedCells[itemId]
                    if cells is not None and propertyId in cells:
                        # marked cell
                        return 'marked'
                    else:
                        # no style
                        return None

        _2_ = _2_()
        self._table.setCellStyleGenerator(_2_)
        # toggle cell 'marked' styling when double-clicked

        class _3_(ItemClickListener):

            def itemClick(self, event):
                if event.getButton() == ItemClickEvent.BUTTON_RIGHT:
                    # you can handle left/right/middle -mouseclick
                    pass
                if event.isDoubleClick():
                    itemId = event.getItemId()
                    propertyId = event.getPropertyId()
                    cells = TableStylingExample_this._markedCells[itemId]
                    if cells is None:
                        cells = set()
                        TableStylingExample_this._markedCells.put(itemId, cells)
                    if propertyId in cells:
                        # toggle marking off
                        cells.remove(propertyId)
                    else:
                        # toggle marking on
                        cells.add(propertyId)
                    # this causes the CellStyleGenerator to return new styles,
                    # but table can't automatically know, we must tell it:
                    TableStylingExample_this._table.requestRepaint()

        _3_ = _3_()
        self._table.addListener(_3_)
        # Editing
        # we don't want to update container before pressing 'save':
        self._table.setWriteThrough(False)
        # edit button
        editButton = Button('Edit')
        self.addComponent(editButton)

        class _4_(Button.ClickListener):

            def buttonClick(self, event):
                TableStylingExample_this._table.setEditable(not TableStylingExample_this._table.isEditable())
                self.editButton.setCaption('Save' if TableStylingExample_this._table.isEditable() else 'Edit')

        _4_ = _4_()
        editButton.addListener(_4_)
        self.setComponentAlignment(editButton, Alignment.TOP_RIGHT)
