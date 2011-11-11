# Copyright (C) 2010 IT Mill Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import logging
import webbrowser

#from os.path import join, dirname
#import static
#from paste.urlmap import URLMap

from optparse import OptionParser

from wsgiref.simple_server import make_server

from paste.session import SessionMiddleware

from muntjac.terminal.gwt.server.application_servlet import ApplicationServlet

from muntjac.demo.HelloWorld import HelloWorld
from muntjac.demo.Calc import Calc
from muntjac.demo.SimpleAddressBook import SimpleAddressBook
from muntjac.demo.MuntjacTunesLayout import MuntjacTunesLayout


def muntjac(applicationClass, host='localhost', port=8880, nogui=False,
            debug=False, serve=True, forever=True, *args, **kw_args):

    level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(stream=sys.stdout, level=level,
            format='%(levelname)s: %(message)s')

    wsgi_app = ApplicationServlet(applicationClass, debug=debug,
            *args, **kw_args)

    wsgi_app = SessionMiddleware(wsgi_app)  # wrap in middleware

#    root = join(dirname(__file__), '..', 'VAADIN')
#
#    urlmap = URLMap({})
#    urlmap['/'] = wsgi_app
#    urlmap['/VAADIN'] = static.Cling(root)

    url = 'http://%s:%d/' % (host, port)

    if nogui == False:
        webbrowser.open(url, new=0)

    httpd = make_server(host, port, wsgi_app)

    if serve:
        print 'Serving at: %s' % url
        if forever:
            # Respond to requests until process is killed
            httpd.serve_forever()
        else:
            # Serve one request, then exit
            httpd.handle_request()


def main(args=sys.argv[1:]):

    parser = OptionParser(usage='usage: muntjac [options]',
        version='Muntjac Version %s' % '@VERSION@')

    parser.add_option('-t', '--test', action='store_true',
        help='run tests and exit')

    parser.add_option('--host', default='localhost', type='string',
        help='WSGI server hostname')

    parser.add_option('--port', default=8080, type='int',
        help='WSGI server port number')

    parser.add_option('--nogui', action='store_true',
        help='do not open browser window')

    parser.add_option('--debug', action='store_true',
        help='run in debug mode')


    opts, args = parser.parse_args(args)

    if len(args) > 0:
        sys.stderr.write('Too many arguments')
        parser.print_help()
        sys.exit(2)


    if opts.test:
        pass
    else:
        host, port, nogui, debug = opts.host, opts.port, opts.nogui, opts.debug

        muntjac(HelloWorld, host, port, nogui, debug,
                widgetset='com.vaadin.demo.gwt.HelloWorldWidgetSet')

        muntjac(Calc, host, port, nogui, debug,
                widgetset='com.vaadin.demo.gwt.CalcWidgetSet')

        muntjac(SimpleAddressBook, host, port, nogui, debug)

        muntjac(MuntjacTunesLayout, host, port, nogui, debug)


if __name__ == '__main__':
    main()
