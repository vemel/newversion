# EOLFixer

[Newversion Index](../README.md#newversion-index) /
[Newversion](./index.md#newversion) /
EOLFixer

> Auto-generated documentation for [newversion.eol_fixer](https://github.com/vemel/newversion/blob/main/newversion/eol_fixer.py) module.

## EOLFixer

[Show source in eol_fixer.py:6](https://github.com/vemel/newversion/blob/main/newversion/eol_fixer.py#L6)

Converter between Unix and Windows line endings.

#### Signature

```python
class EOLFixer: ...
```

### EOLFixer.add_newline

[Show source in eol_fixer.py:63](https://github.com/vemel/newversion/blob/main/newversion/eol_fixer.py#L63)

Add newline character to the end if it is missing.

#### Signature

```python
@classmethod
def add_newline(cls, text: str) -> str: ...
```

### EOLFixer.get_line_ending

[Show source in eol_fixer.py:56](https://github.com/vemel/newversion/blob/main/newversion/eol_fixer.py#L56)

Get line ending character.

#### Signature

```python
@classmethod
def get_line_ending(cls, text: str) -> str: ...
```

### EOLFixer.is_crlf

[Show source in eol_fixer.py:14](https://github.com/vemel/newversion/blob/main/newversion/eol_fixer.py#L14)

        Check whether text has `
` characters.

Arguments:
    text -- Text to check.

#### Signature

```python
@classmethod
def is_crlf(cls, text: str) -> bool: ...
```

### EOLFixer.to_crlf

[Show source in eol_fixer.py:40](https://github.com/vemel/newversion/blob/main/newversion/eol_fixer.py#L40)

        Convert `
` to `
`.

Arguments:
    text -- Text to convert.

Returns:
    Converted text.

#### Signature

```python
@classmethod
def to_crlf(cls, text: str) -> str: ...
```

### EOLFixer.to_lf

[Show source in eol_fixer.py:24](https://github.com/vemel/newversion/blob/main/newversion/eol_fixer.py#L24)

        Convert `
` to `
`.

Arguments:
    text -- Text to convert.

Returns:
    Converted text.

#### Signature

```python
@classmethod
def to_lf(cls, text: str) -> str: ...
```
