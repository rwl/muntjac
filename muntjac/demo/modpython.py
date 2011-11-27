
"""Apache virtual host example using mod_python and paste.modpython.

<VirtualHost *:80>

    <Location /hello>
        SetHandler python-program
        PythonHandler paste.modpython
        PythonPath "['/path/to/muntjac'] + sys.path"
        PythonOption wsgi.application muntjac.demo.modpython::hello_app
        PythonOption SCRIPT_NAME /hello
    </Location>

    Alias /VAADIN "/path/to/VAADIN"
    <Location "/VAADIN">
        SetHandler None
    </Location>

</VirtualHost>
"""

from paste.session import SessionMiddleware
from muntjac.demo.util import MuntjacFileSession

from muntjac.demo.main import hello, calc, address, tunes, sampler


hello_app = SessionMiddleware(hello, session_class=MuntjacFileSession)

calc_app = SessionMiddleware(calc, session_class=MuntjacFileSession)

address_app = SessionMiddleware(address, session_class=MuntjacFileSession)

tunes_app = SessionMiddleware(tunes, session_class=MuntjacFileSession)

sampler_app = SessionMiddleware(sampler, session_class=MuntjacFileSession)
