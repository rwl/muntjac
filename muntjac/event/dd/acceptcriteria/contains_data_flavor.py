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

"""A criterion that checks whether Transferable contains given data
flavor."""

from muntjac.event.dd.acceptcriteria.client_side_criterion import \
    ClientSideCriterion


class ContainsDataFlavor(ClientSideCriterion):
    """A Criterion that checks whether L{Transferable} contains given data
    flavor. The developer might for example accept the incoming data only
    if it contains "Url" or "Text".
    """

    def __init__(self, dataFlavor):
        """Constructs a new instance of L{ContainsDataFlavor}.

        @param dataFlavor:
                   the type of data that will be checked from
                   L{Transferable}
        """
        self._dataFlavorId = dataFlavor


    def paintContent(self, target):
        super(ContainsDataFlavor, self).paintContent(target)
        target.addAttribute('p', self._dataFlavorId)


    def accept(self, dragEvent):
        return (self._dataFlavorId
                in dragEvent.getTransferable().getDataFlavors())


    def getIdentifier(self):
        # extending classes use client side implementation from this class
        return 'com.vaadin.event.dd.acceptcriteria.ContainsDataFlavor'
