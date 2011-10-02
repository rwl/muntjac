# -*- coding: utf-8 -*-
# from com.vaadin.event.ShortcutAction.KeyCode import (KeyCode,)
# from com.vaadin.event.ShortcutAction.ModifierKey import (ModifierKey,)
# from com.vaadin.ui.AbstractField.FocusShortcut import (FocusShortcut,)


class ShortcutBasicsExample(VerticalLayout):

    def __init__(self):
        self.setSpacing(True)
        # Firstname input with an input prompt for demo clarity
        firstname = TextField('Firstname')
        firstname.setInputPrompt('ALT-SHIFT-F to focus')
        self.addComponent(firstname)
        # Add global shortcut that focuses the field
        firstname.addShortcutListener(FocusShortcut(firstname, KeyCode.F, ModifierKey.ALT, ModifierKey.SHIFT))
        # Lastname input with an input prompt for demo clarity
        lastname = TextField('Lastname')
        lastname.setInputPrompt('ALT-SHIFT-L to focus')
        self.addComponent(lastname)
        # Add global shortcut that focuses the field
        lastname.addShortcutListener(FocusShortcut(lastname, KeyCode.L, ModifierKey.ALT, ModifierKey.SHIFT))
        # Button with a simple click-listener

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                self.getWindow().showNotification('Enter button clicked')

        _0_ = _0_()
        enter = Button('Enter', _0_)
        self.addComponent(enter)
        enter.setStyleName('primary')
        # make it look like it's default
        # Add global shortcut using the built-in helper
        enter.setClickShortcut(KeyCode.ENTER)
        # which is easier to find, but otherwise equal to:
        # enter.addShortcutListener(new ClickShortcut(search,KeyCode.ENTER));
