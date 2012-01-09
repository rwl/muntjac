
from muntjac.api import Application, Window, Label

from muntjac.addon.colorpicker.color import Color

from muntjac.addon.colorpicker.color_picker import ColorPicker


class ColorPickerDemo(Application):

    def init(self):
        mainWindow = Window("Color Picker Demo Application")
        label = Label("Hello Muntjac user")
        mainWindow.addComponent(label)
        self.setMainWindow(mainWindow)

        # Create the color picker
        cp = ColorPicker("Our ColorPicker", Color.RED)
        mainWindow.addComponent(cp)

        # Set the button caption
        cp.setButtonCaption("Our color")

        # Hide the color history
#        cp.setHistoryVisibility(False)

        # Hide the HSV tab
#        cp.setHSVVisibility(False)

        # Hide the RGB tab
#        cp.setRGBVisibility(False)


    def colorChanged(self, event):
        self.getMainWindow().showNotification("Color changed!")


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(ColorPickerDemo, nogui=True, forever=True, debug=True)
