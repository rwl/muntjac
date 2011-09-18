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
from com.vaadin.ui.AbstractSelect import (AbstractSelect,)
# from java.util.Collection import (Collection,)


class ListSelect(AbstractSelect):
    """This is a simple list select without, for instance, support for new items,
    lazyloading, and other advanced features.
    """
    _columns = 0
    _rows = 0

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            super(ListSelect, self)()
        elif _1 == 1:
            caption, = _0
            super(ListSelect, self)(caption)
        elif _1 == 2:
            if isinstance(_0[1], Collection):
                caption, options = _0
                super(ListSelect, self)(caption, options)
            else:
                caption, dataSource = _0
                super(ListSelect, self)(caption, dataSource)
        else:
            raise ARGERROR(0, 2)

    def setColumns(self, columns):
        """Sets the number of columns in the editor. If the number of columns is set
        0, the actual number of displayed columns is determined implicitly by the
        adapter.

        @param columns
                   the number of columns to set.
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
        """Sets the number of rows in the editor. If the number of rows is set 0,
        the actual number of displayed rows is determined implicitly by the
        adapter.

        @param rows
                   the number of rows to set.
        """
        if rows < 0:
            rows = 0
        if self._rows != rows:
            self._rows = rows
            self.requestRepaint()

    def paintContent(self, target):
        target.addAttribute('type', 'list')
        # Adds the number of columns
        if self._columns != 0:
            target.addAttribute('cols', self._columns)
        # Adds the number of rows
        if self._rows != 0:
            target.addAttribute('rows', self._rows)
        super(ListSelect, self).paintContent(target)
