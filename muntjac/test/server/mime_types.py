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

from muntjac.application import Application
from muntjac.ui.embedded import Embedded
from muntjac.terminal.class_resource import ClassResource


class TestMimeTypes(TestCase):

    def testEmbeddedPDF(self):

        class app(Application):

            def init(self):
                pass

        e = Embedded('A pdf', ClassResource('file.pddf', app()))
        self.assertEquals('application/octet-stream', e.getMimeType(),
                'Invalid mimetype')

        e = Embedded('A pdf', ClassResource('file.pdf', app()))
        self.assertEquals('application/pdf', e.getMimeType(),
                'Invalid mimetype')
