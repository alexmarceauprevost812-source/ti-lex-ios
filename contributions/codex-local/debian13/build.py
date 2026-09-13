#!/usr/bin/env python3
"""Build TI-LEX using Debian live-build in a fresh dedicated directory."""
import argparse
import hashlib
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent

def options():
    return [
        "--mode", "debian", "--distribution", "trixie",
        "--architecture", "amd64", "--binary-image", "iso-hybrid",
        "--bootloaders", "syslinux,grub-efi",
        "--archive-areas", "main contrib non-free non-free-firmware",
        "--debian-installer", "live", "--debian-installer-gui", "true",
        "--debian-installer-distribution", "trixie",
        "--firmware-chroot", "true", "--firmware-binary", "true",
        "--security", "true", "--updates", "true", "--apt-secure", "true",
        "--checksums", "sha256", "--image-name", "ti-lex-pro-debian13",
        "--iso-volume", "TI_LEX_PRO_13",
        "--bootappend-live",
        "boot=live components quiet splash username=tilex hostname=ti-lex locales=fr_CA.UTF-8 keyboard-layouts=ca timezone=America/Toronto",
    ]

def validate():
    config = ROOT / "config"
    lists = sorted((config / "package-lists").glob("*.list.chroot"))
    if not lists:
        raise SystemExit("Aucune liste de paquets.")
    seen = set()
    for manifest in lists:
        for line in manifest.read_text().splitlines():
            package = line.strip()
            if not package or package.startswith("#"):
                continue
            if any(c not in "abcdefghijklmnopqrstuvwxyz0123456789+.-" for c in package):
                raise SystemExit(f"Nom de paquet incorrect : {package}")
            if package in seen:
                raise SystemExit(f"Paquet en double : {package}")
            seen.add(package)
    for link in config.rglob("*"):
        if link.is_symlink():
            raise SystemExit(f"Lien symbolique interdit dans la configuration : {link}")
    print(f"Configuration : {len(seen)} paquets explicites. Disponibilité APT non vérifiée.")
    return config

def build(config):
    if os.geteuid() != 0:
        raise SystemExit("Utiliser sudo uniquement pour --build dans une VM Debian 13 dédiée.")
    release = platform.freedesktop_os_release()
    if release.get("ID") != "debian" or release.get("VERSION_ID") != "13":
        raise SystemExit("Construction réservée à Debian 13.")
    if platform.machine() not in ("x86_64", "amd64"):
        raise SystemExit("Hôte amd64 nécessaire.")
    missing = [x for x in ("lb", "debootstrap", "xorriso", "mksquashfs") if not shutil.which(x)]
    if missing:
        raise SystemExit("Outils manquants : " + ", ".join(missing))
    if shutil.disk_usage("/var/tmp").free < 40 * 1024**3:
        raise SystemExit("Prévoir au moins 40 Gio libres dans /var/tmp.")
    work = Path(tempfile.mkdtemp(prefix="ti-lex-build-", dir="/var/tmp"))
    work.chmod(0o755)
    print(f"Dossier conservé même en cas d'échec : {work}", flush=True)
    subprocess.run(["lb", "config", *options()], cwd=work, check=True)
    shutil.copytree(config, work / "config", dirs_exist_ok=True)
    for hook in (work / "config/hooks/live").glob("*.hook.chroot"):
        hook.chmod(0o755)
    with (work / "build.log").open("w") as log:
        process = subprocess.Popen(["lb", "build"], cwd=work, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(line, end="", flush=True)
            log.write(line)
            log.flush()
        if process.wait():
            raise SystemExit(f"Échec : consulter {work}/build.log. Rien n'est supprimé.")
    images = list(work.glob("*.iso"))
    if not images:
        raise SystemExit("live-build terminé sans fichier ISO : consulter build.log.")
    for iso in images:
        with iso.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        iso.with_suffix(".iso.sha256").write_text(f"{digest}  {iso.name}\n")
        print(f"ISO produite, à tester en VM : {iso}")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--check", action="store_true", help="Validation locale sans sudo ni réseau")
    choice.add_argument("--build", action="store_true", help="Construction dans une VM dédiée")
    args = parser.parse_args()
    config = validate()
    if args.build:
        build(config)

if __name__ == "__main__":
    main()
