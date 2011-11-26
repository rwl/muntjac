# Copyright (C) 2011 Vaadin Ltd.
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
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

import os
import sys
import locale
import datetime

try:
    import cPickle as pickle
except ImportError:
    import pickle

import paste.webkit

from babel.core import Locale, UnknownLocaleError
from paste.session import FileSession


# Copied from paste.webkit.wsgiapp to avoid paste.deploy dependency.
def sys_path_install():
    webware_dir = os.path.join(os.path.dirname(paste.webkit.__file__),
                               'FakeWebware')
    if webware_dir not in sys.path:
        sys.path.append(webware_dir)


def loadClass(className):
    return (lambda x: getattr(__import__(x.rsplit('.', 1)[0],
                                         fromlist=x.rsplit('.', 1)[0]),
                              x.split('.')[-1]))(className)


def getSuperClass(cls):
    return cls.__mro__[1] if len(cls.__mro__) > 1 else None


def clsname(cls):
    """@return: fully qualified name of given class"""
    return cls.__module__ + "." + cls.__name__


def fullname(obj):
    """@return: fully qualified name of given object's class"""
    return clsname(obj.__class__)


def totalseconds(td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1e6) / 1e6


def defaultLocale():
    try:
        lang, _ = locale.getdefaultlocale()
    except Exception:
        lang = None

    if lang is not None:
        try:
            return Locale.parse(lang)
        except UnknownLocaleError:
            pass
    else:
        try:
            return Locale.default()
        except UnknownLocaleError:
            return Locale('en', 'US')


class MuntjacFileSession(FileSession):
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


class EventObject(object):

    def __init__(self, source):
        self._source = source


    def getSource(self):
        return self._source


class IEventListener(object):
    pass