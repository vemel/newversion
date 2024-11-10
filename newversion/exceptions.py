"""
Exceptions.
"""

from newversion.constants import Commands, VersionParts
from newversion.version import Version


class PackageVersionError(Exception):
    """
    Main PackageVersion error.
    """

    def __init__(self) -> None:
        self.message = "Cannot get Python package version."
        super().__init__(self.message)


class ExecutorError(Exception):
    """
    Main CLI commands executor error.
    """


class CLIError(Exception):
    """
    Main CLI error.
    """


class ComparisonFailedError(ExecutorError):
    """
    Comparison failed error.
    """

    def __init__(self, command: Commands, version: Version, other: Version) -> None:
        message_parts = {
            Commands.LT: "not lesser than",
            Commands.LTE: "not lesser than or equal to",
            Commands.GT: "not greater than",
            Commands.GTE: "not greater than or equal to",
            Commands.EQ: "not equal to",
            Commands.NE: "equal to",
        }
        message_part = message_parts[command]
        self.message = f"Version {version} is {message_part} {other}"
        super().__init__(self.message)


class VersionIsNotStableError(ExecutorError):
    """
    Version is not stable error.
    """

    def __init__(self, version: Version) -> None:
        self.message = f"Version {version} is not stable"
        super().__init__(self.message)


class ReleaseCannotBeBumpedError(ExecutorError):
    """
    Unsupported bump release error.
    """

    def __init__(self, release: VersionParts) -> None:
        self.message = f"Unsupported release {release.value} for bump operation"
        super().__init__(self.message)
