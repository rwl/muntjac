# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

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
