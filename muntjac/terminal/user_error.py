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

from muntjac.terminal.error_message import IErrorMessage
from muntjac.terminal.gwt.server.abstract_application_servlet import AbstractApplicationServlet


class UserError(IErrorMessage):
    """C{UserError} is a controlled error occurred in application. User
    errors are occur in normal usage of the application and guide the user.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    #: Content mode, where the error contains only plain text.
    CONTENT_TEXT = 0

    #: Content mode, where the error contains preformatted text.
    CONTENT_PREFORMATTED = 1

    #: Formatted content mode, where the contents is XML restricted
    #  to the UIDL 1.0 formatting markups.
    CONTENT_UIDL = 2

    #: Content mode, where the error contains XHTML.
    CONTENT_XHTML = 3

    def __init__(self, message, contentMode=None, errorLevel=None):
        """Creates a error message with level and content mode.

        @param message:
                   the error message.
        @param contentMode:
                   the content Mode.
        @param errorLevel:
                   the level of error (defaults to Error).
        """
        # Content mode.
        self._mode = self.CONTENT_TEXT

        # Message in content mode.
        self._msg = message

        # Error level.
        self._level = IErrorMessage.ERROR

        if contentMode is not None:
            # Check the parameters
            if contentMode < 0 or contentMode > 2:
                raise ValueError, 'Unsupported content mode: ' + contentMode
            self._mode = contentMode
            self._level = errorLevel


    def getErrorLevel(self):
        return self._level


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


    def paint(self, target):

        target.startTag('error')

        # Error level
        if self._level >= IErrorMessage.SYSTEMERROR:
            target.addAttribute('level', 'system')

        elif self._level >= IErrorMessage.CRITICAL:
            target.addAttribute('level', 'critical')

        elif self._level >= IErrorMessage.ERROR:
            target.addAttribute('level', 'error')

        elif self._level >= IErrorMessage.WARNING:
            target.addAttribute('level', 'warning')

        else:
            target.addAttribute('level', 'info')

        # Paint the message
        if self._mode == self.CONTENT_TEXT:
            escaped = AbstractApplicationServlet.safeEscapeForHtml(self._msg)
            target.addText(escaped)

        elif self._mode == self.CONTENT_UIDL:
            target.addUIDL("<pre>"
                    + AbstractApplicationServlet.safeEscapeForHtml(self._msg)
                    + "</pre>")

        elif self._mode == self.CONTENT_PREFORMATTED:
            target.startTag('pre')
            target.addText(self._msg)
            target.endTag('pre')

        target.endTag('error')


    def requestRepaintRequests(self):
        pass


    def __str__(self):
        return self._msg


    def getDebugId(self):
        return None


    def setDebugId(self, idd):
        raise NotImplementedError, \
                'Setting testing id for this Paintable is not implemented'
