# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (POSTINC,)
from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
from com.vaadin.terminal.gwt.client.VDebugConsole import (VDebugConsole,)
from com.vaadin.terminal.gwt.client.WidgetSet import (WidgetSet,)
from com.vaadin.terminal.gwt.client.ApplicationConnection import (ApplicationConnection,)
from com.vaadin.terminal.gwt.client.NullConsole import (NullConsole,)
from com.vaadin.terminal.gwt.client.ui.VUnknownComponent import (VUnknownComponent,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
# from com.google.gwt.core.client.EntryPoint import (EntryPoint,)
# from com.google.gwt.core.client.GWT.UncaughtExceptionHandler import (UncaughtExceptionHandler,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.HashMap import (HashMap,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedList import (LinkedList,)
# from java.util.List import (List,)


class ApplicationConfiguration(EntryPoint):
    # Builds number. For example 0-custom_tag in 5.0.0-custom_tag.
    VERSION = None
    # Initialize version numbers from string replaced by build-script.
    if '@VERSION@' == '@' + 'VERSION' + '@':
        VERSION = '9.9.9.INTERNAL-DEBUG-BUILD'
    else:
        VERSION = '@VERSION@'
    _widgetSet = GWT.create(WidgetSet)
    _id = None
    _themeUri = None
    _appUri = None
    _versionInfo = None
    _windowName = None
    _standalone = None
    _communicationErrorCaption = None
    _communicationErrorMessage = None
    _communicationErrorUrl = None
    _authorizationErrorCaption = None
    _authorizationErrorMessage = None
    _authorizationErrorUrl = None
    _requiredWidgetset = None
    _useDebugIdInDom = True
    _usePortletURLs = False
    _portletUidlURLBase = None
    _unknownComponents = None
    _classes = [None] * 1024
    _windowId = None
    callbacks = LinkedList()
    # TODO consider to make this hashmap per application
    _widgetsLoading = None
    _unstartedApplications = list()
    _runningApplications = list()

    def usePortletURLs(self):
        return self._usePortletURLs

    def getPortletUidlURLBase(self):
        return self._portletUidlURLBase

    def getRootPanelId(self):
        return self._id

    def getApplicationUri(self):
        """Gets the application base URI. Using this other than as the download
        action URI can cause problems in Portlet 2.0 deployments.

        @return application base URI
        """
        return self._appUri

    def getThemeUri(self):
        return self._themeUri

    def setAppId(self, appId):
        self._id = appId

    def isStandalone(self):
        """@return true if the application is served by std. Vaadin servlet and is
                considered to be the only or main content of the host page.
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
        """Inits the ApplicationConfiguration by reading the DOM and instantiating
        ApplicationConnections accordingly. Call {@link #startNextApplication()}
        to actually start the applications.

        @param widgetset
                   the widgetset that is running the apps
        """
        appIds = list()
        cls.loadAppIdListFromDOM(appIds)
        _0 = True
        it = appIds
        while True:
            if _0 is True:
                _0 = False
            if not it.hasNext():
                break
            appId = it.next()
            appConf = cls.getConfigFromDOM(appId)
            if cls.canStartApplication(appConf):
                a = GWT.create(ApplicationConnection)
                a.init(cls._widgetSet, appConf)
                cls._unstartedApplications.add(a)
                cls.consumeApplication(appId)
            else:
                VConsole.log('Application ' + appId + ' was not started. Provided widgetset did not match with this module.')

    @classmethod
    def consumeApplication(cls, appId):
        """Marks an applicatin with given id to be initialized. Suggesting other
        modules should not try to start this application anymore.

        @param appId
        """
        JS("""
         $wnd.vaadin.vaadinConfigurations[@{{appId}}].initialized = true;
    """)
        pass

    @classmethod
    def canStartApplication(cls, appConf):
        return (appConf.getRequiredWidgetset() is None) or (appConf.getRequiredWidgetset() == GWT.getModuleName())

    @classmethod
    def startNextApplication(cls):
        """Starts the next unstarted application. The WidgetSet should call this
        once to start the first application; after that, each application should
        call this once it has started. This ensures that the applications are
        started synchronously, which is neccessary to avoid session-id problems.

        @return true if an unstarted application was found
        """
        if len(cls._unstartedApplications) > 0:
            a = cls._unstartedApplications.remove(0)
            a.start()
            cls._runningApplications.add(a)
            return True
        else:
            cls._deferredWidgetLoader = cls.DeferredWidgetLoader()
            return False

    @classmethod
    def getRunningApplications(cls):
        return cls._runningApplications

    @classmethod
    def loadAppIdListFromDOM(cls, list):
        JS("""
         var j;
         for(j in $wnd.vaadin.vaadinConfigurations) {
             if(!$wnd.vaadin.vaadinConfigurations[j].initialized) {
                 @{{list}}.@java.util.Collection::add(Ljava/lang/Object;)(j);
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
        except Exception, e:
            return VUnknownComponent

    def addComponentMappings(self, valueMap, widgetSet):
        keyArray = valueMap.getKeyArray()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(keyArray)):
                break
            key = keyArray.get(i).intern()
            value = valueMap.getInt(key)
            self._classes[value] = widgetSet.getImplementationByClassName(key)
            if self._classes[value] == VUnknownComponent:
                if self._unknownComponents is None:
                    self._unknownComponents = dict()
                self._unknownComponents.put('' + value, key)
            elif key == 'com.vaadin.ui.Window':
                self._windowId = '' + value

    def getEncodedWindowTag(self):
        """@return the integer value that is used to code top level windows
                "com.vaadin.ui.Window"
        """
        return self._windowId

    def getUnknownServerClassNameByEncodedTagName(self, tag):
        if self._unknownComponents is not None:
            return self._unknownComponents[tag]
        return None

    @classmethod
    def runWhenWidgetsLoaded(cls, c):
        """@param c"""
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

    def DeferredWidgetLoader(ApplicationConfiguration_this, *args, **kwargs):

        class DeferredWidgetLoader(Timer):
            _FREE_LIMIT = 4
            _FREE_CHECK_TIMEOUT = 100
            _communicationFree = 0
            _nextWidgetIndex = 0
            _pending = None

            def __init__(self):
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
                        ApplicationConfiguration_this._deferredWidgetLoader = None
                    else:
                        self._communicationFree = 0
                        ApplicationConfiguration_this._widgetSet.loadImplementation(nextType)
                else:
                    self.schedule(self._FREE_CHECK_TIMEOUT)

            def getNextType(self):
                deferredLoadedWidgets = ApplicationConfiguration_this._widgetSet.getDeferredLoadedWidgets()
                if len(deferredLoadedWidgets) <= self._nextWidgetIndex:
                    return None
                else:
                    return deferredLoadedWidgets[POSTINC(globals(), locals(), 'self._nextWidgetIndex')]

            def isBusy(self):
                if ApplicationConfiguration_this._widgetsLoading > 0:
                    self._communicationFree = 0
                    return True
                for app in ApplicationConfiguration_this._runningApplications:
                    if app.hasActiveRequest():
                        # if an UIDL request or widget loading is active, mark as
                        # busy
                        self._communicationFree = 0
                        return True
                self._communicationFree += 1
                return self._communicationFree < self._FREE_LIMIT

        return DeferredWidgetLoader(*args, **kwargs)

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

        class _0_(UncaughtExceptionHandler):

            def onUncaughtException(self, e):
                # Note in case of null console (without ?debug) we eat
                # exceptions. "a1 is not an object" style errors helps nobody,
                # especially end user. It does not work tells just as much.

                VConsole.getImplementation().error(e)

        _0_ = _0_()
        GWT.setUncaughtExceptionHandler(_0_)
        self.initConfigurations()
        self.startNextApplication()

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
        """Checks if client side is in debug mode. Practically this is invoked by
        adding ?debug parameter to URI.

        @return true if client side is currently been debugged
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
