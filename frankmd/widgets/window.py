# window.py
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

from typing import Any
from gi.repository import Adw
from gi.repository import Gtk

from frankmd.app.app_state import AppState
from frankmd.widgets.library_view import LibraryDirView, LibraryView
from frankmd.widgets.md_editor import MdEditor
from frankmd.widgets.sheets_view import SheetsView


@Gtk.Template(resource_path="/fi/sevonj/FrankMD/window.ui")
class MainWindow(Adw.ApplicationWindow):
    """App Main Window"""

    __gtype_name__ = "MainWindow"

    library_sidebar_toggle: Gtk.Button = Gtk.Template.Child()  # type: ignore
    library_split: Adw.NavigationSplitView = Gtk.Template.Child()  # type: ignore
    editor_save_button: Gtk.Button = Gtk.Template.Child()  # type: ignore
    main_view: Adw.ToolbarView = Gtk.Template.Child()  # type: ignore
    main_split: Adw.OverlaySplitView = Gtk.Template.Child()  # type: ignore

    def __init__(self, app: AppState, **kwargs) -> None:
        super().__init__(**kwargs)

        self._app: AppState = app

        self._library_view = LibraryView(app)
        self._library_view.connect("dir_changed", self._on_dir_changed)
        self._library_view.connect("dir_selected", self._on_dir_selected)
        self._sheets_view = SheetsView(app)
        self._sheets_view.connect("sheet_selected", self._on_sheet_selected)
        self.library_split.set_sidebar(self._library_view)
        self.library_split.set_content(self._sheets_view)
        self._md_editor = MdEditor(app)
        self.main_view.set_content(self._md_editor)

        self.library_sidebar_toggle.connect("clicked", self._toggle_sidebar)
        self.editor_save_button.connect("clicked", self._save_sheet)

    def show_sheetview(self) -> None:
        """Go to sheet list. Does nothing unless libray split is collapsed."""
        self.library_split.set_show_content(True)

    def _toggle_sidebar(self, _button: Any) -> None:
        self.main_split.set_show_sidebar(not self.main_split.get_show_sidebar())

    def _save_sheet(self, _button: Any) -> None:
        self._md_editor.save_sheet()

    def _on_dir_changed(self, _source):
        self._sheets_view.refresh()

    def _on_dir_selected(self, _source):
        self._sheets_view.refresh()
        self.library_split.set_show_content(True)

    def _on_sheet_selected(self, _source):
        sheet = self._app.get_current_sheet()
        if sheet is None:
            return
        self._md_editor.open_sheet(sheet)
