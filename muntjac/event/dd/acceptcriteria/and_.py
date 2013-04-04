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

"""A compound criterion that accepts the drag if all of its criteria
accepts the drag."""

from muntjac.event.dd.acceptcriteria.client_side_criterion import \
    ClientSideCriterion


class And(ClientSideCriterion):
    """A compound criterion that accepts the drag if all of its criteria
    accepts the drag.

    @see: L{Or}
    """

    def __init__(self, *criteria):
        """@param criteria:
                   criteria of which the And criterion will be composed
        """
        self.criteria = criteria


    def paintContent(self, target):
        super(And, self).paintContent(target)
        for crit in self.criteria:
            crit.paint(target)


    def accept(self, dragEvent):
        for crit in self.criteria:
            if not crit.accept(dragEvent):
                return False
        return True


    def getIdentifier(self):
        return 'com.vaadin.event.dd.acceptcriteria.And'
