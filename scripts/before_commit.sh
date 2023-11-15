#!/usr/bin/env bash
set -e

ROOT_PATH=$(dirname $(dirname $0))
cd $ROOT_PATH

poetry run black .
poetry run isort .
poetry run npx pyright
poetry run pytest
poetry run flake8 .
