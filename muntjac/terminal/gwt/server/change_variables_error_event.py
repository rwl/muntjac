# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

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
