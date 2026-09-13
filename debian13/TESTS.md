# Validation avant diffusion
Aucun des tests de démarrage suivants n'a encore été exécuté.

1. Construire dans une VM Debian 13 amd64 dédiée, ou par le workflow
   *Construire l'ISO TI-LEX* (onglet Actions), et conserver build.log :
   l'artéfact `journal-live-build` le contient, même si la construction échoue.
2. Vérifier le SHA256 avec sha256sum -c NOM.iso.sha256, après extraction du zip
   d'artéfact le cas échéant.
3. Démarrer en VM BIOS, puis UEFI. Secure Boot : validation distincte, non garantie.
4. Vérifier l'écran de démarrage : mascotte TI-LEX sur fond noir et barre
   orange, sans message noyau. En cas d'écran noir, retirer « splash » de la
   ligne de commande au menu d'amorçage pour voir les messages.
5. Vérifier bureau XFCE, clavier canadien, accents, audio, réseau et navigateur.
6. La session Live est temporaire et privilégiée (sudo permis par Debian Live).
   Ne pas y stocker de secrets, ni exposer des services. Vérifier le comportement
   de connexion Live avant de distribuer l'image.
7. Installer vers un disque VIRTUEL vide, par les deux chemins : « Installer TI-LEX
   Pro » depuis la session live (Calamares), puis l'installateur Debian depuis le
   menu de démarrage. Aucun preseed ne sélectionne ni n'efface de disque
   automatiquement ; Calamares montre un résumé avant d'écrire.
8. Créer un utilisateur et un mot de passe, terminer puis retirer l'ISO et redémarrer.
9. Vérifier le compte installé, sudo, absence du compte temporaire Live,
   absence d'autologin, LightDM et mises à jour apt.
10. Tester la machine réelle en mode Live, sans installation : NVIDIA RTX 5060,
   Wi-Fi, veille et écrans. Aucun pilote propriétaire spécifique n'est promis.
11. Vérifier les pouvoirs en session Live : « flatpak remotes » liste Flathub,
    « podman run --rm hello-world » démarre un conteneur, virt-manager s'ouvre et
    voit /dev/kvm, « lsblk -f » reconnaît exFAT et NTFS, et memtest86+ apparaît au
    menu de démarrage. Sans /dev/kvm — cas d'une machine virtuelle imbriquée — la
    virtualisation reste indisponible : ce n'est pas un défaut de l'image.
12. Ne proposer l'installation réelle qu'après sauvegarde et succès des tests.

Le script ne formate aucun disque. L'installateur peut effacer celui que
l'utilisateur sélectionne : toujours vérifier la cible.
