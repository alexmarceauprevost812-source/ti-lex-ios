"""Native tools only; no shell, credentials, sudo or policy bypass."""
import os
import shutil
import subprocess

TOOLS = {
    "Choisir un réseau Wi-Fi": ("xfce4-terminal", "--disable-server", "--execute", "nmtui-connect"),
    "Profils réseau / VPN": ("nm-connection-editor",),
    "Appareils Bluetooth": ("blueman-manager",),
    "Son et microphones": ("pavucontrol",),
    "Webcam": ("cheese",),
    "Enregistrer le microphone": ("gnome-sound-recorder",),
    "Imprimantes": ("system-config-printer",),
    "Scanner": ("simple-scan",),
    "Écrans": ("xfce4-display-settings",),
    "Clavier": ("xfce4-keyboard-settings",),
    "Souris et pavé tactile": ("xfce4-mouse-settings",),
    "Apparence": ("xfce4-appearance-settings",),
    "Fond du bureau": ("xfdesktop-settings",),
    "Alimentation": ("xfce4-power-manager-settings",),
    "Disques": ("gnome-disks",),
    "Pare-feu": ("gufw",),
    "Processus": ("xfce4-taskmanager",),
    "Tous les paramètres XFCE": ("xfce4-settings-manager",),
}

def available(command):
    return shutil.which(command[0]) is not None and (
        command[0] != "xfce4-terminal" or shutil.which("nmtui-connect") is not None)

def query(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True,
                                timeout=6, env={**os.environ, "LC_ALL": "C"})
        return result.stdout.strip() if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None

def wifi_state():
    devices = query(["nmcli", "-t", "-f", "TYPE", "device"])
    if devices is None:
        return "unknown", "État indisponible"
    if "wifi" not in devices.splitlines():
        return "unknown", "Aucun adaptateur Wi-Fi détecté"
    radio = query(["nmcli", "radio", "wifi"])
    if radio == "enabled":
        return "on", "Activé — radio Wi-Fi (pas une preuve de connexion)"
    if radio == "disabled":
        return "off", "Désactivé — radio Wi-Fi"
    return "unknown", "État indisponible"

def bluetooth_state():
    info = query(["bluetoothctl", "show"])
    if info is None or "Controller " not in info:
        return "unknown", "Adaptateur absent ou service indisponible"
    if "Powered: yes" in info:
        return "on", "Activé — adaptateur Bluetooth par défaut"
    if "Powered: no" in info:
        return "off", "Désactivé — adaptateur Bluetooth par défaut"
    return "unknown", "État indisponible"
