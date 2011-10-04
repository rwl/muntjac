# -*- coding: utf-8 -*-


class PopupViewContentsExample(VerticalLayout):

    def __init__(self):
        # Create a dynamically updating content for the popup
        self.setSpacing(True)
        # ------
        # Static content for the minimized view
        # ------
        # Create the content for the popup
        content = Label('This is a simple Label component inside the popup. You can place any Vaadin components here.')
        # The PopupView popup will be as large as needed by the content
        content.setWidth('300px')
        # Construct the PopupView with simple HTML text representing the
        # minimized view
        popup = PopupView('Static HTML content', content)
        self.addComponent(popup)
        # ------
        # Dynamic content for the minimized view
        # ------
        # In this sample we update the minimized view value with the content of
        # the TextField inside the popup.
        popup = PopupView(self.PopupTextField())
        popup.setDescription('Click to edit')
        popup.setHideOnMouseOut(False)
        self.addComponent(popup)

    class PopupTextField(PopupView.Content):
        _tf = TextField('Edit me')
        _root = VerticalLayout()

        def __init__(self):
            self._root.setSizeUndefined()
            self._root.setSpacing(True)
            self._root.setMargin(True)
            self._root.addComponent(Label('The changes made to any components inside the popup are reflected automatically when the popup is closed, but you might want to provide explicit action buttons for the user, like \"Save\" or \"Close\".'))
            self._root.addComponent(self._tf)
            self._tf.setValue('Initial dynamic content')
            self._tf.setWidth('300px')

        def getMinimizedValueAsHTML(self):
            return str(self._tf.getValue())

        def getPopupComponent(self):
            return self._root
