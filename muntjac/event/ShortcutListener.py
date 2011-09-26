# Copyright (C) 2011 Vaadin Ltd
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

from muntjac.event.Action import Listener
from muntjac.event.ShortcutAction import ShortcutAction


class ShortcutListener(ShortcutAction, Listener):

    def __init__(self, *args):

        nargs = len(args)
        if nargs == 1:
            shorthandCaption, = args
            super(ShortcutListener, self)(shorthandCaption)
        elif nargs == 2:
            shorthandCaption, modifierKeys = args
            super(ShortcutListener, self)(shorthandCaption, modifierKeys)
        elif nargs == 3:
            caption, keyCode, modifierKeys = args
            super(ShortcutListener, self)(caption, keyCode, modifierKeys)
        elif nargs == 4:
            caption, icon, keyCode, modifierKeys = args
            super(ShortcutListener, self)(caption, icon, keyCode, modifierKeys)
        else:
            raise ValueError


    def handleAction(self, sender, target):
        pass
