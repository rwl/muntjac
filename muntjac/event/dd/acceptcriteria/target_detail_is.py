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

"""Criterion for checking if drop target details contains the specific
property with the specific value."""

from muntjac.event.dd.acceptcriteria.client_side_criterion import \
    ClientSideCriterion


class TargetDetailIs(ClientSideCriterion):
    """Criterion for checking if drop target details contains the specific
    property with the specific value. Currently only String values are
    supported.

    TODO: add support for other basic data types that we support in UIDL.
    """

    def __init__(self, dataFlavor, value):
        """Constructs a criterion which ensures that the value there is a
        value in L{TargetDetails} that equals the reference value.

        @param dataFlavor:
                   the type of data to be checked
        @param value:
                   the reference value to which the drop target detail will
                   be compared
        """
        self._propertyName = dataFlavor
        self._value = value


    def paintContent(self, target):
        super(TargetDetailIs, self).paintContent(target)
        target.addAttribute('p', self._propertyName)

        if isinstance(self._value, bool):
            target.addAttribute('v', self._value.booleanValue())
            target.addAttribute('t', 'b')
        elif isinstance(self._value, str):
            target.addAttribute('v', self._value)


    def accept(self, dragEvent):
        data = dragEvent.getTargetDetails().getData(self._propertyName)
        return self._value == data


    def getIdentifier(self):
        # sub classes by default use VDropDetailEquals a client implementation
        return 'com.vaadin.event.dd.acceptcriteria.TargetDetailIs'
