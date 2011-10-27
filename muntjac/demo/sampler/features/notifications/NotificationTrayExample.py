
from muntjac.api import VerticalLayout, TextField, Button, Alignment
from muntjac.ui.window import Notification
from muntjac.ui.button import IClickListener


class NotificationTrayExample(VerticalLayout):

    def __init__(self):
        super(NotificationTrayExample, self).__init__()

        self.setSpacing(True)

        self.setWidth(None)  # layout will grow with content

        caption = TextField('Caption', 'New message')
        caption.setWidth('200px')
        self.addComponent(caption)

        description = TextField('Description', '<b>John:</b> Could you '
                'upload Invoices-2008.csv so that...')
        description.setWidth('300px')
        self.addComponent(description)

        l = ShowListener(self, caption, description)
        show = Button('Show notification', l)
        self.addComponent(show)
        self.setComponentAlignment(show, Alignment.MIDDLE_RIGHT)


class ShowListener(IClickListener):

    def __init__(self, c, caption, description):
        self._c = c
        self._caption = caption
        self._description = description

    def buttonClick(self, event):
        self._c.getWindow().showNotification(self._caption.getValue(),
                self._description.getValue(),
                Notification.TYPE_TRAY_NOTIFICATION)
