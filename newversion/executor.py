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
        self._input = version if version is not None else Version.zero()

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
            return self._input.local or ""

        if release_part == VersionParts.PRE:
            return f"{self._input.pre[0]}{self._input.pre[1]}" if self._input.pre else ""

        if release_part == VersionParts.POST:
            return str(self._input.post) if self._input.post else "0"

        if release_part == VersionParts.DEV:
            return str(self._input.dev) if self._input.dev else "0"

        if release_part == VersionParts.ALPHA:
            return (
                str(self._input.pre[-1]) if self._input.pre and self._input.pre[0] == "a" else "0"
            )

        if release_part == VersionParts.BETA:
            return (
                str(self._input.pre[-1]) if self._input.pre and self._input.pre[0] == "b" else "0"
            )

        if release_part == VersionParts.RC:
            return (
                str(self._input.pre[-1]) if self._input.pre and self._input.pre[0] == "rc" else "0"
            )

        if release_part == VersionParts.EPOCH:
            return str(self._input.epoch) if self._input.epoch else "0"

        result = {
            VersionParts.MAJOR: self._input.major,
            VersionParts.MINOR: self._input.minor,
            VersionParts.MICRO: self._input.micro,
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
            return self._input.bump_release(release_part.value, increment)

        if release_part == VersionParts.PRE:
            return self._input.bump_prerelease(increment)

        if release_part == VersionParts.POST:
            return self._input.bump_postrelease(increment)

        if release_part in (
            VersionParts.RC,
            VersionParts.ALPHA,
            VersionParts.BETA,
        ):
            return self._input.bump_prerelease(increment, release_part.value)

        if release_part == VersionParts.DEV:
            return self._input.bump_dev(increment)

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
            if self._input.prerelease_type == VersionParts.ALPHA.value:
                return self._input.replace(alpha=value)
            if self._input.prerelease_type == VersionParts.BETA.value:
                return self._input.replace(beta=value)
            if self._input.prerelease_type == VersionParts.RC.value:
                return self._input.replace(rc=value)

            return self._input.replace(rc=value)

        if release_part == VersionParts.POST:
            return self._input.replace(post=value)
        if release_part == VersionParts.EPOCH:
            return self._input.replace(epoch=value)
        if release_part == VersionParts.MAJOR:
            return self._input.replace(major=value)
        if release_part == VersionParts.MINOR:
            return self._input.replace(minor=value)
        if release_part == VersionParts.MICRO:
            return self._input.replace(micro=value)
        if release_part == VersionParts.ALPHA:
            return self._input.replace(alpha=value)
        if release_part == VersionParts.BETA:
            return self._input.replace(beta=value)
        if release_part == VersionParts.RC:
            return self._input.replace(rc=value)
        if release_part == VersionParts.DEV:
            return self._input.replace(dev=value)

        raise ExecutorError(f"Unknown release name: {release}") from None

    def command_stable(self) -> Version:
        """
        Get stable non-post, non-local version from current.

        Returns:
            A new Version.
        """
        return self._input.get_stable()

    def command_is_stable(self) -> None:
        """
        Check whether version is stable.

        Raises:
            ExecutorError -- If it is not.
        """
        if not self._input.is_stable:
            raise ExecutorError(f"Version {self._input} is not stable")

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
        if not (op(self._input, other)):
            raise ExecutorError(f"Version {self._input} is {message} {other}")

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

    def command_set_version(self) -> None:
        """
        Set the package version.

        This method attempts to set the package version to the value provided
        by `self._input`. If an error occurs during this process, it raises
        an `ExecutorError` with the original `PackageVersionError` as the cause.

        Raises:
            ExecutorError: If there is an error setting the package version.
        """
        try:
            PackageVersion(Path.cwd()).set(self._input)
        except PackageVersionError as e:
            raise ExecutorError(e) from None
