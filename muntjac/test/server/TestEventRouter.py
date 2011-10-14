# -*- coding: utf-8 -*-
# from com.vaadin.ui.TextField import (TextField,)
# from junit.framework.TestCase import (TestCase,)


class TestEventRouter(TestCase):
    _innerListenerCalls = 0

    def testAddInEventListener(self):
        tf = TextField()

        class outer(ValueChangeListener):

            def valueChange(self, event):

                class inner(ValueChangeListener):

                    def valueChange(self, event):
                        TestEventRouter_this._innerListenerCalls += 1
                        print 'The inner listener was called'

                self.tf.addListener(inner)

        tf.addListener(outer)
        tf.setValue('abc')
        # No inner listener calls, adds one inner
        tf.setValue('def')
        # One inner listener call, adds one inner
        tf.setValue('ghi')
        # Two inner listener calls, adds one inner
        assert self._innerListenerCalls == 3
