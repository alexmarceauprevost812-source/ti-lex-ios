# Identité visuelle TI-LEX Pro

Les fichiers sont intégrés sous /usr/share/ti-lex/branding dans la future image.
- desktop.png : fond du bureau noir, ruban orange, accent vert et texture CRT discrète.
- login.png : fond de connexion avec centre dégagé pour le formulaire LightDM.
- logo.svg, avatar.svg, terminal.svg, settings.svg, tools.svg, folder.svg :
  six éléments vectoriels cohérents et redimensionnables.

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

L'écran de démarrage BIOS/UEFI reste celui de Debian Live. Aucun effet CRT animé
n'est installé. Le verrouillage garde le comportement du verrouilleur de session :
le fond LightDM ne garantit pas le thème de toutes les fenêtres de verrouillage.
ISO et rendu final XFCE/LightDM non encore validés sur matériel.
