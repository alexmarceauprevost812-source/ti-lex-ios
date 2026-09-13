"""Pages of the native control center. Each tool refers to backend.TOOLS."""
import unicodedata

PAGES = [
    ("Wi-Fi et réseau", "ti-lex-network", "Connexion Internet, réseaux enregistrés et VPN.",
     ["Choisir un réseau Wi-Fi", "Profils réseau / VPN"]),
    ("Bluetooth", "bluetooth", "Associez et gérez vos appareils Bluetooth.",
     ["Appareils Bluetooth"]),
    ("Son et caméra", "audio-volume-high", "Haut-parleurs, microphones, enregistrement et webcam.",
     ["Son et microphones", "Enregistrer le microphone", "Webcam"]),
    ("Écrans et périphériques", "video-display", "Affichage, clavier, souris, impression et numérisation.",
     ["Écrans", "Clavier", "Souris et pavé tactile", "Imprimantes", "Scanner"]),
    ("Apparence et bureau", "ti-lex-settings", "Personnalisez votre espace TI-LEX PRO.",
     ["Apparence", "Fond du bureau", "Gestionnaire de fenêtres", "Réglages du panneau",
      "Notifications", "Accessibilité"]),
    ("Applications", "system-software-install", "Ouvrez vos applications et gérez les logiciels installés.",
     ["Navigateur Web", "Ouvrir une application", "Gestionnaire de paquets",
      "Mises à jour disponibles", "Applications Flatpak", "Applications au démarrage"]),
    ("Fichiers et sauvegardes", "ti-lex-files", "Documents, archives, recherche et sauvegardes.",
     ["Fichiers", "Rechercher des fichiers", "Archives", "Sauvegardes", "Capture d’écran"]),
    ("Disques et stockage", "drive-harddisk", "Consultez vos volumes et leur occupation.",
     ["Disques", "Formater un disque ou une clé USB", "Espace disque"]),
    ("Sécurité", "ti-lex-security", "Pare-feu, clés et mots de passe de votre session.",
     ["Pare-feu", "Clés et mots de passe"]),
    ("Terminal et développement", "ti-lex-terminal", "Terminal, commandes, Python et édition de texte.",
     ["Terminal TI-LEX", "Préférences du terminal", "Guide des commandes", "Sessions tmux",
      "Python", "Éditeur de texte", "Éditeur Geany", "Git graphique", "Comparer des fichiers"]),
    ("Virtualisation", "computer", "Machines virtuelles et consultation des conteneurs Podman.",
     ["Machines virtuelles", "Conteneurs"]),
    ("Système et diagnostic", "ti-lex-system", "Matériel, processus, capteurs et journaux.",
     ["Informations système", "Matériel détecté", "Processus", "Températures et capteurs",
      "Journaux système", "Tous les paramètres XFCE"]),
    ("Session et installation", "system-shutdown", "Alimentation, date, session et installation en mode live.",
     ["Alimentation", "Date et heure", "Fermer la session / alimentation", "Installer TI-LEX Pro"]),
]


def normalize(text):
    return "".join(c for c in unicodedata.normalize("NFKD", text.casefold())
                   if not unicodedata.combining(c))


def search_tools(query):
    words = normalize(query).split()
    return [(name, icon, tool) for name, icon, description, tools in PAGES for tool in tools
            if all(word in normalize(" ".join((name, description, tool))) for word in words)]
