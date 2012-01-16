
from muntjac.api \
    import Application, Window, Label, NativeSelect, Button, GridLayout

from muntjac.ui.themes.reindeer \
    import Reindeer

from muntjac.ui.button \
    import IClickListener

from muntjac.addon.csstools.render_info \
    import RenderInfo, ICallback

from muntjac.addon.csstools.client.v_render_info_fetcher \
    import CssProperty


class CssToolsTestApplication(Application):

    def __init__(self):
        Application.__init__(self)

        self._props = dict()


    def init(self):
        main = Window('CSS Tools Add-on Test')
        self.setMainWindow(main)

        testWindow = Window('Normal Window')
        testWindow.addComponent(Label(
                "<p>This window is used as the component to measure.</p>",
                Label.CONTENT_XHTML))
        main.addWindow(testWindow)
        testWindow.center()

        title = Label('CSS Properties to Retrieve')
        title.addStyleName(Reindeer.LABEL_H2)
        main.addComponent(title)

        target = NativeSelect('Target Component')
        main.addComponent(target)

        get = Button('Refresh Properties', GetClickListener(self, target))
        main.addComponent(get)

        main.addComponent(self.buildLabels())

        target.addItem(main.getContent())
        target.setItemCaption(main.getContent(), 'Root layout')
        target.addItem(testWindow)
        target.setItemCaption(testWindow, 'Sub window')
        target.addItem(get)
        target.setItemCaption(get, 'The \'' + get.getCaption() + '\' Button')
        target.setNullSelectionAllowed(False)
        target.select(testWindow)


    def buildLabels(self):
        grid = GridLayout()
        grid.setSpacing(True)
        grid.setWidth('100%')
        grid.setColumns(6)
        for prop in CssProperty.values():
            l = Label('-')
            l.setSizeUndefined()
            l.setCaption(str(prop))
            self._props[prop] = l
            grid.addComponent(l)
        return grid


class GetClickListener(IClickListener):

    def __init__(self, app, target):
        self._app = app
        self._target = target

    def buttonClick(self, event):
        RenderInfo.get(self._target.getValue(), GetCallback(self._app))


class GetCallback(ICallback):

    def __init__(self, app):
        self._app = app

    def infoReceived(self, info):
        for prop in CssProperty.values():
            self._app._props[prop].setValue(str(info.getProperty(prop)))


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(CssToolsTestApplication, nogui=True, forever=True, debug=True,
            widgetset='org.vaadin.csstools.CssToolsWidgetset')
