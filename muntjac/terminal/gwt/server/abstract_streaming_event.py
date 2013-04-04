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

from muntjac.terminal.stream_variable import IStreamingEvent


class AbstractStreamingEvent(IStreamingEvent):
    """Abstract base class for IStreamingEvent implementations."""

    def __init__(self, filename, typ, length, bytesReceived):
        self._filename = filename
        self._type = typ
        self._contentLength = length
        self._bytesReceived = bytesReceived


    def getFileName(self):
        return self._filename


    def getMimeType(self):
        return self._type


    def getContentLength(self):
        return self._contentLength


    def getBytesReceived(self):
        return self._bytesReceived
