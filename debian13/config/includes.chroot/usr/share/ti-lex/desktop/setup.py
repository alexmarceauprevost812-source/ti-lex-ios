#!/usr/bin/python3
"""Apply the initial wallpaper once per account after XFCE initializes its monitors."""
import os
from pathlib import Path
import subprocess
import time

WALLPAPER = "/usr/share/ti-lex/branding/desktop.png"
def apply_once(state, attempts=30):
    if state.exists() or not Path(WALLPAPER).is_file():
        return
    for _ in range(attempts):
        try:
            result = subprocess.run(["xfconf-query", "-c", "xfce4-desktop", "-l"],
                                    capture_output=True, text=True, timeout=5)
            props = [p.strip() for p in result.stdout.splitlines()
                     if p.startswith("/backdrop/") and p.endswith("/last-image")]
            if result.returncode == 0 and not props:
                displays = subprocess.run(["xrandr", "--query"], capture_output=True,
                                          text=True, check=True, timeout=5)
                monitors = [line.split()[0] for line in displays.stdout.splitlines()
                            if " connected" in line]
                props = [f"/backdrop/screen0/monitor{name}/workspace0/last-image"
                         for name in monitors]
                for prop in props:
                    subprocess.run(["xfconf-query", "-c", "xfce4-desktop",
                                    "-p", prop, "--create", "--type", "string",
                                    "--set", WALLPAPER], check=True, timeout=5)
            if result.returncode == 0 and props:
                for prop in props:
                    subprocess.run(["xfconf-query", "-c", "xfce4-desktop",
                                    "-p", prop, "-s", WALLPAPER], check=True, timeout=5)
                state.parent.mkdir(parents=True, exist_ok=True)
                state.write_text("1\n", encoding="utf-8")
                return
        except (OSError, subprocess.SubprocessError):
            pass
        time.sleep(2)
if __name__ == "__main__":
    state_root = Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local/state")
    apply_once(state_root / "ti-lex/desktop-v1")
