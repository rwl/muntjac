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

import sys
import traceback

try:
    from cStringIO import StringIO
except ImportError, e:
    from StringIO import StringIO

from muntjac.terminal.error_message import IErrorMessage


class SysError(RuntimeError, IErrorMessage):
    """C{SystemError} is a runtime exception caused by error in
    system. The system error can be shown to the user as it implements
    C{IErrorMessage} interface, but contains technical information
    such as stack trace and exception.

    SystemError does not support HTML in error messages or stack traces.
    If HTML messages are required, use {@link UserError} or a custom
    implementation of L{ErrorMessage}.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.3
    """

    def __init__(self, *args):
        """Constructor for SystemError with error message and/or causing
        exception specified.

        @param args: tuple of the form
            - ()
            - (message)
              1. the textual error description.
            - (message, cause)
              1. the textual error description.
              2. the throwable causing the system error.
            - (cause)
              1. the throwable causing the system error.
        """
        # The cause of the system error.
        self._cause = None

        nargs = len(args)
        if nargs == 0:
            super(SysError, self).__init__()
        elif nargs == 1:
            if isinstance(args[0], Exception):
                self._cause = args[0]
                super(SysError, self).__init__()
            else:
                super(SysError, self).__init__(args[0])
        elif nargs == 2:
            message, cause = args
            super(SysError, self).__init__(message)
            self._cause = cause
        else:
            raise ValueError, ('too many arguments: %d' % nargs)


    def getErrorLevel(self):
        """@see: L{IErrorMessage.getErrorLevel}"""
        return IErrorMessage.SYSTEMERROR


    def paint(self, target):
        """@see: L{IPaintable.paint}"""

        target.startTag('error')
        target.addAttribute('level', 'system')

        message = self.getHtmlMessage()

        target.addXMLSection('div', message,
                'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd')

        target.endTag('error')


    def getHtmlMessage(self):

        from muntjac.terminal.gwt.server.abstract_application_servlet \
            import AbstractApplicationServlet

        sb = StringIO()
        message = self.message
        if message is not None:
            sb.write('<h2>')
            sb.write(AbstractApplicationServlet.safeEscapeForHtml(message))
            sb.write('</h2>')

        # Paint the exception
        if self._cause is not None:
            sb.write('<h3>Exception</h3>')
            buff = StringIO()
            exc_type, _, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, self._cause,
                    exc_traceback, file=buff)

            sb.write('<pre>')
            pre = buff.getvalue()
            sb.write(AbstractApplicationServlet.safeEscapeForHtml(pre))
            buff.close()
            sb.write('</pre>')

        result = sb.getvalue()
        sb.close()
        return result


    def getCause(self):
        """Gets cause for the error.

        @return: the cause.
        """
        return self._cause


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


    def getDebugId(self):
        return None


    def setDebugId(self, idd):
        raise NotImplementedError, \
                'Setting testing id for this Paintable is not implemented'
