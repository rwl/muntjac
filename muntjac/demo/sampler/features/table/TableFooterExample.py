
import re

from babel.numbers import format_currency
from muntjac.util import defaultLocale

from muntjac.demo.sampler.ExampleUtil import ExampleUtil
from muntjac.api import VerticalLayout, Table


class TableFooterExample(VerticalLayout):

    CURRENCY_PATTERN = u'([\u00A3\u0024\u20AC])(\d+(?:\.\d{2})?)'

    def __init__(self):
        super(TableFooterExample, self).__init__()

        # Create our data source
        dataSource = ExampleUtil.getOrderContainer()

        # Calculate total sum
        totalSum = 0.0
        for i in range(len(dataSource)):
            item = dataSource.getItem(dataSource.getIdByIndex(i))
            value = item.getItemProperty(
                    ExampleUtil.ORDER_ITEMPRICE_PROPERTY_ID).getValue()

            match = re.search(self.CURRENCY_PATTERN, str(value))
            if match is not None:
                amount = match.groups()[1]
                totalSum += float(amount)

        # Create a table to show the data in
        table = Table('Order table', dataSource)
        table.setPageLength(6)
        table.setWidth('100%')

        # Set alignments
        table.setColumnAlignments([Table.ALIGN_LEFT, Table.ALIGN_RIGHT,
                Table.ALIGN_RIGHT, Table.ALIGN_RIGHT])

        # Set column widths
        table.setColumnExpandRatio(ExampleUtil.ORDER_DESCRIPTION_PROPERTY_ID, 1)

        # Enable footer
        table.setFooterVisible(True)

        # Add some total sum and description to footer
        table.setColumnFooter(ExampleUtil.ORDER_DESCRIPTION_PROPERTY_ID,
                'Total Price')
        l = defaultLocale()
        fc = format_currency(totalSum, currency='USD', locale=l).encode('utf-8')
        table.setColumnFooter(ExampleUtil.ORDER_ITEMPRICE_PROPERTY_ID, fc)

        self.addComponent(table)
