#!/usr/bin/env bash
set -e

ROOT_PATH=$(dirname $(dirname $0))
cd $ROOT_PATH

black .
isort .
npx pyright
pytest
flake8 newversion

./scripts/docs.sh
