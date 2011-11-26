
import os
import sys
import logging

try:
    import cPickle as pickle
except ImportError:
    import pickle

from os.path import join, dirname

from wsgiref.simple_server import make_server

import muntjac

from muntjac.terminal.gwt.server.application_servlet import ApplicationServlet

from muntjac.demo.HelloWorld import HelloWorld
from muntjac.demo.Calc import Calc
from muntjac.demo.SimpleAddressBook import SimpleAddressBook
from muntjac.demo.MuntjacTunesLayout import MuntjacTunesLayout
from muntjac.demo.sampler.SamplerApplication import SamplerApplication

from paste.urlmap import URLMap
from paste.session import SessionMiddleware, FileSession
from paste.fileapp import DirectoryApp


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


hello = ApplicationServlet(HelloWorld)

calc = ApplicationServlet(Calc)

address = ApplicationServlet(SimpleAddressBook)

tunes = ApplicationServlet(MuntjacTunesLayout)

sampler = ApplicationServlet(SamplerApplication,
        widgetset='com.vaadin.demo.sampler.gwt.SamplerWidgetSet')

urlmap = URLMap({})
urlmap['/hello'] = hello
urlmap['/calc'] = calc
urlmap['/address'] = address
urlmap['/tunes'] = tunes
urlmap['/sampler'] = sampler


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    wsapp = DirectoryApp(join(dirname(muntjac.__file__), '..', 'VAADIN'))
    urlmap['/VAADIN'] = wsapp

    url_map = SessionMiddleware(urlmap, session_class=MuntjacFileSession)

    make_server('localhost', 8080, url_map).serve_forever()


if __name__ == '__main__':
    main()
