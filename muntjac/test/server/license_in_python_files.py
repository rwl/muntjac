# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

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
