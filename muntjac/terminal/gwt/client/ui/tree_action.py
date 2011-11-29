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

from muntjac.terminal.gwt.client.ui.action import Action


class TreeAction(Action):
    """This class is used for "row actions" in VTree and ITable"""


    def __init__(self, owner, target='', action=''):
        super(TreeAction, self)(owner)

        self._targetKey = target
        self._actionKey = action


    def execute(self):
        """Sends message to server that this action has been fired. Messages
        are "standard" Muntjac messages whose value is comma separated pair of
        targetKey (row, treeNod ...) and actions id.

        Variablename is always "action".

        Actions are always sent immediatedly to server.
        """
        self.owner.getClient().updateVariable(self.owner.getPaintableId(),
                'action', self._targetKey + ',' + self._actionKey, True)
        self.owner.getClient().getContextMenu().hide()


    def getActionKey(self):
        return self._actionKey


    def setActionKey(self, actionKey):
        self._actionKey = actionKey


    def getTargetKey(self):
        return self._targetKey


    def setTargetKey(self, targetKey):
        self._targetKey = targetKey
