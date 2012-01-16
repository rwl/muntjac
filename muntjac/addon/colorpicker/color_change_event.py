# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.ui.component import Event


class ColorChangeEvent(Event):

    def __init__(self, source, color):
        Event.__init__(self, source)

        self._color = color

    def getColor(self):
        return self._color
