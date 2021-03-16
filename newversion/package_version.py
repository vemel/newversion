import logging
import re
from pathlib import Path
from typing import Optional

from newversion.constants import LOGGER_NAME
from newversion.eol_fixer import EOLFixer
from newversion.exceptions import PackageVersionError
from newversion.utils import print_path
from newversion.version import Version


class PackageVersion:
    RE_PYPROJECT = re.compile(r"^version\s*=\s*['\"](\S+)['\"]")
    RE_SETUP_CFG_FILE = re.compile(r"^version\s*=\s*file:\s*(\S+)")
    RE_SETUP_CFG = re.compile(r"^version\s*=\s*(\S+)")
    RE_SETUP_PY = re.compile(r"^\s*version\s*=\s*['\"](\S+)['\"]\s*,?")

    def __init__(self, path: Path) -> None:
        self._path = path
        self._logger = logging.getLogger(LOGGER_NAME)

    @property
    def _setup_py_path(self) -> Path:
        return self._path / "setup.py"

    @property
    def _setup_cfg_path(self) -> Path:
        return self._path / "setup.cfg"

    @property
    def _pyproject_path(self) -> Path:
        return self._path / "pyproject.toml"

    def _get_from_pyproject(self) -> Optional[Version]:
        if not self._pyproject_path.exists():
            return

        self._logger.debug(f"Found {print_path(self._pyproject_path)}, extracting version from it")
        text = self._pyproject_path.read_text()
        for line in text.splitlines():
            if not line.startswith("version"):
                continue

            match = self.RE_PYPROJECT.match(line)
            if not match:
                continue

            version_str = match.group(1)
            self._logger.debug(f"Version {version_str} found")
            return Version(version_str)

    def _set_in_pyproject(self, version: Version) -> None:
        if not self._pyproject_path.exists():
            return

        text = self._pyproject_path.read_text()
        line_ending = EOLFixer.get_line_ending(text)
        lines = []
        changed = False
        for line in text.splitlines():
            if not line.startswith("version"):
                lines.append(line)
                continue

            match = self.RE_PYPROJECT.match(line)
            if not match:
                lines.append(line)
                continue

            old_version = match.group(1)
            self._logger.info(
                f"Changing version in {print_path(self._pyproject_path)}"
                f" from {old_version} to {version.dumps()}"
            )
            new_line = line.replace(old_version, version.dumps())
            lines.append(new_line)
            changed = True

        if changed:
            text = EOLFixer.add_newline(line_ending.join(lines))
            self._pyproject_path.write_text(text)

    def _get_from_setup_cfg(self) -> Optional[Version]:
        if not self._setup_cfg_path.exists():
            return

        self._logger.debug(f"Found {print_path(self._setup_cfg_path)}, extracting version from it")
        text = self._setup_cfg_path.read_text()
        for line in text.splitlines():
            if not line.startswith("version"):
                continue

            match = self.RE_SETUP_CFG_FILE.match(line)
            if match:
                version_path = self._path / Path(match.group(1))
                self._logger.debug(f"Getting version from {match.group(1)}")
                return Version(version_path.read_text().strip())

            match = self.RE_SETUP_CFG.match(line)
            if not match:
                continue

            version_str = match.group(1)
            self._logger.debug(f"Version {version_str} found")
            return Version(version_str)

    def _set_in_setup_cfg(self, version: Version) -> None:
        if not self._setup_cfg_path.exists():
            return

        text = self._setup_cfg_path.read_text()
        line_ending = EOLFixer.get_line_ending(text)
        lines = []
        changed = False
        for line in text.splitlines():
            if not line.startswith("version"):
                lines.append(line)
                continue

            match = self.RE_SETUP_CFG_FILE.match(line)
            if match:
                version_path = self._path / Path(match.group(1))
                self._logger.info(f"Changing version in {match.group(1)} to {version.dumps()}")
                version_path.write_text(f"{version.dumps()}{line_ending}")
                return

            match = self.RE_SETUP_CFG.match(line)
            if not match:
                lines.append(line)
                continue

            old_version = match.group(1)
            self._logger.info(
                f"Changing version in {print_path(self._setup_cfg_path)}"
                f" from {old_version} to {version.dumps()}"
            )
            new_line = line.replace(old_version, version.dumps())
            lines.append(new_line)
            changed = True

        if changed:
            text = EOLFixer.add_newline(line_ending.join(lines))
            self._setup_cfg_path.write_text(text)

    def _get_from_setup_py(self) -> Optional[Version]:
        if not self._setup_py_path.exists():
            return

        self._logger.debug(f"Found {print_path(self._setup_py_path)}, extracting version from it")
        text = self._setup_py_path.read_text()
        for line in text.splitlines():
            if not line.lstrip().startswith("version"):
                continue

            match = self.RE_SETUP_PY.match(line)
            if not match:
                continue

            version_str = match.group(1)
            self._logger.debug(f"Version {version_str} found")
            return Version(version_str)

    def _set_in_setup_py(self, version: Version) -> None:
        if not self._setup_py_path.exists():
            return

        text = self._setup_py_path.read_text()
        line_ending = EOLFixer.get_line_ending(text)
        lines = []
        changed = False
        for line in text.splitlines():
            if not line.lstrip().startswith("version"):
                lines.append(line)
                continue

            match = self.RE_SETUP_PY.match(line)
            if not match:
                lines.append(line)
                continue

            old_version = match.group(1)
            self._logger.info(
                f"Changing version in {print_path(self._setup_py_path)}"
                f" from {old_version} to {version.dumps()}"
            )
            new_line = line.replace(old_version, version.dumps())
            lines.append(new_line)
            changed = True

        if changed:
            text = EOLFixer.add_newline(line_ending.join(lines))
            self._setup_py_path.write_text(text)

    def get(self) -> Version:
        result = self._get_from_pyproject()
        if result:
            return result
        result = self._get_from_setup_cfg()
        if result:
            return result
        result = self._get_from_setup_py()
        if result:
            return result

        raise PackageVersionError("Cannot get Python package version.")

    def set(self, version: Version) -> None:
        self._set_in_pyproject(version)
        self._set_in_setup_cfg(version)
        self._set_in_setup_py(version)
