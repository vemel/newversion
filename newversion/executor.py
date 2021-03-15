"""
CLI commands executor.
"""

import operator

from newversion.constants import VersionParts
from newversion.type_defs import OperatorTypeDef, ReleaseNonLocalTypeDef, ReleaseTypeDef
from newversion.version import Version


class ExecutorError(Exception):
    """
    Main CLI commands executor error.
    """


class Executor:
    """
    CLI commands executor.
    """

    def __init__(
        self,
        input: Version = Version.zero(),
    ) -> None:
        self._input = input

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
        if release == VersionParts.LOCAL:
            return self._input.local[0] if self._input.local else ""

        if release == VersionParts.PRE:
            return f"{self._input.pre[0]}{self._input.pre[1]}" if self._input.pre else ""

        if release == VersionParts.POST:
            return str(self._input.post) if self._input.post else "0"

        if release == VersionParts.ALPHA:
            return (
                str(self._input.pre[-1]) if self._input.pre and self._input.pre[0] == "a" else "0"
            )

        if release == VersionParts.BETA:
            return (
                str(self._input.pre[-1]) if self._input.pre and self._input.pre[0] == "b" else "0"
            )

        if release == VersionParts.RC:
            return (
                str(self._input.pre[-1]) if self._input.pre and self._input.pre[0] == "rc" else "0"
            )

        if release == VersionParts.EPOCH:
            return str(self._input.epoch) if self._input.epoch else "0"

        result = dict(
            major=self._input.major,
            minor=self._input.minor,
            micro=self._input.micro,
        )[release]
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
        if (
            release == VersionParts.MAJOR
            or release == VersionParts.MINOR
            or release == VersionParts.MICRO
        ):
            return self._input.bump_release(release, increment)

        if release == VersionParts.PRE:
            return self._input.bump_prerelease(increment)

        if release == VersionParts.POST:
            return self._input.bump_postrelease(increment)

        if (
            release == VersionParts.RC
            or release == VersionParts.ALPHA
            or release == VersionParts.BETA
        ):
            return self._input.bump_prerelease(increment, release)

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
        if release == VersionParts.PRE:
            if self._input.prerelease_type == VersionParts.ALPHA:
                return self._input.replace(alpha=value)
            if self._input.prerelease_type == VersionParts.BETA:
                return self._input.replace(beta=value)
            if self._input.prerelease_type == VersionParts.RC:
                return self._input.replace(rc=value)

            return self._input.replace(rc=value)

        kwargs = {release: value}
        return self._input.replace(**kwargs)

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
        commands = dict(
            lt=(operator.lt, "not lesser than"),
            lte=(operator.le, "not lesser than or equal to"),
            gt=(operator.gt, "not greater than"),
            gte=(operator.ge, "not greater than or equal to"),
            eq=(operator.eq, "not equal to"),
            ne=(operator.ne, "equal to"),
        )
        op, message = commands[command]
        if not (op(self._input, other)):
            raise ExecutorError(f"Version {self._input} is {message} {other}")
