# md_editor.py
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
from gi.repository import Adw, Gio, Gtk, GtkSource
from frankmd.app.app_state import AppState
from frankmd.app.sheet import Sheet

gi.require_version("Adw", "1")


@Gtk.Template(resource_path="/fi/sevonj/FrankMD/md_editor.ui")
class MdEditor(Adw.Bin):
    """Sidebar project browser"""

    __gtype_name__ = "MdEditor"

    __slots__ = (
        "_app",
        "_content",
        "_sheet",
        "_buffer",
        "_gfile",
        "_file",
        "_sourceview",
    )

    sourceview: GtkSource.View = Gtk.Template.Child()  # type: ignore

    def __init__(self, app: AppState):
        super().__init__()

        self._app = app
        self._content: list = []
        self._sheet: Sheet

        lang_manager = GtkSource.LanguageManager()
        lang: GtkSource.Language = lang_manager.get_language("markdown")  # type: ignore
        assert isinstance(lang, GtkSource.Language)
        self._buffer = GtkSource.Buffer.new_with_language(lang)
        self._gfile: Gio.File
        self._file: GtkSource.File

        self.sourceview.set_buffer(self._buffer)
        self.set_margin_start(32)
        self.set_margin_end(32)

    def open_sheet(self, sheet: Sheet):
        print(f"Editor open: {sheet.get_display_name()}")
        self._sheet = sheet
        self._gfile = Gio.File.new_for_path(sheet.get_path())
        self._file = GtkSource.File(location=self._gfile)

        if not self._gfile.query_exists():
            print(f"open_sheet(): Nonexistent file {sheet.get_path()}")
            return

        try:
            file_loader = GtkSource.FileLoader.new_from_stream(
                buffer=self._buffer,
                file=self._file,
                stream=self._gfile.read(),
            )
            file_loader.load_async(0)

        except BaseException as e:
            print(f"open_sheet(): {e}")

    def save_sheet(self):
        try:
            file_saver = GtkSource.FileSaver.new_with_target(
                buffer=self._buffer,
                file=self._file,
                target_location=self._gfile,
            )
            file_saver.save_async(0)

        except BaseException as e:
            print(f"open_sheet(): {e}")
