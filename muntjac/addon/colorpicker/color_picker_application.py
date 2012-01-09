# Copyright (C) 2011 Vaadin Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

from StringIO import StringIO

from datetime import datetime as Date

from muntjac.addon.colorpicker.color import Color

from muntjac.application import Application

from muntjac.ui.check_box import CheckBox
from muntjac.terminal.stream_resource import IStreamSource, StreamResource
from muntjac.ui.window import Window
from muntjac.ui.embedded import Embedded
from muntjac.ui.panel import Panel
from muntjac.ui.vertical_layout import VerticalLayout
from muntjac.ui.horizontal_layout import HorizontalLayout
from muntjac.ui.grid_layout import GridLayout
from muntjac.ui.button import IClickListener
from muntjac.ui.alignment import Alignment

from muntjac.addon.colorpicker.color_picker \
    import ColorPicker, ButtonStyle, IColorChangeListener


class ColorPickerApplication(Application, IColorChangeListener):
    """Testing application for the ColorPicker.

    @author: John Ahlroos / ITMill Oy Ltd 2010
    @author: Richard Lincoln
    """

    _VERSION = '@VERSION@'

    def __init__(self):
        super(ColorPickerApplication, self).__init__()

        # The foreground color.
        self._foregroundColor = Color.BLACK  # The currently selected

        # The background color.
        self._backgroundColor = Color.WHITE  # The currently selected

        # The display box where the image is rendered.
        self._display = None

        self._colorpicker1 = None
        self._colorpicker2 = None
        self._colorpicker3 = None
        self._colorpicker4 = None
        self._colorpicker5 = None
        self._colorpicker6 = None

        self._rgbVisible = True
        self._hsvVisible = True
        self._swaVisible = True
        self._historyVisible = True
        self._txtfieldVisible = True

        self._rgbBox = CheckBox('RGB tab visible')
        self._hsvBox = CheckBox('HSV tab visible')
        self._swaBox = CheckBox('Swatches tab visible')
        self._hisBox = CheckBox('History visible')
        self._txtBox = CheckBox('CSS field visible')


    def setPopupVisibilities(self):
        self._rgbBox.setEnabled(not (self._rgbVisible
                and not self._hsvVisible and not self._swaVisible))

        self._hsvBox.setEnabled(not (not self._rgbVisible
                and self._hsvVisible and not self._swaVisible))

        self._swaBox.setEnabled(not (not self._rgbVisible
                and not self._hsvVisible and self._swaVisible))

        self._colorpicker1.setRGBVisibility(self._rgbVisible)
        self._colorpicker2.setRGBVisibility(self._rgbVisible)
        self._colorpicker3.setRGBVisibility(self._rgbVisible)
        self._colorpicker4.setRGBVisibility(self._rgbVisible)
        self._colorpicker5.setRGBVisibility(self._rgbVisible)
        self._colorpicker6.setRGBVisibility(self._rgbVisible)

        self._colorpicker1.setHSVVisibility(self._hsvVisible)
        self._colorpicker2.setHSVVisibility(self._hsvVisible)
        self._colorpicker3.setHSVVisibility(self._hsvVisible)
        self._colorpicker4.setHSVVisibility(self._hsvVisible)
        self._colorpicker5.setHSVVisibility(self._hsvVisible)
        self._colorpicker6.setHSVVisibility(self._hsvVisible)

        self._colorpicker1.setSwatchesVisibility(self._swaVisible)
        self._colorpicker2.setSwatchesVisibility(self._swaVisible)
        self._colorpicker3.setSwatchesVisibility(self._swaVisible)
        self._colorpicker4.setSwatchesVisibility(self._swaVisible)
        self._colorpicker5.setSwatchesVisibility(self._swaVisible)
        self._colorpicker6.setSwatchesVisibility(self._swaVisible)

        self._colorpicker1.setHistoryVisibility(self._historyVisible)
        self._colorpicker2.setHistoryVisibility(self._historyVisible)
        self._colorpicker3.setHistoryVisibility(self._historyVisible)
        self._colorpicker4.setHistoryVisibility(self._historyVisible)
        self._colorpicker5.setHistoryVisibility(self._historyVisible)
        self._colorpicker6.setHistoryVisibility(self._historyVisible)

        self._colorpicker1.setTextfieldVisibility(self._txtfieldVisible)
        self._colorpicker2.setTextfieldVisibility(self._txtfieldVisible)
        self._colorpicker3.setTextfieldVisibility(self._txtfieldVisible)
        self._colorpicker4.setTextfieldVisibility(self._txtfieldVisible)
        self._colorpicker5.setTextfieldVisibility(self._txtfieldVisible)
        self._colorpicker6.setTextfieldVisibility(self._txtfieldVisible)


    def init(self):
        # This is called whenever a colorpicker popup is closed
        main = Window()
        main.setWidth('1000px')
        self.setMainWindow(main)

        # Create an instance of the preview and add it to the window
        self._display = Embedded('Color preview')
        self._display.setWidth('270px')
        self._display.setHeight('270px')

        # Add the foreground and background colorpickers to a layout
        mainLayout = HorizontalLayout()
        mainLayout.setMargin(True)
        mainLayout.setSpacing(True)
        main.setContent(mainLayout)

        layout = VerticalLayout()
        layout.setWidth('450px')
        layout.setSpacing(True)

        optPanel = Panel('Customize the color picker popup window',
                GridLayout(3, 2))
        optPanel.getContent().setSizeFull()
        optPanel.getContent().setMargin(True)
        optPanel.getContent().setSpacing(True)

        self._rgbBox.addListener(RgbClickListener(self), IClickListener)
        self._rgbBox.setValue(self._rgbVisible)
        self._rgbBox.setImmediate(True)
        optPanel.getContent().addComponent(self._rgbBox)

        self._hsvBox.addListener(HsvClickListener(self), IClickListener)
        self._hsvBox.setValue(self._hsvVisible)
        self._hsvBox.setImmediate(True)
        optPanel.getContent().addComponent(self._hsvBox)

        self._swaBox.addListener(SwaClickListener(self), IClickListener)
        self._swaBox.setValue(self._swaVisible)
        self._swaBox.setImmediate(True)
        optPanel.getContent().addComponent(self._swaBox)

        self._hisBox.addListener(HisClickListener(self), IClickListener)
        self._hisBox.setValue(self._historyVisible)
        self._hisBox.setImmediate(True)
        optPanel.getContent().addComponent(self._hisBox)

        self._txtBox.addListener(TxtClickListener(self), IClickListener)
        self._txtBox.setValue(self._txtfieldVisible)
        self._txtBox.setImmediate(True)
        optPanel.getContent().addComponent(self._txtBox)

        layout.addComponent(optPanel)

        panel1 = Panel(
                'Button like colorpicker with current color and CSS code',
                HorizontalLayout())
        panel1.getContent().setSizeFull()
        panel1.getContent().setMargin(True)

        self._colorpicker1 = ColorPicker('Foreground', self._foregroundColor)
        self._colorpicker1.setWidth('100px')
        self._colorpicker1.addListener(self)
        panel1.addComponent(self._colorpicker1)
        panel1.getContent().setComponentAlignment(self._colorpicker1,
                Alignment.MIDDLE_CENTER)

        self._colorpicker2 = ColorPicker('Background', self._backgroundColor)
        self._colorpicker2.addListener(self)
        self._colorpicker2.setWidth('100px')
        panel1.addComponent(self._colorpicker2)
        panel1.getContent().setComponentAlignment(self._colorpicker2,
                Alignment.MIDDLE_CENTER)
        layout.addComponent(panel1)

        panel2 = Panel(
                'Button like colorpicker with current color and custom caption',
                HorizontalLayout())
        panel2.getContent().setSizeFull()
        panel2.getContent().setMargin(True)
        self._colorpicker3 = ColorPicker('Foreground', self._foregroundColor)
        self._colorpicker3.addListener(self)
        self._colorpicker3.setWidth('120px')
        self._colorpicker3.setButtonCaption('Foreground')
        panel2.addComponent(self._colorpicker3)
        panel2.getContent().setComponentAlignment(self._colorpicker3,
                Alignment.MIDDLE_CENTER)

        self._colorpicker4 = ColorPicker('Background', self._backgroundColor)
        self._colorpicker4.addListener(self)
        self._colorpicker4.setWidth('120px')
        self._colorpicker4.setButtonCaption('Background')
        panel2.addComponent(self._colorpicker4)
        panel2.getContent().setComponentAlignment(self._colorpicker4,
                Alignment.MIDDLE_CENTER)
        layout.addComponent(panel2)

        panel3 = Panel(
                'Color area color picker with caption',
                HorizontalLayout())
        panel3.getContent().setSizeFull()
        panel3.getContent().setMargin(True)

        self._colorpicker5 = ColorPicker('Foreground', self._foregroundColor)
        self._colorpicker5.setCaption('Foreground')
        self._colorpicker5.addListener(self)
        self._colorpicker5.setButtonStyle(ButtonStyle.BUTTON_AREA)
        panel3.addComponent(self._colorpicker5)
        panel3.getContent().setComponentAlignment(self._colorpicker5,
                Alignment.MIDDLE_CENTER)

        self._colorpicker6 = ColorPicker('Background', self._backgroundColor)
        self._colorpicker6.setCaption('Background')
        self._colorpicker6.addListener(self)
        self._colorpicker6.setButtonStyle(ButtonStyle.BUTTON_AREA)
        panel3.addComponent(self._colorpicker6)
        panel3.getContent().setComponentAlignment(self._colorpicker6,
                Alignment.MIDDLE_CENTER)
        layout.addComponent(panel3)

        mainLayout.addComponent(layout)
        mainLayout.addComponent(self._display)

        self.updateDisplay(self._foregroundColor, self._backgroundColor)


    def updateDisplay(self, fg, bg):
        """Update display.

        @param fg:
                   the foreround color
        @param bg:
                   the background color
        """
        imagesource = MyImageSource(fg, bg)
        now = Date.now()
        frmt = '%H%M%S'
        imageresource = StreamResource(imagesource,
                'myimage' + now.strftime(frmt) + '.png', self)
        imageresource.setCacheTime(0)
        self._display.setSource(imageresource)


    def colorChanged(self, event):
        if ((event.getSource() == self._colorpicker1)
                or (event.getSource() == self._colorpicker3)
                or (event.getSource() == self._colorpicker5)):
            self._foregroundColor = event.getColor()

            if event.getSource() != self._colorpicker1:
                self._colorpicker1.setColor(event.getColor())

            if event.getSource() != self._colorpicker3:
                self._colorpicker3.setColor(event.getColor())

            if event.getSource() != self._colorpicker5:
                self._colorpicker5.setColor(event.getColor())
        elif ((event.getSource() == self._colorpicker2)
                or (event.getSource() == self._colorpicker4)
                or (event.getSource() == self._colorpicker6)):
            self._backgroundColor = event.getColor()

            if event.getSource() != self._colorpicker2:
                self._colorpicker2.setColor(event.getColor())

            if event.getSource() != self._colorpicker4:
                self._colorpicker4.setColor(event.getColor())

            if event.getSource() != self._colorpicker6:
                self._colorpicker6.setColor(event.getColor())
        else:
            return

        self.updateDisplay(self._foregroundColor, self._backgroundColor)


    def getVersion(self):
        return self._VERSION


