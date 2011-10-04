
from muntjac.ui import VerticalLayout, Label


class BrowserInformationExample(VerticalLayout):

    def __init__(self):
        # We use the attach method in this example because getApplication()
        # will return null until the example is attached to the application. In
        # an application you would typically have an application reference to
        # use.
        self._populated = False


    def attach(self):
        if self._populated:
            # Only populate the layout once
            return

        # Find the context we are running in and get the browser information
        # from that.
        context = self.getApplication().getContext()
        webBrowser = context.getBrowser()

        # Create a text to show based on the browser.
        browserText = self.getBrowserAndVersion(webBrowser)
        browserText = browserText + ' in ' + self.getOperatingSystem(webBrowser)

        # Create labels for the information and add them to the application
        ipAddresslabel = Label("Hello user from <b>"
                + webBrowser.getAddress() + "</b>.", Label.CONTENT_XHTML)
        browser = Label("You are running <b>"
                + browserText + "</b>.", Label.CONTENT_XHTML)
        screenSize = Label("Your screen resolution is <b>"
                + webBrowser.getScreenWidth() + "x"
                + webBrowser.getScreenHeight() + "</b>.", Label.CONTENT_XHTML)
        locale = Label("Your browser is set to primarily use the <b>"
                + webBrowser.getLocale() + "</b> locale.", Label.CONTENT_XHTML)

        # FIXME: timezones
#        timeZones = NativeSelect()
#        # Client timezone offset w/o possible DST:
#        rtzOffset = webBrowser.getRawTimezoneOffset()
#        # DST:
#        dst = webBrowser.getDSTSavings()
#        # use raw offset to get possible TZ:
#        tzs = TimeZone.getAvailableIDs(rtzOffset)
#        for id in tzs:
#            tz = TimeZone.getTimeZone(id)
#            if dst == tz.getDSTSavings():
#                # only include zones w/ DST if we know we have DST
#                caption = id + ' (' + tz.getDisplayName() + ')'
#                timeZones.addItem(caption)
#                if timeZones.getValue() is None:
#                    # select first
#                    timeZones.setValue(caption)
#
#        timeZones.setImmediate(True)
#        timeZones.setNullSelectionAllowed(False)
#        timeZones.setCaption(self.getTimeZoneInfoString(webBrowser))

        self.addComponent(ipAddresslabel)
        self.addComponent(browser)
        self.addComponent(screenSize)
        self.addComponent(locale)
#        self.addComponent(timeZones)

        self._populated = True


    def getTimeZoneInfoString(self, webBrowser):
        # Client timezone offset:
        tzOffset = webBrowser.getTimezoneOffset()
        infoStr = 'Your browser indicates GMT%s%d' % \
                ('-' if tzOffset < 0 else '+', abs(self.tzoToHours(tzOffset)))
        if webBrowser.isDSTInEffect():
            infoStr += ' and DST %d' % \
                    self.tzoToHours(webBrowser.getDSTSavings())
        return infoStr + ', which could mean:'


    @classmethod
    def tzoToHours(cls, ms):
        return ms / 1000 / 60 / 60


    def getOperatingSystem(self, webBrowser):
        if webBrowser.isWindows():
            return 'Windows'
        elif webBrowser.isMacOSX():
            return 'Mac OSX'
        elif webBrowser.isLinux():
            return 'Linux'
        else:
            return 'an unknown operating system'


    def getBrowserAndVersion(self, webBrowser):
        if webBrowser.isChrome():
            return ('Chrome ' + webBrowser.getBrowserMajorVersion()
                    + '.' + webBrowser.getBrowserMinorVersion())
        elif webBrowser.isOpera():
            return ('Opera ' + webBrowser.getBrowserMajorVersion()
                    + '.' + webBrowser.getBrowserMinorVersion())
        elif webBrowser.isFirefox():
            return ('Firefox ' + webBrowser.getBrowserMajorVersion()
                    + '.' + webBrowser.getBrowserMinorVersion())
        elif webBrowser.isSafari():
            return ('Safari ' + webBrowser.getBrowserMajorVersion()
                    + '.' + webBrowser.getBrowserMinorVersion())
        elif webBrowser.isIE():
            return 'Internet Explorer ' + webBrowser.getBrowserMajorVersion()
        else:
            return 'an unknown browser'
