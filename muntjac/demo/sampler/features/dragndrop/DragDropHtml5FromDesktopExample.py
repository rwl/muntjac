
try:
    from cStringIO import StringIO
except ImportError, e:
    from StringIO import StringIO

from muntjac.api import \
    VerticalLayout, Label, CssLayout, Panel, ProgressIndicator, Window

from muntjac.terminal.gwt.server.abstract_web_application_context import \
    AbstractWebApplicationContext

from muntjac.ui.window import Notification
from muntjac.ui.drag_and_drop_wrapper import DragAndDropWrapper
from muntjac.event.dd.drop_handler import IDropHandler
from muntjac.terminal.stream_resource import IStreamSource, StreamResource
from muntjac.event.dd.acceptcriteria.accept_all import AcceptAll
from muntjac.ui.embedded import Embedded
from muntjac.terminal.stream_variable import IStreamVariable


class DragDropHtml5FromDesktopExample(VerticalLayout):

    def __init__(self):
        super(DragDropHtml5FromDesktopExample, self).__init__()

        self.addComponent(Label('Drag text from desktop application or '
                'image files from the ' + 'file system to the drop box '
                'below (dragging files requires HTML5 capable browser '
                'like FF 3.6, Safari or Chrome)'))

        dropPane = CssLayout()
        dropPane.setWidth('200px')
        dropPane.setHeight('200px')
        dropPane.addStyleName('image-drop-pane')

        dropBox = ImageDropBox(dropPane, self)
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
            supportsHtml5FileDrop = (webBrowser.isFirefox()
                    and (webBrowser.getBrowserMajorVersion() >= 4)
                    or (webBrowser.getBrowserMajorVersion() == 3
                        and webBrowser.getBrowserMinorVersion() >= 6))

            if not supportsHtml5FileDrop:
                # pretty much all chromes and safaris are new enough
                supportsHtml5FileDrop = (webBrowser.isChrome()
                        or (webBrowser.isSafari()
                            and webBrowser.getBrowserMajorVersion() > 4))

            if not supportsHtml5FileDrop:
                self.getWindow().showNotification('Image file drop is '
                        'only supported on Firefox 3.6 and later. '
                        'Text can be dropped into the box on other browsers.',
                        Notification.TYPE_WARNING_MESSAGE)


class ImageDropBox(DragAndDropWrapper, IDropHandler):

    _FILE_SIZE_LIMIT = 2 * 1024 * 1024  # 2MB

    def __init__(self, root, component):
        super(ImageDropBox, self).__init__(root)
        self.setDropHandler(self)

        self._component = component


    def drop(self, dropEvent):
        # expecting this to be an html5 drag
        tr = dropEvent.getTransferable()
        files = tr.getFiles()
        if files is not None:
            for html5File in files:
                fileName = html5File.getFileName()
                if (html5File.getFileSize() > self._FILE_SIZE_LIMIT):
                    self._component.getWindow().showNotification("File " \
                            "rejected. Max 2Mb files are accepted by Sampler",
                            Notification.TYPE_WARNING_MESSAGE)
                else:
                    bas = StringIO()

                    sv = FileStreamVariable(self, fileName, html5File, bas)
                    html5File.setStreamVariable(sv)

                    self._component._progress.setVisible(True)
        else:
            text = tr.getText()
            if text is not None:
                self.showText(text)


    def showText(self, text):
        self.showComponent(Label(text), 'Wrapped text content')


    def showFile(self, name, typ, bas):

        # resource for serving the file contents
        streamSource = FileStreamSource(bas)
        resource = StreamResource(streamSource, name,
                self._component.getApplication())

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
        self._component.getWindow().addWindow(w)


    def getAcceptCriterion(self):
        return AcceptAll.get()


class FileStreamSource(IStreamSource):

    def __init__(self, bas):
        self._bas = bas


    def getStream(self):
        if self._bas is not None:
            byteArray = self._bas.getvalue()
            return StringIO(byteArray)
        return None


class FileStreamVariable(IStreamVariable):

    def __init__(self, component, fileName, html5file, bas):
        self._component = component
        self._html5file = html5file
        self._fileName = fileName
        self._bas = bas


    def __getstate__(self):
        result = self.__dict__.copy()
        del result['_bas']
        result['_bas_str'] = self._bas.getvalue()
        return result


    def __setstate__(self, d):
        self.__dict__ = d
        bas_str = d.get('_bas_str', '')
        self._bas = StringIO(bas_str)


    def getOutputStream(self):
        return self._bas


    def listenProgress(self):
        return False


    def onProgress(self, event):
        pass


    def streamingStarted(self, event):
        pass


    def streamingFinished(self, event):
        self._component._progress.setVisible(False)
        self.showFile(self._fileName,
                self._html5File.getType(), self._bas)


    def streamingFailed(self, event):
        self._component._progress.setVisible(False)


    def isInterrupted(self):
        return False
