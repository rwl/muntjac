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

import sys
import traceback

from os import listdir

from os.path import exists, dirname, join, isdir, basename

import muntjac

from muntjac.ui.component import IComponent
from muntjac.ui.component_container import IComponentContainer

from muntjac.api import \
    (PopupView, CustomComponent, LoginForm, SplitPanel, VerticalSplitPanel,
     HorizontalSplitPanel, Window)

from muntjac.ui.drag_and_drop_wrapper import DragAndDropWrapper

from muntjac.util import clsname, loadClass


class MuntjacClasses(object):

    @classmethod
    def main(cls, args):
        print 'ComponentContainers'
        print '==================='
        for c in cls.getComponentContainers():
            print clsname(c)
        print
        print 'Components'
        print '=========='
        for c in cls.getComponents():
            print clsname(c)
        print
        print 'Server side classes'
        print '==================='
        for c in cls.getAllServerSideClasses():
            print clsname(c)


    @classmethod
    def getComponents(cls):
        try:
            return cls.findClasses(IComponent, 'muntjac.ui')
        except IOError:
            traceback.print_exc(file=sys.stdout)
            return list()


    @classmethod
    def getAllServerSideClasses(cls):
        try:
            return cls.findClassesNoTests(object, 'muntjac',
                    ['muntjac.tests', 'muntjac.terminal.gwt.client'])
        except IOError:
            traceback.print_exc(file=sys.stdout)
            return list()


    @classmethod
    def getComponentContainers(cls):
        try:
            return cls.findClasses(IComponentContainer, 'muntjac.ui')
        except IOError:
            traceback.print_exc(file=sys.stdout)
            return list()


    @classmethod
    def getComponentContainersSupportingAddRemoveComponent(cls):
        classes = cls.getComponentContainers()
        classes.remove(PopupView)
        classes.remove(CustomComponent)
        classes.remove(DragAndDropWrapper)
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


#    @classmethod
#    def getBasicComponentTests(cls):
#        try:
#            return cls.findClasses(AbstractComponentTest,
#                    'muntjac.tests.components')
#        except IOError:
#            traceback.print_exc(file=sys.stdout)
#            return None


    @classmethod
    def findClasses(cls, baseClass, basePackage, ignoredPackages=None):
        if ignoredPackages == None:
            ignoredPackages = []

        classes = list()
        basePackageDirName = '/' + basePackage.replace('.', '/')
        location = cls.getResource(basePackageDirName)

        if not exists(location):
            raise IOError('Directory ' + location + ' does not exist')
        cls.findPackages(location, basePackage, baseClass, classes,
                ignoredPackages)

        classes.sort(key=lambda klass: clsname(klass))

        return classes


    @classmethod
    def findClassesNoTests(cls, baseClass, basePackage, ignoredPackages):
        classes = cls.findClasses(baseClass, basePackage, ignoredPackages)

        classesNoTests = list()
        for clazz in classes:
            if 'Test' not in clsname(clazz):
                testPresent = False
                #for method in clazz.getMethods():
                #    if method.isAnnotationPresent(Test):
                #        testPresent = True
                #        break
                if not testPresent:
                    classesNoTests.append(clazz)

        return classesNoTests


    @classmethod
    def findPackages(cls, parent, package, baseClass, result, ignoredPackages):

        exceptions = ['__init__.py', 'util.py', 'api.py']

        for ignoredPackage in ignoredPackages:
            if package == ignoredPackage:
                return

        for f in listdir(parent):
            if isdir(f):
                cls.findPackages(file, package + '.' + basename(f),
                        baseClass, result, ignoredPackages)
            elif f.endswith('.py') and basename(f) not in exceptions:
                fullyQualifiedClassName = cls.fullyQualifiedName(package, f)
                cls.addClassIfMatches(result, fullyQualifiedClassName,
                        baseClass)


    @classmethod
    def addClassIfMatches(cls, result, fullyQualifiedClassName, baseClass):
        try:
            # Try to load the class
            c = loadClass(fullyQualifiedClassName)
            if issubclass(c, baseClass) and not cls.isAbstract(c):
                result.append(c)

        except AttributeError:
            # try interface
            pos = fullyQualifiedClassName.rfind('.')
            fullyQualifiedClassName = (fullyQualifiedClassName[:pos + 1] +
                    'I' + fullyQualifiedClassName[pos + 1:])

            try:
                c = loadClass(fullyQualifiedClassName)
#                if issubclass(c, baseClass) and not cls.isAbstract(c):
#                    result.append(c)
            except Exception:
                traceback.print_exc(file=sys.stdout)

        except Exception:
            # Could ignore that class cannot be loaded
            traceback.print_exc(file=sys.stdout)
            # Ignore client side classes that will at least throw LinkageErrors


    @classmethod
    def getResource(cls, path):
        if path[0] == '/':
            path = path[1:]

        root = join(dirname(muntjac.__file__), '..')
        return join(root, path)


    @classmethod
    def isAbstract(self, klass):
        name = klass.__name__

        if name.startswith('_') or name.lower().startswith('abstract'):
            return True
        else:
            return False


    @classmethod
    def fullyQualifiedName(cls, package, filename):
        name = basename(filename).replace('.py', '')
        if '_' in name or (name.lower() == name):
            clsname = cls.toCamel(name)
        else:
            clsname = name

        return package + '.' + name + '.' + clsname


    @classmethod
    def toCamel(cls, name):
        camel = ''
        lastWasUnderScore = False

        for i, c in enumerate(name):
            if i == 0:
                camel += c.upper()
            elif lastWasUnderScore:
                camel += c.upper()
                lastWasUnderScore = False
            elif c == '_':
                lastWasUnderScore = True
            else:
                camel += c

        return camel


if __name__ == '__main__':
    MuntjacClasses.main(sys.argv)
