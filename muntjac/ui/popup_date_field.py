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

"""Defines a date entry component."""

from muntjac.ui.date_field import DateField
from muntjac.data.property import IProperty


class PopupDateField(DateField):
    """A date entry component, which displays the actual date selector
    as a popup.

    @see: L{DateField}
    @see: L{InlineDateField}
    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, *args):
        self._inputPrompt = None

        nargs = len(args)
        if nargs == 0:
            super(PopupDateField, self).__init__()
        elif nargs == 1:
            if isinstance(args[0], IProperty):
                dataSource, = args
                super(PopupDateField, self).__init__(dataSource)
            else:
                caption, = args
                super(PopupDateField, self).__init__(caption)
        elif nargs == 2:
            if isinstance(args[1], IProperty):
                caption, dataSource = args
                super(PopupDateField, self).__init__(caption, dataSource)
            else:
                caption, value = args
                super(PopupDateField, self).__init__(caption, value)
        else:
            raise ValueError, 'too many arguments'


    def paintContent(self, target):
        super(PopupDateField, self).paintContent(target)
        if self._inputPrompt is not None:
            target.addAttribute('prompt', self._inputPrompt)


    def getInputPrompt(self):
        """Gets the current input prompt.

        @see: L{setInputPrompt}
        @return: the current input prompt, or null if not enabled
        """
        return self._inputPrompt


    def setInputPrompt(self, inputPrompt):
        """Sets the input prompt - a textual prompt that is displayed when
        the field would otherwise be empty, to prompt the user for input.
        """
        self._inputPrompt = inputPrompt
        self.requestRepaint()
