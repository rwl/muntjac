
import time
import threading

from time import gmtime, strftime

from muntjac.api import Button, VerticalLayout, Label, TextArea
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.ui.button import IClickListener


class JSApiExample(VerticalLayout):

    def __init__(self):
        super(JSApiExample, self).__init__()

        self._toBeUpdatedFromThread = None
        self._startThread = None
        self._running = Label('')

        self.setSpacing(True)

        javascript = Label("<h3>Run Native JavaScript</h3>",
                Label.CONTENT_XHTML)
        self.addComponent(javascript)

        script = TextArea()
        script.setWidth('100%')
        script.setRows(3)
        script.setValue('alert(\"Hello Muntjac\");')
        self.addComponent(script)

        self.addComponent(Button('Run script', RunListener(self, script)))

#        sync = Label("<h3>Force Server Syncronization</h3>",
#                Label.CONTENT_XHTML)
#        self.addComponent(sync)
#
#        self.addComponent(Label('For advanced client side programmers '
#                'Muntjac offers a simple method which can be used to force '
#                'the client to synchronize with the server. This may be '
#                'needed for example if another part of a mashup changes '
#                'things on server.'))
#
#        self._toBeUpdatedFromThread = Label("This Label component will be "
#                "updated by a background thread. Click \"Start "
#                "background thread\" button and start clicking "
#                "on the link below to force "
#                "synchronization.", Label.CONTENT_XHTML)
#        self.addComponent(self._toBeUpdatedFromThread)
#
#        # This label will be show for 10 seconds while the background process
#        # is working
#        self._running.setCaption('Background process is running for 10 '
#                'seconds, click the link below')
#        self._running.setIcon(
#                ThemeResource('../base/common/img/ajax-loader-medium.gif'))
#
#        # Clicking on this button will start a repeating thread that updates
#        # the label value
#        self._startThread = Button('Start background thread',
#                StartListener(self))
#        self.addComponent(self._startThread)
#
#        # This link will make an Ajax request to the server that will respond
#        # with UI changes that have happened since last request
#        self.addComponent(Label("<a href=\"javascript:vaadin.forceSync();\">"
#                "javascript: vaadin.forceSync();</a>", Label.CONTENT_XHTML))


class RunListener(IClickListener):

    def __init__(self, component, script):
        self._component = component
        self._script = script

    def buttonClick(self, event):
        self._component.getWindow().executeJavaScript(
                str(self._script.getValue()))


class StartListener(IClickListener):

    def __init__(self, component):
        self._component = component

    def buttonClick(self, event):
        self._component._startThread.getParent().replaceComponent(
                self._component._startThread,
                self._component._running)
        BackgroundProcess(self._component).start()


class BackgroundProcess(threading.Thread):

    def __init__(self, component):
        super(BackgroundProcess, self).__init__()
        self._component = component

    def run(self):
        try:
            i = 0
            while i < 10:
                time.sleep(1000)
                self._component._toBeUpdatedFromThread.setValue(
                        '<strong>Server time is '
                        + strftime("%H:%M:%S", gmtime())
                        + '</strong>')
                i += 1

            self._component._toBeUpdatedFromThread.setValue(
                    'Background process finished')

            self._component._running.getParent().replaceComponent(
                    self._component._running, self._component._startThread)
        except self.InterruptedException, e:
            # TODO Auto-generated catch block
            e.printStackTrace()
