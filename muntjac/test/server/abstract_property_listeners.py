# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.data.util.abstract_property import AbstractProperty

from muntjac.data.property import \
    ValueChangeEvent, IValueChangeListener, IReadOnlyStatusChangeEvent, \
    IReadOnlyStatusChangeListener

from muntjac.data.util.object_property import ObjectProperty

from muntjac.test.server.component import abstract_listener_methods_test


class TestAbstractPropertyListeners(
            abstract_listener_methods_test.AbstractListenerMethodsTest):

    def testValueChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(AbstractProperty,
                ValueChangeEvent, IValueChangeListener, ObjectProperty(''))


    def testReadOnlyStatusChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(AbstractProperty,
                IReadOnlyStatusChangeEvent, IReadOnlyStatusChangeListener,
                ObjectProperty(''))
