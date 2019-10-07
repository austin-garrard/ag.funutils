#!/usr/bin/env bash

set -e

echo -e "\n* Setting up...\n"
pipenv install

echo -e "\n* Running tests...\n"
./scripts/test.sh

echo -e "\n* Success!\n"
