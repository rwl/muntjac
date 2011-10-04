# -*- coding: utf-8 -*-
# from com.vaadin.data.Property.ValueChangeListener import (ValueChangeListener,)


class SliderVerticalExample(VerticalLayout):

    def __init__(self):
        self.setSpacing(True)
        value = Label('0')
        value.setSizeUndefined()
        slider = Slider('Select a value between 0 and 100')
        slider.setOrientation(Slider.ORIENTATION_VERTICAL)
        slider.setHeight('200px')
        slider.setMin(0)
        slider.setMax(100)
        slider.setImmediate(True)

        class _0_(ValueChangeListener):

            def valueChange(self, event):
                self.value.setValue(event.getProperty().getValue())

        _0_ = _0_()
        slider.addListener(_0_)
        self.addComponent(slider)
        self.addComponent(value)
        self.setComponentAlignment(slider, Alignment.TOP_CENTER)
        self.setComponentAlignment(value, Alignment.TOP_CENTER)
