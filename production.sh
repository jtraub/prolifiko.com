#!/bin/bash

export $(heroku config -s | xargs)

DISABLE_NEWRELIC=yes foreman start
