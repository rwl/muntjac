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
