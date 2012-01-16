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

"""Defines a text editor component."""

from warnings import warn

from muntjac.ui.abstract_text_field import AbstractTextField
from muntjac.data.property import IProperty


class TextField(AbstractTextField):
    """A text editor component that can be bound to any bindable IProperty.
    The text editor supports both multiline and single line modes, default
    is one-line mode.

    Since C{TextField} extends C{AbstractField} it implements the
    L{IBuffered} interface. A C{TextField} is in write-through mode by default,
    so L{AbstractField.setWriteThrough} must be called to enable buffering.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    CLIENT_WIDGET = None #ClientWidget(VTextField, LoadStyle.EAGER)

    def __init__(self, *args):
        """Constructs a C{TextField} with optional caption, dataSource and/or
        value.

        @param args: tuple of the form
            - ()
            - (caption)
              1. the caption string for the editor
            - (dataSource)
              1. the IProperty to be edited with this editor
            - (caption, dataSource)
              1. the caption string for the editor
              2. the IProperty to be edited with this editor
            - (caption, text)
              1. the caption string for the editor
              2. the initial text content of the editor
        """
        #: Tells if input is used to enter sensitive information that is not
        #  echoed to display. Typically passwords.
        self._secret = False

        #: Number of visible rows in a multiline TextField. Value 0 implies a
        #  single-line text-editor.
        self._rows = 0

        #: Tells if word-wrapping should be used in multiline mode.
        self._wordwrap = True

        nargs = len(args)
        if nargs == 0:
            super(TextField, self).__init__()
            self.setValue('')
        elif nargs == 1:
            if isinstance(args[0], IProperty):
                super(TextField, self).__init__()
                dataSource, = args
                self.setPropertyDataSource(dataSource)
            else:
                caption, = args
                TextField.__init__(self)
                self.setCaption(caption)
        elif nargs == 2:
            if isinstance(args[1], IProperty):
                caption, dataSource = args
                TextField.__init__(self, dataSource)
                self.setCaption(caption)
            else:
                super(TextField, self).__init__()
                caption, value = args
                self.setValue(value)
                self.setCaption(caption)
        else:
            raise ValueError, 'too many arguments'


    def isSecret(self):
        """Gets the secret property. If a field is used to enter secret
        information the information is not echoed to display.

        @return: C{True} if the field is used to enter secret
                 information, C{False} otherwise.

        @deprecated: Use L{PasswordField} instead for secret text input.
        """
        warn('use PasswordField instead', DeprecationWarning)

        return self._secret


    def setSecret(self, secret):
        """Sets the secret property on and off. If a field is used to enter
        secret information the information is not echoed to display.

        @param secret:
                   the value specifying if the field is used to enter secret
                   information.
        @deprecated: Use L{PasswordField} instead for secret text input.
        """
        warn('use PasswordField instead', DeprecationWarning)

        if self._secret != secret:
            self._secret = secret
            self.requestRepaint()


    def paintContent(self, target):
        if self.isSecret():
            target.addAttribute('secret', True)

        rows = self.getRows()
        if rows != 0:
            target.addAttribute('rows', rows)
            target.addAttribute('multiline', True)

            if not self.isWordwrap():
                # Wordwrap is only painted if turned off to minimize
                # communications
                target.addAttribute('wordwrap', False)

        super(TextField, self).paintContent(target)


    def getRows(self):
        """Gets the number of rows in the editor. If the number of rows is set
        to 0, the actual number of displayed rows is determined implicitly by
        the adapter.

        @return: number of explicitly set rows.
        @deprecated: Use L{TextArea} for a multi-line text input.
        """
        warn('use TextArea for a multi-line text input', DeprecationWarning)

        return self._rows


    def setRows(self, rows):
        """Sets the number of rows in the editor.

        @param rows:
                   the number of rows for this editor.
        @deprecated: Use L{TextArea} for a multi-line text input.
        """
        warn('use TextArea for a multi-line text input', DeprecationWarning)

        if rows < 0:
            rows = 0

        if self._rows != rows:
            self._rows = rows
            self.requestRepaint()


    def isWordwrap(self):
        """Tests if the editor is in word-wrap mode.

        @return: C{True} if the component is in the word-wrap mode,
                 C{False} if not.
        @deprecated: Use L{TextArea} for a multi-line text input.
        """
        warn('use TextArea for a multi-line text input', DeprecationWarning)
        return self._wordwrap


    def setWordwrap(self, wordwrap):
        """Sets the editor's word-wrap mode on or off.

        @param wordwrap:
                   the boolean value specifying if the editor should be in
                   word-wrap mode after the call or not.

        @deprecated: Use L{TextArea} for a multi-line text input.
        """
        warn('use TextArea for a multi-line text input', DeprecationWarning)
        if self._wordwrap != wordwrap:
            self._wordwrap = wordwrap
            self.requestRepaint()


    def setHeight(self, height, unit=None):
        """Sets the height of the L{TextField} instance.

        Setting height for L{TextField} also has a side-effect that puts
        L{TextField} into multiline mode (aka "textarea"). Multiline mode
        can also be achieved by calling L{setRows}. The height
        value overrides the number of rows set by L{setRows}.

        If you want to set height of single line L{TextField}, call
        L{setRows} with value 0 after setting the height. Setting
        rows to 0 resets the side-effect.

        You should use L{TextArea} instead of L{TextField} for multiline
        text input.
        """
        if unit is None:
            # will call setHeight(float, int) the actually does the magic.
            # Method is overridden just to document side-effects.
            super(TextField, self).setHeight(height)
        else:
            super(TextField, self).setHeight(height, unit)
            if height > 1 and self.__class__ == TextField:
                # In html based terminals we most commonly want to make
                # component to be textarea if height is defined. Setting row
                # field above 0 will render component as textarea.
                self.setRows(2)
