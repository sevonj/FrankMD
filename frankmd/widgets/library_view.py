# library_view.py
#
# Copyright 2024 Sevonj
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi

gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk, GObject, Pango
from typing import Any, Callable, Self

from frankmd.app.app_state import AppState
from frankmd.app.project import LibraryDir, Project


class LibraryDirView(Adw.ActionRow):

    __gtype_name__ = "LibraryDirView"

    @GObject.Signal
    def selected(self) -> None: ...

    def __init__(self, library_dir: LibraryDir, app: AppState, container: Gtk.ListBox):
        super().__init__()

        self._dir: LibraryDir = library_dir
        self._app: AppState = app
        self._content: dict[str, Self] = {}
        self._container = container

        self.set_margin_top(8)

        self._label = Gtk.Label(label="LABEL")
        self._label.set_ellipsize(Pango.EllipsizeMode.END)
        self._spacer = Gtk.Box()
        self._spacer.set_property("width_request", 12 * self._dir.get_depth())
        self._end_spacer = Gtk.Box()
        self._end_spacer.set_hexpand(True)
        self._button_content = Gtk.Box()
        self._button_content.append(self._spacer)
        self._button_content.append(self._label)
        self._button_content.append(self._end_spacer)
        self.set_activatable(True)
        self.set_child(self._button_content)
        self.connect("activated", self._on_select_click)

    def refresh(self) -> None:
        name = self._dir.get_display_name()
        self._label.set_label(name)

        for subdir in self._dir.get_subdirs():
            child = LibraryDirView(subdir, self._app, self._container)
            self._content[subdir.get_path()] = child  # type: ignore
            self._container.append(child)
            child.refresh()

        if self._dir == self._app.get_current_dir():
            self._container.select_row(self)

    def add_select_callback(self, callback) -> None:
        self.connect("selected", callback)
        for _, child in self._content.items():
            child.add_select_callback(callback)

    def get_dir(self) -> LibraryDir:
        return self._dir

    def _on_select_click(self, _source) -> None:
        self.selected.emit()  # type: ignore


class ProjectView(Adw.ActionRow):

    __gtype_name__ = "ProjectView"

    @GObject.Signal
    def dir_selected(self) -> None: ...
    @GObject.Signal
    def removed(self) -> None: ...

    def __init__(self, project: Project, app: AppState, container: Gtk.ListBox):
        super().__init__()

        self._project: Project = project
        self._app: AppState = app
        self._content: dict[str, LibraryDirView] = {}

        self.set_margin_top(8)
        self.add_css_class("library-view-project")

        self._label = Gtk.Label(label="LABEL")
        self._label.set_ellipsize(Pango.EllipsizeMode.END)
        self._end_spacer = Gtk.Box()
        self._end_spacer.set_hexpand(True)
        self._button_content = Gtk.Box()
        self._button_content.append(self._label)
        self._button_content.append(self._end_spacer)
        self._rm_button = Gtk.Button()
        self._rm_button.set_css_classes(["circular", "flat", "body"])
        self._rm_button.set_icon_name("window-close-symbolic")
        self._rm_button.connect("clicked", self._on_remove_click)
        self._button_content.append(self._rm_button)
        self.set_activatable(True)
        self.set_child(self._button_content)
        self._container = container
        self._container.add_css_class("navigation-sidebar")

    def refresh(self) -> None:
        name = self._project.get_display_name()
        self._label.set_label(name)

        root = self._project.get_root()

        for subdir in root.get_subdirs():
            child = LibraryDirView(subdir, self._app, self._container)
            self._container.append(child)
            child.refresh()
            self._content[subdir.get_path()] = child  # type: ignore

        if root == self._app.get_current_dir():
            self._container.select_row(self)

    def add_select_callback(self, callback) -> None:
        self.connect("dir_selected", callback)
        for _, child in self._content.items():
            child.add_select_callback(callback)

    def get_dir(self) -> LibraryDir:
        return self._project.get_root()

    def _on_select_click(self, _source) -> None:
        self.dir_selected.emit()  # type: ignore

    def _on_remove_click(self, _source) -> None:
        self.removed.emit()  # type: ignore


@Gtk.Template(resource_path="/fi/sevonj/FrankMD/library_view.ui")
class LibraryView(Adw.NavigationPage):
    """Sidebar project browser"""

    __gtype_name__ = "LibraryView"

    # Selected dir was changed by some other action
    @GObject.Signal
    def dir_changed(self) -> None: ...

    # Dir was deliberately changed by user and should be focused
    @GObject.Signal
    def dir_selected(self) -> None: ...

    header: Adw.HeaderBar = Gtk.Template.Child()  # type: ignore
    container: Gtk.ListBox = Gtk.Template.Child()  # type: ignore
    scrollarea: Gtk.ScrolledWindow = Gtk.Template.Child()  # type: ignore
    add_project_button: Gtk.Button = Gtk.Template.Child()  # type: ignore

    def __init__(self, app: AppState):
        super().__init__()

        self._app = app
        self._content: list = []
        self._open_dialog = Gtk.FileDialog()

        self.set_title("Library")

        self.add_project_button.connect("clicked", self._add_new_project)
        self.container.connect("row-activated", self._on_row_activated)

        self.refresh()

    def refresh(self) -> None:
        self.container.remove_all()

        for project in self._app.get_projects():
            project_view = ProjectView(project, self._app, self.container)
            project_view.add_select_callback(self._on_dir_selected)
            project_view.connect("removed", self._on_project_remove)
            self._content.append(project_view)
            self.container.append(project_view)
            project_view.refresh()

    def _on_dir_selected(self, source: LibraryDirView | ProjectView):
        self._app.set_current_dir(source.get_dir())
        self.dir_selected.emit()  # type: ignore
        self.refresh()

    def _on_row_activated(self, _container, row: LibraryDirView | ProjectView):
        self._app.set_current_dir(row.get_dir())
        self.dir_selected.emit()  # type: ignore
        self.refresh()

    def _on_project_remove(self, project_view: ProjectView):
        try:
            assert project_view in self._content
            self._app.remove_project(project_view.get_dir().get_path())
            self.container.remove(project_view)
            self._content.remove(project_view)
        except BaseException as e:
            print(e)
        self.dir_changed.emit()  # type: ignore
        self.refresh()

    def _add_new_project(self, _source):
        self._open_dialog.select_folder(callback=self._add_new_project_callback)

    def _add_new_project_callback(self, dialog: Gtk.FileDialog, result):
        try:
            file = dialog.select_folder_finish(result)
            if file is not None:
                path = file.get_path()
                if path is not None:
                    self._app.add_project(path)
                    self.dir_changed.emit()  # type: ignore
                    self.refresh()
        except BaseException as e:
            print(e)
