# PackageVersion

[newversion Index](../README.md#newversion-index) /
[Newversion](./index.md#newversion) /
PackageVersion

> Auto-generated documentation for [newversion.package_version](https://github.com/vemel/newversion/blob/main/newversion/package_version.py) module.

- [PackageVersion](#packageversion)
  - [PackageVersion](#packageversion-1)
    - [PackageVersion().get](#packageversion()get)
    - [PackageVersion().set](#packageversion()set)

## PackageVersion

[Show source in package_version.py:13](https://github.com/vemel/newversion/blob/main/newversion/package_version.py#L13)

#### Signature

```python
class PackageVersion:
    def __init__(self, path: Path) -> None: ...
```

### PackageVersion().get

[Show source in package_version.py:195](https://github.com/vemel/newversion/blob/main/newversion/package_version.py#L195)

#### Signature

```python
def get(self) -> Version: ...
```

#### See also

- [Version](./version.md#version)

### PackageVersion().set

[Show source in package_version.py:208](https://github.com/vemel/newversion/blob/main/newversion/package_version.py#L208)

#### Signature

```python
def set(self, version: Version) -> None: ...
```

#### See also

- [Version](./version.md#version)