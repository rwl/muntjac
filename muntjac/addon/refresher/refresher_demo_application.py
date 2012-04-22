# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

import time

from threading import Thread

from muntjac.application import Application
from muntjac.ui.window import Window
from muntjac.ui.panel import Panel
from muntjac.ui.horizontal_layout import HorizontalLayout
from muntjac.addon.refresher.refresher import Refresher
from muntjac.ui.label import Label
from muntjac.ui import button
from muntjac.ui.button import Button

SLEEP_TIME_IN_MILLIS = 1000  # a second

class RefresherApplication(Application):

    def init(self):
        mainWindow = Window('Refresher')
        self.setMainWindow(mainWindow)
        panel = Panel('Refresher example')
        layout = HorizontalLayout()
        refresher = Refresher()
        label = Label('0')
        thread = CounterThread(label)
        thread.start()
        label.setData(0)
        panel.addComponent(refresher)
        panel.addComponent(Label("<div style='margin-bottom:10px'>"
                + "The Refresher allows you to affect the UI "
                + "from external threads without "
                + "<a href='http://vaadin.com/forum/-/message_boards/message/69792' target='_blank'>"
                + "the ProgressIndicator hack</a>.</div>", Label.CONTENT_XHTML))
        panel.addComponent(layout)
        layout.setSpacing(True)
        layout.addComponent(Button('Start Counting',
                    StartClickListener(refresher, thread)))
        layout.addComponent(Button('Stop Counting',
                    StopClickListener(refresher, thread)))
        layout.addComponent(label)
        mainWindow.setContent(panel)


class StartClickListener(button.IClickListener):

    def __init__(self, refresher, thread):
        self.refresher = refresher
        self.thread = thread

    def buttonClick(self, event):
        self.refresher.setRefreshInterval(SLEEP_TIME_IN_MILLIS)
        self.thread.startCounting()


class StopClickListener(button.IClickListener):

    def __init__(self, refresher, thread):
        self.refresher = refresher
        self.thread = thread

    def buttonClick(self, event):
        self.refresher.setRefreshInterval(0)
        self.thread.stopCounting()


class CounterThread(Thread):

    def __init__(self, renderLabel):
        super(CounterThread, self).__init__()
        self._renderLabel = renderLabel
        renderLabel.setData(1)
        self._running = False

    def run(self):
        startTime = 1000 * time.time()
        lifetime = 1000 * 60
        # live for a minute.
        try:
            while 1000 * time.time() < startTime + lifetime:
                if self._running:
                    # synchronize with the application, to avoid concurrent
                    # edits on the label's value.
                    number = self._renderLabel.getData()
                    self._renderLabel.setValue(number)
                    self._renderLabel.setData(number + 1)
                time.sleep(SLEEP_TIME_IN_MILLIS)
            self._renderLabel.setValue('[ counter thread expired ]')
        except KeyboardInterrupt:
            self._renderLabel.setValue('[ counter thread interrupted ]')

    def startCounting(self):
        self._running = True

    def stopCounting(self):
        self._running = False


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(RefresherApplication, nogui=True, debug=True,
            contextRoot='.')
