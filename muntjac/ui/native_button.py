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

"""Defines a switch button with native styling."""

from muntjac.ui.button import Button, IClickListener
from muntjac.data.property import IProperty


class NativeButton(Button):

    CLIENT_WIDGET = None #ClientWidget(VNativeButton)

    def __init__(self, *args):
        """Creates a new switch button.

        @param args: tuple of the form
            - ()
            - (caption)
            - (state, initialState)
              1. the Initial state of the switch-button.
              2.
            - (state, dataSource)
              1. the initial state of the switch-button.
              2. boolean property

        @deprecated: use the L{CheckBox} component instead
        """
        nargs = len(args)
        if nargs == 0:
            super(NativeButton, self).__init__()
        elif nargs == 1:
            caption, = args
            super(NativeButton, self).__init__(caption)
        elif nargs == 2:
            if isinstance(args[1], IClickListener):
                caption, listener = args
                super(NativeButton, self).__init__(caption, listener)
            elif isinstance(args[1], IProperty):
                caption, dataSource = args
                super(NativeButton, self).__init__(caption, dataSource)
            else:
                caption, initialState = args
                super(NativeButton, self).__init__(caption, initialState)
        elif nargs == 3:
            caption, target, methodName = args
            super(NativeButton, self).__init__(caption, target, methodName)
        else:
            raise ValueError, 'too many arguments'
