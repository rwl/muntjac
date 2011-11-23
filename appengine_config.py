
"""Appstats configuration."""

from gaesessions import SessionMiddleware


COOKIE_KEY = '@COOKIE_KEY@'

if COOKIE_KEY == '@' + 'COOKIE_KEY' + '@':
    COOKIE_KEY = 'generate a random key OFFLINE and paste to COOKIE_KEY'


def webapp_add_wsgi_middleware(app):
    """WSGI middleware declaration."""
    from google.appengine.ext.appstats import recording
    app = SessionMiddleware(app, cookie_key=COOKIE_KEY)
    app = recording.appstats_wsgi_middleware(app)
    return app
