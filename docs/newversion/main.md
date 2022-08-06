# Main

> Auto-generated documentation for [newversion.main](https://github.com/findtopher/newversion/blob/main/newversion/main.py) module.

- [newversion](../README.md#newversion---your-version-manager) / [Modules](../MODULES.md#newversion-modules) / [Newversion](index.md#newversion) / Main
    - [main_api](#main_api)
    - [main_cli](#main_cli)
    - [setup_logging](#setup_logging)

## main_api

[[find in source code]](https://github.com/findtopher/newversion/blob/main/newversion/main.py#L24)

```python
def main_api(config: argparse.Namespace) -> str:
```

Main API entrypoint.

## main_cli

[[find in source code]](https://github.com/findtopher/newversion/blob/main/newversion/main.py#L55)

```python
def main_cli() -> None:
```

Main entrypoint for CLI.

## setup_logging

[[find in source code]](https://github.com/findtopher/newversion/blob/main/newversion/main.py#L11)

```python
def setup_logging(level: int) -> logging.Logger:
```

Setup logging for CLI usage.
