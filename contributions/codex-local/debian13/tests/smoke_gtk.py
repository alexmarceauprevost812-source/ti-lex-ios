"""Instantiate actual GTK windows in Debian/Xvfb, without launching downloaded code."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import time
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
    print("Settings and launcher windows initialized; no application executed.")

# Validate the actual passive greeter decoration and its drawing code.
spec = importlib.util.spec_from_file_location("decor", ROOT / "greeter/decor.py")
decor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(decor)
import cairo
for width, height in [(1280,720),(1920,1080),(640,480)]:
    for kind, x, y, w, h in decor.zones(0,0,width,height):
        assert x >= 0 and y >= 0 and x+w <= width and y+h <= height
        ornament = decor.Decoration(kind,x,y,w,h)
        assert not ornament.get_accept_focus()
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,w,h)
        ornament.draw_scene(ornament,cairo.Context(surface))
        ornament.destroy()
print("Mascot and Matrix drawn; decoration windows do not accept focus.")
