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

from os import listdir
from os.path import exists, isdir, join, dirname

from unittest import TestCase

import muntjac


class LicenseInPythonFiles(TestCase):

    # The tests are run in the build directory.
    SRC_DIR = dirname(muntjac.__file__)

    def testPythonFilesContainsLicense(self):
        srcDir = self.SRC_DIR
        missing = set()
        self.checkForLicense(srcDir, missing)
        self.assertEquals(len(missing), 0, 'The following files are missing '
                    'license information:\n' + '\n'.join(missing))


    def checkForLicense(self, srcDir, missing):
        self.assertTrue('Source directory ' + srcDir + ' does not exist',
                exists(srcDir))
        for f in listdir(srcDir):
            if isdir(f):
                self.checkForLicense(join(srcDir, f), missing)
            elif f.endswith('.py'):
                self.checkForLicenseInFile(join(srcDir, f), missing)


    def checkForLicenseInFile(self, f, missing):
        fd = None
        try:
            fd = open(f, 'rb')
            contents = fd.read()
            if ('Apache License, Version 2.0') not in contents:
                missing.add(f)
        finally:
            if fd is not None:
                fd.close()
