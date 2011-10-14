# -*- coding: utf-8 -*-
# from com.vaadin.service.FileTypeResolver import (FileTypeResolver,)
# from junit.framework.TestCase import (TestCase,)


class TestFileTypeResolver(TestCase):
    _FLASH_MIME_TYPE = 'application/x-shockwave-flash'
    _TEXT_MIME_TYPE = 'text/plain'
    _HTML_MIME_TYPE = 'text/html'

    def testMimeTypes(self):
        plainFlash = File('MyFlash.swf')
        plainText = File('/a/b/MyFlash.txt')
        plainHtml = File('c:\\MyFlash.html')
        # Flash
        self.assertEquals(FileTypeResolver.getMIMEType(plainFlash.getAbsolutePath()), self._FLASH_MIME_TYPE)
        self.assertEquals(FileTypeResolver.getMIMEType(plainFlash.getAbsolutePath() + '?param1=value1'), self._FLASH_MIME_TYPE)
        self.assertEquals(FileTypeResolver.getMIMEType(plainFlash.getAbsolutePath() + '?param1=value1&param2=value2'), self._FLASH_MIME_TYPE)
        # Plain text
        self.assertEquals(FileTypeResolver.getMIMEType(plainText.getAbsolutePath()), self._TEXT_MIME_TYPE)
        self.assertEquals(FileTypeResolver.getMIMEType(plainText.getAbsolutePath() + '?param1=value1'), self._TEXT_MIME_TYPE)
        self.assertEquals(FileTypeResolver.getMIMEType(plainText.getAbsolutePath() + '?param1=value1&param2=value2'), self._TEXT_MIME_TYPE)
        # Plain text
        self.assertEquals(FileTypeResolver.getMIMEType(plainHtml.getAbsolutePath()), self._HTML_MIME_TYPE)
        self.assertEquals(FileTypeResolver.getMIMEType(plainHtml.getAbsolutePath() + '?param1=value1'), self._HTML_MIME_TYPE)
        self.assertEquals(FileTypeResolver.getMIMEType(plainHtml.getAbsolutePath() + '?param1=value1&param2=value2'), self._HTML_MIME_TYPE)
        # Filename missing
        self.assertEquals(FileTypeResolver.DEFAULT_MIME_TYPE, FileTypeResolver.getMIMEType(''))
        self.assertEquals(FileTypeResolver.DEFAULT_MIME_TYPE, FileTypeResolver.getMIMEType('?param1'))

    def testExtensionCase(self):
        self.assertEquals('image/jpeg', FileTypeResolver.getMIMEType('abc.jpg'))
        self.assertEquals('image/jpeg', FileTypeResolver.getMIMEType('abc.jPg'))
        self.assertEquals('image/jpeg', FileTypeResolver.getMIMEType('abc.JPG'))
        self.assertEquals('image/jpeg', FileTypeResolver.getMIMEType('abc.JPEG'))
        self.assertEquals('image/jpeg', FileTypeResolver.getMIMEType('abc.Jpeg'))
        self.assertEquals('image/jpeg', FileTypeResolver.getMIMEType('abc.JPE'))

    def testCustomMimeType(self):
        self.assertEquals(FileTypeResolver.DEFAULT_MIME_TYPE, FileTypeResolver.getMIMEType('vaadin.foo'))
        FileTypeResolver.addExtension('foo', 'Vaadin Foo/Bar')
        FileTypeResolver.addExtension('FOO2', 'Vaadin Foo/Bar2')
        self.assertEquals('Vaadin Foo/Bar', FileTypeResolver.getMIMEType('vaadin.foo'))
        self.assertEquals('Vaadin Foo/Bar2', FileTypeResolver.getMIMEType('vaadin.Foo2'))
