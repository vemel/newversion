#!/usr/bin/env bash
set -e

newversion            # 0.0.0
newversion bump major # 1.0.0

# get package version from pyproject.toml, setup.cfg or setup.py
newversion -p # 1.2.3
newversion -p bump # 1.2.4
newversion -p bump pre # 1.2.4rc1
newversion -p get minor  # 2

echo "1.2.3rc1" | newversion bump micro   # 1.2.3
echo "1.2.3rc1" | newversion bump minor   # 1.3.0
echo "1.2.3rc1" | newversion bump major   # 2.0.0
echo "1.2.3rc1" | newversion bump pre     # 1.2.3rc2
echo "1.2.3rc1" | newversion bump rc      # 1.2.3rc2
echo "1.2.3rc1" | newversion bump alpha   # 1.2.4a1

echo "1.2.3rc1" | newversion set micro 5  # 1.2.5rc1
echo "1.2.3rc1" | newversion set minor 5  # 1.5.3rc1
echo "1.2.3rc1" | newversion set major 5  # 5.2.3rc1
echo "1.2.3rc1" | newversion set pre 5    # 1.2.3rc5
echo "1.2.3rc1" | newversion set rc 5     # 1.2.3rc5
echo "1.2.3rc1" | newversion set alpha 5  # 1.2.3a5

echo "1.2.3rc1" | newversion get micro    # 1
echo "1.2.3rc1" | newversion get minor    # 2
echo "1.2.3rc1" | newversion get major    # 3
echo "1.2.3rc1" | newversion get pre      # rc1
echo "1.2.3rc1" | newversion get rc       # 1
echo "1.2.3rc1" | newversion get alpha    # 0

echo "1.2.3rc1" | newversion stable # 1.2.3

echo "1.2.3rc1" | newversion is_stable || echo "error!"
echo "1.2.3" | newversion is_stable          # 1.2.3
echo "1.2.3" | newversion is_stable || echo "error!"

echo "1.2.3rc1" | newversion gt "1.2.3" || echo "error!"
echo "1.2.3rc1" | newversion lte "1.2.3"  # "1.2.3rc1"