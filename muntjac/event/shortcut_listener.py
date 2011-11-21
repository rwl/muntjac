# Copyright (C) 2011 Vaadin Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

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
