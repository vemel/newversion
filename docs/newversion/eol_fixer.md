# EOLFixer

> Auto-generated documentation for [newversion.eol_fixer](https://github.com/vemel/newversion/blob/main/newversion/eol_fixer.py) module.

Converter between Unix and WIndows line endings.

- [newversion](../README.md#newversion---your-version-manager) / [Modules](../MODULES.md#newversion-modules) / [Newversion](index.md#newversion) / EOLFixer
    - [EOLFixer](#eolfixer)
        - [EOLFixer.add_newline](#eolfixeradd_newline)
        - [EOLFixer.get_line_ending](#eolfixerget_line_ending)
        - [EOLFixer.is_crlf](#eolfixeris_crlf)
        - [EOLFixer.to_crlf](#eolfixerto_crlf)
        - [EOLFixer.to_lf](#eolfixerto_lf)

## EOLFixer

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/eol_fixer.py#L6)

```python
class EOLFixer():
```

Converter between Unix and WIndows line endings.

### EOLFixer.add_newline

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/eol_fixer.py#L63)

```python
@classmethod
def add_newline(text: str) -> str:
```

Add newline character to the end if it is missing.

### EOLFixer.get_line_ending

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/eol_fixer.py#L56)

```python
@classmethod
def get_line_ending(text: str) -> str:
```

Get line ending character.

### EOLFixer.is_crlf

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/eol_fixer.py#L14)

```python
@classmethod
def is_crlf(text: str) -> bool:
```

        Check whether text has `
` characters.

Arguments:
    text -- Text to check.

### EOLFixer.to_crlf

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/eol_fixer.py#L40)

```python
@classmethod
def to_crlf(text: str) -> str:
```

        Convert `
` to `
`.

Arguments:
    text -- Text to convert.

Returns:
    Converted text.

### EOLFixer.to_lf

[[find in source code]](https://github.com/vemel/newversion/blob/main/newversion/eol_fixer.py#L24)

```python
@classmethod
def to_lf(text: str) -> str:
```

        Convert `
` to `
`.

Arguments:
    text -- Text to convert.

Returns:
    Converted text.
