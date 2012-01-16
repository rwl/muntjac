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

from unittest import TestCase

from muntjac.data.container import IIndexed, IItemSetChangeListener
from muntjac.data.util.filter.simple_string_filter import SimpleStringFilter


class AbstractContainerTest(TestCase):

    # #6043: for items that have been filtered out, Container interface does
    # not specify what to return from getItem() and getContainerProperty(), so
    # need checkGetItemNull parameter for the test to be usable for most
    # current containers
    def validateContainer(self, container, expectedFirstItemId,
                expectedLastItemId, itemIdInSet, itemIdNotInSet,
                checkGetItemNull, expectedSize):

        indexed = None
        if isinstance(container, IIndexed):
            indexed = container

        itemIdList = list(container.getItemIds())

        # size()
        self.assertEquals(expectedSize, len(container))
        self.assertEquals(expectedSize, len(itemIdList))

        # first item, last item
        first = itemIdList[0]
        last = itemIdList[len(itemIdList) - 1]

        self.assertEquals(expectedFirstItemId, first)
        self.assertEquals(expectedLastItemId, last)

        # containsId
        self.assertFalse(container.containsId(itemIdNotInSet))
        self.assertTrue(container.containsId(itemIdInSet))

        # getItem
        if checkGetItemNull:
            self.assertIsNone(container.getItem(itemIdNotInSet))

        self.assertIsNotNone(container.getItem(itemIdInSet))

        # getContainerProperty
        for propId in container.getContainerPropertyIds():
            if checkGetItemNull:
                self.assertIsNone(container.getContainerProperty(itemIdNotInSet,
                        propId))
            self.assertIsNotNone(container.getContainerProperty(itemIdInSet,
                    propId))

        if indexed is not None:
            # firstItemId
            self.assertEquals(first, indexed.firstItemId())

            # lastItemId
            self.assertEquals(last, indexed.lastItemId())

            # nextItemId
            self.assertEquals(itemIdList[1], indexed.nextItemId(first))

            # prevItemId
            self.assertEquals(itemIdList[len(itemIdList) - 2],
                    indexed.prevItemId(last))

            # isFirstId
            self.assertTrue(indexed.isFirstId(first))
            self.assertFalse(indexed.isFirstId(last))

            # isLastId
            self.assertTrue(indexed.isLastId(last))
            self.assertFalse(indexed.isLastId(first))

            # indexOfId
            self.assertEquals(0, indexed.indexOfId(first))
            self.assertEquals(expectedSize - 1, indexed.indexOfId(last))

            # getIdByIndex
            self.assertEquals(indexed.getIdByIndex(0), first)
            self.assertEquals(indexed.getIdByIndex(expectedSize - 1), last)


    FULLY_QUALIFIED_NAME = 'fullyQualifiedName'
    SIMPLE_NAME = 'simpleName'
    REVERSE_FULLY_QUALIFIED_NAME = 'reverseFullyQualifiedName'
    ID_NUMBER = 'idNumber'


    def _testBasicContainerOperations(self, container):
        self.initializeContainer(container)
        # Basic container
        self.validateContainer(container, self.sampleData[0],
                self.sampleData[len(self.sampleData) - 1], self.sampleData[10],
                'abc', True, len(self.sampleData))


    def _testContainerOrdered(self, container):
        idd = container.addItem()
        self.assertIsNotNone(idd)
        item = container.getItem(idd)
        self.assertIsNotNone(item)

        self.assertEquals(idd, container.firstItemId())
        self.assertEquals(idd, container.lastItemId())

        # isFirstId
        self.assertTrue(container.isFirstId(idd))
        self.assertTrue(container.isFirstId(container.firstItemId()))

        # isLastId
        self.assertTrue(container.isLastId(idd))
        self.assertTrue(container.isLastId(container.lastItemId()))

        # Add a new item before the first
        # addItemAfter
        newFirstId = container.addItemAfter(None)
        self.assertIsNotNone(newFirstId)
        self.assertIsNotNone(container.getItem(newFirstId))

        # isFirstId
        self.assertTrue(container.isFirstId(newFirstId))
        self.assertTrue(container.isFirstId(container.firstItemId()))

        # isLastId
        self.assertTrue(container.isLastId(idd))
        self.assertTrue(container.isLastId(container.lastItemId()))

        # nextItemId
        self.assertEquals(idd, container.nextItemId(newFirstId))
        self.assertIsNone(container.nextItemId(idd))
        self.assertIsNone(container.nextItemId('not-in-container'))

        # prevItemId
        self.assertEquals(newFirstId, container.prevItemId(idd))
        self.assertIsNone(container.prevItemId(newFirstId))
        self.assertIsNone(container.prevItemId('not-in-container'))

        # addItemAfter(Object)
        newSecondItemId = container.addItemAfter(newFirstId)
        # order is now: newFirstId, newSecondItemId, idd
        self.assertIsNotNone(newSecondItemId)
        self.assertIsNotNone(container.getItem(newSecondItemId))
        self.assertEquals(idd, container.nextItemId(newSecondItemId))
        self.assertEquals(newFirstId, container.prevItemId(newSecondItemId))

        # addItemAfter(Object,Object)
        fourthId = 'id of the fourth item'
        fourth = container.addItemAfter(newFirstId, fourthId)
        # order is now: newFirstId, fourthId, newSecondItemId, id
        self.assertIsNotNone(fourth)
        self.assertEquals(fourth, container.getItem(fourthId))
        self.assertEquals(newSecondItemId, container.nextItemId(fourthId))
        self.assertEquals(newFirstId, container.prevItemId(fourthId))

        # addItemAfter(Object,Object)
        fifthId = object()
        fifth = container.addItemAfter(None, fifthId)
        # order is now: fifthId, newFirstId, fourthId, newSecondItemId, id
        self.assertIsNotNone(fifth)
        self.assertEquals(fifth, container.getItem(fifthId))
        self.assertEquals(newFirstId, container.nextItemId(fifthId))
        self.assertIsNone(container.prevItemId(fifthId))


    def _testContainerIndexed(self, container, itemId, itemPosition,
                testAddEmptyItemAt, newItemId, testAddItemAtWithId):
        self.initializeContainer(container)

        # indexOfId
        self.assertEquals(itemPosition, container.indexOfId(itemId))

        # getIdByIndex
        self.assertEquals(itemId, container.getIdByIndex(itemPosition))

        # addItemAt
        if testAddEmptyItemAt:
            addedId = container.addItemAt(itemPosition)
            self.assertEquals(itemPosition, container.indexOfId(addedId))
            self.assertEquals(itemPosition + 1, container.indexOfId(itemId))
            self.assertEquals(addedId, container.getIdByIndex(itemPosition))
            self.assertEquals(itemId, container.getIdByIndex(itemPosition + 1))

            newFirstId = container.addItemAt(0)
            self.assertEquals(0, container.indexOfId(newFirstId))
            self.assertEquals(itemPosition + 2, container.indexOfId(itemId))
            self.assertEquals(newFirstId, container.firstItemId())
            self.assertEquals(newFirstId, container.getIdByIndex(0))
            self.assertEquals(itemId, container.getIdByIndex(itemPosition + 2))

            newLastId = container.addItemAt(len(container))
            self.assertEquals(len(container) - 1,
                    container.indexOfId(newLastId))
            self.assertEquals(itemPosition + 2,
                    container.indexOfId(itemId))
            self.assertEquals(newLastId,
                    container.lastItemId())
            self.assertEquals(newLastId,
                    container.getIdByIndex(len(container) - 1))
            self.assertEquals(itemId,
                    container.getIdByIndex(itemPosition + 2))

            self.assertTrue(container.removeItem(addedId))
            self.assertTrue(container.removeItem(newFirstId))
            self.assertTrue(container.removeItem(newLastId))

            self.assertFalse(container.removeItem(addedId),
                    'Removing non-existing item should indicate failure')

        # addItemAt
        if testAddItemAtWithId:
            container.addItemAt(itemPosition, newItemId)
            self.assertEquals(itemPosition, container.indexOfId(newItemId))
            self.assertEquals(itemPosition + 1, container.indexOfId(itemId))
            self.assertEquals(newItemId, container.getIdByIndex(itemPosition))
            self.assertEquals(itemId, container.getIdByIndex(itemPosition + 1))
            self.assertTrue(container.removeItem(newItemId))
            self.assertFalse(container.containsId(newItemId))

            container.addItemAt(0, newItemId)
            self.assertEquals(0, container.indexOfId(newItemId))
            self.assertEquals(itemPosition + 1, container.indexOfId(itemId))
            self.assertEquals(newItemId, container.firstItemId())
            self.assertEquals(newItemId, container.getIdByIndex(0))
            self.assertEquals(itemId, container.getIdByIndex(itemPosition + 1))
            self.assertTrue(container.removeItem(newItemId))
            self.assertFalse(container.containsId(newItemId))

            container.addItemAt(len(container), newItemId)
            self.assertEquals(len(container) - 1,
                    container.indexOfId(newItemId))
            self.assertEquals(itemPosition,
                    container.indexOfId(itemId))
            self.assertEquals(newItemId,
                    container.lastItemId())
            self.assertEquals(newItemId,
                    container.getIdByIndex(len(container) - 1))
            self.assertEquals(itemId,
                    container.getIdByIndex(itemPosition))

            self.assertTrue(container.removeItem(newItemId))
            self.assertFalse(container.containsId(newItemId))


    def _testContainerFiltering(self, container):
        self.initializeContainer(container)

        # Filter by "contains ab"
        f = SimpleStringFilter(self.FULLY_QUALIFIED_NAME, 'ab', False, False)
        container.addContainerFilter(f)

        self.validateContainer(container,
                'com.vaadin.data.BufferedValidatable',
                'com.vaadin.ui.TabSheet',
                'com.vaadin.terminal.gwt.client.Focusable',
                'com.vaadin.data.Buffered',
                self.isFilteredOutItemNull(), 20)

        # Filter by "contains da" (reversed as ad here)
        container.removeAllContainerFilters()
        f = SimpleStringFilter(self.REVERSE_FULLY_QUALIFIED_NAME, 'ad',
                False, False)
        container.addContainerFilter(f)

        self.validateContainer(container,
                'com.vaadin.data.Buffered',
                'com.vaadin.terminal.gwt.server.ComponentSizeValidator',
                'com.vaadin.data.util.IndexedContainer',
                'com.vaadin.terminal.gwt.client.ui.VUriFragmentUtility',
                self.isFilteredOutItemNull(), 37)


    def isFilteredOutItemNull(self):
        """Override in subclasses to return false if the container getItem()
        method returns a non-null value for an item that has been filtered out.

        @return
        """
        return True


    def _testContainerSortingAndFiltering(self, sortable):
        filterable = sortable

        self.initializeContainer(sortable)

        # Filter by "contains ab"
        f = SimpleStringFilter(self.FULLY_QUALIFIED_NAME, 'ab', False, False)
        filterable.addContainerFilter(f)

        # Must be able to sort based on PROP1 for this test
        self.assertTrue(self.FULLY_QUALIFIED_NAME in \
                sortable.getSortableContainerPropertyIds())

        sortable.sort([self.FULLY_QUALIFIED_NAME], [True])

        self.validateContainer(sortable,
                'com.vaadin.data.BufferedValidatable',
                'com.vaadin.ui.TableFieldFactory',
                'com.vaadin.ui.TableFieldFactory',
                'com.vaadin.data.util.BeanItem',
                self.isFilteredOutItemNull(), 20)


    def _testContainerSorting(self, container):
        sortable = container

        self.initializeContainer(container)

        # Must be able to sort based on PROP1 for this test
        self.assertTrue(self.FULLY_QUALIFIED_NAME in \
                sortable.getSortableContainerPropertyIds())

        self.assertTrue(self.REVERSE_FULLY_QUALIFIED_NAME in \
                sortable.getSortableContainerPropertyIds())

        sortable.sort([self.FULLY_QUALIFIED_NAME], [True])

        self.validateContainer(container,
                'com.vaadin.Application',
                'org.vaadin.test.LastClass',
                'com.vaadin.terminal.ApplicationResource',
                'blah', True, len(self.sampleData))

        sortable.sort([self.REVERSE_FULLY_QUALIFIED_NAME], [True])

        self.validateContainer(container,
                'com.vaadin.terminal.gwt.server.ApplicationPortlet2',
                'com.vaadin.data.util.ObjectProperty',
                'com.vaadin.ui.BaseFieldFactory',
                'blah', True, len(self.sampleData))


    def initializeContainer(self, container):
        self.assertTrue(container.removeAllItems())
        propertyIds = list(container.getContainerPropertyIds())
        for propertyId in propertyIds:
            container.removeContainerProperty(propertyId)

        container.addContainerProperty(self.FULLY_QUALIFIED_NAME, str, '')
        container.addContainerProperty(self.SIMPLE_NAME, str, '')
        container.addContainerProperty(self.REVERSE_FULLY_QUALIFIED_NAME,
                str, None)
        container.addContainerProperty(self.ID_NUMBER, int, None)

        for i in range(len(self.sampleData)):
            idd = self.sampleData[i]
            item = container.addItem(idd)
            item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(
                    self.sampleData[i])
            item.getItemProperty(self.SIMPLE_NAME).setValue(
                    self.getSimpleName(self.sampleData[i]))
            item.getItemProperty(self.REVERSE_FULLY_QUALIFIED_NAME).setValue(
                    self.reverse(self.sampleData[i]))
            item.getItemProperty(self.ID_NUMBER).setValue(i)


    @classmethod
    def getSimpleName(cls, name):
        if '.' in name:
            return name[name.rfind('.') + 1:]
        else:
            return name

    @classmethod
    def reverse(cls, string):
        return string[::-1]

    sampleData = [
            'com.vaadin.annotations.AutoGenerated',
            'com.vaadin.Application',
            'com.vaadin.data.Buffered',
            'com.vaadin.data.BufferedValidatable',
            'com.vaadin.data.Container',
            'com.vaadin.data.Item',
            'com.vaadin.data.Property',
            'com.vaadin.data.util.BeanItem',
            'com.vaadin.data.util.BeanItemContainer',
            'com.vaadin.data.util.ContainerHierarchicalWrapper',
            'com.vaadin.data.util.ContainerOrderedWrapper',
            'com.vaadin.data.util.DefaultItemSorter',
            'com.vaadin.data.util.FilesystemContainer',
            'com.vaadin.data.util.Filter',
            'com.vaadin.data.util.HierarchicalContainer',
            'com.vaadin.data.util.IndexedContainer',
            'com.vaadin.data.util.ItemSorter',
            'com.vaadin.data.util.MethodProperty',
            'com.vaadin.data.util.ObjectProperty',
            'com.vaadin.data.util.PropertyFormatter',
            'com.vaadin.data.util.PropertysetItem',
            'com.vaadin.data.util.QueryContainer',
            'com.vaadin.data.util.TextFileProperty',
            'com.vaadin.data.Validatable',
            'com.vaadin.data.validator.AbstractStringValidator',
            'com.vaadin.data.validator.AbstractValidator',
            'com.vaadin.data.validator.CompositeValidator',
            'com.vaadin.data.validator.DoubleValidator',
            'com.vaadin.data.validator.EmailValidator',
            'com.vaadin.data.validator.IntegerValidator',
            'com.vaadin.data.validator.NullValidator',
            'com.vaadin.data.validator.RegexpValidator',
            'com.vaadin.data.validator.StringLengthValidator',
            'com.vaadin.data.Validator',
            'com.vaadin.event.Action',
            'com.vaadin.event.ComponentEventListener',
            'com.vaadin.event.EventRouter',
            'com.vaadin.event.FieldEvents',
            'com.vaadin.event.ItemClickEvent',
            'com.vaadin.event.LayoutEvents',
            'com.vaadin.event.ListenerMethod',
            'com.vaadin.event.MethodEventSource',
            'com.vaadin.event.MouseEvents',
            'com.vaadin.event.ShortcutAction',
            'com.vaadin.launcher.DemoLauncher',
            'com.vaadin.launcher.DevelopmentServerLauncher',
            'com.vaadin.launcher.util.BrowserLauncher',
            'com.vaadin.service.ApplicationContext',
            'com.vaadin.service.FileTypeResolver',
            'com.vaadin.terminal.ApplicationResource',
            'com.vaadin.terminal.ClassResource',
            'com.vaadin.terminal.CompositeErrorMessage',
            'com.vaadin.terminal.DownloadStream',
            'com.vaadin.terminal.ErrorMessage',
            'com.vaadin.terminal.ExternalResource',
            'com.vaadin.terminal.FileResource',
            'com.vaadin.terminal.gwt.client.ApplicationConfiguration',
            'com.vaadin.terminal.gwt.client.ApplicationConnection',
            'com.vaadin.terminal.gwt.client.BrowserInfo',
            'com.vaadin.terminal.gwt.client.ClientExceptionHandler',
            'com.vaadin.terminal.gwt.client.ComponentDetail',
            'com.vaadin.terminal.gwt.client.ComponentDetailMap',
            'com.vaadin.terminal.gwt.client.ComponentLocator',
            'com.vaadin.terminal.gwt.client.Console',
            'com.vaadin.terminal.gwt.client.Container',
            'com.vaadin.terminal.gwt.client.ContainerResizedListener',
            'com.vaadin.terminal.gwt.client.CSSRule',
            'com.vaadin.terminal.gwt.client.DateTimeService',
            'com.vaadin.terminal.gwt.client.DefaultWidgetSet',
            'com.vaadin.terminal.gwt.client.Focusable',
            'com.vaadin.terminal.gwt.client.HistoryImplIEVaadin',
            'com.vaadin.terminal.gwt.client.LocaleNotLoadedException',
            'com.vaadin.terminal.gwt.client.LocaleService',
            'com.vaadin.terminal.gwt.client.MouseEventDetails',
            'com.vaadin.terminal.gwt.client.NullConsole',
            'com.vaadin.terminal.gwt.client.Paintable',
            'com.vaadin.terminal.gwt.client.RenderInformation',
            'com.vaadin.terminal.gwt.client.RenderSpace',
            'com.vaadin.terminal.gwt.client.StyleConstants',
            'com.vaadin.terminal.gwt.client.TooltipInfo',
            'com.vaadin.terminal.gwt.client.ui.Action',
            'com.vaadin.terminal.gwt.client.ui.ActionOwner',
            'com.vaadin.terminal.gwt.client.ui.AlignmentInfo',
            'com.vaadin.terminal.gwt.client.ui.CalendarEntry',
            'com.vaadin.terminal.gwt.client.ui.ClickEventHandler',
            'com.vaadin.terminal.gwt.client.ui.Field',
            'com.vaadin.terminal.gwt.client.ui.Icon',
            'com.vaadin.terminal.gwt.client.ui.layout.CellBasedLayout',
            'com.vaadin.terminal.gwt.client.ui.layout.ChildComponentContainer',
            'com.vaadin.terminal.gwt.client.ui.layout.Margins',
            'com.vaadin.terminal.gwt.client.ui.LayoutClickEventHandler',
            'com.vaadin.terminal.gwt.client.ui.MenuBar',
            'com.vaadin.terminal.gwt.client.ui.MenuItem',
            'com.vaadin.terminal.gwt.client.ui.richtextarea.VRichTextArea',
            'com.vaadin.terminal.gwt.client.ui.richtextarea.VRichTextToolbar',
            'com.vaadin.terminal.gwt.client.ui.ShortcutActionHandler',
            'com.vaadin.terminal.gwt.client.ui.SubPartAware',
            'com.vaadin.terminal.gwt.client.ui.Table',
            'com.vaadin.terminal.gwt.client.ui.TreeAction',
            'com.vaadin.terminal.gwt.client.ui.TreeImages',
            'com.vaadin.terminal.gwt.client.ui.VAbsoluteLayout',
            'com.vaadin.terminal.gwt.client.ui.VAccordion',
            'com.vaadin.terminal.gwt.client.ui.VButton',
            'com.vaadin.terminal.gwt.client.ui.VCalendarPanel',
            'com.vaadin.terminal.gwt.client.ui.VCheckBox',
            'com.vaadin.terminal.gwt.client.ui.VContextMenu',
            'com.vaadin.terminal.gwt.client.ui.VCssLayout',
            'com.vaadin.terminal.gwt.client.ui.VCustomComponent',
            'com.vaadin.terminal.gwt.client.ui.VCustomLayout',
            'com.vaadin.terminal.gwt.client.ui.VDateField',
            'com.vaadin.terminal.gwt.client.ui.VDateFieldCalendar',
            'com.vaadin.terminal.gwt.client.ui.VEmbedded',
            'com.vaadin.terminal.gwt.client.ui.VFilterSelect',
            'com.vaadin.terminal.gwt.client.ui.VForm',
            'com.vaadin.terminal.gwt.client.ui.VFormLayout',
            'com.vaadin.terminal.gwt.client.ui.VGridLayout',
            'com.vaadin.terminal.gwt.client.ui.VHorizontalLayout',
            'com.vaadin.terminal.gwt.client.ui.VLabel',
            'com.vaadin.terminal.gwt.client.ui.VLink',
            'com.vaadin.terminal.gwt.client.ui.VListSelect',
            'com.vaadin.terminal.gwt.client.ui.VMarginInfo',
            'com.vaadin.terminal.gwt.client.ui.VMenuBar',
            'com.vaadin.terminal.gwt.client.ui.VNativeButton',
            'com.vaadin.terminal.gwt.client.ui.VNativeSelect',
            'com.vaadin.terminal.gwt.client.ui.VNotification',
            'com.vaadin.terminal.gwt.client.ui.VOptionGroup',
            'com.vaadin.terminal.gwt.client.ui.VOptionGroupBase',
            'com.vaadin.terminal.gwt.client.ui.VOrderedLayout',
            'com.vaadin.terminal.gwt.client.ui.VOverlay',
            'com.vaadin.terminal.gwt.client.ui.VPanel',
            'com.vaadin.terminal.gwt.client.ui.VPasswordField',
            'com.vaadin.terminal.gwt.client.ui.VPopupCalendar',
            'com.vaadin.terminal.gwt.client.ui.VPopupView',
            'com.vaadin.terminal.gwt.client.ui.VProgressIndicator',
            'com.vaadin.terminal.gwt.client.ui.VScrollTable',
            'com.vaadin.terminal.gwt.client.ui.VSlider',
            'com.vaadin.terminal.gwt.client.ui.VSplitPanel',
            'com.vaadin.terminal.gwt.client.ui.VSplitPanelHorizontal',
            'com.vaadin.terminal.gwt.client.ui.VSplitPanelVertical',
            'com.vaadin.terminal.gwt.client.ui.VTablePaging',
            'com.vaadin.terminal.gwt.client.ui.VTabsheet',
            'com.vaadin.terminal.gwt.client.ui.VTabsheetBase',
            'com.vaadin.terminal.gwt.client.ui.VTabsheetPanel',
            'com.vaadin.terminal.gwt.client.ui.VTextArea',
            'com.vaadin.terminal.gwt.client.ui.VTextField',
            'com.vaadin.terminal.gwt.client.ui.VTextualDate',
            'com.vaadin.terminal.gwt.client.ui.VTime',
            'com.vaadin.terminal.gwt.client.ui.VTree',
            'com.vaadin.terminal.gwt.client.ui.VTwinColSelect',
            'com.vaadin.terminal.gwt.client.ui.VUnknownComponent',
            'com.vaadin.terminal.gwt.client.ui.VUpload',
            'com.vaadin.terminal.gwt.client.ui.VUriFragmentUtility',
            'com.vaadin.terminal.gwt.client.ui.VVerticalLayout',
            'com.vaadin.terminal.gwt.client.ui.VView',
            'com.vaadin.terminal.gwt.client.ui.VWindow',
            'com.vaadin.terminal.gwt.client.UIDL',
            'com.vaadin.terminal.gwt.client.Util',
            'com.vaadin.terminal.gwt.client.ValueMap',
            'com.vaadin.terminal.gwt.client.VCaption',
            'com.vaadin.terminal.gwt.client.VCaptionWrapper',
            'com.vaadin.terminal.gwt.client.VDebugConsole',
            'com.vaadin.terminal.gwt.client.VErrorMessage',
            'com.vaadin.terminal.gwt.client.VTooltip',
            'com.vaadin.terminal.gwt.client.VUIDLBrowser',
            'com.vaadin.terminal.gwt.client.WidgetMap',
            'com.vaadin.terminal.gwt.client.WidgetSet',
            'com.vaadin.terminal.gwt.server.AbstractApplicationPortlet',
            'com.vaadin.terminal.gwt.server.AbstractApplicationServlet',
            'com.vaadin.terminal.gwt.server.AbstractCommunicationManager',
            'com.vaadin.terminal.gwt.server.AbstractWebApplicationContext',
            'com.vaadin.terminal.gwt.server.ApplicationPortlet',
            'com.vaadin.terminal.gwt.server.ApplicationPortlet2',
            'com.vaadin.terminal.gwt.server.ApplicationRunnerServlet',
            'com.vaadin.terminal.gwt.server.ApplicationServlet',
            'com.vaadin.terminal.gwt.server.ChangeVariablesErrorEvent',
            'com.vaadin.terminal.gwt.server.CommunicationManager',
            'com.vaadin.terminal.gwt.server.ComponentSizeValidator',
            'com.vaadin.terminal.gwt.server.Constants',
            'com.vaadin.terminal.gwt.server.GAEApplicationServlet',
            'com.vaadin.terminal.gwt.server.HttpServletRequestListener',
            'com.vaadin.terminal.gwt.server.HttpUploadStream',
            'com.vaadin.terminal.gwt.server.JsonPaintTarget',
            'com.vaadin.terminal.gwt.server.PortletApplicationContext',
            'com.vaadin.terminal.gwt.server.PortletApplicationContext2',
            'com.vaadin.terminal.gwt.server.PortletCommunicationManager',
            'com.vaadin.terminal.gwt.server.PortletRequestListener',
            'com.vaadin.terminal.gwt.server.RestrictedRenderResponse',
            'com.vaadin.terminal.gwt.server.SessionExpiredException',
            'com.vaadin.terminal.gwt.server.SystemMessageException',
            'com.vaadin.terminal.gwt.server.WebApplicationContext',
            'com.vaadin.terminal.gwt.server.WebBrowser',
            'com.vaadin.terminal.gwt.widgetsetutils.ClassPathExplorer',
            'com.vaadin.terminal.gwt.widgetsetutils.WidgetMapGenerator',
            'com.vaadin.terminal.gwt.widgetsetutils.WidgetSetBuilder',
            'com.vaadin.terminal.KeyMapper',
            'com.vaadin.terminal.Paintable',
            'com.vaadin.terminal.PaintException',
            'com.vaadin.terminal.PaintTarget',
            'com.vaadin.terminal.ParameterHandler',
            'com.vaadin.terminal.Resource',
            'com.vaadin.terminal.Scrollable',
            'com.vaadin.terminal.Sizeable',
            'com.vaadin.terminal.StreamResource',
            'com.vaadin.terminal.SystemError',
            'com.vaadin.terminal.Terminal',
            'com.vaadin.terminal.ThemeResource',
            'com.vaadin.terminal.UploadStream',
            'com.vaadin.terminal.URIHandler',
            'com.vaadin.terminal.UserError',
            'com.vaadin.terminal.VariableOwner',
            'com.vaadin.tools.ReflectTools',
            'com.vaadin.tools.WidgetsetCompiler',
            'com.vaadin.ui.AbsoluteLayout',
            'com.vaadin.ui.AbstractComponent',
            'com.vaadin.ui.AbstractComponentContainer',
            'com.vaadin.ui.AbstractField',
            'com.vaadin.ui.AbstractLayout',
            'com.vaadin.ui.AbstractOrderedLayout',
            'com.vaadin.ui.AbstractSelect',
            'com.vaadin.ui.Accordion',
            'com.vaadin.ui.Alignment',
            'com.vaadin.ui.AlignmentUtils',
            'com.vaadin.ui.BaseFieldFactory',
            'com.vaadin.ui.Button',
            'com.vaadin.ui.CheckBox',
            'com.vaadin.ui.ClientWidget',
            'com.vaadin.ui.ComboBox',
            'com.vaadin.ui.Component',
            'com.vaadin.ui.ComponentContainer',
            'com.vaadin.ui.CssLayout',
            'com.vaadin.ui.CustomComponent',
            'com.vaadin.ui.CustomLayout',
            'com.vaadin.ui.DateField',
            'com.vaadin.ui.DefaultFieldFactory',
            'com.vaadin.ui.Embedded',
            'com.vaadin.ui.ExpandLayout',
            'com.vaadin.ui.Field',
            'com.vaadin.ui.FieldFactory',
            'com.vaadin.ui.Form',
            'com.vaadin.ui.FormFieldFactory',
            'com.vaadin.ui.FormLayout',
            'com.vaadin.ui.GridLayout',
            'com.vaadin.ui.HorizontalLayout',
            'com.vaadin.ui.InlineDateField',
            'com.vaadin.ui.Label',
            'com.vaadin.ui.Layout',
            'com.vaadin.ui.Link',
            'com.vaadin.ui.ListSelect',
            'com.vaadin.ui.LoginForm',
            'com.vaadin.ui.MenuBar',
            'com.vaadin.ui.NativeButton',
            'com.vaadin.ui.NativeSelect',
            'com.vaadin.ui.OptionGroup',
            'com.vaadin.ui.OrderedLayout',
            'com.vaadin.ui.Panel',
            'com.vaadin.ui.PopupDateField',
            'com.vaadin.ui.PopupView',
            'com.vaadin.ui.ProgressIndicator',
            'com.vaadin.ui.RichTextArea',
            'com.vaadin.ui.Select',
            'com.vaadin.ui.Slider',
            'com.vaadin.ui.SplitPanel',
            'com.vaadin.ui.Table',
            'com.vaadin.ui.TableFieldFactory',
            'com.vaadin.ui.TabSheet',
            'com.vaadin.ui.TextField',
            'com.vaadin.ui.Tree',
            'com.vaadin.ui.TwinColSelect',
            'com.vaadin.ui.Upload',
            'com.vaadin.ui.UriFragmentUtility',
            'com.vaadin.ui.VerticalLayout',
            'com.vaadin.ui.Window',
            'com.vaadin.util.SerializerHelper',
            'org.vaadin.test.LastClass'
    ]


class AbstractEventCounter(object):
    """Helper class for testing e.g. listeners expecting events to be
    fired."""

    def __init__(self):
        self._eventCount = 0
        self._lastAssertedEventCount = 0


    def increment(self):
        """Increment the event count. To be called by subclasses e.g. from
        a listener method.
        """
        self._eventCount += 1


    def assertNone(self):
        """Check that no one event has occurred since the previous assert
        call."""
        assert self._lastAssertedEventCount == self._eventCount


    def assertOnce(self):
        """Check that exactly one event has occurred since the previous
        assert call.
        """
        self._lastAssertedEventCount += 1
        assert self._lastAssertedEventCount == self._eventCount


    def reset(self):
        """Reset the counter and the expected count."""
        self._eventCount = 0
        self._lastAssertedEventCount = 0


class ItemSetChangeCounter(AbstractEventCounter, IItemSetChangeListener):
    """Test class for counting item set change events and verifying they
    have been received.
    """

    def containerItemSetChange(self, event):
        self.increment()
