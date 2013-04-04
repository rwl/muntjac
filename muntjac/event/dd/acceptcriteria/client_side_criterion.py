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

"""Parent class for criteria that can be completely validated on client
side."""

from muntjac.event.dd.acceptcriteria.accept_criterion import IAcceptCriterion
from muntjac.util import clsname


class ClientSideCriterion(IAcceptCriterion):
    """Parent class for criteria that can be completely validated on client
    side. All classes that provide criteria that can be completely validated
    on client side should extend this class.

    It is recommended that subclasses of ClientSideCriterion re-validate the
    condition on the server side in L{IAcceptCriterion.accept} after
    the client side validation has accepted a transfer.
    """

    def isClientSideVerifiable(self):
        return True


    def paint(self, target):
        target.startTag('-ac')
        target.addAttribute('name', self.getIdentifier())
        self.paintContent(target)
        target.endTag('-ac')


    def paintContent(self, target):
        pass


    def getIdentifier(self):
        return clsname(self.__class__)  # FIXME: Python client-side


    def paintResponse(self, target):
        # NOP, nothing to do as this is client side verified criterion
        pass
