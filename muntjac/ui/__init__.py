"""Provides interfaces and classes in Vaadin.

Package Specification
=====================

Interface hierarchy
-------------------

The {@link com.vaadin.ui.Component} interface is the top-level
interface which must be implemented by all user interface components in
Vaadin. It defines the common properties of the components and how the
framework will handle them. Most simple components, such as {@link
com.vaadin.ui.Button}, for example, do not need to implement the
lower-level interfaces described below. Notice that also the classes and
interfaces required by the component event framework are defined in
{@link com.vaadin.ui.Component}.

The next level in the component hierarchy are the classes
implementing the {@link com.vaadin.ui.ComponentContainer} interface. It
adds the capacity to contain other components to {@link
com.vaadin.ui.Component} with a simple API.

The third and last level is the {@link com.vaadin.ui.Layout},
which adds the concept of location to the components contained in a
{@link com.vaadin.ui.ComponentContainer}. It can be used to create
containers which contents can be positioned.

Component class hierarchy
-------------------------

At the top level is {@link com.vaadin.ui.AbstractComponent} which
implements the {@link com.vaadin.ui.Component} interface. As the name
suggests it is abstract, but it does include a default implementation
for all methods defined in <code>Component</code> so that a component is
free to override only those functionalities it needs.

As seen in the picture, <code>AbstractComponent</code> serves as
the superclass for several "real" components, but it also has a some
abstract extensions. {@link com.vaadin.ui.AbstractComponentContainer}
serves as the root class for all components (for example, panels and
windows) who can contain other components. {@link
com.vaadin.ui.AbstractField}, on the other hand, implements several
interfaces to provide a base class for components that are used for data
display and manipulation.
"""

from muntjac.ui.absolute_layout import AbsoluteLayout
from muntjac.ui.accordion import Accordion
from muntjac.ui.alignment import Alignment
from muntjac.ui.button import Button
from muntjac.ui.check_box import CheckBox
from muntjac.ui.combo_box import ComboBox
from muntjac.ui.css_layout import CssLayout
from muntjac.ui.custom_component import CustomComponent
from muntjac.ui.date_field import DateField
from muntjac.ui.embedded import Embedded
from muntjac.ui.expand_layout import ExpandLayout
from muntjac.ui.form_layout import FormLayout
from muntjac.ui.form import Form
from muntjac.ui.grid_layout import GridLayout
from muntjac.ui.horizontal_layout import HorizontalLayout
from muntjac.ui.horizontal_split_panel import HorizontalSplitPanel
from muntjac.ui.html5_file import Html5File
from muntjac.ui.inline_date_field import InlineDateField
from muntjac.ui.label import Label
from muntjac.ui.link import Link
from muntjac.ui.list_select import ListSelect
from muntjac.ui.login_form import LoginForm
from muntjac.ui.menu_bar import MenuBar
from muntjac.ui.native_button import NativeButton
from muntjac.ui.native_select import NativeSelect
from muntjac.ui.option_group import OptionGroup
from muntjac.ui.ordered_layout import OrderedLayout
from muntjac.ui.panel import Panel
from muntjac.ui.password_field import PasswordField
from muntjac.ui.popup_date_field import PopupDateField
from muntjac.ui.popup_view import PopupView
from muntjac.ui.progress_indicator import ProgressIndicator
from muntjac.ui.rich_text_area import RichTextArea
from muntjac.ui.select import Select
from muntjac.ui.slider import Slider
from muntjac.ui.split_panel import SplitPanel
from muntjac.ui.tab_sheet import TabSheet
from muntjac.ui.table import Table
from muntjac.ui.text_area import TextArea
from muntjac.ui.text_field import TextField
from muntjac.ui.tree import Tree
from muntjac.ui.twin_col_select import TwinColSelect
from muntjac.ui.upload import Upload
from muntjac.ui.uri_fragment_utility import UriFragmentUtility
from muntjac.ui.vertical_layout import VerticalLayout
from muntjac.ui.vertical_split_panel import VerticalSplitPanel
from muntjac.ui.window import Window
