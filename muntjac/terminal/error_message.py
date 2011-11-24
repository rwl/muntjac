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

"""Interface for rendering error messages to terminal."""

from muntjac.terminal.paintable import IPaintable


class IErrorMessage(IPaintable):
    """Interface for rendering error messages to terminal. All the
    visible errors shown to user must implement this interface.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.3
    """

    #: Error code for system errors and bugs.
    SYSTEMERROR = 5000

    #: Error code for critical error messages.
    CRITICAL = 4000

    #: Error code for regular error messages.
    ERROR = 3000

    #: Error code for warning messages.
    WARNING = 2000

    #: Error code for informational messages.
    INFORMATION = 1000

    def getErrorLevel(self):
        """Gets the errors level.

        @return: the level of error as an integer.
        """
        raise NotImplementedError


    def addListener(self, listener, iface=None):
        """Error messages are unmodifiable and thus listeners are not needed.
        This method should be implemented as empty.

        @param listener:
                   the listener to be added.
        @see: L{IPaintable.addListener}
        """
        raise NotImplementedError


    def addCallback(self, callback, eventType=None, *args):
        raise NotImplementedError


    def removeListener(self, listener, iface=None):
        """Error messages are inmodifiable and thus listeners are not needed.
        This method should be implemented as empty.

        @param listener:
                   the listener to be removed.
        @see: L{IPaintable.removeListener}
        """
        raise NotImplementedError


    def removeCallback(self, callback, eventType=None):
        raise NotImplementedError


    def requestRepaint(self):
        """Error messages are inmodifiable and thus listeners are not needed.
        This method should be implemented as empty.

        @see: L{IPaintable.requestRepaint}
        """
        raise NotImplementedError
