# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to
[PEP 440 -- Version Identification and Dependency Specification](https://www.python.org/dev/peps/pep-0440/).

## [Unreleased]
### Added
- `[api]` added `bump_dev()` functionality and tests

### Changed
- `[packaging]` updated dependencies (now `poetry install` works on Apple M1)

### Fixed
- `[cli]` fixed typo in `help` output

## [1.8.0] - 2021-03-16
### Added
- `[cli]` `package` command to get Python package version
- `[cli]` `set_package` command to set Python package version

## [1.7.0] - 2021-03-15

## [1.7.0rc1] - 2021-03-15
### Added
- `[cli]` `echo "1.2.3" | newversion ne "1.2.4"` comamnd to raise error if version is not equal to other

### Changed
- `[api]` reworked `Executor` for easier usage as API

### Fixed
- `[packaging]` console entrypoint `newversion` was not present in wheel package
- `[version]` error on getting `epoch`
- `[packaging]` `typing_extensions` are no longer needed on `python > 3.8`

## [0.1.5] - 2021-02-25
### Changed
- Added compatibility with Python 3.6.10+
