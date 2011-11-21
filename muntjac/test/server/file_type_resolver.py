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
