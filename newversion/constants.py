"""
Constants used in project.
"""


class VersionParts:
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


class Commands:
    """
    CLI commands
    """

    LT = "lt"
    LTE = "lte"
    GT = "gt"
    GTE = "gte"
    EQ = "eq"
    NE = "ne"

    COMPARE = {LT, LTE, GT, GTE, EQ, NE}

    IS_STABLE = "is_stable"
    SET = "set"
    GET = "get"
    BUMP = "bump"
    STABLE = "stable"
