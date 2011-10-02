# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
# from com.vaadin.data.Container import (Container,)
# from com.vaadin.data.Container.Indexed import (Indexed,)
# from com.vaadin.data.util.BeanItem import (BeanItem,)
# from com.vaadin.ui.AbstractField import (AbstractField,)
# from com.vaadin.ui.Button.ClickListener import (ClickListener,)
# from com.vaadin.ui.Component import (Component,)
# from com.vaadin.ui.DefaultFieldFactory import (DefaultFieldFactory,)
# from com.vaadin.ui.Field import (Field,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Collection import (Collection,)
# from java.util.GregorianCalendar import (GregorianCalendar,)


class GeneratedColumnExample(CustomComponent):
    """This example demonstrates the use of generated columns in a table. Generated
    columns can be used for formatting values or calculating them from other
    columns (or properties of the items).

    For the data model, we use POJOs bound to a custom Container with BeanItem
    items.

    @author magi
    """

    class FillUp(object):
        """The business model: fill-up at a gas station."""
        _date = None
        _quantity = None
        _total = None

        def __init__(self, *args):
            _0 = args
            _1 = len(args)
            if _1 == 0:
                pass # astStmt: [Stmt([]), None]
            elif _1 == 5:
                day, month, year, quantity, total = _0
                self._date = GregorianCalendar(year, month - 1, day).getTime()
                self._quantity = quantity
                self._total = total
            else:
                raise ARGERROR(0, 5)

        def price(self):
            """Calculates price per unit of quantity (€/l)."""
            if self._quantity != 0.0:
                return self._total / self._quantity
            else:
                return 0.0

        def dailyConsumption(self, other):
            """Calculates average daily consumption between two fill-ups."""
            difference_ms = self._date.getTime() - other.date.getTime()
            days = difference_ms / 1000 / 3600 / 24
            if days < 0.5:
                days = 1.0
                # Avoid division by zero if two fill-ups on the
                # same day.
            return self._quantity / days

        def dailyCost(self, other):
            """Calculates average daily consumption between two fill-ups."""
            # Getters and setters
            return self.price() * self.dailyConsumption(other)

        def getDate(self):
            return self._date

        def setDate(self, date):
            self._date = date

        def getQuantity(self):
            return self._quantity

        def setQuantity(self, quantity):
            self._quantity = quantity

        def getTotal(self):
            return self._total

        def setTotal(self, total):
            self._total = total

    class MySimpleIndexedContainer(Container, Indexed):
        """This is a custom container that allows adding BeanItems inside it. The
        BeanItem objects must be bound to an object. The item ID is an Integer
        from 0 to 99.

        Most of the interface methods are implemented with just dummy
        implementations, as they are not needed in this example.
        """
        _items = None
        _itemtemplate = None

        def __init__(self, itemtemplate):
            self._itemtemplate = itemtemplate
            self._items = list()
            # Yeah this is just a test

        def addContainerProperty(self, propertyId, type, defaultValue):
            raise self.UnsupportedOperationException()

        def addItem(self, *args):
            """None
            ---
            This addItem method is specific for this container and allows adding
            BeanItem objects. The BeanItems must be bound to MyBean objects.
            """
            _0 = args
            _1 = len(args)
            if _1 == 0:
                raise self.UnsupportedOperationException()
            elif _1 == 1:
                if isinstance(_0[0], BeanItem):
                    item, = _0
                    self._items.add(item)
                else:
                    itemId, = _0
                    raise self.UnsupportedOperationException()
            else:
                raise ARGERROR(0, 1)

        def containsId(self, itemId):
            if isinstance(itemId, int):
                pos = itemId.intValue()
                if pos >= 0 and pos < len(self._items):
                    return self._items[pos] is not None
            return False

        def getContainerProperty(self, itemId, propertyId):
            """The Table will call this method to get the property objects for the
            columns. It uses the property objects to determine the data types of
            the columns.
            """
            if isinstance(itemId, int):
                pos = itemId.intValue()
                if pos >= 0 and pos < len(self._items):
                    item = self._items[pos]
                    # The BeanItem provides the property objects for the items.
                    return item.getItemProperty(propertyId)
            return None

        def getContainerPropertyIds(self):
            """Table calls this to get the column names."""
            item = BeanItem(self._itemtemplate)
            # The BeanItem knows how to get the property names from the bean.
            return item.getItemPropertyIds()

        def getItem(self, itemId):
            if isinstance(itemId, int):
                pos = itemId.intValue()
                if pos >= 0 and pos < len(self._items):
                    return self._items[pos]
            return None

        def getItemIds(self):
            ids = list(len(self._items))
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(self._items)):
                    break
                ids.add(Integer.valueOf.valueOf(i))
            return ids

        def getType(self, propertyId):
            return BeanItem

        def removeAllItems(self):
            raise self.UnsupportedOperationException()

        def removeContainerProperty(self, propertyId):
            raise self.UnsupportedOperationException()

        def removeItem(self, itemId):
            raise self.UnsupportedOperationException()

        def size(self):
            return len(self._items)

        def addItemAt(self, *args):
            # TODO Auto-generated method stub
            _0 = args
            _1 = len(args)
            if _1 == 1:
                index, = _0
                return None
            elif _1 == 2:
                index, newItemId = _0
                return None
            else:
                raise ARGERROR(1, 2)

        # TODO Auto-generated method stub

        def getIdByIndex(self, index):
            return Integer.valueOf.valueOf(index)

        def indexOfId(self, itemId):
            return itemId.intValue()

        def addItemAfter(self, *args):
            # TODO Auto-generated method stub
            _0 = args
            _1 = len(args)
            if _1 == 1:
                previousItemId, = _0
                return None
            elif _1 == 2:
                previousItemId, newItemId = _0
                return None
            else:
                raise ARGERROR(1, 2)

        # TODO Auto-generated method stub

        def firstItemId(self):
            return Integer.valueOf.valueOf(0)

        def isFirstId(self, itemId):
            return itemId.intValue() == 0

        def isLastId(self, itemId):
            return itemId.intValue() == len(self._items) - 1

        def lastItemId(self):
            return Integer.valueOf.valueOf(len(self._items) - 1)

        def nextItemId(self, itemId):
            pos = self.indexOfId(itemId)
            if pos >= len(self._items) - 1:
                return None
            return self.getIdByIndex(pos + 1)

        def prevItemId(self, itemId):
            pos = self.indexOfId(itemId)
            if pos <= 0:
                return None
            return self.getIdByIndex(pos - 1)

    class DateColumnGenerator(Table.ColumnGenerator):
        """Formats the dates in a column containing Date objects."""

        def generateCell(self, source, itemId, columnId):
            """Generates the cell containing the Date value. The column is
            irrelevant in this use case.
            """
            prop = source.getItem(itemId).getItemProperty(columnId)
            if prop.getType() == Date:
                label = Label(String.format.format('%tF', [prop.getValue()]))
                label.addStyleName('column-type-date')
                return label
            return None

    class ValueColumnGenerator(Table.ColumnGenerator):
        """Formats the value in a column containing Double objects."""
        _format = None
        # Format string for the Double values.

        def __init__(self, format):
            """Creates double value column formatter with the given format string."""
            self._format = format

        def generateCell(self, source, itemId, columnId):
            """Generates the cell containing the Double value. The column is
            irrelevant in this use case.
            """
            prop = source.getItem(itemId).getItemProperty(columnId)
            if prop.getType() == float:
                label = Label(String.format.format(self._format, [prop.getValue()]))
                # Set styles for the column: one indicating that it's a value
                # and a more
                # specific one with the column name in it. This assumes that
                # the column
                # name is proper for CSS.
                label.addStyleName('column-type-value')
                label.addStyleName('column-' + columnId)
                return label
            return None

    class PriceColumnGenerator(Table.ColumnGenerator):
        """Table column generator for calculating price column."""

        def generateCell(self, source, itemId, columnId):
            # Retrieve the item.
            item = source.getItem(itemId)
            # Retrieves the underlying POJO from the item.
            fillup = item.getBean()
            # Do the business logic
            price = fillup.price()
            # Create the generated component for displaying the calcucated
            # value.
            label = Label(String.format.format('%1.2f €', [float(price)]))
            # We set the style here. You can't use a CellStyleGenerator for
            # generated columns.
            label.addStyleName('column-price')
            return label

    class ConsumptionColumnGenerator(Table.ColumnGenerator):
        """Table column generator for calculating consumption column."""

        def generateCell(self, *args):
            """Generates a cell containing value calculated from the item."""
            _0 = args
            _1 = len(args)
            if _1 == 2:
                fillup, prev = _0
                consumption = fillup.dailyConsumption(prev)
                # Generate the component for displaying the calculated value.
                label = Label(String.format.format('%3.2f l', [float(consumption)]))
                # We set the style here. You can't use a CellStyleGenerator for
                # generated columns.
                label.addStyleName('column-consumption')
                return label
            elif _1 == 3:
                source, itemId, columnId = _0
                indexedSource = source.getContainerDataSource()
                # Can not calculate consumption for the first item.
                if indexedSource.isFirstId(itemId):
                    label = Label('N/A')
                    label.addStyleName('column-consumption')
                    return label
                # Index of the previous item.
                prevItemId = indexedSource.prevItemId(itemId)
                # Retrieve the POJOs.
                fillup = indexedSource.getItem(itemId).getBean()
                prev = source.getItem(prevItemId).getBean()
                # Do the business logic
                return self.generateCell(fillup, prev)
            else:
                raise ARGERROR(2, 3)

    class DailyCostColumnGenerator(ConsumptionColumnGenerator):
        """Table column generator for calculating daily cost column."""

        def generateCell(self, fillup, prev):
            dailycost = fillup.dailyCost(prev)
            # Generate the component for displaying the calculated value.
            label = Label(String.format.format('%3.2f €', [float(dailycost)]))
            # We set the style here. You can't use a CellStyleGenerator for
            # generated columns.
            label.addStyleName('column-dailycost')
            return label

    class ImmediateFieldFactory(DefaultFieldFactory):
        """Custom field factory that sets the fields as immediate."""

        def createField(self, container, itemId, propertyId, uiContext):
            # Let the DefaultFieldFactory create the fields
            field = super(ImmediateFieldFactory, self).createField(container, itemId, propertyId, uiContext)
            # ...and just set them as immediate
            field.setImmediate(True)
            return field

    def __init__(self):
        table = Table()
        # Define table columns. These include also the column for the generated
        # column, because we want to set the column label to something
        # different than the property ID.
        table.addContainerProperty('date', Date, None, 'Date', None, None)
        table.addContainerProperty('quantity', float, None, 'Quantity (l)', None, None)
        table.addContainerProperty('price', float, None, 'Price (€/l)', None, None)
        table.addContainerProperty('total', float, None, 'Total (€)', None, None)
        table.addContainerProperty('consumption', float, None, 'Consumption (l/day)', None, None)
        table.addContainerProperty('dailycost', float, None, 'Daily Cost (€/day)', None, None)
        # Define the generated columns and their generators.
        table.addGeneratedColumn('date', self.DateColumnGenerator())
        table.addGeneratedColumn('quantity', self.ValueColumnGenerator('%.2f l'))
        table.addGeneratedColumn('price', self.PriceColumnGenerator())
        table.addGeneratedColumn('total', self.ValueColumnGenerator('%.2f €'))
        table.addGeneratedColumn('consumption', self.ConsumptionColumnGenerator())
        table.addGeneratedColumn('dailycost', self.DailyCostColumnGenerator())
        # Create a data source and bind it to the table.
        data = self.MySimpleIndexedContainer(self.FillUp())
        table.setContainerDataSource(data)
        # Generated columns are automatically placed after property columns, so
        # we have to set the order of the columns explicitly.
        table.setVisibleColumns(['date', 'quantity', 'price', 'total', 'consumption', 'dailycost'])
        # Add some data.
        data.addItem(BeanItem(self.FillUp(19, 2, 2005, 44.96, 51.21)))
        data.addItem(BeanItem(self.FillUp(30, 3, 2005, 44.91, 53.67)))
        data.addItem(BeanItem(self.FillUp(20, 4, 2005, 42.96, 49.06)))
        data.addItem(BeanItem(self.FillUp(23, 5, 2005, 47.37, 55.28)))
        data.addItem(BeanItem(self.FillUp(6, 6, 2005, 35.34, 41.52)))
        data.addItem(BeanItem(self.FillUp(30, 6, 2005, 16.07, 20.0)))
        data.addItem(BeanItem(self.FillUp(2, 7, 2005, 36.4, 36.19)))
        data.addItem(BeanItem(self.FillUp(6, 7, 2005, 39.17, 50.9)))
        data.addItem(BeanItem(self.FillUp(27, 7, 2005, 43.43, 53.03)))
        data.addItem(BeanItem(self.FillUp(17, 8, 2005, 20, 29.18)))
        data.addItem(BeanItem(self.FillUp(30, 8, 2005, 46.06, 59.09)))
        data.addItem(BeanItem(self.FillUp(22, 9, 2005, 46.11, 60.36)))
        data.addItem(BeanItem(self.FillUp(14, 10, 2005, 41.51, 50.19)))
        data.addItem(BeanItem(self.FillUp(12, 11, 2005, 35.24, 40.0)))
        data.addItem(BeanItem(self.FillUp(28, 11, 2005, 45.26, 53.27)))
        # Have a check box that allows the user to make the quantity
        # and total columns editable.
        editable = CheckBox('Edit the input values - calculated columns are regenerated')
        editable.setImmediate(True)

        class _0_(ClickListener):

            def buttonClick(self, event):
                self.table.setEditable(self.editable.booleanValue())
                # The columns may not be generated when we want to have them
                # editable.
                if self.editable.booleanValue():
                    self.table.removeGeneratedColumn('quantity')
                    self.table.removeGeneratedColumn('total')
                else:
                    # In non-editable mode we want to show the formatted
                    # values.
                    self.table.addGeneratedColumn('quantity', GeneratedColumnExample_this.ValueColumnGenerator('%.2f l'))
                    self.table.addGeneratedColumn('total', GeneratedColumnExample_this.ValueColumnGenerator('%.2f €'))
                # The visible columns are affected by removal and addition of
                # generated columns so we have to redefine them.
                self.table.setVisibleColumns(['date', 'quantity', 'price', 'total', 'consumption', 'dailycost'])

        _0_ = _0_()
        editable.addListener(_0_)
        # Use a custom field factory to set the edit fields as immediate.
        # This is used when the table is in editable mode.
        table.setTableFieldFactory(self.ImmediateFieldFactory())
        # Setting the table itself as immediate has no relevance in this
        # example,
        # because it is relevant only if the table is selectable and we want to
        # get the selection changes immediately.
        table.setImmediate(True)
        table.setHeight('300px')
        layout = VerticalLayout()
        layout.setMargin(True)
        layout.addComponent(Label('Table with column generators that format and calculate cell values.'))
        layout.addComponent(table)
        layout.addComponent(editable)
        layout.addComponent(Label('Columns displayed in blue are calculated from Quantity and Total. ' + 'Others are simply formatted.'))
        layout.setExpandRatio(table, 1)
        layout.setSizeUndefined()
        self.setCompositionRoot(layout)
        # setSizeFull();
