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

from unittest import TestCase

from muntjac.service.file_type_resolver import FileTypeResolver


class TestFileTypeResolver(TestCase):

    _FLASH_MIME_TYPE = 'application/x-shockwave-flash'

    _TEXT_MIME_TYPE = 'text/plain'

    _HTML_MIME_TYPE = 'text/html'

    def testMimeTypes(self):
        plainFlash = 'MyFlash.swf'
        plainText = '/a/b/MyFlash.txt'
        plainHtml = 'c:\\MyFlash.html'

        # Flash
        self.assertEquals(FileTypeResolver.getMIMEType(plainFlash),
                self._FLASH_MIME_TYPE)
        self.assertEquals(FileTypeResolver.getMIMEType((plainFlash +
                '?param1=value1')), self._FLASH_MIME_TYPE)
        self.assertEquals(FileTypeResolver.getMIMEType((plainFlash +
                '?param1=value1&param2=value2')), self._FLASH_MIME_TYPE)

        # Plain text
        self.assertEquals(FileTypeResolver.getMIMEType(plainText),
                self._TEXT_MIME_TYPE)
        self.assertEquals(FileTypeResolver.getMIMEType((plainText +
                '?param1=value1')), self._TEXT_MIME_TYPE)
        self.assertEquals(FileTypeResolver.getMIMEType((plainText +
                '?param1=value1&param2=value2')), self._TEXT_MIME_TYPE)

        # Plain text
        self.assertEquals(FileTypeResolver.getMIMEType(plainHtml),
                self._HTML_MIME_TYPE)
        self.assertEquals(FileTypeResolver.getMIMEType((plainHtml +
                '?param1=value1')), self._HTML_MIME_TYPE)
        self.assertEquals(FileTypeResolver.getMIMEType((plainHtml +
                '?param1=value1&param2=value2')), self._HTML_MIME_TYPE)

        # Filename missing
        self.assertEquals(FileTypeResolver.DEFAULT_MIME_TYPE,
                FileTypeResolver.getMIMEType(''))
        self.assertEquals(FileTypeResolver.DEFAULT_MIME_TYPE,
                FileTypeResolver.getMIMEType('?param1'))


    def testExtensionCase(self):
        self.assertEquals('image/jpeg',
                FileTypeResolver.getMIMEType('abc.jpg'))
        self.assertEquals('image/jpeg',
                FileTypeResolver.getMIMEType('abc.jPg'))
        self.assertEquals('image/jpeg',
                FileTypeResolver.getMIMEType('abc.JPG'))
        self.assertEquals('image/jpeg',
                FileTypeResolver.getMIMEType('abc.JPEG'))
        self.assertEquals('image/jpeg',
                FileTypeResolver.getMIMEType('abc.Jpeg'))
        self.assertEquals('image/jpeg',
                FileTypeResolver.getMIMEType('abc.JPE'))


    def testCustomMimeType(self):
        self.assertEquals(FileTypeResolver.DEFAULT_MIME_TYPE,
                FileTypeResolver.getMIMEType('muntjac.foo'))

        FileTypeResolver.addExtension('foo', 'Muntjac Foo/Bar')
        FileTypeResolver.addExtension('FOO2', 'Muntjac Foo/Bar2')

        self.assertEquals('Muntjac Foo/Bar',
                FileTypeResolver.getMIMEType('muntjac.foo'))

        self.assertEquals('Muntjac Foo/Bar2',
                FileTypeResolver.getMIMEType('muntjac.Foo2'))
