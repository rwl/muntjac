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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.ui.Button import (Button,)


class NativeButton(Button):

    def __init__(self, *args):
        """None
        ---
        Creates a new switch button with initial value.

        @param state
                   the Initial state of the switch-button.
        @param initialState
        @deprecated use the {@link CheckBox} component instead
        ---
        Creates a new switch button that is connected to a boolean property.

        @param state
                   the Initial state of the switch-button.
        @param dataSource
        @deprecated use the {@link CheckBox} component instead
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            super(NativeButton, self)()
        elif _1 == 1:
            caption, = _0
            super(NativeButton, self)(caption)
        elif _1 == 2:
            if isinstance(_0[1], ClickListener):
                caption, listener = _0
                super(NativeButton, self)(caption, listener)
            elif isinstance(_0[1], Property):
                caption, dataSource = _0
                super(NativeButton, self)(caption, dataSource)
            else:
                caption, initialState = _0
                super(NativeButton, self)(caption, initialState)
        elif _1 == 3:
            caption, target, methodName = _0
            super(NativeButton, self)(caption, target, methodName)
        else:
            raise ARGERROR(0, 3)
