# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component import abstract_listener_methods_test

from muntjac.data.util.indexed_container import IndexedContainer

from muntjac.data.container import \
    (IItemSetChangeEvent, IItemSetChangeListener, IPropertySetChangeEvent,
     IPropertySetChangeListener)


class TestAbstractContainerListeners(
            abstract_listener_methods_test.AbstractListenerMethodsTest):

    def testItemSetChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(IndexedContainer,
                IItemSetChangeEvent, IItemSetChangeListener)

    def testPropertySetChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(IndexedContainer,
                IPropertySetChangeEvent, IPropertySetChangeListener)
