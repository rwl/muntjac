# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

import sys
import logging
import webbrowser

from os.path import join, dirname

from optparse import OptionParser

from wsgiref.simple_server import make_server

from paste.session import SessionMiddleware
from paste.fileapp import DirectoryApp, FileApp

from muntjac.demo.util import InMemorySession

from muntjac.terminal.gwt.server.application_servlet import ApplicationServlet
from muntjac.demo.main import urlmap
from muntjac.test.suite import main as test


def muntjac(application, host='localhost', port=8880, nogui=False,
            debug=False, serve=True, forever=True, servletClass=None,
            *args, **kw_args):

    if servletClass is None:
        servletClass = ApplicationServlet

    level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(stream=sys.stdout, level=level,
            format='%(levelname)s: %(message)s')

    wsgi_app = servletClass(application, debug=debug, *args, **kw_args)

    wsgi_app = SessionMiddleware(wsgi_app, session_class=InMemorySession)

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

    parser = OptionParser(
        usage='usage: muntjac [options]',
        version='Muntjac Version %s' % '1.1.0')

    parser.add_option('-t', '--test', action='store_true',
        help='run tests and exit')

    parser.add_option('--host', default='localhost', type='string',
        help='WSGI server hostname')

    parser.add_option('--port', default=8080, type='int',
        help='WSGI server port number')

    parser.add_option('--nogui', action='store_true', default=False,
        help='do not open browser window')

    parser.add_option('--debug', action='store_true',
        help='run in debug mode')

    parser.add_option('--contextRoot', default='', type='string',
        help='path to VAADIN directory')


    opts, args = parser.parse_args(args)

    level = logging.DEBUG if opts.debug else logging.INFO

    logging.basicConfig(stream=sys.stdout, level=level,
            format='%(levelname)s: %(message)s')

    if opts.test:
        test()
    else:
        nargs = len(args)
        if nargs > 0:
            sys.stderr.write('Too many arguments')
            parser.print_help()
            sys.exit(2)

        rootapp = FileApp(join(dirname(__file__), 'public', 'index.html'))
        cssapp = DirectoryApp(join(dirname(__file__), 'public', 'css'))
        imgapp = DirectoryApp(join(dirname(__file__), 'public', 'img'))

        urlmap['/'] = rootapp
        urlmap['/css'] = cssapp
        urlmap['/img'] = imgapp

        if opts.contextRoot:
            ctxapp = DirectoryApp(join(opts.contextRoot, 'VAADIN'))
            urlmap['/VAADIN'] = ctxapp

        app = SessionMiddleware(urlmap, session_class=InMemorySession)

        url = 'http://%s:%d/' % (opts.host, opts.port)

        if not opts.nogui:
            webbrowser.open(url, new=0)

        print 'Serving at: %s' % url

        httpd = make_server(opts.host, opts.port, app)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print "\nExiting"

    sys.exit(0)


if __name__ == '__main__':
    main()
