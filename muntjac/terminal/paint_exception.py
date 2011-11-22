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


class PaintException(IOError):
    """C{PaintExcepection} is thrown if painting of a
    component fails.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.1
    """

    def __init__(self, arg):
        """Constructs an instance of C{PaintExeception} with the specified
        detail message or an instance of C{PaintExeception} from IOException.

        @param arg:
                   the detail message or the original exception
        """
        super(PaintException, self).__init__( str(arg) )
