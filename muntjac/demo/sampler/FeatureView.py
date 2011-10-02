# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.SamplerApplication import (SamplerApplication,)
from com.vaadin.demo.sampler.CodeLabel import (CodeLabel,)
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.ActiveLink import (ActiveLink,)
# from com.vaadin.data.util.HierarchicalContainer import (HierarchicalContainer,)
# from com.vaadin.terminal.ThemeResource import (ThemeResource,)
# from com.vaadin.ui.Button import (Button,)
# from com.vaadin.ui.HorizontalLayout import (HorizontalLayout,)
# from com.vaadin.ui.NativeButton import (NativeButton,)
# from com.vaadin.ui.Panel import (Panel,)
# from com.vaadin.ui.VerticalLayout import (VerticalLayout,)
# from com.vaadin.ui.Window import (Window,)
# from com.vaadin.ui.themes.BaseTheme import (BaseTheme,)
# from com.vaadin.ui.themes.Reindeer import (Reindeer,)
# from java.util.HashMap import (HashMap,)
LinkActivatedListener = ActiveLink.LinkActivatedListener


class FeatureView(HorizontalLayout):
    _MSG_SHOW_SRC = 'View Source'
    _right = None
    _left = None
    _controls = None
    # private Label title = new Label("", Label.CONTENT_XHTML);
    _showSrc = None
    _exampleCache = dict()
    _currentFeature = None
    _srcWindow = None

    def __init__(self):
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
        self.title.setStyleName('title')
        self._controls.addComponent(self.title)
        self._controls.setExpandRatio(self.title, 1)

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                FeatureView_this.resetExample()

        _0_ = _0_()
        resetExample = NativeButton('Reset', _0_)
        resetExample.setStyleName(BaseTheme.BUTTON_LINK)
        resetExample.addStyleName('reset')
        resetExample.setDescription('Reset Sample')
        self._controls.addComponent(resetExample)
        self._showSrc = ActiveLink()
        self._showSrc.setDescription('Right / middle / ctrl / shift -click for browser window/tab')

        class _0_(LinkActivatedListener):

            def linkActivated(self, event):
                if not event.isLinkOpened():
                    FeatureView_this.showSource(FeatureView_this._currentFeature.getSource())

        _0_ = _0_()
        self._showSrc.addListener(_0_)
        self._showSrc.setCaption(self._MSG_SHOW_SRC)
        self._showSrc.addStyleName('showcode')
        self._showSrc.setTargetBorder(Link.TARGET_BORDER_NONE)
        self._controls.addComponent(self._showSrc)

    def showSource(self, source):
        if self._srcWindow is None:
            self._srcWindow = Window('Java™ source')
            self._srcWindow.getContent().setSizeUndefined()
            self._srcWindow.setWidth('70%')
            self._srcWindow.setHeight('60%')
            self._srcWindow.setPositionX(100)
            self._srcWindow.setPositionY(100)
        self._srcWindow.removeAllComponents()
        self._srcWindow.addComponent(CodeLabel(source))
        if self._srcWindow.getParent() is None:
            self.getWindow().addWindow(self._srcWindow)

    def resetExample(self):
        if self._currentFeature is not None:
            w = self.getWindow()
            w.removeSubwindows()
            f = self._currentFeature
            self._currentFeature = None
            self._exampleCache.remove(f)
            self.setFeature(f)

    def setFeature(self, feature):
        if feature != self._currentFeature:
            # open src in new window -link
            self._currentFeature = feature
            self._right.removeAllComponents()
            self._left.removeAllComponents()
            self._left.addComponent(self._controls)
            self.title.setValue('<span>' + feature.getName() + '</span>')
            if feature.getSinceVersion().isNew():
                self.title.addStyleName('new')
            else:
                self.title.removeStyleName('new')
            self._left.addComponent(self.getExampleFor(feature))
            self._right.setCaption('Description and Resources')
            # Do not show parent description if it's directly inside the root
            all = SamplerApplication.getAllFeatures()
            parent = all.getParent(feature)
            isRoot = all.getParent(parent) is None
            desc = parent.getDescription()
            hasParentDesc = False
            if parent is not None and not isRoot:
                parentLabel = Label(parent.getDescription())
                if desc is not None and desc != '':
                    # parentLabel.setContentMode(Label.CONTENT_XHTML);
                    self._right.addComponent(parentLabel)
                    hasParentDesc = True
            desc = feature.getDescription()
            if desc is not None and desc != '':
                # Sample description uses additional decorations if a parent
                # description is found
                # final Label l = new Label(
                # "<div class=\"outer-deco\"><div class=\"deco\"><span class=\"deco\"></span>"
                # + desc + "</div></div>", Label.CONTENT_XHTML);
                self._right.addComponent(self.l)
                if hasParentDesc:
                    self.l.setStyleName('sample-description')
                else:
                    self.l.setStyleName('description')
            self._showSrc.setTargetName(self._currentFeature.getFragmentName())
            self._showSrc.setResource(ExternalResource(self.getApplication().getURL() + 'src/' + self._currentFeature.getFragmentName()))
            resources = feature.getRelatedResources()
            if resources is not None:
                res = VerticalLayout()
                # Label caption = new Label("<span>Additional Resources</span>",
                # Label.CONTENT_XHTML);
                self.caption.setStyleName('section')
                self.caption.setWidth('100%')
                res.addComponent(self.caption)
                res.setMargin(False, False, True, False)
                for r in resources:
                    l = Link(r.getName(), r)
                    l.setIcon(ThemeResource('../runo/icons/16/note.png'))
                    res.addComponent(l)
                self._right.addComponent(res)
            apis = feature.getRelatedAPI()
            if apis is not None:
                api = VerticalLayout()
                # Label caption = new Label("<span>API Documentation</span>",
                # Label.CONTENT_XHTML);
                self.caption.setStyleName('section')
                self.caption.setWidth('100%')
                api.addComponent(self.caption)
                api.setMargin(False, False, True, False)
                for r in apis:
                    l = Link(r.getName(), r)
                    l.setIcon(ThemeResource('../runo/icons/16/document-txt.png'))
                    api.addComponent(l)
                self._right.addComponent(api)
            features = feature.getRelatedFeatures()
            if features is not None:
                rel = VerticalLayout()
                # Label caption = new Label("<span>Related Samples</span>",
                # Label.CONTENT_XHTML);
                self.caption.setStyleName('section')
                self.caption.setWidth('100%')
                rel.addComponent(self.caption)
                rel.setMargin(False, False, True, False)
                for c in features:
                    f = SamplerApplication.getFeatureFor(c)
                    if f is not None:
                        al = ActiveLink(f.getName(), ExternalResource(self.getApplication().getURL() + '#' + f.getFragmentName()))
                        al.setIcon(ThemeResource('../sampler/icons/category.gif' if isinstance(f, FeatureSet) else '../sampler/icons/sample.png'))

                        class _1_(LinkActivatedListener):

                            def linkActivated(self, event):
                                if event.isLinkOpened():
                                    self.getWindow().showNotification(self.f.getName() + ' opened if new window/tab')
                                else:
                                    w = self.getWindow()
                                    w.setFeature(self.f)

                        _1_ = _1_()
                        al.addListener(_1_)
                        rel.addComponent(al)
                self._right.addComponent(rel)

    def getExampleFor(self, f):
        ex = self._exampleCache[f]
        if ex is None:
            ex = f.getExample()
            self._exampleCache.put(f, ex)
        return ex
