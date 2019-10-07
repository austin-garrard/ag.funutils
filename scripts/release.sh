#!/usr/bin/env bash

set -e

if [[ $1 == "clean" ]]
then
  rm -rf ./build/ ./dist/ ./ag.funutils.egg-info/

elif [[ $1 == "package" ]]
then
  ./scripts/test.sh

  pipenv run pip install --upgrade setuptools wheel

  pipenv run python ./setup.py sdist bdist_wheel

elif [[ $1 == "upload" ]]
then
  pipenv run twine upload dist/*

fi

