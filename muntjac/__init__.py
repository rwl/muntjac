# Copyright (C) 2011 Vaadin Ltd.
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
