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

from com.vaadin.terminal.gwt.widgetsetutils.ClassPathExplorer import (ClassPathExplorer,)
# from java.io.BufferedReader import (BufferedReader,)
# from java.io.BufferedWriter import (BufferedWriter,)
# from java.io.File import (File,)
# from java.io.FileNotFoundException import (FileNotFoundException,)
# from java.io.FileOutputStream import (FileOutputStream,)
# from java.io.FileReader import (FileReader,)
# from java.io.IOException import (IOException,)
# from java.io.OutputStreamWriter import (OutputStreamWriter,)
# from java.io.PrintStream import (PrintStream,)
# from java.io.Reader import (Reader,)
# from java.net.URL import (URL,)
# from java.util.Collection import (Collection,)
# from java.util.HashSet import (HashSet,)
# from java.util.Iterator import (Iterator,)
# from java.util.Map import (Map,)
# from java.util.regex.Matcher import (Matcher,)
# from java.util.regex.Pattern import (Pattern,)
try:
    from cStringIO import (StringIO,)
except ImportError, e:
    from StringIO import (StringIO,)
import sys


class WidgetSetBuilder(object):
    """Helper class to update widgetsets GWT module configuration file. Can be used
    command line or via IDE tools.

    <p>
    If module definition file contains text "WS Compiler: manually edited", tool
    will skip editing file.
    """

    @classmethod
    def main(cls, args):
        if len(args) == 0:
            cls.printUsage()
        else:
            widgetsetname = args[0]
            cls.updateWidgetSet(widgetsetname)

    @classmethod
    def updateWidgetSet(cls, widgetset):
        changed = False
        availableWidgetSets = ClassPathExplorer.getAvailableWidgetSets()
        sourceUrl = availableWidgetSets[widgetset]
        if sourceUrl is None:
            # find first/default source directory
            sourceUrl = ClassPathExplorer.getDefaultSourceDirectory()
        widgetsetfilename = sourceUrl.getFile() + '/' + widgetset.replace('.', '/') + '.gwt.xml'
        widgetsetFile = File(widgetsetfilename)
        if not widgetsetFile.exists():
            # create empty gwt module file
            parent = widgetsetFile.getParentFile()
            if parent is not None and not parent.exists():
                if not parent.mkdirs():
                    raise IOException('Could not create directory for the widgetset: ' + parent.getCanonicalPath())
            widgetsetFile.createNewFile()
            printStream = PrintStream(FileOutputStream(widgetsetFile))
            printStream.print_('<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n' + '<!DOCTYPE module PUBLIC \"-//Google Inc.//DTD ' + 'Google Web Toolkit 1.7.0//EN\" \"http://google' + '-web-toolkit.googlecode.com/svn/tags/1.7.0/dis' + 'tro-source/core/src/gwt-module.dtd\">\n')
            printStream.print_('<module>\n')
            printStream.print_('    <!--\n' + '     Uncomment the following to compile the widgetset for one browser only.\n' + '     This can reduce the GWT compilation time significantly when debugging.\n' + '     The line should be commented out before deployment to production\n' + '     environments.\n\n' + '     Multiple browsers can be specified for GWT 1.7 as a comma separated\n' + '     list. The supported user agents at the moment of writing were:\n' + '     ie6,ie8,gecko,gecko1_8,safari,opera\n\n' + '     The value gecko1_8 is used for Firefox 3 and later and safari is used for\n' + '     webkit based browsers including Google Chrome.\n' + '    -->\n' + '    <!-- <set-property name=\"user.agent\" value=\"gecko1_8\"/> -->\n')
            printStream.print_('\n</module>\n')
            printStream.close()
            changed = True
        content = cls.readFile(widgetsetFile)
        if cls.isEditable(content):
            originalContent = content
            oldInheritedWidgetsets = cls.getCurrentInheritedWidgetsets(content)
            # add widgetsets that do not exist
            i = availableWidgetSets.keys()
            while i.hasNext():
                ws = i.next()
                if ws == widgetset:
                    # do not inherit the module itself
                    continue
                if not oldInheritedWidgetsets.contains(ws):
                    content = cls.addWidgetSet(ws, content)
            for ws in oldInheritedWidgetsets:
                if not (ws in availableWidgetSets):
                    # widgetset not available in classpath
                    content = cls.removeWidgetSet(ws, content)
            changed = changed or (not (content == originalContent))
            if changed:
                cls.commitChanges(widgetsetfilename, content)
        else:
            print 'Widgetset is manually edited. Skipping updates.'

    @classmethod
    def isEditable(cls, content):
        return not content.contains('WS Compiler: manually edited')

    @classmethod
    def removeWidgetSet(cls, ws, content):
        return content.replaceFirst('<inherits name=\"' + ws + '\"[^/]*/>', '')

    @classmethod
    def commitChanges(cls, widgetsetfilename, content):
        bufferedWriter = BufferedWriter(OutputStreamWriter(FileOutputStream(widgetsetfilename)))
        bufferedWriter.write(content)
        bufferedWriter.close()

    @classmethod
    def addWidgetSet(cls, ws, content):
        return content.replace('</module>', '\n    <inherits name=\"' + ws + '\" />' + '\n</module>')

    @classmethod
    def getCurrentInheritedWidgetsets(cls, content):
        hashSet = set()
        inheritsPattern = Pattern.compile(' name=\"([^\"]*)\"')
        matcher = inheritsPattern.matcher(content)
        while matcher.find():
            gwtModule = matcher.group(1)
            if cls.isWidgetset(gwtModule):
                hashSet.add(gwtModule)
        return hashSet

    @classmethod
    def isWidgetset(cls, gwtModuleName):
        return gwtModuleName.toLowerCase().contains('widgetset')

    @classmethod
    def readFile(cls, widgetsetFile):
        fi = FileReader(widgetsetFile)
        bufferedReader = StringIO(fi)
        sb = cls.StringBuilder()
        while line = bufferedReader.readline() is not None:
            sb.append(line)
            sb.append('\n')
        fi.close()
        return str(sb)

    @classmethod
    def printUsage(cls):
        o = sys.stdout
        print WidgetSetBuilder.getSimpleName() + ' usage:'
        print '    1. Set the same classpath as you will ' + 'have for the GWT compiler.'
        print '    2. Give the widgetsetname (to be created or updated)' + ' as first parameter'
        print 
        print 'All found vaadin widgetsets will be inherited in given widgetset'


if __name__ == '__main__':
    import sys
    WidgetSetBuilder().main(sys.argv)
