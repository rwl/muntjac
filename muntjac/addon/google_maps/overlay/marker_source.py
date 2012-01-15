# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@


class IMarkerSource(object):

    def getMarkers(self):
        raise NotImplementedError

    def addMarker(self, newMarker):
        raise NotImplementedError

    def registerEvents(self, map_):
        raise NotImplementedError

    def getMarkerJSON(self):
        raise NotImplementedError

    def getMarker(self, markerId):
        raise NotImplementedError
