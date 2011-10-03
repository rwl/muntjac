
from muntjac import Application
from muntjac.ui.button import IClickListener
from muntjac.ui import GridLayout, Label, Window, Button


class Calc(Application, IClickListener):
    """A simple calculator using Vaadin."""

    def __init__(self):
        # All variables are automatically stored in the session.
        self._current = 0.0
        self._stored = 0.0
        self._lastOperationRequested = 'C'

        # User interface components
        self._display = Label('0.0')

    # Application.init is called once for each application. Here it creates
    # the UI and connects it to the business logic.
    def init(self):
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

    # Event handler for button clicks. Called for all the buttons in the
    # application.
    def buttonClick(self, event):
        # Get the button that was clicked
        button = event.getButton()

        # Get the requested operation from the button caption
        requestedOperation = button.getCaption()[0]

        # Calculate the new value
        newValue = self.calculate(requestedOperation)

        # Update the result label with the new value
        self._display.setValue(newValue)

    # Calculator "business logic" implemented here to keep the example minimal
    def calculate(self, requestedOperation):
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
            self._stored /= self._current
        elif last == '*':
            self._stored *= self._current
        elif last == 'C':
            self._stored = self._current

        self._lastOperationRequested = requestedOperation
        self._current = 0.0

        if requestedOperation == 'C':
            self._stored = 0.0

        return self._stored
