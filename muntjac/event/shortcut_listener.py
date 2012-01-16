# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.event.action import IListener
from muntjac.event.shortcut_action import ShortcutAction


class ShortcutListener(ShortcutAction, IListener):

    def __init__(self, *args):

        nargs = len(args)
        if nargs == 1:
            shorthandCaption, = args
            super(ShortcutListener, self).__init__(shorthandCaption)
        elif nargs == 2:
            shorthandCaption, modifierKeys = args
            super(ShortcutListener, self).__init__(shorthandCaption,
                    modifierKeys)
        elif nargs == 3:
            caption, keyCode, modifierKeys = args
            super(ShortcutListener, self).__init__(caption, keyCode,
                    modifierKeys)
        elif nargs == 4:
            caption, icon, keyCode, modifierKeys = args
            super(ShortcutListener, self).__init__(caption, icon, keyCode,
                    modifierKeys)
        else:
            raise ValueError


    def handleAction(self, sender, target):
        pass
