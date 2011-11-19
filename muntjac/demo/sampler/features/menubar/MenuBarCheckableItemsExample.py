
from muntjac.api import VerticalLayout, MenuBar
from muntjac.ui.menu_bar import ICommand


class MenuBarCheckableItemsExample(VerticalLayout):

    def __init__(self):
        super(MenuBarCheckableItemsExample, self).__init__()

        self._menubar = MenuBar()

        menuCommand = MenuCommand(self)

        f = self._menubar.addItem('File', None)
        f.addItem('New...', menuCommand)
        f.addItem('Open...', menuCommand)
        f.addSeparator()
        f.addItem('Save', menuCommand)
        f.addSeparator()
        # Save on exit is checkable but we do not want any listener to be
        # called when its state changes
        saveOnExit = f.addItem('Save on exit', menuCommand)
        saveOnExit.setCheckable(True)
        saveOnExit.setChecked(True)
        f.addSeparator()
        f.addItem('Exit', menuCommand)

        settings = self._menubar.addItem('Settings', None)
        # These settings are checkable and the listener is called when their
        # state changes
        setting1 = settings.addItem('Allow settings to be changed by all users',
                menuCommand)
        setting1.setCheckable(True)
        setting1.setChecked(True)

        setting2 = settings.addItem('Convert XML files automatically',
                menuCommand)
        setting2.setCheckable(True)

        setting3 = settings.addItem('Convert files automatically',
                menuCommand)
        setting3.setCheckable(True)
        settings.addSeparator()

        # This could be used to show a popup with all the settings for the
        # application
        settings.addItem('More settings...', menuCommand)
        self.addComponent(self._menubar)


class MenuCommand(ICommand):

    def __init__(self, c):
        self._c = c

    def menuSelected(self, selectedItem):
        if selectedItem.isCheckable():
            self._c.getWindow().showNotification('\'' + selectedItem.getText()
                    + '\' was set to '
                    + ('true' if selectedItem.isChecked() else 'false'))
        else:
            self._c.getWindow().showNotification('Non-selectable item \''
                    + selectedItem.getText() + '\' was clicked')
