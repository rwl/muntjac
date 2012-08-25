# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

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
