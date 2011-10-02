# -*- coding: utf-8 -*-
# from com.vaadin.event.ShortcutListener import (ShortcutListener,)
# from com.vaadin.ui.Button.ClickShortcut import (ClickShortcut,)
# from com.vaadin.ui.ComponentContainer import (ComponentContainer,)
# from java.util.Iterator import (Iterator,)


class ShortcutScopeExample(VerticalLayout):

    def __init__(self):
        self.setSpacing(True)
        # We want the panels side-by-side
        hz = HorizontalLayout()
        hz.setSpacing(True)
        self.addComponent(hz)
        # Add two identical panels
        hz.addComponent(self.createPanel(1))
        hz.addComponent(self.createPanel(2))

    def createPanel(self, number):
        p = Panel('Panel ' + number)
        p.getContent().setSpacing(True)
        # Let's create a customized shortcut that jumps to the next field

        class _0_(ShortcutListener):

            def handleAction(self, sender, target):
                # The panel is the sender, loop trough content
                _0 = True
                it = sender.getComponentIterator()
                while True:
                    if _0 is True:
                        _0 = False
                    if not it.hasNext():
                        break
                    # target is the field we're currently in, focus the next
                    if it.next() == target and it.hasNext():
                        next = it.next()
                        if isinstance(next, self.Focusable):
                            next.focus()

        _0_ = _0_()
        p.addAction(_0_)
        # Firstname input with an input prompt for demo clarity
        firstname = TextField('Firstname')
        firstname.setInputPrompt('ALT-SHIFT-F to focus')
        p.addComponent(firstname)
        # Using firstname.addShortcutListener() would add globally,
        # but we want the shortcut only in this panel:
        p.addAction(FocusShortcut(firstname, KeyCode.F, ModifierKey.ALT, ModifierKey.SHIFT))
        # additinally we'll add a global shortcut for this field using the
        # shorthand notation (^1 == CTRL-1, etc)
        firstname.addShortcutListener(FocusShortcut(firstname, 'Focus panel &_' + number))
        p.setDescription('CTRL-' + number + ' to focus')
        # Lastname input with an input prompt for demo clarity
        lastname = TextField('Lastname')
        lastname.setInputPrompt('ALT-SHIFT-L to focus')
        p.addComponent(lastname)
        # Using firstname.addShortcutListener() would add globally,
        # but we want the shortcut only in this panel:
        p.addAction(FocusShortcut(lastname, KeyCode.L, ModifierKey.ALT, ModifierKey.SHIFT))
        # Button with a simple click-listener

        class _1_(Button.ClickListener):

            def buttonClick(self, event):
                self.getWindow().showNotification(self.p.getCaption() + ' save clicked')

        _1_ = _1_()
        save = Button('Save', _1_)
        p.addComponent(save)
        # setClickShortcut() would add global shortcut, instead we
        # 'scope' the shortcut to the panel:
        p.addAction(ClickShortcut(save, KeyCode.S, ModifierKey.ALT, ModifierKey.SHIFT))
        return p
