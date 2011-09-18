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
# from java.lang.reflect.Method import (Method,)


class CheckBox(Button):

    def __init__(self, *args):
        """Creates a new switch button.
        ---
        Creates a new switch button with a caption and a set initial state.

        @param caption
                   the caption of the switch button
        @param initialState
                   the initial state of the switch button
        ---
        Creates a new switch button with a caption and a click listener.

        @param caption
                   the caption of the switch button
        @param listener
                   the click listener
        ---
        Convenience method for creating a new switch button with a method
        listening button clicks. Using this method is discouraged because it
        cannot be checked during compilation. Use
        {@link #addListener(Class, Object, Method)} or
        {@link #addListener(com.vaadin.ui.Component.Listener)} instead. The
        method must have either no parameters, or only one parameter of
        Button.ClickEvent type.

        @param caption
                   the Button caption.
        @param target
                   the Object having the method for listening button clicks.
        @param methodName
                   the name of the method in target object, that receives button
                   click events.
        ---
        Creates a new switch button that is connected to a boolean property.

        @param state
                   the Initial state of the switch-button.
        @param dataSource
        ---
        Creates a new push button with a set caption.

        The value of the push button is always false and they are immediate by
        default.

        @param caption
                   the Button caption.
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.setSwitchMode(True)
        elif _1 == 1:
            caption, = _0
            super(CheckBox, self)(caption, False)
        elif _1 == 2:
            if isinstance(_0[1], ClickListener):
                caption, listener = _0
                super(CheckBox, self)(caption, listener)
                self.setSwitchMode(True)
            elif isinstance(_0[1], Property):
                caption, dataSource = _0
                super(CheckBox, self)(caption, dataSource)
                self.setSwitchMode(True)
            else:
                caption, initialState = _0
                super(CheckBox, self)(caption, initialState)
        elif _1 == 3:
            caption, target, methodName = _0
            super(CheckBox, self)(caption, target, methodName)
            self.setSwitchMode(True)
        else:
            raise ARGERROR(0, 3)

    def setSwitchMode(self, switchMode):
        if self.switchMode and not switchMode:
            raise self.UnsupportedOperationException('CheckBox is always in switch mode (consider using a Button)')
        super(CheckBox, self).setSwitchMode(True)
