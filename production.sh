#!/bin/bash

export $(heroku config -s | xargs)

LOCAL=True foreman start web
