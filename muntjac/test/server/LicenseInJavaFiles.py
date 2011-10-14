# -*- coding: utf-8 -*-
# from java.io.FileInputStream import (FileInputStream,)
# from java.util.HashSet import (HashSet,)
# from junit.framework.Assert import (Assert,)
# from junit.framework.TestCase import (TestCase,)
# from org.apache.commons.io.IOUtils import (IOUtils,)


class LicenseInJavaFiles(TestCase):
    # The tests are run in the build directory.
    SRC_DIR = '../src'

    def testJavaFilesContainsLicense(self):
        srcDir = File(self.SRC_DIR)
        print File('.').getAbsolutePath()
        missing = set()
        self.checkForLicense(srcDir, missing)
        if not missing.isEmpty():
            raise RuntimeError('The following files are missing license information:\n' + str(missing))

    def checkForLicense(self, srcDir, missing):
        Assert.assertTrue('Source directory ' + srcDir + ' does not exist', srcDir.exists())
        for f in srcDir.listFiles():
            if f.isDirectory():
                self.checkForLicense(f, missing)
            elif f.getName().endswith('.java'):
                self.checkForLicenseInFile(f, missing)

    def checkForLicenseInFile(self, f, missing):
        contents = str(FileInputStream(f))
        if not contents.contains('@' + 'ITMillApache2LicenseForJavaFiles' + '@'):
            missing.add(f.getPath())
