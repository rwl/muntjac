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
from com.vaadin.ui.AbstractTextField import (AbstractTextField,)


class TextArea(AbstractTextField):
    """A text field that supports multi line editing."""
    _DEFAULT_ROWS = 5
    # Number of visible rows in the text area.
    _rows = _DEFAULT_ROWS
    # Tells if word-wrapping should be used in the text area.
    _wordwrap = True

    def __init__(self, *args):
        """Constructs an empty TextArea.
        ---
        Constructs an empty TextArea with given caption.

        @param caption
                   the caption for the field.
        ---
        Constructs a TextArea with given property data source.

        @param dataSource
                   the data source for the field
        ---
        Constructs a TextArea with given caption and property data source.

        @param caption
                   the caption for the field
        @param dataSource
                   the data source for the field
        ---
        Constructs a TextArea with given caption and value.

        @param caption
                   the caption for the field
        @param value
                   the value for the field
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.setValue('')
        elif _1 == 1:
            if isinstance(_0[0], Property):
                dataSource, = _0
                self.__init__()
                self.setPropertyDataSource(dataSource)
            else:
                caption, = _0
                self.__init__()
                self.setCaption(caption)
        elif _1 == 2:
            if isinstance(_0[1], Property):
                caption, dataSource = _0
                self.__init__(dataSource)
                self.setCaption(caption)
            else:
                caption, value = _0
                self.__init__(caption)
                self.setValue(value)
        else:
            raise ARGERROR(0, 2)

    def setRows(self, rows):
        """Sets the number of rows in the text area.

        @param rows
                   the number of rows for this text area.
        """
        if rows < 0:
            rows = 0
        if self._rows != rows:
            self._rows = rows
            self.requestRepaint()

    def getRows(self):
        """Gets the number of rows in the text area.

        @return number of explicitly set rows.
        """
        return self._rows

    def setWordwrap(self, wordwrap):
        """Sets the text area's word-wrap mode on or off.

        @param wordwrap
                   the boolean value specifying if the text area should be in
                   word-wrap mode.
        """
        if self._wordwrap != wordwrap:
            self._wordwrap = wordwrap
            self.requestRepaint()

    def isWordwrap(self):
        """Tests if the text area is in word-wrap mode.

        @return <code>true</code> if the component is in word-wrap mode,
                <code>false</code> if not.
        """
        return self._wordwrap

    def paintContent(self, target):
        super(TextArea, self).paintContent(target)
        target.addAttribute('rows', self.getRows())
        if not self.isWordwrap():
            # Wordwrap is only painted if turned off to minimize communications
            target.addAttribute('wordwrap', False)
