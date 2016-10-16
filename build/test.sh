#!/usr/bin/env bash

set -e

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

set -x

./manage.py check --deploy --settings prolifiko.settings.production
pep8 --exclude=migrations,node_modules .
pytest
npm test
