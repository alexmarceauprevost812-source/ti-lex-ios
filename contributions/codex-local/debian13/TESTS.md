# Validation avant diffusion
Aucun des tests de démarrage suivants n'a encore été exécuté.

1. Construire dans une VM Debian 13 amd64 dédiée et conserver build.log.
2. Vérifier le SHA256 avec sha256sum -c NOM.iso.sha256.
3. Démarrer en VM BIOS, puis UEFI. Secure Boot : validation distincte, non garantie.
4. Vérifier bureau XFCE, clavier canadien, accents, audio, réseau et navigateur.
5. La session Live est temporaire et privilégiée (sudo permis par Debian Live).
   Ne pas y stocker de secrets, ni exposer des services. Vérifier le comportement
   de connexion Live avant de distribuer l'image.
6. Démarrer l'installateur depuis le menu de démarrage, vers un disque VIRTUEL vide.
   Aucun preseed ne sélectionne ou n'efface de disque automatiquement.
7. Créer un utilisateur et un mot de passe, terminer puis retirer l'ISO et redémarrer.
8. Vérifier le compte installé, sudo, absence du compte temporaire Live,
   absence d'autologin, LightDM et mises à jour apt.
9. Tester la machine réelle en mode Live, sans installation : NVIDIA RTX 5060,
   Wi-Fi, veille et écrans. Aucun pilote propriétaire spécifique n'est promis.
10. Ne proposer l'installation réelle qu'après sauvegarde et succès des tests.

Le script ne formate aucun disque. L'installateur peut effacer celui que
l'utilisateur sélectionne : toujours vérifier la cible.

