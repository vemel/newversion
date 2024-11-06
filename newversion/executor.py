"""
CLI commands executor.
"""

import operator
from pathlib import Path
from typing import Optional

from newversion.constants import Commands, VersionParts
from newversion.exceptions import ExecutorError, PackageVersionError
from newversion.package_version import PackageVersion
from newversion.type_defs import OperatorTypeDef, ReleaseNonLocalTypeDef, ReleaseTypeDef
from newversion.version import Version


class Executor:
    """
    CLI commands executor.
    """

    def __init__(
        self,
        version: Optional[Version] = None,
    ) -> None:
        self.version = version if version is not None else Version.zero()

    def command_get(
        self,
        release: ReleaseTypeDef,
    ) -> str:
        """
        Get version part.

        Arguments:
            release -- Release part name.

        Returns:
            Part as a string.
        """
        try:
            release_part = VersionParts(release)
        except ValueError:
            raise ExecutorError(f"Unknown release name: {release}") from None

        if release_part == VersionParts.LOCAL:
            return self.version.local or ""

        if release_part == VersionParts.PRE:
            return f"{self.version.pre[0]}{self.version.pre[1]}" if self.version.pre else ""

        if release_part == VersionParts.POST:
            return str(self.version.post) if self.version.post else "0"

        if release_part == VersionParts.DEV:
            return str(self.version.dev) if self.version.dev else "0"

        if release_part == VersionParts.ALPHA:
            return (
                str(self.version.pre[-1])
                if self.version.pre and self.version.pre[0] == "a"
                else "0"
            )

        if release_part == VersionParts.BETA:
            return (
                str(self.version.pre[-1])
                if self.version.pre and self.version.pre[0] == "b"
                else "0"
            )

        if release_part == VersionParts.RC:
            return (
                str(self.version.pre[-1])
                if self.version.pre and self.version.pre[0] == "rc"
                else "0"
            )

        if release_part == VersionParts.EPOCH:
            return str(self.version.epoch) if self.version.epoch else "0"

        if release_part == VersionParts.FULL:
            return str(self.version)

        result = {
            VersionParts.MAJOR: self.version.major,
            VersionParts.MINOR: self.version.minor,
            VersionParts.MICRO: self.version.micro,
        }[release_part]
        return str(result)

    def command_bump(self, release: ReleaseNonLocalTypeDef, increment: int) -> Version:
        """
        Bump release.

        Arguments:
            release -- Release name
            increment -- Number to increase by

        Returns:
            A new Version.
        """
        try:
            release_part = VersionParts(release)
        except ValueError:
            raise ExecutorError(f"Unknown release name: {release}") from None

        if release_part in (
            VersionParts.MAJOR,
            VersionParts.MINOR,
            VersionParts.MICRO,
        ):
            return self.version.bump_release(release_part.value, increment)

        if release_part == VersionParts.PRE:
            return self.version.bump_prerelease(increment)

        if release_part == VersionParts.POST:
            return self.version.bump_postrelease(increment)

        if release_part in (
            VersionParts.RC,
            VersionParts.ALPHA,
            VersionParts.BETA,
        ):
            return self.version.bump_prerelease(increment, release_part.value)

        if release_part == VersionParts.DEV:
            return self.version.bump_dev(increment)

        raise ExecutorError(f"Unknown release name: {release}")

    def command_set(self, release: ReleaseNonLocalTypeDef, value: int) -> Version:
        """
        Set version part.

        Arguments:
            release -- Release name
            value -- Value to set

        Returns:
            A new Version.
        """
        try:
            release_part = VersionParts(release)
        except ValueError:
            raise ExecutorError(f"Unknown release name: {release}") from None

        if release_part == VersionParts.PRE:
            if self.version.prerelease_type == VersionParts.ALPHA.value:
                return self.version.replace(alpha=value)
            if self.version.prerelease_type == VersionParts.BETA.value:
                return self.version.replace(beta=value)
            if self.version.prerelease_type == VersionParts.RC.value:
                return self.version.replace(rc=value)

            return self.version.replace(rc=value)

        if release_part == VersionParts.POST:
            return self.version.replace(post=value)
        if release_part == VersionParts.EPOCH:
            return self.version.replace(epoch=value)
        if release_part == VersionParts.MAJOR:
            return self.version.replace(major=value)
        if release_part == VersionParts.MINOR:
            return self.version.replace(minor=value)
        if release_part == VersionParts.MICRO:
            return self.version.replace(micro=value)
        if release_part == VersionParts.ALPHA:
            return self.version.replace(alpha=value)
        if release_part == VersionParts.BETA:
            return self.version.replace(beta=value)
        if release_part == VersionParts.RC:
            return self.version.replace(rc=value)
        if release_part == VersionParts.DEV:
            return self.version.replace(dev=value)

        raise ExecutorError(f"Unknown release name: {release}") from None

    def command_stable(self) -> Version:
        """
        Get stable non-post, non-local version from current.

        Returns:
            A new Version.
        """
        return self.version.get_stable()

    def command_is_stable(self) -> None:
        """
        Check whether version is stable.

        Raises:
            ExecutorError -- If it is not.
        """
        if not self.version.is_stable:
            raise ExecutorError(f"Version {self.version} is not stable")

    def command_compare(self, command: OperatorTypeDef, other: Version) -> None:
        """
        Execute compare command.

        Arguments:
            command -- Compare operator.
            other -- Version to compare to.

        Returns:
            Processed `Version`.
        """
        command_enum = Commands(command)
        commands = {
            Commands.LT: (operator.lt, "not lesser than"),
            Commands.LTE: (operator.le, "not lesser than or equal to"),
            Commands.GT: (operator.gt, "not greater than"),
            Commands.GTE: (operator.ge, "not greater than or equal to"),
            Commands.EQ: (operator.eq, "not equal to"),
            Commands.NE: (operator.ne, "equal to"),
        }
        op, message = commands[command_enum]
        if not (op(self.version, other)):
            raise ExecutorError(f"Version {self.version} is {message} {other}")

    def command_get_version(self) -> Version:
        """
        Retrieve the current version of the package.

        This method attempts to get the current version of the package by
        using the PackageVersion class. If an error occurs during this
        process, it raises an ExecutorError.

        Returns:
            Version: The current version of the package.

        Raises:
            ExecutorError: If there is an error retrieving the package version.
        """
        try:
            return PackageVersion(Path.cwd()).get()
        except PackageVersionError as e:
            raise ExecutorError(e) from None

    def command_set_version(self, version: Version) -> None:
        """
        Set the package version.

        This method attempts to set the package version to the value provided
        by `self._input`. If an error occurs during this process, it raises
        an `ExecutorError` with the original `PackageVersionError` as the cause.

        Raises:
            ExecutorError: If there is an error setting the package version.
        """
        try:
            PackageVersion(Path.cwd()).set(version)
        except PackageVersionError as e:
            raise ExecutorError(e) from None
