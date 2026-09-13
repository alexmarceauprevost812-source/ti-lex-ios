# Ouvrir une application sans terminal

Dans le gestionnaire de fichiers Thunar, clic droit sur un ZIP, une AppImage,
un script .sh/.py ou un paquet .deb → **Ouvrir avec TI-LEX**.
Sélectionner le programme si le ZIP en contient plusieurs, puis **Ouvrir l’application**.
L'entrée est aussi disponible dans les paramètres et dans le menu Applications.

Le ZIP est extrait dans ~/.local/share/ti-lex/apps/app-* (ou XDG_DATA_HOME).
Le fichier téléchargé est conservé. Aucun programme ne s'exécute pendant l'extraction.
Les chemins sortants, liens symboliques, entrées spéciales et archives chiffrées
sont refusés; limite de 2 Gio décompressés et 20 000 entrées.
Une nouvelle extraction crée un dossier neuf. Les anciens dossiers peuvent être
supprimés dans le gestionnaire de fichiers lorsque l'application est fermée.

Formats : programmes ELF Linux, AppImage, Bash, Python et .deb via GDebi.
Les fichiers .exe Windows, .desktop, archives tar et applications dont les ZIP
exigent des liens symboliques ne sont pas gérés par ce lanceur.
La compatibilité CPU, les bibliothèques, FUSE et les dépendances propres au
programme ne peuvent pas être corrigés automatiquement. Aucun « sans défaut »
universel n'est garanti. Le lanceur ne constitue pas un bac à sable.
Les scripts interactifs qui exigent un terminal doivent utiliser un terminal.

Les sorties du dernier programme sont dans ~/.local/state/ti-lex/application.log.
Ce fichier est local, privé et remplacé au lancement suivant; il n'est pas envoyé.
Les modifications de droits concernent seulement l'exécution par le propriétaire.
GDebi demande lui-même l'autorisation d'installation quand nécessaire.
Les fichiers ZIP restent ouverts par le gestionnaire d'archives par défaut :
l'action TI-LEX est accessible au clic droit.

Les tests automatisés couvrent extraction, sélection, formats rejetés et limites.
L'intégration du menu Thunar et le lancement réel restent à tester dans Debian XFCE.
