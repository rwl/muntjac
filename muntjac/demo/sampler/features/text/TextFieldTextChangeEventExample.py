# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.ExampleUtil import (ExampleUtil,)
# from com.vaadin.event.FieldEvents.TextChangeEvent import (TextChangeEvent,)
# from com.vaadin.event.FieldEvents.TextChangeListener import (TextChangeListener,)
# from com.vaadin.ui.AbstractTextField.TextChangeEventMode import (TextChangeEventMode,)


class TextFieldTextChangeEventExample(VerticalLayout):

    def __init__(self):
        nameContainer = ExampleUtil.getNameContainer()
        filterField = TextField('Filter')
        filterField.setTextChangeEventMode(TextChangeEventMode.LAZY)
        filterField.setTextChangeTimeout(200)

        class _0_(TextChangeListener):

            def textChange(self, event):
                self.nameContainer.removeAllContainerFilters()
                self.nameContainer.addContainerFilter(ExampleUtil.PERSON_PROPERTY_NAME, event.getText(), True, False)

        _0_ = _0_()
        filterField.addListener(_0_)
        table = Table(None, nameContainer)
        table.setColumnHeaderMode(Table.COLUMN_HEADER_MODE_HIDDEN)
        self.setSpacing(False)
        self.addComponent(filterField)
        self.addComponent(table)
        filterField.setWidth('150px')
        table.setWidth('150px')
