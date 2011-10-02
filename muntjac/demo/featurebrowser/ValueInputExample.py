# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
# from com.vaadin.ui.DateField import (DateField,)
# from com.vaadin.ui.InlineDateField import (InlineDateField,)
# from com.vaadin.ui.Slider import (Slider,)


class ValueInputExample(CustomComponent):
    """Shows some basic fields for value input; TextField, DateField, Slider...
     *
    @author IT Mill Ltd.
    """

    def __init__(self):
        main = VerticalLayout()
        main.setMargin(True)
        self.setCompositionRoot(main)
        # listener that shows a value change notification

        class listener(Field.ValueChangeListener):

            def valueChange(self, event):
                self.getWindow().showNotification('Received', '<pre>' + event.getProperty().getValue() + '</pre>', Notification.TYPE_WARNING_MESSAGE)

        # TextField
        horiz = HorizontalLayout()
        horiz.setWidth('100%')
        main.addComponent(horiz)
        left = Panel('TextField')
        left.setStyleName(Reindeer.PANEL_LIGHT)
        horiz.addComponent(left)
        right = Panel('multiline')
        right.setStyleName(Reindeer.PANEL_LIGHT)
        horiz.addComponent(right)
        # basic TextField
        tf = TextField('Basic')
        tf.setColumns(15)
        tf.setImmediate(True)
        tf.addListener(listener)
        left.addComponent(tf)
        # multiline TextField a.k.a TextArea
        ta = TextArea('Area')
        ta.setColumns(15)
        ta.setRows(5)
        ta.setImmediate(True)
        ta.addListener(listener)
        right.addComponent(ta)
        # DateFields
        horiz = HorizontalLayout()
        horiz.setWidth('100%')
        main.addComponent(horiz)
        left = Panel('DateField')
        left.setStyleName(Reindeer.PANEL_LIGHT)
        horiz.addComponent(left)
        right = Panel('inline')
        right.setStyleName(Reindeer.PANEL_LIGHT)
        horiz.addComponent(right)
        # default
        df = DateField('Day resolution')
        df.addListener(listener)
        df.setImmediate(True)
        df.setResolution(DateField.RESOLUTION_DAY)
        left.addComponent(df)
        # minute
        df = DateField('Minute resolution')
        df.addListener(listener)
        df.setImmediate(True)
        df.setResolution(DateField.RESOLUTION_MIN)
        left.addComponent(df)
        # year
        df = DateField('Year resolution')
        df.addListener(listener)
        df.setImmediate(True)
        df.setResolution(DateField.RESOLUTION_YEAR)
        left.addComponent(df)
        # msec
        df = DateField('Millisecond resolution')
        df.addListener(listener)
        df.setImmediate(True)
        df.setResolution(DateField.RESOLUTION_MSEC)
        left.addComponent(df)
        # Inline
        df = InlineDateField()
        df.addListener(listener)
        df.setImmediate(True)
        right.addComponent(df)
        # Slider
        left = Panel('Slider')
        left.setStyleName(Reindeer.PANEL_LIGHT)
        main.addComponent(left)
        # int slider
        slider = Slider(0, 100)
        slider.setWidth('300px')
        # slider.setSize(300);
        slider.setImmediate(True)

        class _1_(Slider.ValueChangeListener):

            def valueChange(self, event):
                # update caption when value changes
                s = event.getProperty()
                s.setCaption('Value: ' + s.getValue())

        _1_ = _1_()
        slider.addListener(_1_)
        try:
            slider.setValue(20)
        except Exception, e:
            e.printStackTrace(System.err)
        left.addComponent(slider)
        # double slider
        slider = Slider(0.0, 1.0, 1)
        slider.setOrientation(Slider.ORIENTATION_VERTICAL)
        slider.setImmediate(True)

        class _2_(Slider.ValueChangeListener):

            def valueChange(self, event):
                # update caption when value changes
                s = event.getProperty()
                s.setCaption('Value: ' + s.getValue())

        _2_ = _2_()
        slider.addListener(_2_)
        try:
            slider.setValue(0.5)
        except Exception, e:
            e.printStackTrace(System.err)
        left.addComponent(slider)
