from typing import TYPE_CHECKING

import gi
gi.require_version("Gtk", "3.0") # pylint: disable=wrong-import-position
from gi.repository import Gtk

from gramps.gen.plug._gramplet import Gramplet

if TYPE_CHECKING:
    from gramps.gen.plug._gramplet import GUIStub



class FormGramplet(Gramplet):

    def __init__(self, gui: "GUIStub", nav_group: int = 0) -> None:
        super().__init__(gui, nav_group)
        self.model: Gtk.ListStore | None = None

    def init(self) -> None:
        container = self.gui.get_container_widget()
        for child in container.get_children():
            container.remove(child)
        gui = self._build_gui()
        container.add(gui)
        gui.show_all()

    def _build_gui(self) -> Gtk.Box:
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.model = Gtk.ListStore(str, str)
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
