
from random import random

from muntjac import Application

from muntjac.data.property import IValueChangeListener
from muntjac.data.util.indexed_container import IndexedContainer

from muntjac.ui import button

from muntjac.ui import \
    (Form, TextField, Table, HorizontalLayout, HorizontalSplitPanel,
     Window, VerticalLayout, Button)


class SimpleAddressBook(Application):

    _fields = ['First Name', 'Last Name', 'Company', 'Mobile Phone',
            'Work Phone', 'Home Phone', 'Work Email', 'Home Email',
            'Street', 'Zip', 'City', 'State', 'Country']

    _visibleCols = ['Last Name', 'First Name', 'Company']

    def __init__(self):
        self._contactList = Table()
        self._contactEditor = Form()
        self._bottomLeftCorner = HorizontalLayout()
        self._contactRemovalButton = None
        self._addressBookData = self.createDummyData()


    def init(self):
        self.initLayout()
        self.initContactAddRemoveButtons()
        self.initAddressList()
        self.initFilteringControls()


    def initLayout(self):
        splitPanel = HorizontalSplitPanel()
        self.setMainWindow(Window('Address Book', splitPanel))
        left = VerticalLayout()
        left.setSizeFull()
        left.addComponent(self._contactList)
        self._contactList.setSizeFull()
        left.setExpandRatio(self._contactList, 1)
        splitPanel.addComponent(left)
        splitPanel.addComponent(self._contactEditor)
        self._contactEditor.setSizeFull()
        self._contactEditor.getLayout().setMargin(True)
        self._contactEditor.setImmediate(True)
        self._bottomLeftCorner.setWidth('100%')
        left.addComponent(self._bottomLeftCorner)


    def initContactAddRemoveButtons(self):
        # New item button
        class NewItemListener(button.IClickListener):

            def __init__(self, book):
                self._book = book

            def buttonClick(self, event):
                idd = self._book._contactList.addItem()
                self._book._contactList.setValue(idd)


        newItem = Button('+', NewItemListener(self))
        self._bottomLeftCorner.addComponent(newItem)

        # Remove item button
        class RemoveItemListener(button.IClickListener):

            def __init__(self, book):
                self._book = book

            def buttonClick(self, event):
                self._book._contactList.removeItem(
                        self._book._contactList.getValue())
                self._book._contactList.select(None)

        self._contactRemovalButton = Button('-', RemoveItemListener(self))
        self._contactRemovalButton.setVisible(False)
        self._bottomLeftCorner.addComponent(self._contactRemovalButton)


    def initAddressList(self):
        self._contactList.setContainerDataSource(self._addressBookData)
        self._contactList.setVisibleColumns(self._visibleCols)
        self._contactList.setSelectable(True)
        self._contactList.setImmediate(True)

        class ChangeListener(IValueChangeListener):

            def __init__(self, book):
                self._book = book

            def valueChange(self, event):
                idd = self._book._contactList.getValue()

                if idd is None:
                    self._book._contactEditor.setItemDataSource(None)
                else:
                    item = self._book._contactList.getItem(idd)
                    self._book._contactEditor.setItemDataSource(item)

                self._book._contactRemovalButton.setVisible(id is not None)

        self._contactList.addListener( ChangeListener(self) )
        return self._visibleCols


    def initFilteringControls(self):
        for pn in self._visibleCols:
            sf = TextField()
            self._bottomLeftCorner.addComponent(sf)
            sf.setWidth("100%")
            sf.setValue(pn)
            sf.setImmediate(True)
            self._bottomLeftCorner.setExpandRatio(sf, 1)

            class ChangeListener(IValueChangeListener):

                def __init__(self, book):
                    self._book = book

                def valueChange(self, event):
                    self._book._addressBookData.removeContainerFilters(pn)
                    if len(str(sf)) > 0 and pn != str(sf):
                        self._book._addressBookData.addContainerFilter(pn,
                                str(sf), True, False)

                    self._book._getMainWindow().showNotification((""
                            + self._book._addressBookData.size()
                            + " matches found"))

            sf.addListener(ChangeListener(self))

    @classmethod
    def createDummyData(cls):
        fnames = ['Peter', 'Alice', 'Joshua', 'Mike', 'Olivia', 'Nina', 'Alex',
                'Rita', 'Dan', 'Umberto', 'Henrik', 'Rene', 'Lisa', 'Marge']
        lnames = ['Smith', 'Gordon', 'Simpson', 'Brown', 'Clavel', 'Simons',
                'Verne', 'Scott', 'Allison', 'Gates', 'Rowling', 'Barks',
                'Ross', 'Schneider', 'Tate']

        ic = IndexedContainer()

        for p in cls._fields:
            ic.addContainerProperty(p, str, '')

        for _ in range(1000):
            idd = ic.addItem()
            fname = fnames[len(fnames) * random()]
            ic.getContainerProperty(idd, 'First Name').setValue(fname)
            lname = lnames[len(lnames) * random()]
            ic.getContainerProperty(idd, 'Last Name').setValue(lname)

        return ic
