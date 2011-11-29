# Copyright (C) 2010 Abo Akademi University
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Note: This is a modified file from GAEContainer. For further information
#       please visit http://vaadin.com/directory#addon/gaecontainer.

from __pyjamas__ import (ARGERROR, POSTINC, PREDEC,)
from muntjac.data.util.gaecontainer.Datastore import (Datastore,)
# from com.google.appengine.api.datastore.Cursor import (Cursor,)
# from com.google.appengine.api.datastore.DatastoreFailureException import (DatastoreFailureException,)
# from com.google.appengine.api.datastore.DatastoreService import (DatastoreService,)
# from com.google.appengine.api.datastore.DatastoreServiceFactory import (DatastoreServiceFactory,)
# from com.google.appengine.api.datastore.Entity import (Entity,)
# from com.google.appengine.api.datastore.EntityNotFoundException import (EntityNotFoundException,)
# from com.google.appengine.api.datastore.FetchOptions import (FetchOptions,)
# from com.google.appengine.api.datastore.FetchOptions.Builder import (Builder,)
# from com.google.appengine.api.datastore.Key import (Key,)
# from com.google.appengine.api.datastore.KeyFactory import (KeyFactory,)
# from com.google.appengine.api.datastore.PreparedQuery import (PreparedQuery,)
# from com.google.appengine.api.datastore.Query import (Query,)
# from com.google.appengine.api.datastore.Query.FilterOperator import (FilterOperator,)
# from com.google.appengine.api.datastore.Query.SortDirection import (SortDirection,)
# from com.google.appengine.api.datastore.Query.SortPredicate import (SortPredicate,)
# from com.google.appengine.api.datastore.QueryResultList import (QueryResultList,)
# from com.google.appengine.api.datastore.Transaction import (Transaction,)
# from java.util.ConcurrentModificationException import (ConcurrentModificationException,)
# from java.util.LinkedList import (LinkedList,)
# from java.util.List import (List,)
# from java.util.NoSuchElementException import (NoSuchElementException,)
# from java.util.logging.Logger import (Logger,)


