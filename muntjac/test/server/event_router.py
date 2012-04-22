# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from unittest import TestCase
from muntjac.ui.text_field import TextField
from muntjac.data.property import IValueChangeListener


class TestEventRouter(TestCase):

    def setUp(self):
        TestCase.setUp(self)

        self._innerListenerCalls = 0


    def testAddInEventListener(self):
        tf = TextField()

        class Outer(IValueChangeListener):

            def __init__(self, test, tf):
                self._test = test
                self._tf = tf

            def valueChange(self, event):

                class Inner(IValueChangeListener):

                    def __init__(self, test):
                        self._test = test

                    def valueChange(self, event):
                        self._test._innerListenerCalls += 1
                        print 'The inner listener was called'

                self._tf.addListener(Inner(self._test), IValueChangeListener)

        tf.addListener(Outer(self, tf), IValueChangeListener)
        tf.setValue('abc')  # No inner listener calls, adds one inner
        tf.setValue('def')  # One inner listener call, adds one inner
        tf.setValue('ghi')  # Two inner listener calls, adds one inner

        self.assertEqual(self._innerListenerCalls, 3)
