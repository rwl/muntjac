# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.ExampleUtil import (ExampleUtil,)
# from com.vaadin.event.Action import (Action,)
# from com.vaadin.ui.Table.CellStyleGenerator import (CellStyleGenerator,)
# from java.util.HashSet import (HashSet,)
# from java.util.Set import (Set,)


class TableMainFeaturesExample(VerticalLayout):
    _table = Table('ISO-3166 Country Codes and flags')
    _markedRows = set()
    ACTION_MARK = Action('Mark')
    ACTION_UNMARK = Action('Unmark')
    ACTION_LOG = Action('Save')
    ACTIONS_UNMARKED = [ACTION_MARK, ACTION_LOG]
    ACTIONS_MARKED = [ACTION_UNMARK, ACTION_LOG]

    def __init__(self):
        self.addComponent(self._table)
        # Label to indicate current selection
        selected = ALabel('No selection')
        self.addComponent(selected)
        # set a style name, so we can style rows and cells
        self._table.setStyleName('iso3166')
        # size
        self._table.setWidth('100%')
        self._table.setHeight('170px')
        # selectable
        self._table.setSelectable(True)
        self._table.setMultiSelect(True)
        self._table.setImmediate(True)
        # react at once when something is selected
        # connect data source
        self._table.setContainerDataSource(ExampleUtil.getISO3166Container())
        # turn on column reordering and collapsing
        self._table.setColumnReorderingAllowed(True)
        self._table.setColumnCollapsingAllowed(True)
        # set column headers
        self._table.setColumnHeaders(['Country', 'Code', 'Icon file'])
        # Icons for column headers
        self._table.setColumnIcon(ExampleUtil.iso3166_PROPERTY_FLAG, ThemeResource('../sampler/icons/action_save.gif'))
        self._table.setColumnIcon(ExampleUtil.iso3166_PROPERTY_NAME, ThemeResource('../sampler/icons/icon_get_world.gif'))
        self._table.setColumnIcon(ExampleUtil.iso3166_PROPERTY_SHORT, ThemeResource('../sampler/icons/page_code.gif'))
        # Column alignment
        self._table.setColumnAlignment(ExampleUtil.iso3166_PROPERTY_SHORT, Table.ALIGN_CENTER)
        # Column width
        self._table.setColumnExpandRatio(ExampleUtil.iso3166_PROPERTY_NAME, 1)
        self._table.setColumnWidth(ExampleUtil.iso3166_PROPERTY_SHORT, 70)
        # Collapse one column - the user can make it visible again
        self._table.setColumnCollapsed(ExampleUtil.iso3166_PROPERTY_FLAG, True)
        # show row header w/ icon
        self._table.setRowHeaderMode(Table.ROW_HEADER_MODE_ICON_ONLY)
        self._table.setItemIconPropertyId(ExampleUtil.iso3166_PROPERTY_FLAG)
        # Actions (a.k.a context menu)

        class _0_(Action.Handler):

            def getActions(self, target, sender):
                if target in TableMainFeaturesExample_this._markedRows:
                    return TableMainFeaturesExample_this.ACTIONS_MARKED
                else:
                    return TableMainFeaturesExample_this.ACTIONS_UNMARKED

            def handleAction(self, action, sender, target):
                if TableMainFeaturesExample_this.ACTION_MARK == action:
                    TableMainFeaturesExample_this._markedRows.add(target)
                    TableMainFeaturesExample_this._table.requestRepaint()
                elif TableMainFeaturesExample_this.ACTION_UNMARK == action:
                    TableMainFeaturesExample_this._markedRows.remove(target)
                    TableMainFeaturesExample_this._table.requestRepaint()
                elif TableMainFeaturesExample_this.ACTION_LOG == action:
                    item = TableMainFeaturesExample_this._table.getItem(target)
                    self.addComponent(ALabel('Saved: ' + target + ', ' + item.getItemProperty(ExampleUtil.iso3166_PROPERTY_NAME).getValue()))

        _0_ = _0_()
        self._table.addActionHandler(_0_)
        # style generator

        class _1_(CellStyleGenerator):

            def getStyle(self, itemId, propertyId):
                if propertyId is None:
                    # no propertyId, styling row
                    return 'marked' if itemId in TableMainFeaturesExample_this._markedRows else None
                elif ExampleUtil.iso3166_PROPERTY_NAME == propertyId:
                    return 'bold'
                else:
                    # no style
                    return None

        _1_ = _1_()
        self._table.setCellStyleGenerator(_1_)
        # listen for valueChange, a.k.a 'select' and update the label

        class _2_(Table.ValueChangeListener):

            def valueChange(self, event):
                # in multiselect mode, a Set of itemIds is returned,
                # in singleselect mode the itemId is returned directly
                value = event.getProperty().getValue()
                if (None is value) or (len(value) == 0):
                    self.selected.setValue('No selection')
                else:
                    self.selected.setValue('Selected: ' + TableMainFeaturesExample_this._table.getValue())

        _2_ = _2_()
        self._table.addListener(_2_)
