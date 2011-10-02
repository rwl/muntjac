# -*- coding: utf-8 -*-
import com.vaadin.Application


class HelloWorld(com.vaadin.Application.Application):

    def init(self):
        """Init is invoked on application load (when a user accesses the application
        for the first time).
        """
        # Main window is the primary browser window
        main = Window('Hello window')
        self.setMainWindow(main)
        # "Hello world" text is added to window as a Label component
        main.addComponent(Label('Hello World!'))
