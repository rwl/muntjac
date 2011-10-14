# -*- coding: utf-8 -*-
# from java.io.File import (File,)
# from java.io.IOException import (IOException,)
# from java.io.Serializable import (Serializable,)
# from java.lang.reflect.Method import (Method,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Collection import (Collection,)
# from java.util.Collections import (Collections,)
# from java.util.Enumeration import (Enumeration,)
# from java.util.Iterator import (Iterator,)
# from java.util.List import (List,)
# from java.util.jar.JarEntry import (JarEntry,)
# from java.util.jar.JarFile import (JarFile,)
# from junit.framework.TestCase import (TestCase,)
# from org.junit.Test import (Test,)


class TestClassesSerializable(TestCase):
    # JARs that will be scanned for classes to test, in addition to classpath
    # directories.

    _JAR_PATTERN = '.*vaadin.*\\.jar'
    _BASE_PACKAGES = ['com.vaadin']
    _EXCLUDED_PATTERNS = ['com\\.vaadin\\.demo\\..*', 'com\\.vaadin\\.external\\.org\\.apache\\.commons\\.fileupload\\..*', 'com\\.vaadin\\.launcher\\..*', 'com\\.vaadin\\.terminal\\.gwt\\.client\\..*', 'com\\.vaadin\\.terminal\\.gwt\\.widgetsetutils\\..*', 'com\\.vaadin\\.tests\\..*', 'com\\.vaadin\\.tools\\..*', 'com\\.vaadin\\.ui\\.themes\\..*', 'com\\.vaadin\\.event\\.FieldEvents', 'com\\.vaadin\\.event\\.LayoutEvents', 'com\\.vaadin\\.event\\.MouseEvents', 'com\\.vaadin\\.terminal\\.gwt\\.server\\.AbstractApplicationPortlet', 'com\\.vaadin\\.terminal\\.gwt\\.server\\.ApplicationPortlet2', 'com\\.vaadin\\.terminal\\.gwt\\.server\\.Constants', 'com\\.vaadin\\.util\\.SerializerHelper', 'com\\.vaadin\\.terminal\\.gwt\\.server\\.AbstractCommunicationManager.*', 'com\\.vaadin\\.terminal\\.gwt\\.server\\.ApplicationRunnerServlet.*', 'com\\.vaadin\\.terminal\\.gwt\\.server\\.CommunicationManager.*', 'com\\.vaadin\\.terminal\\.gwt\\.server\\.PortletCommunicationManager.*']

    def testClassesSerializable(self):
        """Tests that all the relevant classes and interfaces under
        {@link #BASE_PACKAGES} implement Serializable.

        @throws Exception
        """
        rawClasspathEntries = self.getRawClasspathEntries()
        classes = list()
        for location in rawClasspathEntries:
            classes.addAll(self.findServerClasses(location))
        nonSerializableClasses = list()
        for className in classes:
            cls = (lambda x: getattr(__import__(x.rsplit('.', 1)[0], fromlist=x.rsplit('.', 1)[0]), x.split('.')[-1]))(className)
            # skip annotations and synthetic classes
            if cls.isAnnotation() or cls.isSynthetic():
                continue
            # Don't add classes that have a @Test annotation on any methods
            testPresent = False
            for method in cls.getMethods():
                if method.isAnnotationPresent(Test):
                    testPresent = True
                    break
            if testPresent:
                continue
            # report non-serializable classes and interfaces
            if not Serializable.isAssignableFrom(cls):
                nonSerializableClasses.add(cls)
                # TODO easier to read when testing
                # System.err.println(cls);
        # useful failure message including all non-serializable classes and
        # interfaces
        if not nonSerializableClasses.isEmpty():
            nonSerializableString = ''
            it = nonSerializableClasses
            nonSerializableString = it.next().getName()
            while it.hasNext():
                nonSerializableString += ', ' + it.next().getName()
            self.fail('Serializable not implemented by the following classes and interfaces: ' + nonSerializableString)

    @classmethod
    def getRawClasspathEntries(cls):
        """Lists all class path entries by splitting the class path string.

        Adapted from ClassPathExplorer.getRawClasspathEntries(), but without
        filtering.

        @return List of class path segment strings
        """
        # try to keep the order of the classpath
        locations = list()
        pathSep = System.getProperty('path.separator')
        classpath = System.getProperty('java.class.path')
        if classpath.startswith('\"'):
            classpath = classpath[1:]
        if classpath.endswith('\"'):
            classpath = classpath[:-1]
        split = classpath.split(pathSep)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(split)):
                break
            classpathEntry = split[i]
            locations.add(classpathEntry)
        return locations

    def findServerClasses(self, classpathEntry):
        """Finds the server side classes/interfaces under a class path entry -
        either a directory or a JAR that matches {@link #JAR_PATTERN}.

        Only classes under {@link #BASE_PACKAGES} are considered, and those
        matching {@link #EXCLUDED_PATTERNS} are filtered out.

        @param classpathEntry
        @return
        @throws IOException
        """
        classes = list()
        file = File(classpathEntry)
        if file.isDirectory():
            classes = self.findClassesInDirectory(None, file)
        elif file.getName().matches(self._JAR_PATTERN):
            classes = self.findClassesInJar(file)
        else:
            print 'Ignoring ' + classpathEntry
            return Collections.emptyList()
        filteredClasses = list()
        for className in classes:
            ok = False
            for basePackage in self._BASE_PACKAGES:
                if className.startswith(basePackage + '.'):
                    ok = True
                    break
            for excludedPrefix in self._EXCLUDED_PATTERNS:
                if className.matches(excludedPrefix):
                    ok = False
                    break
            # Don't add test classes
            if className.contains('Test'):
                ok = False
            if ok:
                filteredClasses.add(className)
        return filteredClasses

    def findClassesInJar(self, file):
        """Lists class names (based on .class files) in a JAR file.

        @param file
                   a valid JAR file
        @return collection of fully qualified class names in the JAR
        @throws IOException
        """
        classes = list()
        jar = JarFile(file)
        e = jar.entries()
        while e.hasMoreElements():
            entry = e.nextElement()
            if entry.getName().endswith('.class'):
                nameWithoutExtension = entry.getName().replaceAll('\\.class', '')
                className = nameWithoutExtension.replace('/', '.')
                classes.add(className)
        return classes

    @classmethod
    def findClassesInDirectory(cls, parentPackage, parent):
        """Lists class names (based on .class files) in a directory (a package path
        root).

        @param parentPackage
                   parent package name or null at root of hierarchy, used by
                   recursion
        @param parent
                   File representing the directory to scan
        @return collection of fully qualified class names in the directory
        """
        if parent.isHidden() or parent.getPath().contains(File.separator + '.'):
            return Collections.emptyList()
        if parentPackage is None:
            parentPackage = ''
        else:
            parentPackage += '.'
        classNames = list()
        # add all directories recursively
        files = parent.listFiles()
        for child in files:
            if child.isDirectory():
                classNames.addAll(cls.findClassesInDirectory(parentPackage + child.getName(), child))
            elif child.getName().endswith('.class'):
                classNames.add(parentPackage.replace(File.separatorChar, '.') + child.getName().replaceAll('\\.class', ''))
        return classNames
