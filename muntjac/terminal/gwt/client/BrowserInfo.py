# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.VBrowserDetails import (VBrowserDetails,)
# from java.util.Date import (Date,)


class BrowserInfo(object):
    """Class used to query information about web browser.

    Browser details are detected only once and those are stored in this singleton
    class.
    """
    _BROWSER_OPERA = 'op'
    _BROWSER_IE = 'ie'
    _BROWSER_FIREFOX = 'ff'
    _BROWSER_SAFARI = 'sa'
    ENGINE_GECKO = 'gecko'
    ENGINE_WEBKIT = 'webkit'
    ENGINE_PRESTO = 'presto'
    ENGINE_TRIDENT = 'trident'
    _OS_WINDOWS = 'win'
    _OS_LINUX = 'lin'
    _OS_MACOSX = 'mac'
    _instance = None
    _cssClass = None
    browserClassnames = get().getCSSClass()
    RootPanel.get().addStyleName(browserClassnames)
    # Add browser dependent v-* classnames to body to help css hacks

    @classmethod
    def get(cls):
        """Singleton method to get BrowserInfo object.

        @return instance of BrowserInfo object
        """
        if cls._instance is None:
            cls._instance = BrowserInfo()
        return cls._instance

    _browserDetails = None
    _touchDevice = None

    def __init__(self):
        self._browserDetails = VBrowserDetails(self.getBrowserString())
        if self._browserDetails.isIE():
            # Use document mode instead user agent to accurately detect how we
            # are rendering
            documentMode = self.getIEDocumentMode()
            if documentMode != -1:
                self._browserDetails.setIEMode(documentMode)
        self._touchDevice = self.detectTouchDevice()

    def detectTouchDevice(self):
        JS("""
        try { document.createEvent("TouchEvent");return true;} catch(e){return false;};
    """)
        pass

    def getIEDocumentMode(self):
        JS("""
    	var mode = $wnd.document.documentMode;
    	if (!mode)
    		 return -1;
    	return mode;
    """)
        pass

    def getCSSClass(self):
        """Returns a string representing the browser in use, for use in CSS
        classnames. The classnames will be space separated abbreviations,
        optionally with a version appended.

        Abbreviations: Firefox: ff Internet Explorer: ie Safari: sa Opera: op

        Browsers that CSS-wise behave like each other will get the same
        abbreviation (this usually depends on the rendering engine).

        This is quite simple at the moment, more heuristics will be added when
        needed.

        Examples: Internet Explorer 6: ".v-ie .v-ie6 .v-ie60", Firefox 3.0.4:
        ".v-ff .v-ff3 .v-ff30", Opera 9.60: ".v-op .v-op9 .v-op960", Opera 10.10:
        ".v-op .v-op10 .v-op1010"

        @return
        """
        prefix = 'v-'
        if self._cssClass is None:
            browserIdentifier = ''
            majorVersionClass = ''
            minorVersionClass = ''
            browserEngineClass = ''
            if self._browserDetails.isFirefox():
                browserIdentifier = self._BROWSER_FIREFOX
                majorVersionClass = browserIdentifier + self._browserDetails.getBrowserMajorVersion()
                minorVersionClass = majorVersionClass + self._browserDetails.getBrowserMinorVersion()
                browserEngineClass = self.ENGINE_GECKO
            elif self._browserDetails.isChrome():
                # TODO update when Chrome is more stable
                browserIdentifier = self._BROWSER_SAFARI
                majorVersionClass = 'ch'
                browserEngineClass = self.ENGINE_WEBKIT
            elif self._browserDetails.isSafari():
                browserIdentifier = self._BROWSER_SAFARI
                majorVersionClass = browserIdentifier + self._browserDetails.getBrowserMajorVersion()
                minorVersionClass = majorVersionClass + self._browserDetails.getBrowserMinorVersion()
                browserEngineClass = self.ENGINE_WEBKIT
            elif self._browserDetails.isIE():
                browserIdentifier = self._BROWSER_IE
                majorVersionClass = browserIdentifier + self._browserDetails.getBrowserMajorVersion()
                minorVersionClass = majorVersionClass + self._browserDetails.getBrowserMinorVersion()
                browserEngineClass = self.ENGINE_TRIDENT
            elif self._browserDetails.isOpera():
                browserIdentifier = self._BROWSER_OPERA
                majorVersionClass = browserIdentifier + self._browserDetails.getBrowserMajorVersion()
                minorVersionClass = majorVersionClass + self._browserDetails.getBrowserMinorVersion()
                browserEngineClass = self.ENGINE_PRESTO
            self._cssClass = prefix + browserIdentifier
            if not ('' == majorVersionClass):
                self._cssClass = self._cssClass + ' ' + prefix + majorVersionClass
            if not ('' == minorVersionClass):
                self._cssClass = self._cssClass + ' ' + prefix + minorVersionClass
            if not ('' == browserEngineClass):
                self._cssClass = self._cssClass + ' ' + prefix + browserEngineClass
            osClass = self.getOperatingSystemClass()
            if osClass is not None:
                self._cssClass = self._cssClass + ' ' + prefix + osClass
        return self._cssClass

    def getOperatingSystemClass(self):
        if self._browserDetails.isWindows():
            return self._OS_WINDOWS
        elif self._browserDetails.isLinux():
            return self._OS_LINUX
        elif self._browserDetails.isMacOSX():
            return self._OS_MACOSX
        # Unknown OS
        return None

    def isIE(self):
        return self._browserDetails.isIE()

    def isFirefox(self):
        return self._browserDetails.isFirefox()

    def isSafari(self):
        return self._browserDetails.isSafari()

    def isSafari4(self):
        return self.isSafari() and self._browserDetails.getBrowserMajorVersion() == 4

    def isIE6(self):
        return self.isIE() and self._browserDetails.getBrowserMajorVersion() == 6

    def isIE7(self):
        return self.isIE() and self._browserDetails.getBrowserMajorVersion() == 7

    def isIE8(self):
        return self.isIE() and self._browserDetails.getBrowserMajorVersion() == 8

    def isIE9(self):
        return self.isIE() and self._browserDetails.getBrowserMajorVersion() == 9

    def isChrome(self):
        return self._browserDetails.isChrome()

    def isGecko(self):
        return self._browserDetails.isGecko()

    def isWebkit(self):
        return self._browserDetails.isWebKit()

    def isFF2(self):
        # FIXME: Should use browserVersion
        return self._browserDetails.isFirefox() and self._browserDetails.getBrowserEngineVersion() == 1.8

    def isFF3(self):
        # FIXME: Should use browserVersion
        return self._browserDetails.isFirefox() and self._browserDetails.getBrowserEngineVersion() == 1.9

    def isFF4(self):
        return self._browserDetails.isFirefox() and self._browserDetails.getBrowserMajorVersion() == 4

    def getGeckoVersion(self):
        """Returns the Gecko version if the browser is Gecko based. The Gecko
        version for Firefox 2 is 1.8 and 1.9 for Firefox 3.

        @return The Gecko version or -1 if the browser is not Gecko based
        """
        if not self._browserDetails.isGecko():
            return -1
        return self._browserDetails.getBrowserEngineVersion()

    def getWebkitVersion(self):
        """Returns the WebKit version if the browser is WebKit based. The WebKit
        version returned is the major version e.g., 523.

        @return The WebKit version or -1 if the browser is not WebKit based
        """
        if not self._browserDetails.isWebKit():
            return -1
        return self._browserDetails.getBrowserEngineVersion()

    def getIEVersion(self):
        if not self._browserDetails.isIE():
            return -1
        return self._browserDetails.getBrowserMajorVersion()

    def getOperaVersion(self):
        if not self._browserDetails.isOpera():
            return -1
        return self._browserDetails.getBrowserMajorVersion()

    def isOpera(self):
        return self._browserDetails.isOpera()

    def isOpera10(self):
        return self._browserDetails.isOpera() and self._browserDetails.getBrowserMajorVersion() == 10

    def isOpera11(self):
        return self._browserDetails.isOpera() and self._browserDetails.getBrowserMajorVersion() == 11

    @classmethod
    def getBrowserString(cls):
        JS("""
    	return $wnd.navigator.userAgent;
    """)
        pass

    def getScreenWidth(self):
        JS("""
    	return $wnd.screen.width;
    """)
        pass

    def getScreenHeight(self):
        JS("""
    	return $wnd.screen.height;
    """)
        pass

    def getTimezoneOffset(self):
        """Get's the timezone offset from GMT in minutes, as reported by the
        browser. DST affects this value.

        @return offset to GMT in minutes
        """
        JS("""
    	return new Date().getTimezoneOffset();
    """)
        pass

    def getRawTimezoneOffset(self):
        """Gets the timezone offset from GMT in minutes, as reported by the browser
        AND adjusted to ignore daylight savings time. DST does not affect this
        value.

        @return offset to GMT in minutes
        """
        JS("""
        var d = new Date();
        var tzo1 = d.getTimezoneOffset(); // current offset

        for (var m=12;m>0;m--) {
            d.setUTCMonth(m);
            var tzo2 = d.getTimezoneOffset();
            if (tzo1 != tzo2) {
                // NOTE js indicates @{{self}} 'backwards' (e.g -180) 
                return (tzo1 > tzo2 ? tzo1 : tzo2); // offset w/o DST
            }
        }

        return tzo1; // no DST

    """)
        pass

    def getDSTSavings(self):
        """Gets the difference in minutes between the browser's GMT timezone and
        DST.

        @return the amount of minutes that the timezone shifts when DST is in
                effect
        """
        JS("""
        var d = new Date();
        var tzo1 = d.getTimezoneOffset(); // current offset

        for (var m=12;m>0;m--) {
            d.setUTCMonth(m);
            var tzo2 = d.getTimezoneOffset();
            if (tzo1 != tzo2) {
                // NOTE js indicates @{{self}} 'backwards' (e.g -180) 
                return (tzo1 > tzo2 ? tzo1-tzo2 : tzo2-tzo1); // offset w/o DST
            }
        }

        return 0; // no DST
    """)
        pass

    def isDSTInEffect(self):
        """Determines whether daylight savings time (DST) is currently in effect in
        the region of the browser or not.

        @return true if the browser resides at a location that currently is in
                DST
        """
        return self.getTimezoneOffset() != self.getRawTimezoneOffset()

    def getCurrentDate(self):
        """Returns the current date and time of the browser. This will not be
        entirely accurate due to varying network latencies, but should provide a
        close-enough value for most cases.

        @return the current date and time of the browser.
        """
        return Date()

    def isTouchDevice(self):
        """@return true if the browser runs on a touch based device."""
        return self._touchDevice
