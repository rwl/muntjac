# -*- coding: utf-8 -*-
# from com.vaadin.data.Item import (Item,)
# from com.vaadin.data.Property import (Property,)
# from com.vaadin.ui.HorizontalLayout import (HorizontalLayout,)
# from com.vaadin.ui.NativeSelect import (NativeSelect,)
# from com.vaadin.ui.RichTextArea import (RichTextArea,)
# from com.vaadin.ui.Slider import (Slider,)


class NotificationCustomExample(VerticalLayout):
    _CAPTION_PROPERTY = 'CAPTION'

    def __init__(self):
        # Helper to fill the position select with the various possibilities
        self.setSpacing(True)
        caption = TextField('Caption', 'Message sent')
        caption.setDescription('Main info; a short caption-only notification is often most effective.')
        caption.setWidth('200px')
        self.addComponent(caption)
        description = RichTextArea()
        description.setWidth('100%')
        description.setValue('<p>to <i>john.doe@example.com</i></p>')
        description.setCaption('Description')
        description.setDescription('Additional information; try to keep it short.')
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
        delay.setDescription('Delay before fading<br/>Pull all the way to the left to get -1, which means forever (click to hide).')
        delay.setWidth('100%')
        # 'description' will push width
        delay.setMin(Notification.DELAY_FOREVER)
        delay.setMax(10000)
        self.addComponent(delay)
        # TODO icon select

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                # create Notification instance and customize
                n = Notification(self.caption.getValue(), self.description.getValue(), self.style.getValue())
                n.setPosition(self.position.getValue())
                d = self.delay.getValue()
                n.setDelayMsec(d.intValue())
                # sec->msec
                self.getWindow().showNotification(n)

        _0_ = _0_()
        show = Button('Show notification', _0_)
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

    def initTypeItems(self, type):
        type.addContainerProperty(self._CAPTION_PROPERTY, str, None)
        type.setItemCaptionPropertyId(self._CAPTION_PROPERTY)
        i = type.addItem(Notification.TYPE_HUMANIZED_MESSAGE)
        c = i.getItemProperty(self._CAPTION_PROPERTY)
        c.setValue('Humanized')
        i = type.addItem(Notification.TYPE_WARNING_MESSAGE)
        c = i.getItemProperty(self._CAPTION_PROPERTY)
        c.setValue('Warning')
        i = type.addItem(Notification.TYPE_ERROR_MESSAGE)
        c = i.getItemProperty(self._CAPTION_PROPERTY)
        c.setValue('Error')
        i = type.addItem(Notification.TYPE_TRAY_NOTIFICATION)
        c = i.getItemProperty(self._CAPTION_PROPERTY)
        c.setValue('Tray')
        type.setValue(Notification.TYPE_HUMANIZED_MESSAGE)
