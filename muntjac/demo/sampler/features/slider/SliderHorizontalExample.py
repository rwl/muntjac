# -*- coding: utf-8 -*-


class SliderHorizontalExample(HorizontalLayout):

    def __init__(self):
        self.setSpacing(True)
        self.setWidth('100%')
        value = Label('0')
        value.setWidth('3em')
        slider = Slider('Select a value between 0 and 100')
        slider.setWidth('100%')
        slider.setMin(0)
        slider.setMax(100)
        slider.setImmediate(True)

        class _0_(ValueChangeListener):

            def valueChange(self, event):
                self.value.setValue(event.getProperty().getValue())

        _0_ = _0_()
        slider.addListener(_0_)
        self.addComponent(slider)
        self.setExpandRatio(slider, 1)
        self.addComponent(value)
        self.setComponentAlignment(value, Alignment.BOTTOM_LEFT)
