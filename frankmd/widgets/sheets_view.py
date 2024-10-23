# sheets_view.py
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

from frankmd.app.sheet import Sheet

gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk, GObject

from frankmd.app.app_state import AppState


@Gtk.Template(resource_path="/fi/sevonj/FrankMD/sheet_button.ui")
class SheetButton(Gtk.Button):
    """ """

    __gtype_name__ = "SheetButton"

    box: Gtk.Box = Gtk.Template.Child()  # type: ignore
    title: Gtk.Label = Gtk.Template.Child()  # type: ignore
    preview: Gtk.Label = Gtk.Template.Child()  # type: ignore

    def __init__(self, sheet: Sheet, **kwargs) -> None:
        super().__init__(**kwargs)

        self._sheet = sheet

        self.title.set_label(sheet.get_display_name())
        self.preview.set_label(sheet.get_display_stub())

    def get_sheet(self) -> Sheet:
        return self._sheet


@Gtk.Template(resource_path="/fi/sevonj/FrankMD/sheets_view.ui")
class SheetsView(Adw.NavigationPage):
    """Sidebar project browser / dir tree"""

    __gtype_name__ = "SheetsView"

    @GObject.Signal
    def sheet_selected(self) -> None: ...

    header: Adw.HeaderBar = Gtk.Template.Child()  # type: ignore
    title: Gtk.Label = Gtk.Template.Child()  # type: ignore
    container: Gtk.Box = Gtk.Template.Child()  # type: ignore
    scrollarea: Gtk.ScrolledWindow = Gtk.Template.Child()  # type: ignore
    create_sheet_button: Gtk.Button = Gtk.Template.Child()  # type: ignore

    def __init__(self, app: AppState) -> None:
        super().__init__()

        self.set_title("Sheets")

        self._app: AppState = app
        self._content: list = []

        self.create_sheet_button.connect("clicked", self._create_sheet)

        # Use a fake title widget instead, to achieve left align.
        self.title.set_text(self.get_title())

        self.refresh()

    def refresh(self) -> None:
        for widget in self._content:
            self.container.remove(widget)
        self._content.clear()

        directory = self._app.get_current_dir()
        if directory is None:
            self.set_title("Nada")
            self.title.set_text(self.get_title())
            return

        self.set_title(directory.get_display_name())
        self.title.set_text(self.get_title())

        for sheet in directory.get_sheets():
            sheet_button = SheetButton(sheet)
            sheet_button.connect("clicked", self._select_sheet)
            self._content.append(sheet_button)
            self.container.append(sheet_button)

    def _select_sheet(self, source: SheetButton) -> None:
        self._app.set_current_sheet(source.get_sheet())
        self.sheet_selected.emit()  # type: ignore

    def _create_sheet(self, _source) -> None:
        cur_dir = self._app.get_current_dir()
        if cur_dir is None:
            return
        cur_dir.create_sheet()
        self.refresh()
