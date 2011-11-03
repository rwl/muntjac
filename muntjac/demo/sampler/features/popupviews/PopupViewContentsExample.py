
from muntjac.api import VerticalLayout, Label, PopupView, TextField
from muntjac.ui import popup_view


class PopupViewContentsExample(VerticalLayout):  # FIXME: only works once

    def __init__(self):
        super(PopupViewContentsExample, self).__init__()

        self.setSpacing(True)

        # ------
        # Static content for the minimized view
        # ------

        # Create the content for the popup
        content = Label('This is a simple Label component inside the popup. '
                'You can place any Muntjac components here.')

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
        popup = PopupView( PopupTextField() )
        popup.setDescription('Click to edit')
        popup.setHideOnMouseOut(False)
        self.addComponent(popup)


# Create a dynamically updating content for the popup
class PopupTextField(popup_view.IContent):

    def __init__(self):
        self._root = VerticalLayout()
        self._tf = TextField('Edit me')

        self._root.setSizeUndefined()
        self._root.setSpacing(True)
        self._root.setMargin(True)
        self._root.addComponent(Label(('The changes made to any components '
                'inside the popup are reflected automatically when the popup '
                'is closed, but you might want to provide explicit action '
                'buttons for the user, like \"Save\" or \"Close\".')))
        self._root.addComponent(self._tf)

        self._tf.setValue('Initial dynamic content')
        self._tf.setWidth('300px')


    def getMinimizedValueAsHTML(self):
        return str(self._tf.getValue())


    def getPopupComponent(self):
        return self._root
