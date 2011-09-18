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
from com.vaadin.terminal.ErrorMessage import (ErrorMessage,)
# from java.io.PrintWriter import (PrintWriter,)
# from java.io.StringWriter import (StringWriter,)


class SystemError(RuntimeError, ErrorMessage):
    """<code>SystemError</code> is a runtime exception caused by error in system.
    The system error can be shown to the user as it implements
    <code>ErrorMessage</code> interface, but contains technical information such
    as stack trace and exception.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # The cause of the system error. The cause is stored separately as JDK 1.3
    # does not support causes natively.

    _cause = None

    def __init__(self, *args):
        """Constructor for SystemError with error message specified.

        @param message
                   the Textual error description.
        ---
        Constructor for SystemError with causing exception and error message.

        @param message
                   the Textual error description.
        @param cause
                   the throwable causing the system error.
        ---
        Constructor for SystemError with cause.

        @param cause
                   the throwable causing the system error.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Throwable):
                cause, = _0
                self._cause = cause
            else:
                message, = _0
                super(SystemError, self)(message)
        elif _1 == 2:
            message, cause = _0
            super(SystemError, self)(message)
            self._cause = cause
        else:
            raise ARGERROR(1, 2)

    def getErrorLevel(self):
        """@see com.vaadin.terminal.ErrorMessage#getErrorLevel()"""
        return ErrorMessage.SYSTEMERROR

    def paint(self, target):
        """@see com.vaadin.terminal.Paintable#paint(com.vaadin.terminal.PaintTarget)"""
        target.startTag('error')
        target.addAttribute('level', 'system')
        sb = self.StringBuilder()
        message = self.getLocalizedMessage()
        if message is not None:
            sb.append('<h2>')
            sb.append(message)
            sb.append('</h2>')
        # Paint the exception
        if self._cause is not None:
            sb.append('<h3>Exception</h3>')
            buffer = StringWriter()
            self._cause.printStackTrace(PrintWriter(buffer))
            sb.append('<pre>')
            sb.append(str(buffer))
            sb.append('</pre>')
        target.addXMLSection('div', str(sb), 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd')
        target.endTag('error')

    def getCause(self):
        """Gets cause for the error.

        @return the cause.
        @see java.lang.Throwable#getCause()
        """
        # Documented in super interface
        return self._cause

    def addListener(self, listener):
        # Documented in super interface
        pass

    def removeListener(self, listener):
        # Documented in super interface
        pass

    def requestRepaint(self):
        # Documented in super interface
        pass

    def requestRepaintRequests(self):
        pass

    def getDebugId(self):
        return None

    def setDebugId(self, id):
        raise self.UnsupportedOperationException('Setting testing id for this Paintable is not implemented')
