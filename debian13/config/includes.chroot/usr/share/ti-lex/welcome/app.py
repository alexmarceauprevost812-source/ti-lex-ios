#!/usr/bin/python3
"""Post-login welcome screen; authentication remains with LightDM."""
from pathlib import Path
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

BRANDING = Path(__file__).resolve().parent.parent / "branding"
CSS = """
#welcome { background-color: #08080b; background-image: url('%s');
           background-size: cover; background-position: center; color: white; }
#welcome label { color: #ffffff; }
#welcome .eyebrow { color: #ff8a24; font-size: 12px; font-weight: bold; }
#welcome .brand { font-size: 40px; font-weight: normal; }
#welcome .subtitle { color: #b0b0b9; font-size: 14px; }
#welcome button { background-image: none; background-color: #ff8a24;
                  border: none; border-radius: 10px; padding: 13px 22px; }
#welcome button label { color: #08080b; font-weight: bold; }
#welcome button:hover { background-color: #ffa94c; }
#welcome button:focus { outline: 2px solid #b4ff39; outline-offset: 4px; }
""" % (BRANDING / "login.png").as_uri()


class Welcome(Gtk.Window):
    def __init__(self):
        super().__init__(title="Bienvenue — TI-LEX PRO")
        self.set_name("welcome")
        self.set_default_size(1000, 700)
        self.connect("destroy", lambda *_: Gtk.main_quit())
        self.connect("key-press-event", self.on_key)
        self.fullscreen()
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        content.set_halign(Gtk.Align.CENTER)
        content.set_valign(Gtk.Align.CENTER)
        content.set_margin_start(24)
        content.set_margin_end(24)
        self.add(content)
        avatar = Gtk.Image()
        try:
            from gi.repository import GdkPixbuf
            avatar.set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_scale(
                str(BRANDING / "avatar.svg"), 108, 108, True))
        except GLib.Error:
            avatar.set_from_icon_name("avatar-default", Gtk.IconSize.DIALOG)
        content.pack_start(avatar, False, False, 0)
        for text, style in (("BIENVENUE CHEZ VOUS", "eyebrow"),
                            ("TI-LEX PRO", "brand"),
                            ("Votre espace. Vos outils.", "subtitle")):
            label = Gtk.Label(label=text)
            label.get_style_context().add_class(style)
            content.pack_start(label, False, False, 0)
        enter = Gtk.Button(label="Entrer dans le bureau →")
        enter.set_halign(Gtk.Align.CENTER)
        enter.connect("clicked", lambda *_: self.destroy())
        content.pack_start(enter, False, False, 12)
        self.enter_button = enter

    def on_key(self, _window, event):
        if event.keyval == Gdk.KEY_Escape:
            self.destroy()
            return True
        return False


if __name__ == "__main__":
    provider = Gtk.CssProvider()
    provider.load_from_data(CSS.encode())
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider,
                                             Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    window = Welcome()
    window.show_all()
    window.enter_button.grab_focus()
    Gtk.main()
