# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.ui.Action import (Action,)


class TreeAction(Action):
    """This class is used for "row actions" in VTree and ITable"""
    _targetKey = ''
    _actionKey = ''

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            owner, = _0
            super(TreeAction, self)(owner)
        elif _1 == 3:
            owner, target, action = _0
            self.__init__(owner)
            self._targetKey = target
            self._actionKey = action
        else:
            raise ARGERROR(1, 3)

    def execute(self):
        """Sends message to server that this action has been fired. Messages are
        "standard" Vaadin messages whose value is comma separated pair of
        targetKey (row, treeNod ...) and actions id.

        Variablename is always "action".

        Actions are always sent immediatedly to server.
        """
        self.owner.getClient().updateVariable(self.owner.getPaintableId(), 'action', self._targetKey + ',' + self._actionKey, True)
        self.owner.getClient().getContextMenu().hide()

    def getActionKey(self):
        return self._actionKey

    def setActionKey(self, actionKey):
        self._actionKey = actionKey

    def getTargetKey(self):
        return self._targetKey

    def setTargetKey(self, targetKey):
        self._targetKey = targetKey
