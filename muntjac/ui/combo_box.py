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

"""Defines a filtering drop-down single-select."""

from muntjac.ui.select import Select
from muntjac.data.container import IContainer

from muntjac.terminal.gwt.client.ui.v_filter_select import VFilterSelect


class ComboBox(Select):
    """A filtering dropdown single-select. Suitable for newItemsAllowed, but
    it's turned of by default to avoid mistakes. Items are filtered based on
    user input, and loaded dynamically ("lazy-loading") from the server. You
    can turn on newItemsAllowed and change filtering mode (and also turn it
    off), but you can not turn on multi-select mode.
    """

    CLIENT_WIDGET = None #ClientWidget(VFilterSelect)

    def __init__(self, *args):
        self._inputPrompt = None

        #: If text input is not allowed, the ComboBox behaves like a pretty
        #  NativeSelect - the user can not enter any text and clicking the
        #  text field opens the drop down with options
        self._textInputAllowed = True

        nargs = len(args)
        if nargs == 0:
            super(ComboBox, self).__init__()
            self.setMultiSelect(False)
            self.setNewItemsAllowed(False)
        elif nargs == 1:
            caption, = args
            super(ComboBox, self).__init__(caption)
            self.setMultiSelect(False)
            self.setNewItemsAllowed(False)
        elif nargs == 2:
            if isinstance(args[1], IContainer):
                caption, dataSource = args
                super(ComboBox, self).__init__(caption, dataSource)
                self.setMultiSelect(False)
                self.setNewItemsAllowed(False)
            else:
                caption, options = args
                super(ComboBox, self).__init__(caption, options)
                self.setMultiSelect(False)
                self.setNewItemsAllowed(False)
        else:
            raise ValueError, 'too many arguments'


    def setMultiSelect(self, multiSelect):
        if multiSelect and not self.isMultiSelect():
            raise NotImplementedError, 'Multiselect not supported'

        super(ComboBox, self).setMultiSelect(multiSelect)


    def getInputPrompt(self):
        """Gets the current input prompt.

        @see: L{setInputPrompt}
        @return: the current input prompt, or null if not enabled
        """
        return self._inputPrompt


    def setInputPrompt(self, inputPrompt):
        """Sets the input prompt - a textual prompt that is displayed when
        the select would otherwise be empty, to prompt the user for input.

        @param inputPrompt:
                   the desired input prompt, or null to disable
        """
        self._inputPrompt = inputPrompt
        self.requestRepaint()


    def paintContent(self, target):
        if self._inputPrompt is not None:
            target.addAttribute('prompt', self._inputPrompt)

        super(ComboBox, self).paintContent(target)

        if not self._textInputAllowed:
            target.addAttribute(VFilterSelect.ATTR_NO_TEXT_INPUT, True)


    def setTextInputAllowed(self, textInputAllowed):
        """Sets whether it is possible to input text into the field or whether
        the field area of the component is just used to show what is selected.
        By disabling text input, the comboBox will work in the same way as a
        L{NativeSelect}

        @see L{isTextInputAllowed}

        @param textInputAllowed:
                 true to allow entering text, false to just show the current
                 selection
        """
        self._textInputAllowed = textInputAllowed
        self.requestRepaint()


    def isTextInputAllowed(self):
        """Returns true if the user can enter text into the field to either
        filter the selections or enter a new value if :{isNewItemsAllowed}
        returns true. If text input is disabled, the comboBox will work in the
        same way as a L{NativeSelect}.
        """
        return self._textInputAllowed
