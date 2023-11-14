# Version

[newversion Index](../README.md#newversion-index) /
[Newversion](./index.md#newversion) /
Version

> Auto-generated documentation for [newversion.version](https://github.com/vemel/newversion/blob/main/newversion/version.py) module.

- [Version](#version)
  - [Version](#version-1)
    - [Version().base](#version()base)
    - [Version().base](#version()base-1)
    - [Version().bump_dev](#version()bump_dev)
    - [Version().bump_major](#version()bump_major)
    - [Version().bump_micro](#version()bump_micro)
    - [Version().bump_minor](#version()bump_minor)
    - [Version().bump_postrelease](#version()bump_postrelease)
    - [Version().bump_prerelease](#version()bump_prerelease)
    - [Version().bump_release](#version()bump_release)
    - [Version().copy](#version()copy)
    - [Version().dumps](#version()dumps)
    - [Version().get_stable](#version()get_stable)
    - [Version().is_stable](#version()is_stable)
    - [Version().prerelease_type](#version()prerelease_type)
    - [Version().replace](#version()replace)
    - [Version.zero](#versionzero)
  - [VersionError](#versionerror)

## Version

[Show source in version.py:25](https://github.com/vemel/newversion/blob/main/newversion/version.py#L25)

Extended `packaging.version.Version` implementation.

#### Signature

```python
class Version(packaging.version.Version):
    def __init__(self, version: str) -> None: ...
```

### Version().base

[Show source in version.py:64](https://github.com/vemel/newversion/blob/main/newversion/version.py#L64)

Underlying version NamedTuple.

#### Signature

```python
@property
def base(self) -> BaseVersion: ...
```

#### See also

- [BaseVersion](./type_defs.md#baseversion)

### Version().base

[Show source in version.py:71](https://github.com/vemel/newversion/blob/main/newversion/version.py#L71)

#### Signature

```python
@base.setter
def base(self, base: BaseVersion) -> None: ...
```

#### See also

- [BaseVersion](./type_defs.md#baseversion)

### Version().bump_dev

[Show source in version.py:220](https://github.com/vemel/newversion/blob/main/newversion/version.py#L220)

Get next dev version.
If version is stable - bump release for proper versioning as well.
Defaults to bumping `micro`, falls back automatically to `post`

#### Arguments

- `inc` - Increment for dev version.
- [Version().bump_release](#versionbump_release) - Release number to bump if version is stable.

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

#### Signature

```python
def bump_dev(
    self: _R, inc: int = 1, bump_release: ReleaseMainTypeDef = "micro"
) -> _R: ...
```

#### See also

- [ReleaseMainTypeDef](./type_defs.md#releasemaintypedef)

### Version().bump_major

[Show source in version.py:116](https://github.com/vemel/newversion/blob/main/newversion/version.py#L116)

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

#### Signature

```python
def bump_major(self: _R, inc: int = 1) -> _R: ...
```

### Version().bump_micro

[Show source in version.py:186](https://github.com/vemel/newversion/blob/main/newversion/version.py#L186)

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

#### Signature

```python
def bump_micro(self: _R, inc: int = 1) -> _R: ...
```

### Version().bump_minor

[Show source in version.py:150](https://github.com/vemel/newversion/blob/main/newversion/version.py#L150)

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

#### Signature

```python
def bump_minor(self: _R, inc: int = 1) -> _R: ...
```

### Version().bump_postrelease

[Show source in version.py:315](https://github.com/vemel/newversion/blob/main/newversion/version.py#L315)

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

#### Signature

```python
def bump_postrelease(self: _R, inc: int = 1) -> _R: ...
```

### Version().bump_prerelease

[Show source in version.py:264](https://github.com/vemel/newversion/blob/main/newversion/version.py#L264)

Get next prerelease version.
If version is stable - bump `micro` for proper versioning as well.
Defaults to `rc` pre-releases.

#### Arguments

- `inc` - Increment for micro version.
- `release_type` - Prerelease type: alpha, beta, rc.
- [Version().bump_release](#versionbump_release) - Release number to bump if version is stable.

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

#### Signature

```python
def bump_prerelease(
    self: _R,
    inc: int = 1,
    release_type: Optional[PrereleaseLooseTypeDef] = None,
    bump_release: ReleaseMainTypeDef = "micro",
) -> _R: ...
```

#### See also

- [PrereleaseLooseTypeDef](./type_defs.md#prereleaseloosetypedef)
- [ReleaseMainTypeDef](./type_defs.md#releasemaintypedef)

### Version().bump_release

[Show source in version.py:86](https://github.com/vemel/newversion/blob/main/newversion/version.py#L86)

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

#### Signature

```python
def bump_release(
    self: _R, release_type: ReleaseMainTypeDef = "micro", inc: int = 1
) -> _R: ...
```

#### See also

- [ReleaseMainTypeDef](./type_defs.md#releasemaintypedef)

### Version().copy

[Show source in version.py:75](https://github.com/vemel/newversion/blob/main/newversion/version.py#L75)

Create a copy of a current version instance.

#### Signature

```python
def copy(self: _R) -> _R: ...
```

### Version().dumps

[Show source in version.py:43](https://github.com/vemel/newversion/blob/main/newversion/version.py#L43)

Render to string.

#### Signature

```python
def dumps(self) -> str: ...
```

### Version().get_stable

[Show source in version.py:420](https://github.com/vemel/newversion/blob/main/newversion/version.py#L420)

Get stable version from pre- or post- release.

#### Examples

```python
Version("1.2.3").get_stable() # "1.2.3"
Version("2.1.0a2").get_stable() # "2.1.0"
Version("1.2.5.post3").get_stable() # "1.2.5"
```

#### Returns

A new instance.

#### Signature

```python
def get_stable(self: _R) -> _R: ...
```

### Version().is_stable

[Show source in version.py:410](https://github.com/vemel/newversion/blob/main/newversion/version.py#L410)

Whether version is not prerelease or devrelease.

#### Returns

True if it is stable.

#### Signature

```python
@property
def is_stable(self) -> bool: ...
```

### Version().prerelease_type

[Show source in version.py:49](https://github.com/vemel/newversion/blob/main/newversion/version.py#L49)

#### Signature

```python
@property
def prerelease_type(self) -> Optional[PrereleaseTypeDef]: ...
```

#### See also

- [PrereleaseTypeDef](./type_defs.md#prereleasetypedef)

### Version().replace

[Show source in version.py:348](https://github.com/vemel/newversion/blob/main/newversion/version.py#L348)

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

#### Signature

```python
def replace(
    self: _R,
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
) -> _R: ...
```

### Version.zero

[Show source in version.py:36](https://github.com/vemel/newversion/blob/main/newversion/version.py#L36)

Get zero version `0.0.0`

#### Signature

```python
@classmethod
def zero(cls: Type[_R]) -> _R: ...
```



## VersionError

[Show source in version.py:19](https://github.com/vemel/newversion/blob/main/newversion/version.py#L19)

Wrapper for InvalidVersion error.

#### Signature

```python
class VersionError(packaging.version.InvalidVersion): ...
```