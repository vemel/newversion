# Executor

> Auto-generated documentation for [newversion.executor](https://github.com/vemel/newversion//blob/main/newversion/executor.py) module.

CLI commands executor.

- [newversion](../README.md#newversion---your-version-manager) / [Modules](../MODULES.md#newversion-modules) / [Newversion](index.md#newversion) / Executor
    - [Executor](#executor)
        - [Executor().command_bump](#executorcommand_bump)
        - [Executor().command_compare](#executorcommand_compare)
        - [Executor().command_get](#executorcommand_get)
        - [Executor().command_get_version](#executorcommand_get_version)
        - [Executor().command_is_stable](#executorcommand_is_stable)
        - [Executor().command_set](#executorcommand_set)
        - [Executor().command_set_version](#executorcommand_set_version)
        - [Executor().command_stable](#executorcommand_stable)

## Executor

[[find in source code]](https://github.com/vemel/newversion//blob/main/newversion/executor.py#L15)

```python
class Executor():
    def __init__(input: Version = Version.zero()) -> None:
```

CLI commands executor.

#### See also

- [Version](version.md#version)

### Executor().command_bump

[[find in source code]](https://github.com/vemel/newversion//blob/main/newversion/executor.py#L73)

```python
def command_bump(release: ReleaseNonLocalTypeDef, increment: int) -> Version:
```

Bump release.

#### Arguments

- `release` - Release name
- `increment` - Number to increase by

#### Returns

A new Version.

#### See also

- [ReleaseNonLocalTypeDef](type_defs.md#releasenonlocaltypedef)
- [Version](version.md#version)

### Executor().command_compare

[[find in source code]](https://github.com/vemel/newversion//blob/main/newversion/executor.py#L149)

```python
def command_compare(command: OperatorTypeDef, other: Version) -> None:
```

Execute compare command.

#### Arguments

- `command` - Compare operator.
- `other` - Version to compare to.

#### Returns

Processed `Version`.

#### See also

- [OperatorTypeDef](type_defs.md#operatortypedef)
- [Version](version.md#version)

### Executor().command_get

[[find in source code]](https://github.com/vemel/newversion//blob/main/newversion/executor.py#L26)

```python
def command_get(release: ReleaseTypeDef) -> str:
```

Get version part.

#### Arguments

- `release` - Release part name.

#### Returns

Part as a string.

#### See also

- [ReleaseTypeDef](type_defs.md#releasetypedef)

### Executor().command_get_version

[[find in source code]](https://github.com/vemel/newversion//blob/main/newversion/executor.py#L172)

```python
def command_get_version() -> Version:
```

#### See also

- [Version](version.md#version)

### Executor().command_is_stable

[[find in source code]](https://github.com/vemel/newversion//blob/main/newversion/executor.py#L139)

```python
def command_is_stable() -> None:
```

Check whether version is stable.

#### Raises

- `ExecutorError` - If it is not.

### Executor().command_set

[[find in source code]](https://github.com/vemel/newversion//blob/main/newversion/executor.py#L106)

```python
def command_set(release: ReleaseNonLocalTypeDef, value: int) -> Version:
```

Set version part.

#### Arguments

- `release` - Release name
- `value` - Value to set

#### Returns

A new Version.

#### See also

- [ReleaseNonLocalTypeDef](type_defs.md#releasenonlocaltypedef)
- [Version](version.md#version)

### Executor().command_set_version

[[find in source code]](https://github.com/vemel/newversion//blob/main/newversion/executor.py#L178)

```python
def command_set_version() -> None:
```

### Executor().command_stable

[[find in source code]](https://github.com/vemel/newversion//blob/main/newversion/executor.py#L130)

```python
def command_stable() -> Version:
```

Get stable non-post, non-local version from current.

#### Returns

A new Version.

#### See also

- [Version](version.md#version)
