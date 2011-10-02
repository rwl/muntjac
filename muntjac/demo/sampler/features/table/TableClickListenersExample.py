# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.ExampleUtil import (ExampleUtil,)
# from com.vaadin.ui.Table.FooterClickEvent import (FooterClickEvent,)
# from com.vaadin.ui.Table.HeaderClickEvent import (HeaderClickEvent,)


class TableClickListenersExample(VerticalLayout):

    def __init__(self):
        super(TableClickListenersExample, self)()
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
        # Create table
        table = Table('', ExampleUtil.getOrderContainer())
        table.setColumnExpandRatio(ExampleUtil.ORDER_DESCRIPTION_PROPERTY_ID, 1)
        table.setSortDisabled(True)
        table.setWidth('100%')
        table.setPageLength(6)
        table.setFooterVisible(True)
        table.setImmediate(True)
        # Add some total sum and description to footer
        table.setColumnFooter(ExampleUtil.ORDER_DESCRIPTION_PROPERTY_ID, 'Total Price')
        table.setColumnFooter(ExampleUtil.ORDER_ITEMPRICE_PROPERTY_ID, NumberFormat.getCurrencyInstance().format(totalSum))
        # Add a header click handler

        class _0_(Table.HeaderClickListener):

            def headerClick(self, event):
                # Show a notification help text when the user clicks on a
                # column header

                TableClickListenersExample_this.showHeaderHelpText(event.getPropertyId())

        _0_ = _0_()
        table.addListener(_0_)
        # Add a footer click handler

        class _1_(Table.FooterClickListener):

            def footerClick(self, event):
                # Show a notification help text when the user clicks on a
                # column footer

                TableClickListenersExample_this.showFooterHelpText(event.getPropertyId())

        _1_ = _1_()
        table.addListener(_1_)
        self.addComponent(table)

    def showHeaderHelpText(self, column):
        """Shows some help text when clicking on the header

        @param column
        """
        notification = None
        # Description
        if column == ExampleUtil.ORDER_DESCRIPTION_PROPERTY_ID:
            notification = Notification(String.valueOf.valueOf(column) + '<br>', 'The description describes the type of product that has been ordered.')
            # Item price
        elif column == ExampleUtil.ORDER_ITEMPRICE_PROPERTY_ID:
            notification = Notification(String.valueOf.valueOf(column) + '<br>', 'The item price is calculated by multiplying the unit price with the quantity.')
            # Quantity
        elif column == ExampleUtil.ORDER_QUANTITY_PROPERTY_ID:
            notification = Notification(String.valueOf.valueOf(column) + '<br>', 'The quantity describes how many items has been ordered.')
            # Unit price
        elif column == ExampleUtil.ORDER_UNITPRICE_PROPERTY_ID:
            notification = Notification(String.valueOf.valueOf(column) + '<br>', 'The unit price is how much a single items costs. Taxes included.')
        else:
            return
        self.getWindow().showNotification(notification)

    def showFooterHelpText(self, column):
        """Shows a footer help text

        @param column
        """
        notification = Notification('Total Price<br>', 'The total price is calculated by summing every items item price together.')
        self.getWindow().showNotification(notification)
