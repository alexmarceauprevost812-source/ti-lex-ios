"""Extract ZIPs into private app directories; never run during extraction."""
from pathlib import Path, PurePosixPath
import json
import os
import shutil
import stat
import subprocess
import tempfile
import zipfile

LIMIT = 2 * 1024**3
MAX_FILES = 20000
FILETYPES = "/usr/share/ti-lex/filetypes.json"

def icon_file(path, table=FILETYPES):
    """Icône SVG du type de fichier, d'après l'extension. None si rien ne convient :
    l'appelant affiche alors la ligne sans image plutôt que d'échouer."""
    try:
        data = json.loads(Path(table).read_text(encoding="utf-8"))
        name = data["extensions"].get(Path(path).suffix.lower(), data["fallback"])
        icon = Path(data["mimetypes"]) / f"{name}.svg"
    except (OSError, ValueError, KeyError, TypeError):
        return None
    return icon if icon.is_file() else None

def extract_archive(source, destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True, mode=0o700)
    with zipfile.ZipFile(source) as archive:
        entries = archive.infolist()
        if len(entries) > MAX_FILES or sum(i.file_size for i in entries) > LIMIT:
            raise ValueError("Archive trop volumineuse (maximum 2 Gio et 20 000 entrées).")
        for info in entries:
            path = PurePosixPath(info.filename)
            mode = info.external_attr >> 16
            if (not info.filename or path.is_absolute() or ".." in path.parts
                or "\\" in info.filename or ":" in info.filename
                or stat.S_ISLNK(mode)
                or (stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR))):
                raise ValueError("Archive refusée : chemin ou type de fichier non pris en charge.")
            if info.flag_bits & 1:
                raise ValueError("Archive chiffrée : extraire d’abord avec le gestionnaire d’archives.")
        required = sum(i.file_size for i in entries)
        if shutil.disk_usage(destination).free < required + 100 * 1024**2:
            raise ValueError("Espace disque insuffisant.")
        target = Path(tempfile.mkdtemp(prefix="app-", dir=destination)).resolve()
        try:
            total = 0
            for info in entries:
                output = target.joinpath(*PurePosixPath(info.filename).parts)
                if not output.resolve().is_relative_to(target):
                    raise ValueError("Chemin hors du dossier de l’application.")
                if info.is_dir():
                    output.mkdir(parents=True, exist_ok=True, mode=0o700)
                    continue
                output.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
                with archive.open(info) as src, output.open("xb") as dst:
                    while chunk := src.read(1024 * 1024):
                        total += len(chunk)
                        if total > LIMIT:
                            raise ValueError("Limite de décompression dépassée.")
                        dst.write(chunk)
                output.chmod(0o700 if (info.external_attr >> 16) & 0o111 else 0o600)
            return target
        except Exception:
            # Only this newly created, validated private folder is removed.
            shutil.rmtree(target)
            raise

def candidates(folder):
    result = []
    for path in sorted(Path(folder).rglob("*")):
        if not path.is_file() or path.is_symlink() or "__MACOSX" in path.parts:
            continue
        if path.suffix.lower() in (".appimage", ".sh", ".py", ".deb"):
            result.append(path)
        elif not path.suffix or os.access(path, os.X_OK):
            with path.open("rb") as stream:
                if stream.read(4) == b"\x7fELF":
                    result.append(path)
    return result

def command_for(path):
    path = Path(path).resolve(strict=True)
    if not path.is_file():
        raise ValueError("Sélectionnez un fichier.")
    suffix = path.suffix.lower()
    if suffix == ".deb":
        return ["gdebi-gtk", str(path)]
    if suffix == ".py":
        return ["python3", str(path)]
    if suffix == ".sh":
        return ["bash", str(path)]
    with path.open("rb") as stream:
        header = stream.read(4)
    if header != b"\x7fELF":
        raise ValueError("Format non pris en charge. Choisissez un programme Linux, AppImage, .sh, .py ou .deb.")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return [str(path)]
