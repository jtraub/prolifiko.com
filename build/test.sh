#!/usr/bin/env bash
./manage.py check --deploy --settings prolifiko.settings.production
./check.sh
pytest
