
import sys
import logging

from os.path import join, dirname

from wsgiref.simple_server import make_server

import muntjac

from muntjac.demo.util import InMemorySession

from muntjac.terminal.gwt.server.application_servlet import ApplicationServlet

from muntjac.demo.HelloWorld import HelloWorld
from muntjac.demo.Calc import Calc
from muntjac.demo.SimpleAddressBook import SimpleAddressBook
from muntjac.demo.MuntjacTunesLayout import MuntjacTunesLayout
from muntjac.demo.sampler.SamplerApplication import SamplerApplication

from paste.urlmap import URLMap
from paste.session import SessionMiddleware
from paste.fileapp import DirectoryApp


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

ws_app = DirectoryApp(join(dirname(muntjac.__file__), 'public', 'VAADIN'))
urlmap['/VAADIN'] = ws_app


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    url_map = SessionMiddleware(urlmap, session_class=InMemorySession)

    print 'Serving on port: 8080'
    make_server('localhost', 8080, url_map).serve_forever()


if __name__ == '__main__':
    ## $ python -m cProfile -o /tmp/demo.prof muntjac/demo/main.py
    #pstats.Stats("/tmp/demo.prof").sort_stats('time').print_stats(20)
    main()
