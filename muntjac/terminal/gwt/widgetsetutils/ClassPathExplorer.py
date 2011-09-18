# Copyright (C) 2011 Vaadin Ltd
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

from com.vaadin.terminal.gwt.widgetsetutils.WidgetSetBuilder import (WidgetSetBuilder,)
# from java.io.File import (File,)
# from java.io.FileFilter import (FileFilter,)
# from java.io.IOException import (IOException,)
# from java.io.OutputStream import (OutputStream,)
# from java.io.PrintStream import (PrintStream,)
# from java.net.JarURLConnection import (JarURLConnection,)
# from java.net.MalformedURLException import (MalformedURLException,)
# from java.net.URL import (URL,)
# from java.net.URLConnection import (URLConnection,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Collection import (Collection,)
# from java.util.Enumeration import (Enumeration,)
# from java.util.HashMap import (HashMap,)
# from java.util.HashSet import (HashSet,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedHashMap import (LinkedHashMap,)
# from java.util.List import (List,)
# from java.util.Map import (Map,)
# from java.util.Set import (Set,)
# from java.util.jar.Attributes import (Attributes,)
# from java.util.jar.JarEntry import (JarEntry,)
# from java.util.jar.JarFile import (JarFile,)
# from java.util.jar.Manifest import (Manifest,)
# from java.util.logging.Level import (Level,)
# from java.util.logging.Logger import (Logger,)
import time
import sys


