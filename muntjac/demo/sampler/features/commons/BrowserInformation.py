
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.terminal.gwt.server.web_browser import WebBrowser


class BrowserInformation(Feature):

    def getDescription(self):
        return ('Browser differences are mostly hidden by Muntjac but in some '
            'cases it is valuable to get information on the browser the user '
            'is using. In themes special CSS rules are used but it is also '
            'possible to get information about the browser in the application '
            'code. This sample displays the browser name, ip address and the '
            'screen size you are using, and your TimeZone offset. The '
            'information is available on server side.')


    def getName(self):
        return 'Browser information'


    def getSinceVersion(self):
        return Version.V63


    def getRelatedAPI(self):
        return [APIResource(WebBrowser)]


    def getRelatedFeatures(self):
        return None


    def getRelatedResources(self):
        return None
