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


class IDatastore(object):
    """*Wrapper for datastore.

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    def get(self, *args):
        """Gets entities for some criteria.

        Datastore limitations on queries sort orders and filter apply.

        @param query: criteria for the entities
        @param start_index: offset from beginning
        @param amount: amount of entities to get
        @return: as many entities as amount,
        	 * or a partial list if start_index+amount>L{Datastore.size}
        	 * or null if L{Datastore.size} was less than start_index
        ---
        Gets and entity.

        @param key: key of the entity
        @return: the entity with key or null
        """
        raise NotImplementedError


    def put(self, entity, versioned):
        """Puts both new and in the datastore existing entities.

        Note if its new or existing entity is decided depending on if the key
        is complete or not.

        @param entity: entity to be saved
        @param versioned: true if the update should consider versioning
        @return: the same entity now with a complete key or null if failed
        @raise ConcurrentModificationException: if versioned was true and the
        entity was concurrently updated
        @raise NoSuchElementException: if versioned was true and the entity
        was concurrently updated
        """
        raise NotImplementedError


    def delete(self, key):
        """Deletes an entity.

        @param key: key of the entity
        @raise ValueError: if the specified key was invalid
        @raise ConcurrentModificationException: if the entity was modified
        concurently
        @raise DatastoreFailureException: general datastore failure
        """
        raise NotImplementedError


    def size(self, query):
        """Gets the amount of entities of a given kind currently present in
        the datastore.

        @param query: sort and filter representation for desired entities
        @return: number of entities in the datastore
        """
        raise NotImplementedError


    def getPreviousKey(self, key, q):
        """Get the key of the entity previous to the key given key.

        @param key: key of the current entity
        @param q: representation of the current sort order
        @return: key of previous entity or null
        @raise NotImplementedError:
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
