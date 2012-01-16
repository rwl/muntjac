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

from muntjac.terminal.terminal import IErrorEvent as ITerminalErrorEvent


class IUriHandler(object):
    """A IUriHandler is used for handling URIs requested by the user and can
    optionally provide a L{DownloadStream}. If a L{DownloadStream}
    is returned by L{handleURI}, the stream is sent to the client.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def handleURI(self, context, relativeUri):
        """Handles a given URI. If the URI handler to emit a downloadable
        stream it should return a C{DownloadStream} object.

        @param context:
                   the base URL
        @param relativeUri:
                   a URI relative to C{context}
        @return: A downloadable stream or null if no stream is provided
        """
        pass


class IErrorEvent(ITerminalErrorEvent):
    """An C{IErrorEvent} implementation for IUriHandler."""

    def getURIHandler(self):
        """Gets the IUriHandler that caused this error.

        @return: the IUriHandler that caused the error
        """
        pass
