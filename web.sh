#!/bin/bash
CMD="gunicorn prolifiko.wsgi --log-file=- --timeout 120"
[ -z "$DISABLE_NEWRELIC" ] && CMD="newrelic-admin run-program $CMD"

echo $CMD
$CMD
