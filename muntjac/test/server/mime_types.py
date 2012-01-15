# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

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
