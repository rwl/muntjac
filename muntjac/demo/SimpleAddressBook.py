
from random import random

from muntjac.data.util.indexed_container import IndexedContainer

from muntjac.ui.button import ClickEvent

from muntjac.data import property
from muntjac.ui import field

from muntjac.api import \
    (Application, Form, TextField, Table, HorizontalLayout,
     HorizontalSplitPanel, Window, VerticalLayout, Button)


class SimpleAddressBook(Application):

    _fields = ['First Name', 'Last Name', 'Company', 'Mobile Phone',
            'Work Phone', 'Home Phone', 'Work Email', 'Home Email',
            'Street', 'Zip', 'City', 'State', 'Country']

    _visibleCols = ['Last Name', 'First Name', 'Company']

    def __init__(self):
        super(SimpleAddressBook, self).__init__()

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
        newItem = Button('+')
        newItem.addCallback(onNew, ClickEvent, self)
        self._bottomLeftCorner.addComponent(newItem)

        # Remove item button
        self._contactRemovalButton = Button('-')
        self._contactRemovalButton.addCallback(onRemove, ClickEvent, self)
        self._contactRemovalButton.setVisible(False)
        self._bottomLeftCorner.addComponent(self._contactRemovalButton)


    def initAddressList(self):
        self._contactList.setContainerDataSource(self._addressBookData)
        self._contactList.setVisibleColumns(self._visibleCols)
        self._contactList.setSelectable(True)
        self._contactList.setImmediate(True)
        self._contactList.addCallback(onContactChange, field.ValueChangeEvent,
                self)
        return self._visibleCols


    def initFilteringControls(self):
        for pn in self._visibleCols:
            sf = TextField()
            self._bottomLeftCorner.addComponent(sf)
            sf.setWidth("100%")
            sf.setValue(pn)
            sf.setImmediate(True)
            self._bottomLeftCorner.setExpandRatio(sf, 1)
            sf.addCallback(onFilterChange, property.ValueChangeEvent,
                    pn, sf, self)


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
            fname = fnames[int( len(fnames) * random() )]
            ic.getContainerProperty(idd, 'First Name').setValue(fname)
            lname = lnames[int( len(lnames) * random() )]
            ic.getContainerProperty(idd, 'Last Name').setValue(lname)

        return ic


def onNew(event, book):
    idd = book._contactList.addItem()
    book._contactList.setValue(idd)


def onRemove(event, book):
    book._contactList.removeItem( book._contactList.getValue() )
    book._contactList.select(None)


def onContactChange(event, book):
    idd = book._contactList.getValue()

    if idd is None:
        book._contactEditor.setItemDataSource(None)
    else:
        item = book._contactList.getItem(idd)
        book._contactEditor.setItemDataSource(item)

    book._contactRemovalButton.setVisible(idd is not None)


def onFilterChange(event, name, text, book):
    book._addressBookData.removeContainerFilters(name)
    if len(str(text)) > 0 and name != str(text):
        book._addressBookData.addContainerFilter(name, str(text), True, False)

    book.getMainWindow().showNotification("%d matches found" %
            book._addressBookData.size())


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(SimpleAddressBook, nogui=True, forever=True, debug=True)
