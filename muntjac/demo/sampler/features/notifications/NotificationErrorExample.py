# -*- coding: utf-8 -*-
# from com.vaadin.ui.Alignment import (Alignment,)
# from com.vaadin.ui.TextField import (TextField,)
# from com.vaadin.ui.Window.Notification import (Notification,)


class NotificationErrorExample(VerticalLayout):

    def __init__(self):
        self.setSpacing(True)
        self.setWidth(None)
        # layout will grow with content
        caption = TextField('Caption', 'Upload failed')
        caption.setWidth('200px')
        self.addComponent(caption)
        description = TextField('Description', 'Invoices-2008.csv could not be read.<br/>' + 'Perhaps the file is damaged, or in the wrong format?<br/>' + 'Try re-exporting and uploading the file again.')
        description.setWidth('300px')
        self.addComponent(description)

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                self.getWindow().showNotification(self.caption.getValue(), self.description.getValue(), Notification.TYPE_ERROR_MESSAGE)

        _0_ = _0_()
        show = Button('Show notification', _0_)
        self.addComponent(show)
        self.setComponentAlignment(show, Alignment.MIDDLE_RIGHT)
