# -*- coding: utf-8 -*-
# from com.vaadin.ui.Button.ClickListener import (ClickListener,)
# from com.vaadin.ui.GridLayout import (GridLayout,)


class Calc(Application, ClickListener):
    """A simple calculator using Vaadin."""
    # All variables are automatically stored in the session.
    _current = 0.0
    _stored = 0.0
    _lastOperationRequested = 'C'
    # User interface components
    _display = Label('0.0')
    # Application.init is called once for each application. Here it creates the
    # UI and connects it to the business logic.

    def init(self):
        # Create the main layout for our application (4 columns, 5 rows)
        # Event handler for button clicks. Called for all the buttons in the
        # application.
        layout = GridLayout(4, 5)
        # Create the main window for the application using the main layout. The
        # main window is shown when the application is starts.

        self.setMainWindow(Window('Calculator Application', layout))
        # Create a result label that over all 4 columns in the first row
        layout.addComponent(self._display, 0, 0, 3, 0)
        # The operations for the calculator in the order they appear on the
        # screen (left to right, top to bottom)
        operations = ['7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-', '0', '=', 'C', '+']
        for caption in operations:
            # Create a button and use this application for event handling
            button = Button(caption)
            button.addListener(self)
            # Add the button to our main layout
            layout.addComponent(button)

    def buttonClick(self, event):
        # Get the button that was clicked
        # Calculator "business logic" implemented here to keep the example minimal
        button = event.getButton()
        # Get the requested operation from the button caption
        requestedOperation = button.getCaption()[0]
        # Calculate the new value
        newValue = self.calculate(requestedOperation)
        # Update the result label with the new value
        self._display.setValue(newValue)

    def calculate(self, requestedOperation):
        if '0' <= requestedOperation and requestedOperation <= '9':
            self._current = (self._current * 10) + Double.parseDouble.parseDouble('' + requestedOperation)
            return self._current
        _0 = self._lastOperationRequested
        _1 = False
        while True:
            if _0 == '+':
                _1 = True
                self._stored += self._current
                break
            if (_1 is True) or (_0 == '-'):
                _1 = True
                self._stored -= self._current
                break
            if (_1 is True) or (_0 == '/'):
                _1 = True
                self._stored /= self._current
                break
            if (_1 is True) or (_0 == '*'):
                _1 = True
                self._stored *= self._current
                break
            if (_1 is True) or (_0 == 'C'):
                _1 = True
                self._stored = self._current
                break
            break
        self._lastOperationRequested = requestedOperation
        self._current = 0.0
        if requestedOperation == 'C':
            self._stored = 0.0
        return self._stored