class DatastoreImpl(Datastore):
    """Datatore wrapper
    @author: Johan Selanniemi
    @author: Richard Lincoln
    """
    # final Logger log = Logger.getLogger(this.getClass().getName());
    _OFFSET_LIMIT = 1000
    _ds = DatastoreServiceFactory.getDatastoreService()
    # (non-Javadoc)
    # @see muntjac.data.util.gaecontainer.Datastore#get(com.google.appengine.api.datastore.Query, int, int)
    # Since offset is currently limited to 1000 a index of order n-thousand requires n cursors to be fetched

    def get(self, *args):
        # todo investigate .preFetchSize
        # Get cursor by steps of 1000
        # e.g. steps=2 will give cursor for 2000

        _0 = args
        _1 = len(args)
        if _1 == 1:
            key, = _0
            try:
                entity = self._ds.get(key)
                return entity
            except EntityNotFoundException, e:
                return None
        elif _1 == 3:
            query, start_index, amount = _0
            pq = self._ds.prepare(query)
            offset = start_index
            if offset < self._OFFSET_LIMIT:
                # we are under limit to not need cursor
                if offset + amount >= self._OFFSET_LIMIT:
                    amount = amount - (offset + amount) - self._OFFSET_LIMIT
                result = pq.asList(Builder.withLimit(amount).offset(offset).chunkSize(amount))
                return result
            else:
                # need cursor
                steps = start_index / self._OFFSET_LIMIT
                offset = start_index - (steps * self._OFFSET_LIMIT)
                cursor = self.getCursorFor(steps, pq)
                if cursor is not None:
                    result = pq.asList(Builder.withLimit(amount).offset(offset).chunkSize(amount).cursor(cursor))
                    return result
                return None
        else:
            raise ARGERROR(1, 3)

    def getCursorFor(self, steps, pq):
        # (non-Javadoc)
        # @see muntjac.data.util.gaecontainer.Datastore#put(com.google.appengine.api.datastore.Entity, boolean)
        # Determining whether it is a new entity is done by checking the completeness of the key.

        paginator = pq.asQueryResultList(Builder.withLimit(1).chunkSize(1).offset(self._OFFSET_LIMIT - 1))
        cursor = paginator.getCursor()
        while PREDEC(globals(), locals(), 'steps') > 0 and cursor is not None:
            paginator = pq.asQueryResultList(Builder.withLimit(1).chunkSize(1).offset(self._OFFSET_LIMIT - 1).cursor(cursor))
            cursor = paginator.getCursor()
        return cursor

    def put(self, entity, versioned):
        if entity.getKey().isComplete():
            # this is not a new entity
            if versioned:
                return self.doVersionedPut(entity)
            else:
                return self.doNonVersionedPut(entity)
        else:
            # its a new entity
            try:
                entity.setUnindexedProperty('version', 0)
                self._ds.put(entity)
                txn = self._ds.beginTransaction()
                # could also count the db here and create the key entity
                try:
                    sizeEntity = self._ds.get(txn, KeyFactory.createKey('_size', entity.getKind()))
                    sizeEntity.setProperty('size', sizeEntity.getProperty('size') + 1)
                    self._ds.put(sizeEntity)
                except EntityNotFoundException, e:
                    pass # astStmt: [Stmt([]), None]
                txn.commit()
                return entity
            except DatastoreFailureException, e:
                return None

    def doNonVersionedPut(self, entity):
        self._ds.put(entity)
        return entity

    def doVersionedPut(self, entity):
        txn = self._ds.beginTransaction()
        try:
            try:
                dsEntity = self._ds.get(txn, entity.getKey())
            except EntityNotFoundException, e:
                txn.rollback()
                raise NoSuchElementException()
            if dsEntity.getProperty('version') is None:
                # the enitity did not have a version -> add
                dsEntity.setPropertiesFrom(entity)
                dsEntity.setUnindexedProperty('version', 0)
            else:
                version = dsEntity.getProperty('version')
                if entity.getProperty('version') == version:
                    dsEntity.setPropertiesFrom(entity)
                    dsEntity.setUnindexedProperty('version', version + 1)
                else:
                    txn.rollback()
                    raise ConcurrentModificationException('Version numbers did not conform')
            self._ds.put(txn, dsEntity)
            txn.commit()
            return dsEntity
        except DatastoreFailureException, e:
            txn.rollback()
            raise ConcurrentModificationException('Datastore transcation failed')

    def size(self, query):
        if len(query.getFilterPredicates()) != 0:
            return self.getEntityCountFromDB(query).intValue()
        else:
            sizeKey = KeyFactory.createKey('_size', query.getKind())
            # did not exist -> create
            try:
                entity = self._ds.get(sizeKey)
                return entity.getProperty('size').intValue()
            except EntityNotFoundException, e:
                txn = self._ds.beginTransaction()
                try:
                    entity = self._ds.get(txn, sizeKey)
                    txn.rollback()
                    return entity.getProperty('size').intValue()
                except EntityNotFoundException, en:
                    count = self.getEntityCountFromDB(query)
                    entity = Entity(sizeKey)
                    entity.setProperty('size', count)
                    self._ds.put(txn, entity)
                txn.commit()
                return count.intValue()

    def getEntityCountFromDB(self, query):
        query.setKeysOnly()
        fetchOptions = FetchOptions.Builder.withOffset(0)
        preparedQuery = self._ds.prepare(query)
        return len(preparedQuery.asList(fetchOptions))

    def delete(self, key):
        # several fetches needs to be made -> could give erroneous results
        # documentation: Don't ask

        self._ds.delete(key)
        txn = self._ds.beginTransaction()
        # could also count the db here and create the key entity
        try:
            sizeEntity = self._ds.get(txn, KeyFactory.createKey('_size', key.getKind()))
            sizeEntity.setProperty('size', sizeEntity.getProperty('size') - 1)
            self._ds.put(sizeEntity)
        except EntityNotFoundException, e:
            pass # astStmt: [Stmt([]), None]
        txn.commit()

    def doGetAdjacentKey(self, key, q, prev):
        try:
            currentEntity = self._ds.get(key)
        except EntityNotFoundException, e:
            return None
        processedProperties = LinkedList()
        dsQuery = q.getQuery(0, prev)
        i = 0
        while POSTINC(globals(), locals(), 'i') < q.sortQuantity():
            for processedPredicate in processedProperties:
                dsQuery.addFilter(processedPredicate, FilterOperator.EQUAL, currentEntity.getProperty(processedPredicate))
            sortPredicate = dsQuery.getSortPredicates().get(0)
            propertyName = sortPredicate.getPropertyName()
            self.addAdjacentFilters(dsQuery, processedProperties, currentEntity, FilterOperator.GREATER_THAN_OR_EQUAL, FilterOperator.LESS_THAN_OR_EQUAL)
            pq = self._ds.prepare(dsQuery)
            result = pq.asList(Builder.withLimit(2))
            if len(result) == 0:
                raise ConcurrentModificationException('The entity of the given key was either deleted or modified')
            if len(result) == 1:
                if len(processedProperties) == 0:
                    return None
                break
            if propertyName == '__key__':
                # keys are always unique
                return result[1].getKey()
            currentValue = result[0].getProperty(propertyName)
            if (
                currentValue is not None and not (currentValue == result[1].getProperty(propertyName))
            ):
                return result[1].getKey()
            dsQuery = q.getQuery(i, prev)
            processedProperties.add(propertyName)
        dsQuery = q.getQuery(i - 2, prev)
        self.addAdjacentFilters(dsQuery, processedProperties.subList(0, len(processedProperties) - 1), currentEntity, FilterOperator.GREATER_THAN, FilterOperator.LESS_THAN)
        pq = self._ds.prepare(dsQuery)
        result = pq.asList(Builder.withLimit(1))
        if len(result) > 0:
            return result[0].getKey()
        return None

    def getNextKey(self, key, q):
        # *add filters for performing a query for an adjacent key
        # 
        # 	 *q - query to add the filters to
        # 	 *processedProperties - properties that should have equality filters
        # 	 *currentEntitiy - entity we are working on
        # 	 *opt1,opt2 - operators that should be used eg. > or >=

        return self.doGetAdjacentKey(key, q, False)

    def addAdjacentFilters(self, q, processedProperties, currentEntity, opt1, opt2):
        for processedPredicate in processedProperties:
            if currentEntity.getProperty(processedPredicate) is not None:
                q.addFilter(processedPredicate, FilterOperator.EQUAL, currentEntity.getProperty(processedPredicate))
        sortPredicate = q.getSortPredicates().get(0)
        if sortPredicate.getPropertyName() == '__key__':
            value = currentEntity.getKey()
        else:
            value = currentEntity.getProperty(sortPredicate.getPropertyName())
        if value is not None:
            if sortPredicate.getDirection() == SortDirection.ASCENDING:
                q.addFilter(sortPredicate.getPropertyName(), opt1, value)
            else:
                q.addFilter(sortPredicate.getPropertyName(), opt2, value)

    def getPreviousKey(self, key, q):
        return self.doGetAdjacentKey(key, q, True)
