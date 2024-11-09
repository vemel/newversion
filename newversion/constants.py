"""
Constants used in project.
"""

import enum
from typing import Final

PACKAGE_NAME: Final = "newversion"
LOGGER_NAME: Final = "newversion"


class Prerelease:
    """
    Pre-release constants as they are named in PEP 440.
    """

    A: Final = "a"
    B: Final = "b"
    RC: Final = "rc"


class VersionParts(enum.Enum):
    """
    Utility class with constants for version parts.
    """

    ALPHA = "alpha"
    BETA = "beta"
    RC = "rc"
    PRE = "pre"
    POST = "post"
    DEV = "dev"
    MAJOR = "major"
    MINOR = "minor"
    MICRO = "micro"
    LOCAL = "local"
    EPOCH = "epoch"
    FULL = "full"


class Commands(enum.Enum):
    """
    CLI commands.
    """

    LT = "lt"
    LTE = "lte"
    GT = "gt"
    GTE = "gte"
    EQ = "eq"
    NE = "ne"

    IS_STABLE = "is_stable"
    SET = "set"
    GET = "get"
    BUMP = "bump"
    STABLE = "stable"
    PACKAGE = "package"
    SET_PACKAGE = "set_package"
    UNKNOWN = "unknown"
