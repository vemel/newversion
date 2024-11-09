"""
CLI commands executor.
"""

import operator
from pathlib import Path
from typing import Optional

from newversion.constants import Commands, Prerelease, VersionParts
from newversion.exceptions import ExecutorError, PackageVersionError
from newversion.package_version import PackageVersion
from newversion.type_defs import OperatorTypeDef
from newversion.version import Version


class Executor:
    """
    CLI commands executor.
    """

    def __init__(
        self,
        version: Optional[Version] = None,
        path: Optional[Path] = None,
    ) -> None:
        self.path = path or Path.cwd()
        self.version = version if version is not None else Version.zero()

    def command_get(
        self,
        release: VersionParts,
    ) -> str:
        """
        Get version part.

        Arguments:
            release -- Release part name.

        Returns:
            Part as a string.
        """
        if release == VersionParts.LOCAL:
            return self.version.local or ""

        if release == VersionParts.PRE:
            return f"{self.version.pre[0]}{self.version.pre[1]}" if self.version.pre else ""

        if release == VersionParts.POST:
            return str(self.version.post) if self.version.post else "0"

        if release == VersionParts.DEV:
            return str(self.version.dev) if self.version.dev else "0"

        if release == VersionParts.ALPHA:
            return (
                str(self.version.pre[-1])
                if self.version.pre and self.version.pre[0] == Prerelease.A
                else "0"
            )

        if release == VersionParts.BETA:
            return (
                str(self.version.pre[-1])
                if self.version.pre and self.version.pre[0] == Prerelease.B
                else "0"
            )

        if release == VersionParts.RC:
            return (
                str(self.version.pre[-1])
                if self.version.pre and self.version.pre[0] == Prerelease.RC
                else "0"
            )

        if release == VersionParts.EPOCH:
            return str(self.version.epoch) if self.version.epoch else "0"

        if release == VersionParts.FULL:
            return str(self.version)

        result = {
            VersionParts.MAJOR: self.version.major,
            VersionParts.MINOR: self.version.minor,
            VersionParts.MICRO: self.version.micro,
        }[release]
        return str(result)

    def command_bump(self, release: VersionParts, increment: int) -> Version:
        """
        Bump release.

        Arguments:
            release -- Release name
            increment -- Number to increase by

        Returns:
            A new Version.
        """
        if release in (
            VersionParts.MAJOR,
            VersionParts.MINOR,
            VersionParts.MICRO,
        ):
            return self.version.bump_release(release.value, increment)

        if release == VersionParts.PRE:
            return self.version.bump_prerelease(increment)

        if release == VersionParts.POST:
            return self.version.bump_postrelease(increment)

        if release in (
            VersionParts.RC,
            VersionParts.ALPHA,
            VersionParts.BETA,
        ):
            return self.version.bump_prerelease(increment, release.value)

        if release == VersionParts.DEV:
            return self.version.bump_dev(increment)

        raise ExecutorError(f"Unknown release name: {release}")

    def command_set(self, release: VersionParts, value: int) -> Version:
        """
        Set version part.

        Arguments:
            release -- Release name
            value -- Value to set

        Returns:
            A new Version.
        """
        if release == VersionParts.PRE:
            return self.version.replace(
                alpha=value if self.version.prerelease_type == VersionParts.ALPHA.value else None,
                beta=value if self.version.prerelease_type == VersionParts.BETA.value else None,
                rc=value if self.version.prerelease_type in {VersionParts.RC.value, None} else None,
            )

        return self.version.replace(
            post=value if release == VersionParts.POST else None,
            epoch=value if release == VersionParts.EPOCH else None,
            major=value if release == VersionParts.MAJOR else None,
            minor=value if release == VersionParts.MINOR else None,
            micro=value if release == VersionParts.MICRO else None,
            alpha=value if release == VersionParts.ALPHA else None,
            beta=value if release == VersionParts.BETA else None,
            rc=value if release == VersionParts.RC else None,
            dev=value if release == VersionParts.DEV else None,
        )

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
            return PackageVersion(self.path).get()
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
            PackageVersion(self.path).set(version)
        except PackageVersionError as e:
            raise ExecutorError(e) from None
