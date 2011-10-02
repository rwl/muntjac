# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@


class NotificationExample(CustomComponent):
    """Demonstrates the use of Notifications.

    @author IT Mill Ltd.
    @see com.vaadin.ui.Window
    """
    # Dropdown select for notification type, using the native dropdown
    _type = None
    # Textfield for the notification caption
    _caption = None
    # Textfield for the notification content
    _message = None

    def __init__(self):
        """Default constructor; We're subclassing CustomComponent, so we need to
        choose a root component and set it as composition root.
        """
        # Main layout
        main = VerticalLayout()
        main.setSizeUndefined()
        main.setSpacing(True)
        main.setMargin(True)
        # use theme-specific margin
        self.setCompositionRoot(main)
        # Create the 'type' dropdown select.
        self._type = NativeSelect('Notification type')
        main.addComponent(self._type)
        # no empty selection allowed
        self._type.setNullSelectionAllowed(False)
        # we want a different caption than the value
        self._type.addContainerProperty('caption', str, None)
        self._type.setItemCaptionMode(AbstractSelect.ITEM_CAPTION_MODE_PROPERTY)
        self._type.setItemCaptionPropertyId('caption')
        # add some content (items) using the Container API
        i = self._type.addItem(Integer.valueOf.valueOf(Window.Notification.TYPE_HUMANIZED_MESSAGE))
        i.getItemProperty('caption').setValue('Humanized message')
        i = self._type.addItem(Integer.valueOf.valueOf(Window.Notification.TYPE_WARNING_MESSAGE))
        i.getItemProperty('caption').setValue('Warning message')
        i = self._type.addItem(Integer.valueOf.valueOf(Window.Notification.TYPE_ERROR_MESSAGE))
        i.getItemProperty('caption').setValue('Error message')
        i = self._type.addItem(Integer.valueOf.valueOf(Window.Notification.TYPE_TRAY_NOTIFICATION))
        i.getItemProperty('caption').setValue('Tray notification')
        # set the initially selected item
        self._type.setValue(Integer.valueOf.valueOf(Window.Notification.TYPE_HUMANIZED_MESSAGE))
        # Notification caption
        self._caption = TextField('Caption')
        main.addComponent(self._caption)
        self._caption.setColumns(20)
        self._caption.setValue('Brown Fox!')
        # Notification message
        self._message = RichTextArea()
        main.addComponent(self._message)
        self._message.setCaption('Message')
        self._message.setValue('A quick one jumped over the lazy dog.')
        # Button to show the notification

        class _0_(ClickListener):

            def buttonClick(self, event):
                # show the notification
                self.getWindow().showNotification(NotificationExample_this._caption.getValue(), NotificationExample_this._message.getValue(), NotificationExample_this._type.getValue().intValue())

        _0_ = _0_()
        b = Button('Show notification', _0_)
        main.addComponent(b)
        main.setComponentAlignment(b, Alignment.MIDDLE_RIGHT)
