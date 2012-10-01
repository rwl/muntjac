# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.application import Application
from muntjac.ui.window import Window
from muntjac.ui.vertical_layout import VerticalLayout
from muntjac.ui.horizontal_layout import HorizontalLayout
from muntjac.ui.text_field import TextField
from muntjac.ui.button import Button, IClickListener

from muntjac.addon.borderlayout.border_layout import BorderLayout, Constraint

from muntjac.ui.themes.reindeer import Reindeer


class BorderLayoutApplication(Application):

    def init(self):
        self._components = [None] * 5
        self._texts = ['NORTH', 'SOUTH', 'CENTER', 'EAST', 'WEST']

        mainWindow = Window('BorderLayout Application')
        vlo = VerticalLayout()
        vlo.setHeight('100%')
        vlo.setWidth('100%')
        vlo.setSpacing(True)
        mainWindow.setContent(vlo)
        vlo.addComponent(self.getTestButtons())
        for i in range(5):
            self._components[i] = TextField(self._texts[i])
            self._components[i].setSizeFull()
        self._bl = BorderLayout()
        self._bl.addStyleName(Reindeer.LAYOUT_WHITE)
        vlo.addComponent(self._bl)
        vlo.setExpandRatio(self._bl, 1)
        self._bl.addComponent(self._components[0], Constraint.NORTH)
        self._bl.addComponent(self._components[1], Constraint.SOUTH)
        self._bl.addComponent(self._components[2], Constraint.CENTER)
        self._bl.addComponent(self._components[3], Constraint.EAST)
        self._bl.addComponent(self._components[4], Constraint.WEST)
        self.setMainWindow(mainWindow)


    def getTestButtons(self):
        vlo = VerticalLayout()
        vlo.setSpacing(True)
        hlo1 = HorizontalLayout()
        hlo2 = HorizontalLayout()
        hlo3 = HorizontalLayout()
        hlo1.setSpacing(True)
        hlo2.setSpacing(True)
        hlo3.setSpacing(True)
        button1 = Button('Set height 100%')
        button2 = Button('Set height 500px')
        button3 = Button('Set width 400px')
        button4 = Button('Set size full')
        button5 = Button('Remove center')
        button6 = Button('Remove south')
        button7 = Button('Add center')
        button8 = Button('Add south')
        button9 = Button('Remove north')
        button10 = Button('Add north')
        button11 = Button('Toggle margin')
        button12 = Button('Toggle spacing')
        hlo1.addComponent(button2)
        hlo1.addComponent(button3)
        hlo1.addComponent(button4)
        hlo1.addComponent(button1)
        hlo2.addComponent(button5)
        hlo2.addComponent(button7)
        hlo2.addComponent(button6)
        hlo2.addComponent(button8)
        hlo2.addComponent(button9)
        hlo2.addComponent(button10)
        hlo3.addComponent(button11)
        hlo3.addComponent(button12)
        vlo.addComponent(hlo1)
        vlo.addComponent(hlo2)
        vlo.addComponent(hlo3)

        button1.addListener(ClickListener1(self._bl, self._components))
        button2.addListener(ClickListener2(self._bl, self._components))
        button3.addListener(ClickListener3(self._bl, self._components))
        button4.addListener(ClickListener4(self._bl, self._components))
        button5.addListener(ClickListener5(self._bl, self._components))
        button6.addListener(ClickListener6(self._bl, self._components))
        button7.addListener(ClickListener7(self._bl, self._components))
        button8.addListener(ClickListener8(self._bl, self._components))
        button9.addListener(ClickListener9(self._bl, self._components))
        button10.addListener(ClickListener10(self._bl, self._components))
        button11.addListener(ClickListener11(self._bl, self._components))
        button12.addListener(ClickListener12(self._bl, self._components))

        return vlo


class ClickListener(IClickListener):

    def __init__(self, bl, components):
        self._bl = bl
        self._components = components


class ClickListener1(ClickListener):

    def buttonClick(self, event):
        self._bl.setHeight('100%')


class ClickListener2(IClickListener):

    def buttonClick(self, event):
        self._bl.setHeight('500px')


class ClickListener3(IClickListener):

    def buttonClick(self, event):
        self._bl.setWidth('400px')


class ClickListener4(IClickListener):

    def buttonClick(self, event):
        self._bl.setSizeFull()


class ClickListener5(IClickListener):

    def buttonClick(self, event):
        self._bl.removeComponent(self._components[2])


class ClickListener6(IClickListener):

    def buttonClick(self, event):
        self._bl.removeComponent(self._components[1])


class ClickListener7(IClickListener):

    def buttonClick(self, event):
        self._bl.addComponent(self._components[2], Constraint.CENTER)


class ClickListener8(IClickListener):

    def buttonClick(self, event):
        self._bl.addComponent(self._components[1], Constraint.SOUTH)


class ClickListener9(IClickListener):

    def buttonClick(self, event):
        self._bl.removeComponent(self._components[0])


class ClickListener10(IClickListener):

    def buttonClick(self, event):
        self._bl.addComponent(self._components[0], Constraint.NORTH)


class ClickListener11(IClickListener):

    def __init__(self, bl, components):
        super(ClickListener10, self).__init__(bl, components)
        self._margin = False

    def buttonClick(self, event):
        self._margin = not self._margin
        self._bl.setMargin(self._margin)


class ClickListener12(IClickListener):

    def buttonClick(self, event):
        self._bl.setSpacing(not self._bl.isSpacing())


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(BorderLayoutApplication, nogui=True, forever=True, debug=True)
