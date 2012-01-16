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

"""Defines a class that parses the user agent string from the browser and
provides information about the browser."""

import re


class VBrowserDetails(object):
    """Class that parses the user agent string from the browser and provides
    information about the browser. Used internally by L{BrowserInfo} and
    L{WebBrowser}. Should not be used directly.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, userAgent):
        """Create an instance based on the given user agent.

        @param userAgent:
                   User agent as provided by the browser.
        """
        self._isGecko = False
        self._isWebKit = False
        self._isPresto = False
        self._isSafari = False
        self._isChrome = False
        self._isFirefox = False
        self._isOpera = False
        self._isIE = False
        self._isWindows = False
        self._isMacOSX = False
        self._isLinux = False
        self._browserEngineVersion = -1
        self._browserMajorVersion = -1
        self._browserMinorVersion = -1

        userAgent = userAgent.lower()

        # browser engine name
        self._isGecko = (userAgent.find('gecko') != -1
                and userAgent.find('webkit') == -1)
        self._isWebKit = userAgent.find('applewebkit') != -1
        self._isPresto = userAgent.find(' presto/') != -1
        # browser name
        self._isChrome = userAgent.find(' chrome/') != -1
        self._isSafari = ((not self._isChrome)
                and userAgent.find('safari') != -1)
        self._isOpera = userAgent.find('opera') != -1
        self._isIE = (userAgent.find('msie') != -1
                and (not self._isOpera)
                and userAgent.find('webtv') == -1)
        self._isFirefox = userAgent.find(' firefox/') != -1

        # Rendering engine version
        try:
            if self._isGecko:
                rvPos = userAgent.find('rv:')
                if rvPos >= 0:
                    tmp = userAgent[rvPos + 3:]
                    tmp = re.sub('(\\.[0-9]+).+', '\\1', tmp, count=1)
                    self._browserEngineVersion = float(tmp)
            elif self._isWebKit:
                tmp = userAgent[userAgent.find('webkit/') + 7:]
                tmp = re.sub('([0-9]+)[^0-9].+', '\\1', tmp, count=1)
                self._browserEngineVersion = float(tmp)
        except Exception:
            # Browser engine version parsing failed
            print 'Browser engine version parsing failed for: ' + userAgent

        # Browser version
        try:
            if self._isIE:
                ieVersionString = userAgent[userAgent.find('msie ') + 5:]
                ieVersionString = self.safeSubstring(ieVersionString, 0,
                        ieVersionString.find(';'))
                self.parseVersionString(ieVersionString)
            elif self._isFirefox:
                i = userAgent.find(' firefox/') + 9
                ver = self.safeSubstring(userAgent, i, i + 5)
                self.parseVersionString(ver)
            elif self._isChrome:
                i = userAgent.find(' chrome/') + 8
                ver = self.safeSubstring(userAgent, i, i + 5)
                self.parseVersionString(ver)
            elif self._isSafari:
                i = userAgent.find(' version/') + 9
                ver = self.safeSubstring(userAgent, i, i + 5)
                self.parseVersionString(ver)
            elif self._isOpera:
                i = userAgent.find(' version/')
                if i != -1:
                    # Version present in Opera 10 and newer
                    i += 9  # " version/".length
                else:
                    i = userAgent.find('opera/') + 6
                ver = self.safeSubstring(userAgent, i, i + 5)
                self.parseVersionString(ver)
        except Exception:
            # Browser version parsing failed
            print 'Browser version parsing failed for: ' + userAgent

        # Operating system
        if 'windows ' in userAgent:
            self._isWindows = True
        elif 'linux' in userAgent:
            self._isLinux = True
        elif 'macintosh' in userAgent \
                or 'mac osx' in userAgent \
                or 'mac os x' in userAgent:
            self._isMacOSX = True


    def parseVersionString(self, versionString):
        idx = versionString.find('.')
        if idx < 0:
            idx = len(versionString)

        ver = self.safeSubstring(versionString, 0, idx)
        self._browserMajorVersion = int(ver)

        idx2 = versionString.find('.', idx + 1)
        if idx2 < 0:
            idx2 = len(versionString)

        try:
            ver = self.safeSubstring(versionString, idx + 1, idx2)
            self._browserMinorVersion = \
                    int( re.sub('[^0-9].*', '', ver) )
        except ValueError:
            pass  # leave the minor version unmodified (-1 = unknown)


    def safeSubstring(self, string, beginIndex, endIndex):
        if beginIndex < 0:
            beginIndex = 0

        if endIndex < 0 or endIndex > len(string):
            endIndex = len(string)

        return string[beginIndex:endIndex]


    def isFirefox(self):
        """Tests if the browser is Firefox.

        @return: true if it is Firefox, false otherwise
        """
        return self._isFirefox


    def isGecko(self):
        """Tests if the browser is using the Gecko engine

        @return: true if it is Gecko, false otherwise
        """
        return self._isGecko


    def isWebKit(self):
        """Tests if the browser is using the WebKit engine

        @return: true if it is WebKit, false otherwise
        """
        return self._isWebKit


    def isPresto(self):
        """Tests if the browser is using the Presto engine

        @return: true if it is Presto, false otherwise
        """
        return self._isPresto


    def isSafari(self):
        """Tests if the browser is Safari.

        @return: true if it is Safari, false otherwise
        """
        return self._isSafari


    def isChrome(self):
        """Tests if the browser is Chrome.

        @return: true if it is Chrome, false otherwise
        """
        return self._isChrome


    def isOpera(self):
        """Tests if the browser is Opera.

        @return: true if it is Opera, false otherwise
        """
        return self._isOpera


    def isIE(self):
        """Tests if the browser is Internet Explorer.

        @return: true if it is Internet Explorer, false otherwise
        """
        return self._isIE


    def getBrowserEngineVersion(self):
        """Returns the version of the browser engine. For WebKit this is
        an integer e.g., 532.0. For gecko it is a float e.g., 1.8 or 1.9.

        @return: The version of the browser engine
        """
        return self._browserEngineVersion


    def getBrowserMajorVersion(self):
        """Returns the browser major version e.g., 3 for Firefox 3.5, 4 for
        Chrome 4, 8 for Internet Explorer 8.

        Note that Internet Explorer 8 and newer will return the document
        mode so IE8 rendering as IE7 will return 7.

        @return: The major version of the browser.
        """
        return self._browserMajorVersion


    def getBrowserMinorVersion(self):
        """Returns the browser minor version e.g., 5 for Firefox 3.5.

        @see: #getBrowserMajorVersion()

        @return: The minor version of the browser, or -1 if not known/parsed.
        """
        return self._browserMinorVersion


    def setIEMode(self, documentMode):
        """Sets the version for IE based on the documentMode. This is used
        to return the correct the correct IE version when the version from
        the user agent string and the value of the documentMode property do
        not match.

        @param documentMode:
                   The current document mode
        """
        self._browserMajorVersion = documentMode
        self._browserMinorVersion = 0


    def isWindows(self):
        """Tests if the browser is run on Windows.

        @return: true if run on Windows, false otherwise
        """
        return self._isWindows


    def isMacOSX(self):
        """Tests if the browser is run on Mac OSX.

        @return: true if run on Mac OSX, false otherwise
        """
        return self._isMacOSX


    def isLinux(self):
        """Tests if the browser is run on Linux.

        @return: true if run on Linux, false otherwise
        """
        return self._isLinux
