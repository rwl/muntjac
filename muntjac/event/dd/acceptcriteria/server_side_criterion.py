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

"""Parent class for criteria which are verified on the server side."""

from muntjac.event.dd.acceptcriteria.accept_criterion import IAcceptCriterion


class ServerSideCriterion(IAcceptCriterion):
    """Parent class for criteria which are verified on the server side
    during a drag operation to accept/discard dragged content (presented
    by L{Transferable}).

    Subclasses should implement the L{IAcceptCriterion.accept} method.

    As all server side state can be used to make a decision, this is more
    flexible than L{ClientSideCriterion}. However, this does require
    additional requests from the browser to the server during a drag operation.

    @see: IAcceptCriterion
    @see: ClientSideCriterion
    """

    def isClientSideVerifiable(self):
        return False


    def paint(self, target):
        target.startTag('-ac')
        target.addAttribute('name', self.getIdentifier())
        self.paintContent(target)
        target.endTag('-ac')


    def paintContent(self, target):
        pass


    def paintResponse(self, target):
        pass


    def getIdentifier(self):
        #return clsname(ServerSideCriterion)  # FIXME: Python client side
        return 'com.vaadin.event.dd.acceptcriteria.ServerSideCriterion'