class _ColorClickListener(IClickListener):

    def __init__(self, app):
        self._app = app


class RgbClickListener(_ColorClickListener):

    def buttonClick(self, event):
        self._app._rgbVisible = bool(str(event.getButton().getValue()))
        self._app.setPopupVisibilities()


class HsvClickListener(_ColorClickListener):

    def buttonClick(self, event):
        self._app._hsvVisible = bool(str(event.getButton().getValue()))
        self._app.setPopupVisibilities()


class SwaClickListener(_ColorClickListener):

    def buttonClick(self, event):
        self._app._swaVisible = bool(str(event.getButton().getValue()))
        self._app.setPopupVisibilities()


class HisClickListener(_ColorClickListener):

    def buttonClick(self, event):
        self._app._historyVisible = bool(str(event.getButton().getValue()))
        self._app.setPopupVisibilities()


class TxtClickListener(_ColorClickListener):

    def buttonClick(self, event):
        self._app._txtfieldVisible = bool(str(event.getButton().getValue()))
        self._app.setPopupVisibilities()


class MyImageSource(IStreamSource):
    """This class is used to represent the preview of the color selection."""

    def __init__(self, fg, bg):
        """Instantiates a new my image source.

        @param fg:
                   the foreground color
        @param bg:
                   the background color
        """
        self._imagebuffer = None

        self._fgColor = fg
        self._bgColor = bg


    def getStream(self):
        from PIL import Image, ImageDraw  # PIL dependency

        # Create an image and draw something on it.
        image = Image.new("RGB", (270, 270))
        drawable = ImageDraw.Draw(image)
        drawable.rectangle([0, 0, 270, 270], fill=str(Color.BLUE))
        drawable.rectangle([1, 1, 268, 268], fill=str(self._bgColor))
        drawable.ellipse([25, 25, 245, 245], fill=str(self._fgColor))
        drawable.text((50, 100),
                'r=' + str(self._fgColor.getRed()) +
                ',g=' + str(self._fgColor.getGreen()) +
                ',b=' + str(self._fgColor.getBlue()), fill=str(Color.BLACK))
        drawable.text((5, 15),
                'r=' + str(self._bgColor.getRed()) +
                ',g=' + str(self._bgColor.getGreen()) +
                ',b=' + str(self._bgColor.getBlue()), fill=str(Color.BLACK))

        del drawable

        try:
            # Write the image to a buffer.
            self._imagebuffer = StringIO()
            image.save(self._imagebuffer, 'PNG')
            return self._imagebuffer
        except IOError:
            return None


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(ColorPickerApplication, nogui=True, forever=True, debug=True)
