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


class IDataProvider(object):
    """Base interface for data providers.

    The task of the data provider is to supply the container with data by
    using at least a L{Datastore} implementation.

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    def addEntity(self, entity):
        """Adds a new entity.

        @param entity: entity to be added
        @return: they complete key of the entity or null if failed
        """
        raise NotImplementedError


    def containsEntity(self, key):
        """Checks if a entity exists.

        @param key: the key of the entity
        @return: true if existed otherwise false
        """
        raise NotImplementedError


    def getEntity(self, key):
        """Gets an entity.

        @param key: key of the entity
        @return: entity or null if did not exist
        """
        raise NotImplementedError


    def removeEntity(self, key):
        """Removes an entity.

        @param key: key of the entity
        @return: true if succeeded
        """
        raise NotImplementedError


    def size(self, query):
        """Gets the amount of entities in the datastore for a given kind
        and filter order.

        @param query: desired kind and filter combination
        @return: amount of entities
        """
        raise NotImplementedError


    def getKeyByIndexFromStart(self, query, index):
        """Given a query representation fetch element of index index starting
        from beginning.

        @param query: the query representing the current sort order
        @param index: offset from the first entity
        @return: the key corresponding to the index or null if it did not exist
        """
        raise NotImplementedError


    def getKeyByIndexFromEnd(self, query, index):
        """Given a query representation fetch element of index index starting
        from end.

        In other words index=0  will get the last element.

        @param query: the query representing the current sort order
        @param index: offset from the last entity
        @return: the key corresponding to the index or null if it did not exist
        """
        raise NotImplementedError


    def getKeys(self, kind):
        """Gets all entities of a kind.

        @param kind: kind of the entities
        @return: all entities of kind
        @raise NotImplementedError:
        """
        raise NotImplementedError


    def updateEntity(self, entity, versioned):
        """Updates an existing entity.

        The entity must contain a complete key.

        @param entity: entity to be updated
        @param versioned: true if the update should consider versioning
        @raise ConcurrentModificationException: if versioned was true and the
        entity was concurrently updated
        @raise NoSuchElementException: if versioned was true and the entity
        was removed concurrently
        """
        raise NotImplementedError


    def updateProperty(self, entity, versioned):
        """Same as L{updateEntity} but should be used when updating an entity
        that dosen't have all its properties set.

        @param entity:
        @param versioned:
        @raise ConcurrentModificationException:
        @raise NoSuchElementException:
        """
        raise NotImplementedError


    def getPreviousKey(self, key, q):
        """Get the key of the entity previous to the key given key.

        @param key: key of the current entity
        @param q: representation of the current sort order
        @return key: of previous entity or null
        @raise UnsupportedOperationException:
        """
        raise NotImplementedError


    def getNextKey(self, key, q):
        """*Get the key of the entity next from the key given key.

        @param key: key of the current entity
        @param q: representation of the current sort order
        @return: key of next entity or null
        @raise NotImplementedError:
        """
        raise NotImplementedError
