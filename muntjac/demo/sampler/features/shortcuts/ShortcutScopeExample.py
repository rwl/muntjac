
from muntjac.api import \
    VerticalLayout, HorizontalLayout, Panel, TextField, Button

from muntjac.event.shortcut_listener import ShortcutListener
from muntjac.ui.component import IFocusable
from muntjac.ui.abstract_field import FocusShortcut
from muntjac.event.shortcut_action import KeyCode, ModifierKey
from muntjac.ui.button import ClickShortcut, IClickListener


class ShortcutScopeExample(VerticalLayout):

    def __init__(self):
        super(ShortcutScopeExample, self).__init__()

        self.setSpacing(True)

        # We want the panels side-by-side
        hz = HorizontalLayout()
        hz.setSpacing(True)
        self.addComponent(hz)

        # Add two identical panels
        hz.addComponent(self.createPanel(1))
        hz.addComponent(self.createPanel(2))


    def createPanel(self, number):
        p = Panel('Panel %d' % number)
        p.getContent().setSpacing(True)

        # Let's create a customized shortcut that jumps to the next field
        p.addAction(NextFieldListener("Next field", KeyCode.ARROW_DOWN, None))

        # Firstname input with an input prompt for demo clarity
        firstname = TextField('Firstname')
        firstname.setInputPrompt('ALT-SHIFT-F to focus')
        p.addComponent(firstname)

        # Using firstname.addShortcutListener() would add globally,
        # but we want the shortcut only in this panel:
        p.addAction(FocusShortcut(firstname, KeyCode.F, ModifierKey.ALT,
                ModifierKey.SHIFT))

        # additinally we'll add a global shortcut for this field using the
        # shorthand notation (^1 == CTRL-1,NextFieldListener etc)
        firstname.addShortcutListener(FocusShortcut(firstname,
                'Focus panel &_' + str(number)))
        p.setDescription('CTRL-' + str(number) + ' to focus')

        # Lastname input with an input prompt for demo clarity
        lastname = TextField('Lastname')
        lastname.setInputPrompt('ALT-SHIFT-L to focus')
        p.addComponent(lastname)

        # Using firstname.addShortcutListener() would add globally,
        # but we want the shortcut only in this panel:
        p.addAction(FocusShortcut(lastname, KeyCode.L, ModifierKey.ALT,
                ModifierKey.SHIFT))

        # Button with a simple click-listener
        save = Button('Save', SaveListener(self, p))
        p.addComponent(save)

        # setClickShortcut() would add global shortcut, instead we
        # 'scope' the shortcut to the panel:
        p.addAction(ClickShortcut(save, KeyCode.S, ModifierKey.ALT,
                ModifierKey.SHIFT))

        return p


class NextFieldListener(ShortcutListener):

    def handleAction(self, sender, target):
        # The panel is the sender, loop trough content
        for nxt in sender.getComponentIterator():
            # target is the field we're currently in, focus the next
            if isinstance(nxt, IFocusable):
                nxt.focus()


class SaveListener(IClickListener):

    def __init__(self, c, panel):
        self._c = c
        self._panel = panel

    def buttonClick(self, event):
        self._c.getWindow().showNotification(self._panel.getCaption()
                + ' save clicked')
