#!/usr/bin/env bash
npm install
npm rebuild node-sass
npm run build
# Use python3
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
pyenv update
pyenv install 3.5.2
pyenv global 3.5.2
python --version
# Install deps
pip install -r requirements.common.txt
# Run migrations
python manage.py migrate --noinput
# Collect static files for deploy check
python manage.py collectstatic --noinput --settings prolifiko.settings.production
