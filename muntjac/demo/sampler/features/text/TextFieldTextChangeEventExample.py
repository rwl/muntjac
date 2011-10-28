
from muntjac.demo.sampler.ExampleUtil import ExampleUtil
from muntjac.api import VerticalLayout, TextField, Table
from muntjac.ui.abstract_text_field import TextChangeEventMode
from muntjac.event.field_events import ITextChangeListener


class TextFieldTextChangeEventExample(VerticalLayout):

    def __init__(self):
        super(TextFieldTextChangeEventExample, self).__init__()

        nameContainer = ExampleUtil.getNameContainer()
        filterField = TextField('Filter')
        filterField.setTextChangeEventMode(TextChangeEventMode.LAZY)
        filterField.setTextChangeTimeout(200)

        filterField.addListener(FilterListener(nameContainer),
                ITextChangeListener)
        table = Table(None, nameContainer)
        table.setColumnHeaderMode(Table.COLUMN_HEADER_MODE_HIDDEN)

        self.setSpacing(False)

        self.addComponent(filterField)
        self.addComponent(table)

        filterField.setWidth('150px')
        table.setWidth('150px')


class FilterListener(ITextChangeListener):

    def __init__(self, nameContainer):
        self._nameContainer = nameContainer

    def textChange(self, event):
        self._nameContainer.removeAllContainerFilters()
        self._nameContainer.addContainerFilter(
                ExampleUtil.PERSON_PROPERTY_NAME,
                event.getText(), True, False)
