
from muntjac.api import VerticalLayout, MenuBar
from muntjac.terminal.external_resource import ExternalResource
from muntjac.ui.menu_bar import ICommand


class MenuBarTooltipsExample(VerticalLayout):

    def __init__(self):
        super(MenuBarTooltipsExample, self).__init__()

        self._menubar = MenuBar()

        menuCommand = MenuCommand(self)

        # Add tooltip to the menubar itself
        self._menubar.setDescription('Perform some actions by selecting '
                'them from the menus')

        # Save reference to individual items so we can add sub-menu
        # items to them
        f = self._menubar.addItem('File', None)
        f.setDescription('File menu')
        newItem = f.addItem('New', None)
        newItem.setDescription('Add a new..')
        opn = f.addItem('Open file...', menuCommand)
        opn.setDescription('Retrieve a file from the filesystem')
        f.addSeparator()

        item = newItem.addItem('File', menuCommand)
        item.setDescription('Open a file')
        item = newItem.addItem('Folder', menuCommand)
        item.setDescription('Open a folder')
        item = newItem.addItem('Project...', menuCommand)
        item.setDescription('Open a project')
        item = f.addItem('Close', menuCommand)
        item.setDescription('Closes the selected file')
        item = f.addItem('Close All', menuCommand)
        item.setDescription('Closes all files')

        f.addSeparator()
        item = f.addItem('Save', menuCommand)
        item.setDescription('Saves the file')
        item = f.addItem('Save As...', menuCommand)
        item.setDescription('Saves the file with a different name')
        item = f.addItem('Save All', menuCommand)
        item.setDescription('Saves all files')

        edit = self._menubar.addItem('Edit', None)
        edit.setDescription('Edit menu')
        item = edit.addItem('Undo', menuCommand)
        item.setDescription('Reverses recent changes')
        item = edit.addItem('Redo', menuCommand)
        item.setEnabled(False)
        item.setDescription('Redoes undone changed')

        edit.addSeparator()
        item = edit.addItem('Cut', menuCommand)
        item.setDescription('Copies the text to the clipboard and removes it')
        item = edit.addItem('Copy', menuCommand)
        item.setDescription('Copies the text to the clipboard')
        item = edit.addItem('Paste', menuCommand)
        item.setDescription('Copies the contents of the clipboard on to the document')

        edit.addSeparator()
        find = edit.addItem('Find/Replace', menuCommand)
        find.setDescription('Find or Replace text')

        # Actions can be added inline as well, of course
        item = find.addItem('Google Search', SearchCommand(self))
        item.setDescription('Search with Google')

        find.addSeparator()
        item = find.addItem('Find/Replace...', menuCommand)
        item.setDescription('Finds or replaces text')
        item = find.addItem('Find Next', menuCommand)
        item.setDescription('Find the next occurrence')
        item = find.addItem('Find Previous', menuCommand)
        item.setDescription('Find the previous occurrence')

        view = self._menubar.addItem('View', None)
        view.setDescription('View menu')
        item = view.addItem('Show/Hide Status Bar', menuCommand)
        item.setDescription('Toggles the visibility of the Status Bar')
        item = view.addItem('Customize Toolbar...', menuCommand)
        item.setDescription('Add or remove items in the toolbar')

        view.addSeparator()
        item = view.addItem('Actual Size', menuCommand)
        item.setDescription('Resize view to the original size')
        item = view.addItem('Zoom In', menuCommand)
        item.setDescription('Zoom the document in by 10%')
        item = view.addItem('Zoom Out', menuCommand)
        item.setDescription('Zoom the doucment out by 10%')

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
