# -*- coding: utf-8 -*-
from __pyjamas__ import (ARGERROR,)
# from com.vaadin.ui.MenuBar import (MenuBar,)
# from com.vaadin.ui.MenuBar.Command import (Command,)
# from com.vaadin.ui.MenuBar.MenuItem import (MenuItem,)
# from junit.framework.TestCase import (TestCase,)


class MenuBarIds(TestCase, Command):
    _lastSelectedItem = None
    _menuFile = None
    _menuEdit = None
    _menuEditCopy = None
    _menuEditCut = None
    _menuEditPaste = None
    _menuEditFind = None
    _menuFileOpen = None
    _menuFileSave = None
    _menuFileExit = None
    _menuItems = set()
    _menuBar = None

    def setUp(self):
        self._menuBar = MenuBar()
        self._menuFile = self._menuBar.addItem('File', self)
        self._menuEdit = self._menuBar.addItem('Edit', self)
        self._menuEditCopy = self._menuEdit.addItem('Copy', self)
        self._menuEditCut = self._menuEdit.addItem('Cut', self)
        self._menuEditPaste = self._menuEdit.addItem('Paste', self)
        self._menuEdit.addSeparator()
        self._menuEditFind = self._menuEdit.addItem('Find...', self)
        self._menuFileOpen = self._menuFile.addItem('Open', self)
        self._menuFileSave = self._menuFile.addItem('Save', self)
        self._menuFile.addSeparator()
        self._menuFileExit = self._menuFile.addItem('Exit', self)
        self._menuItems.add(self._menuFile)
        self._menuItems.add(self._menuEdit)
        self._menuItems.add(self._menuEditCopy)
        self._menuItems.add(self._menuEditCut)
        self._menuItems.add(self._menuEditPaste)
        self._menuItems.add(self._menuEditFind)
        self._menuItems.add(self._menuFileOpen)
        self._menuItems.add(self._menuFileSave)
        self._menuItems.add(self._menuFileExit)

    def testMenubarIdUniqueness(self):
        # Ids within a menubar must be unique
        self.assertUniqueIds(self._menuBar)
        self._menuBar.removeItem(self._menuFile)
        file2 = self._menuBar.addItem('File2', self)
        file3 = self._menuBar.addItem('File3', self)
        file2sub = file2.addItem('File2 sub menu', self)
        self._menuItems.add(file2)
        self._menuItems.add(file2sub)
        self._menuItems.add(file3)
        self.assertUniqueIds(self._menuBar)

    @classmethod
    def assertUniqueIds(cls, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            menuBar, = _0
            ids = set()
            for item in menuBar.getItems():
                cls.assertUniqueIds(ids, item)
        elif _1 == 2:
            ids, item = _0
            id = item.getId()
            print 'Item ' + item.getText() + ', id: ' + id
            cls.assertFalse(ids.contains(id))
            ids.add(id)
            if item.getChildren() is not None:
                for subItem in item.getChildren():
                    cls.assertUniqueIds(ids, subItem)
        else:
            raise ARGERROR(1, 2)

    def menuSelected(self, selectedItem):
        self.assertNull('lastSelectedItem was not cleared before selecting an item', self._lastSelectedItem)
        self._lastSelectedItem = selectedItem
