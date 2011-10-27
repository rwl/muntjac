
from muntjac.api import \
    (VerticalLayout, TextField, RichTextArea, HorizontalLayout,
     NativeSelect, Slider, Button, Alignment)

from muntjac.ui.button import IClickListener

from muntjac.ui.window import Notification


class NotificationCustomExample(VerticalLayout):

    _CAPTION_PROPERTY = 'CAPTION'

    def __init__(self):
        super(NotificationCustomExample, self).__init__()

        self.setSpacing(True)

        caption = TextField('Caption', 'Message sent')
        caption.setDescription(('Main info; a short caption-only '
                'notification is often most effective.'))
        caption.setWidth('200px')
        self.addComponent(caption)

        description = RichTextArea()
        description.setWidth('100%')
        description.setValue('<p>to <i>john.doe@example.com</i></p>')
        description.setCaption('Description')
        description.setDescription(('Additional information; '
                'try to keep it short.'))
        self.addComponent(description)

        horiz = HorizontalLayout()
        horiz.setSpacing(True)
        self.addComponent(horiz)

        position = NativeSelect('Position')
        position.setNullSelectionAllowed(False)
        horiz.addComponent(position)
        self.initPositionItems(position)

        style = NativeSelect('Style')
        style.setNullSelectionAllowed(False)
        horiz.addComponent(style)
        self.initTypeItems(style)
        delay = Slider('Delay (msec), -1 means click to hide')
        delay.setDescription(('Delay before fading<br/>Pull all the way to '
                'the left to get -1, which means forever (click to hide).'))
        delay.setWidth('100%')  # 'description' will push width
        delay.setMin(Notification.DELAY_FOREVER)
        delay.setMax(10000)
        self.addComponent(delay)

        # TODO icon select

        l = ShowListener(self, caption, description, style, position, delay)
        show = Button('Show notification', l)
        self.addComponent(show)
        self.setComponentAlignment(show, Alignment.MIDDLE_RIGHT)


    def initPositionItems(self, position):
        # Helper to fill the position select with the various possibilities
        position.addContainerProperty(self._CAPTION_PROPERTY, str, None)
        position.setItemCaptionPropertyId(self._CAPTION_PROPERTY)
        i = position.addItem(Notification.POSITION_TOP_LEFT)
        c = i.getItemProperty(self._CAPTION_PROPERTY)
        c.setValue('Top left')
        i = position.addItem(Notification.POSITION_CENTERED_TOP)
        c = i.getItemProperty(self._CAPTION_PROPERTY)
        c.setValue('Top centered')
        i = position.addItem(Notification.POSITION_TOP_RIGHT)
        c = i.getItemProperty(self._CAPTION_PROPERTY)
        c.setValue('Top right')
        i = position.addItem(Notification.POSITION_CENTERED)
        c = i.getItemProperty(self._CAPTION_PROPERTY)
        c.setValue('Centered')
        i = position.addItem(Notification.POSITION_BOTTOM_LEFT)
        c = i.getItemProperty(self._CAPTION_PROPERTY)
        c.setValue('Bottom left')
        i = position.addItem(Notification.POSITION_CENTERED_BOTTOM)
        c = i.getItemProperty(self._CAPTION_PROPERTY)
        c.setValue('Bottom, centered')
        i = position.addItem(Notification.POSITION_BOTTOM_RIGHT)
        c = i.getItemProperty(self._CAPTION_PROPERTY)
        c.setValue('Bottom right')
        position.setValue(Notification.POSITION_CENTERED)


    def initTypeItems(self, typ):
        # Helper to fill the position select with the various possibilities
        typ.addContainerProperty(self._CAPTION_PROPERTY, str, None)
        typ.setItemCaptionPropertyId(self._CAPTION_PROPERTY)
        i = typ.addItem(Notification.TYPE_HUMANIZED_MESSAGE)
        c = i.getItemProperty(self._CAPTION_PROPERTY)
        c.setValue('Humanized')
        i = typ.addItem(Notification.TYPE_WARNING_MESSAGE)
        c = i.getItemProperty(self._CAPTION_PROPERTY)
        c.setValue('Warning')
        i = typ.addItem(Notification.TYPE_ERROR_MESSAGE)
        c = i.getItemProperty(self._CAPTION_PROPERTY)
        c.setValue('Error')
        i = typ.addItem(Notification.TYPE_TRAY_NOTIFICATION)
        c = i.getItemProperty(self._CAPTION_PROPERTY)
        c.setValue('Tray')
        typ.setValue(Notification.TYPE_HUMANIZED_MESSAGE)


class ShowListener(IClickListener):

    def __init__(self, c, caption, description, style, position, delay):
        self._c = c
        self._caption = caption
        self._description = description
        self._style = style
        self._position = position
        self._delay = delay

    def buttonClick(self, event):
        # create Notification instance and customize
        n = Notification(self._caption.getValue(),
                self._description.getValue(), self._style.getValue())
        n.setPosition(self._position.getValue())
        d = self._delay.getValue()
        n.setDelayMsec( int(d) )  # sec->msec
        self._c.getWindow().showNotification(n)
