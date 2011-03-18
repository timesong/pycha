# Copyright(c) 2007-2010 by Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com>
#
# This file is part of Chavier.
#
# Chavier is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Chavier is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Chavier.  If not, see <http://www.gnu.org/licenses/>.

import pygtk
pygtk.require('2.0')
import gtk

from chavier.dialogs import (
    TextInputDialog, PointDialog, OptionDialog, RandomGeneratorDialog,
    AboutDialog, warning,
    )


class GUI(object):

    def __init__(self, app):
        self.app = app

        self.chart = None
        self.surface = None

        self.main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.main_window.connect('delete_event', self.delete_event)
        self.main_window.connect('destroy', self.destroy)
        self.main_window.set_default_size(640, 480)
        self.main_window.set_title(u'Chavier')

        vbox = gtk.VBox()
        self.main_window.add(vbox)
        vbox.show()

        menubar, toolbar = self._create_ui_manager()

        vbox.pack_start(menubar, False, False)
        menubar.show()

        vbox.pack_start(toolbar, False, False)
        toolbar.show()

        hpaned = gtk.HPaned()
        vbox.pack_start(hpaned, True, True)
        hpaned.show()

        vpaned = gtk.VPaned()
        hpaned.add1(vpaned)
        vpaned.show()

        block1 = self._create_sidebar_block(u'Data sets',
                                            self._datasets_notebook_creator)
        self._create_dataset("Dataset 1")
        block1.set_size_request(-1, 200)

        vpaned.add1(block1)
        block1.show()

        block2 = self._create_sidebar_block(u'Options',
                                            self._options_treeview_creator)
        vpaned.add2(block2)
        block2.show()

        self.drawing_area = gtk.DrawingArea()
        self.drawing_area.connect('expose_event',
                                  self.drawing_area_expose_event)
        self.drawing_area.connect('size_allocate',
                                  self.drawing_area_size_allocate_event)
        hpaned.add2(self.drawing_area)
        self.drawing_area.show()

        self.main_window.show()

    def _create_ui_manager(self):
        self.uimanager = gtk.UIManager()
        accel_group = self.uimanager.get_accel_group()
        self.main_window.add_accel_group(accel_group)

        action_group = gtk.ActionGroup('default')
        action_group.add_actions([
                ('file', None, '_File', None, 'File', None),
                ('quit', gtk.STOCK_QUIT, None, None, 'Quit the program',
                 self.quit),

                ('edit', None, '_Edit', None, 'Edit', None),
                ('add_dataset', gtk.STOCK_ADD, '_Add dataset',
                 '<ctrl><alt>plus', 'Add another dataset', self.add_dataset),
                ('remove_dataset', gtk.STOCK_REMOVE, '_Remove dataset',
                 '<ctrl><alt>minus', 'Remove the current dataset',
                 self.remove_dataset),
                ('edit_dataset', gtk.STOCK_EDIT, '_Edit dataset name',
                 '<ctrl><alt>e', 'Edit the name of the current dataset',
                 self.edit_dataset),
                ('add_point', gtk.STOCK_ADD, 'Add _point', '<ctrl>plus',
                 'Add another point to the current dataset', self.add_point),
                ('remove_point', gtk.STOCK_REMOVE, 'Remove p_oint',
                 '<ctrl>minus',
                 'Remove the current point of the current dataset',
                 self.remove_point),
                ('edit_point', gtk.STOCK_EDIT, 'Edit po_int', '<ctrl>e',
                 'Edit the current point of the current dataset',
                 self.edit_point),
                ('edit_option', gtk.STOCK_EDIT, 'Edit op_tion', None,
                 'Edit the current option',
                 self.edit_option),

                ('view', None, '_View', None, 'View', None),
                ('refresh', gtk.STOCK_REFRESH, None, '<ctrl>r',
                 'Update the chart', self.refresh),

                ('tools', None, '_Tools', None, 'Tools', None),
                ('random-points', gtk.STOCK_EXECUTE, '_Generate random points',
                 '<ctrl>g', 'Generate random points',
                 self.generate_random_points),
                ('dump-chart-state', gtk.STOCK_CONVERT, '_Dump chart state',
                 '<ctrl>d', 'Dump internal chart variables',
                 self.dump_chart_state),
                ('help', None, '_Help', None, 'Help', None),
                ('about', gtk.STOCK_ABOUT, None, None, 'About this program',
                 self.about),
                ])
        action_group.add_radio_actions([
                ('verticalbar', None, '_Vertical bars', None,
                 'Use vertical bars chart', self.app.VERTICAL_BAR_TYPE),
                ('horizontalbar', None, '_Horizontal bars', None,
                 'Use horizontal bars chart', self.app.HORIZONTAL_BAR_TYPE),
                ('line', None, '_Line', None,
                 'Use lines chart', self.app.LINE_TYPE),
                ('pie', None, '_Pie', None,
                 'Use pie chart', self.app.PIE_TYPE),
                ('scatter', None, '_Scatter', None,
                 'Use scatter chart', self.app.SCATTER_TYPE),
                ('stackedverticalbar', None, '_Stacked Vertical bars', None,
                 'Use stacked vertical bars chart',
                 self.app.STACKED_VERTICAL_BAR_TYPE),
                ('stackedhorizontalbar', None, '_Stacked Horizontal bars', None,
                 'Use stacked horizontal bars chart',
                 self.app.STACKED_HORIZONTAL_BAR_TYPE),
                ], self.app.VERTICAL_BAR_TYPE, self.on_chart_type_change)
        self.uimanager.insert_action_group(action_group, -1)

        ui = """<ui>
  <menubar name="MenuBar">
    <menu action="file">
      <menuitem action="quit"/>
    </menu>
    <menu action="edit">
      <menuitem action="add_dataset"/>
      <menuitem action="remove_dataset"/>
      <menuitem action="edit_dataset"/>
      <separator />
      <menuitem action="add_point"/>
      <menuitem action="remove_point"/>
      <menuitem action="edit_point"/>
      <separator />
      <menuitem action="edit_option"/>
    </menu>
    <menu action="view">
      <menuitem action="refresh"/>
      <separator />
      <menuitem action="verticalbar"/>
      <menuitem action="horizontalbar"/>
      <menuitem action="stackedverticalbar"/>
      <menuitem action="stackedhorizontalbar"/>
      <menuitem action="line"/>
      <menuitem action="pie"/>
      <menuitem action="scatter"/>
    </menu>
    <menu action="tools">
      <menuitem action="random-points"/>
      <menuitem action="dump-chart-state"/>
    </menu>
    <menu action="help">
      <menuitem action="about"/>
    </menu>
  </menubar>
  <toolbar name="ToolBar">
    <toolitem action="quit"/>
    <separator />
    <toolitem action="add_dataset"/>
    <toolitem action="remove_dataset"/>
    <separator />
    <toolitem action="add_point"/>
    <toolitem action="remove_point"/>
    <separator />
    <toolitem action="refresh"/>
  </toolbar>
</ui>
"""
        self.uimanager.add_ui_from_string(ui)
        self.uimanager.ensure_update()
        menubar = self.uimanager.get_widget('/MenuBar')
        toolbar = self.uimanager.get_widget('/ToolBar')

        return menubar, toolbar

    def _create_sidebar_block(self, title, child_widget_creator):
        box = gtk.VBox(spacing=6)
        box.set_border_width(6)
        label = gtk.Label()
        label.set_markup(u'<span size="large" weight="bold">%s</span>' % title)
        label.set_alignment(0.0, 0.5)
        box.pack_start(label, False, False)
        label.show()

        child_widget = child_widget_creator()
        box.pack_start(child_widget, True, True)
        child_widget.show()

        return box

    def _datasets_notebook_creator(self):
        self.datasets_notebook = gtk.Notebook()
        self.datasets_notebook.set_scrollable(True)
        return self.datasets_notebook

    def _dataset_treeview_creator(self):
        store = gtk.ListStore(float, float)
        treeview = gtk.TreeView(store)

        column1 = gtk.TreeViewColumn('x', gtk.CellRendererText(), text=0)
        treeview.append_column(column1)

        column2 = gtk.TreeViewColumn('y', gtk.CellRendererText(), text=1)
        treeview.append_column(column2)

        treeview.connect('row-activated', self.dataset_treeview_row_activated)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scrolled_window.add(treeview)
        treeview.show()

        return scrolled_window

    def _options_treeview_creator(self):
        self.options_store = gtk.TreeStore(str, str, object)
        options = self.app.get_default_options()
        self._fill_options_store(options, None, self.app.OPTIONS_TYPES)

        self.options_treeview = gtk.TreeView(self.options_store)

        column1 = gtk.TreeViewColumn('Name', gtk.CellRendererText(), text=0)
        self.options_treeview.append_column(column1)

        column2 = gtk.TreeViewColumn('Value', gtk.CellRendererText(), text=1)
        self.options_treeview.append_column(column2)

        self.options_treeview.expand_all()

        self.options_treeview.connect('row-activated',
                                      self.options_treeview_row_activated)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scrolled_window.add(self.options_treeview)
        self.options_treeview.show()

        return scrolled_window

    def _fill_options_store(self, options, parent_node, types):
        for name, value in options.items():
            value_type = types[name]
            if isinstance(value, dict):
                current_parent = self.options_store.append(parent_node,
                                                           (name, None, None))
                self._fill_options_store(value, current_parent, value_type)

            else:
                if value is not None:
                    value = str(value)
                self.options_store.append(parent_node,
                                          (name, value, value_type))

    def _get_current_dataset_tab(self):
        current_tab = self.datasets_notebook.get_current_page()
        if current_tab != -1:
            return self.datasets_notebook.get_nth_page(current_tab)

    def _create_dataset(self, name):
        scrolled_window = self._dataset_treeview_creator()
        scrolled_window.show()
        label = gtk.Label(name)
        self.datasets_notebook.append_page(scrolled_window, label)

    def _get_datasets(self):
        datasets = []
        n_pages = self.datasets_notebook.get_n_pages()
        for i in range(n_pages):
            tab = self.datasets_notebook.get_nth_page(i)
            label = self.datasets_notebook.get_tab_label(tab)
            name = label.get_label()
            treeview = tab.get_children()[0]
            model = treeview.get_model()
            points = [(x, y) for x, y in model]
            if len(points) > 0:
                datasets.append((name, points))
        return datasets

    def _get_chart_type(self):
        action_group = self.uimanager.get_action_groups()[0]
        action = action_group.get_action('verticalbar')
        return action.get_current_value()

    def _get_options(self, iter):
        options = {}
        while iter is not None:
            name, value, value_type = self.options_store.get(iter, 0, 1, 2)
            if value_type is None:
                child = self.options_store.iter_children(iter)
                options[name] = self._get_options(child)
            else:
                if value is not None:
                    converter = str_converters[value_type]
                    value = converter(value)
                options[name] = value

            iter = self.options_store.iter_next(iter)

        return options

    def _edit_point_internal(self, model, iter):
        x, y = model.get(iter, 0, 1)

        dialog = PointDialog(self.main_window, x, y)
        response = dialog.run()
        if response == gtk.RESPONSE_ACCEPT:
            x, y = dialog.get_point()
            model.set(iter, 0, x, 1, y)
            self.refresh()
        dialog.destroy()

    def _edit_option_internal(self, model, iter):
        name, value, value_type = model.get(iter, 0, 1, 2)
        parents = []
        parent = model.iter_parent(iter)
        while parent is not None:
            parents.append(model.get_value(parent, 0))
            parent = model.iter_parent(parent)
        parents.reverse()
        parents.append(name)
        label = u'.'.join(parents)

        dialog = OptionDialog(self.main_window, label, value, value_type)
        response = dialog.run()
        if response == gtk.RESPONSE_ACCEPT:
            new_value = dialog.get_value()
            if new_value == "":
                new_value = None
            model.set_value(iter, 1, new_value)
            self.refresh()
        dialog.destroy()

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def drawing_area_expose_event(self, widget, event, data=None):
        if self.chart is None:
            return

        cr = widget.window.cairo_create()
        cr.rectangle(event.area.x, event.area.y,
                     event.area.width, event.area.height)
        cr.clip()
        cr.set_source_surface(self.chart.surface, 0, 0)
        cr.paint()

    def drawing_area_size_allocate_event(self, widget, event, data=None):
        if self.chart is not None:
            self.refresh()

    def on_chart_type_change(self, action, current, data=None):
        if self.chart is not None:
            self.refresh()

    def dataset_treeview_row_activated(self, treeview, path, view_column):
        model = treeview.get_model()
        iter = model.get_iter(path)
        self._edit_point_internal(model, iter)

    def options_treeview_row_activated(self, treeview, path, view_column):
        model = treeview.get_model()
        iter = model.get_iter(path)
        self._edit_option_internal(model, iter)

    def quit(self, action):
        self.main_window.destroy()

    def add_dataset(self, action):
        n_pages = self.datasets_notebook.get_n_pages()
        suggested_name = u'Dataset %d' % (n_pages + 1)
        dialog = TextInputDialog(self.main_window, suggested_name)
        response = dialog.run()
        if response == gtk.RESPONSE_ACCEPT:
            name = dialog.get_name()
            self._create_dataset(name)
            self.datasets_notebook.set_current_page(n_pages)
        dialog.destroy()

    def remove_dataset(self, action):
        current_tab = self.datasets_notebook.get_current_page()
        assert current_tab != -1

        self.datasets_notebook.remove_page(current_tab)

    def edit_dataset(self, action):
        tab = self._get_current_dataset_tab()
        assert tab is not None

        label = self.datasets_notebook.get_tab_label(tab)
        name = label.get_label()
        dialog = TextInputDialog(self.main_window, name)
        response = dialog.run()
        if response == gtk.RESPONSE_ACCEPT:
            name = dialog.get_name()
            label.set_label(name)
        dialog.destroy()

    def add_point(self, action):
        tab = self._get_current_dataset_tab()
        assert tab is not None

        treeview = tab.get_children()[0]
        model = treeview.get_model()

        dialog = PointDialog(self.main_window, len(model) * 1.0, 0.0)
        response = dialog.run()
        if response == gtk.RESPONSE_ACCEPT:
            x, y = dialog.get_point()
            model.append((x, y))
            self.refresh()
        dialog.destroy()

    def remove_point(self, action):
        tab = self._get_current_dataset_tab()
        assert tab is not None

        treeview = tab.get_children()[0]
        selection = treeview.get_selection()
        model, selected = selection.get_selected()
        if selected is None:
            warning(self.main_window, "You must select the point to remove")
            return

        model.remove(selected)
        self.refresh()

    def edit_point(self, action):
        tab = self._get_current_dataset_tab()
        assert tab is not None

        treeview = tab.get_children()[0]
        selection = treeview.get_selection()
        model, selected = selection.get_selected()
        if selected is None:
            warning(self.main_window, "You must select the point to edit")
            return

        self._edit_point_internal(model, selected)

    def edit_option(self, action):
        selection = self.options_treeview.get_selection()
        model, selected = selection.get_selected()
        if selected is None:
            warning(self.main_window, "You must select the option to edit")
            return

        self._edit_option_internal(model, selected)

    def refresh(self, action=None):
        datasets = self._get_datasets()
        if datasets:
            root = self.options_store.get_iter_first()
            options = self._get_options(root)

            chart_type = self._get_chart_type()
            alloc = self.drawing_area.get_allocation()
            self.chart = self.app.get_chart(datasets, options, chart_type,
                                            alloc.width, alloc.height)
            self.drawing_area.queue_draw()
        else:
            self.chart = None

    def generate_random_points(self, action=None):
        tab = self._get_current_dataset_tab()
        assert tab is not None

        treeview = tab.get_children()[0]
        model = treeview.get_model()

        dialog = RandomGeneratorDialog(self.main_window)
        response = dialog.run()
        if response == gtk.RESPONSE_ACCEPT:
            points = dialog.generate_points()
            for point in points:
                model.append(point)
            self.refresh()
        dialog.destroy()

    def dump_chart_state(self, action=None):
        if self.chart is None:
            return

        alloc = self.drawing_area.get_allocation()

        print 'CHART STATE'
        print '-' * 70
        print 'surface: %d x %d' % (alloc.width, alloc.height)
        print 'area   :', self.chart.area
        print
        print 'minxval:', self.chart.minxval
        print 'maxxval:', self.chart.maxxval
        print 'xrange :', self.chart.xrange
        print
        print 'minyval:', self.chart.minyval
        print 'maxyval:', self.chart.maxyval
        print 'yrange :', self.chart.yrange

    def about(self, action=None):
        dialog = AboutDialog(self.main_window)
        dialog.run()
        dialog.destroy()

    def run(self):
        gtk.main()


def str2bool(str):
    if str.lower() == "true":
        return True
    else:
        return False


str_converters = {
    str: str,
    int: int,
    float: float,
    unicode: unicode,
    bool: str2bool,
}
