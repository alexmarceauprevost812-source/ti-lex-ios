# Terminal TI-LEX Pro

Ouvrir Applications → Système → Terminal TI-LEX Pro, ou les paramètres TI-LEX.
Le terminal utilise XFCE Terminal et Bash : onglets, copier/coller, recherche,
polices et préférences sont ceux du vrai terminal Linux.
Le terminal a un fond noir, une écriture blanche, des suggestions vert lime et
une invite, un titre et un curseur orange. Après une commande en échec,
la prochaine invite affiche `[erreur N]` en rouge, avec son code de sortie.
Les applications gardent le contrôle des couleurs de leurs propres sorties.
La palette est fournie pour les nouveaux comptes. Le prompt TI-LEX
ne s'applique qu'au lanceur dédié et charge d'abord le fichier .bashrc personnel.

Tapez `tilex aide`. Les commandes disponibles sont :
systeme, processus, reseau, wifi, disques, memoire, services, journaux,
sessions, python, editeur, parametres, terminal, sauvegarde.

Exemples : `tilex processus`, `tilex reseau`, `tilex sessions`.
Les sessions tmux se détachent avec Ctrl+B puis D.
Python : quitter avec Ctrl+D. Nano : quitter avec Ctrl+X.

Git, Python/venv/pip, GCC, make, ripgrep, jq, curl, wget, rsync, SSH client,
htop, tmux, ncdu, tree, lsof, strace et les outils réseau sont dans les listes
de paquets de l'image. Leur installation effective dépend du succès de live-build.
Déjà Dup fournit le panneau de sauvegarde; aucune sauvegarde ne démarre seule.
Aucun compte externe ni modèle IA n'est installé automatiquement.

Les outils conservent les permissions Linux de la session. Les journaux visibles
dépendent de ces permissions. Les erreurs de commande sont retournées telles quelles.

Validation : tests Python avec doublures des commandes; démarrage graphique
et utilisation interactive à vérifier dans Debian/XFCE.
Documentation : https://docs.xfce.org/apps/xfce4-terminal/command-line
