#!/usr/bin/env python3
"""TI-LEX GTK 3 control center. Run as the desktop user, never sudo."""
from pathlib import Path
import subprocess
import sys
import threading
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
from backend import TOOLS, available, wifi_state, bluetooth_state
from pages import PAGES, search_tools
# crt.py vit dans le dossier parent, partagé par les fenêtres TI-LEX.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from crt import Tube

CSS = b"""
window, .root { background-color: #08080b; color: #ffffff; }
headerbar { background: #111116; color: #b4ff39; border-radius: 18px 18px 0 0; }
label { color: #ffffff; }
.title { color: #b4ff39; font-size: 24px; font-weight: bold; }
.card { background: #15151c; border: 1px solid #34343c; border-radius: 20px; padding: 18px; }
button { background-image: none; background-color: #ff8a24; color: #08080b;
         border: none; border-radius: 16px; padding: 10px 16px; }
button label { color: #08080b; }
button:hover { background-color: #ffa94c; }
button:disabled { background-color: #39393f; }
button:disabled label { color: #cccccc; }
.on { color: #b4ff39; }
.off { color: #ff6068; }
.unknown { color: #ffffff; }
.subtitle { color: #b8b8c2; }
stackswitcher, stacksidebar { background-color: #111116; }
stacksidebar row { padding: 9px; }
stacksidebar row:selected { background-color: #502b13; }
entry { background-color: #17171c; color: #ffffff; border-radius: 10px; padding: 10px; }
"""

