# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@


class IMarker(object):
    """@author: Henri Muurimaa
    @author: Richard Lincoln"""

    def getId(self):
        raise NotImplementedError

    def isVisible(self):
        raise NotImplementedError

    def getLatLng(self):
        raise NotImplementedError

    def getIconUrl(self):
        raise NotImplementedError

    def getIconAnchor(self):
        raise NotImplementedError

    def getTitle(self):
        raise NotImplementedError

    def getInfoWindowContent(self):
        raise NotImplementedError

    def isDraggable(self):
        raise NotImplementedError
