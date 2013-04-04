# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

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
