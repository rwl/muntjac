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

"""Defines a component with two lists: left side for available items
and right side for selected items."""

from muntjac.ui.abstract_select import AbstractSelect

from muntjac.terminal.gwt.client.ui.v_twin_col_select import VTwinColSelect


class TwinColSelect(AbstractSelect):
    """Multiselect component with two lists: left side for available items
    and right side for selected items.
    """

    CLIENT_WIDGET = None #ClientWidget(VTwinColSelect, LoadStyle.EAGER)

    def __init__(self, *args):
        """
        @param args: tuple of the form
            - ()
            - (caption)
            - (caption, dataSource)
            - (caption, options)
        """
        self._columns = 0
        self._rows = 0
        self._leftColumnCaption = None
        self._rightColumnCaption = None

        super(TwinColSelect, self).__init__(*args)


    def setColumns(self, columns):
        """Sets the number of columns in the editor. If the number of columns
        is set 0, the actual number of displayed columns is determined
        implicitly by the adapter.

        The number of columns overrides the value set by setWidth. Only if
        columns are set to 0 (default) the width set using
        L{setWidth} or L{setWidth} is used.

        @param columns: the number of columns to set.
        """
        if columns < 0:
            columns = 0
        if self._columns != columns:
            self._columns = columns
            self.requestRepaint()


    def getColumns(self):
        return self._columns


    def getRows(self):
        return self._rows


    def setRows(self, rows):
        """Sets the number of rows in the editor. If the number of rows is set
        to 0, the actual number of displayed rows is determined implicitly by
        the adapter.

        If a height if set (using L{setHeight} or L{setHeight}) it overrides
        the number of rows. Leave the height undefined to use this method. This
        is the opposite of how L{setColumns} work.

        @param rows: the number of rows to set.
        """
        if rows < 0:
            rows = 0
        if self._rows != rows:
            self._rows = rows
            self.requestRepaint()


    def paintContent(self, target):
        target.addAttribute('type', 'twincol')

        # Adds the number of columns
        if self._columns != 0:
            target.addAttribute('cols', self._columns)

        # Adds the number of rows
        if self._rows != 0:
            target.addAttribute('rows', self._rows)

        # Right and left column captions and/or icons (if set)
        lc = self.getLeftColumnCaption()
        rc = self.getRightColumnCaption()
        if lc is not None:
            target.addAttribute(VTwinColSelect.ATTRIBUTE_LEFT_CAPTION, lc)

        if rc is not None:
            target.addAttribute(VTwinColSelect.ATTRIBUTE_RIGHT_CAPTION, rc)

        super(TwinColSelect, self).paintContent(target)


    def setRightColumnCaption(self, rightColumnCaption):
        """Sets the text shown above the right column.

        @param rightColumnCaption: The text to show
        """
        self._rightColumnCaption = rightColumnCaption
        self.requestRepaint()


    def getRightColumnCaption(self):
        """Returns the text shown above the right column.

        @return: The text shown or null if not set.
        """
        return self._rightColumnCaption


    def setLeftColumnCaption(self, leftColumnCaption):
        """Sets the text shown above the left column.

        @param leftColumnCaption: The text to show
        """
        self._leftColumnCaption = leftColumnCaption
        self.requestRepaint()


    def getLeftColumnCaption(self):
        """Returns the text shown above the left column.

        @return: The text shown or null if not set.
        """
        return self._leftColumnCaption
