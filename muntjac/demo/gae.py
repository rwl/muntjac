
import logging

import warnings

from muntjac.demo.HelloWorld \
    import HelloWorld

from muntjac.demo.Calc \
    import Calc

from muntjac.demo.SimpleAddressBook \
    import SimpleAddressBook

from muntjac.demo.MuntjacTunesLayout \
    import MuntjacTunesLayout

from muntjac.demo.sampler.SamplerApplication \
    import SamplerApplication

from muntjac.addon.colorpicker.color_picker_application \
    import ColorPickerApplication

from muntjac.addon.codemirror.code_mirror_application \
    import CodeMirrorApplication

from muntjac.addon.google_maps.google_map_app \
    import GoogleMapWidgetApp

from google.appengine.ext.webapp.util \
    import run_wsgi_app

from paste.urlmap \
    import URLMap

from muntjac.terminal.gwt.server.gae_application_servlet \
    import GaeApplicationServlet


logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

warnings.filterwarnings("ignore", category=DeprecationWarning)


hello = GaeApplicationServlet(HelloWorld)

calc = GaeApplicationServlet(Calc)

address = GaeApplicationServlet(SimpleAddressBook)

tunes = GaeApplicationServlet(MuntjacTunesLayout)

sampler = GaeApplicationServlet(SamplerApplication,
        widgetset='com.vaadin.demo.sampler.gwt.SamplerWidgetSet')

colorpicker = GaeApplicationServlet(ColorPickerApplication)

codemirror = GaeApplicationServlet(CodeMirrorApplication)

googlemaps = GaeApplicationServlet(GoogleMapWidgetApp)


def main():
    urlmap = URLMap({})
    urlmap['/hello'] = hello
    urlmap['/calc'] = calc
    urlmap['/address'] = address
    urlmap['/tunes'] = tunes
    urlmap['/sampler'] = sampler
    urlmap['/colorpicker'] = colorpicker
    urlmap['/codemirror'] = codemirror
    urlmap['/googlemaps'] = googlemaps

    run_wsgi_app(urlmap)


if __name__ == "__main__":
    main()
