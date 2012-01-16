# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

"""Defines a class that provides information about the web browser the user
is using."""

from time import time
from datetime import date

from muntjac.terminal.gwt.client.v_browser_details import VBrowserDetails
from muntjac.terminal.terminal import ITerminal


class WebBrowser(ITerminal):
    """Class that provides information about the web browser the user is
    using. Provides information such as browser name and version, screen
    resolution and IP address.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self):
        self._screenHeight = 0
        self._screenWidth = 0
        self._browserApplication = None
        self._locale = None
        self._address = None
        self._secureConnection = None
        self._timezoneOffset = 0
        self._rawTimezoneOffset = 0
        self._dstSavings = None
        self._dstInEffect = None
        self._touchDevice = None

        self._browserDetails = None
        self._clientServerTimeDelta = None


    def getDefaultTheme(self):
        """There is no default-theme for this terminal type.

        @return: Always returns null.
        """
        return None


    def getScreenHeight(self):
        return self._screenHeight


    def getScreenWidth(self):
        return self._screenWidth


    def getBrowserApplication(self):
        """Get the browser user-agent string.

        @return: The raw browser userAgent string
        """
        return self._browserApplication


    def getAddress(self):
        """Gets the IP-address of the web browser. If the application is
        running inside a portlet, this method will return C{None}.

        @return: IP-address in 1.12.123.123 -format
        """
        return self._address


    def getLocale(self):
        """Get the default locate of the browser."""
        return self._locale


    def isSecureConnection(self):
        """Is the connection made using HTTPS?"""
        return self._secureConnection


    def isFirefox(self):
        """Tests whether the user is using Firefox.

        @return: true if the user is using Firefox, false if the user is not
                using Firefox or if no information on the browser is present
        """
        if self._browserDetails is None:
            return False

        return self._browserDetails.isFirefox()


    def isIE(self):
        """Tests whether the user is using Internet Explorer.

        @return: true if the user is using Internet Explorer, false if the
                user is not using Internet Explorer or if no information on
                the browser is present
        """
        if self._browserDetails is None:
            return False

        return self._browserDetails.isIE()


    def isSafari(self):
        """Tests whether the user is using Safari.

        @return: true if the user is using Safari, false if the user is not
                using Safari or if no information on the browser is present
        """
        if self._browserDetails is None:
            return False

        return self._browserDetails.isSafari()


    def isOpera(self):
        """Tests whether the user is using Opera.

        @return: true if the user is using Opera, false if the user is not
                using Opera or if no information on the browser is present
        """
        if self._browserDetails is None:
            return False

        return self._browserDetails.isOpera()


    def isChrome(self):
        """Tests whether the user is using Chrome.

        @return: true if the user is using Chrome, false if the user is not
                using Chrome or if no information on the browser is present
        """
        if self._browserDetails is None:
            return False

        return self._browserDetails.isChrome()


    def getBrowserMajorVersion(self):
        """Gets the major version of the browser the user is using.

        Note that Internet Explorer in IE7 compatibility mode might
        return 8 in some cases even though it should return 7.

        @return: The major version of the browser or -1 if not known.
        """
        if self._browserDetails is None:
            return -1

        return self._browserDetails.getBrowserMajorVersion()


    def getBrowserMinorVersion(self):
        """Gets the minor version of the browser the user is using.

        @see: #getBrowserMajorVersion()

        @return: The minor version of the browser or -1 if not known.
        """
        if self._browserDetails is None:
            return -1

        return self._browserDetails.getBrowserMinorVersion()


    def isLinux(self):
        """Tests whether the user is using Linux.

        @return: true if the user is using Linux, false if the user is not
                using Linux or if no information on the browser is present
        """
        return self._browserDetails.isLinux()


    def isMacOSX(self):
        """Tests whether the user is using Mac OS X.

        @return: true if the user is using Mac OS X, false if the user is not
                using Mac OS X or if no information on the browser is present
        """
        return self._browserDetails.isMacOSX()


    def isWindows(self):
        """Tests whether the user is using Windows.

        @return: true if the user is using Windows, false if the user is not
                using Windows or if no information on the browser is present
        """
        return self._browserDetails.isWindows()


    def getTimezoneOffset(self):
        """Returns the browser-reported TimeZone offset in milliseconds from
        GMT. This includes possible daylight saving adjustments, to figure
        out which TimeZone the user actually might be in, see
        L{getRawTimezoneOffset}.

        @see: L{getRawTimezoneOffset}
        @return: timezone offset in milliseconds, 0 if not available
        """
        return self._timezoneOffset


    def getRawTimezoneOffset(self):
        """Returns the browser-reported TimeZone offset in milliseconds
        from GMT ignoring possible daylight saving adjustments that may
        be in effect in the browser.

        You can use this to figure out which TimeZones the user could actually
        be in by calling L{TimeZone.getAvailableIDs}.

        If L{getRawTimezoneOffset} and L{getTimezoneOffset} returns the same
        value, the browser is either in a zone that does not currently have
        daylight saving time, or in a zone that never has daylight saving time.

        @return: timezone offset in milliseconds excluding DST, 0 if not
                available
        """
        return self._rawTimezoneOffset


    def getDSTSavings(self):
        """Gets the difference in minutes between the browser's GMT TimeZone
        and DST.

        @return: the amount of minutes that the TimeZone shifts when DST is in
                effect
        """
        return self._dstSavings


    def isDSTInEffect(self):
        """Determines whether daylight savings time (DST) is currently in
        effect in the region of the browser or not.

        @return: true if the browser resides at a location that currently is in
                DST
        """
        return self._dstInEffect


    def getCurrentDate(self):
        """Returns the current date and time of the browser. This will not be
        entirely accurate due to varying network latencies, but should provide
        a close-enough value for most cases. Also note that the returned Date
        object uses servers default time zone, not the clients.

        @return: the current date and time of the browser.
        @see: L{isDSTInEffect}
        @see: L{getDSTSavings}
        @see: L{getTimezoneOffset}
        """
        return date.fromtimestamp(time() + self._clientServerTimeDelta)


    def isTouchDevice(self):
        """@return: true if the browser is detected to support touch events"""
        return self._touchDevice


    def updateClientSideDetails(self, sw, sh, tzo, rtzo, dstSavings,
                dstInEffect, curDate, touchDevice):
        """For internal use by AbstractApplicationServlet only. Updates all
        properties in the class according to the given information.

        @param sw:
                   Screen width
        @param sh:
                   Screen height
        @param tzo:
                   TimeZone offset in minutes from GMT
        @param rtzo:
                   raw TimeZone offset in minutes from GMT (w/o DST adjustment)
        @param dstSavings:
                   the difference between the raw TimeZone and DST in minutes
        @param dstInEffect:
                   is DST currently active in the region or not?
        @param curDate:
                   the current date in milliseconds since the epoch
        @param touchDevice:
        """
        if sw is not None:
            try:
                self._screenHeight = int(sh)
                self._screenWidth = int(sw)
            except ValueError:
                self._screenHeight = self._screenWidth = 0
        if tzo is not None:
            try:
                # browser->python conversion: min->ms, reverse sign
                self._timezoneOffset = -int(tzo) * 60 * 1000
            except ValueError:
                self._timezoneOffset = 0  # default gmt+0
        if rtzo is not None:
            try:
                # browser->python conversion: min->ms, reverse sign
                self._rawTimezoneOffset = -int(rtzo) * 60 * 1000
            except ValueError:
                self._rawTimezoneOffset = 0  # default gmt+0
        if dstSavings is not None:
            try:
                # browser->python conversion: min->ms
                self._dstSavings = int(dstSavings) * 60 * 1000
            except ValueError:
                self._dstSavings = 0  # default no savings

        if dstInEffect is not None:
            self._dstInEffect = bool(dstInEffect)

        if curDate is not None:
            try:
                curTime = int(curDate)
                self._clientServerTimeDelta = curTime - time()
            except ValueError:
                self._clientServerTimeDelta = 0

        self._touchDevice = touchDevice


    def updateRequestDetails(self, locale, address, secureConnection, agent):
        """For internal use by AbstractApplicationServlet only. Updates all
        properties in the class according to the given information.

        @param locale:
                   The browser primary locale
        @param address:
                   The browser ip address
        @param secureConnection:
                   true if using an https connection
        @param agent:
                   Raw userAgent string from the browser
        """
        self._locale = locale
        self._address = address
        self._secureConnection = secureConnection
        if agent is not None:
            self._browserApplication = agent
            self._browserDetails = VBrowserDetails(agent)
