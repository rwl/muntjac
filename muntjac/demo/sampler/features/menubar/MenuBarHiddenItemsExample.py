
from muntjac.ui.vertical_layout import VerticalLayout
from muntjac.api import MenuBar, Button
from muntjac.ui.menu_bar import ICommand
from muntjac.terminal.external_resource import ExternalResource
from muntjac.ui.button import IClickListener


class MenuBarHiddenItemsExample(VerticalLayout):

    def __init__(self):
        super(MenuBarHiddenItemsExample, self).__init__()

        self._menubar = MenuBar()

        menuCommand = MenuCommand(self)

        # Save reference to individual items so we can add sub-menu
        # items to them
        f = self._menubar.addItem('File', None)
        newItem = f.addItem('New', None)
        f.addItem('Open f...', menuCommand)
        f.addSeparator()
        newItem.addItem('File', menuCommand)
        newItem.addItem('Folder', menuCommand)
        newItem.addItem('Project...', menuCommand)
        f.addItem('Close', menuCommand)
        f.addItem('Close All', menuCommand)
        f.addSeparator()
        f.addItem('Save', menuCommand)
        f.addItem('Save As...', menuCommand)
        f.addItem('Save All', menuCommand)

        edit = self._menubar.addItem('Edit', None)
        edit.addItem('Undo', menuCommand)

        redo = edit.addItem('Redo', menuCommand)
        redo.setEnabled(False)

        edit.addSeparator()
        edit.addItem('Cut', menuCommand)
        edit.addItem('Copy', menuCommand)
        edit.addItem('Paste', menuCommand)
        edit.addSeparator()

        find = edit.addItem('Find/Replace', menuCommand)

        # Actions can be added inline as well, of course
        find.addItem('Google Search', SearchCommand(self))
        find.addSeparator()
        find.addItem('Find/Replace...', menuCommand)
        find.addItem('Find Next', menuCommand)
        find.addItem('Find Previous', menuCommand)

        view = self._menubar.addItem('View', None)
        view.addItem('Show/Hide Status Bar', menuCommand)
        view.addItem('Customize Toolbar...', menuCommand)
        view.addSeparator()
        view.addItem('Actual Size', menuCommand)
        view.addItem('Zoom In', menuCommand)
        view.addItem('Zoom Out', menuCommand)

        self.addComponent(self._menubar)
        self.addComponent( Button('Hide File menu', HideListener(f)) )

        l = RedoListener(redo)
        self.addComponent( Button('Enable Edit -> Redo action', l) )
        self.setSpacing(True)


class SearchCommand(ICommand):

    def __init__(self, c):
        self._c = c

    def menuSelected(self, selectedItem):
        er = ExternalResource('http://www.google.com')
        self._c.getWindow().open(er)


class HideListener(IClickListener):

    def __init__(self, f):
        self._f = f

    def buttonClick(self, event):
        self._f.setVisible(not self._f.isVisible())
        event.getButton().setCaption('Hide File menu' \
                if self._f.isVisible() else 'Show File menu')


class RedoListener(IClickListener):

    def __init__(self, redo):
        self._redo = redo

    def buttonClick(self, event):
        self._redo.setEnabled(not self._redo.isEnabled())
        event.getButton().setCaption('Disable Edit -> Redo action' \
                if self._redo.isEnabled() else 'Enable Edit -> Redo action')


class MenuCommand(ICommand):

    def __init__(self, c):
        self._c = c

    def menuSelected(self, selectedItem):
        self._c.getWindow().showNotification('Action '
                + selectedItem.getText())
