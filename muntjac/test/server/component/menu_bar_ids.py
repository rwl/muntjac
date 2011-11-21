# Copyright (C) 2011 Vaadin Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

from unittest import TestCase
from muntjac.ui.menu_bar import ICommand, MenuBar


class MenuBarIds(TestCase, ICommand):

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

        self._menuItems = set()
        self._menuItems.add(self._menuFile)
        self._menuItems.add(self._menuEdit)
        self._menuItems.add(self._menuEditCopy)
        self._menuItems.add(self._menuEditCut)
        self._menuItems.add(self._menuEditPaste)
        self._menuItems.add(self._menuEditFind)
        self._menuItems.add(self._menuFileOpen)
        self._menuItems.add(self._menuFileSave)
        self._menuItems.add(self._menuFileExit)

        self._lastSelectedItem = None


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
        nargs = len(args)
        if nargs == 1:
            menuBar, = args
            ids = set()
            for item in menuBar.getItems():
                cls.assertUniqueIds(ids, item)
        elif nargs == 2:
            ids, item = args
            idd = item.getId()
            print 'Item ' + item.getText() + ', id: ' + str(idd)
            assert idd not in ids
            ids.add(idd)
            if item.getChildren() is not None:
                for subItem in item.getChildren():
                    cls.assertUniqueIds(ids, subItem)
        else:
            raise ValueError


    def menuSelected(self, selectedItem):
        self.assertEquals(('lastSelectedItem was not cleared before '
                'selecting an item'), self._lastSelectedItem)
        self._lastSelectedItem = selectedItem
