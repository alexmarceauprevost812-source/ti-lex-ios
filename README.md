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
L'effet vieille TV, les applications TI-LEX, les agents IA et le pilote NVIDIA
spécifique RTX 5060 ne sont pas encore intégrés ni validés.

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
