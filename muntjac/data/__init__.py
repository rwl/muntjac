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

"""<p>Contains interfaces for the data layer, mainly for binding typed
data and data collections to components, and for validating data.</p>

<h2>Data binding</h2>

<p>The package contains a three-tiered structure for typed data
objects and collections of them:</p>

<ul>
    <li>A {@link com.vaadin.data.Property Property} represents a
    single, typed data value.

    <li>An {@link com.vaadin.data.Item Item} embodies a set of <i>Properties</i>.
    A locally unique (inside the {@link com.vaadin.data.Item Item})
    Property identifier corresponds to each Property inside the Item.</li>
    <li>A {@link com.vaadin.data.Container Container} contains a set
    of Items, each corresponding to a locally unique Item identifier. Note
    that Container imposes a few restrictions on the data stored in it, see
    {@link com.vaadin.data.Container Container} for further information.</li>
</ul>

<p>For more information on the data model, see the <a
    href="http://vaadin.com/book/-/page/datamodel.html">Data model
chapter</a> in Book of Vaadin.</p>

<h2>Buffering</h2>

<p>A {@link com.vaadin.data.Buffered Buffered} implementor is able
to track and buffer changes and commit or discard them later.</p>

<h2>Validation</h2>

<p>{@link com.vaadin.data.Validator Validator} implementations are
used to validate data, typically the value of a {@link
com.vaadin.ui.Field Field}. One or more {@link com.vaadin.data.Validator
Validators} can be added to a {@link com.vaadin.data.Validatable
Validatable} implementor and then used to validate the value of the
Validatable. </p>"""