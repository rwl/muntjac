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

from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterion import (VAcceptCriterion,)


class VTargetDetailIs(VAcceptCriterion):

    def accept(self, drag, configuration):
        name = configuration.getStringAttribute('p')
        t = configuration.getStringAttribute('t').intern() if configuration.hasAttribute('t') else 's'
        value = None
        if t == 's':
            value = configuration.getStringAttribute('v')
        elif t == 'b':
            value = configuration.getBooleanAttribute('v')
        if value is not None:
            object = drag.getDropDetails().get(name)
            if isinstance(object, Enum):
                return object.name() == value
            else:
                return value == object
        else:
            return False
