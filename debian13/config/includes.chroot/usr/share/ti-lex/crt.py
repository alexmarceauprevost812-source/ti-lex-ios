"""Allumage et extinction « vieille télévision » des fenêtres TI-LEX.

X11 et xfwm4 n'animent pas la géométrie des fenêtres, et redimensionner une fenêtre
GTK ne descend jamais sous la taille minimale de son contenu : l'effet ne peut donc
pas venir du gestionnaire de fenêtres. Il est peint par la fenêtre elle-même. Un
gestionnaire « draw » comprime le contenu vers une ligne centrale avant que GTK ne
dessine les enfants ; un second, exécuté après, pose le voile lumineux du tube.

L'animation ne change rien à la disposition : si elle est coupée, la fenêtre reste
simplement normale, et la fermeture garde son chemin habituel.
"""
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib

FRAME = 16  # millisecondes, environ 60 images par seconde
NOIR = (0.031, 0.031, 0.043)


class Tube:
    """Effet d'une fenêtre. L'appelant garde l'instance aussi longtemps que la fenêtre."""

    def __init__(self, window):
        self.window = window
        self.scale = 1.0   # 1 : image entière ; proche de 0 : ligne d'extinction
        self.flash = 0.0   # voile blanc du tube
        self.active = False
        self.running = False
        self.timer = None
        window.connect("destroy", self.cancel)
        window.connect("draw", self._compress)
        window.connect_after("draw", self._veil)

    def compress(self, context, height):
        """Fond noir, puis compression du dessin vers la ligne centrale du tube."""
        context.set_source_rgb(*NOIR)
        context.paint()
        context.translate(0, height / 2)
        context.scale(1.0, max(self.scale, 0.004))
        context.translate(0, -height / 2)

    def veil(self, context, width, height):
        """Voile lumineux du tube, par-dessus le contenu déjà dessiné."""
        context.identity_matrix()
        context.set_source_rgba(1, 1, 1, min(0.8, self.flash))
        context.rectangle(0, 0, width, height)
        context.fill()

    def _compress(self, widget, context):
        if self.active:
            self.compress(context, widget.get_allocated_height())
        return False

    def _veil(self, widget, context):
        if self.active and self.flash > 0.01:
            self.veil(context, widget.get_allocated_width(), widget.get_allocated_height())
        return False

    def _play(self, duration, step, done=None):
        if self.running:
            self.cancel()
        self.running = True
        self.active = True
        frames = max(1, int(duration / FRAME))
        state = {"count": 0}

        def tick():
            state["count"] += 1
            step(min(1.0, state["count"] / frames))
            self.window.queue_draw()
            if state["count"] < frames:
                return True
            self.active = False
            self.running = False
            self.timer = None
            self.window.queue_draw()
            if done:
                done()
            return False

        self.timer = GLib.timeout_add(FRAME, tick)

    def cancel(self, *_):
        if self.timer is not None:
            GLib.source_remove(self.timer)
            self.timer = None
        self.running = False
        self.active = False

    def turn_on(self, duration=420):
        """La ligne s'ouvre vers le haut et le bas, le voile s'efface."""
        self.scale, self.flash = 0.004, 0.75
        self.active = True
        self.window.queue_draw()

        def step(progress):
            self.scale = min(1.0, 0.004 + progress ** 0.45)
            self.flash = max(0.0, 0.75 - progress * 0.95)

        self._play(duration, step)

    def turn_off(self, done, duration=300):
        """L'image se referme sur une ligne lumineuse, puis « done » ferme la fenêtre."""
        def step(progress):
            self.scale = max(0.004, (1 - progress) ** 2)
            self.flash = min(0.8, progress * progress * 1.1)

        self._play(duration, step, done)
        if not self.running and done:   # animation refusée : la fermeture doit avoir lieu
            done()
