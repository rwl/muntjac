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

"""A criterion that ensures the drag source is the same as drop target."""

from muntjac.event.transferable_impl import TransferableImpl

from muntjac.event.dd.acceptcriteria.client_side_criterion import \
    ClientSideCriterion


class SourceIsTarget(ClientSideCriterion):
    """A criterion that ensures the drag source is the same as drop target.
    Eg. L{Tree} or L{Table} could support only re-ordering of items,
    but no L{Transferable}s coming outside.

    Note! Class is singleton, use L{get} method to get the instance.
    """

    _instance = None

    def __init__(self):
        pass


    def accept(self, dragEvent):
        if isinstance(dragEvent.getTransferable(), TransferableImpl):
            sourceComponent = dragEvent.getTransferable().getSourceComponent()
            target = dragEvent.getTargetDetails().getTarget()
            return sourceComponent == target
        return False


    @classmethod
    def get(cls):
        return cls._instance


    def getIdentifier(self):
        return 'com.vaadin.event.dd.acceptcriteria.SourceIsTarget'


SourceIsTarget._instance = SourceIsTarget()
