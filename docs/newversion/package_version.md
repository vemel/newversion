# PackageVersion

> Auto-generated documentation for [newversion.package_version](https://github.com/vemel/newversion/blob/main/newversion/package_version.py) module.

- [newversion](../README.md#newversion---your-version-manager) / [Modules](../MODULES.md#newversion-modules) / [Newversion](index.md#newversion) / PackageVersion
    - [PackageVersion](#packageversion)
        - [PackageVersion().get](#packageversionget)
        - [PackageVersion().set](#packageversionset)

## PackageVersion

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/package_version.py#L13)

```python
class PackageVersion():
    def __init__(path: Path) -> None:
```

### PackageVersion().get

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/package_version.py#L195)

```python
def get() -> Version:
```

#### See also

- [Version](version.md#version)

### PackageVersion().set

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/package_version.py#L208)

```python
def set(version: Version) -> None:
```

#### See also

- [Version](version.md#version)
