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
