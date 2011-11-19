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

#from muntjac.ui.abstract_component import IComponentErrorEvent


class ChangeVariablesErrorEvent(object):#IComponentErrorEvent):

    def __init__(self, component, throwable, variableChanges):
        self._component = component
        self._throwable = throwable
        self._variableChanges = variableChanges


    def getThrowable(self):
        return self._throwable


    def getComponent(self):
        return self._component


    def getVariableChanges(self):
        return self._variableChanges
