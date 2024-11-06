"""
Main entrypoint.
"""

import sys

from newversion.cli_parser import CLINamespace, parse_args
from newversion.constants import Commands
from newversion.exceptions import CLIError, ExecutorError
from newversion.executor import Executor
from newversion.logger import setup_logging
from newversion.version import Version


def _run_main_api(executor: Executor, config: CLINamespace) -> str:
    if config.command in (
        Commands.LT,
        Commands.LTE,
        Commands.GT,
        Commands.GTE,
        Commands.EQ,
        Commands.NE,
    ):
        executor.command_compare(config.command.value, config.other)
        return ""
    if config.command == Commands.IS_STABLE:
        executor.command_is_stable()
        return ""
    if config.command == Commands.PACKAGE:
        return executor.command_get_version().dumps()
    if config.command == Commands.SET_PACKAGE:
        executor.command_set_version(config.version)
        return ""
    if config.command == Commands.SET:
        return executor.command_set(config.release, config.value).dumps()
    if config.command == Commands.GET:
        return executor.command_get(config.release)
    if config.command == Commands.BUMP:
        return executor.command_bump(config.release, config.increment).dumps()
    if config.command == Commands.STABLE:
        return executor.command_stable().dumps()

    return executor.version.dumps()


def main_api(config: CLINamespace) -> str:
    """
    Run main API entrypoint.
    """
    executor = Executor(config.version)
    if config.package:
        executor.version = executor.command_get_version()
    try:
        result = _run_main_api(executor, config)
    except ExecutorError as e:
        raise CLIError(e) from None

    if config.save and result:
        executor.command_set_version(Version(result))
        return ""

    return result


def main_cli() -> None:
    """
    Run main entrypoint for CLI.
    """
    config = parse_args(sys.argv[1:])

    logger = setup_logging(config.log_level)
    try:
        output = main_api(config)
    except CLIError:
        logger.exception("Error")
        sys.exit(1)

    if output:
        sys.stdout.write(f"{output}\n")
