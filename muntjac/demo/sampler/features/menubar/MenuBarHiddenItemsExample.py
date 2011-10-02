# -*- coding: utf-8 -*-
# from com.vaadin.ui.Button import (Button,)
# from com.vaadin.ui.Button.ClickEvent import (ClickEvent,)


class MenuBarHiddenItemsExample(VerticalLayout):
    _menubar = MenuBar()

    def __init__(self):
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
        edit = self._menubar.addItem('Edit', None)
        edit.addItem('Undo', self.menuCommand)
        redo = edit.addItem('Redo', self.menuCommand)
        redo.setEnabled(False)
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
        self.addComponent(self._menubar)
        self.addComponent(


        class _1_(Button.ClickListener):

            def buttonClick(self, event):
                self.file.setVisible(not self.file.isVisible())
                event.getButton().setCaption('Hide File menu' if self.file.isVisible() else 'Show File menu')


        _1_ = _1_()
        Button('Hide File menu', _1_))
        self.addComponent(


        class _1_(Button.ClickListener):

            def buttonClick(self, event):
                self.redo.setEnabled(not self.redo.isEnabled())
                event.getButton().setCaption('Disable Edit -> Redo action' if self.redo.isEnabled() else 'Enable Edit -> Redo action')


        _1_ = _1_()
        Button('Enable Edit -> Redo action', _1_))
        self.setSpacing(True)

    class menuCommand(Command):

        def menuSelected(self, selectedItem):
            self.getWindow().showNotification('Action ' + selectedItem.getText())
