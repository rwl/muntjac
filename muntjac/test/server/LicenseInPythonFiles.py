# Copyright (C) 2010 IT Mill Ltd.
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

from os import listdir
from os.path import exists, isdir, join, dirname

from unittest import TestCase

import muntjac


class LicenseInPythonFiles(TestCase):

    # The tests are run in the build directory.
    SRC_DIR = join(dirname(muntjac.__file__), '..')

    def testPythonFilesContainsLicense(self):
        srcDir = self.SRC_DIR
        print __file__
        missing = set()
        self.checkForLicense(srcDir, missing)
        if len(missing) > 0:
            raise RuntimeError, ('The following files are missing license '
                    'information:\n' + str(missing))


    def checkForLicense(self, srcDir, missing):
        self.assertTrue('Source directory ' + srcDir + ' does not exist',
                exists(srcDir))
        for f in listdir(srcDir):
            if isdir(f):
                self.checkForLicense(f, missing)
            elif f.endswith('.py'):
                self.checkForLicenseInFile(f, missing)


    def checkForLicenseInFile(self, f, missing):
        fd = open(f, 'rb')
        contents = fd.read()
        if ('@' + 'ITMillApache2LicenseForJavaFiles' + '@') not in contents:
            missing.add(f)
