# Cli Parser

[newversion Index](../README.md#newversion-index) /
[Newversion](./index.md#newversion) /
Cli Parser

> Auto-generated documentation for [newversion.cli_parser](https://github.com/vemel/newversion/blob/main/newversion/cli_parser.py) module.

- [Cli Parser](#cli-parser)
  - [get_stdin](#get_stdin)
  - [parse_args](#parse_args)

## get_stdin

[Show source in cli_parser.py:14](https://github.com/vemel/newversion/blob/main/newversion/cli_parser.py#L14)

Get input from stdin.

#### Returns

Parsed version.

#### Signature

```python
def get_stdin() -> Version: ...
```

#### See also

- [Version](./version.md#version)



## parse_args

[Show source in cli_parser.py:31](https://github.com/vemel/newversion/blob/main/newversion/cli_parser.py#L31)

Main CLI parser.

#### Returns

Argument parser Namespace.

#### Signature

```python
def parse_args(args: Sequence[str]) -> argparse.Namespace: ...
```