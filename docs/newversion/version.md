# Version

> Auto-generated documentation for [newversion.version](https://github.com/vemel/newversion/blob/main/newversion/version.py) module.

Extended `packaging.version.Version` implementation.

- [newversion](../README.md#newversion---your-version-manager) / [Modules](../MODULES.md#newversion-modules) / [Newversion](index.md#newversion) / Version
    - [Version](#version)
        - [Version().base](#versionbase)
        - [Version().base](#versionbase)
        - [Version().bump_dev](#versionbump_dev)
        - [Version().bump_major](#versionbump_major)
        - [Version().bump_micro](#versionbump_micro)
        - [Version().bump_minor](#versionbump_minor)
        - [Version().bump_postrelease](#versionbump_postrelease)
        - [Version().bump_prerelease](#versionbump_prerelease)
        - [Version().bump_release](#versionbump_release)
        - [Version().copy](#versioncopy)
        - [Version().dumps](#versiondumps)
        - [Version().get_stable](#versionget_stable)
        - [Version().is_stable](#versionis_stable)
        - [Version().prerelease_type](#versionprerelease_type)
        - [Version().replace](#versionreplace)
        - [Version.zero](#versionzero)
    - [VersionError](#versionerror)

## Version

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/version.py#L21)

```python
class Version(packaging.version.Version):
    def __init__(version: str) -> None:
```

Extended `packaging.version.Version` implementation.

### Version().base

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/version.py#L60)

```python
@property
def base() -> BaseVersion:
```

Underlying version NamedTuple.

### Version().base

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/version.py#L67)

```python
@base.setter
def base(base: BaseVersion) -> None:
```

### Version().bump_dev

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/version.py#L216)

```python
def bump_dev(
    inc: int = 1,
    bump_release: ReleaseMainTypeDef = VersionParts.MICRO,
) -> _R:
```

Get next dev version.
If version is stable - bump release for proper versioning as well.
Defaults to bumping `micro`

#### Arguments

- `inc` - Increment for dev version.
- `bump_release` - Release number to bump if version is stable.

#### Examples

```python
Version("1.2.3").bump_dev()  # "1.2.4.dev0"
Version("1.2.3").bump_dev(1, 'minor')  # "1.3.0.dev0"
Version("1.2.3.dev14").bump_dev()  # "1.2.3.dev15"
Version("1.2.3a4).bump_dev()  # "1.2.3a4.dev0"
Version("1.2.3b5.dev9").bump_dev()  # "1.2.3b5.dev10"
Version("1.2.3.dev3").bump_dev(2)  # "1.2.3.dev5"
Version("1.2.3.post4").bump_dev()  # "1.2.3.post5.dev0"
```

#### Returns

A new copy.

#### See also

- [ReleaseMainTypeDef](type_defs.md#releasemaintypedef)

### Version().bump_major

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/version.py#L112)

```python
def bump_major(inc: int = 1) -> _R:
```

Get next major version.

#### Arguments

- `inc` - Increment for major version.

#### Examples

```python
Version("1.2.3").bump_major()  # "2.0.0"
Version("1.2.3.dev14").bump_major()  # "2.0.0"
Version("1.2.3a5").bump_major()  # "2.0.0"
Version("1.2.3rc3").bump_major(2)  # "3.0.0"
Version("1.2.3rc3").bump_major(0)  # "1.0.0"
```

#### Returns

A new copy.

### Version().bump_micro

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/version.py#L182)

```python
def bump_micro(inc: int = 1) -> _R:
```

Get next micro version.

#### Arguments

- `inc` - Increment for micro version.

#### Examples

```python
Version("1.2.3").bump_micro()  # "1.2.4"
Version("1.2.3.dev14").bump_micro()  # "1.2.4"
Version("1.2.3a5").bump_micro()  # "1.2.4"
Version("1.2.3rc3").bump_micro(2)  # "1.2.5"
Version("1.2.3rc3").bump_micro(0)  # "1.2.3"
```

#### Returns

A new copy.

### Version().bump_minor

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/version.py#L146)

```python
def bump_minor(inc: int = 1) -> _R:
```

Get next minor version.

#### Arguments

- `inc` - Increment for minor version.

#### Examples

```python
Version("1.2.3").bump_minor()  # "1.3.0"
Version("1.2.3.dev14").bump_minor()  # "1.3.0"
Version("1.2.3a5").bump_minor()  # "1.3.0"
Version("1.2.3rc3").bump_minor(2)  # "1.4.0"
Version("1.2.3rc3").bump_minor(0)  # "1.2.0"
Version("1.3.0rc3").bump_minor()  # "1.3.0"
Version("1.3.0rc3").bump_minor(2)  # "1.4.0"
```

#### Returns

A new copy.

### Version().bump_postrelease

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/version.py#L308)

```python
def bump_postrelease(inc: int = 1) -> _R:
```

Get next postrelease version.

#### Arguments

- `inc` - Increment for micro version.

#### Examples

```python
Version("1.2.3").bump_postrelease()  # "1.2.3.post1"
Version("1.2.3.post3").bump_postrelease()  # "1.2.3.post4"
Version("1.2.3a5").bump_postrelease()  # "1.2.3.post1"
Version("1.2.3.post4").bump_postrelease(2)  # "1.2.3.post6"
```

#### Returns

A new copy.

### Version().bump_prerelease

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/version.py#L257)

```python
def bump_prerelease(
    inc: int = 1,
    release_type: PrereleaseLooseTypeDef = None,
    bump_release: ReleaseMainTypeDef = VersionParts.MICRO,
) -> _R:
```

Get next prerelease version.
If version is stable - bump `micro` for proper versioning as well.
Defaults to `rc` pre-releases.

#### Arguments

- `inc` - Increment for micro version.
- `release_type` - Prerelease type: alpha, beta, rc.
- `bump_release` - Release number to bump if version is stable.

#### Examples

```python
Version("1.2.3").bump_prerelease()  # "1.2.4rc1"
Version("1.2.3").bump_prerelease(bump_release="major")  # "2.0.0rc1"
Version("1.2.3.dev14").bump_prerelease()  # "1.2.3rc1"
Version("1.2.3a5").bump_prerelease()  # "1.2.3a6"
Version("1.2.3rc3").bump_prerelease(2, "beta")  # "1.2.3rc5"
```

#### Returns

A new copy.

#### See also

- [PrereleaseLooseTypeDef](type_defs.md#prereleaseloosetypedef)
- [ReleaseMainTypeDef](type_defs.md#releasemaintypedef)

### Version().bump_release

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/version.py#L82)

```python
def bump_release(
    release_type: ReleaseMainTypeDef = VersionParts.MICRO,
    inc: int = 1,
) -> _R:
```

Get next release version.

#### Arguments

- `release_type` - Release type: major, minor, micro.
- `inc` - Increment for major version.

#### Examples

```python
Version("1.2.3").bump_release()  # "1.2.4"
Version("1.2.3").bump_release("major")  # "2.0.0"
Version("1.2.3.dev14").bump_release("minor", 2)  # "1.4.0"
```

#### Returns

A new copy.

#### See also

- [ReleaseMainTypeDef](type_defs.md#releasemaintypedef)

### Version().copy

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/version.py#L71)

```python
def copy() -> _R:
```

Create a copy of a current version instance.

### Version().dumps

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/version.py#L39)

```python
def dumps() -> str:
```

Render to string.

### Version().get_stable

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/version.py#L413)

```python
def get_stable() -> _R:
```

Get stable version from pre- or post- release.

#### Examples

```python
Version("1.2.3").get_stable() # "1.2.3"
Version("2.1.0a2").get_stable() # "2.1.0"
Version("1.2.5.post3").get_stable() # "1.2.5"
```

#### Returns

A new instance.

### Version().is_stable

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/version.py#L403)

```python
@property
def is_stable() -> bool:
```

Whether version is not prerelease or devrelease.

#### Returns

True if it is stable.

### Version().prerelease_type

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/version.py#L45)

```python
@property
def prerelease_type() -> Optional[PrereleaseTypeDef]:
```

### Version().replace

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/version.py#L341)

```python
def replace(
    major: Optional[int] = None,
    minor: Optional[int] = None,
    micro: Optional[int] = None,
    alpha: Optional[int] = None,
    beta: Optional[int] = None,
    rc: Optional[int] = None,
    dev: Optional[int] = None,
    post: Optional[int] = None,
    epoch: Optional[int] = None,
    local: Optional[str] = None,
) -> _R:
```

Modify version parts.

#### Examples

```python
Version("1.2.3").replace(dev=24) # "1.2.3.dev24"
Version("1.2.3rc5").replace(17) # "1.2.3.dev17"
```

#### Arguments

- `major` - Major release number.
- `minor` - Minor release number.
- `micro` - Micro release number.
- `alpha` - Alpha pre-release number.
- `beta` - Beta pre-release number.
- `rc` - RC pre-release number.
- `dev` - Dev release number.
- `post` - Post release number.
- `epoch` - Release epoch.
- `local` - Local release identifier.

#### Returns

A new instance.

### Version.zero

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/version.py#L32)

```python
@classmethod
def zero() -> _R:
```

Get zero version `0.0.0`

## VersionError

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/version.py#L15)

```python
class VersionError(packaging.version.InvalidVersion):
```

Wrapper for InvalidVersion error.
