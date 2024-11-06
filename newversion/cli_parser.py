"""
Main CLI parser.
"""

import argparse
import contextlib
import enum
import importlib.metadata
import logging
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Optional, Union

from newversion.constants import PACKAGE_NAME, Commands, VersionParts
from newversion.type_defs import ReleaseNonLocalTypeDef
from newversion.version import Version


def get_stdin() -> Version:
    """
    Get input from stdin.

    Returns:
        Parsed version.
    """
    if sys.stdin.isatty():
        return Version.zero()

    for line in sys.stdin.readlines():
        safe_line = line.strip().split(" ")[-1].replace('"', "").replace("'", "")
        return Version(safe_line)

    return Version.zero()


def get_program_version() -> str:
    """
    Get program version.
    """
    with contextlib.suppress(importlib.metadata.PackageNotFoundError):
        return importlib.metadata.version(PACKAGE_NAME)

    return "0.0.0"


@dataclass
class CLINamespace:
    """
    CLI namespace dataclass.
    """

    version: Version
    command: Commands
    release: ReleaseNonLocalTypeDef
    increment: int
    other: Version
    value: int
    log_level: int
    package: bool
    save: bool


class EnumListAction(argparse.Action):
    """
    Argparse action for handling Enums.
    """

    def __init__(
        self,
        *,
        type: type[enum.Enum],  # noqa: A002
        option_strings: Sequence[str],
        dest: str,
        default: Optional[Sequence[enum.Enum]] = None,
        required: bool = False,
        choices: Optional[Sequence[enum.Enum]] = None,
        nargs: Union[str, int, None] = None,
        **kwargs: Optional[str],
    ) -> None:
        self._enum_class = type
        super_choices = choices if choices is not None else list(self._enum_class)
        self._is_singular = default is not None and nargs is None
        if self._is_singular:
            nargs = "?"

        super().__init__(
            choices=tuple(e.value for e in super_choices),
            option_strings=option_strings,
            default=default,
            dest=dest,
            type=None,
            required=required,
            nargs=nargs,
            **kwargs,
        )

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        value: Union[str, Sequence[Any], None],
        _option_string: Optional[str] = None,
    ) -> None:
        """
        Convert value back into an Enum.
        """
        value_list: list[str] = []
        if isinstance(value, str):
            value_list.append(value)
        if isinstance(value, list):
            value_list.extend([i for i in value if isinstance(i, str)])
        enum_values = [self._enum_class(i) for i in value_list]

        if self._is_singular:
            enum_values = enum_values[0] if enum_values else self.default
        else:
            enum_values = enum_values or self.default

        setattr(namespace, self.dest, enum_values)


def parse_args(args: Sequence[str]) -> CLINamespace:
    """
    Parse CLI arguments.

    Returns:
        Argument parser Namespace.
    """
    parser = argparse.ArgumentParser(
        "newversion",
        description="SemVer helpers for PEP-440 versions",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=get_program_version(), help="Show version"
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="version",
        type=Version,
        default=None,
        help="Input version, can be provided as a pipe-in as well.",
    )
    parser.add_argument(
        "-p",
        "--package",
        action="store_true",
        help="Get or set Python package version. Supports pyproject.toml, setup.cfg and setup.py.",
    )
    parser.add_argument(
        "-s",
        "--save",
        action="store_true",
        help=(
            "Set output version as Python package version."
            " Supports pyproject.toml, setup.cfg and setup.py."
        ),
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    parser.add_argument("-q", "--quiet", action="store_true", help="No logging")

    subparsers = parser.add_subparsers(help="Available subcommands", dest="command")
    parser_bump = subparsers.add_parser(Commands.BUMP.value, help="Bump current version")
    parser_bump.add_argument(
        "release",
        type=VersionParts,
        action=EnumListAction,
        choices=[
            VersionParts.MAJOR,
            VersionParts.MINOR,
            VersionParts.MICRO,
            VersionParts.PRE,
            VersionParts.POST,
            VersionParts.RC,
            VersionParts.ALPHA,
            VersionParts.BETA,
            VersionParts.DEV,
        ],
        default=VersionParts.MICRO,
        help=f"Release type. Default: {VersionParts.MICRO.value}",
    )
    parser_bump.add_argument(
        "increment",
        type=int,
        default=1,
        nargs="?",
        help="Version increment. Default: 1",
    )

    parser_get = subparsers.add_parser(Commands.GET.value, help="Get release number")
    parser_get.add_argument(
        "release",
        type=VersionParts,
        action=EnumListAction,
        default=VersionParts.FULL,
        help="Release type",
    )

    parser_set = subparsers.add_parser(Commands.SET.value, help="Set release number")
    parser_set.add_argument(
        "release",
        type=VersionParts,
        action=EnumListAction,
        help="Release type",
    )
    parser_set.add_argument(
        "value",
        type=int,
        help="Release number",
    )

    subparsers.add_parser(Commands.STABLE.value, help="Get stable release of current version")

    subparsers.add_parser(
        Commands.IS_STABLE.value,
        help="Check if current version is not a pre- or dev release",
    )

    subparsers.add_parser(
        Commands.PACKAGE.value,
        help="Get Python package version. Supports pyproject.toml, setup.cfg and setup.py.",
    )

    subparsers.add_parser(
        Commands.SET_PACKAGE.value,
        help="Set Python package version. Supports pyproject.toml, setup.cfg and setup.py.",
    )

    parser_lt = subparsers.add_parser(
        Commands.LT.value,
        help="Check if current version is lesser than the other",
    )
    parser_lt.add_argument(
        "other",
        type=Version,
        help="Version to compare",
    )

    parser_lte = subparsers.add_parser(
        Commands.LTE.value,
        help="Check if current version is lesser or equal to the other",
    )
    parser_lte.add_argument(
        "other",
        type=Version,
        help="Version to compare",
    )

    parser_gt = subparsers.add_parser(
        Commands.GT.value,
        help="Check if current version is greater than the other",
    )
    parser_gt.add_argument(
        "other",
        type=Version,
        help="Version to compare",
    )

    parser_gte = subparsers.add_parser(
        Commands.GTE.value,
        help="Check if current version is greater or equal to the other",
    )
    parser_gte.add_argument(
        "other",
        type=Version,
        help="Version to compare",
    )

    parser_eq = subparsers.add_parser(
        Commands.EQ.value,
        help="Check if current version is equal to the other",
    )
    parser_eq.add_argument(
        "other",
        type=Version,
        help="Version to compare",
    )

    parser_ne = subparsers.add_parser(
        Commands.NE.value,
        help="Check if current version is not equal to the other",
    )
    parser_ne.add_argument(
        "other",
        type=Version,
        help="Version to compare",
    )

    result = parser.parse_args(args)

    if result.version is None:
        result.version = get_stdin()

    log_level = logging.DEBUG if result.verbose else logging.INFO
    if result.quiet:
        log_level = logging.CRITICAL

    return CLINamespace(
        version=result.version,
        command=Commands(result.command) if result.command else Commands.UNKNOWN,
        release=result.release if getattr(result, "release", "") else VersionParts.MICRO.value,
        increment=getattr(result, "increment", 1),
        other=getattr(result, "other", Version.zero()),
        value=getattr(result, "value", 1),
        log_level=log_level,
        package=result.package,
        save=result.save,
    )
