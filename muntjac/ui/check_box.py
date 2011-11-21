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

"""Defines a switch button."""

from warnings import warn

from muntjac.ui.button import Button, IClickListener
from muntjac.data.property import IProperty


class CheckBox(Button):

    CLIENT_WIDGET = None #ClientWidget(VCheckBox)

    def __init__(self, *args):
        """Creates a new switch button.

        @param args: tuple of the form
            - (caption, initialState)
              1. the caption of the switch button
              2. the initial state of the switch button
            - (caption, listener)
              1. the caption of the switch button
              2. the click listener
            - (caption, target, methodName)
              1. the Button caption.
              2. the Object having the method for listening button clicks.
              3. the name of the method in target object, that receives
                 button click events.
            - (state, dataSource)
              1. the Initial state of the switch-button.
              2. boolean property
            - (caption)
              1. the switch button caption
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


    def setDisableOnClick(self, disableOnClick):
        raise NotImplementedError, "CheckBox does not support disable on click"
