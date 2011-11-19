# Copyright (C) 2011 Vaadin Ltd.
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
