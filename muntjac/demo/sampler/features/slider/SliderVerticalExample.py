
from muntjac.api import VerticalLayout, Label, Slider, Alignment
from muntjac.data.property import IValueChangeListener


class SliderVerticalExample(VerticalLayout):

    def __init__(self):
        super(SliderVerticalExample, self).__init__()

        self.setSpacing(True)

        value = Label('0')
        value.setSizeUndefined()

        slider = Slider('Select a value between 0 and 100')
        slider.setOrientation(Slider.ORIENTATION_VERTICAL)
        slider.setHeight('200px')
        slider.setMin(0)
        slider.setMax(100)
        slider.setImmediate(True)

        slider.addListener(SliderListener(value), IValueChangeListener)

        self.addComponent(slider)
        self.addComponent(value)

        self.setComponentAlignment(slider, Alignment.TOP_CENTER)
        self.setComponentAlignment(value, Alignment.TOP_CENTER)


class SliderListener(IValueChangeListener):

    def __init__(self, value):
        self._value = value

    def valueChange(self, event):
        self._value.setValue(event.getProperty().getValue())
