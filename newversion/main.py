import argparse
import sys

from newversion.cli_parser import parse_args
from newversion.executor import Executor, ExecutorError


class CLIError(Exception):
    """
    Main CLI error
    """


def main_api(config: argparse.Namespace) -> str:
    """
    Main API entrypoint.
    """
    executor = Executor(config.input)
    try:
        if config.command in {"lt", "lte", "gt", "gte", "eq"}:
            executor.command_compare(config.command, config.other)
            return config.input.dumps()
        if config.command == "is_stable":
            executor.command_is_stable()
            return config.input.dumps()
        if config.command == "set":
            return executor.command_set(config.release, config.value).dumps()
        if config.command == "get":
            return executor.command_get(config.release)
        if config.command == "bump":
            return executor.command_bump(config.release, config.increment).dumps()
        if config.command == "stable":
            return executor.command_stable().dumps()

        return config.input.dumps()
    except ExecutorError as e:
        raise CLIError(e)


def main_cli() -> None:
    """
    Main entrypoint for CLI.
    """
    config = parse_args(sys.argv[1:])
    try:
        output = main_api(config)
    except CLIError as e:
        sys.stderr.write(f"ERROR {e}\n")
        sys.exit(1)

    sys.stdout.write(f"{output}\n")
