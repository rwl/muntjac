# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.addon.google_maps.overlay.poly_overlay \
    import PolyOverlay


class Polygon(PolyOverlay):

    def __init__(self, Id, points, strokeColor='#ffffff', strokeWeight=1,
                strokeOpacity=1.0, fillColor='#777777', fillOpacity=0.2,
                clickable=False):
        super(Polygon, self).__init__(Id, points, strokeColor, strokeWeight,
                strokeOpacity, clickable)
        self._fillColor = fillColor
        self._fillOpacity = fillOpacity


    def getFillColor(self):
        return self._fillColor


    def setFillColor(self, fillColor):
        self._fillColor = fillColor


    def getFillOpacity(self):
        return self._fillOpacity


    def setFillOpacity(self, fillOpacity):
        self._fillOpacity = fillOpacity
