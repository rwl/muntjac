# -*- coding: utf-8 -*-
from muntjac.demo.sampler.ExampleUtil import (ExampleUtil,)
# from com.vaadin.data.util.IndexedContainer import (IndexedContainer,)
# from com.vaadin.ui.Table import (Table,)
# from java.text.NumberFormat import (NumberFormat,)
# from java.text.ParseException import (ParseException,)


class TableFooterExample(VerticalLayout):

    def __init__(self):
        # Create our data source
        dataSource = ExampleUtil.getOrderContainer()
        # Calculate total sum
        totalSum = 0.0
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(dataSource)):
                break
            item = dataSource.getItem(dataSource.getIdByIndex(i))
            value = item.getItemProperty(ExampleUtil.ORDER_ITEMPRICE_PROPERTY_ID).getValue()
            try:
                amount = NumberFormat.getCurrencyInstance().parse(str(value))
                totalSum += amount.doubleValue()
            except ParseException, e:
                e.printStackTrace()
        # Create a table to show the data in
        table = Table('Order table', dataSource)
        table.setPageLength(6)
        table.setWidth('100%')
        # Set alignments
        table.setColumnAlignments([Table.ALIGN_LEFT, Table.ALIGN_RIGHT, Table.ALIGN_RIGHT, Table.ALIGN_RIGHT])
        # Set column widths
        table.setColumnExpandRatio(ExampleUtil.ORDER_DESCRIPTION_PROPERTY_ID, 1)
        # Enable footer
        table.setFooterVisible(True)
        # Add some total sum and description to footer
        table.setColumnFooter(ExampleUtil.ORDER_DESCRIPTION_PROPERTY_ID, 'Total Price')
        table.setColumnFooter(ExampleUtil.ORDER_ITEMPRICE_PROPERTY_ID, NumberFormat.getCurrencyInstance().format(totalSum))
        self.addComponent(table)
