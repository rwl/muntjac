
from muntjac.demo.sampler.features.table import \
    (TableFooter, TableColumnHeaders, TableMultipleSelection,
     TableClickListeners, TableColumnAlignment, TableActions, TableRowHeaders,
     TableColumnReordering, TableRowStyling, TableMouseEvents,
     TableHeaderIcons, TableSorting, TableLazyLoading, TableCellStyling,
     TableKeyboardNavigation, TableColumnCollapsing)

from muntjac.demo.sampler.features.selects import \
    (OptionGroupDisabledItems, TwinColumnSelect, ComboBoxPlain, OptionGroups,
     ComboBoxInputPrompt, ComboBoxContains, NativeSelection, ComboBoxNewItems,
     ComboBoxStartsWith, ListSelectMultiple, ListSelectSingle)

from muntjac.demo.sampler.features.windows import \
    (SubwindowPositioned, SubwindowClose, SubwindowModal, SubwindowAutoSized,
     Subwindow, SubwindowSized, NativeWindow)

from muntjac.demo.sampler.features.layouts import \
    (CustomLayouts, SplitPanelBasic, SplitPanelPositioning, WebLayout,
     CssLayouts, LayoutSpacing, VerticalLayoutBasic, HorizontalLayoutBasic,
     ExpandingComponent, LayoutAlignment, ClickableLayoutBasic, LayoutMargin,
     GridLayoutBasic, ApplicationLayout, AbsoluteLayoutBasic)

from muntjac.demo.sampler.features.commons import \
    JSApi, Icons, Tooltips, BrowserInformation, PackageIcons, Errors

from muntjac.demo.sampler.features.text import \
    (LabelPlain, LabelPreformatted, TextFieldSingle, LabelRich,
     TextFieldTextChangeEvent, TextArea, RichTextEditor, TextFieldInputPrompt,
     TextFieldSecret)

from muntjac.demo.sampler.features.tabsheets import \
    TabSheetClosing, TabSheetIcons, TabSheetScrolling, TabSheetDisabled

from muntjac.demo.sampler.features.panels import PanelBasic, PanelLight

from muntjac.demo.sampler.features.menubar import \
    (MenuBarTooltips, MenuBarHiddenItems, BasicMenuBar,
     MenuBarKeyboardNavigation, MenuBarCheckableItems, MenuBarWithIcons,
     MenuBarCollapsing, MenuBarItemStyles)

from muntjac.demo.sampler.features.dates import \
    (DateLocale, DatePopupInputPrompt, DateInline, DatePopup, DateResolution,
     DatePopupKeyboardNavigation)

from muntjac.demo.sampler.features.notifications import \
    (NotificationError, NotificationWarning, NotificationHumanized,
     NotificationCustom, NotificationTray)

from muntjac.demo.sampler.features.trees import \
    (TreeKeyboardNavigation, TreeMouseEvents, TreeSingleSelect,
     TreeMultiSelect, TreeActions)

from muntjac.demo.sampler.features.dragndrop import \
    (DragDropTreeSorting, DragDropHtml5FromDesktop, DragDropTableTree,
     DragDropServerValidation, DragDropRearrangeComponents)

from muntjac.demo.sampler.features.upload import \
    UploadBasic, ImmediateUpload, UploadWithProgressMonitoring

from muntjac.demo.sampler.features.link import \
    LinkCurrentWindow, LinkNoDecorations, LinkSizedWindow

from muntjac.demo.sampler.features.shortcuts import \
    ShortcutScope, ShortcutBasics

from muntjac.demo.sampler.features.form import \
    LoginForm, FormBasic, FormAdvancedLayout

from muntjac.demo.sampler.features.accordions import \
    AccordionDisabled, AccordionIcons

from muntjac.demo.sampler.features.popupviews import \
    PopupViewClosing, PopupViewContents

from muntjac.demo.sampler.features.embedded import \
    ImageEmbed, WebEmbed, FlashEmbed

from muntjac.demo.sampler.features.buttons import \
    ButtonLink, ButtonPush, CheckBoxes

from muntjac.demo.sampler.features.slider import \
    SliderVertical, SliderHorizontal, SliderKeyboardNavigation

from muntjac.demo.sampler.features.progressindicator import ProgressIndicators

from muntjac.demo.sampler.features.blueprints import ProminentPrimaryAction

from muntjac.demo.sampler.Feature import Version, Feature

from muntjac.data.util.hierarchical_container import HierarchicalContainer


