# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

import os
import sys
import locale

import paste.webkit

from babel.core import Locale, UnknownLocaleError


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


class EventObject(object):

    def __init__(self, source):
        self._source = source


    def getSource(self):
        return self._source


class IEventListener(object):
    pass