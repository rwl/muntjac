# Copyright (C) 2011 Vaadin Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

from __pyjamas__ import JS

import pygwt as GWT

from pyjamas.Timer import Timer

from muntjac.terminal.gwt.client.v_console import VConsole
from muntjac.terminal.gwt.client.v_debug_console VDebugConsole
from muntjac.terminal.gwt.client.widget_set import WidgetSet
from muntjac.terminal.gwt.client.application_connection import ApplicationConnection
from muntjac.terminal.gwt.client.null_console import NullConsole
from muntjac.terminal.gwt.client.ui.v_unknown_component import VUnknownComponent
from muntjac.terminal.gwt.client.browser_info import BrowserInfo


class ApplicationConfiguration(object):#EntryPoint):

    # Builds number. For example 0-custom_tag in 5.0.0-custom_tag.
    VERSION = None

    # Initialize version numbers from string replaced by build-script.
    if '@VERSION@' == '@' + 'VERSION' + '@':
        VERSION = '9.9.9.INTERNAL-DEBUG-BUILD'
    else:
        VERSION = '@VERSION@'

    _widgetSet = GWT.create(WidgetSet)

    # TODO consider to make this hashmap per application
    callbacks = list()

    _widgetsLoading = None

    _unstartedApplications = list()

    _runningApplications = list()


    def __init__(self):
        self._id = None
        self._themeUri = None
        self._appUri = None
        self._versionInfo = None
        self._windowName = None
        self._standalone = None
        self._communicationErrorCaption = None
        self._communicationErrorMessage = None
        self._communicationErrorUrl = None
        self._authorizationErrorCaption = None
        self._authorizationErrorMessage = None
        self._authorizationErrorUrl = None
        self._requiredWidgetset = None
        self._useDebugIdInDom = True
        self._usePortletURLs = False
        self._portletUidlURLBase = None
        self._unknownComponents = None
        self._classes = [None] * 1024
        self._windowId = None


    def usePortletURLs(self):
        return self._usePortletURLs


    def getPortletUidlURLBase(self):
        return self._portletUidlURLBase


    def getRootPanelId(self):
        return self._id


    def getApplicationUri(self):
        """Gets the application base URI. Using this other than as the download
        action URI can cause problems in Portlet 2.0 deployments.

        @return: application base URI
        """
        return self._appUri


    def getThemeUri(self):
        return self._themeUri


    def setAppId(self, appId):
        self._id = appId


    def isStandalone(self):
        """@return: true if the application is served by std. Muntjac servlet
                    and is considered to be the only or main content of the
                    host page.
        """
        return self._standalone


    def setInitialWindowName(self, name):
        self._windowName = name


    def getInitialWindowName(self):
        return self._windowName


    def getVersionInfoJSObject(self):
        return self._versionInfo


    def getCommunicationErrorCaption(self):
        return self._communicationErrorCaption


    def getCommunicationErrorMessage(self):
        return self._communicationErrorMessage


    def getCommunicationErrorUrl(self):
        return self._communicationErrorUrl


    def getAuthorizationErrorCaption(self):
        return self._authorizationErrorCaption


    def getAuthorizationErrorMessage(self):
        return self._authorizationErrorMessage


    def getAuthorizationErrorUrl(self):
        return self._authorizationErrorUrl


    def getRequiredWidgetset(self):
        return self._requiredWidgetset


    def loadFromDOM(self):
        JS("""
            var id = @{{self}}.@com.vaadin.terminal.gwt.client.ApplicationConfiguration::id;
            if($wnd.vaadin.vaadinConfigurations && $wnd.vaadin.vaadinConfigurations[id]) {
                var jsobj = $wnd.vaadin.vaadinConfigurations[id];
                var uri = jsobj.appUri;
                if(uri != null && uri[uri.length -1] != "/") {
                    uri = uri + "/";
                }
                @{{self}}.@com.vaadin.terminal.gwt.client.ApplicationConfiguration::appUri = uri;
                @{{self}}.@com.vaadin.terminal.gwt.client.ApplicationConfiguration::themeUri = jsobj.themeUri;
                if(jsobj.windowName) {
                    @{{self}}.@com.vaadin.terminal.gwt.client.ApplicationConfiguration::windowName = jsobj.windowName;
                }
                if('useDebugIdInDom' in jsobj && typeof(jsobj.useDebugIdInDom) == "boolean") {
                    @{{self}}.@com.vaadin.terminal.gwt.client.ApplicationConfiguration::useDebugIdInDom = jsobj.useDebugIdInDom;
                }
                if(jsobj.versionInfo) {
                    @{{self}}.@com.vaadin.terminal.gwt.client.ApplicationConfiguration::versionInfo = jsobj.versionInfo;
                }
                if(jsobj.comErrMsg) {
                    @{{self}}.@com.vaadin.terminal.gwt.client.ApplicationConfiguration::communicationErrorCaption = jsobj.comErrMsg.caption;
                    @{{self}}.@com.vaadin.terminal.gwt.client.ApplicationConfiguration::communicationErrorMessage = jsobj.comErrMsg.message;
                    @{{self}}.@com.vaadin.terminal.gwt.client.ApplicationConfiguration::communicationErrorUrl = jsobj.comErrMsg.url;
                }
                if(jsobj.authErrMsg) {
                    @{{self}}.@com.vaadin.terminal.gwt.client.ApplicationConfiguration::authorizationErrorCaption = jsobj.authErrMsg.caption;
                    @{{self}}.@com.vaadin.terminal.gwt.client.ApplicationConfiguration::authorizationErrorMessage = jsobj.authErrMsg.message;
                    @{{self}}.@com.vaadin.terminal.gwt.client.ApplicationConfiguration::authorizationErrorUrl = jsobj.authErrMsg.url;
                }
                if (jsobj.usePortletURLs) {
                    @{{self}}.@com.vaadin.terminal.gwt.client.ApplicationConfiguration::usePortletURLs = jsobj.usePortletURLs;
                }
                if (jsobj.portletUidlURLBase) {
                    @{{self}}.@com.vaadin.terminal.gwt.client.ApplicationConfiguration::portletUidlURLBase = jsobj.portletUidlURLBase;
                }
                if (jsobj.standalone) {
                    @{{self}}.@com.vaadin.terminal.gwt.client.ApplicationConfiguration::standalone = true;
                }
                if (jsobj.widgetset) {
                    @{{self}}.@com.vaadin.terminal.gwt.client.ApplicationConfiguration::requiredWidgetset = jsobj.widgetset;
                }
            } else {
                $wnd.alert("Vaadin app failed to initialize: " + @{{self}}.id);
            }
        """)
        pass


    @classmethod
    def initConfigurations(cls):
        """Inits the ApplicationConfiguration by reading the DOM and
        instantiating ApplicationConnections accordingly. Call
        L{startNextApplication} to actually start the applications.

        @param widgetset:
                   the widgetset that is running the apps
        """
        appIds = list()
        cls.loadAppIdListFromDOM(appIds)
        for appId in appIds:
            appConf = cls.getConfigFromDOM(appId)
            if cls.canStartApplication(appConf):
                a = GWT.create(ApplicationConnection)
                a.init(cls._widgetSet, appConf)
                cls._unstartedApplications.add(a)
                cls.consumeApplication(appId)
            else:
                VConsole.log('Application ' + appId + ' was not started. '
                        'Provided widgetset did not match with this module.')


    @classmethod
    def consumeApplication(cls, appId):
        """Marks an applicatin with given id to be initialized. Suggesting
        other modules should not try to start this application anymore.
        """
        JS("""
            $wnd.vaadin.vaadinConfigurations[@{{appId}}].initialized = true;
        """)
        pass


    @classmethod
    def canStartApplication(cls, appConf):
        return ((appConf.getRequiredWidgetset() is None)
                or (appConf.getRequiredWidgetset() == GWT.getModuleName()))


    @classmethod
    def startNextApplication(cls):
        """Starts the next unstarted application. The WidgetSet should call
        this once to start the first application; after that, each application
        should call this once it has started. This ensures that the
        applications are started synchronously, which is necessary to avoid
        session-id problems.

        @return: true if an unstarted application was found
        """
        if len(cls._unstartedApplications) > 0:
            a = cls._unstartedApplications.remove(0)
            a.start()
            cls._runningApplications.add(a)
            return True
        else:
            cls._deferredWidgetLoader = DeferredWidgetLoader()
            return False


    @classmethod
    def getRunningApplications(cls):
        return cls._runningApplications


    @classmethod
    def loadAppIdListFromDOM(cls, lst):
        JS("""
            var j;
            for(j in $wnd.vaadin.vaadinConfigurations) {
                if(!$wnd.vaadin.vaadinConfigurations[j].initialized) {
                    @{{lst}}.@java.util.Collection::add(Ljava/lang/Object;)(j);
                }
            }
        """)
        pass


    @classmethod
    def getConfigFromDOM(cls, appId):
        conf = ApplicationConfiguration()
        conf.setAppId(appId)
        conf.loadFromDOM()
        return conf


    def getServletVersion(self):
        JS("""
            return @{{self}}.@com.vaadin.terminal.gwt.client.ApplicationConfiguration::versionInfo.vaadinVersion;
        """)
        pass


    def getApplicationVersion(self):
        JS("""
            return @{{self}}.@com.vaadin.terminal.gwt.client.ApplicationConfiguration::versionInfo.applicationVersion;
        """)
        pass


    def useDebugIdInDOM(self):
        return self._useDebugIdInDom


    def getWidgetClassByEncodedTag(self, tag):
        # component was not present in mappings
        try:
            parseInt = int(tag)
            return self._classes[parseInt]
        except Exception:
            return VUnknownComponent


    def addComponentMappings(self, valueMap, widgetSet):
        keyArray = valueMap.getKeyArray()
        for i in range(len(keyArray)):
            key = keyArray.get(i).intern()
            value = valueMap.getInt(key)
            self._classes[value] = widgetSet.getImplementationByClassName(key)
            if self._classes[value] == VUnknownComponent:
                if self._unknownComponents is None:
                    self._unknownComponents = dict()
                self._unknownComponents[str(value)] = key
            elif key == 'com.vaadin.ui.Window':
                self._windowId = str(value)


    def getEncodedWindowTag(self):
        """@return: the integer value that is used to code top level windows
                "com.vaadin.ui.Window"
        """
        return self._windowId


    def getUnknownServerClassNameByEncodedTagName(self, tag):
        if self._unknownComponents is not None:
            return self._unknownComponents.get(tag)
        return None


    @classmethod
    def runWhenWidgetsLoaded(cls, c):
        if cls._widgetsLoading == 0:
            c.execute()
        else:
            cls.callbacks.add(c)


    @classmethod
    def startWidgetLoading(cls):
        cls._widgetsLoading += 1


    @classmethod
    def endWidgetLoading(cls):
        # This loop loads widget implementation that should be loaded deferred.
        cls._widgetsLoading -= 1
        if cls._widgetsLoading == 0 and not cls.callbacks.isEmpty():
            for cmd in cls.callbacks:
                cmd.execute()
            cls.callbacks.clear()
        elif cls._widgetsLoading == 0 and cls._deferredWidgetLoader is not None:
            cls._deferredWidgetLoader.trigger()


    _deferredWidgetLoader = None


    def onModuleLoad(self):
        # Enable IE6 Background image caching
        # From ImageSrcIE6
        if BrowserInfo.get().isIE6():
            self.enableIE6BackgroundImageCache()

        # Prepare VConsole for debugging
        if self.isDebugMode():
            console = GWT.create(VDebugConsole)
            console.setQuietMode(self.isQuietDebugMode())
            console.init()
            VConsole.setImplementation(console)
        else:
            VConsole.setImplementation(GWT.create(NullConsole))

        # Display some sort of error of exceptions in web mode to debug
        # console. After this, exceptions are reported to VConsole and possible
        # GWT hosted mode.
        GWT.setUncaughtExceptionHandler(self.onUncaughtException)

        self.initConfigurations()
        self.startNextApplication()


    def onUncaughtException(self, e):
        # Note in case of null console (without ?debug) we eat
        # exceptions. "a1 is not an object" style errors helps nobody,
        # especially end user. It does not work tells just as much.
        VConsole.getImplementation().error(e)


    @classmethod
    def enableIE6BackgroundImageCache(cls):
        JS("""
           // Fix IE background image refresh bug, present through IE6
           // see http://www.mister-pixel.com/#Content__state=is_that_simple
           // @{{self}} only works with IE6 SP1+
           try {
             $doc.execCommand("BackgroundImageCache", false, true);
           } catch (e) {
             // ignore error on other browsers
           }
        """)
        pass


    @classmethod
    def isDebugMode(cls):
        """Checks if client side is in debug mode. Practically this is invoked
        by adding ?debug parameter to URI.

        @return: true if client side is currently been debugged
        """
        JS("""
            if($wnd.vaadin.debug) {
                var parameters = $wnd.location.search;
                var re = /debug[^\/]*$/;
                return re.test(parameters);
            } else {
                return false;
            }
        """)
        pass


    @classmethod
    def isQuietDebugMode(cls):
        JS("""
            var uri = $wnd.location;
            var re = /debug=q[^\/]*$/;
            return re.test(uri);
        """)
        pass


