# -*- coding: utf-8 -*-
# from com.vaadin.ui.ProgressIndicator import (ProgressIndicator,)


class ProgressIndicatorsExample(VerticalLayout):
    _pi1 = None
    _pi2 = None
    _worker1 = None
    _worker2 = None
    _startButton1 = None
    _startButton2 = None

    def __init__(self):
        self.setSpacing(True)
        self.addComponent(ALabel('<strong>Normal mode</strong> Runs for 20 seconds', ALabel.CONTENT_XHTML))
        hl = HorizontalLayout()
        hl.setSpacing(True)
        self.addComponent(hl)
        # Add a normal progress indicator
        self._pi1 = ProgressIndicator()
        self._pi1.setIndeterminate(False)
        self._pi1.setEnabled(False)
        hl.addComponent(self._pi1)
        hl.setComponentAlignment(self._pi1, Alignment.MIDDLE_LEFT)

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                ProgressIndicatorsExample_this._worker1 = ProgressIndicatorsExample_this.Worker1()
                ProgressIndicatorsExample_this._worker1.start()
                ProgressIndicatorsExample_this._pi1.setEnabled(True)
                ProgressIndicatorsExample_this._pi1.setValue(0.0)
                ProgressIndicatorsExample_this._startButton1.setEnabled(False)

        _0_ = _0_()
        Button('Start normal', _0_)
        self._startButton1 = _0_
        self._startButton1.setStyleName('small')
        hl.addComponent(self._startButton1)
        self.addComponent(ALabel('<strong>Indeterminate mode</strong> Runs for 10 seconds', ALabel.CONTENT_XHTML))
        hl = HorizontalLayout()
        hl.setSpacing(True)
        self.addComponent(hl)
        # Add an indeterminate progress indicator
        self._pi2 = ProgressIndicator()
        self._pi2.setIndeterminate(True)
        self._pi2.setPollingInterval(5000)
        self._pi2.setEnabled(False)
        hl.addComponent(self._pi2)

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                ProgressIndicatorsExample_this._worker2 = ProgressIndicatorsExample_this.Worker2()
                ProgressIndicatorsExample_this._worker2.start()
                ProgressIndicatorsExample_this._pi2.setEnabled(True)
                ProgressIndicatorsExample_this._pi2.setVisible(True)
                ProgressIndicatorsExample_this._startButton2.setEnabled(False)

        _0_ = _0_()
        Button('Start indeterminate', _0_)
        self._startButton2 = _0_
        self._startButton2.setStyleName('small')
        hl.addComponent(self._startButton2)

    def prosessed(self):
        i = self._worker1.getCurrent()
        if i == self.Worker1.MAX:
            self._pi1.setEnabled(False)
            self._startButton1.setEnabled(True)
            self._pi1.setValue(1.0)
        else:
            self._pi1.setValue(i / self.Worker1.MAX)

    def prosessed2(self):
        self._pi2.setEnabled(False)
        self._startButton2.setEnabled(True)

    def Worker1(ProgressIndicatorsExample_this, *args, **kwargs):

        class Worker1(VerticalLayout.Thread):
            _current = 1
            MAX = 20

            def run(self):
                _0 = True
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        self._current += 1
                    if not (self._current <= self.MAX):
                        break
                    # All modifications to Vaadin components should be synchronized
                    # over application instance. For normal requests this is done
                    # by the servlet. Here we are changing the application state
                    # via a separate thread.
                    try:
                        self.Thread.sleep(1000)
                    except self.InterruptedException, e:
                        e.printStackTrace()
                    ProgressIndicatorsExample_this.prosessed()

            def getCurrent(self):
                return self._current

        return Worker1(*args, **kwargs)

    def Worker2(ProgressIndicatorsExample_this, *args, **kwargs):

        class Worker2(VerticalLayout.Thread):

            def run(self):
                # synchronize changes over application
                try:
                    self.Thread.sleep(10000)
                except self.InterruptedException, e:
                    e.printStackTrace()
                ProgressIndicatorsExample_this.prosessed2()

        return Worker2(*args, **kwargs)
