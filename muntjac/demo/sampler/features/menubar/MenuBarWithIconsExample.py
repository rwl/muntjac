# -*- coding: utf-8 -*-
# from com.vaadin.terminal.ThemeResource import (ThemeResource,)


class MenuBarWithIconsExample(VerticalLayout):
    _menubar = MenuBar()

    def __init__(self):
        # Save reference to individual items so we can add sub-menu items to
        # them
        file = self._menubar.addItem('File', None)
        newItem = file.addItem('New', None)
        file.addItem('Open file...', ThemeResource('../runo/icons/16/folder.png'), self.menuCommand)
        file.addSeparator()
        newItem.addItem('File', ThemeResource('../runo/icons/16/document.png'), self.menuCommand)
        newItem.addItem('Folder', ThemeResource('../runo/icons/16/folder.png'), self.menuCommand)
        newItem.addItem('Project...', ThemeResource('../runo/icons/16/globe.png'), self.menuCommand)
        file.addItem('Close', self.menuCommand)
        file.addItem('Close All', self.menuCommand)
        file.addSeparator()
        file.addItem('Save', self.menuCommand)
        file.addItem('Save As...', self.menuCommand)
        file.addItem('Save All', self.menuCommand)
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
        view = self._menubar.addItem('View', ThemeResource('../runo/icons/16/user.png'), None)
        view.addItem('Show/Hide Status Bar', self.menuCommand)
        view.addItem('Customize Toolbar...', self.menuCommand)
        view.addSeparator()
        view.addItem('Actual Size', self.menuCommand)
        view.addItem('Zoom In', self.menuCommand)
        view.addItem('Zoom Out', self.menuCommand)
        self.addComponent(self._menubar)

    class menuCommand(Command):

        def menuSelected(self, selectedItem):
            self.getWindow().showNotification('Action ' + selectedItem.getText())
