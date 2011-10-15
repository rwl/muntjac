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

from com.vaadin.tests.components.AbstractComponentTest import \
    AbstractComponentTest

# from com.vaadin.Application import (Application,)
# from com.vaadin.ui.Component import (Component,)
# from com.vaadin.ui.ComponentContainer import (ComponentContainer,)
# from com.vaadin.ui.CustomComponent import (CustomComponent,)
# from com.vaadin.ui.DragAndDropWrapper import (DragAndDropWrapper,)
# from com.vaadin.ui.HorizontalSplitPanel import (HorizontalSplitPanel,)
# from com.vaadin.ui.LoginForm import (LoginForm,)
# from com.vaadin.ui.PopupView import (PopupView,)
# from com.vaadin.ui.SplitPanel import (SplitPanel,)
# from com.vaadin.ui.VerticalSplitPanel import (VerticalSplitPanel,)
# from com.vaadin.ui.Window import (Window,)
# from java.io.File import (File,)
# from java.io.IOException import (IOException,)
# from java.lang.reflect.Method import (Method,)
# from java.lang.reflect.Modifier import (Modifier,)
# from java.net.JarURLConnection import (JarURLConnection,)
# from java.net.URISyntaxException import (URISyntaxException,)
# from java.net.URL import (URL,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Collection import (Collection,)
# from java.util.Collections import (Collections,)
# from java.util.Comparator import (Comparator,)
# from java.util.Enumeration import (Enumeration,)
# from java.util.List import (List,)
# from java.util.jar.JarEntry import (JarEntry,)
# from org.junit.Test import (Test,)
AbstractComponentTest = AbstractComponentTest.AbstractComponentTest


class VaadinClasses(object):

    @classmethod
    def main(cls, args):
        print 'ComponentContainers'
        print '==================='
        for c in cls.getComponentContainers():
            print c.getName()
        print
        print 'Components'
        print '=========='
        for c in cls.getComponents():
            print c.getName()
        print
        print 'Server side classes'
        print '==================='
        for c in cls.getAllServerSideClasses():
            print c.getName()

    @classmethod
    def getComponents(cls):
        try:
            return cls.findClasses(Component, 'com.vaadin.ui')
        except IOException, e:
            e.printStackTrace()
            return None

    @classmethod
    def getAllServerSideClasses(cls):
        try:
            return cls.findClassesNoTests(cls.Object, 'com.vaadin', ['com.vaadin.tests', 'com.vaadin.terminal.gwt.client'])
        except IOException, e:
            e.printStackTrace()
            return None

    @classmethod
    def getComponentContainers(cls):
        try:
            return cls.findClasses(ComponentContainer, 'com.vaadin.ui')
        except IOException, e:
            e.printStackTrace()
            return None

    @classmethod
    def getComponentContainersSupportingAddRemoveComponent(cls):
        classes = cls.getComponentContainers()
        classes.remove(PopupView)
        classes.remove(CustomComponent)
        classes.remove(DragAndDropWrapper)
        classes.remove(CustomComponent)
        classes.remove(LoginForm)
        return classes

    @classmethod
    def getComponentContainersSupportingUnlimitedNumberOfComponents(cls):
        classes = cls.getComponentContainersSupportingAddRemoveComponent()
        classes.remove(SplitPanel)
        classes.remove(VerticalSplitPanel)
        classes.remove(HorizontalSplitPanel)
        classes.remove(Window)
        return classes

    @classmethod
    def getBasicComponentTests(cls):
        try:
            return cls.findClasses(AbstractComponentTest, 'com.vaadin.tests.components')
        except IOException, e:
            e.printStackTrace()
            return None

    @classmethod
    def findClasses(cls, *args):
        _0 = args
        _1 = len(args)
        if _1 == 2:
            baseClass, basePackage = _0
            return cls.findClasses(baseClass, basePackage, [])
        elif _1 == 3:
            baseClass, basePackage, ignoredPackages = _0
            classes = list()
            basePackageDirName = '/' + basePackage.replace('.', '/')
            location = Application.getResource(basePackageDirName)
            if location.getProtocol() == 'file':
                try:
                    f = File(location.toURI())
                    if not f.exists():
                        raise IOException('Directory ' + str(f) + ' does not exist')
                    cls.findPackages(f, basePackage, baseClass, classes, ignoredPackages)
                except URISyntaxException, e:
                    raise IOException(e.getMessage())
            elif location.getProtocol() == 'jar':
                juc = location.openConnection()
                cls.findPackages(juc, basePackage, baseClass, classes)

            class _0_(Comparator):

                def compare(self, o1, o2):
                    return o1.getName().compareTo(o2.getName())

            _0_ = _0_()
            Collections.sort(classes, _0_)
            return classes
        else:
            raise ARGERROR(2, 3)

    @classmethod
    def findClassesNoTests(cls, baseClass, basePackage, ignoredPackages):
        classes = cls.findClasses(baseClass, basePackage, ignoredPackages)
        classesNoTests = list()
        for clazz in classes:
            if not clazz.getName().contains('Test'):
                testPresent = False
                for method in clazz.getMethods():
                    if method.isAnnotationPresent(Test):
                        testPresent = True
                        break
                if not testPresent:
                    classesNoTests.add(clazz)
        return classesNoTests

    @classmethod
    def findPackages(cls, *args):
        _0 = args
        _1 = len(args)
        if _1 == 4:
            juc, javaPackage, baseClass, result = _0
            prefix = 'com/vaadin/ui'
            ent = juc.getJarFile().entries()
            while ent.hasMoreElements():
                e = ent.nextElement()
                if e.getName().endswith('.class') and e.getName().startswith(prefix):
                    fullyQualifiedClassName = e.getName().replace('/', '.').replace('.class', '')
                    cls.addClassIfMatches(result, fullyQualifiedClassName, baseClass)
        elif _1 == 5:
            parent, javaPackage, baseClass, result, ignoredPackages = _0
            for ignoredPackage in ignoredPackages:
                if javaPackage == ignoredPackage:
                    return
            for file in parent.listFiles():
                if file.isDirectory():
                    cls.findPackages(file, javaPackage + '.' + file.getName(), baseClass, result, ignoredPackages)
                elif file.getName().endswith('.class'):
                    fullyQualifiedClassName = javaPackage + '.' + file.getName().replace('.class', '')
                    cls.addClassIfMatches(result, fullyQualifiedClassName, baseClass)
        else:
            raise ARGERROR(4, 5)

    @classmethod
    def addClassIfMatches(cls, result, fullyQualifiedClassName, baseClass):
        # Try to load the class
        # Could ignore that class cannot be loaded
        # Ignore. Client side classes will at least throw LinkageErrors
        try:
            c = (lambda x: getattr(__import__(x.rsplit('.', 1)[0], fromlist=x.rsplit('.', 1)[0]), x.split('.')[-1]))(fullyQualifiedClassName)
            if baseClass.isAssignableFrom(c) and not Modifier.isAbstract(c.getModifiers()):
                result.add(c)
        except Exception, e:
            e.printStackTrace()
        except cls.LinkageError, e:
            pass # astStmt: [Stmt([]), None]


if __name__ == '__main__':
    import sys
    VaadinClasses().main(sys.argv)
