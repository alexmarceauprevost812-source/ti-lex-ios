#!/usr/bin/python3
"""GUI launch action for Thunar; extraction is not an application security sandbox."""
import os
from pathlib import Path
import subprocess
import sys
import threading
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from core import extract_archive, candidates, command_for

class Launcher(Gtk.Window):
    def __init__(self, source):
        super().__init__(title="Ouvrir avec TI-LEX")
        self.set_default_size(600, 360)
        self.set_icon_from_file("/usr/share/ti-lex/branding/tools.svg")
        self.connect("destroy", Gtk.main_quit)
        self.source = source.resolve()
        self.paths = []
        self.alive = True
        self.connect("destroy", lambda *_: setattr(self, "alive", False))
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16, margin=24)
        self.add(box)
        title = Gtk.Label(label="Votre application, sans terminal", xalign=0)
        box.pack_start(title, False, False, 0)
        label = Gtk.Label(label=self.source.name, xalign=0)
        label.set_line_wrap(True)
        box.pack_start(label, False, False, 0)
        self.status = Gtk.Label(label="Préparation…", xalign=0)
        self.status.set_line_wrap(True)
        box.pack_start(self.status, False, False, 0)
        self.choice = Gtk.ComboBoxText()
        box.pack_start(self.choice, False, False, 0)
        notice = Gtk.Label(label="Exécutez uniquement une application dont vous connaissez la provenance. Elle aura accès aux fichiers de votre compte.", xalign=0)
        notice.set_line_wrap(True)
        box.pack_start(notice, False, False, 0)
        self.run_button = Gtk.Button(label="Ouvrir l’application")
        self.run_button.get_style_context().add_class("suggested-action")
        self.run_button.set_sensitive(False)
        self.run_button.connect("clicked", self.launch)
        box.pack_start(self.run_button, False, False, 0)
        threading.Thread(target=self.prepare, daemon=True).start()

    def prepare(self):
        try:
            if self.source.suffix.lower() == ".zip":
                base = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share")
                folder = extract_archive(self.source, base / "ti-lex/apps")
                paths = candidates(folder)
                message = "Extraction terminée. Choisissez le programme à ouvrir."
            else:
                paths = [self.source] if self.source.is_file() else []
                message = "Prêt à ouvrir. Un paquet .deb utilisera l’installateur graphique."
            GLib.idle_add(self.ready, paths, message)
        except Exception as exc:
            GLib.idle_add(self.ready, [], str(exc))

    def ready(self, paths, message):
        if not self.alive:
            return False
        self.paths = paths
        self.status.set_text(message if paths else message + "\nAucun programme Linux compatible disponible.")
        for path in paths:
            self.choice.append_text(str(path.relative_to(path.parents[0])) if len(paths) == 1 else str(path))
        if paths:
            self.choice.set_active(0)
            self.run_button.set_sensitive(True)
        return False

    def launch(self, *_):
        index = self.choice.get_active()
        if index < 0:
            return
        path = self.paths[index]
        try:
            command = command_for(path)
            # No root launch, shell interpolation, or archive auto-execution.
            log_dir = Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local/state") / "ti-lex"
            log_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
            log = log_dir / "application.log"
            with log.open("w", encoding="utf-8") as stream:
                log.chmod(0o600)
                process = subprocess.Popen(command, cwd=path.parent, stdin=subprocess.DEVNULL,
                                           stdout=stream, stderr=stream, start_new_session=True)
            self.run_button.set_sensitive(False)
            self.status.set_text("Programme démarré. Les dépendances et la compatibilité restent celles de l’application.")
            def wait():
                code = process.wait()
                GLib.idle_add(self.finished, code, log)
            threading.Thread(target=wait, daemon=True).start()
        except (OSError, ValueError) as exc:
            self.status.set_text("Ouverture impossible : " + str(exc))

    def finished(self, code, log):
        if not self.alive:
            return False
        self.run_button.set_sensitive(True)
        self.status.set_text("Programme terminé." if code == 0 else f"Le programme s’est arrêté (code {code}). Détails : {log}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        dialog = Gtk.FileChooserDialog(title="Choisir une application ou un ZIP", action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons("Annuler", Gtk.ResponseType.CANCEL, "Choisir", Gtk.ResponseType.OK)
        response = dialog.run()
        selected = dialog.get_filename()
        dialog.destroy()
        if response != Gtk.ResponseType.OK:
            sys.exit(0)
    else:
        selected = sys.argv[1]
    window = Launcher(Path(selected))
    window.show_all()
    Gtk.main()
