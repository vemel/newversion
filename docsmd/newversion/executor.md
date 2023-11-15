# Executor

[Newversion Index](../README.md#newversion-index) /
[Newversion](./index.md#newversion) /
Executor

> Auto-generated documentation for [newversion.executor](https://github.com/vemel/newversion/blob/main/newversion/executor.py) module.

## Executor

[Show source in executor.py:16](https://github.com/vemel/newversion/blob/main/newversion/executor.py#L16)

CLI commands executor.

#### Signature

```python
class Executor:
    def __init__(self, input: Optional[Version] = None) -> None: ...
```

#### See also

- [Version](./version.md#version)

### Executor().command_bump

[Show source in executor.py:77](https://github.com/vemel/newversion/blob/main/newversion/executor.py#L77)

Bump release.

#### Arguments

- `release` - Release name
- `increment` - Number to increase by

#### Returns

A new Version.

#### Signature

```python
def command_bump(self, release: ReleaseNonLocalTypeDef, increment: int) -> Version: ...
```

#### See also

- [ReleaseNonLocalTypeDef](./type_defs.md#releasenonlocaltypedef)
- [Version](./version.md#version)

### Executor().command_compare

[Show source in executor.py:174](https://github.com/vemel/newversion/blob/main/newversion/executor.py#L174)

Execute compare command.

#### Arguments

- `command` - Compare operator.
- `other` - Version to compare to.

#### Returns

Processed `Version`.

#### Signature

```python
def command_compare(self, command: OperatorTypeDef, other: Version) -> None: ...
```

#### See also

- [OperatorTypeDef](./type_defs.md#operatortypedef)
- [Version](./version.md#version)

### Executor().command_get

[Show source in executor.py:27](https://github.com/vemel/newversion/blob/main/newversion/executor.py#L27)

Get version part.

#### Arguments

- `release` - Release part name.

#### Returns

Part as a string.

#### Signature

```python
def command_get(self, release: ReleaseTypeDef) -> str: ...
```

#### See also

- [ReleaseTypeDef](./type_defs.md#releasetypedef)

### Executor().command_get_version

[Show source in executor.py:197](https://github.com/vemel/newversion/blob/main/newversion/executor.py#L197)

#### Signature

```python
def command_get_version(self) -> Version: ...
```

#### See also

- [Version](./version.md#version)

### Executor().command_is_stable

[Show source in executor.py:164](https://github.com/vemel/newversion/blob/main/newversion/executor.py#L164)

Check whether version is stable.

#### Raises

- `ExecutorError` - If it is not.

#### Signature

```python
def command_is_stable(self) -> None: ...
```

### Executor().command_set

[Show source in executor.py:113](https://github.com/vemel/newversion/blob/main/newversion/executor.py#L113)

Set version part.

#### Arguments

- `release` - Release name
- `value` - Value to set

#### Returns

A new Version.

#### Signature

```python
def command_set(self, release: ReleaseNonLocalTypeDef, value: int) -> Version: ...
```

#### See also

- [ReleaseNonLocalTypeDef](./type_defs.md#releasenonlocaltypedef)
- [Version](./version.md#version)

### Executor().command_set_version

[Show source in executor.py:203](https://github.com/vemel/newversion/blob/main/newversion/executor.py#L203)

#### Signature

```python
def command_set_version(self) -> None: ...
```

### Executor().command_stable

[Show source in executor.py:155](https://github.com/vemel/newversion/blob/main/newversion/executor.py#L155)

Get stable non-post, non-local version from current.

#### Returns

A new Version.

#### Signature

```python
def command_stable(self) -> Version: ...
```

#### See also

- [Version](./version.md#version)
