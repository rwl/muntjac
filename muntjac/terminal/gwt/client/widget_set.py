# Copyright (C) 2011 Vaadin Ltd.
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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

import pygwt as GWT

from muntjac.terminal.gwt.client.ui.v_window import VWindow
from muntjac.terminal.gwt.client.ui.v_list_select import VListSelect
from muntjac.terminal.gwt.client.widget_map import WidgetMap
from muntjac.terminal.gwt.client.ui.v_password_field import VPasswordField
from muntjac.terminal.gwt.client.ui.v_view import VView
from muntjac.terminal.gwt.client.ui.v_text_field import VTextField
from muntjac.terminal.gwt.client.ui.v_check_box import VCheckBox
from muntjac.terminal.gwt.client.ui.v_split_panel_vertical import VSplitPanelVertical
from muntjac.terminal.gwt.client.ui.v_filter_select import VFilterSelect
from muntjac.terminal.gwt.client.ui.v_button import VButton
from muntjac.terminal.gwt.client.ui.v_text_area import VTextArea
from muntjac.terminal.gwt.client.ui.v_split_panel_horizontal import VSplitPanelHorizontal
from muntjac.terminal.gwt.client.ui.v_unknown_component import VUnknownComponent


class WidgetSet(object):

    def __init__(self):
        # WidgetSet (and its extensions) delegate instantiation of widgets and
        # client-server matching to WidgetMap. The actual implementations are
        # generated with gwts generators/deferred binding.
        self._widgetMap = GWT.create(WidgetMap)


    def createWidget(self, uidl, conf):
        """Create an uninitialized component that best matches given UIDL. The
        component must be a {@link Widget} that implements {@link Paintable}.

        @param uidl:
                   UIDL to be painted with returned component.
        @param client:
                   the application connection that whishes to instantiate widget

        @return: New uninitialized and unregistered component that can paint
                 given UIDL.
        """
        # Yes, this (including the generated code in WidgetMap) may look very
        # odd code, but due the nature of GWT, we cannot do this any cleaner.
        # Luckily this is mostly written by WidgetSetGenerator, here are just
        # some hacks. Extra instantiation code is needed if client side widget
        # has no "native" counterpart on client side.
        #
        # TODO: should try to get rid of these exceptions here

        classType = self.resolveWidgetType(uidl, conf)
        if (classType is None) or (classType == VUnknownComponent):
            serverSideName = conf.getUnknownServerClassNameByEncodedTagName(
                    uidl.getTag())
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
                typ = uidl.getStringAttribute('type').intern()
                if 'legacy-multi' == typ:
                    return VListSelect
        elif widgetClass == VTextField:
            if uidl.hasAttribute('multiline'):
                return VTextArea
            elif uidl.hasAttribute('secret'):
                return VPasswordField
        elif (widgetClass == VSplitPanelHorizontal
                and uidl.hasAttribute('vertical')):
            return VSplitPanelVertical

        return widgetClass


    def isCorrectImplementation(self, currentWidget, uidl, conf):
        """Test if the given component implementation conforms to UIDL.

        @param currentWidget:
                   Current implementation of the component
        @param uidl:
                   UIDL to test against
        @return: true iff createWidget would return a new component of the same
                 class than currentWidget
        """
        return currentWidget.getClass() == self.resolveWidgetType(uidl, conf)


    def getImplementationByClassName(self, fullyqualifiedName):
        """Due its nature, GWT does not support dynamic classloading. To bypass
        this limitation, widgetset must have function that returns Class by its
        fully qualified name.
        """
        if fullyqualifiedName is None:
            return VUnknownComponent

        implementationByServerSideClassName = \
                self._widgetMap.getImplementationByServerSideClassName(
                        fullyqualifiedName)

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
