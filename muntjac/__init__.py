# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""The Muntjac base package. Contains the Application class, the
starting point of any application that uses Muntjac.

Contains all Muntjac core classes. A Muntjac application is based
on the L{Application} class and deployed as a servlet
using L{ApplicationServlet} or L{GaeApplicationServlet}
(for Google App Engine).

All classes in Muntjac are pickleable unless otherwise noted.
This allows Muntjac applications to run in cluster and cloud
environments.
"""
