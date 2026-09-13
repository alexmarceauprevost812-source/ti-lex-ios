#!/bin/sh
# Démarre réellement plymouthd sur le serveur X de test et vérifie que le thème
# TI-LEX se charge et dessine. À lancer sous xvfb-run, après avoir installé le
# thème, la mascotte et /etc/plymouth/plymouthd.conf comme le fait l'image.
set -eu

LOG=/tmp/ti-lex-plymouth.log
SHOT=/tmp/ti-lex-plymouth.png
CONSOLE=/tmp/ti-lex-plymouth-console.log
THEME=/usr/share/plymouth/themes/ti-lex
CONF=/etc/plymouth/plymouthd.conf
rm -f "$LOG" "$SHOT" "$CONSOLE"

for file in ti-lex.plymouth ti-lex.script bar.png track.png mascot.png; do
    test -f "$THEME/$file" || { echo "Fichier de thème manquant : $file" >&2; exit 1; }
done

# Un poste de développement garde sa configuration : on n'écrit que si elle manque,
# et on la retire ensuite. plymouthd n'a pas d'option pour choisir un thème.
temporary=""
if [ ! -f "$CONF" ]; then
    mkdir -p /etc/plymouth
    printf '[Daemon]\nTheme=ti-lex\n' > "$CONF"
    temporary=yes
fi
grep -q "^Theme=ti-lex" "$CONF" || {
    echo "$CONF ne sélectionne pas le thème ti-lex." >&2
    exit 1
}

cleanup() {
    plymouth quit >/dev/null 2>&1 || true
    kill "$daemon" 2>/dev/null || true
    test -z "$temporary" || rm -f "$CONF"
}
trap cleanup EXIT

# Sans « splash » sur la ligne de commande noyau, plymouthd refuse le mode graphique ;
# le conteneur d'intégration n'en a pas, d'où la ligne simulée.
plymouthd --debug --debug-file="$LOG" --no-daemon --mode=boot \
    --kernel-command-line="quiet splash" --graphical-boot > "$CONSOLE" 2>&1 &
daemon=$!

# La socket de Plymouth est abstraite : seul un ping dit que le démon écoute.
tries=0
while ! plymouth --ping >/dev/null 2>&1 && [ "$tries" -lt 100 ]; do
    tries=$((tries + 1))
    sleep 0.1
done
plymouth --ping || { cat "$CONSOLE" >&2; echo "plymouthd ne répond pas." >&2; exit 1; }

plymouth --show-splash
sleep 3

python3 - "$SHOT" <<'PY'
import sys
import gi
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk

root = Gdk.get_default_root_window()
width, height = root.get_width(), root.get_height()
shot = Gdk.pixbuf_get_from_window(root, 0, 0, width, height)
if shot is None:
    raise SystemExit("Capture impossible : aucune image renvoyée par X.")
shot.savev(sys.argv[1], "png", [], [])

# La mascotte et la barre sont les seules sources d'orange à l'écran : en trouver
# prouve que le script du thème s'est exécuté et a dessiné quelque chose.
pixels, stride, channels = shot.get_pixels(), shot.get_rowstride(), shot.get_n_channels()
orange = 0
for y in range(0, height, 2):
    row = y * stride
    for x in range(0, width, 2):
        offset = row + x * channels
        red, green, blue = pixels[offset], pixels[offset + 1], pixels[offset + 2]
        if red > 150 and 80 < green < 190 and blue < 110:
            orange += 1
print(f"Capture {width}x{height}, {orange} pixels orange TI-LEX.")
if orange < 50:
    raise SystemExit("Le thème n'a rien dessiné d'orange : mascotte ou barre absente.")
PY

# Plymouth ne vide son fichier de trace qu'en s'arrêtant : lire avant serait vain.
plymouth quit
wait "$daemon" 2>/dev/null || true
cat "$CONSOLE" >> "$LOG"

grep -qi "Loading boot splash theme.*ti-lex" "$LOG" || {
    echo "Le journal ne montre pas le chargement du thème TI-LEX." >&2
    exit 1
}
if grep -i "script error\|failed to parse\|failed to load theme" "$LOG"; then
    echo "Erreurs de thème dans le journal Plymouth ci-dessus." >&2
    exit 1
fi

echo "Thème Plymouth TI-LEX chargé et dessiné ; capture dans $SHOT."
