# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@


class InfoWindowTab(object):

    def __init__(self, parent, content, label=None, selected=False):
        self._content = content
        self._content.setParent(parent)
        self._label = label
        self._selected = selected

    def getContent(self):
        return self._content

    def getLabel(self):
        return self._label

    def setLabel(self, label):
        self._label = label

    def isSelected(self):
        return self._selected

    def setSelected(self, selected):
        self._selected = selected
