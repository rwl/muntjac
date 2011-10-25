
from muntjac.ui.abstract_component import AbstractComponent


class GoogleAnalytics(AbstractComponent):

    CLIENT_WIDGET = None #ClientWidget(VGoogleAnalytics)

    def __init__(self, trackerId, domainName=None):
        super(GoogleAnalytics, self).__init__()

        self._trackerId = trackerId
        self._pageId = None
        self._domainName = domainName


    def getTrackerId(self):
        return self._trackerId


    def getDomainName(self):
        return self._domainName


    def trackPageview(self, pageId):
        self._pageId = pageId
        self.requestRepaint()


    def paintContent(self, target):
        super(GoogleAnalytics, self).paintContent(target)

        target.addAttribute('trackerid', self._trackerId)

        if self._pageId is not None:
            target.addAttribute('pageid', self._pageId)

        if self._domainName is not None:
            target.addAttribute('domain', self._domainName)
