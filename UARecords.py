from __future__ import annotations
from typing import TYPE_CHECKING, List

import gi

from base_edit_form import BaseEditForm
gi.require_version("Gtk", "3.0") # pylint: disable=wrong-import-position
from gi.repository import Gtk, GObject

from gramps.gen.plug._gramplet import Gramplet
from settings.settings_manager import get_settings_manager, SettingsManager
from settings.settings_ui import SettingsUI
from ulogging.autoinit import logger

if TYPE_CHECKING:
    from gramps.gen.plug._gramplet import GUIStub
    from gramps.gen.plug.menu import MenuOption


class UARecords(Gramplet):

    def __init__(self, gui: "GUIStub", nav_group: int = 0) -> None:
        logger.channel("success").debug("Starting UARecords gramplet initialization")
        self.settings_manager: SettingsManager = get_settings_manager()
        logger.channel("success").info("Settings manager initialized successfully")
        self.settings_ui = SettingsUI(self.settings_manager)
        super().__init__(gui, nav_group)
        self.model: Gtk.ListStore | None = None
        self.opts_cache: List[MenuOption] = []
        logger.channel("success").info("UARecords gramplet initialization completed")       

    def init(self) -> None:
        logger.channel("success").debug("Starting gramplet initialization process")
        logger.channel("success").info("Initializing gramplet GUI")
        logger.channel("success").warning("This is a test warning message")
        container = self.gui.get_container_widget()
        for child in container.get_children():
            container.remove(child)
        gui = self._build_gui()
        container.add(gui)
        gui.show_all()
        try:
            # Simulate a potential error for demonstration
            test_value = 1 / 0  # This won't actually error, just for demo
            if test_value == 1:
                logger.channel("exceptions").error("Demo error: simulated issue in GUI initialization")
        except Exception as e:
            logger.channel("exceptions").critical("Critical error during GUI initialization", exc=e)
        logger.channel("success").info("GUI initialization completed successfully")

    def _build_gui(self) -> Gtk.Box:
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.model = Gtk.ListStore(GObject.TYPE_STRING, GObject.TYPE_STRING)
        view = Gtk.TreeView(model=self.model)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Список форм", renderer, text=1)
        view.append_column(column)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        scroll.add(view)
        vbox.pack_start(scroll, True, True, 0)
        return vbox

    def build_options(self) -> None:
        self.opts_cache = self.settings_ui.build_options()
        for opt in self.opts_cache:
            self.add_option(opt)

    def save_options(self) -> None:
        opts = self.opts_cache
        if len(opts) < 10:
            return

        self.settings_manager.set_ai_provider(opts[0].get_value())
        self.settings_manager.set_ai_model(opts[1].get_value())
        self.settings_manager.set_ai_api_key(opts[2].get_value())

        self.settings_manager.set_birth_columns(int(opts[3].get_value()))
        self.settings_manager.set_death_columns(int(opts[4].get_value()))
        self.settings_manager.set_marriage_columns(int(opts[5].get_value()))

        self.settings_manager.set_form_density(opts[6].get_value())

        self.settings_manager.set_person_name_length(int(opts[7].get_value()))
        self.settings_manager.set_place_title_length(int(opts[8].get_value()))
        self.settings_manager.set_citation_text_length(int(opts[9].get_value()))

        self._refresh_open_forms()

    def save_update_options(self, obj: object) -> None:
        self.save_options()
        self.update()

    def _refresh_open_forms(self) -> None:
        for win in Gtk.Window.list_toplevels():
            if isinstance(win, BaseEditForm) and hasattr(win, "refresh_options"):
                try:
                    win.refresh_options(None)
                except Exception:
                    pass