class ClassPathExplorer(object):
    """Utility class to collect widgetset related information from classpath.
    Utility will seek all directories from classpaths, and jar files having
    "Vaadin-Widgetsets" key in their manifest file.
    <p>
    Used by WidgetMapGenerator and ide tools to implement some monkey coding for
    you.
    <p>
    Developer notice: If you end up reading this comment, I guess you have faced
    a sluggish performance of widget compilation or unreliable detection of
    components in your classpaths. The thing you might be able to do is to use
    annotation processing tool like apt to generate the needed information. Then
    either use that information in {@link WidgetMapGenerator} or create the
    appropriate monkey code for gwt directly in annotation processor and get rid
    of {@link WidgetMapGenerator}. Using annotation processor might be a good
    idea when dropping Java 1.5 support (integrated to javac in 6).
    """
    _logger = Logger.getLogger(ClassPathExplorer.getName())
    _VAADIN_ADDON_VERSION_ATTRIBUTE = 'Vaadin-Package-Version'
    # File filter that only accepts directories.

    class DIRECTORIES_ONLY(FileFilter):

        def accept(self, f):
            if f.exists() and f.isDirectory():
                return True
            else:
                return False

    # Raw class path entries as given in the java class path string. Only
    # entries that could include widgets/widgetsets are listed (primarily
    # directories, Vaadin JARs and add-on JARs).

    _rawClasspathEntries = getRawClasspathEntries()
    # Map from identifiers (either a package name preceded by the path and a
    # slash, or a URL for a JAR file) to the corresponding URLs. This is
    # constructed from the class path.

    _classpathLocations = getClasspathLocations(_rawClasspathEntries)

    def __init__(self):
        """No instantiation from outside, callable methods are static."""
        pass

    @classmethod
    def getPaintablesHavingWidgetAnnotation(cls):
        """Finds server side widgets with {@link ClientWidget} annotation on the
        class path (entries that can contain widgets/widgetsets - see
        {@link #getRawClasspathEntries()}).

        As a side effect, also accept criteria are searched under the same class
        path entries and added into the acceptCriterion collection.

        @return a collection of {@link Paintable} classes
        """
        cls._logger.info('Searching for paintables..')
        start = 1000 * time.time()
        paintables = set()
        keySet = cls._classpathLocations.keys()
        for url in keySet:
            cls._logger.fine('Searching for paintables in ' + cls._classpathLocations[url])
            cls.searchForPaintables(cls._classpathLocations[url], url, paintables)
        end = 1000 * time.time()
        cls._logger.info('Search took ' + (end - start) + 'ms')
        return paintables

    @classmethod
    def getCriterion(cls):
        """Finds all accept criteria having client side counterparts (classes with
        the {@link ClientCriterion} annotation).

        @return Collection of AcceptCriterion classes
        """
        if cls._acceptCriterion.isEmpty():
            # accept criterion are searched as a side effect, normally after
            # paintable detection
            cls.getPaintablesHavingWidgetAnnotation()
        return cls._acceptCriterion

    @classmethod
    def getAvailableWidgetSets(cls):
        """Finds the names and locations of widgetsets available on the class path.

        @return map from widgetset classname to widgetset location URL
        """
        start = 1000 * time.time()
        widgetsets = dict()
        keySet = cls._classpathLocations.keys()
        for location in keySet:
            cls.searchForWidgetSets(location, widgetsets)
        end = 1000 * time.time()
        sb = cls.StringBuilder()
        sb.append('Widgetsets found from classpath:\n')
        for ws in widgetsets.keys():
            sb.append('\t')
            sb.append(ws)
            sb.append(' in ')
            sb.append(widgetsets[ws])
            sb.append('\n')
        cls._logger.info(str(sb))
        cls._logger.info('Search took ' + (end - start) + 'ms')
        return widgetsets

    @classmethod
    def searchForWidgetSets(cls, locationString, widgetsets):
        """Finds all GWT modules / Vaadin widgetsets in a valid location.

        If the location is a directory, all GWT modules (files with the
        ".gwt.xml" extension) are added to widgetsets.

        If the location is a JAR file, the comma-separated values of the
        "Vaadin-Widgetsets" attribute in its manifest are added to widgetsets.

        @param locationString
                   an entry in {@link #classpathLocations}
        @param widgetsets
                   a map from widgetset name (including package, with dots as
                   separators) to a URL (see {@link #classpathLocations}) - new
                   entries are added to this map
        """
        location = cls._classpathLocations[locationString]
        directory = File(location.getFile())
        if directory.exists() and not directory.isHidden():
            # Get the list of the files contained in the directory
            files = directory.list()
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(files)):
                    break
                # we are only interested in .gwt.xml files
                if not files[i].endswith('.gwt.xml'):
                    continue
                # remove the .gwt.xml extension
                classname = files[i][:len(files[i]) - 8]
                packageName = locationString[locationString.rfind('/') + 1:]
                classname = packageName + '.' + classname
                if not WidgetSetBuilder.isWidgetset(classname):
                    # Only return widgetsets and not GWT modules to avoid
                    # comparing modules and widgetsets
                    continue
                if not (classname in widgetsets):
                    packagePath = packageName.replaceAll('\\.', '/')
                    basePath = location.getFile().replaceAll('/' + packagePath + '$', '')
                    # should never happen as based on an existing URL,
                    # only changing end of file name/path part
                    try:
                        url = URL(location.getProtocol(), location.getHost(), location.getPort(), basePath)
                        widgetsets.put(classname, url)
                    except MalformedURLException, e:
                        cls._logger.log(Level.SEVERE, 'Error locating the widgetset ' + classname, e)
        else:
            # check files in jar file, entries will list all directories
            # and files in jar
            try:
                openConnection = location.openConnection()
                if isinstance(openConnection, JarURLConnection):
                    conn = openConnection
                    jarFile = conn.getJarFile()
                    manifest = jarFile.getManifest()
                    if manifest is None:
                        # No manifest so this is not a Vaadin Add-on
                        return
                    value = manifest.getMainAttributes().getValue('Vaadin-Widgetsets')
                    if value is not None:
                        widgetsetNames = value.split(',')
                        _1 = True
                        i = 0
                        while True:
                            if _1 is True:
                                _1 = False
                            else:
                                i += 1
                            if not (i < len(widgetsetNames)):
                                break
                            widgetsetname = widgetsetNames[i].trim().intern()
                            if not (widgetsetname == ''):
                                widgetsets.put(widgetsetname, location)
            except IOException, e:
                cls._logger.log(Level.WARNING, 'Error parsing jar file', e)

    @classmethod
    def getRawClasspathEntries(cls):
        """Splits the current class path into entries, and filters them accepting
        directories, Vaadin add-on JARs with widgetsets and Vaadin JARs.

        Some other non-JAR entries may also be included in the result.

        @return filtered list of class path entries
        """
        # try to keep the order of the classpath
        locations = list()
        pathSep = System.getProperty('path.separator')
        classpath = System.getProperty('java.class.path')
        if classpath.startswith('\"'):
            classpath = classpath[1:]
        if classpath.endswith('\"'):
            classpath = classpath[:-1]
        cls._logger.fine('Classpath: ' + classpath)
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
            if cls.acceptClassPathEntry(classpathEntry):
                locations.add(classpathEntry)
        return locations

    @classmethod
    def getClasspathLocations(cls, rawClasspathEntries):
        """Determine every URL location defined by the current classpath, and it's
        associated package name.

        See {@link #classpathLocations} for information on output format.

        @param rawClasspathEntries
                   raw class path entries as split from the Java class path
                   string
        @return map of classpath locations, see {@link #classpathLocations}
        """
        start = 1000 * time.time()
        # try to keep the order of the classpath
        locations = LinkedHashMap()
        for classpathEntry in rawClasspathEntries:
            file = File(classpathEntry)
            cls.include(None, file, locations)
        end = 1000 * time.time()
        if cls._logger.isLoggable(Level.FINE):
            cls._logger.fine('getClassPathLocations took ' + (end - start) + 'ms')
        return locations

    @classmethod
    def acceptClassPathEntry(cls, classpathEntry):
        """Checks a class path entry to see whether it can contain widgets and
        widgetsets.

        All directories are automatically accepted. JARs are accepted if they
        have the "Vaadin-Widgetsets" attribute in their manifest or the JAR file
        name contains "vaadin-" or ".vaadin.".

        Also other non-JAR entries may be accepted, the caller should be prepared
        to handle them.

        @param classpathEntry
                   class path entry string as given in the Java class path
        @return true if the entry should be considered when looking for widgets
                or widgetsets
        """
        if not classpathEntry.endswith('.jar'):
            # accept all non jars (practically directories)
            return True
        elif classpathEntry.contains('vaadin-') or classpathEntry.contains('.vaadin.'):
            return True
        else:
            try:
                url = URL('file:' + File(classpathEntry).getCanonicalPath())
                url = URL('jar:' + url.toExternalForm() + '!/')
                conn = url.openConnection()
                cls._logger.fine(str(url))
                jarFile = conn.getJarFile()
                manifest = jarFile.getManifest()
                if manifest is not None:
                    mainAttributes = manifest.getMainAttributes()
                    if mainAttributes.getValue('Vaadin-Widgetsets') is not None:
                        return True
            except MalformedURLException, e:
                cls._logger.log(Level.FINEST, 'Failed to inspect JAR file', e)
            except IOException, e:
                cls._logger.log(Level.FINEST, 'Failed to inspect JAR file', e)
            return False
        # accepts jars that comply with vaadin-component packaging
        # convention (.vaadin. or vaadin- as distribution packages),

    @classmethod
    def include(cls, name, file, locations):
        """Recursively add subdirectories and jar files to locations - see
        {@link #classpathLocations}.

        @param name
        @param file
        @param locations
        """
        if not file.exists():
            return
        if not file.isDirectory():
            # could be a JAR file
            cls.includeJar(file, locations)
            return
        if file.isHidden() or file.getPath().contains(File.separator + '.'):
            return
        if name is None:
            name = ''
        else:
            name += '.'
        # add all directories recursively
        dirs = file.listFiles(cls.DIRECTORIES_ONLY)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(dirs)):
                break
            # add the present directory
            try:
                if (
                    not dirs[i].isHidden() and not dirs[i].getPath().contains(File.separator + '.')
                ):
                    key = dirs[i].getCanonicalPath() + '/' + name + dirs[i].getName()
                    locations.put(key, URL('file://' + dirs[i].getCanonicalPath()))
            except Exception, ioe:
                return
            cls.include(name + dirs[i].getName(), dirs[i], locations)

    @classmethod
    def includeJar(cls, file, locations):
        """Add a jar file to locations - see {@link #classpathLocations}.

        @param name
        @param locations
        """
        # e.printStackTrace();
        try:
            url = URL('file:' + file.getCanonicalPath())
            url = URL('jar:' + url.toExternalForm() + '!/')
            conn = url.openConnection()
            jarFile = conn.getJarFile()
            if jarFile is not None:
                # the key does not matter here as long as it is unique
                locations.put(str(url), url)
        except Exception, e:
            return

    @classmethod
    def searchForPaintables(cls, location, locationString, paintables):
        """Searches for all paintable classes and accept criteria under a location
        based on {@link ClientWidget} and {@link ClientCriterion} annotations.

        Note that client criteria are updated directly to the
        {@link #acceptCriterion} field, whereas paintables are added to the
        paintables map given as a parameter.

        @param location
        @param locationString
        @param paintables
        """
        # Get a File object for the package
        # A print stream that ignores all output.
        # 
        # This is used to hide error messages from static initializers of classes
        # being inspected.

        directory = File(location.getFile())
        if directory.exists() and not directory.isHidden():
            # Get the list of the files contained in the directory
            files = directory.list()
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(files)):
                    break
                # we are only interested in .class files
                if files[i].endswith('.class'):
                    # remove the .class extension
                    classname = files[i][:len(files[i]) - 6]
                    packageName = locationString[locationString.rfind('/') + 1:]
                    classname = packageName + '.' + classname
                    cls.tryToAdd(classname, paintables)
        else:
            # check files in jar file, entries will list all directories
            # and files in jar
            try:
                openConnection = location.openConnection()
                if isinstance(openConnection, JarURLConnection):
                    conn = openConnection
                    jarFile = conn.getJarFile()
                    # Only scan for paintables in Vaadin add-ons
                    if not cls.isVaadinAddon(jarFile):
                        return
                    e = jarFile.entries()
                    while e.hasMoreElements():
                        entry = e.nextElement()
                        entryname = entry.getName()
                        if not entry.isDirectory() and entryname.endswith('.class'):
                            classname = entryname[:-6]
                            if classname.startswith('/'):
                                classname = classname[1:]
                            classname = classname.replace('/', '.')
                            cls.tryToAdd(classname, paintables)
            except IOException, e:
                cls._logger.warning(str(e))

    _devnull = 
    class _1_(OutputStream):

        def write(self, b):
            # NOP
            pass

    _1_ = _1_()
    PrintStream(_1_)
    # Collection of all {@link AcceptCriterion} classes, updated as a side
    # effect of {@link #searchForPaintables(URL, String, Collection)} based on
    # {@link ClientCriterion} annotations.

    _acceptCriterion = set()

    @classmethod
    def tryToAdd(cls, fullclassName, paintables):
        """Checks a class for the {@link ClientWidget} and {@link ClientCriterion}
        annotations, and adds it to the appropriate collection if it has either.

        @param fullclassName
        @param paintables
                   the collection to which to add server side classes with
                   {@link ClientWidget} annotation
        """
        out = sys.stdout
        err = System.err
        errorToShow = None
        logLevel = None
        try:
            System.setErr(cls._devnull)
            System.setOut(cls._devnull)
            c = (lambda x: getattr(__import__(x.rsplit('.', 1)[0], fromlist=x.rsplit('.', 1)[0]), x.split('.')[-1]))(fullclassName)
            if c.getAnnotation(cls.ClientWidget) is not None:
                paintables.add(c)
                # System.out.println("Found paintable " + fullclassName);
            elif c.getAnnotation(cls.ClientCriterion) is not None:
                cls._acceptCriterion.add(c)
        except UnsupportedClassVersionError, e:
            logLevel = Level.INFO
            errorToShow = e
        except ClassNotFoundException, e:
            logLevel = Level.FINE
            errorToShow = e
        except LinkageError, e:
            logLevel = Level.FINE
            errorToShow = e
        except Exception, e:
            logLevel = Level.FINE
            errorToShow = e
        finally:
            System.setErr(err)
            System.setOut(out)
        # Inform the user about this as the class might contain a Paintable
        # Typically happens when using an add-on that is compiled using a
        # newer Java version.
        # Don't show to avoid flooding the user with irrelevant messages
        # Don't show to avoid flooding the user with irrelevant messages
        # Don't show to avoid flooding the user with irrelevant messages
        # Must be done here after stderr and stdout have been reset.
        if errorToShow is not None and logLevel is not None:
            cls._logger.log(logLevel, 'Failed to load class ' + fullclassName + '. ' + errorToShow.getClass().getName() + ': ' + errorToShow.getMessage())

    @classmethod
    def getDefaultSourceDirectory(cls):
        """Find and return the default source directory where to create new
        widgetsets.

        Return the first directory (not a JAR file etc.) on the classpath by
        default.

        TODO this could be done better...

        @return URL
        """
        if cls._logger.isLoggable(Level.FINE):
            cls._logger.fine('classpathLocations values:')
            locations = list(cls._classpathLocations.keys())
            for location in locations:
                cls._logger.fine(String.valueOf.valueOf(cls._classpathLocations[location]))
        it = cls._rawClasspathEntries
        while it.hasNext():
            entry = it.next()
            directory = File(entry)
            if directory.exists() and not directory.isHidden() and directory.isDirectory():
                try:
                    return URL('file://' + directory.getCanonicalPath())
                except MalformedURLException, e:
                    cls._logger.log(Level.FINEST, 'Ignoring exception', e)
                    # ignore: continue to the next classpath entry
                except IOException, e:
                    cls._logger.log(Level.FINEST, 'Ignoring exception', e)
                    # ignore: continue to the next classpath entry
        return None

    @classmethod
    def isVaadinAddon(cls, jarFile):
        """Checks if the given jarFile is a Vaadin add-on.

        @param jarFile
        @return true if the file is an add-on, false otherwise
        @throws IOException
        """
        manifest = jarFile.getManifest()
        if manifest is None:
            return False
        mainAttributes = manifest.getMainAttributes()
        if mainAttributes is None:
            return False
        return mainAttributes.getValue(cls._VAADIN_ADDON_VERSION_ATTRIBUTE) is not None

    @classmethod
    def main(cls, args):
        """Test method for helper tool"""
        paintables = ClassPathExplorer.getPaintablesHavingWidgetAnnotation()
        cls._logger.info('Found annotated paintables:')
        for cls in paintables:
            cls._logger.info(cls.getCanonicalName())
        cls._logger.info('')
        cls._logger.info('Searching available widgetsets...')
        availableWidgetSets = ClassPathExplorer.getAvailableWidgetSets()
        for string in availableWidgetSets.keys():
            cls._logger.info(string + ' in ' + availableWidgetSets[string])


if __name__ == '__main__':
    import sys
    ClassPathExplorer().main(sys.argv)
