#!/bin/bash

export $(heroku config -s | xargs)

gunicorn prolifiko.wsgi --log-file=-
