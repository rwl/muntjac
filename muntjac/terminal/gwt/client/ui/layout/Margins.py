# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@


class Margins(object):
    _marginTop = None
    _marginBottom = None
    _marginLeft = None
    _marginRight = None
    _horizontal = 0
    _vertical = 0

    def __init__(self, marginTop, marginBottom, marginLeft, marginRight):
        super(Margins, self)()
        self._marginTop = marginTop
        self._marginBottom = marginBottom
        self._marginLeft = marginLeft
        self._marginRight = marginRight
        self.updateHorizontal()
        self.updateVertical()

    def getMarginTop(self):
        return self._marginTop

    def getMarginBottom(self):
        return self._marginBottom

    def getMarginLeft(self):
        return self._marginLeft

    def getMarginRight(self):
        return self._marginRight

    def getHorizontal(self):
        return self._horizontal

    def getVertical(self):
        return self._vertical

    def setMarginTop(self, marginTop):
        self._marginTop = marginTop
        self.updateVertical()

    def setMarginBottom(self, marginBottom):
        self._marginBottom = marginBottom
        self.updateVertical()

    def setMarginLeft(self, marginLeft):
        self._marginLeft = marginLeft
        self.updateHorizontal()

    def setMarginRight(self, marginRight):
        self._marginRight = marginRight
        self.updateHorizontal()

    def updateVertical(self):
        self._vertical = self._marginTop + self._marginBottom

    def updateHorizontal(self):
        self._horizontal = self._marginLeft + self._marginRight

    def toString(self):
        return 'Margins [marginLeft=' + self._marginLeft + ',marginTop=' + self._marginTop + ',marginRight=' + self._marginRight + ',marginBottom=' + self._marginBottom + ']'
