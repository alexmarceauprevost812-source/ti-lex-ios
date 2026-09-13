# TI-LEX ISO

Distribution Linux TI-LEX basée sur Ubuntu Desktop.

## Vision

Un système noir et orange orienté Python, IA locale, administration Ubuntu et
cybersécurité défensive. La fondation v0.1 fournit un constructeur ISO expérimental.

## Prérequis

```bash
sudo apt update
sudo apt install -y python3 python3-venv xorriso squashfs-tools rsync \
  grub-pc-bin grub-efi-amd64-bin mtools isolinux
```

Prévoyez 30 Go d'espace libre et 8 Go de mémoire.

## Construction

```bash
git clone https://github.com/alexmarceauprevost812-source/ti-lex-ios.git
cd ti-lex-ios
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
sudo .venv/bin/ti-lex-build --source ~/Téléchargements/ubuntu-desktop-amd64.iso
```

Résultat : `dist/ti-lex-pro-amd64.iso`.

Testez toujours l'image dans GNOME Boxes ou VirtualBox avant une installation réelle.

## Feuille de route

- [x] Structure et constructeur Python
- [x] Manifeste de logiciels
- [ ] Bureau TI-LEX noir/orange
- [ ] Paramètres et Terminal TI-LEX
- [ ] Ollama et agents IA facultatifs
- [ ] Tests de démarrage en machine virtuelle
- [ ] ISO candidate d'installation
