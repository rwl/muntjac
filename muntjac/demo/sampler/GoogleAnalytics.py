# -*- coding: utf-8 -*-
from __pyjamas__ import (ARGERROR,)
# from com.vaadin.ui.AbstractComponent import (AbstractComponent,)


class GoogleAnalytics(AbstractComponent):
    _trackerId = None
    _pageId = None
    _domainName = None

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            trackerId, = _0
            self._trackerId = trackerId
        elif _1 == 2:
            trackerId, domainName = _0
            self.__init__(trackerId)
            self._domainName = domainName
        else:
            raise ARGERROR(1, 2)

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
