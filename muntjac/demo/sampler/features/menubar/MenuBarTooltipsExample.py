# -*- coding: utf-8 -*-


class MenuBarTooltipsExample(VerticalLayout):
    _menubar = MenuBar()

    def __init__(self):
        # Add tooltip to the menubar itself
        self._menubar.setDescription('Perform some actions by selecting them from the menus')
        # Save reference to individual items so we can add sub-menu items to
        # them
        file = self._menubar.addItem('File', None)
        file.setDescription('File menu')
        newItem = file.addItem('New', None)
        newItem.setDescription('Add a new..')
        open = file.addItem('Open file...', self.menuCommand)
        open.setDescription('Retrieve a file from the filesystem')
        file.addSeparator()
        item = newItem.addItem('File', self.menuCommand)
        item.setDescription('Open a file')
        item = newItem.addItem('Folder', self.menuCommand)
        item.setDescription('Open a folder')
        item = newItem.addItem('Project...', self.menuCommand)
        item.setDescription('Open a project')
        item = file.addItem('Close', self.menuCommand)
        item.setDescription('Closes the selected file')
        item = file.addItem('Close All', self.menuCommand)
        item.setDescription('Closes all files')
        file.addSeparator()
        item = file.addItem('Save', self.menuCommand)
        item.setDescription('Saves the file')
        item = file.addItem('Save As...', self.menuCommand)
        item.setDescription('Saves the file with a different name')
        item = file.addItem('Save All', self.menuCommand)
        item.setDescription('Saves all files')
        edit = self._menubar.addItem('Edit', None)
        edit.setDescription('Edit menu')
        item = edit.addItem('Undo', self.menuCommand)
        item.setDescription('Reverses recent changes')
        item = edit.addItem('Redo', self.menuCommand)
        item.setEnabled(False)
        item.setDescription('Redoes undone changed')
        edit.addSeparator()
        item = edit.addItem('Cut', self.menuCommand)
        item.setDescription('Copies the text to the clipboard and removes it')
        item = edit.addItem('Copy', self.menuCommand)
        item.setDescription('Copies the text to the clipboard')
        item = edit.addItem('Paste', self.menuCommand)
        item.setDescription('Copies the contents of the clipboard on to the document')
        edit.addSeparator()
        find = edit.addItem('Find/Replace', self.menuCommand)
        find.setDescription('Find or Replace text')
        # Actions can be added inline as well, of course

        class _0_(Command):

            def menuSelected(self, selectedItem):
                self.getWindow().open(ExternalResource('http://www.google.com'))

        _0_ = _0_()
        find.addItem('Google Search', _0_)
        item = _0_
        item.setDescription('Search with Google')
        find.addSeparator()
        item = find.addItem('Find/Replace...', self.menuCommand)
        item.setDescription('Finds or replaces text')
        item = find.addItem('Find Next', self.menuCommand)
        item.setDescription('Find the next occurrence')
        item = find.addItem('Find Previous', self.menuCommand)
        item.setDescription('Find the previous occurrence')
        view = self._menubar.addItem('View', None)
        view.setDescription('View menu')
        item = view.addItem('Show/Hide Status Bar', self.menuCommand)
        item.setDescription('Toggles the visibility of the Status Bar')
        item = view.addItem('Customize Toolbar...', self.menuCommand)
        item.setDescription('Add or remove items in the toolbar')
        view.addSeparator()
        item = view.addItem('Actual Size', self.menuCommand)
        item.setDescription('Resize view to the original size')
        item = view.addItem('Zoom In', self.menuCommand)
        item.setDescription('Zoom the document in by 10%')
        item = view.addItem('Zoom Out', self.menuCommand)
        item.setDescription('Zoom the doucment out by 10%')
        self.addComponent(self._menubar)

    class menuCommand(Command):

        def menuSelected(self, selectedItem):
            self.getWindow().showNotification('Action ' + selectedItem.getText())
