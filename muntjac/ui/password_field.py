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

"""Defines a field that is used to enter secret text information like
passwords."""

from muntjac.ui.abstract_text_field import AbstractTextField
from muntjac.data.property import IProperty


class PasswordField(AbstractTextField):
    """A field that is used to enter secret text information like passwords.
    The entered text is not displayed on the screen.
    """

    CLIENT_WIDGET = None #ClientWidget(VPasswordField, LoadStyle.EAGER)

    def __init__(self, *args):
        """Constructs a PasswordField with caption and/or value/data source.

        @param args: tuple of the form
            - ()
            - (caption)
              1. the caption for the field
            - (dataSource)
              1. the property data source for the field
            - (caption, dataSource)
              1. the caption for the field
              2. the property data source for the field
            - (caption, value)
              1. the caption for the field
              2. the value for the field
        """
        super(PasswordField, self).__init__()

        nargs = len(args)
        if nargs == 0:
            self.setValue('')
        elif nargs == 1:
            if isinstance(args[0], IProperty):
                dataSource, = args
                self.setPropertyDataSource(dataSource)
            else:
                caption, = args
                PasswordField.__init__(self)
                self.setCaption(caption)
        elif nargs == 2:
            if isinstance(args[1], IProperty):
                caption, dataSource = args
                PasswordField.__init__(self, dataSource)
                self.setCaption(caption)
            else:
                caption, value = args
                self.setValue(value)
                self.setCaption(caption)
        else:
            raise ValueError, 'too many arguments'
