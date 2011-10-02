# -*- coding: utf-8 -*-


class MenuBarCheckableItemsExample(VerticalLayout):
    _menubar = MenuBar()

    def __init__(self):
        file = self._menubar.addItem('File', None)
        file.addItem('New...', self.menuCommand)
        file.addItem('Open...', self.menuCommand)
        file.addSeparator()
        file.addItem('Save', self.menuCommand)
        file.addSeparator()
        # Save on exit is checkable but we do not want any listener to be
        # called when its state changes
        saveOnExit = file.addItem('Save on exit', None)
        saveOnExit.setCheckable(True)
        saveOnExit.setChecked(True)
        file.addSeparator()
        file.addItem('Exit', self.menuCommand)
        settings = self._menubar.addItem('Settings', None)
        # These settings are checkable and the listener is called when their
        # state changes
        setting1 = settings.addItem('Allow settings to be changed by all users', self.menuCommand)
        setting1.setCheckable(True)
        setting1.setChecked(True)
        setting2 = settings.addItem('Convert XML files automatically', self.menuCommand)
        setting2.setCheckable(True)
        setting3 = settings.addItem('Convert files automatically', self.menuCommand)
        setting3.setCheckable(True)
        settings.addSeparator()
        # This could be used to show a popup with all the settings for the
        # application
        settings.addItem('More settings...', self.menuCommand)
        self.addComponent(self._menubar)

    class menuCommand(Command):

        def menuSelected(self, selectedItem):
            if selectedItem.isCheckable():
                self.getWindow().showNotification('\'' + selectedItem.getText() + '\' was set to ' + selectedItem.isChecked())
            else:
                self.getWindow().showNotification('Non-selectable item \'' + selectedItem.getText() + '\' was clicked')
