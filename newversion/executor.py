"""
CLI commands executor.
"""

import operator
from pathlib import Path
from typing import Optional

from newversion.constants import Commands, Prerelease, VersionParts
from newversion.exceptions import (
    ComparisonFailedError,
    ExecutorError,
    PackageVersionError,
    ReleaseCannotBeBumpedError,
    ValueMustBeIntError,
    VersionIsNotStableError,
)
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
            release: Release part name.

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
            release: Release name
            increment: Number to increase by

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

        raise ReleaseCannotBeBumpedError(release)

    def command_set(self, release: VersionParts, value: str) -> Version:
        """
        Set version part.

        Arguments:
            release: Release name
            value: Value to set

        Returns:
            A new Version.
        """
        if release == VersionParts.LOCAL:
            return self.version.replace(local=value)

        if not value.isdigit():
            raise ValueMustBeIntError(release, value)

        value_int = int(value)
        if release == VersionParts.PRE:
            return self.version.replace(
                alpha=value_int
                if self.version.prerelease_type == VersionParts.ALPHA.value
                else None,
                beta=value_int if self.version.prerelease_type == VersionParts.BETA.value else None,
                rc=value_int
                if self.version.prerelease_type in {VersionParts.RC.value, None}
                else None,
            )

        return self.version.replace(
            post=value_int if release == VersionParts.POST else None,
            epoch=value_int if release == VersionParts.EPOCH else None,
            major=value_int if release == VersionParts.MAJOR else None,
            minor=value_int if release == VersionParts.MINOR else None,
            micro=value_int if release == VersionParts.MICRO else None,
            alpha=value_int if release == VersionParts.ALPHA else None,
            beta=value_int if release == VersionParts.BETA else None,
            rc=value_int if release == VersionParts.RC else None,
            dev=value_int if release == VersionParts.DEV else None,
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
            ExecutorError: If it is not.
        """
        if not self.version.is_stable:
            raise VersionIsNotStableError(self.version)

    def command_compare(self, command: OperatorTypeDef, other: Version) -> None:
        """
        Execute compare command.

        Arguments:
            command: Compare operator.
            other: Version to compare to.

        Returns:
            Processed `Version`.
        """
        command_enum = Commands(command)
        operators = {
            Commands.LT: operator.lt,
            Commands.LTE: operator.le,
            Commands.GT: operator.gt,
            Commands.GTE: operator.ge,
            Commands.EQ: operator.eq,
            Commands.NE: operator.ne,
        }
        op = operators[command_enum]
        if not (op(self.version, other)):
            raise ComparisonFailedError(command_enum, self.version, other)

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