class FeatureSet(Feature):
    """Contains the FeatureSet implementation and the structure for the feature
    'tree'.

    Each set is implemented as it's own class to facilitate linking to sets in
    the same way as linking to individual features.
    """

    FEATURES = None

    _pathnameToFeature = None

    def getSinceVersion(self):
        return Version.OLD


    def __init__(self, *args):
        super(FeatureSet, self).__init__()

        self._pathname = None
        self._name = None
        self._desc = None
        self._icon = 'folder.gif'
        self._content = None
        self._container = None
        self._containerRecursive = False

        nargs = len(args)
        if nargs == 2:
            pathname, content = args
            FeatureSet.__init__(self, pathname, pathname, '', content)
        elif nargs == 3:
            pathname, name, content = args
            FeatureSet.__init__(self, pathname, name, '', content)
        elif nargs == 4:
            pathname, name, desc, content = args
            self._pathname = pathname
            self._name = name
            self._desc = desc
            self._content = content
            FeatureSet.addFeature(self)
            if content is not None:
                for f in content:
                    if isinstance(f, FeatureSet):
                        continue
                    FeatureSet.addFeature(f)
        else:
            raise ValueError


    @classmethod
    def addFeature(cls, f):
        if cls._pathnameToFeature is None:
            cls._pathnameToFeature = dict()

        if f.getFragmentName() in cls._pathnameToFeature:
            raise ValueError, ('Duplicate pathname for '
                    + f.getFragmentName() + ': '
                    + cls._pathnameToFeature[f.getFragmentName()].__class__
                    + ' / ' + f.__class__)

        cls._pathnameToFeature[f.getFragmentName()] = f


    def getFeature(self, pathname):
        return self._pathnameToFeature.get(pathname)


    def getFeatures(self):
        return self._content


    def getContainer(self, recurse):
        if self._container is None or self._containerRecursive != recurse:
            self._container = HierarchicalContainer()
            self._container.addContainerProperty(self.PROPERTY_NAME,
                    str, '')
            self._container.addContainerProperty(self.PROPERTY_DESCRIPTION,
                    str, '')
            # fill
            self.addFeatures(self, self._container, recurse)
        return self._container


    def addFeatures(self, f, c, recurse):
        features = f.getFeatures()
        for i in range(len(features)):
            item = c.addItem(features[i])
            prop = item.getItemProperty(self.PROPERTY_NAME)
            prop.setValue(features[i].getName())
            prop = item.getItemProperty(self.PROPERTY_DESCRIPTION)
            prop.setValue(features[i].getDescription())
            if recurse:
                c.setParent(features[i], f)
                if isinstance(features[i], FeatureSet):
                    self.addFeatures(features[i], c, recurse)
            if not isinstance(features[i], FeatureSet):
                c.setChildrenAllowed(features[i], False)


    def getDescription(self):
        return self._desc


    def getFragmentName(self):
        return self._pathname


    def getName(self):
        return self._name


    def getIconName(self):
        return self._icon


    def getRelatedAPI(self):
        return None


    def getRelatedFeatures(self):
        return None


    def getRelatedResources(self):
        return None


class Blueprints(FeatureSet):

    def __init__(self):
        super(Blueprints, self).__init__('Blueprints',
                [ProminentPrimaryAction()])


class Basics(FeatureSet):

    def __init__(self):
        super(Basics, self).__init__('Basics',
                'UI Basics',
                'The building blocks of any web application interface',
                [Tooltips(),
                 Icons(),
                 PackageIcons(),
                 Errors(),
#                 ProgressIndicators(),
                 JSApi(),
                 BrowserInformation(),
                 Buttons(),
                 Links(),
                 Texts(),
                 Embedding(),
                 Shortcuts()])


class Shortcuts(FeatureSet):

    def __init__(self):
        super(Shortcuts, self).__init__('Shortcuts',
                'Keyboard shortcuts',
                'Binding keyboard shortcuts to actions',
                [ShortcutBasics(),
                 ShortcutScope()])


    def getSinceVersion(self):
        return Version.V63


class ValueInput(FeatureSet):

    def __init__(self):
        super(ValueInput, self).__init__('Input',
                'Value Input Components',
                'Components used for gathering input from the user',
                [Dates(),
                 TextFields(),
                 Selects(),
                 Sliders(),
#                 Uploads()
                 ])


class FormsAndData(FeatureSet):

    def __init__(self):
        super(FormsAndData, self).__init__('FormsAndData',
                'Forms and Data Model',
                'Grouping fields and data manipulation samples',
                [Forms()])


class GridsAndTrees(FeatureSet):

    def __init__(self):
        super(GridsAndTrees, self).__init__('GridsAndTrees',
                'Grids and Trees',
                'For large sets of data, the Table (Grid) and Tree components come in handy',
                [Tables(),
                 Trees()])


class Layouting(FeatureSet):

    def __init__(self):
        super(Layouting, self).__init__('ComponentContainers',
                'Layouts & Component Containers',
                'Laying out and grouping components together',
                [Layouts(),
                 Panels(),
                 Tabsheets(),
                 Accordions()])


