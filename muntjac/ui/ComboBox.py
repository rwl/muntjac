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
from com.vaadin.ui.Select import (Select,)
# from java.util.Collection import (Collection,)


class ComboBox(Select):
    """A filtering dropdown single-select. Suitable for newItemsAllowed, but it's
    turned of by default to avoid mistakes. Items are filtered based on user
    input, and loaded dynamically ("lazy-loading") from the server. You can turn
    on newItemsAllowed and change filtering mode (and also turn it off), but you
    can not turn on multi-select mode.
    """
    _inputPrompt = None

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.setMultiSelect(False)
            self.setNewItemsAllowed(False)
        elif _1 == 1:
            caption, = _0
            super(ComboBox, self)(caption)
            self.setMultiSelect(False)
            self.setNewItemsAllowed(False)
        elif _1 == 2:
            if isinstance(_0[1], Collection):
                caption, options = _0
                super(ComboBox, self)(caption, options)
                self.setMultiSelect(False)
                self.setNewItemsAllowed(False)
            else:
                caption, dataSource = _0
                super(ComboBox, self)(caption, dataSource)
                self.setMultiSelect(False)
                self.setNewItemsAllowed(False)
        else:
            raise ARGERROR(0, 2)

    def setMultiSelect(self, multiSelect):
        if multiSelect and not self.isMultiSelect():
            raise self.UnsupportedOperationException('Multiselect not supported')
        super(ComboBox, self).setMultiSelect(multiSelect)

    def getInputPrompt(self):
        """Gets the current input prompt.

        @see #setInputPrompt(String)
        @return the current input prompt, or null if not enabled
        """
        return self._inputPrompt

    def setInputPrompt(self, inputPrompt):
        """Sets the input prompt - a textual prompt that is displayed when the
        select would otherwise be empty, to prompt the user for input.

        @param inputPrompt
                   the desired input prompt, or null to disable
        """
        self._inputPrompt = inputPrompt
        self.requestRepaint()

    def paintContent(self, target):
        if self._inputPrompt is not None:
            target.addAttribute('prompt', self._inputPrompt)
        super(ComboBox, self).paintContent(target)
