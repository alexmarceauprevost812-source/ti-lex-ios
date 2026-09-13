#!/bin/sh
set -eu
trap 'plymouth quit || true' EXIT
plymouthd --debug --debug-file=/tmp/ti-lex-plymouth.log --mode=boot --kernel-command-line="splash"
plymouth show-splash
sleep 3
python3 - <<'PY'
import gi
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk
root = Gdk.get_default_root_window()
pixels = Gdk.pixbuf_get_from_window(root,0,0,root.get_width(),root.get_height())
assert pixels is not None
pixels.savev("/tmp/ti-lex-plymouth.png","png",[],[])
data = pixels.get_pixels()
channels = pixels.get_n_channels()
orange = green = 0
for y in range(pixels.get_height()):
    for x in range(pixels.get_width()):
        index = y*pixels.get_rowstride()+x*channels
        r,g,b = data[index:index+3]
        orange += r>80 and r>g*1.2 and g>b*1.15
        green += g>50 and g>r*1.4 and g>b*1.15
assert orange>50 and green>50, (orange,green)
print("Plymouth: mascot/orange and Matrix/green pixels rendered.")
PY
