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

from muntjac.event.transferable import ITransferable


class TransferableImpl(ITransferable):

    def __init__(self, sourceComponent, rawVariables):
        self._sourceComponent = sourceComponent
        self._rawVariables = rawVariables


    def getSourceComponent(self):
        return self._sourceComponent


    def getData(self, dataFlavor):
        return self._rawVariables.get(dataFlavor)


    def setData(self, dataFlavor, value):
        self._rawVariables[dataFlavor] = value


    def getDataFlavors(self):
        return self._rawVariables.keys()
