# Identité visuelle TI-LEX Pro

Les fichiers sont intégrés sous /usr/share/ti-lex/branding dans la future image.
- desktop.png : fond du bureau noir, ruban orange, accent vert et texture CRT discrète.
- login.png : fond de connexion avec centre dégagé pour le formulaire LightDM.
- logo.svg, avatar.svg, terminal.svg, settings.svg, tools.svg, folder.svg :
  six éléments vectoriels cohérents et redimensionnables.
- mascot.svg et mascot.png : téléviseur CRT souriant, source vectorielle et rendu
  512 x 512 utilisé par l'écran de démarrage.

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
commande noyau porte « quiet splash ». L'intégration continue le charge réellement
sous Xvfb et vérifie qu'il dessine ; il n'a jamais été vu sur un démarrage réel.

Le verrouillage garde le comportement du verrouilleur de session :
le fond LightDM ne garantit pas le thème de toutes les fenêtres de verrouillage.
ISO et rendu final XFCE/LightDM non encore validés sur matériel.
