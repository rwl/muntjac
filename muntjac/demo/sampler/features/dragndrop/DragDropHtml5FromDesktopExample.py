# -*- coding: utf-8 -*-
# from com.vaadin.service.ApplicationContext import (ApplicationContext,)
# from com.vaadin.terminal.StreamResource import (StreamResource,)
# from com.vaadin.terminal.StreamResource.StreamSource import (StreamSource,)
# from com.vaadin.terminal.StreamVariable import (StreamVariable,)
# from com.vaadin.terminal.gwt.server.AbstractWebApplicationContext import (AbstractWebApplicationContext,)
# from com.vaadin.terminal.gwt.server.WebBrowser import (WebBrowser,)
# from com.vaadin.ui.Label import (Label,)
# from com.vaadin.ui.Component import (Component,)
# from com.vaadin.ui.CssLayout import (CssLayout,)
# from com.vaadin.ui.Embedded import (Embedded,)
# from com.vaadin.ui.Panel import (Panel,)
# from com.vaadin.ui.ProgressIndicator import (ProgressIndicator,)
# from com.vaadin.ui.Window import (Window,)
# from com.vaadin.ui.Window.Notification import (Notification,)
# from java.io.ByteArrayInputStream import (ByteArrayInputStream,)
# from java.io.ByteArrayOutputStream import (ByteArrayOutputStream,)
# from java.io.InputStream import (InputStream,)
# from java.io.OutputStream import (OutputStream,)


class DragDropHtml5FromDesktopExample(VerticalLayout):
    _progress = None

    def __init__(self):
        self.addComponent(Label('Drag text from desktop application or image files from the ' + 'file system to the drop box below (dragging files requires HTML5 capable browser like FF 3.6, Safari or Chrome)'))
        dropPane = CssLayout()
        dropPane.setWidth('200px')
        dropPane.setHeight('200px')
        dropPane.addStyleName('image-drop-pane')
        dropBox = self.ImageDropBox(dropPane)
        dropBox.setSizeUndefined()
        panel = Panel(dropBox)
        panel.setSizeUndefined()
        panel.addStyleName('no-vertical-drag-hints')
        panel.addStyleName('no-horizontal-drag-hints')
        self.addComponent(panel)
        self._progress = ProgressIndicator()
        self._progress.setIndeterminate(True)
        self._progress.setVisible(False)
        self.addComponent(self._progress)

    def attach(self):
        super(DragDropHtml5FromDesktopExample, self).attach()
        # warn the user if the browser does not support file drop
        context = self.getApplication().getContext()
        if isinstance(context, AbstractWebApplicationContext):
            webBrowser = context.getBrowser()
            # FF
            supportsHtml5FileDrop = webBrowser.isFirefox() and (webBrowser.getBrowserMajorVersion() >= 4) or (webBrowser.getBrowserMajorVersion() == 3 and webBrowser.getBrowserMinorVersion() >= 6)
            if not supportsHtml5FileDrop:
                # pretty much all chromes and safaris are new enough
                supportsHtml5FileDrop = webBrowser.isChrome() or (webBrowser.isSafari() and webBrowser.getBrowserMajorVersion() > 4)
            if not supportsHtml5FileDrop:
                self.getWindow().showNotification('Image file drop is only supported on Firefox 3.6 and later. ' + 'Text can be dropped into the box on other browsers.', Notification.TYPE_WARNING_MESSAGE)

    class ImageDropBox(DragAndDropWrapper, DropHandler):
        _FILE_SIZE_LIMIT = 2 * 1024 * 1024
        # 2MB

        def __init__(self, root):
            super(ImageDropBox, self)(root)
            self.setDropHandler(self)

        def drop(self, dropEvent):
            # expecting this to be an html5 drag
            tr = dropEvent.getTransferable()
            files = tr.getFiles()
            if files is not None:
                # for (final Html5File html5File : files) {
                # final String fileName = html5File.getFileName();
                # if (html5File.getFileSize() > FILE_SIZE_LIMIT) {
                # getWindow()
                # .showNotification(
                # "File rejected. Max 2Mb files are accepted by Sampler",
                # Notification.TYPE_WARNING_MESSAGE);
                # } else {
                # final ByteArrayOutputStream bas = new ByteArrayOutputStream();
                # StreamVariable streamVariable = new StreamVariable() {
                # public OutputStream getOutputStream() {
                # return bas;
                # }
                # public boolean listenProgress() {
                # return false;
                # }
                # public void onProgress(StreamingProgressEvent event) {
                # }
                # public void streamingStarted(
                # StreamingStartEvent event) {
                # }
                # public void streamingFinished(
                # StreamingEndEvent event) {
                # progress.setVisible(false);
                # showFile(fileName, html5File.getType(), bas);
                # }
                # public void streamingFailed(
                # StreamingErrorEvent event) {
                # progress.setVisible(false);
                # }
                # public boolean isInterrupted() {
                # return false;
                # }
                # };
                # html5File.setStreamVariable(streamVariable);
                # progress.setVisible(true);
                # }
                # }
                pass
            else:
                text = tr.getText()
                if text is not None:
                    self.showText(text)

        def showText(self, text):
            self.showComponent(Label(text), 'Wrapped text content')

        def showFile(self, name, type, bas):
            # resource for serving the file contents

            class streamSource(StreamSource):

                def getStream(self):
                    if self.bas is not None:
                        byteArray = self.bas.toByteArray()
                        return ByteArrayInputStream(byteArray)
                    return None

            resource = StreamResource(streamSource, name, self.getApplication())
            # show the file contents - images only for now
            embedded = Embedded(name, resource)
            self.showComponent(embedded, name)

        def showComponent(self, c, name):
            layout = VerticalLayout()
            layout.setSizeUndefined()
            layout.setMargin(True)
            w = Window(name, layout)
            w.setSizeUndefined()
            c.setSizeUndefined()
            w.addComponent(c)
            self.getWindow().addWindow(w)

        def getAcceptCriterion(self):
            return AcceptAll.get()
