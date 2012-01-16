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

"""Interface for rendering error messages to terminal."""

from muntjac.terminal.paintable import IPaintable


class IErrorMessage(IPaintable):
    """Interface for rendering error messages to terminal. All the
    visible errors shown to user must implement this interface.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
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