class Windowing(FeatureSet):

    def __init__(self):
        super(Windowing, self).__init__('Windowing',
                'Windows, Popups and Navigation',
                '',
                [MenuBars(),
                 Windows(),
                 PopupViews(),
                 Notifications()])


class Buttons(FeatureSet):

    def __init__(self):
        super(Buttons, self).__init__('Buttons',
                'Buttons',
                'A button is one of the fundamental building blocks of any application.',
                [ButtonPush(),
                 ButtonLink(),
                 CheckBoxes()])


class Links(FeatureSet):

    def __init__(self):
        super(Links, self).__init__('Links',
                'Links',
                ('An external link. This is the basic HTML-style link, '
                 'changing the url of the browser w/o triggering a '
                 'server-side event (like the link-styled Button).'),
                [LinkCurrentWindow(),
                 LinkNoDecorations(),
                 LinkSizedWindow()])


class MenuBars(FeatureSet):

    def __init__(self):
        super(MenuBars, self).__init__('Menubars',
                'Menubars',
                ('MenuBar has hierarchical set of actions that are presented '
                 'in drop down menus. The root level is a horizontal list of '
                 'items that open the drop down menus.'),
                [BasicMenuBar(),
                 MenuBarWithIcons(),
                 MenuBarCheckableItems(),
                 MenuBarCollapsing(),
                 MenuBarHiddenItems(),
                 MenuBarItemStyles(),
                 MenuBarKeyboardNavigation(),
                 MenuBarTooltips()])


class Notifications(FeatureSet):

    def __init__(self):
        super(Notifications, self).__init__('Notifications',
                'Notifications',
                ('Notifications are lightweight informational messages, used '
                 'to inform the user of various events.'),
                [NotificationHumanized(),
                 NotificationWarning(),
                 NotificationTray(),
                 NotificationError(),
                 NotificationCustom()])


class Selects(FeatureSet):

    def __init__(self):
        super(Selects, self).__init__('Selects',
                [ListSelectSingle(),
                 ListSelectMultiple(),
                 TwinColumnSelect(),
                 OptionGroups(),
                 OptionGroupDisabledItems(),
                 NativeSelection(),
                 ComboBoxPlain(),
                 ComboBoxInputPrompt(),
                 ComboBoxStartsWith(),
                 ComboBoxContains(),
                 ComboBoxNewItems()])


class Sliders(FeatureSet):

    def __init__(self):
        super(Sliders, self).__init__('Sliders',
                'Sliders',
                ('Slider component allows the user to select a numeric value '
                 'from a specified range of values.'),
                [SliderHorizontal(),
                 SliderVertical(),
                 SliderKeyboardNavigation()])


class Layouts(FeatureSet):

    def __init__(self):
        super(Layouts, self).__init__('Layouts',
                'Layouts',
                ('Making a usable, good looking, dynamic layout can be '
                 'tricky, but with the right tools almost anything is '
                 'possible.<br/>'),
                [LayoutMargin(),
                 LayoutSpacing(),
                 VerticalLayoutBasic(),
                 HorizontalLayoutBasic(),
                 GridLayoutBasic(),
                 AbsoluteLayoutBasic(),
                 LayoutAlignment(),
                 ExpandingComponent(),
                 SplitPanelBasic(),
                 SplitPanelPositioning(),
                 ApplicationLayout(),
                 WebLayout(),
                 CustomLayouts(),
                 CssLayouts(),
                 ClickableLayoutBasic()])


class Tabsheets(FeatureSet):

    def __init__(self):
        super(Tabsheets, self).__init__('Tabsheets',
                'Tabsheets',
                ('A Tabsheet organizes multiple components so that only the '
                 'one component associated with the currently selected '
                 '\'tab\' is shown. Typically a tab will contain a Layout, '
                 'which in turn may contain many components.'),
                [TabSheetIcons(),
                 TabSheetScrolling(),
                 TabSheetDisabled(),
                 TabSheetClosing()])


class Accordions(FeatureSet):

    def __init__(self):
        super(Accordions, self).__init__('Accordions',
                'Accordions',
                ('An accordion component is a specialized case of a tabsheet.'
                 ' Within an accordion, the tabs are organized vertically,'
                 ' and the content will be shown directly below the tab.'),
                [AccordionIcons(),
                 AccordionDisabled()])


class Panels(FeatureSet):

    def __init__(self):
        super(Panels, self).__init__('Panels',
                'Panels',
                ('Panel is a simple container that supports scrolling.<br/>'
                 'It\'s internal layout (by default VerticalLayout) can be '
                 'configured or exchanged to get desired results. Components '
                 'that are added to the Panel will in effect be added to the '
                 'layout.'),
                [PanelBasic(),
                 PanelLight()])


