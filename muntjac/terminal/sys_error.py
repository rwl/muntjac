# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

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
    @version: 1.1.0
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
