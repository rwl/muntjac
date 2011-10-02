# -*- coding: utf-8 -*-
from __pyjamas__ import (POSTINC,)
# from com.vaadin.terminal.ThemeResource import (ThemeResource,)
# from com.vaadin.ui.ALabel import (ALabel,)
# from com.vaadin.ui.Button import (Button,)
# from com.vaadin.ui.Button.ClickEvent import (ClickEvent,)
# from com.vaadin.ui.Layout import (Layout,)
# from com.vaadin.ui.TextArea import (TextArea,)
# from com.vaadin.ui.VerticalLayout import (VerticalLayout,)
# from java.text.SimpleDateFormat import (SimpleDateFormat,)
# from java.util.Date import (Date,)


class JSApiExample(VerticalLayout):
    _toBeUpdatedFromThread = None
    _startThread = None
    _running = ALabel('')

    def __init__(self):
        self.setSpacing(True)
        # Label javascript = new Label("<h3>Run Native JavaScript</h3>",
        # Label.CONTENT_XHTML);
        self.addComponent(self.javascript)
        script = TextArea()
        script.setWidth('100%')
        script.setRows(3)
        script.setValue('alert(\"Hello Vaadin\");')
        self.addComponent(script)
        self.addComponent(


        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                self.getWindow().executeJavaScript(str(self.script.getValue()))


        _0_ = _0_()
        Button('Run script', _0_))
        # Label sync = new Label("<h3>Force Server Syncronization</h3>",
        # Label.CONTENT_XHTML);
        self.addComponent(self.sync)
        self.addComponent(ALabel('For advanced client side programmers Vaadin offers a simple ' + 'method which can be used to force the client to synchronize with the ' + 'server. This may be needed for example if another part of a mashup ' + 'changes things on server.'))
        # toBeUpdatedFromThread = new Label(
        # "This Label component will be updated by a background thread. Click \"Start "
        # + "background thread\" button and start clicking on the link below to force "
        # + "synchronization.", Label.CONTENT_XHTML);
        self.addComponent(self._toBeUpdatedFromThread)
        # This label will be show for 10 seconds while the background process
        # is working
        self._running.setCaption('Background process is running for 10 seconds, click the link below')
        self._running.setIcon(ThemeResource('../base/common/img/ajax-loader-medium.gif'))
        # Clicking on this button will start a repeating thread that updates
        # the label value

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                JSApiExample_this._startThread.getParent().replaceComponent(JSApiExample_this._startThread, JSApiExample_this._running)
                JSApiExample_this.BackgroundProcess().start()

        _0_ = _0_()
        Button('Start background thread', _0_)
        self._startThread = _0_
        self.addComponent(self._startThread)
        # This link will make an Ajax request to the server that will respond
        # with UI changes that have happened since last request
        # addComponent(new Label(
        # "<a href=\"javascript:vaadin.forceSync();\">javascript: vaadin.forceSync();</a>",
        # Label.CONTENT_XHTML));

    def BackgroundProcess(JSApiExample_this, *args, **kwargs):

        class BackgroundProcess(VerticalLayout.Thread):
            _f = SimpleDateFormat('HH:mm:ss')

            def run(self):
                # TODO Auto-generated catch block
                try:
                    i = 0
                    while POSTINC(globals(), locals(), 'i') < 10:
                        self.Thread.sleep(1000)
                        JSApiExample_this._toBeUpdatedFromThread.setValue('<strong>Server time is ' + self._f.format(Date()) + '</strong>')
                    JSApiExample_this._toBeUpdatedFromThread.setValue('Background process finished')
                    JSApiExample_this._running.getParent().replaceComponent(JSApiExample_this._running, JSApiExample_this._startThread)
                except self.InterruptedException, e:
                    e.printStackTrace()

        return BackgroundProcess(*args, **kwargs)
