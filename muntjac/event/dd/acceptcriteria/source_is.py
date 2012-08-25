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

"""Client side criteria that checks if the drag source is one of the given
components."""

from muntjac.event.transferable_impl import TransferableImpl

from muntjac.event.dd.acceptcriteria.client_side_criterion import \
    ClientSideCriterion


class SourceIs(ClientSideCriterion):
    """Client side criteria that checks if the drag source is one of the given
    components.
    """

    def __init__(self, *component):
        self._component = component


    def paintContent(self, target):
        super(SourceIs, self).paintContent(target)
        target.addAttribute('c', len(self._component))
        for i, c in enumerate(self._component):
            target.addAttribute('component' + i, c)


    def accept(self, dragEvent):
        if isinstance(dragEvent.getTransferable(), TransferableImpl):
            sourceComponent = dragEvent.getTransferable().getSourceComponent()
            for c in self._component:
                if c == sourceComponent:
                    return True
        return False


    def getIdentifier(self):
        return 'com.vaadin.event.dd.acceptcriteria.SourceIs'
