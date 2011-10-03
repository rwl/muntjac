
from time import sleep

from muntjac.ui import CustomComponent, VerticalLayout, Label, TabSheet


class ClientCachingExample(CustomComponent):
    """This example is a (simple) demonstration of client-side caching. The
    content in one tab is intentionally made very slow to produce server-side.
    When the user changes to this tab for the first time, there will be a 3
    second wait before the content shows up, but the second time it shows up
    immediately since the content has not changed and is cached client-side.

    @author IT Mill Ltd.
    """

    _msg = ('This example is a (simple) demonstration of client-side caching.'
        + ' The content in one tab is intentionally made very slow to'
        + ' \'produce\' server-side. When you changes to this tab for the'
        + ' first time, there will be a 3 second wait before the content'
        + ' shows up, but the second time it shows up immediately since the'
        + ' content has not changed and is cached client-side.')

    def __init__(self):
        main = VerticalLayout()
        main.setMargin(True)
        self.setCompositionRoot(main)

        main.addComponent(Label(self._msg))

        ts = TabSheet()
        main.addComponent(ts)

        layout = VerticalLayout()
        layout.setMargin(True)
        l = Label('This is a normal label, quick to render.')
        l.setCaption('A normal label')
        layout.addComponent(l)

        ts.addTab(layout, 'Normal', None)

        layout = VerticalLayout()
        layout.setMargin(True)

        class SlowLabel(Label):

            def __init__(self):
                super(SlowLabel, self).__init__(('Slow label - until '
                        'cached client side.'))

            def paintContent(self, target):
                try:
                    sleep(3000)  # FIXME: Thread
                except Exception:
                    pass  # IGNORED
                super(SlowLabel, self).paintContent(target)

        l = SlowLabel()
        l.setCaption('A slow label')
        layout.addComponent(l)
        ts.addTab(layout, 'Slow', None)
