# Copyright (C) 2010 IT Mill Ltd.
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

from warnings import warn

from muntjac.ui.button import Button, IClickListener
from muntjac.data.property import IProperty


class CheckBox(Button):

    CLIENT_WIDGET = None #ClientWidget(VCheckBox)

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
        @param listener:
                   the click listener
        ---
        Convenience method for creating a new switch button with a method
        listening button clicks. Using this method is discouraged because it
        cannot be checked during compilation. Use
        L{#addListener(Class, Object, Method)} or
        L{#addListener(com.vaadin.ui.Component.Listener)} instead. The
        method must have either no parameters, or only one parameter of
        Button.ClickEvent type.

        @param caption
                   the Button caption.
        @param target
                   the Object having the method for listening button clicks.
        @param methodName
                   the name of the method in target object, that receives
                   button click events.
        ---
        Creates a new switch button that is connected to a boolean property.

        @param state
                   the Initial state of the switch-button.
        @param dataSource
        ---
        Creates a new push button with a set caption.

        The value of the push button is always false and they are immediate
        by default.

        @param caption
                   the Button caption.
        """
        nargs = len(args)
        if nargs == 0:
            super(CheckBox, self).__init__()
            self.setSwitchMode(True)
        elif nargs == 1:
            caption, = args
            super(CheckBox, self).__init__(caption, False)
        elif nargs == 2:
            if isinstance(args[1], IClickListener):
                caption, listener = args
                super(CheckBox, self).__init__(caption, listener)
                self.setSwitchMode(True)
            elif isinstance(args[1], IProperty):
                caption, dataSource = args
                super(CheckBox, self).__init__(caption, dataSource)
                self.setSwitchMode(True)
            else:
                caption, initialState = args
                super(CheckBox, self).__init__(caption, initialState)
        elif nargs == 3:
            caption, target, methodName = args
            super(CheckBox, self).__init__(caption, target, methodName)
            self.setSwitchMode(True)
        else:
            raise ValueError, 'too many arguments'


    def setSwitchMode(self, switchMode):
        warn('CheckBox is always in switch mode', DeprecationWarning)

        if self._switchMode and not switchMode:
            raise NotImplementedError, ('CheckBox is always in switch '
                    'mode (consider using a Button)')

        super(CheckBox, self).setSwitchMode(True)
