
#from muntjac.demo.Calc import Calc as App
from muntjac.demo.sampler.SamplerApplication import SamplerApplication as App

from google.appengine.ext.webapp.util import run_wsgi_app

from muntjac.terminal.gwt.server.gae_application_servlet import \
    GaeApplicationServlet

from gaesessions import SessionMiddleware


servlet = GaeApplicationServlet(App, debug=True,
        widgetset='com.vaadin.demo.sampler.gwt.SamplerWidgetSet')

app = SessionMiddleware(servlet,
        cookie_key=GaeApplicationServlet.SID,
        cookie_only_threshold=0)


def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
