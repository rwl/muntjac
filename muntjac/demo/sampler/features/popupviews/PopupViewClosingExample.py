
from muntjac.api import VerticalLayout, Label, PopupView
from muntjac.ui.popup_view import IPopupVisibilityListener


class PopupViewClosingExample(VerticalLayout, IPopupVisibilityListener):

    def __init__(self):
        super(PopupViewClosingExample, self).__init__()

        self.setSpacing(True)

        # Create the content for the popup
        content = Label('This popup will close as soon as you move the '
                'mouse cursor outside of the popup area.')
        # The PopupView popup will be as large as needed by the content
        content.setWidth('300px')
        # Construct the PopupView with simple HTML text representing the
        # minimized view
        popup = PopupView('Default popup', content)
        popup.setHideOnMouseOut(True)
        popup.addListener(self, IPopupVisibilityListener)
        self.addComponent(popup)

        content = Label('This popup will only close if you click '
                'the mouse outside the popup area.')
        # The PopupView popup will be as large as needed by the content
        content.setWidth('300px')
        popup = PopupView('Popup that won\'t auto-close', content)
        popup.setHideOnMouseOut(False)
        popup.addListener(self, IPopupVisibilityListener)
        self.addComponent(popup)


    def popupVisibilityChange(self, event):  # FIXME: not fired
        if not event.isPopupVisible():
            self.getWindow().showNotification('Popup closed')
