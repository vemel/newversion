import sys

if sys.version_info < (3, 8, 0):
    from typing_extensions import Literal  # type: ignore
else:
    from typing import Literal

ReleaseTypeDef = Literal[
    "major",
    "minor",
    "micro",
    "local",
    "pre",
    "post",
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
    "alpha",
    "beta",
    "rc",
    "epoch",
]

ReleaseMainTypeDef = Literal["major", "minor", "micro"]

OperatorTypeDef = Literal["lt", "lte", "gt", "gte", "eq", "ne"]

PrereleaseTypeDef = Literal["rc", "alpha", "beta"]
PrereleaseLooseTypeDef = Literal["rc", "alpha", "beta", "a", "b"]
