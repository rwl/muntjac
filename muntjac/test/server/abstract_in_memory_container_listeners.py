# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.data.util.indexed_container import IndexedContainer
from muntjac.data.container import IItemSetChangeEvent, IItemSetChangeListener


class TestAbstractInMemoryContainerListeners(AbstractListenerMethodsTest):

    def testItemSetChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(IndexedContainer,
                IItemSetChangeEvent, IItemSetChangeListener)
