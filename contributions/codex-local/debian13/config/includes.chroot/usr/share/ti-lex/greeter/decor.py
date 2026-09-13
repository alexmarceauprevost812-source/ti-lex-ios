#!/usr/bin/python3
"""Passive decoration only. No authentication, keyboard, mouse or account access."""
import configparser
from pathlib import Path
import time
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
import cairo

ASSET = "/usr/share/ti-lex/branding/mascot.png"
def zones(x, y, width, height):
    gap = min(width, max(520, int(width * .46)))
    side = max(0, (width - gap) // 2)
    size = max(64, min(240, int(height * .30)))
    top = min(48, max(26, int(height * .06)))
    result = [("mascot", x + (width-size)//2, y+top, size, size)]
    if side >= 36:
        result += [("rain", x, y+32, side, height-32),
                   ("rain", x+width-side, y+32, side, height-32)]
    return result

class Decoration(Gtk.Window):
    def __init__(self, kind, x, y, width, height, animate=True):
        super().__init__(type=Gtk.WindowType.POPUP)
        self.kind, self.animate = kind, animate
        self.started = time.monotonic()
        self.set_decorated(False)
        self.set_accept_focus(False)
        self.set_focus_on_map(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_resizable(False)
        self.move(x, y)
        self.set_default_size(width, height)
        self.connect("realize", self.realize_passive)
        self.connect("draw", self.draw_scene)
        self.timer = None
        if kind == "mascot":
            self.mascot = GdkPixbuf.Pixbuf.new_from_file_at_scale(ASSET, width, height, True)
        self.show_all()
        if animate and kind == "rain":
            self.timer = GLib.timeout_add(80, self.tick)
        self.connect("destroy", self.cleanup)

    def realize_passive(self, *_):
        # An empty X11 input region lets every pointer event reach the stock greeter.
        self.get_window().input_shape_combine_region(cairo.Region(), 0, 0)
        self.get_window().set_accept_focus(False)

    def tick(self):
        self.queue_draw()
        return True

    def cleanup(self, *_):
        if self.timer is not None:
            GLib.source_remove(self.timer)
            self.timer = None

    def draw_scene(self, widget, ctx):
        w, h = self.get_allocated_width(), self.get_allocated_height()
        ctx.set_source_rgb(0, 0, 0)
        ctx.paint()
        if self.kind == "mascot":
            Gdk.cairo_set_source_pixbuf(ctx, self.mascot,
                (w-self.mascot.get_width())/2, (h-self.mascot.get_height())/2)
            ctx.paint()
            return False
        elapsed = time.monotonic()-self.started if self.animate else 0
        ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(16)
        alphabet = "01TI-LEX{}<>/+=*"
        for column, x in enumerate(range(10, w, 25)):
            head = (elapsed*(34+(column%7)*7)+column*97) % (h+260)
            for row in range(12):
                yy = head-row*21
                if not 0 < yy < h:
                    continue
                alpha = (1-row/12)*.75
                ctx.set_source_rgba(.58 if row == 0 else .05, 1 if row == 0 else .74, .55 if row == 0 else .27, alpha)
                ctx.move_to(x, yy)
                ctx.show_text(alphabet[(column*3+row+int(elapsed*2))%len(alphabet)])
        return False

def main():
    config = configparser.ConfigParser()
    config.read("/etc/ti-lex/animation.conf")
    animate = config.getboolean("animation", "enabled", fallback=True)
    display = Gdk.Display.get_default()
    windows = []
    for i in range(display.get_n_monitors()):
        rect = display.get_monitor(i).get_geometry()
        for args in zones(rect.x, rect.y, rect.width, rect.height):
            windows.append(Decoration(*args, animate=animate))
    # Stock greeter maps its background at startup; raise only our passive,
    # spatially separate areas, never the central login form.
    def lift():
        for window in windows:
            window.get_window().raise_()
        return True
    GLib.timeout_add_seconds(1, lift)
    Gtk.main()
if __name__ == "__main__":
    main()
