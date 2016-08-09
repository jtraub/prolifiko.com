#!/bin/bash

export $(heroku config -s | xargs)

foreman start