class PopupViews(FeatureSet):

    def __init__(self):
        super(PopupViews, self).__init__('PopupViews',
                'PopupViews',
                ('PopupView is a container that allows to disclose parts of '
                 'the interface to a popup dialog. It only presents a minimal '
                 'amount of information initially.'),
                [PopupViewClosing(),
                 PopupViewContents()])


class Forms(FeatureSet):

    def __init__(self):
        super(Forms, self).__init__('Forms',
                'Forms',
                ('The Form -component provides a convenient way to organize'
                 ' related fields visually.'),
                [
#                 FormBasic(),
#                 FormAdvancedLayout(),
                 LoginForm()])


class Uploads(FeatureSet):

    def __init__(self):
        super(Uploads, self).__init__('Uploads',
                'Uploads',
                ('Upload is a component providing a method for clients to '
                 'send files to server.'),
                [UploadBasic(),
                 ImmediateUpload(),
                 UploadWithProgressMonitoring()])


class Windows(FeatureSet):

    def __init__(self):
        super(Windows, self).__init__('Windows',
                'Windows',
                ('Windows are one essential part of desktop style '
                 'applications. Windows can (for instance) organize the '
                 'UI, save space (popup windows), focus attention (modal '
                 'windows), or provide multiple views for the same data '
                 'for multitasking or dual screen setups (native browser '
                 'windows).'),
                [Subwindow(),
                 SubwindowModal(),
                 SubwindowAutoSized(),
                 SubwindowSized(),
                 SubwindowPositioned(),
                 SubwindowClose(),
                 NativeWindow()])


class Tables(FeatureSet):

    def __init__(self):
        super(Tables, self).__init__('Table (Grid)',
                'Table (Grid)',
                ('A Table, also known as a (Data)Grid, can be used to show '
                 'data in a tabular fashion. It\'s well suited for showing '
                 'large datasets.'),
                [TableHeaderIcons(),
                 TableColumnHeaders(),
                 TableFooter(),
                 TableColumnReordering(),
                 TableColumnCollapsing(),
                 TableColumnAlignment(),
                 TableCellStyling(),
                 TableSorting(),
                 TableRowHeaders(),
                 TableRowStyling(),
                 TableActions(),
                 TableMouseEvents(),
                 TableLazyLoading(),
                 TableMultipleSelection(),
                 TableClickListeners(),
                 TableKeyboardNavigation()])


class Texts(FeatureSet):

    def __init__(self):
        super(Texts, self).__init__('Texts',
                'Texts',
                ('A label is a simple component that allows you to add '
                 '(optionally formatted) text components to your application'),
                [LabelPlain(),
                 LabelPreformatted(),
                 LabelRich()])


class Embedding(FeatureSet):

    def __init__(self):
        super(Embedding, self).__init__('Embedding',
                'Embedding',
                'How to add non-textual content to your applications',
                [ImageEmbed(),
                 FlashEmbed(),
                 WebEmbed()])


class TextFields(FeatureSet):

    def __init__(self):
        super(TextFields, self).__init__('TextFields',
                'Text inputs',
                ('Text inputs are probably the most needed components in '
                 'any application that require user input or editing.'),
                [TextFieldSingle(),
                 TextFieldSecret(),
                 TextFieldInputPrompt(),
                 TextFieldTextChangeEvent(),
                 TextArea(),
                 RichTextEditor()])


class Trees(FeatureSet):

    def __init__(self):
        super(Trees, self).__init__('Trees',
                'Trees',
                ('The Tree component provides a natural way to represent '
                 'data that has hierarchical relationships, such as '
                 'filesystems or message threads.'),
                [TreeSingleSelect(),
                 TreeMultiSelect(),
                 TreeActions(),
                 TreeMouseEvents(),
                 TreeKeyboardNavigation()])


class Dates(FeatureSet):

    def __init__(self):
        super(Dates, self).__init__('Dates',
                'Dates',
                ('The DateField component can be used to produce various '
                 'date and time input fields with different resolutions. '
                 'The date and time format used with this component is '
                 'reported to Muntjac by the browser.'),
                [DatePopup(),
                 DatePopupInputPrompt(),
                 DatePopupKeyboardNavigation(),
                 DateInline(),
                 DateLocale(),
                 DateResolution()])


class DragDrop(FeatureSet):

    def __init__(self):
        super(DragDrop, self).__init__('Dragdrop',
                'Drag\'n\'drop',
                ('Drag\'n\'drop supports dragging data and components to '
                 'other components or items within a component.'),
                [DragDropTreeSorting(),
#                 DragDropTableTree(),
#                 DragDropServerValidation(),
                 DragDropRearrangeComponents(),
#                 DragDropHtml5FromDesktop()
                 ])

# MAIN structure; root is always a FeatureSet that is not shown
FeatureSet.FEATURES = FeatureSet('', [Basics(), ValueInput(), FormsAndData(),
        GridsAndTrees(), DragDrop(), Layouting(), Windowing()])
