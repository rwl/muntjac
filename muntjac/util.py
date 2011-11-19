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

import os
import sys
import locale

import paste.webkit

from babel import Locale


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
        return Locale.parse(lang)
    else:
        return Locale.default()


class EventObject(object):

    def __init__(self, source):
        self._source = source


    def getSource(self):
        return self._source


class IEventListener(object):
    pass