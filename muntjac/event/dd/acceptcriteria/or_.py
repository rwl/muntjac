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

"""A compound criterion that accepts the drag if any of its criterion
accepts it."""

from muntjac.event.dd.acceptcriteria.client_side_criterion import \
    ClientSideCriterion


class Or(ClientSideCriterion):
    """A compound criterion that accepts the drag if any of its criterion
    accepts it.

    @see: And
    """

    def __init__(self, *criteria):
        """@param criteria:
                   the criteria of which the Or criteria will be composed
        """
        self._criteria = criteria


    def paintContent(self, target):
        super(Or, self).paintContent(target)
        for crit in self._criteria:
            crit.paint(target)


    def accept(self, dragEvent):
        for crit in self._criteria:
            if crit.accept(dragEvent):
                return True
        return False


    def getIdentifier(self):
        return 'com.vaadin.event.dd.acceptcriteria.Or'
