"""
Constants used in project.
"""

from typing import Final

PACKAGE_NAME: Final = "newversion"
LOGGER_NAME: Final = "newversion"


class VersionParts:
    """
    Utility class with constants for version parts.
    """

    ALPHA: Final = "alpha"
    BETA: Final = "beta"
    RC: Final = "rc"
    PRE: Final = "pre"
    POST: Final = "post"
    DEV: Final = "dev"
    MAJOR: Final = "major"
    MINOR: Final = "minor"
    MICRO: Final = "micro"
    LOCAL: Final = "local"
    EPOCH: Final = "epoch"


class Commands:
    """
    CLI commands.
    """

    LT: Final = "lt"
    LTE: Final = "lte"
    GT: Final = "gt"
    GTE: Final = "gte"
    EQ: Final = "eq"
    NE: Final = "ne"

    COMPARE: Final = {LT, LTE, GT, GTE, EQ, NE}

    IS_STABLE: Final = "is_stable"
    SET: Final = "set"
    GET: Final = "get"
    BUMP: Final = "bump"
    STABLE: Final = "stable"
    PACKAGE: Final = "package"
    SET_PACKAGE: Final = "set_package"
