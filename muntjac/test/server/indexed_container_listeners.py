# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.data.util.indexed_container import IndexedContainer
from muntjac.data.property import ValueChangeEvent, IValueChangeListener

from muntjac.test.server.component import abstract_listener_methods_test

from muntjac.data.container import \
    IPropertySetChangeEvent, IPropertySetChangeListener


class IndexedContainerListeners(
            abstract_listener_methods_test.AbstractListenerMethodsTest):

    def testValueChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(IndexedContainer,
                ValueChangeEvent, IValueChangeListener)

    def testPropertySetChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(IndexedContainer,
                IPropertySetChangeEvent, IPropertySetChangeListener)
