# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
# from java.util.HashMap import (HashMap,)


class WidgetMap(object):
    instmap = dict()

    def instantiate(self, classType):
        return self.instmap[classType].get()

    def getImplementationByServerSideClassName(self, fullyqualifiedName):
        pass

    def getDeferredLoadedWidgets(self):
        pass

    def ensureInstantiator(self, classType):
        pass
