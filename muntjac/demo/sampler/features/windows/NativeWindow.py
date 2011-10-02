# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.windows.Subwindow import (Subwindow,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Links = FeatureSet.Links
Windows = FeatureSet.Windows
Version = Feature.Version


class NativeWindow(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Native window'

    def getDescription(self):
        return 'A <i>NativeWindow</i> is a separate browser window, which' + ' looks and works just like the main window.<br/>' + ' There are multiple ways to make native windows; you can' + ' override Application.getWindow() (recommended in any case)' + ' but you can also use Application.addWindow() - the added' + ' window will be available from a separate URL (which is' + ' based on the window name.)<br/> When you view Sampler in' + ' a new window, the getWindow() method is used, this example' + ' also uses addWindow().'

    def getRelatedAPI(self):
        return [APIResource(Window)]

    def getRelatedFeatures(self):
        return [Subwindow, Links, Windows]

    def getRelatedResources(self):
        return None