class Settings(Gtk.Window):
    def __init__(self):
        super().__init__(title="Paramètres TI-LEX Pro")
        try:
            self.set_icon_from_file("/usr/share/ti-lex/branding/settings.svg")
        except GLib.Error:
            self.set_icon_name("preferences-system")
        self.set_default_size(1100, 760)
        self.alive = True
        self.busy = False
        self.connect("destroy", self.close)
        # Allumage et extinction du tube : l'effet ne retarde que la fermeture.
        self.tube = Tube(self)
        self.closing = False
        self.connect("map-event", self.power_on)
        self.connect("delete-event", self.power_off)
        header = Gtk.HeaderBar(title="TI-LEX Pro")
        header.set_show_close_button(True)
        self.set_titlebar(header)
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12, margin=16)
        self.add(root)
        self.search = Gtk.SearchEntry()
        self.search.set_placeholder_text("Rechercher un outil ou un paramètre…")
        self.search.connect("search-changed", self.search_changed)
        root.pack_start(self.search, False, False, 0)
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_hhomogeneous(False)
        self.stack.set_vhomogeneous(False)
        navigation = Gtk.StackSidebar()
        navigation.set_stack(self.stack)
        navigation_scroll = Gtk.ScrolledWindow()
        navigation_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        navigation_scroll.set_size_request(245, -1)
        navigation_scroll.add(navigation)
        layout = Gtk.Box(spacing=16)
        layout.pack_start(navigation_scroll, False, False, 0)
        layout.pack_start(self.stack, True, True, 0)
        root.pack_start(layout, True, True, 0)
        self.status = {}
        self.page_before_search = "Accueil"
        home = self.add_page("Accueil", "Vos outils et paramètres Linux, réunis au même endroit.")
        home_flow = self.new_flow()
        home.pack_start(home_flow, False, False, 0)
        for name, icon, description, buttons in PAGES:
            card = self.add_page(name, description)
            shortcut = Gtk.Button(label=name)
            shortcut.set_image(Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.DIALOG))
            shortcut.set_always_show_image(True)
            shortcut.connect("clicked", self.open_page, name)
            home_flow.add(shortcut)
            state_key = "Wi-Fi" if name == "Wi-Fi et réseau" else name
            if state_key in ("Wi-Fi", "Bluetooth"):
                state = Gtk.Label(label="Lecture de l’état…", xalign=0)
                state.set_line_wrap(True)
                card.pack_start(state, False, False, 0)
                self.status[state_key] = state
            flow = self.new_flow()
            for text in buttons:
                flow.add(self.tool_button(text, icon))
            card.pack_start(flow, False, False, 0)
        results = self.add_page("Recherche", "Résultats dans toutes les catégories.")
        self.result_count = Gtk.Label(xalign=0)
        results.pack_start(self.result_count, False, False, 0)
        self.results_flow = self.new_flow()
        results.pack_start(self.results_flow, False, False, 0)
        self.stack.set_visible_child_name("Accueil")
        refresh = Gtk.Button(label="Actualiser les états")
        refresh.connect("clicked", lambda *_: self.refresh())
        root.pack_start(refresh, False, False, 0)
        note = Gtk.Label(label="Les réglages s’ouvrent dans les outils système. Les autorisations Linux restent actives.",
                         xalign=0)
        note.set_line_wrap(True)
        root.pack_start(note, False, False, 0)
        self.timer = GLib.timeout_add_seconds(10, self.refresh)
        self.refresh()

    def add_page(self, name, description):
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        body = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20, margin=12)
        scroll.add(body)
        title = Gtk.Label(label=name, xalign=0)
        title.get_style_context().add_class("title")
        body.pack_start(title, False, False, 0)
        subtitle = Gtk.Label(label=description, xalign=0)
        subtitle.set_line_wrap(True)
        subtitle.get_style_context().add_class("subtitle")
        body.pack_start(subtitle, False, False, 0)
        self.stack.add_titled(scroll, name, name)
        return body

    @staticmethod
    def new_flow():
        flow = Gtk.FlowBox()
        flow.set_selection_mode(Gtk.SelectionMode.NONE)
        flow.set_min_children_per_line(1)
        flow.set_max_children_per_line(2)
        flow.set_column_spacing(12)
        flow.set_row_spacing(12)
        return flow

    def tool_button(self, text, icon):
        command = TOOLS[text]
        installed = available(command)
        button = Gtk.Button()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8, margin=8)
        box.pack_start(Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.DIALOG), False, False, 0)
        label = Gtk.Label(label=text)
        label.set_line_wrap(True)
        box.pack_start(label, False, False, 0)
        hint = Gtk.Label(label="Ouvrir" if installed else "Outil non installé")
        box.pack_start(hint, False, False, 0)
        button.add(box)
        button.set_sensitive(installed)
        button.set_tooltip_text(text if installed else "Cet outil n’est pas installé sur ce système.")
        button.connect("clicked", self.launch, command, text)
        return button

    def open_page(self, _button, name):
        self.search.set_text("")
        self.page_before_search = name
        self.stack.set_visible_child_name(name)

    def search_changed(self, entry):
        query = entry.get_text().strip()
        if not query:
            if self.stack.get_visible_child_name() == "Recherche":
                self.stack.set_visible_child_name(self.page_before_search)
            return
        if self.stack.get_visible_child_name() != "Recherche":
            self.page_before_search = self.stack.get_visible_child_name()
        for child in self.results_flow.get_children():
            child.destroy()
        matches = search_tools(query)
        self.result_count.set_text(f"{len(matches)} outil(s) trouvé(s)" if matches else "Aucun outil trouvé. Essayez un autre mot.")
        for _category, icon, tool in matches:
            self.results_flow.add(self.tool_button(tool, icon))
        self.results_flow.show_all()
        self.stack.set_visible_child_name("Recherche")

    def power_on(self, *_):
        self.tube.turn_on()
        return False

    def power_off(self, *_):
        """Éteint d'abord, ferme ensuite. Le second passage laisse filer la fermeture."""
        if self.closing:
            return False
        self.closing = True
        self.tube.turn_off(self.destroy)
        return True

    def close(self, *_):
        self.alive = False
        GLib.source_remove(self.timer)
        Gtk.main_quit()

    def refresh(self):
        if not self.alive:
            return False
        if self.busy:
            return True
        self.busy = True
        def worker():
            result = {"Wi-Fi": wifi_state(), "Bluetooth": bluetooth_state()}
            GLib.idle_add(self.render_states, result)
        threading.Thread(target=worker, daemon=True).start()
        return True

    def render_states(self, result):
        self.busy = False
        if not self.alive:
            return False
        for key, (kind, text) in result.items():
            label = self.status[key]
            for css in ("on", "off", "unknown"):
                label.get_style_context().remove_class(css)
            label.get_style_context().add_class(kind)
            label.set_text(text)
        return False

    def launch(self, button, command, title):
        if title == "Disques":
            dialog = Gtk.MessageDialog(transient_for=self, modal=True,
                message_type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK_CANCEL,
                text="Ouvrir la gestion des disques ?")
            dialog.format_secondary_text("Le formatage et les modifications de partitions peuvent effacer des données.")
            response = dialog.run()
            dialog.destroy()
            if response != Gtk.ResponseType.OK:
                return
        button.set_sensitive(False)
        def worker():
            try:
                # No secrets or output are captured or logged.
                process = subprocess.Popen(command, stdout=subprocess.DEVNULL,
                                           stderr=subprocess.DEVNULL)
                code = process.wait()
                error = None if code == 0 else f"L’outil s’est terminé avec le code {code}. Une autorisation a pu être refusée."
            except OSError as exc:
                error = f"Impossible de lancer cet outil : {exc}"
            GLib.idle_add(self.finished, button, error)
        threading.Thread(target=worker, daemon=True).start()

    def finished(self, button, error):
        if not self.alive:
            return False
        button.set_sensitive(True)
        if error:
            dialog = Gtk.MessageDialog(transient_for=self, modal=True,
                message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CLOSE,
                text=error)
            dialog.run()
            dialog.destroy()
        self.refresh()
        return False

if __name__ == "__main__":
    provider = Gtk.CssProvider()
    provider.load_from_data(CSS)
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider,
                                             Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    window = Settings()
    window.show_all()
    Gtk.main()
