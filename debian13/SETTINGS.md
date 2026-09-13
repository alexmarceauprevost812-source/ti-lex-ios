# Paramètres TI-LEX Pro

Le centre de contrôle propose un accueil et 13 pages : Wi-Fi et réseau,
Bluetooth, son et caméra, écrans et périphériques, apparence et bureau,
applications, fichiers et sauvegardes, disques et stockage, sécurité,
terminal et développement, virtualisation, système et diagnostic,
session et installation. La barre latérale et les cartes de l'accueil
ouvrent ces pages. La recherche parcourt toutes les catégories et ignore
les accents et la casse ; effacer la recherche revient à la page précédente.

Chaque outil du catalogue possède une page et ouvre une application native.
Les outils absents restent visibles avec la mention « Outil non installé ».
Ce catalogue couvre les outils intégrés au projet, pas tous les logiciels
disponibles dans les dépôts Linux. Les icônes utilisent le thème TI-LEX et
son thème de repli ; la planche utilisateur reste une référence non découpée.
Lanceur : menu Applications → Paramètres → Paramètres TI-LEX Pro.
Commande : python3 /usr/share/ti-lex/settings/app.py (sans sudo).

L'interface GTK propose des boutons orange arrondis, un fond noir et les états
Wi-Fi/Bluetooth lus réellement. Vert = radio active, rouge = inactive,
blanc = état inconnu ou matériel absent. Radio active ne signifie pas connecté.

Wi-Fi : ouvre nmtui-connect dans le terminal XFCE pour choisir un réseau et
saisir son mot de passe dans l'outil NetworkManager. Profils/VPN :
nm-connection-editor. Activer/désactiver le Wi-Fi via l'applet réseau XFCE.
Bluetooth : Blueman gère alimentation, découverte, appairage et suppression.
Son : pavucontrol. Les autres boutons ouvrent leurs panneaux XFCE ou système.
Aucun mot de passe n'est traité par notre application, aucune règle Polkit
n'est relâchée, aucun service distant n'est activé. Les privilèges sont
demandés par les outils natifs lorsqu'ils en ont besoin.

Les fenêtres externes conservent leur propre thème. L'arrondi de toute la
surface des fenêtres dépend du compositeur; ce module ne le garantit pas.

## À tester en VM puis sur matériel
- Ouvrir chaque panneau et vérifier les messages en cas d'outil manquant.
- Wi-Fi : réseau protégé, mauvais mot de passe, reconnexion et coupure radio.
- Bluetooth : absence d'adaptateur, appareil détecté, appairage et déconnexion.
- Vérifier états après changement externe (actualisation toutes les 10 s).
- Refus d'autorisation, indisponibilité des services, session utilisateur non root.
- Stockage : ouvrir seulement, ne pas formater pour le test.
- Vérifier démarrage Bluetooth et agent d'authentification de la session XFCE.
Tests matériels et test visuel GTK non encore effectués.

Micro : pavucontrol, onglet Périphériques d’entrée : niveau, sélection, sourdine.
Enregistrement audio : GNOME Sound Recorder; webcam : Cheese; scanner : Simple Scan;
imprimantes : system-config-printer. Aucune capture automatique au démarrage.

Terminal et développement : terminal TI-LEX, préférences XFCE Terminal, guide
des commandes, sessions tmux, Python et Mousepad.
Fichiers et diagnostic : lanceur d'applications TI-LEX, Thunar, Xarchiver,
Déjà Dup, ncdu, capture d'écran, informations système et journaux.
Ces outils sont ajoutés aux listes de paquets de la future image.
