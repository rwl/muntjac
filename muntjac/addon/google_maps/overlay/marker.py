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


class IMarker(object):
    """@author: Henri Muurimaa
    @author: Richard Lincoln"""

    def getId(self):
        raise NotImplementedError

    def isVisible(self):
        raise NotImplementedError

    def getLatLng(self):
        raise NotImplementedError

    def getIconUrl(self):
        raise NotImplementedError

    def getIconAnchor(self):
        raise NotImplementedError

    def getTitle(self):
        raise NotImplementedError

    def getInfoWindowContent(self):
        raise NotImplementedError

    def isDraggable(self):
        raise NotImplementedError
