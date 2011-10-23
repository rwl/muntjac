
from muntjac.ui.window import Window

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class NativeWindow(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Native window'


    def getDescription(self):
        return ('A <i>NativeWindow</i> is a separate browser window, which'
            ' looks and works just like the main window.<br/>'
            ' There are multiple ways to make native windows; you can'
            ' override Application.getWindow() (recommended in any case)'
            ' but you can also use Application.addWindow() - the added'
            ' window will be available from a separate URL (which is'
            ' based on the window name.)<br/> When you view Sampler in'
            ' a new window, the getWindow() method is used, this example'
            ' also uses addWindow().')


    def getRelatedAPI(self):
        return [APIResource(Window)]


    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.windows.Subwindow import Subwindow
        from muntjac.demo.sampler.FeatureSet import Links, Windows
        return [Subwindow, Links, Windows]


    def getRelatedResources(self):
        return None
