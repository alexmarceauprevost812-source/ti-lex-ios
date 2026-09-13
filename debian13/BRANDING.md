# Identité visuelle TI-LEX Pro

Les fichiers sont intégrés sous /usr/share/ti-lex/branding dans la future image.
- desktop.png : fond du bureau noir, ruban orange, accent vert et texture CRT discrète.
- login.png : fond de connexion avec centre dégagé pour le formulaire LightDM.
- logo.svg, avatar.svg, terminal.svg, settings.svg, tools.svg, folder.svg :
  six éléments vectoriels cohérents et redimensionnables.
- mascot.svg et mascot.png : téléviseur CRT souriant, source vectorielle et rendu
  512 x 512 utilisé par l'écran de démarrage.
- file-tools.png : planche de référence 1234 x 1274 des 49 types de fichiers et
  outils, d'où sont tirées les tuiles vectorielles du thème d'icônes. Le système
  n'utilise pas cette image : elle documente l'intention, les icônes servies étant
  les SVG, nets à toute taille.

Le hook LightDM choisit login.png et l'avatar. Le script de première session XFCE
applique desktop.png aux propriétés d'écran présentes, puis conserve un marqueur
dans ~/.local/state/ti-lex : les choix de fond ultérieurs sont conservés.
Les nouveaux écrans ajoutés après cette initialisation se règlent dans Fond du bureau.
Les accents GTK 3 complètent Adwaita-dark. Les applications GTK 4 et Qt gardent
leurs thèmes natifs. Les icônes sont utilisées par les lanceurs TI-LEX; il ne
s'agit pas du remplacement de toutes les icônes des applications Linux.

Deux fonds PNG générés avec l'outil de génération d'images intégré.
Prompts complets : IMAGE-PROMPTS.md. Icônes SVG créées dans le dépôt.
Dimensions réelles des PNG : 1672 × 941; pas de revendication de résolution 4K.

Le menu d'amorçage BIOS/UEFI reste celui de Debian Live. L'écran qui suit est le
thème Plymouth « ti-lex » : mascotte centrée sur fond noir, respiration lente,
barre de progression orange, et puces si un disque chiffré réclame sa phrase
secrète. Le langage de script Plymouth ne trace pas de formes et n'a pas de police
garantie dans l'initramfs : les barres sont des images unies mises à l'échelle, et
rien n'y est écrit en toutes lettres. /etc/plymouth/plymouthd.conf sélectionne le
thème, le hook 0700 y copie la mascotte et régénère l'initramfs, et la ligne de
commande noyau porte « quiet splash » — en live par lb config, et sur le système
installé par /etc/default/grub.d/99-ti-lex-splash.cfg. L'intégration continue le charge réellement
sous Xvfb et vérifie qu'il dessine ; il n'a jamais été vu sur un démarrage réel.

Le verrouillage garde le comportement du verrouilleur de session :
le fond LightDM ne garantit pas le thème de toutes les fenêtres de verrouillage.
ISO et rendu final XFCE/LightDM non encore validés sur matériel.

## Icônes de types de fichiers
49 tuiles vectorielles sous /usr/share/icons/TI-LEX : 42 types de fichiers dans
scalable/mimetypes, 7 outils TI-LEX dans scalable/apps. Chaque tuile est une page à
coin corné, dégradé vertical, pictogramme blanc et bandeau portant le nom du type.
Le thème déclare Inherits=Adwaita : toute icône non fournie garde celle du système,
et aucune icône générique de dossier n'est remplacée. xsettings sélectionne TI-LEX.

Elles sont générées par `python3 debian13/tools/make-icons.py` : modifier la table
ICONS ou TOOLS, relancer, et les 49 fichiers sont réécrits. Les creux (engrenage,
puce, disque) reçoivent la couleur de leur tuile, faute de masque fiable entre
librsvg et GdkPixbuf. Les bandeaux utilisent textLength : le nom tient dans la
largeur même si la police de rendu diffère de celle de génération.

/usr/share/ti-lex/filetypes.json relie extension et icône. Le lanceur s'en sert pour
la liste des programmes trouvés dans une archive, l'aperçu web pour ses exemples.

## Allumage et extinction des fenêtres
Les fenêtres TI-LEX s'ouvrent et se ferment comme un tube cathodique : ligne
lumineuse qui s'ouvre, voile blanc qui s'efface, puis l'inverse à la fermeture.
X11 et xfwm4 n'animent pas la géométrie des fenêtres, et une fenêtre GTK ne se
redimensionne jamais sous la taille minimale de son contenu : l'effet est donc
peint par la fenêtre, dans /usr/share/ti-lex/crt.py. Un gestionnaire de dessin
comprime le contenu avant que GTK ne dessine les enfants, un second pose le voile.
La fermeture est retardée du temps de l'extinction, puis suit son chemin habituel.
L'aperçu web reproduit le même effet en CSS, et les deux respectent la préférence
système de mouvement réduit.

