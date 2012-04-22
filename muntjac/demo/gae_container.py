
from muntjac.data.util.gaecontainer.impl.cache.factory.local_memory_cache_config import RemoveStrategy, Builder as LocalMemoryCacheConfigBuilder
from muntjac.data.util.gaecontainer.impl.cache.factory.mem_cache_config import Builder as MemCacheConfigBuilder
from muntjac.data.util.gaecontainer.impl.gae_container import GAEContainer
from muntjac.data.util.gaecontainer.impl.cache.factory.cache_factory import CacheFactory

from muntjac.application import Application
from muntjac.ui.table import Table
from muntjac.ui.window import Window


#localMemoryCacheConfig = LocalMemoryCacheConfigBuilder()\
#    .withCacheFilteredIndexes(True)\
#    .withCacheFilteredSizes(True)\
#    .withIndexCapacity(50)\
#    .withIndexLifeTime(60)\
#    .withItemCapacity(500)\
#    .withItemLifeTime(60)\
#    .withLineSize(25)\
#    .withRemoveStrategy(RemoveStrategy.LRU)\
#    .withSizeCapacity(10)\
#    .withSizeLifeTime(60).Build()
#
#memCacheConfig = MemCacheConfigBuilder()\
#    .withCacheFilteredIndexes(True)\
#    .withIndexLifeTime(500)\
#    .withItemLifeTime(500)\
#    .withLineSize(50).Build()

# create the GAEContainer with the caches and property write trough and
# no optimistic locking
addressBookData = GAEContainer("People", True, False,
#        CacheFactory.getCache(localMemoryCacheConfig),
#        CacheFactory.getCache(memCacheConfig)
)

class GAEContainerApplication(Application):

    def init(self):
        self.setMainWindow(Window("GAE Container"))
        contactList = Table()
        contactList.setContainerDataSource(addressBookData)
#        contactList.setVisibleColumns(visibleCols)
        contactList.setSelectable(True)
        self.getMainWindow().getContainer().addComponent(contactList)


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(GAEContainerApplication, debug=True)
