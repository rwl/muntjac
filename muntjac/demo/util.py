
import os

try:
    import cPickle as pickle
except ImportError:
    import pickle

import paste.session


class MuntjacFileSession(paste.session.FileSession):
    """Overridden to specify pickle protocol."""

    def close(self):
        if self._data is not None:
            filename = self.filename()
            exists = os.path.exists(filename)
            if not self._data:
                if exists:
                    os.unlink(filename)
            else:
                f = open(filename, 'wb')
                # select the highest protocol version supported
                pickle.dump(self._data, f, -1)
                f.close()
                if not exists and self.chmod:
                    os.chmod(filename, self.chmod)


_SESSION_CACHE = {}

class InMemorySession(object):

    def __init__(self, sid, create=False, expiration=2880):
        """
        @param expiration:
            The time each session lives on disk.  Old sessions are
            culled from disk based on this.  Default 48 hours.
        """
        self.sid = sid
        if not sid:
            raise KeyError
        if not create:
            if sid not in _SESSION_CACHE:
                raise KeyError
        self._data = None
        self.expiration = expiration


    def data(self):
        if self._data is not None:
            return self._data
        self._data = _SESSION_CACHE.get(self.sid, {})
        return self._data


    def close(self):
        if self._data is not None:
            _SESSION_CACHE[self.sid] = self._data


    def clean_up(self):
        return
