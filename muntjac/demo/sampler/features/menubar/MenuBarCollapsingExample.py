# -*- coding: utf-8 -*-


class MenuBarCollapsingExample(VerticalLayout):
    _menubar = MenuBar()

    def __init__(self):
        # In order to collapse items, the MenuBar must have a specified width
        self._menubar.setWidth('50%')
        # Save reference to individual items so we can add sub-menu items to
        # them
        file = self._menubar.addItem('File', None)
        newItem = file.addItem('New', None)
        file.addItem('Open file...', self.menuCommand)
        file.addSeparator()
        newItem.addItem('File', self.menuCommand)
        newItem.addItem('Folder', self.menuCommand)
        newItem.addItem('Project...', self.menuCommand)
        file.addItem('Close', self.menuCommand)
        file.addItem('Close All', self.menuCommand)
        file.addSeparator()
        file.addItem('Save', self.menuCommand)
        file.addItem('Save As...', self.menuCommand)
        file.addItem('Save All', self.menuCommand)
        # Generate bogus items so we can show the collapsing
        _0 = True
        i = 1
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 5):
                break
            self._menubar.addItem('Item ' + i, self.menuCommand).setEnabled(False)
        edit = self._menubar.addItem('Edit', None)
        edit.addItem('Undo', self.menuCommand)
        edit.addItem('Redo', self.menuCommand).setEnabled(False)
        edit.addSeparator()
        edit.addItem('Cut', self.menuCommand)
        edit.addItem('Copy', self.menuCommand)
        edit.addItem('Paste', self.menuCommand)
        edit.addSeparator()
        find = edit.addItem('Find/Replace', self.menuCommand)
        # Actions can be added inline as well, of course

        class _0_(Command):

            def menuSelected(self, selectedItem):
                self.getWindow().open(ExternalResource('http://www.google.com'))

        _0_ = _0_()
        find.addItem('Google Search', _0_)
        find.addSeparator()
        find.addItem('Find/Replace...', self.menuCommand)
        find.addItem('Find Next', self.menuCommand)
        find.addItem('Find Previous', self.menuCommand)
        view = self._menubar.addItem('View', None)
        view.addItem('Show/Hide Status Bar', self.menuCommand)
        view.addItem('Customize Toolbar...', self.menuCommand)
        view.addSeparator()
        view.addItem('Actual Size', self.menuCommand)
        view.addItem('Zoom In', self.menuCommand)
        view.addItem('Zoom Out', self.menuCommand)
        # Generate bogus items so we can show the collapsing
        _1 = True
        i = 1
        while True:
            if _1 is True:
                _1 = False
            else:
                i += 1
            if not (i < 5):
                break
            self._menubar.addItem('Item ' + i, self.menuCommand).setEnabled(False)
        self.addComponent(self._menubar)

    class menuCommand(Command):

        def menuSelected(self, selectedItem):
            self.getWindow().showNotification('Action ' + selectedItem.getText())
