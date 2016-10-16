#!/usr/bin/env bash

set -e

echo "Installing pyenv..."

# Install pyenv
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Use python3
pyenv update
pyenv install 3.5.2
pyenv global 3.5.2

set -x

# Install python deps
pip install -r requirements.common.txt
# Run migrations
python manage.py migrate --noinput

# Build front end
npm install
npm rebuild node-sass
npm run build

# Collect static files for deploy check
python manage.py collectstatic --noinput --settings prolifiko.settings.production
