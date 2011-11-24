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

"""For combining multiple error messages together."""

import sys

from muntjac.terminal.error_message import IErrorMessage
from muntjac.terminal.paintable import IRepaintRequestListener


class CompositeErrorMessage(IErrorMessage):
    """Class for combining multiple error messages together.

    @author: Vaadin Ltd.
    @version: 1.0.3
    """

    def __init__(self, errorMessages):
        """Constructor for CompositeErrorMessage.

        @param errorMessages:
                   the Collection of error messages that are listed
                   together. At least one message is required.
        """
        # Array of all the errors.
        self._errors = None

        # Level of the error.
        self._level = None

        self._errors = list()
        self._level = -sys.maxint - 1
        for m in errorMessages:
            self.addErrorMessage(m)

        if len(self._errors) == 0:
            raise ValueError, \
                    'Composite error message must have at least one error'


    def getErrorLevel(self):
        """The error level is the largest error level in.

        @see: L{muntjac.terminal.IErrorMessage.getErrorLevel}
        """
        return self._level


    def addErrorMessage(self, error):
        """Adds a error message into this composite message. Updates the level
        field.

        @param error:
                   the error message to be added. Duplicate errors are ignored.
        """
        if error is not None and error not in self._errors:
            self._errors.append(error)
            l = error.getErrorLevel()
            if l > self._level:
                self._level = l


    def iterator(self):
        """Gets Error Iterator.

        @return: the error iterator.
        """
        return iter(self._errors)


    def paint(self, target):
        """@see: L{IPaintable.paint}"""
        if len(self._errors) == 1:
            self._errors[0].paint(target)
        else:
            target.startTag('error')

            if self._level > 0 and self._level <= IErrorMessage.INFORMATION:
                target.addAttribute('level', 'info')

            elif self._level <= IErrorMessage.WARNING:
                target.addAttribute('level', 'warning')

            elif self._level <= IErrorMessage.ERROR:
                target.addAttribute('level', 'error')

            elif self._level <= IErrorMessage.CRITICAL:
                target.addAttribute('level', 'critical')

            else:
                target.addAttribute('level', 'system')

            # Paint all the exceptions
            for error in self._errors:
                error.paint(target)

            target.endTag('error')


    def addListener(self, listener, iface=None):
        pass


    def addCallback(self, callback, eventType=None, *args):
        pass


    def removeListener(self, listener, iface=None):
        pass


    def removeCallback(self, callback, eventType=None):
        pass


    def requestRepaint(self):
        pass


    def requestRepaintRequests(self):
        pass


    def __str__(self):
        """Returns a comma separated list of the error messages.

        @return: comma separated list of error messages.
        """
        retval = '['
        pos = 0
        for error in self._errors:
            if pos > 0:
                retval += ','
            pos += 1
            retval += str(error)
        retval += ']'
        return retval


    def getDebugId(self):
        return None


    def setDebugId(self, idd):
        raise NotImplementedError, \
                'Setting testing id for this Paintable is not implemented'
