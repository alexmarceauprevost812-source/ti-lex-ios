# Paramètres TI-LEX Pro
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
