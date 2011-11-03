
try:
    from cStringIO import StringIO
except ImportError, e:
    from StringIO import StringIO

from muntjac.demo.sampler.FeatureSet import FeatureSet


class TestRow(object):

    def getHtml(self):
        pass


class Comment(TestRow):

    def __init__(self, comment):
        self._comment = comment

    def getHtml(self):
        return '<!--' + self._comment + '-->\n'


class Command(TestRow):

    def __init__(self, cmd, target, value):
        super(Command, self).__init__()
        self._cmd = cmd
        self._target = target
        self._value = value

    def getHtml(self):
        return ('<tr>\n' + '<td>' + self._cmd + '</td>\n'
            + '<td>' + self._target + '</td>\n' + '<td>'
            + self._value + '</td>\n' + '</tr>\n')


class WaitForMuntjacCommand(Command):

    def __init__(self):
        super(WaitForMuntjacCommand, self).__init__('waitForMuntjac', '', '')


class MuntjacTestBenchTest(object):

    _header = ('<?xml version=\"1.0\" encoding=\"UTF-8\"?>'
        + '<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">'
        + '<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"en\" lang=\"en\">'
        + '<head profile=\"http://selenium-ide.openqa.org/profiles/test-case\">'
        + '<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />'
        + '<link rel=\"selenium.base\" href=\"\" />'
        + '<title>#name#</title>'
        + '</head>'
        + '<body>'
        + '<table cellpadding=\"1\" cellspacing=\"1\" border=\"1\">'
        + '<thead>'
        + '<tr><td rowspan=\"1\" colspan=\"3\">#name#</td></tr>'
        + '</thead><tbody>')

    _footer = '</tbody></table>' + '</body>' + '</html>'

    def __init__(self, name):
        self._name = name
        self._rows = list()


    def addCmd(self, cmd, target, value):
        self._rows.add(Command(cmd, target, value))


    def addComment(self, comment):
        self._rows.add(Comment(comment))


    def output(self):
        print self._header.replace('#name#', self._name)
        for row in self._rows:
            print row.getHtml()
        print self._footer.replace('#name#', self._name)


class GenerateSamplerTest(object):

    _NEXT_BUTTON = 'vaadin=sampler::/VVerticalLayout[0]/ChildComponentContainer[0]/VHorizontalLayout[0]/ChildComponentContainer[6]/VHorizontalLayout[0]/ChildComponentContainer[1]/VNativeButton[0]'

    _test = None

    @classmethod
    def main(cls):
        cls._test = MuntjacTestBenchTest('sampler-all-samples')
        cls._test.addCmd('openAndWait', '/', '')
        cls._test.addComment('Open sampler from demo page')
        cls._test.addCmd('mouseClickAndWait', '//div[@id=\'sampler\']/a/strong', '96,14')
        cls._test.addComment('Close left side tree menu')
        cls._test.addCmd('mouseClick', 'vaadin=sampler::/VVerticalLayout[0]/ChildComponentContainer[0]/VHorizontalLayout[0]/ChildComponentContainer[5]/VHorizontalLayout[0]/ChildComponentContainer[1]/VNativeButton[0]', '22,11')
        cls._test.addComment('Main page screenshot')
        cls._test.addCmd('pause', '5000', '')
        cls._test.addCmd('screenCapture', '', 'mainview')
        script = StringIO()
        cls._test.addComment('Scrolling through all samples to load images')
        samplerFeatureSet = FeatureSet.FEATURES
        cls.writeFeatureSet(script, samplerFeatureSet, False)
        cls._test.addComment('Start over from the main page')
        cls._test.addCmd('mouseClick', 'vaadin=sampler::/VVerticalLayout[0]/ChildComponentContainer[0]/VHorizontalLayout[0]/ChildComponentContainer[1]/VCustomComponent[0]/VHorizontalLayout[0]/ChildComponentContainer[0]/VActiveLink[0]/domChild[0]/domChild[0]', '1,1')
        cls._test.addComment('Scroll through all samples in order and capture screenshots')
        cls.writeFeatureSet(script, samplerFeatureSet, True)
        cls._test.output()

    @classmethod
    def writeFeatureSet(cls, script, featureSet, capture):
        for feature in featureSet.getFeatures():
            if isinstance(feature, FeatureSet):
                cls.writeFeatureSet(script, feature, capture)
            else:
                cls.writeFeature(script, feature, capture)

    @classmethod
    def writeFeature(cls, script, feature, capture):
        cls._test.addCmd('mouseClick', cls._NEXT_BUTTON, '1,1')
        if capture:
            idd = cls.getId(feature)
            cls._test.addComment(idd)
            if cls.includeScreenshotInTest(idd):
                if cls.needsPause(feature):
                    cls._test.addCmd('pause', '1000', '')
                if feature.getFragmentName().endswith('PackageIcons'):
                    # Firefox3, sometimes you disappoint me
                    cls._test.addCmd('pause', '3000', '')
                cls._test.addCmd('screenCapture', '', idd)

    @classmethod
    def includeScreenshotInTest(cls, idd):
        if idd.startswith('Date'):
            return False
        if idd == 'BrowserInformation':
            return False
        if idd == 'WebEmbed':
            return False
        if idd == 'JSApi':
            return False
        return True

    @classmethod
    def needsPause(cls, feature):
        if feature.getFragmentName().endswith('Embed'):
            return True
        # the previous test (drag and drop files) may leave a notification open
        if feature.getFragmentName().endswith('LayoutMargin'):
            return True
        if feature.getFragmentName().endswith('LoginForm'):
            return True
        if feature.getFragmentName().endswith('PackageIcons'):
            return True
        return False

    @classmethod
    def getId(cls, feature):
        # Sampler changed so that FragmentName is unique
        return feature.getFragmentName()


if __name__ == '__main__':
    GenerateSamplerTest.main()
