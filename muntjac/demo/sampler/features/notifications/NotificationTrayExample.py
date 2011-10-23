
from muntjac.api import VerticalLayout, TextField, button, Button, Alignment
from muntjac.ui.window import Notification


class NotificationTrayExample(VerticalLayout):

    def __init__(self):
        self.setSpacing(True)

        self.setWidth(None)  # layout will grow with content

        caption = TextField('Caption', 'New message')
        caption.setWidth('200px')
        self.addComponent(caption)

        description = TextField(('Description', '<b>John:</b> Could you '
                'upload Invoices-2008.csv so that...'))
        description.setWidth('300px')
        self.addComponent(description)

        class ShowListener(button.IClickListener):

            def __init__(self, c):
                self._c = c

            def buttonClick(self, event):
                self._c.getWindow().showNotification(self.caption.getValue(),
                        self.description.getValue(),
                        Notification.TYPE_TRAY_NOTIFICATION)

        show = Button('Show notification', ShowListener(self))
        self.addComponent(show)
        self.setComponentAlignment(show, Alignment.MIDDLE_RIGHT)
