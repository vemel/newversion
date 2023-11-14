from unittest.mock import patch

import pytest

from newversion.exceptions import ExecutorError, PackageVersionError
from newversion.executor import Executor, ExecutorError
from newversion.package_version import PackageVersion
from newversion.version import Version


class TestVersion:
    def test_command_get(self):
        executor = Executor(Version("1.2.3rc4"))
        assert executor.command_get("major") == "1"
        assert executor.command_get("minor") == "2"
        assert executor.command_get("micro") == "3"
        assert executor.command_get("rc") == "4"
        assert executor.command_get("pre") == "rc4"
        assert executor.command_get("alpha") == "0"
        assert executor.command_get("beta") == "0"
        assert executor.command_get("post") == "0"
        assert executor.command_get("epoch") == "0"
        assert Executor(Version("1.2.3a4")).command_get("alpha") == "4"
        assert Executor(Version("1.2.3b5")).command_get("beta") == "5"
        assert Executor(Version("1.2.3.post7")).command_get("post") == "7"
        assert Executor(Version("1.2.3.post6.dev2")).command_get("dev") == "2"
        assert Executor(Version("1234!1.2.3.post7")).command_get("epoch") == "1234"
        assert Executor(Version("1234!1.2.3.post7+localver")).command_get("local") == "localver"

    def test_command_stable(self):
        assert Executor(Version("1.2.3a4")).command_stable() == Version("1.2.3")
        assert Executor(Version("1.2.4")).command_stable() == Version("1.2.4")
        assert Executor(Version("1.2.4.post4")).command_stable() == Version("1.2.4")
        assert Executor(Version("1234!1.2")).command_stable() == Version("1.2.0")

    def test_command_is_stable(self):
        assert Executor(Version("1.2.3")).command_is_stable() is None
        assert Executor(Version("1.2.3.post3")).command_is_stable() is None
        assert Executor(Version("123!1.2.3.post3")).command_is_stable() is None
        with pytest.raises(ExecutorError):
            Executor(Version("1.2.3a4")).command_is_stable()

    def test_command_compare(self):
        assert Executor(Version("1.2.3")).command_compare("lt", Version("1.3.0")) is None
        assert Executor(Version("1.3.0.dev3")).command_compare("lt", Version("1.3.0")) is None
        assert Executor(Version("1.2.3")).command_compare("lte", Version("1.3.0")) is None
        assert Executor(Version("1.2.3")).command_compare("gt", Version("1.2.0")) is None
        assert Executor(Version("1.2.3")).command_compare("gte", Version("1.2.3")) is None
        assert Executor(Version("1.2.3")).command_compare("eq", Version("1.2.3")) is None
        with pytest.raises(ExecutorError):
            Executor(Version("1.2.3")).command_compare("ne", Version("1.2.3"))

    def test_command_set(self):
        assert Executor(Version("1.2.3")).command_set("major", 3) == Version("3.2.3")
        assert Executor(Version("1.2.3")).command_set("minor", 3) == Version("1.3.3")
        assert Executor(Version("1.2.3")).command_set("micro", 4) == Version("1.2.4")
        assert Executor(Version("1.2.3")).command_set("pre", 4) == Version("1.2.3rc4")
        assert Executor(Version("1.2.3rc2")).command_set("pre", 4) == Version("1.2.3rc4")
        assert Executor(Version("1.2.3a2")).command_set("pre", 4) == Version("1.2.3a4")
        assert Executor(Version("1.2.3b2")).command_set("pre", 4) == Version("1.2.3b4")
        assert Executor(Version("1.2.3")).command_set("epoch", 1234) == Version("1234!1.2.3")
        assert Executor(Version("1.2.3")).command_set("alpha", 4) == Version("1.2.3a4")
        assert Executor(Version("1.2.3")).command_set("beta", 4) == Version("1.2.3b4")
        assert Executor(Version("1.2.3")).command_set("rc", 4) == Version("1.2.3rc4")
        assert Executor(Version("1.2.3")).command_set("post", 5) == Version("1.2.3.post5")
        assert Executor(Version("1.2.3+local")).command_set("dev", 0) == Version("1.2.3.dev0+local")

    def test_command_bump(self):
        assert Executor(Version("1.2.3")).command_bump("major", 3) == Version("4.0.0")
        assert Executor(Version("1.2.3")).command_bump("minor", 3) == Version("1.5.0")
        assert Executor(Version("1.2.3")).command_bump("micro", 3) == Version("1.2.6")
        assert Executor(Version("1.2.3")).command_bump("pre", 3) == Version("1.2.4rc3")
        assert Executor(Version("1.2.3rc1")).command_bump("pre", 3) == Version("1.2.3rc4")
        assert Executor(Version("1.2.3rc2")).command_bump("rc", 3) == Version("1.2.3rc5")
        assert Executor(Version("1.2.3rc2")).command_bump("alpha", 3) == Version("1.2.4a3")
        assert Executor(Version("1.2.3")).command_bump("post", 1) == Version("1.2.3.post1")
        assert Executor(Version("1.2.3.post5")).command_bump("post", 1) == Version("1.2.3.post6")
        assert Executor(Version("1.2.3")).command_bump("dev", 1) == Version("1.2.4.dev0")
        with pytest.raises(ExecutorError):
            Executor(Version("1.2.3.post5")).command_bump("unknown", 1)

    def test_command_get_version(self):
        with patch.object(PackageVersion, "get") as get_mock:
            get_mock.return_value = "test"
            assert Executor(Version("1.2.3")).command_get_version() == "test"
            get_mock.assert_called_with()
            get_mock.side_effect = PackageVersionError
            with pytest.raises(ExecutorError):
                Executor(Version("1.2.3")).command_get_version()

    def test_command_set_version(self):
        with patch.object(PackageVersion, "set") as set_mock:
            assert Executor(Version("1.2.3")).command_set_version() is None
            set_mock.assert_called_with(Version("1.2.3"))
            set_mock.side_effect = PackageVersionError
            with pytest.raises(ExecutorError):
                Executor(Version("1.2.3")).command_set_version()
