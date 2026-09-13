from __future__ import annotations
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ("xorriso", "unsquashfs", "mksquashfs", "mount", "umount", "chroot")

def run(*args: str) -> None:
    print("+", " ".join(args), flush=True)
    subprocess.run(args, check=True)

def safe(path: Path) -> Path:
    result = path.expanduser().resolve()
    if result in {Path("/"), Path.home().resolve()}:
        raise SystemExit(f"Chemin refusé: {result}")
    return result

def packages() -> list[str]:
    lines = (ROOT / "config/packages.txt").read_text(encoding="utf-8").splitlines()
    return [x.strip() for x in lines if x.strip() and not x.lstrip().startswith("#")]

def customize(rootfs: Path) -> None:
    mounted: list[Path] = []
    specs = [("--bind", "/dev", "dev"), ("-t", "proc", "proc", "proc"),
             ("-t", "sysfs", "sysfs", "sys"), ("--bind", "/run", "run")]
    try:
        shutil.copy2("/etc/resolv.conf", rootfs / "etc/resolv.conf")
        for *options, source, relative in specs:
            target = rootfs / relative
            target.mkdir(parents=True, exist_ok=True)
            run("mount", *options, source, str(target))
            mounted.append(target)
        run("chroot", str(rootfs), "apt-get", "update")
        run("chroot", str(rootfs), "env", "DEBIAN_FRONTEND=noninteractive",
            "apt-get", "install", "-y", "--no-install-recommends", *packages())
        run("chroot", str(rootfs), "apt-get", "clean")
        (rootfs / "etc/ti-lex-release").write_text(
            'NAME="TI-LEX"\nVERSION="0.1"\nBASE="Ubuntu"\n', encoding="utf-8")
    finally:
        for target in reversed(mounted):
            subprocess.run(["umount", "-lf", str(target)], check=False)

def build(source: Path, work: Path, output: Path) -> None:
    if os.geteuid() != 0:
        raise SystemExit("Lancez la construction avec sudo.")
    missing = [x for x in TOOLS if shutil.which(x) is None]
    if missing:
        raise SystemExit("Dépendances manquantes: " + ", ".join(missing))
    source, work, output = source.expanduser().resolve(), safe(work), safe(output)
    if not source.is_file():
        raise SystemExit(f"ISO source introuvable: {source}")
    if work.exists():
        raise SystemExit(f"{work} existe déjà; inspectez puis déplacez ce dossier.")
    iso, rootfs = work / "iso", work / "rootfs"
    iso.mkdir(parents=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    run("xorriso", "-osirrox", "on", "-indev", str(source), "-extract", "/", str(iso))
    candidates = list(iso.glob("casper/*filesystem*.squashfs"))
    if not candidates:
        raise SystemExit("SquashFS Ubuntu introuvable dans casper/.")
    squash = max(candidates, key=lambda p: p.stat().st_size)
    run("unsquashfs", "-d", str(rootfs), str(squash))
    customize(rootfs)
    squash.unlink()
    run("mksquashfs", str(rootfs), str(squash), "-comp", "xz", "-noappend")
    (squash.parent / "filesystem.size").write_text(
        str(sum(p.stat().st_size for p in rootfs.rglob("*") if p.is_file())),
        encoding="ascii")
    run("xorriso", "-indev", str(source), "-outdev", str(output),
        "-map", str(iso), "/", "-boot_image", "any", "replay")
    print(f"ISO créée: {output}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Construire l'ISO TI-LEX")
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--work", type=Path, default=ROOT / "work")
    parser.add_argument("--output", type=Path, default=ROOT / "dist/ti-lex-pro-amd64.iso")
    args = parser.parse_args()
    try:
        build(args.source, args.work, args.output)
    except subprocess.CalledProcessError as error:
        print(f"Commande échouée: {error.returncode}", file=sys.stderr)
        raise SystemExit(error.returncode) from error

if __name__ == "__main__":
    main()

