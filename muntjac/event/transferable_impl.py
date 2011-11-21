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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

from muntjac.event.transferable import ITransferable


class TransferableImpl(ITransferable):

    def __init__(self, sourceComponent, rawVariables):
        self._sourceComponent = sourceComponent
        self._rawVariables = rawVariables


    def getSourceComponent(self):
        return self._sourceComponent


    def getData(self, dataFlavor):
        return self._rawVariables.get(dataFlavor)


    def setData(self, dataFlavor, value):
        self._rawVariables[dataFlavor] = value


    def getDataFlavors(self):
        return self._rawVariables.keys()
