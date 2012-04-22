# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Implementation of ITargetDetails for terminal implementation and
extension."""

from muntjac.event.dd.target_details import ITargetDetails


class TargetDetailsImpl(ITargetDetails):
    """A HashMap backed implementation of L{ITargetDetails} for terminal
    implementation and for extension.
    """

    def __init__(self, rawDropData, dropTarget=None):
        self._data = dict()

        self._data.update(rawDropData)
        self._dropTarget = dropTarget


    def getData(self, key):
        return self._data.get(key)


    def setData(self, key, value):
        if key in self._data:
            return self._data[key]
        else:
            self._data[key] = value
            return None


    def getTarget(self):
        return self._dropTarget
