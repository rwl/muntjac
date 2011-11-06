
import warnings

from muntjac.demo.HelloWorld import HelloWorld
from muntjac.demo.Calc import Calc
from muntjac.demo.SimpleAddressBook import SimpleAddressBook
from muntjac.demo.MuntjacTunesLayout import MuntjacTunesLayout
from muntjac.demo.sampler.SamplerApplication import SamplerApplication

from google.appengine.ext.webapp.util import run_wsgi_app

from paste.urlmap import URLMap

from muntjac.terminal.gwt.server.gae_application_servlet import \
    GaeApplicationServlet

from gaesessions import SessionMiddleware


warnings.filterwarnings("ignore", category=DeprecationWarning)


def main():
    hello = GaeApplicationServlet(HelloWorld)
    hello = SessionMiddleware(hello, '0ce25d8fb6eb44f2c442d1f4fa4ff4a5')

    calc = GaeApplicationServlet(Calc)
    calc = SessionMiddleware(calc, 'ce25c4ad8fb6eb44f42d1f4f24ff4a5e')

    address = GaeApplicationServlet(SimpleAddressBook)
    address = SessionMiddleware(address, 'e25c48fb6eb44f242d1f4fad4ff4a5e0')

    tunes = GaeApplicationServlet(MuntjacTunesLayout)
    tunes = SessionMiddleware(tunes, '25c4428fb6eb44f2d1f4fad4ff4a5e0d')

    sampler = GaeApplicationServlet(SamplerApplication,
            widgetset='com.vaadin.demo.sampler.gwt.SamplerWidgetSet')
    sampler = SessionMiddleware(sampler, '5c442d16eb44f24fff4fad8fb4a5e0df')

    urlmap = URLMap({})
    urlmap['/hello'] = hello
    urlmap['/calc'] = calc
    urlmap['/address'] = address
    urlmap['/tunes'] = tunes
    urlmap['/sampler'] = sampler

    run_wsgi_app(urlmap)


if __name__ == "__main__":
    main()
