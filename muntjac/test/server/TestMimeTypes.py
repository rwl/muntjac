# -*- coding: utf-8 -*-
# from com.vaadin.Application import (Application,)
# from com.vaadin.terminal.ClassResource import (ClassResource,)
# from com.vaadin.ui.Embedded import (Embedded,)
# from junit.framework.TestCase import (TestCase,)


class TestMimeTypes(TestCase):

    def testEmbeddedPDF(self):

        class app(Application):

            def init(self):
                # TODO Auto-generated method stub
                pass

        e = Embedded('A pdf', ClassResource('file.pddf', app))
        self.assertEquals('Invalid mimetype', 'application/octet-stream', e.getMimeType())
        e = Embedded('A pdf', ClassResource('file.pdf', app))
        self.assertEquals('Invalid mimetype', 'application/pdf', e.getMimeType())
