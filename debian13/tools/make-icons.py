#!/usr/bin/python3
"""Génère les icônes de types de fichiers TI-LEX et leur table de correspondance.

Les 49 tuiles reprennent une planche fournie : page à coin corné, dégradé vertical,
pictogramme blanc, bandeau sombre portant le nom du type. Tout est vectoriel, donc
net à 16 comme à 512 pixels, et régénérable : modifier ICONS puis relancer ce script.

    python3 debian13/tools/make-icons.py
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1] / "config/includes.chroot/usr/share"
THEME = ROOT / "icons/TI-LEX"
TABLE = ROOT / "ti-lex/filetypes.json"

# Pictogrammes dessinés dans une boîte de 48 x 48, en blanc. « {creux} » reçoit la
# couleur de la tuile : c'est ainsi qu'un engrenage ou une puce garde son trou sans
# masque ni fill-rule, que librsvg et GdkPixbuf rendent diversement.
GLYPHS = {
    "image": '<rect x="5" y="9" width="38" height="30" rx="4" fill="none" stroke="#fff" stroke-width="3.4"/>'
             '<circle cx="16" cy="19" r="3.6" fill="#fff"/><path d="M9 34l10-11 7 8 5-5 8 8z" fill="#fff"/>',
    "pen": '<path d="M31 5l12 12-5 5-12-12z" fill="#fff"/><path d="M24 12l12 12-15 15-13 4 4-13z" fill="#fff"/>'
           '<path d="M8 43l3-9 6 6z" fill="#fff"/>',
    "film": '<rect x="5" y="8" width="30" height="26" rx="3" fill="none" stroke="#fff" stroke-width="3.2"/>'
            '<path d="M13 41h25a4 4 0 0 0 4-4V15" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>'
            '<path d="M16 14l10 7-10 7z" fill="#fff"/>',
    "aperture": '<circle cx="24" cy="24" r="18" fill="#fff"/><circle cx="24" cy="24" r="11" fill="{creux}"/>'
                '<path d="M24 6v12M40 17l-11 6M40 31l-11-6M24 42V30M8 31l11-6M8 17l11 6" '
                'stroke="{creux}" stroke-width="3" stroke-linecap="round"/>',
    "play": '<circle cx="24" cy="24" r="18" fill="#fff"/><path d="M19 15l14 9-14 9z" fill="{creux}"/>',
    "note": '<path d="M38 4v25a7.5 7.5 0 1 1-5-7V14L19 17v18a7.5 7.5 0 1 1-5-7V12z" fill="#fff"/>',
    "piano": '<g fill="#fff"><rect x="7" y="9" width="7" height="30" rx="2"/><rect x="16" y="9" width="7" height="30" rx="2"/>'
             '<rect x="25" y="9" width="7" height="30" rx="2"/><rect x="34" y="9" width="7" height="30" rx="2"/></g>',
    "lines": '<g fill="#fff"><rect x="8" y="11" width="32" height="4.5" rx="2.2"/>'
             '<rect x="8" y="21.5" width="32" height="4.5" rx="2.2"/><rect x="8" y="32" width="21" height="4.5" rx="2.2"/></g>',
    "table": '<rect x="5" y="8" width="38" height="32" rx="3.5" fill="#fff"/>'
             '<path d="M5 19h38M5 29h38M18 8v32M31 8v32" stroke="{creux}" stroke-width="3"/>',
    "pie": '<path d="M22 5v21h21A21 21 0 0 1 22 47 21 21 0 0 1 22 5z" fill="#fff"/>'
           '<path d="M27 3a21 21 0 0 1 19 19H27z" fill="#fff" opacity=".62"/>',
    "bookmark": '<path d="M13 4h22a4 4 0 0 1 4 4v37l-15-9-15 9V8a4 4 0 0 1 4-4z" fill="#fff"/>',
    "zip": '<g fill="#fff"><rect x="19" y="4" width="10" height="6" rx="1.5"/><rect x="19" y="12" width="10" height="6" rx="1.5"/>'
           '<rect x="19" y="20" width="10" height="6" rx="1.5"/><rect x="16" y="29" width="16" height="15" rx="4"/></g>'
           '<circle cx="24" cy="36" r="3" fill="{creux}"/>',
    "stack": '<g fill="#fff"><rect x="6" y="8" width="36" height="9" rx="3"/><rect x="6" y="20" width="36" height="9" rx="3"/>'
             '<rect x="6" y="32" width="36" height="9" rx="3"/></g>',
    "blocks": '<g fill="#fff"><rect x="7" y="7" width="15" height="15" rx="3.5"/><rect x="26" y="7" width="15" height="15" rx="3.5"/>'
              '<rect x="7" y="26" width="15" height="15" rx="3.5"/><rect x="26" y="26" width="15" height="15" rx="3.5"/></g>',
    "cube": '<path d="M24 4l18 10v20L24 44 6 34V14z" fill="none" stroke="#fff" stroke-width="3.2" stroke-linejoin="round"/>'
            '<path d="M6 14l18 10 18-10M24 24v20" fill="none" stroke="#fff" stroke-width="3.2" stroke-linejoin="round"/>',
    "disc": '<circle cx="24" cy="24" r="18" fill="#fff"/><circle cx="24" cy="24" r="9" fill="{creux}"/>'
            '<circle cx="24" cy="24" r="3.5" fill="#fff"/>',
    "package": '<path d="M24 3l19 10-19 10L5 13z" fill="#fff"/><path d="M4 16v18l18 10V26z" fill="#fff" opacity=".78"/>'
               '<path d="M44 16v18L26 44V26z" fill="#fff" opacity=".55"/>',
    "gear": '<circle cx="24" cy="24" r="13" fill="#fff"/><circle cx="24" cy="24" r="5" fill="{creux}"/>{dents}',
    "prompt": '<rect x="4" y="8" width="40" height="31" rx="4.5" fill="none" stroke="#fff" stroke-width="3.2"/>'
              '<path d="M12 18l6 5.5-6 5.5" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
              '<rect x="23" y="27" width="13" height="3.6" rx="1.8" fill="#fff"/>',
    "download": '<path d="M24 5v21m0 0l-8.5-8.5M24 26l8.5-8.5" fill="none" stroke="#fff" stroke-width="3.6" '
                'stroke-linecap="round" stroke-linejoin="round"/>'
                '<path d="M7 31v7a5 5 0 0 0 5 5h24a5 5 0 0 0 5-5v-7" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/>',
    "shield": '<path d="M24 3l17 6v14c0 11-7.5 18-17 21C14.5 41 7 34 7 23V9z" fill="#fff"/>'
              '<path d="M16 23l6 6 11-11" fill="none" stroke="{creux}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>',
    "chip": '<rect x="11" y="11" width="26" height="26" rx="4" fill="#fff"/><rect x="18" y="18" width="12" height="12" rx="2" fill="{creux}"/>'
            '<g stroke="#fff" stroke-width="3" stroke-linecap="round"><path d="M17 4v7M24 4v7M31 4v7M17 37v7M24 37v7M31 37v7'
            'M4 17h7M4 24h7M4 31h7M37 17h7M37 24h7M37 31h7"/></g>',
    "globe": '<circle cx="24" cy="24" r="18" fill="none" stroke="#fff" stroke-width="3.2"/>'
             '<path d="M6 24h36M24 6c5.5 5 5.5 31 0 36M24 6c-5.5 5-5.5 31 0 36" fill="none" stroke="#fff" stroke-width="3.2"/>',
    "folder": '<path d="M5 12a4 4 0 0 1 4-4h9.5l4.5 5.5H39a4 4 0 0 1 4 4V36a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4z" fill="#fff"/>',
    "markdown": '<path d="M6 12h6l6 8 6-8h6v24h-6V22l-6 8-6-8v14H6z" fill="#fff"/>'
                '<path d="M37 12v15m0 0l-5-5m5 5l5-5" fill="none" stroke="#fff" stroke-width="3.4" '
                'stroke-linecap="round" stroke-linejoin="round"/>',
}

TEXT_GLYPH = ('<text x="24" y="{base}" text-anchor="middle" fill="#fff" font-family="DejaVu Sans, Noto Sans, sans-serif" '
              'font-weight="700" font-size="{size}" textLength="{length}" lengthAdjust="spacingAndGlyphs">{text}</text>')


def glyph(name, color):
    """Rend un pictogramme, en bouchant les creux avec la couleur de la tuile."""
    if name.startswith("texte:"):
        _, text, size, length = name.split(":")
        return TEXT_GLYPH.format(text=text, size=size, length=length, base=33)
    teeth = "".join(
        f'<rect x="21" y="1.5" width="6" height="9" rx="2.4" fill="#fff" transform="rotate({angle} 24 24)"/>'
        for angle in range(0, 360, 45))
    return GLYPHS[name].format(creux=color, dents=teeth)


# (nom du bandeau, nom de fichier de l'icône, couleur, pictogramme, extensions)
ICONS = [
    ("PNG", "image-png", "#f59120", "image", [".png"]),
    ("JPG", "image-jpeg", "#f4511e", "image", [".jpg", ".jpeg", ".jpe"]),
    ("GIF", "image-gif", "#ec2f7b", "image", [".gif"]),
    ("SVG", "image-svg+xml", "#8e24d0", "pen", [".svg", ".svgz"]),
    ("TIFF", "image-tiff", "#1e88f0", "film", [".tif", ".tiff"]),
    ("RAW", "image-x-dcraw", "#3a3a40", "aperture", [".raw", ".cr2", ".nef", ".arw", ".dng"]),
    ("MP4", "video-mp4", "#e5252a", "play", [".mp4", ".m4v", ".mkv", ".webm", ".avi", ".mov"]),
    ("MP3", "audio-mpeg", "#1976f2", "note", [".mp3"]),
    ("WAV", "audio-x-wav", "#43b514", "note", [".wav"]),
    ("FLAC", "audio-flac", "#7b1fd0", "note", [".flac"]),
    ("OGG", "audio-ogg", "#f57c00", "note", [".ogg", ".oga", ".opus"]),
    ("WMA", "audio-x-ms-wma", "#d81b8c", "note", [".wma"]),
    ("MIDI", "audio-midi", "#5e35b1", "piano", [".mid", ".midi"]),
    ("M4A", "audio-mp4", "#00acc1", "note", [".m4a", ".aac"]),
    ("DOC", "application-msword", "#2b7cf5", "lines", [".doc"]),
    ("DOCX", "application-vnd.openxmlformats-officedocument.wordprocessingml.document",
     "#1e6fe0", "lines", [".docx", ".odt"]),
    ("XLS", "application-vnd.ms-excel", "#2faa44", "table", [".xls"]),
    ("XLSX", "application-vnd.openxmlformats-officedocument.spreadsheetml.sheet",
     "#26963a", "table", [".xlsx", ".ods", ".csv"]),
    ("PPT", "application-vnd.ms-powerpoint", "#ef6c1a", "pie", [".ppt"]),
    ("PPTX", "application-vnd.openxmlformats-officedocument.presentationml.presentation",
     "#f08326", "pie", [".pptx", ".odp"]),
    ("PDF", "application-pdf", "#e02020", "bookmark", [".pdf"]),
    ("TXT", "text-plain", "#6b6b73", "lines", [".txt", ".text"]),
    ("RTF", "text-rtf", "#45454c", "lines", [".rtf"]),
    ("MD", "text-markdown", "#7d1fd0", "markdown", [".md", ".markdown"]),
    ("JSON", "application-json", "#2b56f5", "texte:{ }:26:26", [".json"]),
    ("HTML", "text-html", "#f4681c", "texte:&lt;/&gt;:21:34", [".html", ".htm", ".xhtml"]),
    ("CSS", "text-css", "#e8441c", "texte:{ }:26:26", [".css", ".scss"]),
    ("JS", "application-javascript", "#ef8c1b", "texte:Js:28:24", [".js", ".mjs", ".cjs", ".ts"]),
    ("ZIP", "application-zip", "#f5b400", "zip", [".zip"]),
    ("RAR", "application-vnd.rar", "#8e24d0", "stack", [".rar"]),
    ("7Z", "application-x-7z-compressed", "#1e88f0", "blocks", [".7z"]),
    ("TAR", "application-x-tar", "#45454c", "cube", [".tar", ".tgz", ".txz", ".gz", ".xz", ".bz2", ".zst"]),
    ("ISO", "application-x-cd-image", "#6b6b73", "disc", [".iso", ".img"]),
    ("APP", "application-x-executable", "#21b5d8", "package", [".bin", ".run", ".elf"]),
    ("DEB", "application-vnd.debian.binary-package", "#3aa524", "package", [".deb"]),
    ("EXE", "application-x-ms-dos-executable", "#f57c00", "gear", [".exe", ".msi", ".dll"]),
    ("SH", "application-x-shellscript", "#e5252a", "prompt", [".sh", ".bash", ".zsh"]),
    ("PY", "text-x-python", "#f59120", "texte:Py:28:24", [".py", ".pyw"]),
    ("APPIMAGE", "application-vnd.appimage", "#2b7cf5", "download", [".appimage"]),
    ("SNAP", "application-vnd.snap", "#7b1fd0", "cube", [".snap"]),
    ("FLATPAK", "application-vnd.flatpak", "#43b514", "package", [".flatpak", ".flatpakref"]),
    ("SERVICE", "text-x-systemd-unit", "#45454c", "gear", [".service", ".timer", ".socket"]),
]

# Sept tuiles d'outils : ce sont les icônes des fenêtres TI-LEX, pas des types de
# fichiers. Elles ne remplacent donc aucune icône générique du bureau.
TOOLS = [
    ("DOSSIERS", "ti-lex-files", "#f59120", "folder"),
    ("RÉSEAU", "ti-lex-network", "#e5252a", "globe"),
    ("PARAMÈTRES", "ti-lex-settings", "#2b7cf5", "gear"),
    ("TERMINAL", "ti-lex-terminal", "#43b514", "prompt"),
    ("SÉCURITÉ", "ti-lex-security", "#8e24d0", "shield"),
    ("SYSTÈME", "ti-lex-system", "#21b5d8", "chip"),
    ("LOGS", "ti-lex-logs", "#f5b400", "lines"),
]


def lighter(color, amount=0.26):
    """Éclaircit vers le blanc : le haut de la tuile capte la lumière."""
    red, green, blue = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    mix = lambda value: round(value + (255 - value) * amount)
    return f"#{mix(red):02x}{mix(green):02x}{mix(blue):02x}"


def ribbon(label):
    """Le bandeau : la taille suit la longueur, et textLength garantit l'ajustement
    même si la police de rendu diffère de celle du poste de génération."""
    size = {1: 22, 2: 22, 3: 21, 4: 18, 5: 16, 6: 14, 7: 12.5}.get(len(label), 11)
    return (f'<rect x="22" y="86" width="84" height="25" rx="7" fill="#000" opacity=".46"/>'
            f'<text x="64" y="103.5" text-anchor="middle" fill="#fff" '
            f'font-family="DejaVu Sans, Noto Sans, sans-serif" font-weight="700" font-size="{size}" '
            f'textLength="{min(74, size * 0.66 * len(label)):.1f}" lengthAdjust="spacingAndGlyphs">{label}</text>')


def tile(label, color, picto):
    """Une tuile : page à coin corné, dégradé, pictogramme, bandeau."""
    key = f"g{abs(hash((label, color))) % 100000}"
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">'
        f'<defs><linearGradient id="{key}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{lighter(color)}"/><stop offset="1" stop-color="{color}"/>'
        '</linearGradient></defs>'
        f'<path d="M26 6h64l24 24v80a12 12 0 0 1-12 12H26a12 12 0 0 1-12-12V18A12 12 0 0 1 26 6z" fill="url(#{key})"/>'
        '<path d="M90 6l24 24H90z" fill="#fff" opacity=".32"/>'
        f'<g transform="translate(40 26)">{glyph(picto, color)}</g>'
        f'{ribbon(label)}</svg>')


def main():
    mimetypes = THEME / "scalable/mimetypes"
    apps = THEME / "scalable/apps"
    for folder in (mimetypes, apps):
        folder.mkdir(parents=True, exist_ok=True)

    (THEME / "index.theme").write_text(
        "[Icon Theme]\n"
        "Name=TI-LEX\n"
        "Comment=Types de fichiers et outils TI-LEX Pro\n"
        "Inherits=Adwaita,hicolor\n"
        "Directories=scalable/mimetypes,scalable/apps\n\n"
        "[scalable/mimetypes]\nSize=48\nMinSize=16\nMaxSize=512\nContext=MimeTypes\nType=Scalable\n\n"
        "[scalable/apps]\nSize=48\nMinSize=16\nMaxSize=512\nContext=Applications\nType=Scalable\n",
        encoding="utf-8")

    extensions = {}
    for label, name, color, picto, suffixes in ICONS:
        (mimetypes / f"{name}.svg").write_text(tile(label, color, picto), encoding="utf-8")
        for suffix in suffixes:
            extensions[suffix] = name
    for label, name, color, picto in TOOLS:
        (apps / f"{name}.svg").write_text(tile(label, color, picto), encoding="utf-8")

    TABLE.write_text(json.dumps({
        "theme": "TI-LEX",
        "mimetypes": "/usr/share/icons/TI-LEX/scalable/mimetypes",
        "apps": "/usr/share/icons/TI-LEX/scalable/apps",
        "fallback": "text-plain",
        "extensions": dict(sorted(extensions.items())),
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(ICONS)} types et {len(TOOLS)} outils écrits dans {THEME}")


if __name__ == "__main__":
    main()
