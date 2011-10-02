# -*- coding: utf-8 -*-
# from com.vaadin.data.Property import (Property,)
# from com.vaadin.data.Property.ValueChangeEvent import (ValueChangeEvent,)
# from com.vaadin.data.util.IndexedContainer import (IndexedContainer,)
# from com.vaadin.ui.Button.ClickEvent import (ClickEvent,)
# from com.vaadin.ui.Form import (Form,)
# from com.vaadin.ui.TextField import (TextField,)


class SimpleAddressBook(Application):
    _fields = ['First Name', 'Last Name', 'Company', 'Mobile Phone', 'Work Phone', 'Home Phone', 'Work Email', 'Home Email', 'Street', 'Zip', 'City', 'State', 'Country']
    _visibleCols = ['Last Name', 'First Name', 'Company']
    _contactList = Table()
    _contactEditor = Form()
    _bottomLeftCorner = HorizontalLayout()
    _contactRemovalButton = None
    _addressBookData = createDummyData()

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
        self._bottomLeftCorner.addComponent(


        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                id = SimpleAddressBook_this._contactList.addItem()
                SimpleAddressBook_this._contactList.setValue(id)


        _0_ = _0_()
        Button('+', _0_))
        # Remove item button

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                SimpleAddressBook_this._contactList.removeItem(SimpleAddressBook_this._contactList.getValue())
                SimpleAddressBook_this._contactList.select(None)

        _0_ = _0_()
        Button('-', _0_)
        self._contactRemovalButton = _0_
        self._contactRemovalButton.setVisible(False)
        self._bottomLeftCorner.addComponent(self._contactRemovalButton)

    def initAddressList(self):
        self._contactList.setContainerDataSource(self._addressBookData)
        self._contactList.setVisibleColumns(self._visibleCols)
        self._contactList.setSelectable(True)
        self._contactList.setImmediate(True)

        class _0_(Property.ValueChangeListener):

            def valueChange(self, event):
                id = SimpleAddressBook_this._contactList.getValue()
                SimpleAddressBook_this._contactEditor.setItemDataSource(None if id is None else SimpleAddressBook_this._contactList.getItem(id))
                SimpleAddressBook_this._contactRemovalButton.setVisible(id is not None)

        _0_ = _0_()
        self._contactList.addListener(_0_)
        return self._visibleCols

    def initFilteringControls(self):
        # for (final String pn : visibleCols) {
        # final TextField sf = new TextField();
        # bottomLeftCorner.addComponent(sf);
        # sf.setWidth("100%");
        # sf.setValue(pn);
        # sf.setImmediate(true);
        # bottomLeftCorner.setExpandRatio(sf, 1);
        # sf.addListener(new Property.ValueChangeListener() {
        # public void valueChange(ValueChangeEvent event) {
        # addressBookData.removeContainerFilters(pn);
        # if (sf.toString().length() > 0 && !pn.equals(sf.toString())) {
        # addressBookData.addContainerFilter(pn, sf.toString(),
        # true, false);
        # }
        # getMainWindow().showNotification(
        # "" + addressBookData.size() + " matches found");
        # }
        # });
        # }
        pass

    @classmethod
    def createDummyData(cls):
        fnames = ['Peter', 'Alice', 'Joshua', 'Mike', 'Olivia', 'Nina', 'Alex', 'Rita', 'Dan', 'Umberto', 'Henrik', 'Rene', 'Lisa', 'Marge']
        lnames = ['Smith', 'Gordon', 'Simpson', 'Brown', 'Clavel', 'Simons', 'Verne', 'Scott', 'Allison', 'Gates', 'Rowling', 'Barks', 'Ross', 'Schneider', 'Tate']
        ic = IndexedContainer()
        for p in cls._fields:
            ic.addContainerProperty(p, str, '')
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 1000):
                break
            id = ic.addItem()
            ic.getContainerProperty(id, 'First Name').setValue(fnames[len(fnames) * cls.Math.random()])
            ic.getContainerProperty(id, 'Last Name').setValue(lnames[len(lnames) * cls.Math.random()])
        return ic
