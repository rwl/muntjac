
from muntjac.ui import \
    (VerticalLayout, HorizontalLayout, Panel, TextField, button, Button)

from muntjac.event.shortcut_listener import ShortcutListener
from muntjac.ui.component import IFocusable
from muntjac.ui.abstract_field import FocusShortcut
from muntjac.event.shortcut_action import KeyCode, ModifierKey
from muntjac.ui.button import ClickShortcut


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
        class NextFieldListener(ShortcutListener):

            def handleAction(self, sender, target):
                # The panel is the sender, loop trough content
                for nxt in sender.getComponentIterator():
                    # target is the field we're currently in, focus the next
                    if isinstance(nxt, IFocusable):
                        nxt.focus()

        p.addAction(NextFieldListener())

        # Firstname input with an input prompt for demo clarity
        firstname = TextField('Firstname')
        firstname.setInputPrompt('ALT-SHIFT-F to focus')
        p.addComponent(firstname)

        # Using firstname.addShortcutListener() would add globally,
        # but we want the shortcut only in this panel:
        p.addAction(FocusShortcut(firstname, KeyCode.F, ModifierKey.ALT,
                ModifierKey.SHIFT))

        # additinally we'll add a global shortcut for this field using the
        # shorthand notation (^1 == CTRL-1, etc)
        firstname.addShortcutListener(FocusShortcut(firstname,
                'Focus panel &_' + number))
        p.setDescription('CTRL-' + number + ' to focus')

        # Lastname input with an input prompt for demo clarity
        lastname = TextField('Lastname')
        lastname.setInputPrompt('ALT-SHIFT-L to focus')
        p.addComponent(lastname)

        # Using firstname.addShortcutListener() would add globally,
        # but we want the shortcut only in this panel:
        p.addAction(FocusShortcut(lastname, KeyCode.L, ModifierKey.ALT,
                ModifierKey.SHIFT))

        # Button with a simple click-listener
        class SaveListener(button.IClickListener):

            def __init__(self, c):
                self._c = c

            def buttonClick(self, event):
                self._c.getWindow().showNotification(self.p.getCaption()
                        + ' save clicked')

        save = Button('Save', SaveListener(self))
        p.addComponent(save)

        # setClickShortcut() would add global shortcut, instead we
        # 'scope' the shortcut to the panel:
        p.addAction(ClickShortcut(save, KeyCode.S, ModifierKey.ALT,
                ModifierKey.SHIFT))

        return p
