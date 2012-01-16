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


class Html5File(object):
    """L{DragAndDropWrapper} can receive also files from client computer
    if appropriate HTML 5 features are supported on client side. This class
    wraps information about dragged file on server side.
    """

    def __init__(self, name, size, mimeType):
        self._name = name
        self._size = size
        self._type = mimeType
        self._streamVariable = None


    def getFileName(self):
        return self._name


    def getFileSize(self):
        return self._size


    def getType(self):
        return self._type


    def setStreamVariable(self, streamVariable):
        """Sets the L{StreamVariable} that into which the file contents
        will be written. Usage of StreamVariable is similar to L{Upload}
        component.

        If the L{StreamVariable} is not set in the L{DropHandler}
        the file contents will not be sent to server.

        I{Note!} receiving file contents is experimental feature
        depending on HTML 5 API's. It is supported only by modern web browsers
        like Firefox 3.6 and above and recent webkit based browsers (Safari 5,
        Chrome 6) at this time.

        @param streamVariable:
                   the callback that returns stream where the implementation
                   writes the file contents as it arrives.
        """
        self._streamVariable = streamVariable


    def getStreamVariable(self):
        return self._streamVariable
