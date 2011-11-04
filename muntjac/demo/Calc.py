
from muntjac.api import Application, Button, GridLayout, Label, Window

from muntjac.ui.button import IClickListener


class Calc(Application, IClickListener):
    """A simple calculator using Muntjac."""

    def __init__(self):
        super(Calc, self).__init__()

        # All variables are automatically stored in the session.
        self._current = 0.0
        self._stored = 0.0
        self._lastOperationRequested = 'C'

        # User interface components
        self._display = Label('0.0')


    def init(self):
        # Application.init is called once for each application. Here it
        # creates the UI and connects it to the business logic.

        # Create the main layout for our application (4 columns, 5 rows)
        layout = GridLayout(4, 5)

        # Create the main window for the application using the main layout.
        # The main window is shown when the application is starts.
        self.setMainWindow(Window('Calculator Application', layout))

        # Create a result label that over all 4 columns in the first row
        layout.addComponent(self._display, 0, 0, 3, 0)

        # The operations for the calculator in the order they appear on the
        # screen (left to right, top to bottom)
        operations = ['7', '8', '9', '/', '4', '5', '6',
                '*', '1', '2', '3', '-', '0', '=', 'C', '+']

        for caption in operations:
            # Create a button and use this application for event handling
            button = Button(caption)
            button.addListener(self)

            # Add the button to our main layout
            layout.addComponent(button)


    def buttonClick(self, event):
        # Event handler for button clicks. Called for all the buttons in
        # the application.

        # Get the button that was clicked
        button = event.getButton()

        # Get the requested operation from the button caption
        requestedOperation = button.getCaption()[0]

        # Calculate the new value
        newValue = self.calculate(requestedOperation)

        # Update the result label with the new value
        self._display.setValue(newValue)


    def calculate(self, requestedOperation):
        # Calculator "business logic" implemented here to keep the example
        # minimal

        if '0' <= requestedOperation and requestedOperation <= '9':
            self._current = ((self._current * 10) +
                    float('' + requestedOperation))
            return self._current

        last = self._lastOperationRequested
        if last == '+':
            self._stored += self._current
        elif last == '-':
            self._stored -= self._current
        elif last == '/':
            try:
                self._stored /= self._current
            except ZeroDivisionError:
                pass
        elif last == '*':
            self._stored *= self._current
        elif last == 'C':
            self._stored = self._current

        self._lastOperationRequested = requestedOperation
        self._current = 0.0

        if requestedOperation == 'C':
            self._stored = 0.0

        return self._stored


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(Calc, nogui=True, forever=True, debug=True)
