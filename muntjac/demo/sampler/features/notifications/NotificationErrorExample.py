
from muntjac.api import VerticalLayout, TextField, button, Button, Alignment
from muntjac.ui.window import Notification


class NotificationErrorExample(VerticalLayout):

    def __init__(self):
        self.setSpacing(True)

        self.setWidth(None)
        # layout will grow with content
        caption = TextField('Caption', 'Upload failed')
        caption.setWidth('200px')
        self.addComponent(caption)

        description = TextField(('Description', 'Invoices-2008.csv could not '
                'be read.<br/>'
                'Perhaps the file is damaged, or in the wrong format?<br/>'
                'Try re-exporting and uploading the file again.'))
        description.setWidth('300px')
        self.addComponent(description)

        class ShowListener(button.IClickListener):

            def __init__(self, c):
                self._c = c

            def buttonClick(self, event):
                self._c.getWindow().showNotification(self.caption.getValue(),
                        self.description.getValue(),
                        Notification.TYPE_ERROR_MESSAGE)

        show = Button('Show notification', ShowListener(self))
        self.addComponent(show)
        self.setComponentAlignment(show, Alignment.MIDDLE_RIGHT)
