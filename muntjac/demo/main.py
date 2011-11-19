
import sys
import logging

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
from paste.session import SessionMiddleware
from paste.fileapp import DirectoryApp


helloServlet = ApplicationServlet(HelloWorld)
hello = SessionMiddleware(helloServlet)

calcServlet = ApplicationServlet(Calc)
calc = SessionMiddleware(calcServlet)

addressServlet = ApplicationServlet(SimpleAddressBook)
address = SessionMiddleware(addressServlet)

tunesServlet = ApplicationServlet(MuntjacTunesLayout)
tunes = SessionMiddleware(tunesServlet)

samplerServlet = ApplicationServlet(SamplerApplication,
        widgetset='com.vaadin.demo.sampler.gwt.SamplerWidgetSet')
sampler = SessionMiddleware(samplerServlet)

urlmap = URLMap({})
urlmap['/hello'] = hello
urlmap['/calc'] = calc
urlmap['/address'] = address
urlmap['/tunes'] = tunes
urlmap['/sampler'] = sampler


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    wsapp = DirectoryApp(join(dirname(muntjac.__file__), 'public', 'VAADIN'))
    urlmap['/VAADIN'] = wsapp

    make_server('localhost', 8080, urlmap).serve_forever()
