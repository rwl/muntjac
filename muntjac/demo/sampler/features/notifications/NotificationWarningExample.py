
from muntjac.ui import VerticalLayout, TextField, Button, button, Alignment
from muntjac.ui.window import Notification


class NotificationWarningExample(VerticalLayout):

    def __init__(self):
        self.setSpacing(True)

        self.setWidth(None)  # layout will grow with content

        caption = TextField('Caption', 'Upload canceled')
        caption.setWidth('200px')
        self.addComponent(caption)

        description = TextField('Description',
                'Invoices-2008.csv will not be processed')
        description.setWidth('300px')
        self.addComponent(description)

        class ShowListener(button.IClickListener):

            def __init__(self, c):
                self._c = c

            def buttonClick(self, event):
                self._c.getWindow().showNotification(self.caption.getValue(),
                        self.description.getValue(),
                        Notification.TYPE_WARNING_MESSAGE)

        show = Button('Show notification', ShowListener(self))
        self.addComponent(show)
        self.setComponentAlignment(show, Alignment.MIDDLE_RIGHT)
