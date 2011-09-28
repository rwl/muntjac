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

from muntjac.terminal.IPaintable import IPaintable


class IErrorMessage(IPaintable):
    """Interface for rendering error messages to terminal. All the
    visible errors shown to user must implement this interface.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    # Error code for system errors and bugs.
    SYSTEMERROR = 5000

    # Error code for critical error messages.
    CRITICAL = 4000

    # Error code for regular error messages.
    ERROR = 3000

    # Error code for warning messages.
    WARNING = 2000

    # Error code for informational messages.
    INFORMATION = 1000

    def getErrorLevel(self):
        """Gets the errors level.

        @return the level of error as an integer.
        """
        raise NotImplementedError


    def addListener(self, listener):
        """Error messages are inmodifiable and thus listeners are not needed.
        This method should be implemented as empty.

        @param listener
                   the listener to be added.
        @see com.vaadin.terminal.IPaintable#addListener(listener)
        """
        raise NotImplementedError


    def removeListener(self, listener):
        """Error messages are inmodifiable and thus listeners are not needed.
        This method should be implemented as empty.

        @param listener
                   the listener to be removed.
        @see com.vaadin.terminal.IPaintable#removeListener(listener)
        """
        raise NotImplementedError


    def requestRepaint(self):
        """Error messages are inmodifiable and thus listeners are not needed.
        This method should be implemented as empty.

        @see com.vaadin.terminal.IPaintable#requestRepaint()
        """
        raise NotImplementedError
