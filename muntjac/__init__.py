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

"""<p>The Vaadin base package. Contains the Application class, the
starting point of any application that uses Vaadin.</p>

<p>Contains all Vaadin core classes. A Vaadin application is based
on the L{com.vaadin.Application} class and deployed as a servlet
using L{com.vaadin.terminal.gwt.server.ApplicationServlet} or
L{com.vaadin.terminal.gwt.server.GAEApplicationServlet} (for Google
App Engine).</p>

<p>Vaadin applications can also be deployed as portlets using {@link
com.vaadin.terminal.gwt.server.ApplicationPortlet} (JSR-168) or {@link
com.vaadin.terminal.gwt.server.ApplicationPortlet2} (JSR-286).</p>

<p>All classes in Vaadin are serializable unless otherwise noted.
This allows Vaadin applications to run in cluster and cloud
environments.</p>
"""
