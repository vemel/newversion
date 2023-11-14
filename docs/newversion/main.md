# Main

[newversion Index](../README.md#newversion-index) /
[Newversion](./index.md#newversion) /
Main

> Auto-generated documentation for [newversion.main](https://github.com/vemel/newversion/blob/main/newversion/main.py) module.

- [Main](#main)
  - [main_api](#main_api)
  - [main_cli](#main_cli)
  - [setup_logging](#setup_logging)

## main_api

[Show source in main.py:24](https://github.com/vemel/newversion/blob/main/newversion/main.py#L24)

Main API entrypoint.

#### Signature

```python
def main_api(config: argparse.Namespace) -> str: ...
```



## main_cli

[Show source in main.py:55](https://github.com/vemel/newversion/blob/main/newversion/main.py#L55)

Main entrypoint for CLI.

#### Signature

```python
def main_cli() -> None: ...
```



## setup_logging

[Show source in main.py:11](https://github.com/vemel/newversion/blob/main/newversion/main.py#L11)

Setup logging for CLI usage.

#### Signature

```python
def setup_logging(level: int) -> logging.Logger: ...
```