class DeferredWidgetLoader(Timer):

    _FREE_LIMIT = 4
    _FREE_CHECK_TIMEOUT = 100

    def __init__(self, config):
        self._communicationFree = 0
        self._nextWidgetIndex = 0
        self._pending = None

        self._config = config
        self.schedule(5000)


    def trigger(self):
        if not self._pending:
            self.schedule(self._FREE_CHECK_TIMEOUT)


    def schedule(self, delayMillis):
        super(DeferredWidgetLoader, self).schedule(delayMillis)
        self._pending = True


    def run(self):
        self._pending = False
        if not self.isBusy():
            nextType = self.getNextType()
            if nextType is None:
                # ensured that all widgets are loaded
                self._config._deferredWidgetLoader = None
            else:
                self._communicationFree = 0
                self._config._widgetSet.loadImplementation(nextType)
        else:
            self.schedule(self._FREE_CHECK_TIMEOUT)


    def getNextType(self):
        deferredLoadedWidgets = self._config._widgetSet.getDeferredLoadedWidgets()
        if len(deferredLoadedWidgets) <= self._nextWidgetIndex:
            return None
        else:
            r = deferredLoadedWidgets[self._nextWidgetIndex]
            self._nextWidgetIndex += 1
            return r


    def isBusy(self):
        if self._config._widgetsLoading > 0:
            self._communicationFree = 0
            return True
        for app in self._config._runningApplications:
            if app.hasActiveRequest():
                # if an UIDL request or widget loading is active, mark as
                # busy
                self._communicationFree = 0
                return True
        self._communicationFree += 1
        return self._communicationFree < self._FREE_LIMIT
