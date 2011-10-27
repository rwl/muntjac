
from muntjac.api import VerticalLayout
from muntjac.ui.menu_bar import MenuBar, ICommand
from muntjac.terminal.external_resource import ExternalResource


class MenuBarCollapsingExample(VerticalLayout):

    def __init__(self):
        super(MenuBarCollapsingExample, self).__init__()

        self._menubar = MenuBar()

        menuCommand = MenuCommand(self)

        # In order to collapse items, the MenuBar must have a specified width
        self._menubar.setWidth('50%')

        # Save reference to individual items so we can add sub-menu items to
        # them
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

        # Generate bogus items so we can show the collapsing
        for i in range(5):
            self._menubar.addItem('Item %d' % i, menuCommand).setEnabled(False)

        edit = self._menubar.addItem('Edit', None)
        edit.addItem('Undo', menuCommand)
        edit.addItem('Redo', menuCommand).setEnabled(False)
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

        # Generate bogus items so we can show the collapsing
        for i in range(5):
            self._menubar.addItem('Item %d' % i, menuCommand).setEnabled(False)

        self.addComponent(self._menubar)


class SearchCommand(ICommand):

    def __init__(self, c):
        self._c = c

    def menuSelected(self, selectedItem):
        er = ExternalResource('http://www.google.com')
        self._c.getWindow().open(er)


class MenuCommand(ICommand):

    def __init__(self, c):
        self._c = c

    def menuSelected(self, selectedItem):
        self._c.getWindow().showNotification('Action '
                + selectedItem.getText())
