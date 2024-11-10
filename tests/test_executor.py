from unittest.mock import patch

import pytest

from newversion.constants import VersionParts
from newversion.exceptions import (
    ComparisonFailedError,
    ExecutorError,
    PackageVersionError,
    ReleaseCannotBeBumpedError,
    VersionIsNotStableError,
)
from newversion.executor import Executor
from newversion.package_version import PackageVersion
from newversion.version import Version


class TestVersion:
    def test_command_get(self) -> None:
        executor = Executor(Version("1.2.3rc4"))
        assert executor.command_get(VersionParts.MAJOR) == "1"
        assert executor.command_get(VersionParts.MINOR) == "2"
        assert executor.command_get(VersionParts.MICRO) == "3"
        assert executor.command_get(VersionParts.RC) == "4"
        assert executor.command_get(VersionParts.PRE) == "rc4"
        assert executor.command_get(VersionParts.ALPHA) == "0"
        assert executor.command_get(VersionParts.BETA) == "0"
        assert executor.command_get(VersionParts.POST) == "0"
        assert executor.command_get(VersionParts.EPOCH) == "0"
        assert executor.command_get(VersionParts.DEV) == "0"
        assert Executor(Version("1.2.3a4")).command_get(VersionParts.ALPHA) == "4"
        assert Executor(Version("1.2.3b5")).command_get(VersionParts.BETA) == "5"
        assert Executor(Version("1.2.3.post7")).command_get(VersionParts.POST) == "7"
        assert Executor(Version("1.2.3.post6.dev2")).command_get(VersionParts.DEV) == "2"
        assert Executor(Version("1234!1.2.3.post7")).command_get(VersionParts.EPOCH) == "1234"
        assert (
            Executor(Version("1234!1.2.3.post7+localver")).command_get(VersionParts.LOCAL)
            == "localver"
        )

    def test_command_stable(self) -> None:
        assert Executor(Version("1.2.3a4")).command_stable() == Version("1.2.3")
        assert Executor(Version("1.2.4")).command_stable() == Version("1.2.4")
        assert Executor(Version("1.2.4.post4")).command_stable() == Version("1.2.4")
        assert Executor(Version("1234!1.2")).command_stable() == Version("1.2.0")

    def test_command_is_stable(self) -> None:
        assert Executor(Version("1.2.3")).command_is_stable() is None
        assert Executor(Version("1.2.3.post3")).command_is_stable() is None
        assert Executor(Version("123!1.2.3.post3")).command_is_stable() is None
        with pytest.raises(VersionIsNotStableError):
            Executor(Version("1.2.3a4")).command_is_stable()

    def test_command_compare(self) -> None:
        assert Executor(Version("1.2.3")).command_compare("lt", Version("1.3.0")) is None
        assert Executor(Version("1.3.0.dev3")).command_compare("lt", Version("1.3.0")) is None
        assert Executor(Version("1.2.3")).command_compare("lte", Version("1.3.0")) is None
        assert Executor(Version("1.2.3")).command_compare("gt", Version("1.2.0")) is None
        assert Executor(Version("1.2.3")).command_compare("gte", Version("1.2.3")) is None
        assert Executor(Version("1.2.3")).command_compare("eq", Version("1.2.3")) is None
        with pytest.raises(ComparisonFailedError):
            Executor(Version("1.2.3")).command_compare("ne", Version("1.2.3"))

    def test_command_set(self) -> None:
        assert Executor(Version("1.2.3")).command_set(VersionParts.MAJOR, 3) == Version("3.2.3")
        assert Executor(Version("1.2.3")).command_set(VersionParts.MINOR, 3) == Version("1.3.3")
        assert Executor(Version("1.2.3")).command_set(VersionParts.MICRO, 4) == Version("1.2.4")
        assert Executor(Version("1.2.3")).command_set(VersionParts.PRE, 4) == Version("1.2.3rc4")
        assert Executor(Version("1.2.3rc2")).command_set(VersionParts.PRE, 4) == Version("1.2.3rc4")
        assert Executor(Version("1.2.3a2")).command_set(VersionParts.PRE, 4) == Version("1.2.3a4")
        assert Executor(Version("1.2.3b2")).command_set(VersionParts.PRE, 4) == Version("1.2.3b4")
        assert Executor(Version("1.2.3")).command_set(VersionParts.EPOCH, 1234) == Version(
            "1234!1.2.3"
        )
        assert Executor(Version("1.2.3")).command_set(VersionParts.ALPHA, 4) == Version("1.2.3a4")
        assert Executor(Version("1.2.3")).command_set(VersionParts.BETA, 4) == Version("1.2.3b4")
        assert Executor(Version("1.2.3")).command_set(VersionParts.RC, 4) == Version("1.2.3rc4")
        assert Executor(Version("1.2.3")).command_set(VersionParts.POST, 5) == Version(
            "1.2.3.post5"
        )
        assert Executor(Version("1.2.3+local")).command_set(VersionParts.DEV, 0) == Version(
            "1.2.3.dev0+local"
        )

    def test_command_bump(self) -> None:
        assert Executor(Version("1.2.3")).command_bump(VersionParts.MAJOR, 3) == Version("4.0.0")
        assert Executor(Version("1.2.3")).command_bump(VersionParts.MINOR, 3) == Version("1.5.0")
        assert Executor(Version("1.2.3")).command_bump(VersionParts.MICRO, 3) == Version("1.2.6")
        assert Executor(Version("1.2.3")).command_bump(VersionParts.PRE, 3) == Version("1.2.4rc3")
        assert Executor(Version("1.2.3rc1")).command_bump(VersionParts.PRE, 3) == Version(
            "1.2.3rc4"
        )
        assert Executor(Version("1.2.3rc2")).command_bump(VersionParts.RC, 3) == Version("1.2.3rc5")
        assert Executor(Version("1.2.3rc2")).command_bump(VersionParts.ALPHA, 3) == Version(
            "1.2.4a3"
        )
        assert Executor(Version("1.2.3")).command_bump(VersionParts.POST, 1) == Version(
            "1.2.3.post1"
        )
        assert Executor(Version("1.2.3.post5")).command_bump(VersionParts.POST, 1) == Version(
            "1.2.3.post6"
        )
        assert Executor(Version("1.2.3")).command_bump(VersionParts.DEV, 1) == Version("1.2.4.dev0")
        with pytest.raises(ReleaseCannotBeBumpedError):
            Executor(Version("1.2.3.post5")).command_bump(VersionParts.EPOCH, 1)

    def test_command_get_version(self) -> None:
        with patch.object(PackageVersion, "get") as get_mock:
            get_mock.return_value = "test"
            assert Executor(Version("1.2.3")).command_get_version() == "test"
            get_mock.assert_called_with()
            get_mock.side_effect = PackageVersionError
            with pytest.raises(ExecutorError):
                Executor(Version("1.2.3")).command_get_version()

    def test_command_set_version(self) -> None:
        with patch.object(PackageVersion, "set") as set_mock:
            assert Executor(Version("1.2.0")).command_set_version(Version("1.2.3")) is None
            set_mock.assert_called_with(Version("1.2.3"))
            set_mock.side_effect = PackageVersionError
            with pytest.raises(ExecutorError):
                Executor(Version("1.2.0")).command_set_version(Version("1.2.3"))
