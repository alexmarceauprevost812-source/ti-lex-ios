"""Instantiate actual GTK windows in Debian/Xvfb, without launching downloaded code."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import time
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

ROOT = Path(__file__).resolve().parents[1] / "config/includes.chroot/usr/share/ti-lex"
def load(name, folder):
    sys.path.insert(0, str(folder))
    spec = importlib.util.spec_from_file_location(name, folder / "app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
settings = load("settings_app", ROOT / "settings")
provider = Gtk.CssProvider()
provider.load_from_data(settings.CSS)
Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
window = settings.Settings()
window.show_all()
window.connect("destroy", lambda *_: None)
launcher = load("launcher_app", ROOT / "launcher")
with tempfile.TemporaryDirectory() as folder:
    program = Path(folder) / "example.py"
    program.write_text("print('not executed')")
    opener = launcher.Launcher(program)
    opener.show_all()
    deadline = time.monotonic() + 3
    while time.monotonic() < deadline:
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)
        if opener.run_button.get_sensitive():
            break
        time.sleep(.05)
    assert opener.paths == [program.resolve()], opener.paths
    assert opener.run_button.get_sensitive()
    print("Settings and launcher windows initialized; no application executed.")
