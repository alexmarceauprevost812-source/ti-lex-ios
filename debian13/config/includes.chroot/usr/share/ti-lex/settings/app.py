#!/usr/bin/env python3
"""TI-LEX GTK 3 control center. Run as the desktop user, never sudo."""
import subprocess
import threading
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
from backend import TOOLS, available, wifi_state, bluetooth_state

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
"""

class Settings(Gtk.Window):
    def __init__(self):
        super().__init__(title="Paramètres TI-LEX Pro")
        try:
            self.set_icon_from_file("/usr/share/ti-lex/branding/settings.svg")
        except GLib.Error:
            self.set_icon_name("preferences-system")
        self.set_default_size(900, 720)
        self.alive = True
        self.busy = False
        self.connect("destroy", self.close)
        header = Gtk.HeaderBar(title="TI-LEX Pro")
        header.set_show_close_button(True)
        self.set_titlebar(header)
        scroll = Gtk.ScrolledWindow()
        self.add(scroll)
        body = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16, margin=24)
        scroll.add(body)
        title = Gtk.Label(label="Paramètres", xalign=0)
        title.get_style_context().add_class("title")
        body.pack_start(title, False, False, 0)
        legend = Gtk.Label(label="Vert : activé • Rouge : désactivé • Blanc : non défini / indisponible",
                           xalign=0)
        legend.set_line_wrap(True)
        body.pack_start(legend, False, False, 0)
        self.status = {}
        for name, buttons in [
            ("Wi-Fi", ["Choisir un réseau Wi-Fi", "Profils réseau / VPN"]),
            ("Bluetooth", ["Appareils Bluetooth"]),
            ("Bureau et matériel", ["Son et microphones", "Enregistrer le microphone", "Webcam",
                "Imprimantes", "Scanner", "Écrans", "Clavier",
                "Souris et pavé tactile", "Apparence", "Fond du bureau", "Alimentation"]),
            ("Système", ["Disques", "Pare-feu", "Processus", "Tous les paramètres XFCE"]),
            ("Terminal et développement", ["Terminal TI-LEX", "Préférences du terminal",
                "Guide des commandes", "Sessions tmux", "Python", "Éditeur de texte"]),
            ("Fichiers et diagnostic", ["Ouvrir une application", "Fichiers", "Archives", "Sauvegardes",
                "Espace disque", "Capture d’écran", "Informations système", "Journaux système"]),
        ]:
            card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
            card.get_style_context().add_class("card")
            label = Gtk.Label(label=name, xalign=0)
            label.get_style_context().add_class("on")
            card.pack_start(label, False, False, 0)
            if name in ("Wi-Fi", "Bluetooth"):
                state = Gtk.Label(label="Lecture de l’état…", xalign=0)
                state.set_line_wrap(True)
                card.pack_start(state, False, False, 0)
                self.status[name] = state
            flow = Gtk.FlowBox()
            flow.set_selection_mode(Gtk.SelectionMode.NONE)
            flow.set_max_children_per_line(3)
            for text in buttons:
                command = TOOLS[text]
                button = Gtk.Button(label=text)
                button.set_sensitive(available(command))
                button.set_tooltip_text("Ouvrir l’outil système" if available(command)
                                        else "Outil non installé — indisponible")
                button.connect("clicked", self.launch, command, text)
                flow.add(button)
            card.pack_start(flow, False, False, 0)
            body.pack_start(card, False, False, 0)
        refresh = Gtk.Button(label="Actualiser les états")
        refresh.connect("clicked", lambda *_: self.refresh())
        body.pack_start(refresh, False, False, 0)
        note = Gtk.Label(label="Les réglages s’ouvrent dans les outils système. Les autorisations Linux restent actives.",
                         xalign=0)
        note.set_line_wrap(True)
        body.pack_start(note, False, False, 0)
        self.timer = GLib.timeout_add_seconds(10, self.refresh)
        self.refresh()

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
