# main.py
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

import sys
from typing import Any, Callable
import gi

from frankmd.app.app_state import AppState


gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("GtkSource", "5")

from gi.repository import Gtk, Gio, Adw, GtkSource
from frankmd.widgets.window import MainWindow


class FrankmdApp(Adw.Application):
    """The main application singleton class."""

    _app: AppState

    def __init__(self):
        super().__init__(
            application_id="fi.sevonj.FrankMD", flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )
        GtkSource.init()  # Needed to use GtkSource widgets in ui xml

        self.create_action("quit", lambda *_: self.quit(), ["<primary>q"])
        self.create_action("about", self.on_about_action)
        self.create_action("preferences", self.on_preferences_action)

        self._app = AppState()

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = MainWindow(self._app, application=self)
        assert isinstance(win, MainWindow)
        win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""

        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name="frankmd",
            application_icon="fi.sevonj.FrankMD",
            developer_name="Sevonj",
            version="0.1.0",
            developers=["Sevonj"],
            copyright="© 2024 Sevonj",
        )
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print("app.preferences action activated")

    def create_action(self, name: str, callback: Callable[..., Any], shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(_version: str) -> int:
    """The application's entry point."""

    app = FrankmdApp()
    return app.run(sys.argv)
