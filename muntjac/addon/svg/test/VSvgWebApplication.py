# -*- coding: utf-8 -*-
from org.vaadin.svg.test.FileExample import (FileExample,)
# from com.vaadin.Application import (Application,)
# from com.vaadin.terminal.ClassResource import (ClassResource,)
# from com.vaadin.ui.Button import (Button,)
# from com.vaadin.ui.Button.ClickEvent import (ClickEvent,)
# from com.vaadin.ui.Button.ClickListener import (ClickListener,)
# from com.vaadin.ui.CssLayout import (CssLayout,)
# from com.vaadin.ui.HorizontalLayout import (HorizontalLayout,)
# from com.vaadin.ui.Window import (Window,)


class VSvgWebApplication(Application):

    def init(self):
        mainWindow = Window('Vsvgweb Application')
        self.setMainWindow(mainWindow)
        example = CssLayout()
        example.setWidth('100%')
        example.addComponent(FileExample(self))
        hl = HorizontalLayout()
        # Button b = new Button("Java 2d demo", new ClickListener() {
        # public void buttonClick(ClickEvent event) {
        # example.removeAllComponents();
        # example.addComponent(new Java2DExample());
        # }
        # });
        # hl.addComponent(b);
        # b = new Button("Jung library demo", new ClickListener() {
        # public void buttonClick(ClickEvent event) {
        # example.removeAllComponents();
        # example.addComponent(new JungExample());
        # }
        # });
        # hl.addComponent(b);
        # b = new Button("Basic file example", new ClickListener() {
        # public void buttonClick(ClickEvent event) {
        # example.removeAllComponents();
        # example.addComponent(new FileExample(VsvgwebApplication.this));
        # }
        # });
        # hl.addComponent(b);
        # b = new Button("Animation example", new ClickListener() {
        # public void buttonClick(ClickEvent event) {
        # example.removeAllComponents();
        # example.addComponent(new AnimationExample(VsvgwebApplication.this));
        # }
        # });
        # hl.addComponent(b);
        mainWindow.addComponent(hl)
        mainWindow.addComponent(example)
