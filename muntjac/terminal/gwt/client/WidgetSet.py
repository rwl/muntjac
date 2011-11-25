# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.VWindow import (VWindow,)
from com.vaadin.terminal.gwt.client.ui.VListSelect import (VListSelect,)
from com.vaadin.terminal.gwt.client.WidgetMap import (WidgetMap,)
from com.vaadin.terminal.gwt.client.ui.VPasswordField import (VPasswordField,)
from com.vaadin.terminal.gwt.client.ui.VView import (VView,)
from com.vaadin.terminal.gwt.client.ui.VTextField import (VTextField,)
from com.vaadin.terminal.gwt.client.ui.VCheckBox import (VCheckBox,)
from com.vaadin.terminal.gwt.client.ui.VSplitPanelVertical import (VSplitPanelVertical,)
from com.vaadin.terminal.gwt.client.ui.VFilterSelect import (VFilterSelect,)
from com.vaadin.terminal.gwt.client.ui.VButton import (VButton,)
from com.vaadin.terminal.gwt.client.ui.VTextArea import (VTextArea,)
from com.vaadin.terminal.gwt.client.ui.VSplitPanelHorizontal import (VSplitPanelHorizontal,)
from com.vaadin.terminal.gwt.client.ui.VUnknownComponent import (VUnknownComponent,)


class WidgetSet(object):
    # WidgetSet (and its extensions) delegate instantiation of widgets and
    # client-server matching to WidgetMap. The actual implementations are
    # generated with gwts generators/deferred binding.

    _widgetMap = GWT.create(WidgetMap)

    def createWidget(self, uidl, conf):
        """Create an uninitialized component that best matches given UIDL. The
        component must be a {@link Widget} that implements {@link Paintable}.

        @param uidl
                   UIDL to be painted with returned component.
        @param client
                   the application connection that whishes to instantiate widget

        @return New uninitialized and unregistered component that can paint given
                UIDL.
        """
        # Yes, this (including the generated code in WidgetMap) may look very
        # odd code, but due the nature of GWT, we cannot do this any cleaner.
        # Luckily this is mostly written by WidgetSetGenerator, here are just
        # some hacks. Extra instantiation code is needed if client side widget
        # has no "native" counterpart on client side.
        # 
        # TODO should try to get rid of these exceptions here

        classType = self.resolveWidgetType(uidl, conf)
        if (classType is None) or (classType == VUnknownComponent):
            serverSideName = conf.getUnknownServerClassNameByEncodedTagName(uidl.getTag())
            c = GWT.create(VUnknownComponent)
            c.setServerSideClassName(serverSideName)
            return c
        elif VWindow == classType:
            return GWT.create(VWindow)
        else:
            # let the auto generated code instantiate this type
            return self._widgetMap.instantiate(classType)

    def resolveWidgetType(self, uidl, conf):
        tag = uidl.getTag()
        widgetClass = conf.getWidgetClassByEncodedTag(tag)
        # add our historical quirks
        if widgetClass == VButton and uidl.hasAttribute('type'):
            return VCheckBox
        elif widgetClass == VView and uidl.hasAttribute('sub'):
            return VWindow
        elif widgetClass == VFilterSelect:
            if uidl.hasAttribute('type'):
                type = uidl.getStringAttribute('type').intern()
                if 'legacy-multi' == type:
                    return VListSelect
        elif widgetClass == VTextField:
            if uidl.hasAttribute('multiline'):
                return VTextArea
            elif uidl.hasAttribute('secret'):
                return VPasswordField
        elif widgetClass == VSplitPanelHorizontal and uidl.hasAttribute('vertical'):
            return VSplitPanelVertical
        return widgetClass

    def isCorrectImplementation(self, currentWidget, uidl, conf):
        """Test if the given component implementation conforms to UIDL.

        @param currentWidget
                   Current implementation of the component
        @param uidl
                   UIDL to test against
        @return true iff createWidget would return a new component of the same
                class than currentWidget
        """
        return currentWidget.getClass() == self.resolveWidgetType(uidl, conf)

    def getImplementationByClassName(self, fullyqualifiedName):
        """Due its nature, GWT does not support dynamic classloading. To bypass this
        limitation, widgetset must have function that returns Class by its fully
        qualified name.

        @param fullyQualifiedName
        @param applicationConfiguration
        @return
        """
        if fullyqualifiedName is None:
            return VUnknownComponent
        implementationByServerSideClassName = self._widgetMap.getImplementationByServerSideClassName(fullyqualifiedName)
        # Also ensure that our historical quirks have their instantiators
        # loaded. Without these, legacy code will throw NPEs when e.g. a Select
        # is in multiselect mode, causing the clientside implementation to
        # *actually* be VListSelect, when the annotation says VFilterSelect

        if fullyqualifiedName == 'com.vaadin.ui.Button':
            self.loadImplementation(VCheckBox)
        elif fullyqualifiedName == 'com.vaadin.ui.Select':
            self.loadImplementation(VListSelect)
        elif fullyqualifiedName == 'com.vaadin.ui.TextField':
            self.loadImplementation(VTextArea)
            self.loadImplementation(VPasswordField)
        elif fullyqualifiedName == 'com.vaadin.ui.SplitPanel':
            self.loadImplementation(VSplitPanelVertical)
        return implementationByServerSideClassName

    def getDeferredLoadedWidgets(self):
        return self._widgetMap.getDeferredLoadedWidgets()

    def loadImplementation(self, nextType):
        self._widgetMap.ensureInstantiator(nextType)
