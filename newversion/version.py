"""
Extended `packaging.version.Version` implementation.
"""

from typing import Any, Optional, Union

import packaging.version
from typing_extensions import Self

from newversion.constants import Prerelease, VersionParts
from newversion.type_defs import (
    BaseVersion,
    PrereleaseLooseTypeDef,
    PrereleaseTypeDef,
    ReleaseMainPostTypeDef,
    ReleaseMainTypeDef,
)


class VersionError(packaging.version.InvalidVersion):
    """
    Wrapper for InvalidVersion error.
    """


class Version(packaging.version.Version):
    """
    Extended `packaging.version.Version` implementation.
    """

    def __init__(self, version: str) -> None:
        try:
            super().__init__(version)
        except packaging.version.InvalidVersion as e:
            raise VersionError(e) from None

    @classmethod
    def zero(cls) -> Self:
        """
        Get zero version `0.0.0`.
        """
        return cls("0.0.0")

    def dumps(self) -> str:
        """
        Render to string.
        """
        return str(self)

    @property
    def prerelease_type(self) -> Optional[PrereleaseTypeDef]:
        """
        Repease type as VersionParts.
        """
        if not self.pre:
            return None

        letter = self.pre[0]
        if letter == Prerelease.RC:
            return VersionParts.RC.value
        if letter == Prerelease.A:
            return VersionParts.ALPHA.value
        if letter == Prerelease.B:
            return VersionParts.BETA.value

        return None

    @property
    def base(self) -> BaseVersion:
        """
        Underlying version NamedTuple.
        """
        return self._version

    @base.setter
    def base(self, base: BaseVersion) -> None:
        self._version = base

    def copy(self) -> Self:
        """
        Create a copy of a current version instance.
        """
        return self.__class__(self.dumps())

    def _replace(self, base: BaseVersion) -> Self:
        new_version = self.copy()
        new_version.base = base
        return new_version.copy()

    def bump_release(
        self,
        release_type: ReleaseMainTypeDef = VersionParts.MICRO.value,
        inc: int = 1,
    ) -> Self:
        """
        Get next release version.

        Arguments:
            release_type: Release type: major, minor, micro.
            inc: Increment for major version.

        Examples:
            ```python
            Version("1.2.3").bump_release()  # "1.2.4"
            Version("1.2.3").bump_release("major")  # "2.0.0"
            Version("1.2.3.dev14").bump_release("minor", 2)  # "1.4.0"
            ```

        Returns:
            A new copy.
        """
        if release_type == VersionParts.MAJOR.value:
            return self.bump_major(inc)
        if release_type == VersionParts.MINOR.value:
            return self.bump_minor(inc)

        return self.bump_micro(inc)

    def bump_major(self, inc: int = 1) -> Self:
        """
        Get next major version.

        Arguments:
            inc: Increment for major version.

        Examples:
            ```python
            Version("1.2.3").bump_major()  # "2.0.0"
            Version("1.2.3.dev14").bump_major()  # "2.0.0"
            Version("1.2.3a5").bump_major()  # "2.0.0"
            Version("1.2.3rc3").bump_major(2)  # "3.0.0"
            Version("1.2.3rc3").bump_major(0)  # "1.0.0"
            ```

        Returns:
            A new copy.
        """
        if not self.is_stable and self.minor == 0 and self.micro == 0:
            return self.get_stable().bump_major(inc - 1)

        return self._replace(
            BaseVersion(
                epoch=0,
                release=(self.major + inc, 0, 0),
                pre=None,
                post=None,
                dev=None,
                local=None,
            )
        )

    def bump_minor(self, inc: int = 1) -> Self:
        """
        Get next minor version.

        Arguments:
            inc: Increment for minor version.

        Examples:
            ```python
            Version("1.2.3").bump_minor()  # "1.3.0"
            Version("1.2.3.dev14").bump_minor()  # "1.3.0"
            Version("1.2.3a5").bump_minor()  # "1.3.0"
            Version("1.2.3rc3").bump_minor(2)  # "1.4.0"
            Version("1.2.3rc3").bump_minor(0)  # "1.2.0"
            Version("1.3.0rc3").bump_minor()  # "1.3.0"
            Version("1.3.0rc3").bump_minor(2)  # "1.4.0"
            ```

        Returns:
            A new copy.
        """
        if not self.is_stable and self.micro == 0:
            return self.get_stable().bump_minor(inc - 1)

        return self._replace(
            BaseVersion(
                epoch=0,
                release=(self.major, self.minor + inc, 0),
                pre=None,
                post=None,
                dev=None,
                local=None,
            )
        )

    def bump_micro(self, inc: int = 1) -> Self:
        """
        Get next micro version.

        Arguments:
            inc: Increment for micro version.

        Examples:
            ```python
            Version("1.2.3").bump_micro()  # "1.2.4"
            Version("1.2.3.dev14").bump_micro()  # "1.2.4"
            Version("1.2.3a5").bump_micro()  # "1.2.4"
            Version("1.2.3rc3").bump_micro(2)  # "1.2.5"
            Version("1.2.3rc3").bump_micro(0)  # "1.2.3"
            ```

        Returns:
            A new copy.
        """
        if not self.is_stable:
            return self.get_stable().bump_micro(inc - 1)

        return self._replace(
            BaseVersion(
                epoch=0,
                release=(self.major, self.minor, self.micro + inc),
                pre=None,
                post=None,
                dev=None,
                local=None,
            )
        )

    def bump_dev(
        self,
        inc: int = 1,
        bump_release: ReleaseMainPostTypeDef = "micro",
    ) -> Self:
        """
        Get next dev version.

        If version is stable - bump release for proper versioning as well.
        Defaults to bumping `micro`, falls back automatically to `post`

        Arguments:
            inc: Increment for dev version.
            bump_release: Release number to bump if version is stable.

        Examples:
            ```python
            Version("1.2.3").bump_dev()  # "1.2.4.dev0"
            Version("1.2.3").bump_dev(1, 'minor')  # "1.3.0.dev0"
            Version("1.2.3.dev14").bump_dev()  # "1.2.3.dev15"
            Version("1.2.3a4).bump_dev()  # "1.2.3a4.dev0"
            Version("1.2.3b5.dev9").bump_dev()  # "1.2.3b5.dev10"
            Version("1.2.3.dev3").bump_dev(2)  # "1.2.3.dev5"
            Version("1.2.3.post4").bump_dev()  # "1.2.3.post5.dev0"
            ```

        Returns:
            A new copy.
        """
        if self.is_devrelease:
            # this is a dev release already, increment the dev value
            dev_version = self.dev or 0
            return self.replace(dev=(dev_version + inc))

        if bump_release == VersionParts.POST.value or self.is_postrelease:
            # this is a postrelease or we want to create one
            return self.bump_postrelease().replace(dev=(inc - 1))

        if self.is_stable:
            # this is a stable release and we want to bump the release and add dev
            return self.bump_release(bump_release).replace(dev=(inc - 1))

        return self.replace(dev=(inc - 1))

    def bump_prerelease(
        self,
        inc: int = 1,
        release_type: Optional[PrereleaseLooseTypeDef] = None,
        bump_release: ReleaseMainTypeDef = VersionParts.MICRO.value,
    ) -> Self:
        """
        Get next prerelease version.

        If version is stable - bump `micro` for proper versioning as well.
        Defaults to `rc` pre-releases.

        Arguments:
            inc: Increment for micro version.
            release_type: Prerelease type: alpha, beta, rc.
            bump_release: Release number to bump if version is stable.

        Examples:
            ```python
            Version("1.2.3").bump_prerelease()  # "1.2.4rc1"
            Version("1.2.3").bump_prerelease(bump_release="major")  # "2.0.0rc1"
            Version("1.2.3.dev14").bump_prerelease()  # "1.2.3rc1"
            Version("1.2.3a5").bump_prerelease()  # "1.2.3a6"
            Version("1.2.3rc3").bump_prerelease(2, "beta")  # "1.2.3rc5"
            ```

        Returns:
            A new copy.
        """
        prerelease_type = release_type or self.prerelease_type or VersionParts.RC.value
        increment = inc if not self.base.pre else (max(self.base.pre[-1], 1) + inc)
        pre = (prerelease_type, increment)

        new_version = self._replace(self._copy_base(pre=pre))
        if new_version < self:
            prerelease_type = release_type or VersionParts.RC.value
            new_version = self.get_stable().bump_release(bump_release)

        if prerelease_type != self.prerelease_type:
            increment = inc

        base = BaseVersion(
            epoch=0,
            release=new_version.base.release,
            pre=(prerelease_type, increment),
            post=None,
            dev=None,
            local=None,
        )
        return self._replace(base)

    def bump_postrelease(self, inc: int = 1) -> Self:
        """
        Get next postrelease version.

        Arguments:
            inc: Increment for micro version.

        Examples:
            ```python
            Version("1.2.3").bump_postrelease()  # "1.2.3.post1"
            Version("1.2.3.post3").bump_postrelease()  # "1.2.3.post4"
            Version("1.2.3a5").bump_postrelease()  # "1.2.3.post1"
            Version("1.2.3.post4").bump_postrelease(2)  # "1.2.3.post6"
            ```

        Returns:
            A new copy.
        """
        post = (VersionParts.POST.value, max(inc, 1))
        base_post: Optional[tuple[str, int]] = self._version.post
        if base_post:
            post = (VersionParts.POST.value, max(base_post[1], 1) + inc)
        base = BaseVersion(
            epoch=0,
            release=self._version.release,
            pre=None,
            post=post,
            dev=None,
            local=None,
        )
        return self._replace(base)

    def replace(
        self,
        major: Optional[int] = None,
        minor: Optional[int] = None,
        micro: Optional[int] = None,
        *,
        alpha: Optional[int] = None,
        beta: Optional[int] = None,
        rc: Optional[int] = None,
        dev: Optional[int] = None,
        post: Optional[int] = None,
        epoch: Optional[int] = None,
        local: Optional[str] = None,
    ) -> Self:
        """
        Modify version parts.

        Examples:
            ```python
            Version("1.2.3").replace(dev=24) # "1.2.3.dev24"
            Version("1.2.3rc5").replace(17) # "1.2.3.dev17"
            ```

        Arguments:
            major: Major release number.
            minor: Minor release number.
            micro: Micro release number.
            alpha: Alpha pre-release number.
            beta: Beta pre-release number.
            rc: RC pre-release number.
            dev: Dev release number.
            post: Post release number.
            epoch: Release epoch.
            local: Local release identifier.

        Returns:
            A new instance.
        """
        kwargs: dict[str, Any] = {
            "release": (
                major if major is not None else self.major,
                minor if minor is not None else self.minor,
                micro if micro is not None else self.micro,
            )
        }
        if alpha is not None:
            kwargs[VersionParts.PRE.value] = (VersionParts.ALPHA.value, alpha)
        if beta is not None:
            kwargs[VersionParts.PRE.value] = (VersionParts.BETA.value, beta)
        if rc is not None:
            kwargs[VersionParts.PRE.value] = (VersionParts.RC.value, rc)
        if dev is not None:
            kwargs[VersionParts.DEV.value] = (VersionParts.DEV.value, dev)
        if post is not None:
            kwargs[VersionParts.POST.value] = (VersionParts.POST.value, post)
        if epoch is not None:
            kwargs[VersionParts.EPOCH.value] = epoch
        if local is not None:
            kwargs[VersionParts.LOCAL.value] = [local]

        return self._replace(self._copy_base(**kwargs))

    @property
    def is_stable(self) -> bool:
        """
        Whether version is not prerelease or devrelease.

        Returns:
            True if it is stable.
        """
        return not self.is_prerelease

    def get_stable(self) -> Self:
        """
        Get stable version from pre- or post- release.

        Examples:
            ```python
            Version("1.2.3").get_stable() # "1.2.3"
            Version("2.1.0a2").get_stable() # "2.1.0"
            Version("1.2.5.post3").get_stable() # "1.2.5"
            ```

        Returns:
            A new instance.
        """
        return self._replace(
            BaseVersion(
                epoch=0,
                release=(self.major, self.minor, self.micro),
                pre=None,
                post=None,
                dev=None,
                local=None,
            )
        )

    def _copy_base(
        self,
        *,
        epoch: Optional[int] = None,
        release: Optional[tuple[int, ...]] = None,
        dev: Optional[tuple[str, int]] = None,
        pre: Optional[tuple[str, int]] = None,
        post: Optional[tuple[str, int]] = None,
        local: Optional[tuple[Union[int, str], ...]] = None,
    ) -> BaseVersion:
        return BaseVersion(
            epoch=epoch if epoch is not None else self.base.epoch,
            release=release if release is not None else self.base.release,
            pre=pre if pre is not None else self.base.pre,
            post=post if post is not None else self.base.post,
            dev=dev if dev is not None else self.base.dev,
            local=local if local is not None else self.base.local,
        )
