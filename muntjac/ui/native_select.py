# Copyright (C) 2011 Vaadin Ltd.
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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

"""Defines a simple drop-down select."""

from muntjac.ui.abstract_select import AbstractSelect
from muntjac.data.container import IContainer


class NativeSelect(AbstractSelect):
    """This is a simple drop-down select without, for instance, support
    for multiselect, new items, lazyloading, and other advanced features.
    Sometimes "native" select without all the bells-and-whistles of the
    ComboBox is a better choice.
    """

    CLIENT_WIDGET = None #ClientWidget(VNativeWidget)

    def __init__(self, *args):
        # width in characters, mimics TextField
        self._columns = 0

        args = args
        nargs = len(args)
        if nargs == 0:
            super(NativeSelect, self).__init__()
        elif nargs == 1:
            caption, = args
            super(NativeSelect, self).__init__(caption)
        elif nargs == 2:
            if isinstance(args[1], IContainer):
                caption, dataSource = args
                super(NativeSelect, self).__init__(caption, dataSource)
            else:
                caption, options = args
                super(NativeSelect, self).__init__(caption, options)
        else:
            raise ValueError, 'too many arguments'


    def setColumns(self, columns):
        """Sets the number of columns in the editor. If the number of columns
        is set 0, the actual number of displayed columns is determined
        implicitly by the adapter.

        @param columns:
                   the number of columns to set.
        """
        if columns < 0:
            columns = 0

        if self._columns != columns:
            self._columns = columns
            self.requestRepaint()


    def getColumns(self):
        return self._columns


    def paintContent(self, target):
        target.addAttribute('type', 'native')
        # Adds the number of columns
        if self._columns != 0:
            target.addAttribute('cols', self._columns)

        super(NativeSelect, self).paintContent(target)


    def setMultiSelect(self, multiSelect):
        if multiSelect == True:
            raise NotImplementedError, 'Multiselect not supported'


    def setNewItemsAllowed(self, allowNewOptions):
        if allowNewOptions == True:
            raise NotImplementedError, 'newItemsAllowed not supported'
