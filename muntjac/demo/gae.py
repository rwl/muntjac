
from muntjac.demo.Calc import Calc

from google.appengine.ext.webapp.util import run_wsgi_app

from muntjac.terminal.gwt.server.gae_application_servlet import \
    GaeApplicationServlet

from gaesessions import SessionMiddleware, get_current_session


class GaeSessionMiddleware(SessionMiddleware):

    def __call__(self, environ, start_response):

        environ['paste.session.factory'] = get_current_session

        return super(GaeSessionMiddleware, self).__call__(environ,
                start_response)


calc_servlet = GaeApplicationServlet(Calc, debug=True)

calc_app = GaeSessionMiddleware(calc_servlet,
        cookie_key=GaeApplicationServlet.SID)


def main():
    run_wsgi_app(calc_app)

if __name__ == "__main__":
    main()
