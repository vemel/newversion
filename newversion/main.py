import argparse
import logging
import sys

from newversion.cli_parser import parse_args
from newversion.constants import LOGGER_NAME, Commands
from newversion.exceptions import CLIError, ExecutorError
from newversion.executor import Executor


def setup_logging(level: int) -> logging.Logger:
    """
    Setup logging for CLI usage.
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
    logger.addHandler(stream_handler)
    return logger


def main_api(config: argparse.Namespace) -> str:
    """
    Main API entrypoint.
    """
    executor = Executor(config.input)
    try:
        if config.command in Commands.COMPARE:
            executor.command_compare(config.command, config.other)
            return ""
        if config.command == Commands.IS_STABLE:
            executor.command_is_stable()
            return ""
        if config.command == Commands.PACKAGE:
            return executor.command_get_version().dumps()
        if config.command == Commands.SET_PACKAGE:
            executor.command_set_version()
            return ""
        if config.command == Commands.SET:
            return executor.command_set(config.release, config.value).dumps()
        if config.command == Commands.GET:
            return executor.command_get(config.release)
        if config.command == Commands.BUMP:
            return executor.command_bump(config.release, config.increment).dumps()
        if config.command == Commands.STABLE:
            return executor.command_stable().dumps()

        return config.input.dumps()
    except ExecutorError as e:
        raise CLIError(e)


def main_cli() -> None:
    """
    Main entrypoint for CLI.
    """
    config = parse_args(sys.argv[1:])
    log_level = logging.INFO
    if config.verbose:
        log_level = logging.DEBUG
    if config.quiet:
        log_level = logging.CRITICAL

    logger = setup_logging(log_level)
    try:
        output = main_api(config)
    except CLIError as e:
        logger.error(f"{e}")
        sys.exit(1)

    if output:
        sys.stdout.write(f"{output}\n")
