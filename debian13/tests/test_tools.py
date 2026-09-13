import contextlib
import importlib.util
import importlib.machinery
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import zipfile
import stat

ROOT = Path(__file__).resolve().parents[1]
INC = ROOT / "config/includes.chroot"
def module(name, path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    result = importlib.util.module_from_spec(spec)
    loader.exec_module(result)
    return result
backend = module("backend", INC / "usr/share/ti-lex/settings/backend.py")
cli = module("tilex", INC / "usr/local/bin/tilex")
desktop = module("desktop", INC / "usr/share/ti-lex/desktop/setup.py")
archive_core = module("archive_core", INC / "usr/share/ti-lex/launcher/core.py")

class ToolsTests(unittest.TestCase):
    def test_nested_terminal_dependency(self):
        with patch.object(backend.shutil, "which", side_effect=lambda x: None if x == "nmtui-connect" else "/usr/bin/" + x):
            self.assertFalse(backend.available(backend.TOOLS["Choisir un réseau Wi-Fi"]))
            self.assertTrue(backend.available(backend.TOOLS["Préférences du terminal"]))
    def test_missing_terminal(self):
        with patch.object(backend.shutil, "which", return_value=None):
            self.assertFalse(backend.available(backend.TOOLS["Python"]))
    def test_wifi_hardware_before_radio(self):
        with patch.object(backend, "query", return_value="ethernet"):
            self.assertEqual(backend.wifi_state()[0], "unknown")
    def test_bluetooth_off(self):
        with patch.object(backend, "query", return_value="Controller AA:BB\n Powered: no"):
            self.assertEqual(backend.bluetooth_state()[0], "off")
    def test_cli_missing_tool(self):
        with patch.object(cli.shutil, "which", return_value=None), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(cli.main(["reseau"]), 127)
    def test_cli_preserves_exit_code_and_argv(self):
        with patch.object(cli.shutil, "which", return_value="/usr/bin/nmcli"), patch.object(cli.subprocess, "run", return_value=subprocess.CompletedProcess([], 7)) as run:
            self.assertEqual(cli.main(["reseau"]), 7)
            run.assert_called_once_with(("nmcli", "device", "status"), check=False)
    def test_help_never_launches(self):
        with patch.object(cli.subprocess, "run") as run, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(["aide"]), 0)
            run.assert_not_called()
    def test_wallpaper_keeps_user_choice(self):
        with tempfile.TemporaryDirectory() as folder:
            state = Path(folder) / "done"
            state.touch()
            with patch.object(desktop.subprocess, "run") as run:
                desktop.apply_once(state)
                run.assert_not_called()
    def test_wallpaper_failure_does_not_mark_complete(self):
        with tempfile.TemporaryDirectory() as folder:
            state = Path(folder) / "done"
            with patch.object(desktop, "WALLPAPER", __file__), patch.object(desktop.subprocess, "run", side_effect=OSError("No display")), patch.object(desktop.time, "sleep"):
                desktop.apply_once(state, attempts=1)
            self.assertFalse(state.exists())
    def test_svg_and_config_xml(self):
        for path in [*INC.rglob("*.svg"), *INC.rglob("*.xml")]:
            ET.parse(path)
    def test_launcher_asset_paths(self):
        for path in INC.rglob("*.desktop"):
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.startswith("Icon=/usr/share/ti-lex/"):
                    self.assertTrue((INC / line.split("=", 1)[1].lstrip("/")).is_file(), str(path))
    def test_raster_headers(self):
        for name in ("desktop.png", "login.png"):
            path = INC / "usr/share/ti-lex/branding" / name
            self.assertEqual(path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")

    def test_zip_extract_and_find_app_without_execution(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "app.zip"
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr("Mon application/start.py", "print('test')")
                archive.writestr("Mon application/readme.txt", "readme")
            with patch.object(archive_core.subprocess, "Popen") as launch:
                extracted = archive_core.extract_archive(source, root / "apps")
                found = archive_core.candidates(extracted)
                self.assertEqual(len(found), 1)
                self.assertEqual(found[0].name, "start.py")
                self.assertEqual(archive_core.command_for(found[0]), ["python3", str(found[0])])
                launch.assert_not_called()

    def test_zip_rejects_traversal_and_symlink(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for index, name in enumerate(("../escape.py", "/absolute.py", "C:/escape.py", "evil")):
                source = root / f"{index}.zip"
                with zipfile.ZipFile(source, "w") as archive:
                    info = zipfile.ZipInfo(name)
                    if name == "evil":
                        info.create_system = 3
                        info.external_attr = (stat.S_IFLNK | 0o777) << 16
                    archive.writestr(info, "target")
                with self.assertRaises(ValueError):
                    archive_core.extract_archive(source, root / "apps")
            self.assertFalse((root / "escape.py").exists())

    def test_zip_enforces_size_limit(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "large.zip"
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr("large.py", "x" * 30)
            with patch.object(archive_core, "LIMIT", 20), self.assertRaises(ValueError):
                archive_core.extract_archive(source, Path(folder) / "apps")

    def test_windows_executable_not_accepted(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "app.exe"
            path.write_bytes(b"MZexample")
            with self.assertRaises(ValueError):
                archive_core.command_for(path)

if __name__ == "__main__":
    unittest.main()


class IconTests(unittest.TestCase):
    """Les 49 tuiles, leur table et le thème doivent rester cohérents entre eux."""

    THEME = INC / "usr/share/icons/TI-LEX"
    TABLE = INC / "usr/share/ti-lex/filetypes.json"

    def setUp(self):
        import json
        self.data = json.loads(self.TABLE.read_text(encoding="utf-8"))

    def test_every_extension_points_to_an_existing_icon(self):
        names = {p.stem for p in (self.THEME / "scalable/mimetypes").glob("*.svg")}
        self.assertIn(self.data["fallback"], names)
        missing = {suffix: name for suffix, name in self.data["extensions"].items() if name not in names}
        self.assertEqual({}, missing)

    def test_extensions_are_lowercase_with_a_dot(self):
        for suffix in self.data["extensions"]:
            self.assertRegex(suffix, r"^\.[a-z0-9+]+$")

    def test_every_icon_is_well_formed_and_carries_its_label(self):
        icons = sorted((self.THEME / "scalable").rglob("*.svg"))
        self.assertEqual(49, len(icons))
        for icon in icons:
            tree = ET.parse(icon)
            self.assertEqual("{http://www.w3.org/2000/svg}svg", tree.getroot().tag)
            texts = [e.text for e in tree.iter("{http://www.w3.org/2000/svg}text") if e.text]
            self.assertTrue(texts, f"{icon.name} n'a pas de bandeau")

    def test_icon_lookup_falls_back_and_survives_a_missing_table(self):
        with tempfile.TemporaryDirectory() as folder:
            table = Path(folder) / "filetypes.json"
            icons = Path(folder) / "icons"
            icons.mkdir()
            (icons / "image-png.svg").write_text("<svg/>")
            (icons / "text-plain.svg").write_text("<svg/>")
            table.write_text(json.dumps({"mimetypes": str(icons), "fallback": "text-plain",
                                         "extensions": {".png": "image-png"}}))
            self.assertEqual("image-png.svg", archive_core.icon_file("A.PNG", table).name)
            self.assertEqual("text-plain.svg", archive_core.icon_file("a.inconnu", table).name)
            self.assertIsNone(archive_core.icon_file("a.png", Path(folder) / "absent.json"))

    def test_theme_inherits_so_unknown_icons_keep_working(self):
        index = (self.THEME / "index.theme").read_text(encoding="utf-8")
        self.assertIn("Inherits=Adwaita", index)
        self.assertIn("scalable/mimetypes", index)

