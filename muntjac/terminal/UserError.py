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


class UserError(ErrorMessage):
    """<code>UserError</code> is a controlled error occurred in application. User
    errors are occur in normal usage of the application and guide the user.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # Content mode, where the error contains only plain text.
    CONTENT_TEXT = 0
    # Content mode, where the error contains preformatted text.
    CONTENT_PREFORMATTED = 1
    # Formatted content mode, where the contents is XML restricted to the UIDL
    # 1.0 formatting markups.

    CONTENT_UIDL = 2
    # Content mode.
    _mode = CONTENT_TEXT
    # Message in content mode.
    _msg = None
    # Error level.
    _level = ErrorMessage.ERROR

    def __init__(self, *args):
        """Creates a textual error message of level ERROR.

        @param textErrorMessage
                   the text of the error message.
        ---
        Creates a error message with level and content mode.

        @param message
                   the error message.
        @param contentMode
                   the content Mode.
        @param errorLevel
                   the level of error.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            textErrorMessage, = _0
            self._msg = textErrorMessage
        elif _1 == 3:
            message, contentMode, errorLevel = _0
            if (contentMode < 0) or (contentMode > 2):
                raise java.lang.IllegalArgumentException('Unsupported content mode: ' + contentMode)
            self._msg = message
            self._mode = contentMode
            self._level = errorLevel
        else:
            raise ARGERROR(1, 3)

    # Check the parameters
    # Documenten in interface

    def getErrorLevel(self):
        # Documenten in interface
        return self._level

    def addListener(self, listener):
        # Documenten in interface
        pass

    def removeListener(self, listener):
        # Documenten in interface
        pass

    def requestRepaint(self):
        # Documenten in interface
        pass

    def paint(self, target):
        # Documenten in interface
        target.startTag('error')
        # Error level
        if self._level >= ErrorMessage.SYSTEMERROR:
            target.addAttribute('level', 'system')
        elif self._level >= ErrorMessage.CRITICAL:
            target.addAttribute('level', 'critical')
        elif self._level >= ErrorMessage.ERROR:
            target.addAttribute('level', 'error')
        elif self._level >= ErrorMessage.WARNING:
            target.addAttribute('level', 'warning')
        else:
            target.addAttribute('level', 'info')
        # Paint the message
        _0 = self._mode
        _1 = False
        while True:
            if _0 == self.CONTENT_TEXT:
                _1 = True
                target.addText(self._msg)
                break
            if (_1 is True) or (_0 == self.CONTENT_UIDL):
                _1 = True
                target.addUIDL(self._msg)
                break
            if (_1 is True) or (_0 == self.CONTENT_PREFORMATTED):
                _1 = True
                target.startTag('pre')
                target.addText(self._msg)
                target.endTag('pre')
            break
        target.endTag('error')

    def requestRepaintRequests(self):
        # Documented in superclass
        pass

    def toString(self):
        return self._msg

    def getDebugId(self):
        return None

    def setDebugId(self, id):
        raise self.UnsupportedOperationException('Setting testing id for this Paintable is not implemented')
