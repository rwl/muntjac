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

"""Defines a text field that supports multi-line editing."""

from muntjac.ui.abstract_text_field import AbstractTextField
from muntjac.data.property import IProperty


class TextArea(AbstractTextField):
    """A text field that supports multi line editing."""

    CLIENT_WIDGET = None #ClientWidget(VTextArea, LoadStyle.EAGER)

    _DEFAULT_ROWS = 5

    def __init__(self, *args):
        """Constructs a TextArea with an optional caption, data source,
        and/or value.

        @param args: tuple of the form
            - ()
            - (caption)
              1. the caption for the field
            - (dataSource)
              1. the data source for the field
            - (caption, dataSource)
              1. the caption for the field
              2. the data source for the field
            - (caption, value)
              1. the caption for the field
              2. the value for the field
        """
        # Number of visible rows in the text area.
        self._rows = self._DEFAULT_ROWS

        # Tells if word-wrapping should be used in the text area.
        self._wordwrap = True

        nargs = len(args)
        if nargs == 0:
            super(TextArea, self).__init__()
            self.setValue('')
        elif nargs == 1:
            if isinstance(args[0], IProperty):
                dataSource, = args
                TextArea.__init__(self)
                self.setPropertyDataSource(dataSource)
            else:
                caption, = args
                TextArea.__init__(self)
                self.setCaption(caption)
        elif nargs == 2:
            if isinstance(args[1], IProperty):
                caption, dataSource = args
                TextArea.__init__(self, dataSource)
                self.setCaption(caption)
            else:
                caption, value = args
                TextArea.__init__(self, caption)
                self.setValue(value)
        else:
            raise ValueError, 'too many arguments'


    def setRows(self, rows):
        """Sets the number of rows in the text area.

        @param rows: the number of rows for this text area.
        """
        if rows < 0:
            rows = 0

        if self._rows != rows:
            self._rows = rows
            self.requestRepaint()


    def getRows(self):
        """Gets the number of rows in the text area.

        @return: number of explicitly set rows.
        """
        return self._rows


    def setWordwrap(self, wordwrap):
        """Sets the text area's word-wrap mode on or off.

        @param wordwrap:
                   the boolean value specifying if the text area should be
                   in word-wrap mode.
        """
        if self._wordwrap != wordwrap:
            self._wordwrap = wordwrap
            self.requestRepaint()


    def isWordwrap(self):
        """Tests if the text area is in word-wrap mode.

        @return: C{True} if the component is in word-wrap mode,
                 C{False} if not.
        """
        return self._wordwrap


    def paintContent(self, target):
        super(TextArea, self).paintContent(target)

        target.addAttribute('rows', self.getRows())

        if not self.isWordwrap():
            # Wordwrap is only painted if turned off to minimize
            # communications
            target.addAttribute('wordwrap', False)
