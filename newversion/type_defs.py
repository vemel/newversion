"""
Type definitions used in the newversion package.
"""

from typing import Literal, NamedTuple, Optional, Union

ReleaseTypeDef = Literal[
    "major",
    "minor",
    "micro",
    "local",
    "pre",
    "post",
    "dev",
    "alpha",
    "beta",
    "rc",
    "epoch",
]

ReleaseNonLocalTypeDef = Literal[
    "major",
    "minor",
    "micro",
    "pre",
    "post",
    "dev",
    "alpha",
    "beta",
    "rc",
    "epoch",
]

ReleaseMainTypeDef = Literal["major", "minor", "micro"]
ReleaseMainPostTypeDef = Literal["major", "minor", "micro", "post"]

OperatorTypeDef = Literal["lt", "lte", "gt", "gte", "eq", "ne"]

PrereleaseTypeDef = Literal["rc", "alpha", "beta"]
PrereleaseLooseTypeDef = Literal["rc", "alpha", "beta", "a", "b", "c", None]


class BaseVersion(NamedTuple):
    """
    BaseVersion is a NamedTuple that represents a version with several components.

    Attributes:
        epoch (int): The epoch of the version.
        release (Tuple[int, ...]): The release segment of the version, represented as
            a tuple of integers.
        dev (Optional[Tuple[str, int]]): The development release segment, represented as
            an optional tuple containing a string and an integer.
        pre (Optional[Tuple[str, int]]): The pre-release segment, represented as
            an optional tuple containing a string and an integer.
        post (Optional[Tuple[str, int]]): The post-release segment, represented as
            an optional tuple containing a string and an integer.
        local (Optional[Tuple[Union[int, str], ...]]): The local version segment, represented as
            an optional tuple containing integers and/or strings.
    """

    epoch: int
    release: tuple[int, ...]
    dev: Optional[tuple[str, int]]
    pre: Optional[tuple[str, int]]
    post: Optional[tuple[str, int]]
    local: Optional[tuple[Union[int, str], ...]]
