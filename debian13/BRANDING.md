# Images TI-LEX
Déposer les PNG dans :
`debian13/config/includes.chroot/usr/share/ti-lex/branding/`

- `login.png` : fond de connexion. Incorporer le logo dans cette image.
- `avatar.png` : avatar de connexion par défaut.

Le hook active automatiquement ces deux fichiers s'ils existent, sinon LightDM
conserve son fond uni. Garder la zone centrale du fond sobre pour lire le formulaire.
Les PNG doivent être de vraies images lisibles, non des liens symboliques.

Le thème actuel est Adwaita-dark (provisoire). La palette orange, les icônes,
le fond XFCE multi-écrans, le logo du menu de démarrage et l'animation vieille TV
nécessitent encore leur intégration et leurs tests : ajouter une image ne suffit
pas pour ces éléments. Ne pas modifier les fichiers PAM d'authentification.
