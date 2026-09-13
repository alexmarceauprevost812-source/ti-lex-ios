# Bureau TI-LEX PRO

Après la connexion, un accueil plein écran reprend le fond noir et orange,
l'avatar, « Bienvenue chez vous » et le bouton « Entrer dans le bureau ».
Le bouton, Entrée lorsqu'il a le focus, ou Échap ferment cet accueil.
LightDM continue de gérer l'authentification. L'accueil peut être désactivé
dans les applications au démarrage XFCE (Bienvenue TI-LEX PRO).

L'accueil, les paramètres et le lanceur TI-LEX s'ouvrent depuis une ligne
lumineuse et se referment avec un effet de tube cathodique. Une fermeture
demandée pendant l'ouverture interrompt l'animation puis ferme la fenêtre.
Cet effet est propre aux fenêtres GTK TI-LEX ; il ne modifie pas les fenêtres
des applications externes ni le terminal XFCE. Un effet global nécessiterait
une prise en charge par le compositeur du bureau.

Les nouveaux comptes XFCE reçoivent une barre supérieure noire avec menu
TI-LEX PRO, fenêtres ouvertes, zone de notification réseau/Bluetooth,
horloge et actions de session. Un dock vertical à droite ouvre les fichiers,
le terminal, les paramètres et le lanceur d'applications.

Le premier démarrage ajoute ces quatre raccourcis au dossier Bureau sans
remplacer les fichiers existants. Le fond livré est `branding/desktop.png`.
Les panneaux ont des accents orange et un indicateur de focus vert lime.

La capture de référence représente l'aperçu web : la pluie de caractères
animée et le texte décoratif ne sont pas encore reproduits sur le bureau XFCE.
La base système demeure Debian 13. La configuration des panneaux dans
`/etc/skel` concerne les nouveaux comptes, pas les bureaux déjà personnalisés.

Validation restante dans une session XFCE : position des deux panneaux,
ouverture des quatre applications, notifications NetworkManager/Blueman,
lisibilité et placement des raccourcis sur le côté gauche.
