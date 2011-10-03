# Copyright (C) 2010 IT Mill Ltd.
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

from muntjac.ui.abstract_text_field import AbstractTextField
from muntjac.data.property import IProperty


class PasswordField(AbstractTextField):
    """A field that is used to enter secret text information like passwords.
    The entered text is not displayed on the screen.
    """

    #CLIENT_WIDGET = ClientWidget(VPasswordField, LoadStyle.EAGER)

    def __init__(self, *args):
        """Constructs an empty PasswordField.
        ---
        Constructs a PasswordField with given property data source.

        @param dataSource
                   the property data source for the field
        ---
        Constructs a PasswordField with given caption and property data
        source.

        @param caption
                   the caption for the field
        @param dataSource
                   the property data source for the field
        ---
        Constructs a PasswordField with given value and caption.

        @param caption
                   the caption for the field
        @param value
                   the value for the field
        ---
        Constructs a PasswordField with given caption.

        @param caption
                   the caption for the field
        """
        nargs = len(args)
        if nargs == 0:
            self.setValue('')
        elif nargs == 1:
            if isinstance(args[0], IProperty):
                dataSource, = args
                self.setPropertyDataSource(dataSource)
            else:
                caption, = args
                self.__init__()
                self.setCaption(caption)
        elif nargs == 2:
            if isinstance(args[1], IProperty):
                caption, dataSource = args
                self.__init__(dataSource)
                self.setCaption(caption)
            else:
                caption, value = args
                self.setValue(value)
                self.setCaption(caption)
        else:
            raise ValueError, 'too many arguments'
