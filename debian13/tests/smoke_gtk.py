"""Instantiate actual GTK windows in Debian/Xvfb, without launching downloaded code."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import time
import cairo
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf

ROOT = Path(__file__).resolve().parents[1] / "config/includes.chroot/usr/share/ti-lex"
for icon in (ROOT / "branding").glob("*.svg"):
    GdkPixbuf.Pixbuf.new_from_file(str(icon))
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

# L'effet « vieille télévision » se peint lui-même : on exécute vraiment ses
# gestionnaires de dessin dans un contexte cairo, puis on vérifie que l'allumage
# se termine et que l'extinction rappelle bien la fermeture de la fenêtre.
def settle(condition, seconds=4):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)
        if condition():
            return True
        time.sleep(.01)
    return False

tube = window.tube

# Peinture : état figé au milieu de l'effet, le voile doit marquer la surface.
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 320, 220)
context = cairo.Context(surface)
tube.scale, tube.flash = .25, .7
tube.compress(context, 220)
tube.veil(context, 320, 220)
surface.flush()
pixels = bytes(surface.get_data())
# Blanc à 70 % sur le noir du tube : environ 181, bien au-dessus du fond.
clair = sum(1 for i in range(0, len(pixels) - 4, 4)
            if pixels[i] > 150 and pixels[i + 1] > 150 and pixels[i + 2] > 150)
assert clair > 320 * 220 * 0.9, f"le voile du tube n'a pas été peint ({clair} pixels clairs)"
tube.scale, tube.flash = 1.0, 0.0

# Minuterie : l'allumage se termine, l'extinction rappelle la fermeture.
tube.turn_on(duration=96)
assert tube.active, "l'allumage n'a pas démarré"
assert settle(lambda: not tube.active and not tube.running), "l'allumage ne s'est pas terminé"

closed = []
tube.turn_off(lambda: closed.append("fermé"), duration=96)
assert settle(lambda: closed), "l'extinction n'a jamais rappelé la fermeture"
print("Settings and launcher windows initialized; CRT power-on and power-off ran; no application executed.")
