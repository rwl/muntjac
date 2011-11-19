
from muntjac.demo.sampler.CodeLabel import CodeLabel
from muntjac.demo.sampler.FeatureSet import FeatureSet
from muntjac.demo.sampler.ActiveLink import ActiveLink

from muntjac.terminal.theme_resource import ThemeResource
from muntjac.terminal.external_resource import ExternalResource

from muntjac.ui.themes import Reindeer, BaseTheme
from muntjac.ui.button import IClickListener
from muntjac.demo.sampler.ActiveLink import ILinkActivatedListener

from muntjac.api import \
    (HorizontalLayout, Label, VerticalLayout, Panel, NativeButton,
     Link, Window)


class FeatureView(HorizontalLayout):

    _MSG_SHOW_SRC = 'View Source'

    def __init__(self):
        super(FeatureView, self).__init__()

        self._right = None
        self._left = None
        self._controls = None
        self._title = Label("", Label.CONTENT_XHTML)
        self._showSrc = None
        self._exampleCache = dict()
        self._currentFeature = None
        self._srcWindow = None

        self.setWidth('100%')
        self.setMargin(True)
        self.setSpacing(True)
        self.setStyleName('sample-view')

        self._left = VerticalLayout()
        self._left.setWidth('100%')
        self._left.setSpacing(True)
        self._left.setMargin(False)
        self.addComponent(self._left)
        self.setExpandRatio(self._left, 1)

        rightLayout = VerticalLayout()
        self._right = Panel(rightLayout)
        rightLayout.setMargin(True, False, False, False)
        self._right.setStyleName(Reindeer.PANEL_LIGHT)
        self._right.addStyleName('feature-info')
        self._right.setWidth('319px')
        self.addComponent(self._right)

        self._controls = HorizontalLayout()
        self._controls.setWidth('100%')
        self._controls.setStyleName('feature-controls')

        self._title.setStyleName('title')
        self._controls.addComponent(self._title)
        self._controls.setExpandRatio(self._title, 1)

        resetExample = NativeButton('Reset', ResetListener(self))
        resetExample.setStyleName(BaseTheme.BUTTON_LINK)
        resetExample.addStyleName('reset')
        resetExample.setDescription('Reset Sample')
        self._controls.addComponent(resetExample)
        self._showSrc = ActiveLink()
        self._showSrc.setDescription('Right / middle / ctrl / shift -click for browser window/tab')

        self._showSrc.addListener(ShowSrcListener(self), ILinkActivatedListener)
        self._showSrc.setCaption(self._MSG_SHOW_SRC)
        self._showSrc.addStyleName('showcode')
        self._showSrc.setTargetBorder(Link.TARGET_BORDER_NONE)
        self._controls.addComponent(self._showSrc)


    def showSource(self, source):
        if self._srcWindow is None:
            self._srcWindow = Window('Python source')
            self._srcWindow.getContent().setSizeUndefined()
            self._srcWindow.setWidth('70%')
            self._srcWindow.setHeight('60%')
            self._srcWindow.setPositionX(100)
            self._srcWindow.setPositionY(100)

        self._srcWindow.removeAllComponents()
        self._srcWindow.addComponent( CodeLabel(source) )

        if self._srcWindow.getParent() is None:
            self.getWindow().addWindow(self._srcWindow)


    def resetExample(self):
        if self._currentFeature is not None:
            w = self.getWindow()
            w.removeSubwindows()
            f = self._currentFeature
            self._currentFeature = None
            if f in self._exampleCache:
                del self._exampleCache[f]
            self.setFeature(f)


    def setFeature(self, feature):

        from muntjac.demo.sampler.SamplerApplication import SamplerApplication

        if feature != self._currentFeature:
            self._currentFeature = feature
            self._right.removeAllComponents()
            self._left.removeAllComponents()

            self._left.addComponent(self._controls)
            self._title.setValue('<span>' + feature.getName() + '</span>')
