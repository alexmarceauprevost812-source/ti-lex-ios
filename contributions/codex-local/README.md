# TI-LEX Pro — Debian 13
Branche de travail : `ti-lex-ios`. Base : Debian 13 « trixie », amd64, XFCE et LightDM.

**État : configuration de construction préparée, ISO non construite et non testée.**
Le noyau, les paquets et l'installateur viennent des dépôts Debian. Ce dépôt ne recopie pas leurs sources.

## Construire
Utiliser une **VM Debian 13 amd64 dédiée**, avec accès Internet, 8 Go de RAM et
60 Go libres conseillés. Ne pas exécuter la construction sur le système quotidien.

```bash
sudo apt update
sudo apt install -y git python3 live-build debootstrap squashfs-tools xorriso isolinux syslinux-common grub-pc-bin grub-efi-amd64-bin mtools dosfstools
git clone --branch ti-lex-ios https://github.com/alexmarceauprevost812-source/ti-lex-ios.git
cd ti-lex-ios
python3 debian13/build.py --check
sudo python3 debian13/build.py --build
```

Le script crée un dossier neuf dans `/var/tmp/ti-lex-build-*`, sans nettoyage automatique.
Il affiche le chemin de l'ISO et de son SHA256. Conserver les journaux et les listes
de paquets de live-build. L'opération télécharge plusieurs Go et nécessite du temps.

## Contenu
- Linux amd64, Debian Live, démarrage BIOS/UEFI configuré.
- XFCE, LightDM GTK, thème sombre provisoire.
- Réseau, firmware Debian, son PipeWire, Firefox ESR.
- Python, Git, diagnostic, sauvegarde et outils de base.
- Installateur Debian Live graphique depuis le menu de démarrage.
- Installation interactive : choix du disque et création du compte par l'utilisateur.
- Aucun serveur SSH, mot de passe personnel ou clé API préinstallé.

## Images
Voir [debian13/BRANDING.md](debian13/BRANDING.md).
Voir [debian13/TESTS.md](debian13/TESTS.md) avant toute installation réelle.
L'effet vieille TV animé, les agents IA et le pilote NVIDIA spécifique RTX 5060
ne sont pas encore intégrés ni validés.

## Bureau, terminal et ouverture simplifiée
- Deux fonds PNG bureau/connexion et six icônes SVG sont intégrés dans la configuration.
- La planche file-tools.png rassemble les formats et outils visuels de TI-LEX.
- Le fond alternatif `desktop-lexos.png` est fourni pour le choix d’apparence LexOS Pro.
- La plaquette gamer.svg regroupe les accès jeux, performances, streaming et captures.
- Le workflow `iso-build.yml` construit l’ISO Debian 13 et publie l’ISO ainsi que son SHA-256 dans les artefacts GitHub.
- La plaquette Gamer inclut le support GeForce RTX 5060 (nvidia-driver, Vulkan, gamemode) et conserve Mesa pour les GPU intégrés.
- La sélection développeur fournit les compilateurs, langages, débogueurs, conteneurs et outils de virtualisation courants.
- Installation Québec : français canadien (`fr_CA.UTF-8`), clavier canadien et fuseau `America/Toronto`; le service `ti-lex-update` vérifie les mises à jour chaque semaine.
- Le mode live permet d’essayer TI‑LEX depuis une clé USB ou une VM avant installation; voir `debian13/LIVE-MODE.md`.
- Une page graphique **Installer TI‑LEX Pro** est disponible dans le mode live avec Calamares; voir `debian13/LIVE-INSTALLER.md`.
- Terminal TI-LEX basé sur XFCE Terminal/Bash, palette dédiée et commande `tilex aide`.
- Paramètres enrichis : terminal, Python, éditeur, fichiers, archives, sauvegardes et diagnostic.
- Clic droit Thunar → Ouvrir avec TI-LEX pour ZIP, AppImage, .sh, .py et .deb compatibles.
- Aucun exécutable téléchargé ne démarre automatiquement.
- [Guide du terminal](debian13/TERMINAL.md), [guide du lanceur](debian13/OPEN-APPS.md).
- [Aperçu interactif Vercel](https://ti-lex-pro-preview-alexmarceauprevost812-3889s-projects.vercel.app) :
  démonstration web du bureau; ne lance pas Linux et ne remplace pas les tests de l'ISO.

Les tests locaux Python passent. Les vérifications GitHub contrôlent aussi les fichiers
et l'initialisation GTK dans Debian. Démarrage complet, matériel et installateur
restent à valider. La disposition de l'aperçu web est illustrative.

## Ancien prototype
`src/ti_lex_builder`, `config/packages.txt` et `pyproject.toml` sont conservés
pour historique. Ils concernent l'ancien prototype Ubuntu : **ne pas utiliser
ti-lex-build pour Debian 13**. Seul `python3 debian13/build.py` est le nouveau point d'entrée.

## Sources et redistribution
[Documentation live-build Debian 13](https://manpages.debian.org/trixie/live-build/lb_config.1.en.html).
Les licences Debian et celles des firmwares restent applicables.
Conserver les notices /usr/share/doc/*/copyright et prévoir la fourniture des sources
correspondantes avant diffusion publique. Les versions APT évoluent :
cette configuration n'est pas une garantie de reproductibilité bit à bit.
