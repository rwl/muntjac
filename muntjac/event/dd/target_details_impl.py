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

"""Implementation of ITargetDetails for terminal implementation and
extension."""

from muntjac.event.dd.target_details import ITargetDetails


class TargetDetailsImpl(ITargetDetails):
    """A HashMap backed implementation of L{ITargetDetails} for terminal
    implementation and for extension.
    """

    def __init__(self, rawDropData, dropTarget=None):
        self._data = dict()

        self._data.update(rawDropData)
        self._dropTarget = dropTarget


    def getData(self, key):
        return self._data.get(key)


    def setData(self, key, value):
        if key in self._data:
            return self._data[key]
        else:
            self._data[key] = value
            return None


    def getTarget(self):
        return self._dropTarget