#            if feature.getSinceVersion().isNew():
#                self._title.addStyleName('new')
#            else:
#                self._title.removeStyleName('new')

            self._left.addComponent(self.getExampleFor(feature))

            self._right.setCaption('Description and Resources')

            # Do not show parent description if it's directly inside the root
            alll = SamplerApplication.getAllFeatures()
            parent = alll.getParent(feature)
            isRoot = alll.getParent(parent) is None
            desc = parent.getDescription()
            hasParentDesc = False

            if parent is not None and not isRoot:
                parentLabel = Label(parent.getDescription())
                if desc is not None and desc != '':
                    parentLabel.setContentMode(Label.CONTENT_XHTML)
                    self._right.addComponent(parentLabel)
                    hasParentDesc = True
            desc = feature.getDescription()
            if desc is not None and desc != '':
                # Sample description uses additional decorations if a parent
                # description is found
                l = Label(("<div class=\"outer-deco\"><div class=\"deco\">"
                        "<span class=\"deco\"></span>")
                        + desc + "</div></div>", Label.CONTENT_XHTML)
                self._right.addComponent(l)
                if hasParentDesc:
                    l.setStyleName('sample-description')
                else:
                    l.setStyleName('description')

            # open src in new window -link
            self._showSrc.setTargetName(self._currentFeature.getFragmentName())
            er = ExternalResource(self.getApplication().getURL()
                    + 'src/' + self._currentFeature.getFragmentName())
            self._showSrc.setResource(er)

            resources = feature.getRelatedResources()
            if resources is not None:
                res = VerticalLayout()
                self.caption = Label("<span>Additional Resources</span>",
                        Label.CONTENT_XHTML)
                self.caption.setStyleName('section')
                self.caption.setWidth('100%')
                res.addComponent(self.caption)
                res.setMargin(False, False, True, False)
                for r in resources:
                    l = Link(r.getName(), r)
                    l.setIcon( ThemeResource('../runo/icons/16/note.png') )
                    res.addComponent(l)
                self._right.addComponent(res)

            apis = feature.getRelatedAPI()
            if apis is not None:
                api = VerticalLayout()
                self.caption = Label("<span>API Documentation</span>",
                        Label.CONTENT_XHTML)
                self.caption.setStyleName('section')
                self.caption.setWidth('100%')
                api.addComponent(self.caption)
                api.setMargin(False, False, True, False)
                for r in apis:
                    l = Link(r.getName(), r)
                    ic = ThemeResource('../runo/icons/16/document-txt.png')
                    l.setIcon(ic)
                    api.addComponent(l)
                self._right.addComponent(api)

            features = feature.getRelatedFeatures()
            if features is not None:
                rel = VerticalLayout()
                self.caption = Label("<span>Related Samples</span>",
                        Label.CONTENT_XHTML)
                self.caption.setStyleName('section')
                self.caption.setWidth('100%')
                rel.addComponent(self.caption)
                rel.setMargin(False, False, True, False)
                for c in features:
                    f = SamplerApplication.getFeatureFor(c)
                    if f is not None:
                        er = ExternalResource(self.getApplication().getURL()
                                + '#' + f.getFragmentName())
                        al = ActiveLink(f.getName(), er)
                        if isinstance(f, FeatureSet):
                            ic = ThemeResource('../sampler/icons/category.gif')
                        else:
                            ic = ThemeResource('../sampler/icons/sample.png')
                        al.setIcon(ic)

                        al.addListener(LinkListener(self, f),
                                ILinkActivatedListener)
                        rel.addComponent(al)
                self._right.addComponent(rel)


    def getExampleFor(self, f):
        ex = self._exampleCache.get(f)
        if ex is None:
            ex = f.getExample()
            self._exampleCache[f] = ex
        return ex


class ResetListener(IClickListener):

    def __init__(self, view):
        self._view = view

    def buttonClick(self, event):
        self._view.resetExample()


class ShowSrcListener(ILinkActivatedListener):

    def __init__(self, view):
        self._view = view

    def linkActivated(self, event):
        if not event.isLinkOpened():
            self._view.showSource(
                    self._view._currentFeature.getSource())


class LinkListener(ILinkActivatedListener):

    def __init__(self, view, feature):
        self._view = view
        self._feature = feature

    def linkActivated(self, event):
        if event.isLinkOpened():
            self._view.getWindow().showNotification(
                    (self._feature.getName()
                     + ' opened if new window/tab'))
        else:
            w = self._view.getWindow()
            w.setFeature(self._feature)