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

from com.vaadin.terminal.gwt.client.ui.VView import (VView,)
from com.vaadin.ui.ClientWidget import (LoadStyle,)
from com.vaadin.terminal.gwt.widgetsetutils.ClassPathExplorer import (ClassPathExplorer,)
# from java.io.PrintWriter import (PrintWriter,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Collection import (Collection,)
# from java.util.Date import (Date,)
# from java.util.HashMap import (HashMap,)
# from java.util.HashSet import (HashSet,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedList import (LinkedList,)
# from java.util.TreeSet import (TreeSet,)


class WidgetMapGenerator(Generator):
    """WidgetMapGenerator's are GWT generator to build WidgetMapImpl dynamically
    based on {@link ClientWidget} annotations available in workspace. By
    modifying the generator it is possible to do some fine tuning for the
    generated widgetset (aka client side engine). The components to be included
    in the client side engine can modified be overriding
    {@link #getUsedPaintables()}.
    <p>
    The generator also decides how the client side component implementations are
    loaded to the browser. The default generator is
    {@link EagerWidgetMapGenerator} that builds a monolithic client side engine
    that loads all widget implementation on application initialization. This has
    been the only option until Vaadin 6.4.
    <p>
    This generator uses the loadStyle hints from the {@link ClientWidget}
    annotations. Depending on the {@link LoadStyle} used, the widget may be
    included in the initially loaded JavaScript, loaded when the application has
    started and there is no communication to server or lazy loaded when the
    implementation is absolutely needed.
    <p>
    The GWT module description file of the widgetset (
    <code>...Widgetset.gwt.xml</code>) can be used to define the
    WidgetMapGenarator. An example that defines this generator to be used:

    <pre>
    <code>
    &lt;generate-with
              class="com.vaadin.terminal.gwt.widgetsetutils.MyWidgetMapGenerator"&gt;
             &lt;when-type-is class="com.vaadin.terminal.gwt.client.WidgetMap" /&gt;
    &lt;/generate-with&gt;

    </code>
    </pre>

    <p>
    Vaadin package also includes {@link LazyWidgetMapGenerator}, which is a good
    option if the transferred data should be minimized, and
    {@link CustomWidgetMapGenerator} for easy overriding of loading strategies.
    """
    _packageName = None
    _className = None

    def generate(self, logger, context, typeName):
        # return the fully qualifed name of the class generated
        try:
            typeOracle = context.getTypeOracle()
            # get classType and save instance variables
            classType = typeOracle.getType(typeName)
            self._packageName = classType.getPackage().getName()
            self._className = classType.getSimpleSourceName() + 'Impl'
            # Generate class source code
            self.generateClass(logger, context)
        except Exception, e:
            logger.log(self.TreeLogger.ERROR, 'WidgetMap creation failed', e)
        return self._packageName + '.' + self._className

    def generateClass(self, logger, context):
        """Generate source code for WidgetMapImpl

        @param logger
                   Logger object
        @param context
                   Generator context
        """
        # get print writer that receives the source code
        printWriter = None
        printWriter = context.tryCreate(logger, self._packageName, self._className)
        # print writer if null, source code has ALREADY been generated,
        # return (WidgetMap is equal to all permutations atm)
        if printWriter is None:
            return
        # logger.log(Type.INFO,
        # "Detecting Vaadin components in classpath to generate WidgetMapImpl.java ...");
        date = Date()
        # init composer, set class properties, create source writer
        composer = None
        composer = self.ClassSourceFileComposerFactory(self._packageName, self._className)
        composer.addImport('com.google.gwt.core.client.GWT')
        composer.addImport('java.util.HashMap')
        composer.addImport('com.google.gwt.core.client.RunAsyncCallback')
        composer.setSuperclass('com.vaadin.terminal.gwt.client.WidgetMap')
        sourceWriter = composer.createSourceWriter(context, printWriter)
        paintablesHavingWidgetAnnotation = self.getUsedPaintables()
        self.validatePaintables(logger, context, paintablesHavingWidgetAnnotation)
        # generator constructor source code
        self.generateImplementationDetector(sourceWriter, paintablesHavingWidgetAnnotation)
        self.generateInstantiatorMethod(sourceWriter, paintablesHavingWidgetAnnotation)
        # close generated class
        sourceWriter.outdent()
        print '}'
        # commit generated class
        context.commit(logger, printWriter)
        # logger.log(Type.INFO,
        # "Done. (" + (new Date().getTime() - date.getTime()) / 1000
        # + "seconds)");

    def validatePaintables(self, logger, context, paintablesHavingWidgetAnnotation):
        """Verifies that all client side components are available for client side
        GWT module.

        @param logger
        @param context
        @param paintablesHavingWidgetAnnotation
        """
        typeOracle = context.getTypeOracle()
        _0 = True
        iterator = paintablesHavingWidgetAnnotation
        while True:
            if _0 is True:
                _0 = False
            if not iterator.hasNext():
                break
            class1 = iterator.next()
            annotation = class1.getAnnotation(self.ClientWidget)
            if typeOracle.findType(annotation.value().getName()) is None:
                # GWT widget not inherited
                # logger.log(Type.WARN, "Widget class "
                # + annotation.value().getName()
                # + " was not found. The component " + class1.getName()
                # + " will not be included in the widgetset.");
                iterator.remove()
        # logger.log(Type.INFO,
        # "Widget set will contain implementations for following components: ");
        classNames = TreeSet()
        loadStyle = dict()
        for class1 in paintablesHavingWidgetAnnotation:
            className = class1.getCanonicalName()
            classNames.add(className)
            if self.getLoadStyle(class1) == LoadStyle.DEFERRED:
                loadStyle.put(className, 'DEFERRED')
            elif self.getLoadStyle(class1) == LoadStyle.LAZY:
                loadStyle.put(className, 'LAZY')
        for className in classNames:
            msg = className
            if className in loadStyle:
                msg += ' (load style: ' + loadStyle[className] + ')'
            # logger.log(Type.INFO, "\t" + msg);

    def getUsedPaintables(self):
        """This method is protected to allow creation of optimized widgetsets. The
        Widgetset will contain only implementation returned by this function. If
        one knows which widgets are needed for the application, returning only
        them here will significantly optimize the size of the produced JS.

        @return a collections of Vaadin components that will be added to
                widgetset
        """
        return ClassPathExplorer.getPaintablesHavingWidgetAnnotation()

    def getLoadStyle(self, paintableType):
        """Returns true if the widget for given component will be lazy loaded by the
        client. The default implementation reads the information from the
        {@link ClientWidget} annotation.
        <p>
        The method can be overridden to optimize the widget loading mechanism. If
        the Widgetset is wanted to be optimized for a network with a high latency
        or for a one with a very fast throughput, it may be good to return false
        for every component.

        @param paintableType
        @return true iff the widget for given component should be lazy loaded by
                the client side engine
        """
        annotation = paintableType.getAnnotation(self.ClientWidget)
        return annotation.loadStyle()

    def generateInstantiatorMethod(self, sourceWriter, paintablesHavingWidgetAnnotation):
        deferredWidgets = LinkedList()
        # TODO detect if it would be noticably faster to instantiate with a
        # lookup with index than with the hashmap
        print 'public void ensureInstantiator(Class<? extends Paintable> classType) {'
        print 'if(!instmap.containsKey(classType)){'
        first = True
        lazyLoadedWidgets = list()
        widgetsWithInstantiator = set()
        for class1 in paintablesHavingWidgetAnnotation:
            annotation = class1.getAnnotation(self.ClientWidget)
            clientClass = annotation.value()
            if clientClass in widgetsWithInstantiator:
                continue
            if clientClass == VView:
                # VView's are not instantiated by widgetset
                continue
            if not first:
                sourceWriter.print_(' else ')
            else:
                first = False
            sourceWriter.print_('if( classType == ' + clientClass.getName() + '.class) {')
            instantiator = 'new WidgetInstantiator() {\n public Paintable get() {\n return GWT.create(' + clientClass.getName() + '.class );\n}\n}\n'
            loadStyle = self.getLoadStyle(class1)
            if loadStyle != LoadStyle.EAGER:
                sourceWriter.print_('ApplicationConfiguration.startWidgetLoading();\n' + 'GWT.runAsync( \n' + 'new WidgetLoader() { void addInstantiator() {instmap.put(' + clientClass.getName() + '.class,' + instantiator + ');}});\n')
                lazyLoadedWidgets.add(class1)
                if loadStyle == LoadStyle.DEFERRED:
                    deferredWidgets.add(class1)
            else:
                # widget implementation in initially loaded js script
                sourceWriter.print_('instmap.put(')
                sourceWriter.print_(clientClass.getName())
                sourceWriter.print_('.class, ')
                sourceWriter.print_(instantiator)
                sourceWriter.print_(');')
            sourceWriter.print_('}')
            widgetsWithInstantiator.add(clientClass)
        print '}'
        print '}'
        print 'public Class<? extends Paintable>[] getDeferredLoadedWidgets() {'
        print 'return new Class[] {'
        first = True
        for class2 in deferredWidgets:
            if not first:
                print ','
            first = False
            annotation = class2.getAnnotation(self.ClientWidget)
            value = annotation.value()
            sourceWriter.print_(value.getName() + '.class')
        print '};'
        print '}'
        # in constructor add a "thread" that lazyly loads lazy loaded widgets
        # if communication to server idles
        # TODO an array of lazy loaded widgets
        # TODO an index of last ensured widget in array
        print 'public Paintable instantiate(Class<? extends Paintable> classType) {'
        sourceWriter.indent()
        print 'Paintable p = super.instantiate(classType); if(p!= null) return p;'
        print 'return instmap.get(classType).get();'
        sourceWriter.outdent()
        print '}'

    def generateImplementationDetector(self, sourceWriter, paintablesHavingWidgetAnnotation):
        """@param sourceWriter
                   Source writer to output source code
        @param paintablesHavingWidgetAnnotation
        """
        print 'public Class<? extends Paintable> ' + 'getImplementationByServerSideClassName(String fullyQualifiedName) {'
        sourceWriter.indent()
        print 'fullyQualifiedName = fullyQualifiedName.intern();'
        for class1 in paintablesHavingWidgetAnnotation:
            annotation = class1.getAnnotation(self.ClientWidget)
            clientClass = annotation.value()
            sourceWriter.print_('if ( fullyQualifiedName == \"')
            sourceWriter.print_(class1.getName())
            sourceWriter.print_('\" ) { ensureInstantiator(' + clientClass.getName() + '.class); return ')
            sourceWriter.print_(clientClass.getName())
            print '.class;}'
            sourceWriter.print_('else ')
        print 'return com.vaadin.terminal.gwt.client.ui.VUnknownComponent.class;'
        sourceWriter.outdent()
        print '}'
