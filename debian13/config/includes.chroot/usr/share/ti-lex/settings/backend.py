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
    "Accessibilité": ("xfce4-accessibility-settings",),
    "Notifications": ("xfce4-notifyd-config",),
    "Gestionnaire de fenêtres": ("xfwm4-settings",),
    "Réglages du panneau": ("xfce4-panel", "--preferences"),
    "Applications au démarrage": ("xfce4-session-settings",),
    "Tous les paramètres XFCE": ("xfce4-settings-manager",),
    "Gestionnaire de paquets": ("synaptic-pkexec",),
    "Mises à jour disponibles": ("xfce4-terminal", "--disable-server", "--hold", "--execute", "apt", "list", "--upgradable"),
    "Clés et mots de passe": ("seahorse",),
    "Applications Flatpak": ("xfce4-terminal", "--disable-server", "--hold", "--execute", "flatpak", "list"),
    "Machines virtuelles": ("virt-manager",),
    "Conteneurs": ("xfce4-terminal", "--disable-server", "--hold", "--execute", "podman", "ps", "-a"),
    "Rechercher des fichiers": ("catfish",),
    "Date et heure": ("xfce4-terminal", "--disable-server", "--hold", "--execute", "timedatectl", "status"),
    "Températures et capteurs": ("xfce4-terminal", "--disable-server", "--hold", "--execute", "sensors"),
    "Matériel détecté": ("xfce4-terminal", "--disable-server", "--hold", "--execute", "inxi", "-Fxz"),
    "Terminal TI-LEX": ("ti-lex-terminal",),
    "Ouvrir une application": ("ti-lex-open",),
    "Préférences du terminal": ("xfce4-terminal", "--preferences"),
    "Guide des commandes": ("xfce4-terminal", "--disable-server", "--hold", "--execute", "tilex", "aide"),
    "Sessions tmux": ("xfce4-terminal", "--disable-server", "--execute", "tmux", "new-session", "-A", "-s", "ti-lex"),
    "Python": ("xfce4-terminal", "--disable-server", "--execute", "python3"),
    "Éditeur de texte": ("mousepad",),
    "Fichiers": ("thunar",),
    "Archives": ("xarchiver",),
    "Sauvegardes": ("deja-dup",),
    "Espace disque": ("xfce4-terminal", "--disable-server", "--execute", "ncdu"),
    "Capture d’écran": ("xfce4-screenshooter",),
    "Informations système": ("xfce4-terminal", "--disable-server", "--hold", "--execute", "tilex", "systeme"),
    "Journaux système": ("xfce4-terminal", "--disable-server", "--hold", "--execute", "tilex", "journaux"),
}

def available(command):
    if not command or shutil.which(command[0]) is None:
        return False
    if command[0] == "xfce4-terminal" and "--execute" in command:
        index = command.index("--execute") + 1
        return index < len(command) and shutil.which(command[index]) is not None
    return True

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
