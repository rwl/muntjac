

from muntjac.terminal.gwt.server.application_servlet import ApplicationServlet

from muntjac.demo.HelloWorld import HelloWorld
from muntjac.demo.Calc import Calc
from muntjac.demo.SimpleAddressBook import SimpleAddressBook
from muntjac.demo.MuntjacTunesLayout import MuntjacTunesLayout
from muntjac.demo.sampler.SamplerApplication import SamplerApplication

from paste.urlmap import URLMap

from paste.session import SessionMiddleware


hello = ApplicationServlet(HelloWorld)
hello = SessionMiddleware(hello)

calc = ApplicationServlet(Calc)
calc = SessionMiddleware(calc)

address = ApplicationServlet(SimpleAddressBook)
address = SessionMiddleware(address)

tunes = ApplicationServlet(MuntjacTunesLayout)
tunes = SessionMiddleware(tunes)

sampler = ApplicationServlet(SamplerApplication,
        widgetset='com.vaadin.demo.sampler.gwt.SamplerWidgetSet')
sampler = SessionMiddleware(sampler)

app = URLMap({})
app['/hello'] = hello
app['/calc'] = calc
app['/address'] = address
app['/tunes'] = tunes
app['/sampler'] = sampler
