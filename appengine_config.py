
"""Appstats configuration."""

from gaesessions import SessionMiddleware, Session, _tls


COOKIE_KEY = '@COOKIE_KEY@'

if COOKIE_KEY == '@' + 'COOKIE_KEY' + '@':
    COOKIE_KEY = 'generate a random key OFFLINE and paste to COOKIE_KEY'

class GaeSessionMiddleware(SessionMiddleware):

    def __call__(self, environ, start_response):
        # initialize a session for the current user
        _tls.current_session = Session(lifetime=self.lifetime, no_datastore=self.no_datastore, cookie_only_threshold=self.cookie_only_thresh, cookie_key=self.cookie_key)

        # create a hook for us to insert a cookie into the response headers
        def my_start_response(status, headers, exc_info=None):
            try:
                _tls.current_session.save() # store the session if it was changed
            except ValueError:  # 1Mb memcache limit
                _tls.current_session.clear()

            for ch in _tls.current_session.make_cookie_headers():
                headers.append(('Set-Cookie', ch))

            return start_response(status, headers, exc_info)

        # let the app do its thing
        return self.app(environ, my_start_response)


def webapp_add_wsgi_middleware(app):
    """WSGI middleware declaration."""
    from google.appengine.ext.appstats import recording
    app = GaeSessionMiddleware(app, cookie_key=COOKIE_KEY)
    app = recording.appstats_wsgi_middleware(app)
    return app
