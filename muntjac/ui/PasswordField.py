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


class PasswordField(AbstractTextField):
    """A field that is used to enter secret text information like passwords. The
    entered text is not displayed on the screen.
    """

    def __init__(self, *args):
        """Constructs an empty PasswordField.
        ---
        Constructs a PasswordField with given property data source.

        @param dataSource
                   the property data source for the field
        ---
        Constructs a PasswordField with given caption and property data source.

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
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.setValue('')
        elif _1 == 1:
            if isinstance(_0[0], Property):
                dataSource, = _0
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
                self.setValue(value)
                self.setCaption(caption)
        else:
            raise ARGERROR(0, 2)
