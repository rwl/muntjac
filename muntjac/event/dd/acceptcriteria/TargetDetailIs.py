# Copyright (C) 2011 Vaadin Ltd
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __pyjamas__ import (ARGERROR,)
from com.vaadin.event.dd.acceptcriteria.ClientSideCriterion import (ClientSideCriterion,)


class TargetDetailIs(ClientSideCriterion):
    """Criterion for checking if drop target details contains the specific property
    with the specific value. Currently only String values are supported.

    @since 6.3

           TODO add support for other basic data types that we support in UIDL.
    """
    _serialVersionUID = 763165450054331246L
    _propertyName = None
    _value = None

    def __init__(self, *args):
        """Constructs a criterion which ensures that the value there is a value in
        {@link TargetDetails} that equals the reference value.

        @param dataFlavor
                   the type of data to be checked
        @param value
                   the reference value to which the drop target detail will be
                   compared
        """
        _0 = args
        _1 = len(args)
        if _1 == 2:
            if isinstance(_0[1], bool):
                dataFlavor, true1 = _0
                self._propertyName = dataFlavor
                self._value = true1
            else:
                dataFlavor, value = _0
                self._propertyName = dataFlavor
                self._value = value
        else:
            raise ARGERROR(2, 2)

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
        return TargetDetailIs.getCanonicalName()
