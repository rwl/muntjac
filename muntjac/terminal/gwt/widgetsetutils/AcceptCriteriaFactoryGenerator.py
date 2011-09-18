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
# from com.google.gwt.core.ext.Generator import (Generator,)
# from com.google.gwt.core.ext.GeneratorContext import (GeneratorContext,)
# from com.google.gwt.core.ext.TreeLogger import (TreeLogger,)
# from com.google.gwt.core.ext.TreeLogger.Type import (Type,)
# from com.google.gwt.core.ext.UnableToCompleteException import (UnableToCompleteException,)
# from com.google.gwt.core.ext.typeinfo.JClassType import (JClassType,)
# from com.google.gwt.core.ext.typeinfo.TypeOracle import (TypeOracle,)
# from com.google.gwt.user.rebind.ClassSourceFileComposerFactory import (ClassSourceFileComposerFactory,)
# from com.google.gwt.user.rebind.SourceWriter import (SourceWriter,)
# from java.io.PrintWriter import (PrintWriter,)
# from java.util.Collection import (Collection,)
# from java.util.Date import (Date,)


class AcceptCriteriaFactoryGenerator(Generator):
    """GWT generator to build {@link VAcceptCriterionFactory} implementation
    dynamically based on {@link ClientCriterion} annotations available in
    classpath.
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
            logger.log(TreeLogger.ERROR, 'Accept criterion factory creation failed', e)
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
        # logger.log(Type.INFO, "Detecting available criteria ...");
        date = Date()
        # init composer, set class properties, create source writer
        composer = None
        composer = ClassSourceFileComposerFactory(self._packageName, self._className)
        composer.addImport('com.google.gwt.core.client.GWT')
        composer.setSuperclass('com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterionFactory')
        sourceWriter = composer.createSourceWriter(context, printWriter)
        # generator constructor source code
        self.generateInstantiatorMethod(sourceWriter, context, logger)
        # close generated class
        sourceWriter.outdent()
        print '}'
        # commit generated class
        context.commit(logger, printWriter)
        # logger.log(Type.INFO,
        # "Done. (" + (new Date().getTime() - date.getTime()) / 1000
        # + "seconds)");

    def generateInstantiatorMethod(self, sourceWriter, context, logger):
        print 'public VAcceptCriterion get(String name) {'
        sourceWriter.indent()
        print 'name = name.intern();'
        clientSideVerifiableCriterion = ClassPathExplorer.getCriterion()
        for class1 in clientSideVerifiableCriterion:
            # logger.log(Type.INFO,
            # "creating mapping for " + class1.getCanonicalName());
            canonicalName = class1.getCanonicalName()
            clientClass = class1.getAnnotation(self.ClientCriterion).value()
            sourceWriter.print_('if (\"')
            sourceWriter.print_(canonicalName)
            sourceWriter.print_('\" == name) return GWT.create(')
            sourceWriter.print_(clientClass.getCanonicalName())
            print '.class );'
            sourceWriter.print_('else ')
        print 'return null;'
        sourceWriter.outdent()
        print '}'
