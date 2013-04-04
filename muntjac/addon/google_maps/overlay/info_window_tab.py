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


class InfoWindowTab(object):

    def __init__(self, parent, content, label=None, selected=False):
        self._content = content
        self._content.setParent(parent)
        self._label = label
        self._selected = selected

    def getContent(self):
        return self._content

    def getLabel(self):
        return self._label

    def setLabel(self, label):
        self._label = label

    def isSelected(self):
        return self._selected

    def setSelected(self, selected):
        self._selected = selected
