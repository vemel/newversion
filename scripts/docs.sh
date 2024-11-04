#!/usr/bin/env bash
set -e

ROOT_PATH=$(dirname $(dirname $0))
cd $ROOT_PATH

uv run handsdown --external `git config --get remote.origin.url` --branch main -n newversion newversion --exclude '*/build/*' --cleanup --panic
