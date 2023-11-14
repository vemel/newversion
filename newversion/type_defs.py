from typing import Literal, NamedTuple, Optional, Tuple, Union

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
    epoch: int
    release: Tuple[int, ...]
    dev: Optional[Tuple[str, int]]
    pre: Optional[Tuple[str, int]]
    post: Optional[Tuple[str, int]]
    local: Optional[Tuple[Union[int, str], ...]]
