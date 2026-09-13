#!/usr/bin/python3
"""Apply the initial wallpaper once per account after XFCE initializes its monitors."""
import os
from pathlib import Path
import subprocess
import time

WALLPAPER = "/usr/share/ti-lex/branding/desktop.png"
INSTALLER = "/usr/share/applications/ti-lex-install.desktop"
# p=8 : bord droit, centré verticalement, dans l'énumération de position XFCE.
DOCK_POSITION = "p=8;x=0;y=0"

def move_dock(state):
    """Colle le dock au bord droit, à la verticale.

    La barre du haut n'est jamais touchée : s'il n'existe qu'un seul panneau,
    le déplacer priverait l'utilisateur de son menu, donc on ne fait rien.
    """
    if state.exists():
        return
    try:
        listing = subprocess.run(["xfconf-query", "-c", "xfce4-panel", "-p", "/panels", "-l"],
                                 capture_output=True, text=True, timeout=5)
        if listing.returncode != 0:
            return
        panels = sorted({line.strip().split("/")[2] for line in listing.stdout.splitlines()
                         if line.strip().startswith("/panels/panel-") and len(line.strip().split("/")) > 2})
        if len(panels) < 2:
            return
        dock = panels[-1]
        for name, kind, value in ((f"/panels/{dock}/mode", "int", "1"),
                                  (f"/panels/{dock}/position", "string", DOCK_POSITION)):
            subprocess.run(["xfconf-query", "-c", "xfce4-panel", "-p", name,
                            "--create", "--type", kind, "--set", value],
                           check=True, timeout=5)
        state.parent.mkdir(parents=True, exist_ok=True)
        state.write_text("1\n", encoding="utf-8")
    except (OSError, subprocess.SubprocessError):
        pass


def offer_shortcuts(state):
    """Install initial shortcuts once, preserving existing user files."""
    if state.exists():
        return
    try:
        result = subprocess.run(["xdg-user-dir", "DESKTOP"], capture_output=True,
                                text=True, timeout=5, check=True)
        directory = Path(result.stdout.strip())
        if not result.stdout.strip() or not directory.is_absolute() or not directory.is_dir():
            return
        for name in ("thunar.desktop", "ti-lex-terminal.desktop",
                     "ti-lex-settings.desktop", "ti-lex-open.desktop"):
            source = Path("/usr/share/applications") / name
            if not source.is_file():
                return
            target = directory / name
            try:
                with target.open("x", encoding="utf-8") as stream:
                    stream.write(source.read_text(encoding="utf-8"))
                target.chmod(0o755)
            except FileExistsError:
                continue
        state.parent.mkdir(parents=True, exist_ok=True)
        state.write_text("1\n", encoding="utf-8")
    except (OSError, subprocess.SubprocessError):
        pass


def offer_installer(state):
    """Copie le lanceur d'installation sur le bureau, en session live seulement.
    Le système installé n'a plus Calamares : rien n'est copié, aucune entrée morte."""
    if state.exists() or not Path("/usr/bin/calamares").is_file() or not Path(INSTALLER).is_file():
        return
    try:
        result = subprocess.run(["xdg-user-dir", "DESKTOP"], capture_output=True,
                                text=True, timeout=5)
        desktop = Path(result.stdout.strip()) if result.returncode == 0 and result.stdout.strip() else None
        if desktop is None or not desktop.is_dir():
            return
        target = desktop / "ti-lex-install.desktop"
        target.write_text(Path(INSTALLER).read_text(encoding="utf-8"), encoding="utf-8")
        target.chmod(0o755)
        state.parent.mkdir(parents=True, exist_ok=True)
        state.write_text("1\n", encoding="utf-8")
    except (OSError, subprocess.SubprocessError):
        pass

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
    offer_installer(state_root / "ti-lex/installer-v1")
    offer_shortcuts(state_root / "ti-lex/shortcuts-v1")
    move_dock(state_root / "ti-lex/dock-v1")
