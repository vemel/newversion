import tempfile
from pathlib import Path

from newversion.exceptions import PackageVersionError
from newversion.package_version import PackageVersion
from newversion.version import Version


class TestPackageVersion:
    def test_get(self):
        with tempfile.TemporaryDirectory() as path_str:
            path = Path(path_str)
            (path / "setup.py").write_text("\n\nsetup(\n    version ='1.2.3',\n)")
            assert PackageVersion(path).get() == Version("1.2.3")
            (path / "setup.cfg").write_text("name=mypackage\n\nversion = 1.2.4\n\n")
            assert PackageVersion(path).get() == Version("1.2.4")
            (path / "version.txt").write_text("1.2.5\n")
            (path / "setup.cfg").write_text("name=mypackage\n\nversion = file: version.txt\n\n")
            assert PackageVersion(path).get() == Version("1.2.5")
            (path / "pyproject.toml").write_text(
                '[tool.poetry]\nname= "mypackage"\n\nversion = "1.2.6"\n\n'
            )
            assert PackageVersion(path).get() == Version("1.2.6")

    def test_set(self):
        with tempfile.TemporaryDirectory() as path_str:
            path = Path(path_str)
            assert PackageVersion(path).set(Version("1.2.3")) is None
            (path / "setup.py").write_text("\n\nsetup(\n    version ='1.2.0',\n)")
            (path / "setup.cfg").write_text("name=mypackage\n\nversion= 1.1.0\n\n")
            (path / "pyproject.toml").write_text(
                '[tool.poetry]\nname= "mypackage"\n\nversion = "1.1.1"\n\n'
            )
            assert PackageVersion(path).set(Version("1.2.3")) is None
            assert (path / "setup.py").read_text() == "\n\nsetup(\n    version ='1.2.3',\n)\n"
            assert (path / "setup.cfg").read_text() == "name=mypackage\n\nversion= 1.2.3\n"
            assert (
                path / "pyproject.toml"
            ).read_text() == '[tool.poetry]\nname= "mypackage"\n\nversion = "1.2.3"\n'
            (path / "setup.cfg").write_text("name=mypackage\n\nversion = file: version.txt\n\n")
            assert PackageVersion(path).set(Version("1.2.3")) is None
            assert (path / "version.txt").read_text() == "1.2.3\n"
