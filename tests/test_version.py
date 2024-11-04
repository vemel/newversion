import pytest

from newversion.version import Version, VersionError


class TestVersion:
    def test_parse(self) -> None:
        assert Version.zero().dumps() == "0.0.0"
        assert Version("1.2.3").major == 1
        assert Version("1.2.3").minor == 2
        assert Version("1.2.3").micro == 3
        assert Version("1.2.3").pre is None
        assert Version("1.2.3rc4").pre == ("rc", 4)
        assert Version("1.2.3.alpha4").pre == ("a", 4)
        assert Version("1.2.3.alpha").pre == ("a", 0)
        assert Version("1.2.3-rc4").pre == ("rc", 4)
        assert Version("1.2.3.dev0").dev == 0
        assert Version("1.2.3.dev3").dev == 3
        assert Version("1.2.3-dev5").is_devrelease
        assert Version("1.2.3").is_stable
        assert not Version("1.2.3").is_devrelease
        assert not Version("1.2.3.dev4").is_stable
        assert Version("1.2.3.post3").is_stable
        assert Version("1.2.3.post3").is_postrelease

        with pytest.raises(VersionError):
            Version("invalid")

    def test_bump_major(self) -> None:
        assert Version.zero().bump_major().dumps() == "1.0.0"
        assert Version("1.2.3").bump_major().dumps() == "2.0.0"
        assert Version("1.2.3rc4").bump_major(2).dumps() == "3.0.0"
        assert Version("2.0.0").bump_major().dumps() == "3.0.0"
        assert Version("2.0.0rc4").bump_major().dumps() == "2.0.0"
        assert Version("2.1.0rc4").bump_major().dumps() == "3.0.0"
        assert Version("2.3.2.dev5").bump_major().dumps() == "3.0.0"
        assert Version("2.1.0rc4").bump_major(2).dumps() == "4.0.0"

    def test_bump_minor(self) -> None:
        assert Version("1.2.3").bump_minor().dumps() == "1.3.0"
        assert Version("1.2.3rc4").bump_minor(2).dumps() == "1.4.0"
        assert Version("1.2.3rc4").bump_minor(0).dumps() == "1.2.0"
        assert Version("1.3.0rc4").bump_minor().dumps() == "1.3.0"
        assert Version("1.3.0rc4").bump_minor(2).dumps() == "1.4.0"
        assert Version("2.3.2.dev5").bump_minor().dumps() == "2.4.0"
        assert Version("1").bump_minor().dumps() == "1.1.0"

    def test_bump_micro(self) -> None:
        assert Version("1.2.3").bump_micro().dumps() == "1.2.4"
        assert Version("1.2.3rc4").bump_micro().dumps() == "1.2.3"
        assert Version("1.2.3rc4").bump_micro(2).dumps() == "1.2.4"
        assert Version("1.2.3rc4").bump_micro(0).dumps() == "1.2.2"
        assert Version("2.3.2.dev5").bump_micro().dumps() == "2.3.2"
        assert Version("1").bump_micro().dumps() == "1.0.1"
        assert Version("1.2").bump_micro().dumps() == "1.2.1"

    def test_bump_prerelease(self) -> None:
        assert Version("1.2.3").bump_prerelease().dumps() == "1.2.4rc1"
        assert Version("2.3.2.dev5").bump_prerelease().dumps() == "2.3.2rc1"
        assert Version("1.2.3alpha").bump_prerelease().dumps() == "1.2.3a2"
        assert Version("3.4.5c9").bump_prerelease().dumps() == "3.4.5rc10"
        assert Version("1.2.3rc4").bump_prerelease(2).dumps() == "1.2.3rc6"
        assert Version("1.2.3rc4").bump_prerelease(2, "alpha").dumps() == "1.2.4a2"
        assert Version("1.2.3").bump_prerelease(2, "alpha").dumps() == "1.2.4a2"
        assert Version("1.2.3").bump_prerelease(2, "alpha", "major").dumps() == "2.0.0a2"
        assert Version("1.2.3a3").bump_prerelease(2, "alpha", "major").dumps() == "1.2.3a5"
        assert Version("1.2.3a3").bump_prerelease(2, "rc", "major").dumps() == "1.2.3rc2"

    def test_bump_postrelease(self) -> None:
        assert Version("1.2.3").bump_postrelease().dumps() == "1.2.3.post1"
        assert Version("1.2.3alpha").bump_postrelease().dumps() == "1.2.3.post1"
        assert Version("1.2.3.post4").bump_postrelease(2).dumps() == "1.2.3.post6"
        assert Version("1.2.3.post").bump_postrelease().dumps() == "1.2.3.post2"
        assert Version("1.2.3").bump_postrelease(2).dumps() == "1.2.3.post2"

    def test_bump_dev(self) -> None:
        assert Version("1.2.3").bump_dev().dumps() == "1.2.4.dev0"
        assert Version("4.5.6").bump_dev(1, "major").dumps() == "5.0.0.dev0"
        assert Version("8.9.10").bump_dev(2, "post").dumps() == "8.9.10.post1.dev1"
        assert Version("1.2.3.dev14").bump_dev(2).dumps() == "1.2.3.dev16"
        assert Version("1.2.3rc5").bump_dev().dumps() == "1.2.3rc5.dev0"
        assert Version("1.2.3alpha").bump_dev(2).dumps() == "1.2.3a0.dev1"
        assert Version("3.4.5.post3").bump_dev().dumps() == "3.4.5.post4.dev0"
        assert Version("2.3.4.post2.dev4").bump_dev().dumps() == "2.3.4.post2.dev5"
        assert Version("1.2.3.dev0+mylocal").bump_dev().dumps() == "1.2.3.dev1+mylocal"
        # should not bump release/postrelease if we're already a dev release
        assert Version("1.2.3.post3.dev2").bump_dev(1, "post").dumps() == "1.2.3.post3.dev3"
        # this also tests correcting a missing `.` in a dev release
        assert Version("1.2.3dev4").bump_dev(1, "major").dumps() == "1.2.3.dev5"
        # this also tests correcting an incorrect beta `.`
        assert Version("4.5.6.b6.dev33").bump_dev().dumps() == "4.5.6b6.dev34"

    def test_replace(self) -> None:
        assert Version("1.2.3").replace(dev=45).dumps() == "1.2.3.dev45"
        assert Version("1.2.3.dev14").replace(dev=36).dumps() == "1.2.3.dev36"
        assert Version("1.2.3-dev14").replace(dev=45).dumps() == "1.2.3.dev45"
        assert Version("1.2.3rc3").replace(dev=45).dumps() == "1.2.3rc3.dev45"
        assert Version("1.2.3rc3").replace(major=3).dumps() == "3.2.3rc3"
        assert Version("1.2.3rc3").replace(local="test-1").dumps() == "1.2.3rc3+test.1"

    def test_get_stable(self) -> None:
        assert Version("1.2.3").get_stable().dumps() == "1.2.3"
        assert Version("2.1.0a2").get_stable().dumps() == "2.1.0"
        assert Version("1.2.5.post3").get_stable().dumps() == "1.2.5"
        assert Version("3.4.5.dev4").get_stable().dumps() == "3.4.5"
        assert Version("4.5.6b3.dev4").get_stable().dumps() == "4.5.6"

    def test_comparison(self) -> None:
        assert Version("1.2.32") > Version("1.2.5")
        assert Version("1.2.3") > Version("1.2.3.rc3")
        assert Version("1.2.3.rc3") > Version("1.2.3.rc2")
        assert Version("1.2.3rc3") == Version("1.2.3.rc3")
        assert Version("1.2.3alpha3") == Version("1.2.3a3")
        assert Version("1.2.3.rc3") < Version("1.2.3.rc4")
        assert Version("1.2.3.rc3") < Version("1.2.3")
        assert Version("1.2.3.dev3") < Version("1.2.3a1")
        assert Version("1.2.3.post3") > Version("1.2.3")
        assert Version("1.2.3.dev0") > Version("1.2.2")
        assert Version("1.2.3.dev9") < Version("1.2.3")
