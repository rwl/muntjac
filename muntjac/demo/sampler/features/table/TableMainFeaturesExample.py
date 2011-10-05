
from muntjac.demo.sampler.ExampleUtil import ExampleUtil

from muntjac.ui import VerticalLayout, Table, Label
from muntjac.event.action import Action
from muntjac.event import action
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.ui.table import ICellStyleGenerator
from muntjac.data.property import IValueChangeListener


class TableMainFeaturesExample(VerticalLayout):

    ACTION_MARK = Action('Mark')
    ACTION_UNMARK = Action('Unmark')
    ACTION_LOG = Action('Save')
    ACTIONS_UNMARKED = [ACTION_MARK, ACTION_LOG]
    ACTIONS_MARKED = [ACTION_UNMARK, ACTION_LOG]

    def __init__(self):
        self._markedRows = set()

        self._table = Table('ISO-3166 Country Codes and flags')
        self.addComponent(self._table)

        # Label to indicate current selection
        selected = Label('No selection')
        self.addComponent(selected)


        # set a style name, so we can style rows and cells
        self._table.setStyleName('iso3166')

        # size
        self._table.setWidth('100%')
        self._table.setHeight('170px')

        # selectable
        self._table.setSelectable(True)
        self._table.setMultiSelect(True)
        self._table.setImmediate(True)  # react at once when something is selected

        # connect data source
        self._table.setContainerDataSource(ExampleUtil.getISO3166Container())

        # turn on column reordering and collapsing
        self._table.setColumnReorderingAllowed(True)
        self._table.setColumnCollapsingAllowed(True)

        # set column headers
        self._table.setColumnHeaders(['Country', 'Code', 'Icon file'])

        # Icons for column headers
        self._table.setColumnIcon(ExampleUtil.iso3166_PROPERTY_FLAG,
                ThemeResource('../sampler/icons/action_save.gif'))
        self._table.setColumnIcon(ExampleUtil.iso3166_PROPERTY_NAME,
                ThemeResource('../sampler/icons/icon_get_world.gif'))
        self._table.setColumnIcon(ExampleUtil.iso3166_PROPERTY_SHORT,
                ThemeResource('../sampler/icons/page_code.gif'))

        # Column alignment
        self._table.setColumnAlignment(ExampleUtil.iso3166_PROPERTY_SHORT,
                Table.ALIGN_CENTER)

        # Column width
        self._table.setColumnExpandRatio(ExampleUtil.iso3166_PROPERTY_NAME, 1)
        self._table.setColumnWidth(ExampleUtil.iso3166_PROPERTY_SHORT, 70)

        # Collapse one column - the user can make it visible again
        self._table.setColumnCollapsed(ExampleUtil.iso3166_PROPERTY_FLAG, True)

        # show row header w/ icon
        self._table.setRowHeaderMode(Table.ROW_HEADER_MODE_ICON_ONLY)
        self._table.setItemIconPropertyId(ExampleUtil.iso3166_PROPERTY_FLAG)

        # Actions (a.k.a context menu)
        class TableActionHandler(action.IHandler):

            def __init__(self, c):
                self._c = c

            def getActions(self, target, sender):
                if target in self._c._markedRows:
                    return self._c.ACTIONS_MARKED
                else:
                    return self._c.ACTIONS_UNMARKED

            def handleAction(self, action, sender, target):
                if self._c.ACTION_MARK == action:
                    self._c._markedRows.add(target)
                    self._c._table.requestRepaint()
                elif self._c.ACTION_UNMARK == action:
                    self._c._markedRows.remove(target)
                    self._c._table.requestRepaint()
                elif self._c.ACTION_LOG == action:
                    item = self._c._table.getItem(target)
                    self.addComponent(Label('Saved: ' + target + ', '
                            + item.getItemProperty(
                                ExampleUtil.iso3166_PROPERTY_NAME).getValue()))

        self._table.addActionHandler( TableActionHandler(self) )

        # style generator
        class TableStyleGenerator(ICellStyleGenerator):

            def __init__(self, c):
                self._c = c

            def getStyle(self, itemId, propertyId):
                if propertyId is None:
                    # no propertyId, styling row
                    return 'marked' if itemId in self._c._markedRows else None
                elif ExampleUtil.iso3166_PROPERTY_NAME == propertyId:
                    return 'bold'
                else:
                    # no style
                    return None

        self._table.setCellStyleGenerator( TableStyleGenerator(self) )

        # listen for valueChange, a.k.a 'select' and update the label
        class TableChangeListener(IValueChangeListener):

            def __init__(self, c):
                self._c = c

            def valueChange(self, event):
                value = event.getProperty().getValue()
                if (None is value) or (len(value) == 0):
                    # in multiselect mode, a Set of itemIds is returned,
                    self.selected.setValue('No selection')
                else:
                    # in singleselect mode the itemId is returned directly
                    self.selected.setValue('Selected: '
                            + self._c._table.getValue())

        self._table.addListener( TableChangeListener(self) )
